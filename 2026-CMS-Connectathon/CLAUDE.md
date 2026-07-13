# CLAUDE.md — OHIA CMS Connectathon Test Data

**Doc version:** 4.7
**Last updated:** 2026-07-13 (by: claude.ai chat)
**Repo:** `lp-digitalhealth/ohia-test-data`, folder `2026-CMS-Connectathon/`

> This file is the single source of truth for this project's decisions, structure, and state. It lives in the repo, not in any one chat. Whoever works on this project next — claude.ai chat or Claude Code — reads this file first, and updates it (including the Session Log at the bottom) before finishing a session.
>
> **Where we actually are:** UC01's test data is organized around **4 key interactions** (not the 7 clinical encounters — see Section 3 for why). **Interaction 1 is built.** Interactions 2–4 are still in design. Most of the project's real decisions — the remaining 3 interactions, and all of UC02–05 — have not been made yet. This is early-stage design work, not an execution backlog. Don't let Claude Code batch-generate interactions or use cases from pattern-matching alone; each needs the same design discussion Interaction 1 got. **[Note: this specific paragraph is stale as of v4.1 — UC01 now has 5 interactions built/designed and UC02 work is well underway. Left as-is pending a dedicated cleanup pass; don't treat it as current status.]**
>
> **Standing instruction (added v4.1, updated v4.2, applies to all future dental use cases, not just UC02):** this project is fundamentally about **dental** interoperability — FHIR-based clinical data exchange, with a genuinely heavy emphasis on **imaging exchange via CDex**. Don't let imaging (`ImagingStudy`, `DocumentReference` for radiographs/periodontal charting/intraoral images) ride along as an afterthought bundled inside "the referral package" — it deserves to be modeled as its own real, tested pattern. Critically, **the imaging transport mechanism is direction-dependent and already established, don't re-derive it each time**: dental-to-dental referrals (UC02 and beyond) use **support-a-pull** (receiver retrieves via CDex); referrals where either side is medical (UC01) use a **separate push** (`DocumentReference/$submit-attachment`), since the medical side exposes no inbound pull. Check which direction applies before building imaging resources for any new use case — don't assume UC01's push pattern is the default.
>
> **DICOM is also standing infrastructure here, not optional detail — confirmed directly against HL7's own ImagingStudy spec, not assumed.** FHIR's `ImagingStudy` resource does **not** contain the actual image — it's a metadata/pointer layer only, referencing DICOM Study/Series/SOP Instance UIDs. The real pixel data lives in DICOM format on a PACS (or DICOMweb server), and actual retrieval happens via **WADO-RS** (a DICOMweb REST API — `ImagingStudy.endpoint` typically points at a WADO-RS base URL). So the accurate technical stack for any dental imaging exchange in this project is: **CDex** (the Da Vinci-governed clinical exchange pattern, push or pull per direction) → **`ImagingStudy`** (the FHIR-side pointer/metadata) → **DICOM/WADO-RS** (the actual image standard and retrieval mechanism). All three should be named explicitly when imaging is discussed — not simplified down to "CDex pulls the image," which skips the layer that actually matters for real implementers.

---

## 1. What this project is

Loadable FHIR test data + supporting artifacts for the OHIA (Oral Health Interoperability Alliance) CMS Connectathon, so participating firms can read a use case, pick which interaction(s) to test, and load exactly what they need. UC01 (Medical-to-Dental Referral, Head & Neck Cancer, patient John Smith) is the model use case.

**Repo caveat:** this GitHub repo also contains a separate, pre-existing, unrelated dataset at `2026-usrealm-testdata/` (different patients — Emily Watkins, Jason Morales, Laura Jennings; different payers — Delta Dental/Cigna Dental/Anthem BCBS of Kentucky). Not part of this project.

---

## 2. Repository structure

```
2026-CMS-Connectathon/
├── CLAUDE.md              This file.
├── use-cases/             Clinician-readable narrative docs — no FHIR jargon.
│                          Per use case, the clinical story is documented as
│                          numbered ENCOUNTERS (the real clinical visits), but
│                          test data is organized by INTERACTION (see below).
├── fhir-resources/        Loadable FHIR R4 JSON — the actual test data,
│                          organized by interaction, not 1:1 by encounter.
├── hl7v2/                 Sample HL7 v2 wire-level messages, same interaction
│                          organization.
└── companion-guides/      Prep guidance + readiness checklists per use case.
```

**Note on cross-repo feedback:** proposed changes to repos we don't control (e.g. `ode-360x-adapter`, `ohia-fhirr4-scratchpad`) do NOT live in this repo — they belong with the repo they're proposing changes to, and are delivered/tracked separately (see Section 5a for the current one). Don't add an `external-proposals/`-style folder back into this repo structure; keep this repo scoped to Connectathon test data only.

**Encounter vs. Interaction — two different organizing concepts, don't conflate them:**
- **Encounter** = a real clinical visit in the narrative (UC01 has 7, enumerated in `use-cases/.../UC01-Medical-to-Dental-Tongue-Cancer.md` Appendix Section 0). This is the clinical *story*.
- **Interaction** = a specific integration point worth building test data for (UC01 has 4 — see Section 3). Most clinical encounters (e.g., the tooth extractions) are "business as usual" and don't get their own modeled resources; an interaction may correspond to one encounter, or span/skip across several. This is what actually gets built as `fhir-resources/`/`hl7v2/` content.

**Design principle:** `use-cases/` explains the clinical story to a clinician; `fhir-resources/`+`hl7v2/` are the complete parts inventory for engineers, organized by interaction; `companion-guides/` ties the two together with concrete prep instructions — without over-prescribing internal implementation. One combined guide per use case (not separate guides per role).

### FHIR resource tiers (settled — don't re-litigate without a real reason)

| Tier | Location | Contents | Reusable across use cases? |
|---|---|---|---|
| **Registry** | `fhir-resources/common/` | Organization, Practitioner, Location, InsurancePlan, Endpoint, payer CRD/DTR rules (PlanDefinition/Library/Questionnaire) | Yes — tied to the real-world institution/clinician/plan, not the story |
| **Use-case base** | `fhir-resources/uc01-.../base/` | Patient, Coverage, Consent, **PractitionerRole** | No — specific to this patient's episode. PractitionerRole is deliberately NOT in the registry: the role *pairing* (clinician+org+specialty+location) can vary by use case even when the underlying Practitioner doesn't |
| **Per-interaction** | `fhir-resources/uc01-.../interactions/interaction-0N/` | Encounter, Condition, ServiceRequest, Task, Provenance, etc. | No — tied to that specific interaction in the story |

---

## 3. UC01: 7 clinical encounters (clinical reference, unchanged) → 4 test interactions (what actually gets built)

**Why the reframe:** the purpose of this project is to test integrations, not to model every clinical visit. Most of UC01's clinical narrative (e.g., the three tooth extractions) is "business as usual" and doesn't need its own FHIR resources. The 7-encounter clinical enumeration below is still the accurate clinical story and stays in the use case doc unchanged — but test data is built around 4 key interactions instead.

### 7 clinical encounters (unchanged, clinical reference only)

| # | Date | Encounter |
|---|---|---|
| 1 | 2026-07-06 | Oncology visit — IMRT order & referral |
| 2 | 2026-07-23 | Dental exam & radiographs |
| 3 | 2026-07-27 | Extraction #4 |
| 4 | 2026-07-28 | Extraction #17 |
| 5 | 2026-07-29 | Extraction #30 + implant placement |
| 6 | 2026-07-31 | Dental clearance visit |
| 7 | 2026-08-24 | Revised IMRT start |

Full breakdown and the 6-vs-7 decision reasoning: `use-cases/UC01-medical-to-dental-tongue-cancer/UC01-Medical-to-Dental-Tongue-Cancer.md`, Appendix Section 0.

### 4 test interactions (what gets built as fhir-resources/hl7v2) — now 3, see fold decision below

| # | Corresponds to encounter(s) | Interaction | Status |
|---|---|---|---|
| 1 | Encounter #1 | Request for radiation + payer indication that dental clearance is required + initial referral | ✅ Built + verified |
| 2 | Encounter #2 + a later ~early-August moment | Request for additional information — now covers BOTH the DDC dose inquiry (07-23) AND the treatment extension request (~08-03–08-10) | ✅ FHIR resources built (DDC portion only — see gaps below); use-case writeup built (both parts) |
| ~~3~~ | ~~Between encounters #5–7~~ | ~~Communication of final treatment plan + extension request~~ — **folded into Interaction 2** (see below) | N/A |
| 3 (renumbered) | Encounter #6 | **The Clearance** — Dr. Bellweather's structured dental clearance transmitted to FCCC, closing the referral loop and satisfying the payer's documentation requirement | ✅ Built + QA'd |
| 4 | Related to encounter #1's CRD/DTR pathway | Packaging treatment for submission to medical payer (PA Claim/ClaimResponse) | ✅ Built |

**Fold decision (this session):** the extension request (Dr. Bellweather/Penn Dental telling Dr. Whitfield the radiation start needs to move from 2026-08-10 to 2026-08-24, due to extraction/implant healing time) is modeled using the **identical mechanism** as the DDC dose inquiry — an informal note, per the base COW "Requesting additional information" pattern — even though it happens at a different point in the clinical timeline (after clearance/PA approval, not during the dental exam). Since both are the same pattern, Interaction 3 was folded into Interaction 2 rather than kept as a separate interaction. The use-case writeup (`uc01-i2-dental-exam-open-questions.md`) now covers both; **the FHIR resources for the extension-request portion are not yet built** — only the DDC dose inquiry's resources exist so far (Encounter, 2 DiagnosticReports, Observation).

**Known gaps in Interaction 2, not yet fixed:**
- The Task transition to `in-progress` (with the businessStatus update, communicated back to the EHR through the bridge) **before** the dental exam happens — flagged, not yet built. This should be the actual first step of Interaction 2, and is currently missing.
- No FHIR resources yet for the extension-request half of Interaction 2 (the note itself, and whatever formally captures the revised IMRT start date — likely an update to `ServiceRequest/servicerequest-imrt-order`'s `occurrenceDateTime`, not yet done).
- No companion guide content for Interaction 2 at all (Interaction 1 only, in `UC01-companion-guide.md`).

**Interaction 3 — "The Clearance" (Encounter #6), scoped in detail, business-terms writeup built, FHIR resources not yet built:**

What happens (business terms, full writeup in `use-cases/.../uc01-i3-the-clearance.md`): after all three teeth are addressed (#4, #17 extracted; #30 extracted + immediate implant per the dose finding from Interaction 2), Dr. Bellweather re-examines John, confirms healing, and formally documents clearance — structured data, not a PDF or fax — sent to FCCC 30 minutes later. Two independent things close at this single moment: **(1)** the referral relationship itself (Dr. Bellweather reporting back what Dr. Whitfield asked for in Interaction 1), and **(2)** the payer's specific documentation requirement (the dental-clearance prerequisite IBX flagged back in Interaction 1's CRD/DTR pathway) — same real-world event, two separate things being tracked.

**Core deliverable:** `ClinicalImpression` (Dental Clearance) — fully specified in the use case appendix already: `status` completed, `code` SNOMED 146328D, `assessor` Dr. Bellweather, `date` 2026-07-31, full summary/findings/recommendations text already written out in the source doc.

**One Task, not two — resolved this session by checking base COW directly, not just the 360X-scoped crosswalk:**

Initially thought a second, separate CDex documentation Task was needed (distinct from the 360X `ODEReferralTask`), based on the use case doc's own resource table describing "the open dental clearance documentation requirement" as if it were tracked separately. **Checked the base COW IG (`fhir-cow-ig`) directly and reversed this.** COW's own guidance: one Coordination Task per Request is the *preferred* pattern, with `Task.output` absorbing all fulfillment artifacts (the `ClinicalImpression` clearance included) and `businessStatus` progressing to reflect documentation status alongside referral status. Multiple Coordination Tasks per Request are explicitly optional in base COW, but **this project's own adopted 360X-scoped COW subset (per the `ode-360x-adapter` crosswalk) explicitly excludes "multiple Coordination Tasks per Request" and `Task.partOf` sub-tasks as out of scope** — so building a second Task would violate a scope boundary we already committed to.

**Resolved design:** the single `ODEReferralTask` (already built in Interaction 1) tracks both the referral relationship AND the payer's documentation requirement together. At Interaction 3, this same Task's `businessStatus` advances to reflect the clearance being received, and `Task.output` gains a reference to the `ClinicalImpression` once built — no second Task resource.

**Corrections made to reflect this** (this session): the use case doc's master "Key FHIR Resources Exercised" table (`Task` row) corrected to describe one Task, not two, with the COW/crosswalk citation inline. The Task resource's own `note` (`task-360x-dental-referral.json`) strengthened to explicitly state it absorbs the documentation requirement too. Also fixed, while in the doc: the "Request Treatment Delay" row was still describing a formal `Communication` resource, contradicting the note-based decision already locked in for Interaction 2 — corrected to match.

**Explicitly open, not yet decided:** how the clearance actually transmits — bare `ClinicalImpression`, wrapped in a `DocumentReference`, or a purpose-built ODE resource. This isn't us being indecisive — the use case doc itself states this is an open design question for the ODE IG (line 167 of the source doc). Worth deciding deliberately before building, and possibly worth its own entry in the ODE interface issues log if the ODE spec doesn't resolve it.

**Explicitly out of scope for Interaction 3:** the PA `Claim` submission to IBX (that's Interaction 4). Also undecided: whether individual `Procedure` resources are needed for the 3 extractions/implant, or whether narrative text within `ClinicalImpression` is sufficient — not yet decided.

---

## 4. Interaction 1 — complete (the template/pattern, not a rubber stamp for interactions 2-4)

**34 FHIR resources** in `fhir-resources/uc01-medical-to-dental/interactions/interaction-01/` (plus registry/base dependencies), cross-referenced programmatically — every identifier, date, and code checked to match exactly across resources. Filenames/resource `id`s inside this folder still say "encounter-01" in places (e.g. the `Encounter` resource itself, the bundle was renamed to `interaction-01-bundle.json`) — intentionally not renamed further, since the `Encounter` resource legitimately represents the clinical visit and touching its `id` would mean updating every cross-reference for no correctness benefit.

- Encounter, Condition (tongue cancer, ICD-10-CM C02.1)
- AllergyIntolerance (penicillin, RxNorm 7980) + 3× MedicationRequest (lisinopril, atorvastatin, oxycodone/acetaminophen) + medication List (`ODEMedicationList`)
- 2× ServiceRequest (IMRT order; dental referral, `ode-medical-to-dental-referral` profile) + Task (360X referral tracking, `ode-referral-task` profile) + Provenance
- CDS Hooks discovery config for the payer's `order-sign` service (not a FHIR resource — flagged as such in-file)
- Self-contained transaction bundle combining all of the above (`interaction-01-bundle.json`)

**1 HL7 v2 message** in `hl7v2/uc01-medical-to-dental/interaction-01/`: the PCC-55 referral request (`OMG^O19`), built field-by-field against HL7 v2.5.1, cross-verified against the FHIR resources. QA notes file documents verified-vs-illustrative parts and revision history — **read it before modifying the message.**

**1 companion checklist**: `companion-guides/UC01-readiness-checklist.md` — Interaction 1 only, broken into the two distinct technical pathways (payer coverage check vs. referral transmission). Not built for interactions 2–4. Full companion guide (Section 7c) is complete for Interaction 1.

---

## 5. Critical external dependency: `lp-digitalhealth/ode-360x-adapter`

Separate GitHub repo — reference implementation bridging IHE 360X (HL7v2/C-CDA over Direct/XDM) and "ODE Native" FHIR. Its `spec/` folder is the conformance contract. Facts below are confirmed from primary sources, not assumed:

- **Architecture**: ports-and-adapters. Three ports: `FhirBackend`, `IheCodec`, `IheOutboundTransport`. Symmetric/bidirectional — direction depends on who initiates.
- **Critical EHR/FHIR boundary**: the medical EHR (FCCC) is HL7v2 + C-CDA native for the 360X referral pathway — **no FHIR capability needed there at all**. The FHIR resources are the bridge's *output* for the dental side. FCCC's FHIR involvement is limited to the separate CRD/DTR (prior auth) pathway. (Modeled wrong initially; corrected.)
- **PCC-55 (Referral Request) = `OMG^O19`**, NOT `REF^I12` (error made and corrected). Structure: `MSH → PID → {AL1} → {ORC → OBR → {DG1}...}`. Referral ID in `ORC-2`/`OBR-2`, matching FHIR `urn:ohia:referral-id`. **No `IN1` segment** — insurance lives only in FHIR `Coverage` (caught as a regression once — watch for it).
- **`ServiceRequest`**: directional profile (`ode-medical-to-dental-referral` / `ode-dental-to-dental-referral` / `ode-dental-to-medical-referral`). ICD-10-CM `reasonCode` + `reasonReference` to Condition (both required), CPT/HCPCS `code` (CDT dropped for medical-side directions, kept dental-to-dental), `supportingInfo` → medication List + AllergyIntolerance.
- **`Task`**: profile `ode-referral-task`. `code.coding` = task-code `fulfill`. `businessStatus` from `ode-referral-sub-status` (`received`, `accepted`, `declined`, `interim-results`, `outcome-final`, `appointment-booked`...). PCC-55 intake stamps `received`. `Task.input` references the referral package.
- **`Provenance`** required in the referral bundle (from `referral_fhir.py`, not the crosswalk doc — easy to miss).
- **Transaction lifecycle**: PCC-55 (request) → PCC-56 (accept) → PCC-60 (appointment) → PCC-59 (interim note, optional) → PCC-57 (outcome, closes loop) → PCC-58 (cancel, optional) → PCC-61 (no-show, optional). Interaction 1 = PCC-55. The PCC-56/60 accept+appointment pair happens between Interaction 1 and Interaction 2 and isn't modeled as its own artifact yet. Interaction 2 deliberately does NOT map to PCC-59 (interim consultation note) — that transaction is the wrong direction (specialist reporting TO referrer; our interaction is the reverse) — see Section 3's Interaction 2 note.
- **Explicitly out of scope, don't over-build**: `Task.partOf` sub-tasks, performer reassignment/baton-passing, multiple Coordination Tasks per Request.
- **CDS Hooks**: this use case's narrative specifies `order-sign` (not `order-select` — corrected).

## 5a. Second critical external dependency: `lp-digitalhealth/ohia-fhirr4-scratchpad`

Separate repo, separate concern from `ode-360x-adapter`: this is the **ODE-native REST interface contract itself** (`interfaces/openapi.yaml`) — what a dental PMS/FHIR server should expose, independent of whether any 360X bridge exists. Confirmed via direct read: it defines `ServiceRequest` (3 directional referral profiles), `Task` (`ODEReferralTask`), `MedicationRequest`/`List` (`ODEMedicationList`), `DocumentReference` (pull/push imaging), `Subscription`, and one `POST /` for initial referral submission.

**Real gap found (not speculative) while building Interaction 2**: this interface has no path for `Encounter`, `DiagnosticReport`, or `Observation` at all, and no mechanism to add content to an already-open referral — only initial submission. It also doesn't model `Task.input`/`Task.output` in its own schema, despite the `ode-360x-adapter` crosswalk explicitly adopting both as in-scope COW elements. This means Interaction 2 (as built) **cannot currently be executed against this interface**, bridge or no bridge. Logged as **Issue 001** in the running `ODE-INTERFACE-ISSUES-LOG.md` (see below) — this is the first entry in what's expected to be an ongoing log, not a one-off.

**Standing practice, going forward:** the ODE interface is an IG under active development (a separate project is converting this OpenAPI spec into a full IG). As we build out UC01's remaining interactions and eventually UC02–05, **finding more gaps in this interface is expected, not exceptional.** Every time an interaction can't be executed against the current interface, that's a new numbered issue in the log, not a special occurrence requiring discussion about whether to log it.

**Proposed fix for Issue 001, drafted** — delivered as a **standalone package, separate from this repo** (it targets `ohia-fhirr4-scratchpad`, not `ohia-test-data`, so it doesn't belong committed here): reuses the COW pattern already defined in the crosswalk (interim content → `Task.output`) rather than inventing something new. Adds `POST/GET Encounter`, `DiagnosticReport`, `Observation`; adds `input`/`output` to the `ODEReferralTask` schema; adds a new `POST /Task/{id}/$append-interim` operation (the ODE-native equivalent of a bridge's PCC-59 handling, usable without a bridge). The "request for additional information" itself still needs no new resource — it's a `Task.note`, and `PATCH /Task/{id}` already exists in this interface.

**We have no write access to this repo either** — this is a draft to hand to its maintainers, delivered outside this repo's package so the two repos' content doesn't get mixed up. The full running log of these issues (this one plus any future ones) lives in `ODE-INTERFACE-ISSUES-LOG.md` in that same standalone package.

---

## 6. Verification discipline (an instruction — follow this, don't just read it as history)

This project has repeatedly caught real errors by checking codes/facts against actual sources instead of asserting from memory: 2 wrong SNOMED codes, a wrong NUCC taxonomy code, a wrong v3-ActCode, a wrong CDS Hooks trigger name, a wrong MSH Processing ID, a wrong HL7v2 message type entirely, a real-world credential correction (Dr. Bellweather's title/board cert, confirmed against his actual Penn Dental faculty page), an `IN1` segment regression caught via cross-check against prior QA notes, and a fabricated `Encounter.note` element (FHIR R4 `Encounter` has no `note` element at all — caught by the user's FSH validation pipeline, not by our own checks).

**Important limit on our own verification, made concrete by the `Encounter.note` case:** our JSON structural validation (`json.load()`, cross-reference checks) only catches malformed JSON and mismatched identifiers — it does NOT catch a plausible-looking but nonexistent FHIR element, since fabricated-but-well-formed JSON parses fine. **Real FHIR/FSH validation is a strictly stronger check than what we've been doing ourselves**, and should be treated as more authoritative when available. This same bug existed in both the OpenAPI schema *and* our actual built test data (`encounter-02-dental-exam.json`'s Encounter resource) — a reminder that spec-level and resource-level content need to be checked in parallel, since the same modeling error tends to appear in both.

**Rule: verify codes/facts via search before finalizing. Flag anything unverifiable as text-only/uncoded rather than guessing. Before rebuilding any file, check it against its own existing QA notes so fixes don't silently regress. When possible, prefer real FHIR/FSH structural validation over our own JSON-only checks — they catch a different, stronger class of error.**

---

## 7. Working preferences

- Markdown only; no Word/Excel/PPTX unless explicitly requested
- Companion guides/checklists: capabilities needed, not rigid implementation steps
- One thing at a time when reviewing/fixing — don't bundle multiple changes into one pass
- Source of truth is this repo — no local zip exports

## 7a. How work is split between claude.ai chat and Claude Code

This project is deliberately worked in **two modes**, and each session should know which mode it's in:

- **Design/decision mode (claude.ai chat):** working out *what* an interaction should contain, resolving ambiguity in the narrative, researching external specs, making judgment calls (like the 6-vs-7 encounter decision, the registry/base tiering split, or the encounter→interaction reframe itself). Exploratory, back-and-forth, one thing at a time.
- **Execution mode (Claude Code):** once a pattern is settled (as it now is for Interaction 1), building the actual files — FHIR JSON, HL7v2 messages, companion guide sections — against that settled pattern, with real repo/git access.

**Claude Code should not use pattern-matching from Interaction 1 to auto-generate Interactions 2–4.** Each interaction has its own clinical content, its own 360X transaction (if any — Interaction 2 explicitly has none), and its own open questions (see Section 3). Claude Code's job is to implement *decisions already made in this file*, not to make new ones by extrapolation. If Claude Code hits a genuine design gap (something not covered in this file), it should stop and flag it rather than guessing — the same verification discipline in Section 6 applies regardless of which mode is active.

**Handoff protocol:**
1. Decisions get made in chat → this file gets updated (relevant section + Session Log) → committed to the repo.
2. Claude Code reads this file at session start, executes against it, updates this file (status table + Session Log) before finishing, commits.
3. Since claude.ai chat cannot reliably read this repo directly (GitHub project-sync has not worked reliably as of this writing — confirmed via direct test), **paste the current CLAUDE.md content into the first message of a new chat session** to resume design work. If specific built files need review in chat (not just the summary), paste/attach those too.

---

## 7b. IG conformance matrix (cross-use-case, by encounter — predates the interaction reframe)

`companion-guides/stakeholder-matrix.md` — restructured (v1.2) from an earlier stakeholder-first design into an **encounter-first** conformance matrix: rows are Use Case + Encounter, columns are Implementation Guides (CRD, DTR, SMART App Launch, IHE 360X, ODE, CARIN Blue Button, Provider Access API) with a responsible-party sub-header, cells are R (required) / NR (not required) / U (unknown), last column is a plain-language description. **Note:** this matrix predates the encounter→interaction reframe (Section 3) and still uses encounter numbers as rows. It should be revisited to decide whether it should shift to interaction-based rows too, or stay encounter-based since it's a conformance/IG lens rather than a test-data-build lens — not yet decided.

Key facts this surfaced for UC01:
- **Provider Access API** (CARIN BB-based, provider-facing, out-of-band) is confirmed NOT required at Interaction 1 — needed at a later interaction, not yet pinned down which one (candidate: Interaction 3 or 4, unconfirmed).
- **"Stub" is a first-class, cross-cutting concept** — Patient App needs stubs for EHR/PMS/Payer; EHR and Dental Tech providers are sometimes the same vendor building an EHR *stub*.
- A separate **stakeholder-to-IG responsibility reference table** (who's primarily responsible for each IG, independent of any encounter/interaction) lives below the main matrix in the same file.

## 7c. Companion guide (Interaction 1 — finalized by user directly in the repo)

`companion-guides/UC01-companion-guide.md` — Interaction 1 (referred to as "Encounter #1" throughout the current text, predating the reframe) complete and user-edited directly in GitHub (not just Claude-drafted). User's edits added real value beyond the original draft: per-role "Files for this role" tables in Section 2, Stub Specifications moved to its own Section 3, and a **Section 4 Resource Index** — a complete table of every file needed, organized by tier (registry/base/encounter), with direct links. Sections numbered 0–9 consistently. **This confirms the user is now editing the repo directly — treat GitHub as authoritative over any local/chat-side copy going forward; if there's ever a conflict, ask which is newer rather than assuming chat's version wins.** **Not yet updated for interaction terminology** — still says "Encounter #1" throughout; whether/when to rename is the user's call given they're actively hand-editing this file.

---

## 8. Not yet built

- Interactions 3–4 (FHIR resources, HL7v2 samples where applicable, clinician writeups) for UC01 — **design work needed first, not just execution**
- Companion guide content for Interactions 2–4 (Interaction 1 is complete — see Section 7c)
- Interaction-level test scripts (human-readable + ideally FHIR `TestScript`)
- 360X response transactions relevant to Interaction 1's referral loop: accept (PCC-56), outcome/clearance (PCC-57), optional cancel (PCC-58) / no-show (PCC-61). Note PCC-59 (interim note) is NOT needed for Interaction 2 (wrong direction — see Section 3).
- Decision on whether `stakeholder-matrix.md` should shift to interaction-based rows (currently encounter-based, see Section 7b)
- UC02–UC05 entirely (currently placeholder/synthetic organizations and practitioners in the source use-case docs; need the same real-entity research UC01 received)

## 9. Open questions (unresolved, worth raising externally)

- Whether ODE defines its own patient-facing FHIR profile for referral/appointment status, or whether that rides on the standard Patient Access API surface.
- No discrete field for the *receiving* clinician's identity in the `OMG^O19` message structure — worked around via free text (`NTE`); worth raising to the OHIA/`ode-360x-adapter` maintainers as a possible real gap.

---

## Session Log

*Append-only. Newest entry at the top. Every session (chat or Code) adds one entry before finishing.*

### 2026-07-13 — claude.ai chat (v4.7) — Interaction filenames renamed and shortened to match new titles
Per user: filenames themselves (not just H1 titles) needed updating, and shortened where possible. Renamed all 29 interaction files to the pattern `uc0X[a/b]-iN-short-slug.md`, e.g. `uc02a-interaction-01-prior-authorization-cycle.md` → `uc02a-i1-prior-authorization-wait.md`, `uc04b-interaction-01-coverage-providersearch-assessment-referral.md` → `uc04b-i1-midnight-pain-diabetes-flag.md` — considerably shorter across the board, derived from the new narrative titles rather than the old technical ones.

Updated all 29 filename references across the four README index files, verified programmatically that every link in every README now resolves to a real file (zero broken links). Also found and fixed two stale filename references sitting in `CLAUDE.md`'s own *active* content (Section 3's Interaction 2 fold-decision note and Interaction 3 scoping note) — left the historical Session Log entries below them untouched, since those correctly describe filenames as they existed at the time each entry was written.

### 2026-07-13 — claude.ai chat (v4.6) — Interaction naming convention standardized: UC0X-IY: Descriptive Name
Per user: UC01's interaction titles ("The Clearance," "Ending the Prior Authorization") had real narrative flavor; UC02–04's were rushed, technical, resource-checklist-style titles — most damningly, "Claims-Sharing" was used as the title verbatim six separate times across different use cases with zero distinguishing flavor. Redesigned all 29 interaction titles for narrative quality matching UC01's standard, and applied a new consistent format across every file: **`UC0X-IY: Descriptive Name`** (e.g. `UC02a-I3: The Extraction`, `UC04b-I1: Midnight Pain, A Diabetes Flag`) — replacing the old inconsistent mix of "Interaction N:", "UC0Xa — Interaction N:", and "Encounter #1:" formats.

Updated all 29 interaction file H1 headers plus all 4 README index files (UC01/UC02/UC03/UC04) to reference the new titles. Full new naming table:

- UC01: I1 Request for Radiation & Referral · I2 Dental Exam & Open Questions · I3 The Clearance · I4 Ending the Prior Authorization
- UC02a: I1 The Prior Authorization Wait · I2 The Handoff to Oral Surgery · I3 The Extraction · I4 Closing the Loop · I5 Billing the Extraction
- UC02b: I1 Checking Coverage, Choosing a Path · I2 The Handoff to Oral Surgery · I3 Extraction and Implant, Same Day · I4 Closing the Loop, Implant Included · I5 Billing for Two Procedures
- UC03: I1 A Routine Checkup Finds Something Else · I2 Records Before the Visit · I3 Three Months Later · I4 Telling Both Doctors · I5 Billing Timothy's Visit
- UC04a: I1 Tuesday Night Pain · I2 An Appointment by Morning · I3 The Root Canal · I4 Reporting Back · I5 Two Bills, One Visit
- UC04b: I1 Midnight Pain, A Diabetes Flag · I2 An Appointment Within 48 Hours · I3 More Than Expected · I4 Closing the Loop, Then Checking In · I5 Billing Three Teeth

Note: file names themselves were NOT renamed (still e.g. `uc02a-interaction-01-prior-authorization-cycle.md`) — only the H1 title inside each file and the README references were updated. If file renaming is also wanted later, that's a separate, not-yet-done step.

### 2026-07-13 — claude.ai chat (v4.5) — UC03/UC04 provider grounding: researched real orgs, then pivoted to fictional per user direction
Researched and verified three real organizations matching each use case's jurisdiction/payer context (Sutton Dental Group, New Haven — confirmed Husky B acceptance directly from their own site; BLVD Dentistry & Orthodontics, Austin — confirmed Aetna acceptance; Avion Dental, San Antonio — confirmed explicit "STAR Medicaid" acceptance). **User then directed a pivot: use fictional organizations instead, at least for now** — a different call than UC02a's Austin Oral Surgery (a large, multi-location, already-OHIA-member USOSM partner), since these would have been small independent practices named without their involvement.

Built three fictional identities instead, grounded in real local flavor (real neighborhoods/landmarks) without naming actual businesses: **Elm City Pediatric Dental Care** (UC03, New Haven — "Elm City" is New Haven's real nickname), **Barton Springs Dental Group** (UC04a, Austin — near the real Barton Springs area), **Mission Trail Family Dental** (UC04b, San Antonio — near the real Mission Trail). Updated each use case doc's Organization Resource Data appendix and all specific identity references (FHIR endpoints, MRN systems, employment fields) — confirmed the interaction writeups themselves didn't need touching, since they refer to practices generically ("Dr. Watson's practice") rather than by name.

**Real error caught and fixed along the way, unrelated to the naming question**: UC03's placeholder address was "450 Congress Avenue, New Haven, CT" — Congress Avenue is a well-known Austin, TX street, not a New Haven one. A clear copy-paste artifact from the Texas use cases, corrected to a real New Haven street (Whalley Avenue).

Updated the UC04 interactions README to explain the fictional-not-real approach explicitly, distinguishing it from UC02a's real-org precedent as a deliberate choice, not an inconsistency.

### 2026-07-13 — claude.ai chat (v4.4) — UC04 scoped and built (both sub-use-cases), rigorous QA applied throughout
Read both UC04a (commercial) and UC04b (Medicaid) fully, pulled exact timelines before proposing anything. Proposed and confirmed a 5-interaction breakdown per sub-use-case (10 total), then built all 10 writeups with the same proactive QA discipline used for UC03: exact times cross-checked against the source timeline tables, automated checks run before considering it done (all clean — one flagged "vague date" hit was a false positive, verified and dismissed rather than blindly trusted).

**Two structural differences from prior use cases, resolved deliberately rather than pattern-matched from UC01/UC02:**
1. **No imaging exchange between providers** — the virtual/teledentistry provider has no way to generate a radiograph, so imaging is captured fresh in-office (Interaction 3 of each), not pulled/pushed at referral time. Noted explicitly in both writeups and the README, same as UC03's "no DICOM here" callout.
2. **Two separate claims-sharing packages per use case, one per submitting organization** (teledentistry org + in-office org, same payer) — a genuine new pattern for the claims-sharing profile, resolved as "yes, two packages" rather than left as an open question.

**Real finding, not just narrative polish:** UC04a's own source appendix labels tooth #19 using FDI notation ("FDI 36") in a `Procedure` resource description — directly contradicting the ADA's confirmation (established earlier in this project) that FDI isn't used for US dental data. This is the **second** time this exact error pattern has surfaced (the first was in the other dataset's Jason Morales precedent file). Flagged in the writeup, not silently propagated or silently corrected without note.

**Also newly tested in UC04b specifically:** mid-encounter scope expansion (two additional decayed teeth found beyond the referred one, Interaction 3) and a next-day same-provider follow-up `Communication` explicitly modeled as NOT reopening the referral or being a new clinical encounter (Interaction 4).

**Flagged, not addressed this session:** UC04's organizations are still synthetic placeholders — unlike UC02a's Austin Oral Surgery, no real-organization grounding has been done here. Noted in the README as an open item for a future session, not silently skipped.

No FHIR resources built yet for either UC04a or UC04b — narrative-only, per established discipline.

### 2026-07-13 — claude.ai chat (v4.3) — UC03 scoped, rigorously QA'd from the start
Read the full UC03 doc (pediatric periodontitis / Type 1 diabetes, Connecticut Husky B, Connie state HIE). Proposed and confirmed a 5-interaction breakdown, then built all 5 writeups applying the QA discipline established last session **proactively this time**, not as a follow-up correction pass: exact dates cross-checked against the source Timeline table before writing (including preserving the source's own `~2026-03-05` approximation rather than asserting false precision), FHIR resources explicitly listed per interaction as requested, and ran the same automated checks that caught real errors in UC02 (split headers, vague date language, incorrect payer-direction reasoning) before considering this done — all clean on first pass.

**Two genuine open modeling questions found and flagged, not resolved:** (1) whether the two-quadrant D4341 scaling/root planing should be one `Procedure` resource or two, given the source doc's appendix presents it as one entry while CDT billing convention normally bills per-quadrant as separate lines; (2) two distinct `Flag` resources are needed for the diabetes-periodontal relationship, pointed in opposite directions (Interaction 1's diabetes→periodontal-risk flag vs. Interaction 4's new periodontal→glycemic-risk flag to the endocrinologist) — these must not be modeled as the same Flag reused.

**Also carried forward honestly rather than resolved:** the source doc's own two flagged coverage uncertainties (whether D4341 needs PA under Husky B; whether D4381 is covered at all) — Interaction 5 states these as open per the source, not silently assumed either way.

**Noted explicitly:** UC03 doesn't involve imaging/DICOM at all (structured clinical bundles via CDex/Connie, not radiographs) — the v4.1/v4.2 imaging standing instruction doesn't apply here, called out in the README so its absence isn't mistaken for an oversight.

No FHIR resources built yet — narrative-only, per established discipline.

### 2026-07-13 — claude.ai chat (v4.2) — DICOM named explicitly, verified against HL7's own spec
Per user: DICOM is also standard/common here and should be named explicitly, not left implicit under "CDex." Verified precisely (not assumed) against HL7's own `ImagingStudy` spec before writing anything: `ImagingStudy` does NOT contain the actual image — it's a metadata/pointer layer referencing DICOM Study/Series/SOP Instance UIDs; the real pixel data lives in DICOM format on a PACS, retrieved via **WADO-RS** (a DICOMweb REST API), with `ImagingStudy.endpoint` typically pointing at the WADO-RS base URL.

Updated the standing instruction in the top banner to name the full, accurate three-layer stack: **CDex** (the Da Vinci-governed exchange pattern) → **`ImagingStudy`** (FHIR-side pointer/metadata) → **DICOM/WADO-RS** (the actual image standard and retrieval mechanism) — all three should be named explicitly going forward, not simplified to "CDex pulls the image," which skips the layer that matters for real implementers. Updated both UC02a and UC02b's Interaction 2 writeups to reflect this precisely rather than the looser "retrieves via CDex" framing from last session.

### 2026-07-13 — claude.ai chat (v4.1) — Dental/imaging/CDex emphasis + one more QA catch
Per user: this project is fundamentally about dental interoperability with heavy emphasis on **imaging exchange via CDex** — added as a **standing instruction in the top banner** (not just this session's fix) so it persists across all future dental use cases, not just UC02. Key point captured: the imaging transport mechanism is **direction-dependent and already established** — dental-to-dental (UC02+) uses **support-a-pull**; anything touching the medical side (UC01) uses a **separate push**, since medical-side receivers expose no inbound pull. Don't re-derive this each time.

Rebuilt UC02a and UC02b's Interaction 2 writeups to give imaging/CDex real weight as its own tested pattern (support-a-pull, named explicitly, `ImagingStudy`/`DocumentReference` retrieval as the actual thing being tested) rather than riding along as a bullet point inside "the referral package."

**Also caught, missed in the previous QA pass:** UC02a-Interaction-2 had the same split "What Frank Sees" header issue already fixed in UC02a-Interaction-1 last session — confirms the value of checking *every* file individually rather than assuming a fix in one file generalizes. Fixed; verified via repo search that no other files have this issue.

**Also flagged, not fixed this session:** the top banner's "Where we actually are" paragraph is now stale (still describes UC01 as mid-design when it has 5 interactions built/designed and UC02 is well underway) — noted inline in the banner itself as a known issue pending a dedicated cleanup pass.

### 2026-07-13 — claude.ai chat (v4.0) — Rigorous QA of UC02 interaction writeups
Per user: the 10 UC02 writeups built last session were "sloppy and imprecise" — did a real QA pass, pulling every exact date/time from the source doc's Timeline & Dates tables and cross-checking each file line by line, rather than re-skimming. Found real problems, not just polish:

1. **Substantive factual/logical error, repeated in both claims-sharing files (UC02a-05, UC02b-05):** both originally claimed a CPT crosswalk was needed "since this may route through a medical-adjacent Medicaid pathway" — wrong. UC02a and UC02b both bill **dental** payers (Texas Medicaid Dental Plan, Commercial Dental PPO — both 837D per the source doc), not medical. This directly contradicted the very next section in the same files, which correctly frames these as the dental-payer proof point. Rebuilt both: CDT is what's actually required; no CPT crosswalk reasoning asserted; explicit contrast drawn against UC01's medical-payer direction where the crosswalk *was* load-bearing.
2. **Structural inconsistency:** UC02a-Interaction-1 had split "What Frank Sees" into two separate headers mid-document, breaking from the single-callout pattern every other file (including all of UC01's) uses. Rebuilt as one section.
3. **Vague, unanchored dates**, tightened to specifics verified against the source timeline: both claims-sharing files' "shortly after"/"sometime before" replaced with exact dates, explicitly framed as "the FHIR-native equivalent of what would otherwise become the 837D on [exact date]." UC02a-2's "within about 35 minutes" (actually exactly 35 minutes, computed from 14:30→15:05) simplified. UC02b-1's "same visit" (referral sent 30-60 min after the clinical exam per the timeline, not literally the same visit) corrected to "that same morning" in both the header and body. UC02a-4's "a couple hours after the extraction" (imprecise since exact procedure duration isn't specified in the source) replaced with "by 11:30," which is what the source actually states.

All 10 files re-verified clean after fixes (no remaining vague-date or incorrect-reasoning language, confirmed via repo search).

### 2026-07-13 — claude.ai chat (v3.9) — UC02 interaction breakdown + writeups
Confirmed with user: UC02a and UC02b each get **5 interactions** (raised from an initial 4-interaction proposal — user confirmed the claims-sharing interaction is a "key driver," not optional/deferrable, worth the 5th slot in both use cases).

**UC02a (Texas Medicaid):** 1) Prior Authorization Cycle (CRD→DTR→PAS, first-of-kind test in a dental benefit context), 2) Referral Send/Receipt/Scheduling, 3) Surgical Consultation & Extraction, 4) Post-Op Summary & Referral Closure, 5) Claims-Sharing (exercises `ODEOralProfessionalEOB` against a dental Medicaid payer).

**UC02b (Commercial):** 1) Benefit Verification & Referral Send (CRD returns *negative*/no-PA-needed — deliberately different test than UC02a's positive case), 2) Referral Receipt & Scheduling, 3) Consultation/Extraction/Immediate Implant (first use of `Device` resource in this project), 4) Post-Op Summary with Device Record & Referral Closure, 5) Claims-Sharing (commercial-payer direction).

Built all 10 clinician-readable writeups (`use-cases/UC02-tooth-extraction/interactions/`), matching UC01's exact template: "What Happens," embedded "What Frank Sees" patient-facing callouts, "Why This Matters For Testing," explicit "What's NOT part of this interaction." **Flagged, not resolved:** UC02b's Interaction 5 has a genuine open scope question — whether claims-sharing here should also anticipate the future crown claim (tied to the `Device` record), given the source doc names "restorative continuity" as B's core value proposition. Built narrower (UC02a-parallel) scope for now, question stated explicitly in the file itself.

No FHIR resources built yet for either UC02a or UC02b — narrative-only session, per established discipline.

### 2026-07-13 — claude.ai chat (v3.8) — UC02a real organization, fictional surgeon
Per user request and confirmation: replaced UC02a's placeholder "Oral Surgery Practice — Texas (Synthetic)" with the real **Austin Oral Surgery** — a genuine, verified USOSM (U.S. Oral Surgery Management) founding partner practice, 12+ locations across Central Texas, real published Central Austin address (711 W. 38th Street, Suite A-1). User confirmed USOSM is an OHIA member and would generally be supportive of this use. Consistent with the UC01 pattern established this session (real institutions, fictional individual clinicians): **Dr. Alex Maxil, DDS, MD remains fictional** — never a real person, not modeled on any specific real surgeon at Austin Oral Surgery — now simply employed by this real organization. Updated: the appendix Organization Resource Data table (name, real address, USOSM note), Dr. Maxil's employment reference, both narrative introductions (Use Case A and B — B references A's org data by pointer, so one edit propagated), and stale placeholder FHIR/MRN endpoint domains for consistency. No FHIR resources built yet for UC02 — this was use-case-doc-level only.

### 2026-07-13 — claude.ai chat (v3.7) — Provider fictionalization
**Significant correction, prompted by a similar concern surfacing while scoping UC02:** UC01's four named clinicians (previously real, identifiable individuals — Dr. Thomas Galloway, Dr. Cecelia Schmalbach, Dr. Thomas Sollecito, Dr. Teh Lin, real professionals at Fox Chase Cancer Center / Penn Dental Medicine) have been replaced with fully fictional identities: **Dr. Marcus Whitfield** (Radiation Oncology), **Dr. Renata Osei** (Surgical Oncology), **Dr. Andrew Bellweather** (Oral Medicine), **Dr. Priya Nandakumar** (Medical Physics). New synthetic NPIs, license numbers, and email addresses were generated for all four; genericized their credential/bio text (removed specific real board-certification years and a specific real institutional title/department claim that had been verified against an actual real faculty page earlier in this project).

**Institutions were NOT fictionalized** — Fox Chase Cancer Center, Penn Dental Medicine, and Independence Blue Cross remain real, named institutions. Only individual clinicians were in scope for this correction, per the user's specific concern (fabricating clinical scenarios — invented symptoms, treatment decisions — attributed to a real, identifiable private individual is a different and more sensitive thing than referencing a real institution's public role).

**Scope of the fix**: 45 files changed across FHIR resources, the use case doc, all companion guides, the HL7v2 message, and this file — every reference to the four real names, their NPIs, license numbers, and email addresses. All 4 bundles rebuilt (counts unchanged: 35/40/48/51, confirming this was a pure identity substitution, not a structural change). Verified via repo-wide search: zero remaining traces of the real names, NPIs, or personal email addresses.

**Note on historical entries above this one in the session log**: earlier entries describing verification actions (e.g., checking a real board certification, confirming a real title against an actual faculty page) accurately describe what was done *at the time*, against the real individual who has since been replaced. Those entries are left as historical record rather than rewritten, but should be read with this correction in mind — the fictional identities now in the resources were not themselves independently verified against any real person's credentials (nor should they be, since they're fictional).

**Same correction still pending for UC02**: this session also flagged that UC02a's planned real dentist/oral surgeon should likewise be fictional, not real named individuals — not yet built, this was a UC01 retrofit only.

### 2026-07-12 — claude.ai chat (v3.6) — GitHub repo merge
User uploaded their actual GitHub repo state (a zip, `CLAUDE.md` there at v2.4/Claude Code, dated 2026-07-12) since it had fallen behind this thread's work. Compared file-by-file and merged, rather than wholesale-replacing:

**Preserved untouched from the upload** (don't exist in this thread's work, not ours to touch): `UC02-tooth-extraction/UC02-tooth-extraction.md`, `UC03-Pediatric-Referral.md`, `UC04-Teledentistry-Referral.md`, `UC05-SleepApnea Referral.md`, `hl7v2/_reference/360x-cow-crosswalk-summary.md` (a useful working copy of the crosswalk, harmless to keep).

**Replaced with this thread's current/authoritative versions** (the upload was behind — old encounter-vs-interaction duplication still present, missing Interactions 3/4, missing the Subscription, missing the fluoride/scope corrections, missing the claims-sharing narrative): `CLAUDE.md`, all of `companion-guides/`, `use-cases/UC01-medical-to-dental-tongue-cancer/` (including its `interactions/` subfolder), `fhir-resources/common/`, `fhir-resources/uc01-medical-to-dental/base/` and `interactions/`, `hl7v2/uc01-medical-to-dental/interaction-01/`, root `README.md` (refreshed to point at `CLAUDE.md` as authoritative).

**Discarded as superseded/stray**, present in the upload but no longer correct: the old `fhir-resources/uc01-medical-to-dental/encounters/` folder (superseded by `interactions/`, exactly the duplication issue flagged earlier), a stray `fhir-resources/uc01-medical-to-dental/coverage/coverage-john-smith.json` (duplicate outside `base/`), `uc01-base-resources-bundle.json` (old-style, superseded), `hl7v2/uc01-medical-to-dental/encounter-01/` (old duplicate folder), `use-cases/UC01.../encounters/` (old duplicate folder), `companion-guides/UC01-interaction-02-companion-guide.md` (a separate file; superseded by the unified single-file structure already reviewed and approved by the user in this thread).

**Reconciled rather than discarded — the most important merge decision:** the upload's Claude Code session had actually built the Interaction 2 Task-update gap this thread had flagged as missing (`task-360x-dental-referral-interim.json`, plus a matching `interaction-02-delta-bundle.json`) — genuinely valuable work product from a parallel session. But its note claimed the update corresponded to a 360X PCC-59 wire transaction "not yet built" — directly contradicting this thread's explicit, deliberate decision (made and documented repeatedly since v1.8) that Interaction 2 has NO 360X wire-level artifact at all, by design. Kept the valuable data (Task status/owner/output) and corrected the note to state the design decision accurately, rather than either discarding the file or keeping its incorrect claim. This is now the accurate final state for that gap — no longer flagged as missing.

**All 4 bundles rebuilt** to include the corrected interim Task at its correct temporal position: Interaction 1 = 35, Interaction 2 = 40 (was 38 — now includes the interim Task), Interaction 3 = 48, Interaction 4 = 51.

### 2026-07-11 — claude.ai chat (v3.5)
Per user: fluoride trays/gel are never insurance-covered and were removed entirely from the narrative — not just from billing-relevant sections. Confirmed via repo-wide search this touched 5 files: the use case doc's Section I narrative (removed the whole fabrication paragraph, edited the clearance-transmission sentence), the Recommendations row in the ClinicalImpression appendix table, the actual built `clinicalimpression-dental-clearance.json` resource's recommendation text, and the Interaction 3 clinician writeup's aftercare summary. Bundles 3 (47) and 4 (50) rebuilt to reflect the corrected `ClinicalImpression`. Verified repo-wide: zero remaining mentions of "fluoride" anywhere in the project.

### 2026-07-11 — claude.ai chat (v3.4)
**Interaction 5 scoped (narrative only, no FHIR resources yet) and use case doc updated.** User corrected initial scoping: Interaction 5 is explicitly NOT a claim submission — it's the production of the interoperable `ODEOralProfessionalEOB` bundle itself, designed so any PMS can hand it off for automated conversion into whatever format a specific payer/CMS requires. The actual claim submission and format-specific conversion are explicitly downstream, out of scope. Goal stated as industry consensus on one interoperable shape, not solving billing for this one patient.

Updated `UC01-Medical-to-Dental-Tongue-Cancer.md`: (1) added Interaction 5's narrative to Section I (Business Overview), continuing directly from the existing PA-approval paragraph; (2) added a new `ExplanationOfBenefit` row in the Key FHIR Resources table distinguishing its two uses (PDex PPA for PA status vs. the new claims-sharing profile) — previously only the PA use was documented; (3) added a full new technical subsection, "The Oral-Optimized Claims-Sharing Profile (`ODEOralProfessionalEOB`)," documenting the CARIN BB gap this profile fills, its derivation, the confirmed Universal Tooth Designation System resolution, the non-financial/forward-compatible design, and — importantly — that it's dual-purpose by design: UC01 exercises its medical-payer direction, UC02 is expected to exercise its dental-payer direction, proving one shape generalizes across both rather than being use-case-specific.

No FHIR resources built yet for Interaction 5 — this session was narrative/documentation only, per the established discipline of confirming the story before building.

### 2026-07-11 — claude.ai chat (v3.3)
**Interaction 4 built** — "Ending the Prior Authorization" (PA request/approval, 2026-08-01–08-03). User caught a scoping error before build: the `Claim` (PA request) is for the IMRT/radiation service itself (same CPT planning codes 77301/77338 as Interaction 1's original order), NOT for Dr. Bellweather's dental procedures — the dental clearance is supporting evidence attached to the radiation request, not its own claim. Confirmed the CPT crosswalk code (`41899`) used as a placeholder in the earlier claims-sharing draft is independently validated by the use case doc's own appendix. Built: `Claim` (PAS profile, `use: preauthorization`), `ClaimResponse` (PAS profile, `outcome: complete`, `preAuthRef`/`preAuthPeriod` — deliberately omitted an uncertain adjudication category code rather than guess), `ExplanationOfBenefit` (verified real PDex PPA profile canonical, confirmed via direct search rather than assumed). Explicitly confirmed out of scope for this interaction: actual reimbursement billing (837P/835) — that's future work using the project's separately-designed claims-sharing profile. Bundle: 50 resources (registry + base + all 4 interactions).

### 2026-07-11 — claude.ai chat (v3.2)
Per user clarification: "missing patient-facing companion guide" meant the **interaction writeups** (`use-cases/.../interactions/*.md`), not the companion guide document — user wanted specific, structured patient-facing callouts within each interaction's narrative, not just a separate consolidated section. Confirmed via check: Interaction 1 and 3 had one throwaway sentence each; Interaction 2 had none at all.

**Bigger finding while fixing this:** Interaction 2's writeup was missing its Steps 1–2 entirely (Penn Dental's acceptance on 2026-07-07, and the exam itself) — despite these being explicitly designed and confirmed in an earlier chat turn ("Now if you were in charge of interaction 2..."), that content was never actually written into the file. It jumped straight to the two info-requests (DDC inquiry, extension request) as if those were the whole interaction. Rebuilt the file with all 4 steps.

**Added "What John Sees (patient-facing)" callout sections to all three interaction writeups**, each with a concrete notification-text example, plus — for Interaction 2 specifically — explicit call-outs that Steps 3 and 4 (the provider-to-provider notes) should generate **no patient notification at all**, framed as a real testable failure mode (an app that fires on backend chatter is doing the wrong thing), not just documented as an absence.

Flagged in Interaction 2's writeup: the Task update reflecting the Step 1–2 status transitions still isn't built as its own file (same gap already tracked in `CLAUDE.md`/companion guide from earlier sessions — not new, just now visible in the narrative too).

### 2026-07-11 — claude.ai chat (v3.1)
Per user follow-up: the v3.0 fix (Subscription resource + tiny per-interaction blurbs) was not enough — patient-facing content was still scattered across three fragments with no consolidated place to read it, unlike Payer/EHR/Dental Tech, which each get proper step-by-step treatment. Recognized that the patient app is structurally different from the other stakeholders: it does the *same thing* throughout (subscribe once, display milestones) rather than different actions per interaction, so it warranted **one consolidated section**, not per-interaction repetition. Added a new "Patient-Facing App Companion Guide" section (placed before Interaction 2, spanning all interactions) with: what to build, a milestone-by-milestone table mapping each Task status/businessStatus change to what John should see (including an explicit non-milestone — the DDC/extension notes should NOT surface as patient notifications, a real failure mode worth testing for), and pointers to credentials/stub sections rather than duplicating them. Trimmed the three scattered per-interaction blurbs to short cross-references pointing at this new section instead of repeating content.

### 2026-07-11 — claude.ai chat (v3.0)
**Real gap caught by user: patient-facing content was missing entirely.** Confirmed via check: no `Subscription` resource existed anywhere, despite the use case doc's own master "Key FHIR Resources Exercised" table explicitly naming `Subscription`/`SubscriptionStatus` as the mechanism for patient-app milestone notifications (referral sent, appointment scheduled, DDC received, clearance transmitted, PA approved). Also, the companion guide only had a "Patient-Facing App" subsection for Interaction 1 — none for Interactions 2 or 3.

**Fixed:**
1. Built `fhir-resources/uc01-medical-to-dental/base/subscriptions/subscription-john-smith-referral-status.json`. Verified the correct mechanic directly against the HL7 FHIR Subscriptions R4 Backport IG before building: the `SubscriptionTopic` canonical URL belongs in `Subscription.criteria` itself, not a separate extension (a different, non-HL7 implementation — Carequality's — uses an extension instead; don't conflate the two). Placed in `base/`, not a specific interaction, since it's ongoing infrastructure spanning the whole use case.
2. Added "Patient-Facing App" subsections to the companion guide for Interactions 2 and 3 (previously only Interaction 1 had one), each pointing back to this same Subscription rather than inventing new per-interaction patient-app resources.
3. **Also found and fixed, while in the companion guide**: an entire block of stale `encounters/encounter-01/` path and `encounter-01-bundle.json` filename references that predated the v1.8 rename and were never updated (missed in the v2.8 partial fix) — corrected globally across the file.

All three bundles rebuilt with the Subscription added to the base tier: Interaction 1 = 35 (was 34), Interaction 2 = 39 (was 38), Interaction 3 = 47 (was 46).

### 2026-07-11 — claude.ai chat (v2.9)
**Interaction 3 ("The Clearance") built, with rigorous QA that surfaced a significant terminology finding.**

**Terminology QA finding — the use case doc's "SNOMED CT Clinical Codes" table is unreliable.** While sourcing codes for the new Procedure/Observation/ClinicalImpression resources, checked 4 of the 5 codes in that table: `146328D` (dental clearance) confirmed invalid — SNOMED identifiers are purely numeric, this one has a trailing letter. `394839003` (tooth extraction) and `234223000` (implant placement) — no confirmation found; a *different* code (`55162003`) surfaced for tooth extraction instead. `276339004` (osteoradionecrosis) — no confirmation; a different code (`109716001`, "Osteoradionecrosis of the mandible") surfaced instead, itself not fully confirmed as the right match. `52474006` (IMRT) — not checked. Important caveat: general web search is a poor tool for verifying SNOMED concepts specifically (SNOMED's browser content isn't well-indexed by search engines), so this may partly reflect a tooling limitation rather than definitive proof all 5 are wrong — but the hit rate is bad enough that none should be trusted as-is. **Resolution:** all affected resources built text-only (no `coding`) for these specific concepts; the use case doc's table replaced with an explicit caution + audit status per code, rather than silently using or silently deleting the original codes.

**Resources built** (all in `fhir-resources/uc01-medical-to-dental/interactions/interaction-03/`): 3x `Procedure` (CDT-coded D7210/D6010, confirmed real, not part of the suspect SNOMED table), disposition `Observation` (text-only), `ClinicalImpression` (text-only assessment code, full narrative summary/recommendations per the appendix), `DocumentReference` (C-CDA Consultation Note wrapper, LOINC `11488-4`, verified), and **versioned snapshots** (not in-place edits) of the referral `Task` and `ServiceRequest` reflecting PCC-57 completion (`status: completed`, `businessStatus: outcome-final`, `Task.owner` set for the first time, `Task.output` populated per the crosswalk's PCC-57 row).

**Process note — a mistake caught and corrected within this session:** initially edited the Interaction 1 Task file directly to jump its status to `completed`, which would have destroyed the intake-state snapshot and skipped the accepted/in-progress states already documented as belonging to Interaction 2. Reverted, and instead built the completed state as a separate snapshot file (`task-360x-dental-referral-completed.json`) sharing the same resource `id` — correct FHIR versioning semantics (sequential `PUT`s to the same `id`/URL represent version history), consistent with how Interaction 2's Task update was already planned to work.

**Use case doc corrections**: fixed the "two independent tracking mechanisms" framing in Interaction 3's writeup (contradicted the single-Task decision from v2.6) to "two things, one underlying record"; added a technical mechanics paragraph naming PCC-57 explicitly; replaced the SNOMED table per the finding above; fixed the narrative line and two Procedure appendix sections that cited the now-flagged codes.

**Companion guide**: added Interaction 3 section, same two-part structure as Interaction 2 (continuing vs. starting fresh), Resource Index, and the terminology caution called out explicitly so a firm doesn't mistake text-only codes for an oversight.

Interaction 3 bundle: 46 resources (registry + base + all three interactions, correct temporal order for the two versioned resources).

### 2026-07-11 — claude.ai chat (v2.8)
Appended an "Interaction 2" section to `companion-guides/UC01-companion-guide.md` (same file, per its own stated intent), matching Interaction 1's format but not made navigable (no hyperlinks, per user instruction). Structured as **two parts**: Part A (continuing directly from Interaction 1 — update the existing Task, load exam content) and Part B (starting fresh at Interaction 2 — load Interaction 1's output as prerequisite fixture state, or use the `interaction-02-bundle.json` shortcut). Flagged two real gaps in the Resource Index rather than glossing over them: no updated Task resource yet exists reflecting the acceptance/in-progress transitions and `Task.owner` assignment described in the interaction writeup, and no discrete resource yet for the treatment-extension request. Also fixed a stale path reference in the existing troubleshooting section (`encounters/README.md` → `interactions/README.md`, missed during the v1.8 rename).

### 2026-07-11 — claude.ai chat (v2.7)
**Retroactive review of Interaction 1**, per user request, applying everything learned since it was built (crosswalk segment table, single-Task decision). Found and fixed two real issues:
1. **`Task.owner` was set prematurely.** Per the crosswalk's segment table, `Task.owner` specifically represents the accepting provider's identity, populated at PCC-56 (accept) — not PCC-55 (intake). Our Interaction 1 Task had `owner: Organization/org-penndental` set at intake, which doesn't happen until acceptance (2026-07-07, not yet modeled as its own artifact). Removed `owner`; added a note explaining why it's absent and when it should be added (once a PCC-56 accept artifact exists).
2. **Inconsistent requester reference granularity** — `servicerequest-imrt-order.json` used `Practitioner/pract-galloway` while `servicerequest-dental-referral.json` used `PractitionerRole/role-galloway` for the same person. Aligned both to `PractitionerRole`.

Both bundles rebuilt (Interaction 1: 34, Interaction 2: 38 — counts unchanged, content updated).

**Folder structure cleanup:** user noticed both an "encounters" and "interactions" folder existing somewhere. Confirmed the local/delivered copy has **only** `interactions/` (the `encounters/` → `interactions/` rename from v1.8 is complete and clean here) — the duplication user is seeing is in the live GitHub repo, likely introduced by separate Claude Code work that didn't follow the rename. **Fix on the repo side: delete any `encounters/` folder there entirely; everything should live under `interactions/` only**, matching this package's structure exactly.

**Interaction 3 build deferred** — per user instruction, holding before building Interaction 3's files until Interaction 1's retroactive review (this entry) and the repo folder cleanup are both settled.

### 2026-07-11 — claude.ai chat (v2.6)
Reversed last session's plan to build a second, separate CDex documentation Task. Checked the base COW IG (`fhir-cow-ig`) directly: one Coordination Task per Request is COW's own preferred pattern (`Task.output` absorbs all fulfillment artifacts; `businessStatus` tracks progress), and multiple Coordination Tasks per Request — while optional in base COW — is explicitly excluded from this project's own already-adopted 360X-scoped COW subset (per the `ode-360x-adapter` crosswalk). Building a second Task would have violated a scope boundary we'd already committed to. **Resolved design:** the single `ODEReferralTask` (built in Interaction 1) tracks both the referral relationship and the payer's documentation requirement together — no second Task. Made corrections to reflect this: (1) the use case doc's master resource table `Task` row rewritten to describe one Task with inline COW/crosswalk citation; (2) `task-360x-dental-referral.json`'s note strengthened to explicitly state it absorbs the documentation requirement; (3) both bundles (Interaction 1: 34 resources, Interaction 2: 38 resources) rebuilt with the updated Task. Also fixed, found while in the doc: the "Request Treatment Delay" row still described a formal `Communication` resource, contradicting the note-based decision already locked in for Interaction 2 (v2.4) — corrected to match. Interaction 3 ("The Clearance") FHIR resources still not built — this session was pure design resolution.

### 2026-07-11 — claude.ai chat (v2.5)
Scoped Interaction 3 = "The Clearance" (corresponds to clinical Encounter #6, 2026-07-31), following user's decision to describe what happens before deciding how to build it. Built the business-terms writeup (`use-cases/UC01-medical-to-dental-tongue-cancer/interactions/interaction-03-the-clearance.md`) only — no FHIR resources yet, by design (scope first). Key finding while scoping: the use case doc's own resource table describes a **second, separate Task** (a CDex documentation-requirement Task, distinct from the 360X ODEReferralTask) that should have opened at DTR launch back in Interaction 1 — we only ever mentioned it in a note, never built it as its own resource. This is a retroactive gap in Interaction 1, surfaced by properly scoping Interaction 3, not a new requirement. Also confirmed the clearance's transmission mechanism (bare ClinicalImpression vs. wrapped DocumentReference vs. purpose-built ODE resource) is explicitly an open design question in the source use case doc itself (not us being indecisive) — flagged for a deliberate decision before building, not yet resolved. Interaction numbering: since old-Interaction-3 (extension request) folded into Interaction 2 last session, "the clearance" takes the Interaction 3 slot; Interaction 4 (payer packaging) unchanged.

### 2026-07-11 — claude.ai chat (v2.4)
Per user decision: the treatment-extension request (Bellweather/Penn Dental telling Whitfield the IMRT start needs to move from 2026-08-10 to 2026-08-24) is folded into Interaction 2 rather than kept as separate Interaction 3, since it uses the identical mechanism as the DDC dose inquiry — an informal note per the base COW "Requesting additional information" pattern — even though it happens later in the clinical timeline (after clearance/PA approval, not during the dental exam). Built `use-cases/UC01-medical-to-dental-tongue-cancer/interactions/interaction-02-request-for-additional-information.md` covering both moments. **Scope of this session's work was the use-case writeup only** — no new FHIR resources built for the extension-request portion (still needed: the note itself, and likely an update to `servicerequest-imrt-order`'s `occurrenceDateTime` to reflect the revised date — not yet done). Also confirmed via direct check (previous turn) that Interaction 2 is still missing: (1) the Task transition to `in-progress` that should happen *before* the dental exam, communicated to the EHR through the bridge — flagged as the actual first step of Interaction 2, not yet built; (2) any companion guide content. Interaction table in Section 3 updated to show the fold and the current gap list.

### 2026-07-11 — claude.ai chat (v2.3)
User ran the proposed `openapi.yaml` (Section 5a's ODE interface fix) through their FSH validation pipeline — it failed. User supplied a corrected version. Diffed it against ours: the only substantive difference is removal of a fabricated `note` property from the `ODEEncounter` schema (FHIR R4 `Encounter` has genuinely no `note` element — independently verified against HL7's own R4 spec before adopting the fix, not just trusted). Adopted the corrected file as canonical for the ODE interface deliverable. **Also fixed the same bug in our actual test data**: `fhir-resources/uc01-medical-to-dental/interactions/interaction-02/encounter-02-dental-exam.json` had the identical fabricated `Encounter.note` element. Removed it — no content lost, since the Observation resource in the same interaction already independently carries the full explanation. Interaction 2 bundle rebuilt (still 38 resources). Updated Section 6 (verification discipline) with the concrete lesson: our own JSON-structural validation cannot catch a plausible-but-nonexistent FHIR element, since fabricated-but-well-formed JSON still parses fine — real FHIR/FSH validation is a strictly stronger check and should be preferred when available. Also noted that the same modeling error tends to appear in both a spec and the resources built against it, so both need checking when one is found.

### 2026-07-11 — claude.ai chat (v2.2)
Per user direction: ODE interface gaps are **expected and ongoing**, not one-off findings — the ODE interface is an IG under active development, with a separate project converting this OpenAPI spec into a full IG. Restructured the standalone proposal package accordingly: renamed `ode-interface-refactor-proposal.md` → `ISSUE-001-encounter-diagnosticreport-observation-gap.md` (numbered, trackable), added a new `ODE-INTERFACE-ISSUES-LOG.md` index file (status values, how-to-use instructions, index table) as the durable home for this and all future findings. This is now a standing practice, not a special occurrence: every time an interaction can't be executed against the current ODE interface, that becomes a new numbered issue in the log. Updated this file's Section 5a to point at the log and state the practice explicitly.

### 2026-07-11 — claude.ai chat (v2.1)
Per user correction: the `ode-interface-refactor-proposal.md` file (drafted last session) targets a *different* repo (`ohia-fhirr4-scratchpad`), so it shouldn't live inside this repo's package (`ohia-test-data`) at all — moved out of `external-proposals/` (which is now removed entirely) into its own standalone deliverable. Repo structure (Section 2) reverted to the original 4 folders, with an explicit note added that cross-repo feedback/proposals don't belong in this repo going forward — deliver them separately, scoped to whichever repo they target. No content changes to the proposal itself, just packaging/location.

### 2026-07-11 — claude.ai chat (v2.0)
Read the actual ODE-native REST interface spec (`lp-digitalhealth/ohia-fhirr4-scratchpad/interfaces/openapi.yaml`, 791 lines) — a separate repo/concern from `ode-360x-adapter`. Found a real, non-speculative gap: this interface has no path for `Encounter`, `DiagnosticReport`, or `Observation`, and no mechanism to attach content to an already-open referral (only initial submission via `POST /`) — meaning Interaction 2, as already built, cannot be executed against this interface at all, independent of whether a 360X bridge exists. Also found the `ODEReferralTask` schema doesn't model `Task.input`/`Task.output`, despite the crosswalk explicitly adopting both as in-scope. Drafted a full proposed refactor in new file `external-proposals/ode-interface-refactor-proposal.md`: reuses the COW `Task.output` pattern already defined in the crosswalk (rather than inventing something new), adds the three missing resource paths, adds a new `$append-interim` operation (ODE-native equivalent of a bridge's PCC-59 handling), and documents the fix as traceable directly to UC01 Interaction 2's actual resources. New top-level folder `external-proposals/` created for this and any future cross-repo feedback — **flagging placement as an assumption**, not a confirmed decision, same as prior folder additions. We have no write access to `ohia-fhirr4-scratchpad` either — this is a draft for its maintainers, not something we can commit.

### 2026-07-11 — claude.ai chat (v1.9)
**Interaction 2 built.** 4 new FHIR resources in `fhir-resources/uc01-medical-to-dental/interactions/interaction-02/`: `Encounter` (dental exam visit, `basedOn` the Interaction 1 referral), 2x `DiagnosticReport` (periapical CDT D0220/LOINC 62443-7 — verified "Single view Teeth Document XR"; panoramic CDT D0330/LOINC 24828-6), `Observation` (52 Gy dose at tooth #30 — the LOINC-gap resource). The DDC info request/response is captured as `.note` text on both the Encounter and Observation, per the locked-in design decision (not a standalone resource). Self-contained bundle built (`interaction-02-bundle.json`, 38 resources = Interaction 1's 34 + these 4, since Interaction 2 presumes Interaction 1's referral is already open). All JSON validated. `fhir-resources/.../interactions/README.md` updated with Interaction 2 detail. Ready for Interaction 3 (treatment plan + extension request) design.

### 2026-07-11 — claude.ai chat (v1.8)
**Structural reframe, per user direction:** the project's organizing unit for test data changes from "encounter" (7, 1:1 with clinical visits) to "interaction" (4, the specific integration points worth testing — most clinical encounters, e.g. the extractions, are "business as usual" and don't get modeled). The 7-encounter clinical enumeration is unchanged and stays in the use case doc as the clinical reference; it's a different axis from what gets built as test data now.

**Renames executed:**
- `fhir-resources/uc01-medical-to-dental/encounters/` → `interactions/`; `encounter-01/` → `interaction-01/`; `encounter-01-bundle.json` → `interaction-01-bundle.json`
- `hl7v2/uc01-medical-to-dental/encounter-01/` → `interaction-01/`
- `use-cases/UC01-medical-to-dental-tongue-cancer/encounters/` → `interactions/`; the Interaction 1 writeup file renamed to `interaction-01-request-for-radiation-referral.md`
- **Deliberately NOT renamed:** the FHIR `Encounter` resource's own `id`/filename inside interaction-01 (still "encounter-01-imrt-order") — it legitimately represents the clinical visit; renaming would mean touching every cross-reference for no correctness benefit.
- Both README.md files inside the renamed folders rewritten to explain the encounter-vs-interaction distinction.
- `CLAUDE.md` itself substantially restructured: Section 3 now shows both the 7-encounter clinical table (reference only) and the 4-interaction table (what's actually built/tracked), Sections 4/5/7a/8 updated to interaction terminology.

**Not yet updated for the new terminology** (flagged, not fixed, since these are either user-owned or not yet built): `companion-guides/UC01-companion-guide.md` and `stakeholder-matrix.md` still say "Encounter #1" throughout — user is actively hand-editing the companion guide directly in GitHub, so renaming is their call, not something to silently change out from under them. `stakeholder-matrix.md`'s encounter-based row structure also needs a decision on whether to shift to interactions.

**The 4 interactions, locked in:**
1. Request for radiation + payer dental-clearance requirement + initial referral (= old Encounter #1, built)
2. Request for additional information (dental exam findings + DDC dose inquiry) — **design locked in this session**: modeled as a note, confirmed as a legitimate instance of the base COW IG's own named "Requesting additional information" pattern (verified directly from `HL7/fhir-cow-ig`, not assumed) — a real, documented gap between base COW and the 360X-scoped crosswalk, worth raising to `ode-360x-adapter` maintainers. Not yet built as files.
3. Communication of final treatment plan + extension request — not yet designed in detail
4. Packaging treatment for submission to medical payer — not yet designed in detail

### 2026-07-11 — claude.ai chat (v1.7)
Real clinical-modeling correction for Encounter #2 design, via user pushback: the DDC data exchange (Dr. Bellweather asking Dr. Nandakumar for tooth #30 dose data) is **not** a `ServiceRequest` (not ordering a service to be performed) and **not** even a `CommunicationRequest`/`Communication` (too formal) — it's an **informal inter-provider information request between practitioners already in an established clinical relationship**, correctly modeled as a **note/annotation**, not a standalone FHIR resource. The resulting dose value (52 Gy at tooth #30) is still captured formally as an `Observation` — only the request/response *mechanism* is downgraded to a note. Corrected `use-cases/UC01-medical-to-dental-tongue-cancer/UC01-Medical-to-Dental-Tongue-Cancer.md` in two places: the Encounter #2 appendix detail (was mislabeled "ServiceRequest (Dosimetric Dental Contouring Request)") and the master "Key FHIR Resources Exercised" table (previously listed DDC under `Communication`/`CommunicationRequest` — corrected to note that only the *IMRT delay request*, a separate later-encounter item, legitimately uses those resource types). No FHIR/HL7v2 resource files built yet for Encounter #2 — this was pure clinical-modeling design work, still in progress. Other three Encounter #2 design questions (from v1.6) remain open: whether the "push-only imaging" rule applies symmetrically, and how/whether Encounter #1's Task transitions at Encounter #2.

### 2026-07-11 — claude.ai chat (v1.6)
User made real edits directly in GitHub to both `UC01-readiness-checklist.md` (verified unchanged from prior version — no edits found) and `UC01-companion-guide.md` (substantively improved: per-role file tables in Section 2, Stub Specs as its own Section 3, new Section 4 Resource Index with every file organized by tier, sections renumbered 0-9). Fetched both directly from GitHub and confirmed via read. Synced local copy of the companion guide to match. **Encounter #1 is now considered fully complete and finalized** — FHIR resources, HL7v2, both companion docs. Ready to begin Encounter #2 design. Re-raised (not yet answered) 4 open design questions for Encounter #2: (1) DDC ServiceRequest direction (dental→medical) — new 360X transaction or follow-up under existing Task? (2) Does the "push-only, no pull" imaging rule apply symmetrically when FCCC is the receiver? (3) Does Encounter #1's Task get updated in-place (new version) at Encounter #2, or does #2 get its own Task? (4) Confirmed CDT+LOINC dual-coding is correct for Penn Dental's internal DiagnosticReports (D0220/LOINC 62443-7, D0330/LOINC 24828-6) since they don't cross to the medical side.

### 2026-07-11 — claude.ai chat (v1.5)
Added two more tooling sections to `UC01-companion-guide.md`: Section 7 (FHIR services — HAPI FHIR/OnyxOS server setup, loading mechanics, profile validation via the official HL7 FHIR Validator CLI and Inferno, CDS Hooks testing via plain HTTP) and Section 8 (Patient-facing app credentials — SMART App Launch registration, client ID/secret, redirect URIs, scopes, sandbox vs. production credential handling, and a caution against committing real secrets to the repo). Renumbered the troubleshooting section to 8 (fixed a numbering gap in the same edit — sections now run 0-8 sequentially). No FHIR/HL7v2 resource changes this session — companion guide content only.

### 2026-07-11 — claude.ai chat (v1.4)
Verified all file references in `UC01-companion-guide.md` actually resolve on disk — found and fixed a real gap: `CLAUDE.md`, `stakeholder-matrix.md`, and `UC01-companion-guide.md` had been built as standalone downloads only, never placed into the local repo tree alongside the rest of the library. Copied all three into their correct locations and re-verified (16/16 file references now resolve; all JSON still valid; bundle resource count still 34). Also added a new Section 6 to the companion guide: HL7v2 tooling requirements (parsing libraries, MLLP/interface engines like Mirth Connect, the bridge's own internal parser, and lightweight validators for spot-checking) — this was previously discussed in chat but not captured in the guide itself.

### 2026-07-11 — claude.ai chat (v1.3)
Built `companion-guides/UC01-companion-guide.md` for Encounter #1: Business Overview, Stub Specifications (per role), step-by-step prep per stakeholder type (Payer/Dental Tech/EHR/Patient App), loading order, and a pointer to existing QA notes for troubleshooting. This completes Encounter #1's companion-guide work — the two gaps flagged in v1.1/1.2 (Business Overview, Stub Specs) are now filled. No FHIR/HL7v2 resource changes this session.

### 2026-07-11 — claude.ai chat (v1.2)
Restructured `companion-guides/stakeholder-matrix.md` from a stakeholder-first (provides/consumes/depends-on) design to an encounter-first IG conformance matrix, per user direction: rows = Use Case + Encounter, columns = IG (with responsible-party sub-header), cells = R/NR/U, last column = description. Kept the stakeholder-to-IG responsibility mapping as a secondary reference table in the same file. UC01 Encounter #1 fully filled in (R across CRD/DTR/SMART/360X/ODE, NR for CARIN BB/Provider Access API); Encounters #2-7 and UC02-05 marked U/not-yet-reviewed. No FHIR/HL7v2 resource changes this session.

### 2026-07-11 — claude.ai chat (v1.1)
Encounter #1 companion-guide work: identified that the readiness checklist alone doesn't serve all 5 stakeholder types (esp. non-technical business users, and the "stub" concept cutting across all 4 technical roles). Designed and built `companion-guides/stakeholder-matrix.md` — global provides/consumes/depends-on table across all stakeholders and all use cases, UC01 fully detailed, UC02-05 stubbed. Surfaced Provider Access API (CARIN BB-based, provider-facing, out-of-band) as a 4th payer capability. Still needed before the companion guide is complete: Business Overview section, Stub Specifications section. No FHIR/HL7v2 resource changes this session.

### 2026-07-11 — claude.ai chat (v1.0)
Restructured the standalone continuity doc into this repo-resident `CLAUDE.md`, added the mode-split protocol (Section 7a) and this Session Log. No new project content built this session — this was a tooling/workflow session. Confirmed (via a Claude Code test, reported by user) that GitHub project-sync into claude.ai chat is not working reliably — chat cannot see this repo's files directly as of this writing. Established convention: user pastes this file's contents into new chat sessions to resume design work.
