#!/usr/bin/env python3
"""Checks UC07 Interaction 6 (Patient Access, CARIN Blue Button 2.2.0).

    python3 check_interaction_06.py [--c4bb hl7.fhir.us.carin-bb-2.2.0.tgz]

Offline checks (always): every JSON file parses and has the expected resourceType; local references resolve; ids are unique and
do not collide with any other UC07 fixture; the bundle is a transaction of PUTs that match the files exactly; every match key in
crosswalk.json really is present on BOTH sides; the money adds up; dates agree with the provider-side data; the payer's online
member ID appears only on the payer side.

Profile-structure checks (with --c4bb): required elements, required slices, fixed patterns and enumerated required bindings, read
from the published package (https://packages.simplifier.net/hl7.fhir.us.carin-bb/2.2.0). THIS IS NOT THE FHIR VALIDATOR: it does
not check invariants, FHIRPath, external terminologies (CDT, ICD-10, place of service, ADA tooth codes) or US Core. Run the HL7
validator against the 2.2.0 and US Core 6.1.0 packages for that.

Exit code 0 = every check passed, 1 = a check failed.
"""
import argparse
import json
import re
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
UC = HERE.parent.parent  # .../uc07-pediatric-rootcanal
ROOT = UC.parent.parent  # .../fhir-resources
failures: list[str] = []
passed = 0


def ok(cond, msg):
    global passed
    if cond:
        passed += 1
    else:
        failures.append(msg)
        print("FAIL:", msg)


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def walk_refs(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "reference" and isinstance(v, str):
                out.append(v)
            else:
                walk_refs(v, out)
    elif isinstance(o, list):
        for x in o:
            walk_refs(x, out)


def idents(res):
    return {(i.get("system"), i.get("value")) for i in res.get("identifier", [])}


# ---- load -----------------------------------------------------------------------------------------------------------
files = sorted(p for p in HERE.glob("*.json") if p.name not in ("interaction-06-bundle.json", "crosswalk.json"))
res = {}
for p in files:
    try:
        r = load(p)
    except ValueError as e:
        ok(False, f"{p.name} does not parse: {e}")
        continue
    res[f"{r.get('resourceType')}/{r.get('id')}"] = r
ok(len(res) == 9, f"expected 9 payer-side resources, found {len(res)}")
bundle, cw = load(HERE / "interaction-06-bundle.json"), load(HERE / "crosswalk.json")

# ---- provider-side resources, by reference --------------------------------------------------------------------------
provider = {}
for p in list(UC.glob("base/*/*.json")) + list(UC.glob("interactions/interaction-0[124]/*.json")) + list((ROOT / "durable").glob("*/*.json")):
    try:
        r = load(p)
    except ValueError:
        continue
    if isinstance(r, dict) and "resourceType" in r and "id" in r and r["resourceType"] != "Bundle":
        provider[f"{r['resourceType']}/{r['id']}"] = r

# ---- 1. files, references, ids --------------------------------------------------------------------------------------
for ref, r in res.items():
    ok(ref.split("/")[0] == r["resourceType"] and r["id"].endswith(("-payer", "-c4bb")), f"{ref}: id should end in -payer (or -c4bb for an EOB)")
    ok(ref not in provider, f"{ref}: collides with an existing UC07 fixture id")
refs = []
for r in res.values():
    walk_refs(r, refs)
for ref in set(refs):
    ok(ref in res, f"dangling reference: {ref}")

# ---- 2. bundle ------------------------------------------------------------------------------------------------------
ok(bundle.get("type") == "transaction", "bundle is not a transaction")
entries = bundle.get("entry", [])
ok(len(entries) == len(res), f"bundle has {len(entries)} entries, folder has {len(res)} resources")
urls, fulls = set(), set()
for e in entries:
    r = e["resource"]
    key = f"{r['resourceType']}/{r['id']}"
    ok(e["request"]["method"] == "PUT" and e["request"]["url"] == key, f"bundle entry {key}: request must be PUT {key}")
    ok(res.get(key) == r, f"bundle entry {key} differs from its file")
    urls.add(key)
    fulls.add(e.get("fullUrl"))
ok(len(fulls) == len(entries), "bundle fullUrls must be unique")
# Relative references resolve against the fullUrl of the entry that holds them, so every fullUrl must be an absolute
# "<base>/<Type>/<id>" on one base; urn:uuid full URLs cannot resolve relative references (the profile invariants use resolve()).
bases = {e["fullUrl"].rsplit(f"/{e['resource']['resourceType']}/", 1)[0] for e in entries if f"/{e['resource']['resourceType']}/{e['resource']['id']}" in str(e.get("fullUrl"))}
ok(len(bases) == 1 and all(str(e.get("fullUrl")).startswith("http") and str(e["fullUrl"]).endswith(f"/{e['resource']['resourceType']}/{e['resource']['id']}") for e in entries),
   "bundle fullUrls must be absolute http(s) URLs of the form <one base>/<Type>/<id>, so relative references resolve")

# ---- 2b. the published profiles' own ERROR invariants, written out (they are FHIRPath in the package) --------------------
def npi_luhn(n):
    s, tot = "80840" + n, 0
    for i, ch in enumerate(reversed(s)):
        d = int(ch) * (2 if i % 2 else 1)
        tot += d - 9 if d > 9 else d
    return tot % 10 == 0


for key, r in res.items():
    ok(bool(r.get("meta", {}).get("lastUpdated")), f"{key}: meta.lastUpdated is required (uncontained-requires-lastUpdated)")
    ok(any(p.startswith("http://hl7.org/fhir/us/carin-bb/StructureDefinition/") and p.endswith("|2.2.0") for p in r["meta"]["profile"]), f"{key}: meta.profile must be a Blue Button profile pinned to |2.2.0")
    for i in r.get("identifier", []):
        if i.get("system") == "http://hl7.org/fhir/sid/us-npi":
            ok(len(i["value"]) == 10 and i["value"].isdigit() and npi_luhn(i["value"]), f"{key}: NPI {i['value']} must be 10 digits with a valid check digit (us-core-16, us-core-17)")
    if key.startswith("Practitioner/"):
        ok(any(i.get("system") in ("http://hl7.org/fhir/sid/us-npi", "urn:oid:2.16.840.1.113883.4.4") for i in r["identifier"]), f"{key}: Practitioner.identifier must include an NPI or a Tax ID")
    if key.startswith("Patient/"):
        ok(all(n.get("family") or n.get("given") for n in r["name"]), f"{key}: every name needs a family or given name (us-core-6)")
    if key.startswith("Coverage/"):
        ok(bool(r.get("subscriberId")) or any(c.get("code") == "MB" for i in r.get("identifier", []) for c in i.get("type", {}).get("coding", [])), f"{key}: member ID required (us-core-15)")
    if key.startswith("ExplanationOfBenefit/"):
        ok(sum(1 for x in r["insurance"] if x.get("focal")) < 2, f"{key}: at most one insurance with focal = true")
        for c in r["careTeam"]:
            if c["role"]["coding"][0]["code"] in ("rendering", "primary", "referring", "supervisor"):
                ok(c["provider"]["reference"].startswith("Practitioner/"), f"{key}: care team role {c['role']['coding'][0]['code']} must refer to a Practitioner")
        ok(not any(c["code"] == "other" for c in r["payee"]["type"]["coding"]) or "party" in r["payee"], f"{key}: payee type other needs a party")
        ok(r["provider"]["reference"].startswith("Practitioner/"), f"{key}: provider must be a Practitioner (C4BB-Practitioner)")

# ---- 3. crosswalk: every key present on both sides ------------------------------------------------------------------
covered = set()
for row in cw["resources"]:
    pv, py = provider.get(row["provider"]), res.get(row["payer"])
    ok(pv is not None, f"crosswalk: provider {row['provider']} not found")
    ok(py is not None, f"crosswalk: payer {row['payer']} not found")
    if pv is None or py is None:
        continue
    covered.add(row["payer"])
    for m in row["matchOn"]:
        if "identifier" in m:
            k = (m["identifier"]["system"], m["identifier"]["value"])
            ok(k in idents(pv), f"{row['provider']} lacks identifier {k}")
            ok(k in idents(py), f"{row['payer']} lacks identifier {k}")
        if "subscriberId" in m:
            ok(pv.get("subscriberId") == py.get("subscriberId") == m["subscriberId"], f"subscriberId differs for {row['payer']}")
    if row["payer"].startswith("Patient/"):
        ok(py.get("birthDate") == pv.get("birthDate") and py.get("name") == pv.get("name") and py.get("gender") == pv.get("gender"),
           "payer Patient name/gender/birthDate differ from the provider-side Patient")
ok(covered == {k for k in res if not k.startswith("ExplanationOfBenefit/")}, "every payer-side non-EOB resource must appear once in the crosswalk")

# prior authorization
pa = cw["priorAuthorization"]
cr = provider[pa["providerClaimResponse"]]
eob_r = res[pa["payerEob"]]
ok(cr["preAuthRef"] == pa["matchOn"]["value"] and pa["matchOn"]["value"] in eob_r["insurance"][0].get("preAuthRef", []), "prior authorization number differs between ClaimResponse and EOB")

# services: each EOB item is matched by CDT + date + tooth + rendering NPI
seen = set()
for s in cw["services"]:
    eob = res[s["payerEob"]]
    item = next(i for i in eob["item"] if i["sequence"] == s["payerItemSequence"])
    pr = provider[s["providerProcedure"]]
    m = s["matchOn"]
    seen.add((s["payerEob"], s["payerItemSequence"]))
    ok(item["productOrService"]["coding"][0]["code"] == m["cdtCode"] == pr["code"]["coding"][0]["code"], f"CDT code mismatch for {s['providerProcedure']}")
    pdate = (pr.get("performedDateTime") or "")[:10] or pr["performedPeriod"]["start"][:10]
    ok(item["servicedDate"] == m["serviceDate"] == pdate, f"service date mismatch for {s['providerProcedure']}")
    tooth_p = pr["bodySite"][0]["coding"][0]["code"] if pr.get("bodySite") else None
    tooth_e = item["bodySite"]["coding"][0]["code"] if item.get("bodySite") else None
    ok(tooth_e == m["toothDesignation"] == tooth_p, f"tooth mismatch for {s['providerProcedure']}")
    rend = next(c for c in eob["careTeam"] if c["role"]["coding"][0]["code"] == "rendering")
    npi = {i["value"] for i in res[rend["provider"]["reference"]]["identifier"] if i.get("system") == "http://hl7.org/fhir/sid/us-npi"}
    ok(m["renderingNpi"] in npi, f"rendering NPI mismatch for {s['providerProcedure']}")
ok(seen == {(k, i["sequence"]) for k, e in res.items() if k.startswith("ExplanationOfBenefit/") for i in e["item"]}, "every EOB line must be matched exactly once in the crosswalk")

# ---- 4. patient-app entry: the online member ID is payer-side only --------------------------------------------------
oid = cw["patientAppEntry"]["onlineMemberId"]
k = (oid["system"], oid["value"])
ok(k in idents(res[cw["patientAppEntry"]["returns"]]), "online member ID missing from the payer Patient")
ok(sum(1 for r in res.values() if k in idents(r)) == 1, "online member ID must appear on exactly one payer-side resource")
ok(all(k not in idents(r) for r in provider.values()), "online member ID must not appear on any provider-side resource")

# ---- 5. money and dates ---------------------------------------------------------------------------------------------
def amt(lst, code):
    return [a["amount"]["value"] for a in lst if a["category"]["coding"][0]["code"] == code]


for key, e in res.items():
    if not key.startswith("ExplanationOfBenefit/"):
        continue
    sub = sum(sum(amt(i["adjudication"], "submitted")) for i in e["item"])
    ben = sum(sum(amt(i["adjudication"], "benefit")) for i in e["item"])
    tot = e["total"]
    ok(sum(amt(tot, "submitted")) == sub, f"{key}: total submitted != sum of lines")
    ok(sum(amt(tot, "benefit")) == ben, f"{key}: total benefit != sum of lines")
    ok(sum(amt(tot, "discount")) == sub - ben, f"{key}: discount != submitted - benefit")
    ok(sum(amt(tot, "paidtoprovider")) == ben == e["payment"]["amount"]["value"], f"{key}: paid to provider must equal the benefit amount and the payment")
    ok(sum(amt(tot, "memberliability")) == 0 and all(sum(amt(i["adjudication"], "memberliability")) == 0 for i in e["item"]), f"{key}: Medicaid member liability must be 0")
    ok(any("SYNTHETIC" in n["text"] for n in e.get("processNote", [])), f"{key}: must carry the SYNTHETIC amounts note")
    recv = next(s["timingDate"] for s in e["supportingInfo"] if s["category"]["coding"][0]["code"] == "clmrecvddate")
    ok(e["billablePeriod"]["start"] < recv < e["created"][:10] <= e["meta"]["lastUpdated"][:10], f"{key}: dates must run service < claim received < created <= last updated")
    ok(e["billablePeriod"]["start"] == e["item"][0]["servicedDate"], f"{key}: billablePeriod must equal the service date")

# ---- 6. profile structure against the published package (optional) --------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("--c4bb", help="path to hl7.fhir.us.carin-bb-2.2.0.tgz")
args = ap.parse_args()
unverifiable: set[str] = set()
if args.c4bb:
    tg = tarfile.open(args.c4bb)
    pkg = json.load(tg.extractfile("package/package.json"))
    ok(pkg.get("version") == "2.2.0", f"package is {pkg.get('version')}, expected 2.2.0")

    def sd(name):
        return json.load(tg.extractfile(f"package/StructureDefinition-{name}.json"))

    def vs_codes(name):
        d = json.load(tg.extractfile(f"package/ValueSet-{name}.json"))
        out = set()
        for inc in d["compose"]["include"]:
            if inc.get("concept"):
                out |= {(inc["system"], c["code"]) for c in inc["concept"]}
            else:
                unverifiable.add(f"{name}: whole system {inc['system']}")
                return None
        return out

    def resolve(parents, name):
        out = []
        for p in parents:
            v = p.get(name) if isinstance(p, dict) else None
            out += v if isinstance(v, list) else ([v] if v is not None else [])
        return out

    def present(parent, last):
        if last.endswith("[x]"):
            b = last[:-3]
            return any(k.startswith(b) and len(k) > len(b) and k[len(b)].isupper() for k in parent)
        v = parent.get(last)
        return v not in (None, "", [], {})

    for key, r in res.items():
        prof = next((p for p in r.get("meta", {}).get("profile", []) if "carin-bb" in p), None)
        if not prof:
            continue
        name, _, ver = prof.partition("|")
        ok(ver == "2.2.0", f"{key}: profile must be pinned to |2.2.0")
        d = sd(name.rsplit("/", 1)[1])
        for el in d["snapshot"]["element"]:
            eid = el["id"]
            parts = eid.split(".")[1:]
            if el.get("min", 0) < 1 or ":" in eid or not parts or len(parts) > 4 or parts[-1] in ("id", "extension", "modifierExtension"):
                continue
            parents = [r]
            for seg in parts[:-1]:
                parents = resolve(parents, seg)
            for par in parents:
                ok(present(par, parts[-1]), f"{key}: missing required element {eid}")
            for k in el:
                if k.startswith("pattern") and k[7:] in ("CodeableConcept", "Code") and len(parts) == 1:
                    want = el[k]
                    got = r.get(parts[0])
                    if k == "patternCode":
                        ok(got == want, f"{key}: {eid} must be {want}")
                    else:
                        ok(any(all(c.get(x) == y for x, y in w.items()) for w in want["coding"] for c in (got or {}).get("coding", [])), f"{key}: {eid} must match pattern {json.dumps(want)[:90]}")
        # required slices, by their discriminator code
        def has(lst, code):
            return any(c.get("code") == code for a in lst for c in a.get("category", a.get("type", {})).get("coding", []))

        if key.startswith("ExplanationOfBenefit/"):
            ok(has(r["identifier"], "uc"), f"{key}: identifier:uniqueclaimid (type uc) missing")
            for code in ("renderingnetworkstatus", "benefitpaymentstatus"):
                ok(has(r["adjudication"], code), f"{key}: adjudication:{code} missing")
            for i in r["item"]:
                ok(has(i["adjudication"], "benefitpaymentstatus"), f"{key} item {i['sequence']}: item.adjudication:benefitpaymentstatus missing")
                ok(any(a["category"]["coding"][0]["code"] in ("submitted", "benefit", "copay", "eligible", "deductible", "coinsurance", "noncovered", "priorpayerpaid", "paidtopatient", "paidtoprovider", "memberliability", "discount") for a in i["adjudication"]), f"{key} item {i['sequence']}: no adjudication amount type")
            # required bindings with enumerated value sets
            def chk(vs, values, path):
                allowed = vs_codes(vs)
                if allowed is None:
                    return
                for v in values:
                    ok(any((c["system"], c["code"]) in allowed for c in v.get("coding", [])), f"{key}: {path} has a code outside {vs}")
            chk("C4BBClaimProfessionalAndNonClinicianCareTeamRole", [c["role"] for c in r["careTeam"]], "careTeam.role")
            chk("C4BBClaimProfessionalAndNonClinicianDiagnosisType", [t for dg in r["diagnosis"] for t in dg["type"]], "diagnosis.type")
            chk("C4BBPayeeType", [r["payee"]["type"]], "payee.type")
            chk("C4BBPayerClaimPaymentStatusCode", [r["payment"]["type"]], "payment.type")
            for a in r["adjudication"] + [a for i in r["item"] for a in i["adjudication"]]:
                if "reason" in a:
                    chk("C4BBPayerBenefitPaymentStatus", [a["reason"]], "adjudication.reason")
            amount_cats = [a["category"] for i in r["item"] for a in i["adjudication"] if "amount" in a] + [t["category"] for t in r["total"]]
            chk("C4BBAdjudication", amount_cats, "adjudication/total category")
        elif key.startswith("Patient/"):
            ok(any(c.get("code") == "MB" for i in r["identifier"] for c in i.get("type", {}).get("coding", [])), f"{key}: identifier:memberid (type MB) missing")
    print(f"profile-structure checks used {tg.name}; bindings not verifiable here: {len(unverifiable)} ({', '.join(sorted(unverifiable)[:3])}...)" if unverifiable else f"profile-structure checks used {tg.name}")
else:
    print("(profile-structure checks skipped: pass --c4bb hl7.fhir.us.carin-bb-2.2.0.tgz)")

print(f"\n{passed} checks passed, {len(failures)} failed.")
sys.exit(1 if failures else 0)
