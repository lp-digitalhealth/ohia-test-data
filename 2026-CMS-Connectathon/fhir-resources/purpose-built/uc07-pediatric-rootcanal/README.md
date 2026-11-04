# UC07 FHIR test data — DentaQuest Texas: root canal, build-up and crown (Joe Castle)

**Status: DRAFT, November connectathon. Interaction 1 (I1) only.** I2 and I4 are next; I3 and I5 are deferred (owner decision). This file describes what is actually committed here. It replaces nothing: `../../../use-cases/UC07-Texas-Medicaid-Pediatric-RootCanal/README-fhir.md` describes a 71-file set that is **not** this folder and is not on any branch of this repository.

Narrative: [`UC07-Texas-Medicaid-Pediatric-RootCanal.md`](../../../use-cases/UC07-Texas-Medicaid-Pediatric-RootCanal/UC07-Texas-Medicaid-Pediatric-RootCanal.md). Test-server roles for the event: section 8 of [`UC07-companion-guide.md`](../../../use-cases/UC07-Texas-Medicaid-Pediatric-RootCanal/UC07-companion-guide.md).

## What is here

| Tier | Location | Files |
|---|---|---:|
| Durable (new, UC07) | `../../durable/` | 10: three organizations, two locations, two practitioners, three endpoints |
| Base | `base/` | 5: `Patient`, `RelatedPerson`, `Coverage`, two `PractitionerRole` |
| Interaction 1 | `interactions/interaction-01/` | 22 resources + `interaction-01-bundle.json` + 2 placeholder image payloads in `arex-payloads/` |

The new durable files are `org-pediatric-dental-tx`, `org-restorative-dental-tx`, `org-dentaquest-tx`, `loc-pediatric-dental-tx`, `loc-restorative-dental-tx`, `pract-mary-parker`, `pract-max-garcia`, `endpoint-pediatric-fhir`, `endpoint-restorative-fhir`, `endpoint-dentaquest-tx`. They are **new records** and no existing durable file was edited: UC02a already has a `pract-parker` (a different clinician, NPI and practice) and an `org-dentaquest` (different endpoint and identifiers).

## I1 content (what the narrative's first interaction needs)

Evaluation record (`encounter-eval`, two diagnoses for tooth #4, two uncoded findings), two radiographs as `ImagingStudy` pointers with CDT-coded `DiagnosticReport`s, clinical notes and treatment plan, three CDT procedures (D0140, D0220, D0270), the referral `ServiceRequest` (`ode-dental-to-dental-referral`), the provider-to-payer `Communication`, the single referral `Task`, a `Provenance`, and an ARex manifest of the two image entries (see below).

## Radiographs: ARex manifest plus `ImagingStudy` pointer

Owner decisions for this event: radiographs are **an ARex manifest of image entries plus an `ImagingStudy` pointer**; WADO-RS is deferred.

- `arex-manifest-radiographs` is a `List` (profile `arex-manifest`) listing `arex-entry-periapical` and `arex-entry-bitewing` (`DocumentReference`, profile `arex-content-entry`). Each entry has an absolute `url`, a `size`, and a SHA-256 `arex-digest` computed over the file in `arex-payloads/`. No inline data.
- **Link convention (decided, not an ARex rule):** each `ImagingStudy.identifier` repeats the manifest's transaction-context `businessIdentifier` (`urn:ohia:referral-id|REF-2026-UC07-001`). A consumer finds the manifest with ARex's `transaction-identifier` search parameter. ARex v0.2.0 does not define any `ImagingStudy` link.
- The payload files are **8x8 placeholder PNGs, not radiographs**. The URLs are synthetic `example.org` addresses; for a live retrieval test the files must be served by an ARex content server.
- `arex-provenance-radiographs` carries a **placeholder signature**: the ARex Provenance profile requires `signature` (min 1), but a valid detached JWS cannot be committed here. `signature.data` is not a valid JWS and must be regenerated at test time.

## Bundle semantics (CLAUDE.md section 6)

`interaction-01-bundle.json` is a **transaction** Bundle, **cumulative** (the 10 UC07 durable files + base + I1), every entry a `PUT` to `ResourceType/id`, so loading is **idempotent**. It assumes an empty or reset server (do not load it beside UC02a in one unpartitioned server, per the repository's isolation rule). `fullUrl`s are valid lowercase UUIDs (v5, deterministic); references inside resources stay relative (`Type/id`). It does **not** include external services: the ARex content server, the payer CRD/DTR/PAS endpoints, or any X12 clearinghouse.

## Values not in the narrative (ASSUMPTIONS)

- Referral identifier `REF-2026-UC07-001` (the narrative names none).
- Referral `authoredOn` 10:15 (the narrative's transmission time) and notification 10:16; evaluation start 09:30; no encounter end time.
- ARex manifest expiry (14 days after publication, borrowed from the I2 window) and manifest identifier `MAN-2026-0708-0001`.
- Coverage `class` value `TX-MEDICAID-DENTAL`.
- No practice street addresses (the narrative gives none).
- DICOM UIDs are synthetic `2.25.*` values; no DICOM objects exist.

## Modeling choices to confirm

- **Referral code:** the first requested service (D3320) is in `ServiceRequest.code`; D2950 and D2740 are in `orderDetail`. One `ServiceRequest` carries the three-procedure plan, as the narrative describes.
- **ICD-10 K02.53** for the caries finding is as written in the narrative; the project notes it needs a dentist's confirmation (K02.63 may fit better).
- **Tooth code:** ADA Universal `4`, displayed as "Permanent maxillary right second premolar tooth" (the display the terminology requires, per the HL7 validator; UC02a's files display the bare number, and those files were not validated here).
- **Guardian:** `RelatedPerson.relationship` carries v3-RoleCode `MTH` and `GUARD`.
- **Single `Task`**, per CLAUDE.md section 7; `owner` is not set at I1.
- **DiagnosticReport** is coded with CDT (D0220, D0270), not LOINC, per the narrative.

## Notes moved out of resources

R4 `Organization` and `Coverage` have no `note` element, so these were removed from the resources and are recorded here:

- **`Organization/org-pediatric-dental-tx`** — UC07 referring practice (Dr. Mary Parker). Fictional practice; NPI is synthetic (UC07 narrative, Appendix A). Street address is not given in the narrative and is intentionally omitted.
- **`Organization/org-restorative-dental-tx`** — UC07 receiving practice (Dr. Max Garcia). Fictional practice; NPI is synthetic (UC07 narrative, Appendix A). Street address is not given in the narrative and is intentionally omitted.
- **`Organization/org-dentaquest-tx`** — UC07 payer. Real organization used as the payer identity; one of the Texas HHSC-contracted dental plans. Payer ID CX014 is the clearinghouse routing ID per the UC07 narrative. A payer carries no NPI. The endpoint is synthetic. This is a NEW record, separate from the existing org-dentaquest (UC02a), so UC02a's file is not edited; consolidating the two is a follow-up.
- **`Coverage/coverage-joe-castle-dentaquest`** — Medicaid (not CHIP); Texas Health Steps (EPSDT) eligible. Coverage period 2026-01-01 to 2026-12-31, status active (UC07 narrative). The class value TX-MEDICAID-DENTAL is an ASSUMPTION: the narrative gives no plan identifier.

## Validation (what was run, and what was not)

- **Structural checks** (author's script, not committed): all files parse; file name equals `id`; no duplicate logical ids; every local reference resolves; Bundle entries are `PUT` with matching URLs; entry count recomputed (37); NPIs pass the Luhn check; ARex digests and sizes match the payload files; each `ImagingStudy.identifier` matches the manifest's business identifier. All passed.
- **HL7 FHIR Validator** (R4 4.0.1, `hl7.fhir.us.core#6.1.0`, the ARex profiles from the IG, terminology **off**, `-allow-example-urls true` because this data is synthetic by design): **0 errors, 169 warnings, 18 information messages.**
- **What the warnings are:** best-practice notes (relative references versus the UUID `fullUrl`s; resources without narrative); code systems that could not be checked with terminology off (including CDT, NUCC taxonomy and BCP-47); two ARex content URLs the validator could not fetch (synthetic hosts).
- **NOT validated:** the **ODE profiles** (`ode-dental-to-dental-referral`, `ode-referral-task`) — the validator could not find them, so the referral and the Task were checked against the base resources only; the ODE profile source is unbuilt FSH. **CDT, NUCC and BCP-47 codes** were not checked. **Clinical correctness** was not assessed.
- `fullUrl` form: UC04a's bundle uses `urn:uuid:Type-id`, the same form the validator rejected as "not a valid UUID" in this folder's first draft. Other bundles were not validated here. UC07 uses valid UUIDs.
