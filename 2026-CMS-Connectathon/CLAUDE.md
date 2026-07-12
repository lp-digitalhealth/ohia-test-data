# CLAUDE.md — OHIA CMS Connectathon Test Data

**Doc version:** 2.3
**Last updated:** 2026-07-11 (by: claude.ai chat)
**Repo:** `lp-digitalhealth/ohia-test-data`, folder `2026-CMS-Connectathon/`

> This file is the single source of truth for this project's decisions, structure, and state. It lives in the repo, not in any one chat. Whoever works on this project next — claude.ai chat or Claude Code — reads this file first, and updates it (including the Session Log at the bottom) before finishing a session.
>
> **Where we actually are:** UC01's test data is organized around **4 key interactions** (not the 7 clinical encounters — see Section 3 for why). **Interaction 1 is built.** Interactions 2–4 are still in design. Most of the project's real decisions — the remaining 3 interactions, and all of UC02–05 — have not been made yet. This is early-stage design work, not an execution backlog. Don't let Claude Code batch-generate interactions or use cases from pattern-matching alone; each needs the same design discussion Interaction 1 got.

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

### 4 test interactions (what gets built as fhir-resources/hl7v2)

| # | Corresponds to encounter(s) | Interaction | Status |
|---|---|---|---|
| 1 | Encounter #1 | Request for radiation + payer indication that dental clearance is required + initial referral | ✅ Built + verified |
| 2 | Encounter #2 | Request for additional information (dental exam findings + DDC dose inquiry) | ✅ Built |
| 3 | Between encounters #5–7 | Communication of final treatment plan + extension request | ⬜ Not yet designed in detail |
| 4 | Related to encounter #1's CRD/DTR pathway | Packaging treatment for submission to medical payer (PA Claim/ClaimResponse) | ⬜ Not yet designed in detail |

**Interaction 2 design decision (locked in):** the DDC dose inquiry (Dr. Sollecito asking Dr. Lin for tooth #30 dose data) is **not** a `ServiceRequest` (not ordering a service) and **not** a `CommunicationRequest`/`Communication` (too formal) — it's modeled as a **note/annotation**. This is confirmed as a legitimate implementation of the base COW IG's (`HL7/fhir-cow-ig`) own named "Requesting additional information" workflow pattern, which explicitly offers three flexible mechanisms — RESTful query, letter, or instruction — with a note mapping to "letter." This pattern is real and named at the base-COW level but is **not carried into the 360X-scoped crosswalk** our bridge implements (a genuine, documented scope gap worth raising to the `ode-360x-adapter` maintainers, using COW's own language). The resulting dose value (52 Gy at tooth #30) is still captured formally as an `Observation` — only the request/response *mechanism* is a note.

Expected new resources for Interaction 2 (not yet built): `Encounter` (dental exam visit), 2x `DiagnosticReport` (periapical D0220/LOINC 62443-7, panoramic D0330/LOINC 24828-6), `Observation` (dose at tooth #30, 52 Gy).

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

This project has repeatedly caught real errors by checking codes/facts against actual sources instead of asserting from memory: 2 wrong SNOMED codes, a wrong NUCC taxonomy code, a wrong v3-ActCode, a wrong CDS Hooks trigger name, a wrong MSH Processing ID, a wrong HL7v2 message type entirely, a real-world credential correction (Dr. Sollecito's title/board cert, confirmed against his actual Penn Dental faculty page), an `IN1` segment regression caught via cross-check against prior QA notes, and a fabricated `Encounter.note` element (FHIR R4 `Encounter` has no `note` element at all — caught by the user's FSH validation pipeline, not by our own checks).

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
Real clinical-modeling correction for Encounter #2 design, via user pushback: the DDC data exchange (Dr. Sollecito asking Dr. Lin for tooth #30 dose data) is **not** a `ServiceRequest` (not ordering a service to be performed) and **not** even a `CommunicationRequest`/`Communication` (too formal) — it's an **informal inter-provider information request between practitioners already in an established clinical relationship**, correctly modeled as a **note/annotation**, not a standalone FHIR resource. The resulting dose value (52 Gy at tooth #30) is still captured formally as an `Observation` — only the request/response *mechanism* is downgraded to a note. Corrected `use-cases/UC01-medical-to-dental-tongue-cancer/UC01-Medical-to-Dental-Tongue-Cancer.md` in two places: the Encounter #2 appendix detail (was mislabeled "ServiceRequest (Dosimetric Dental Contouring Request)") and the master "Key FHIR Resources Exercised" table (previously listed DDC under `Communication`/`CommunicationRequest` — corrected to note that only the *IMRT delay request*, a separate later-encounter item, legitimately uses those resource types). No FHIR/HL7v2 resource files built yet for Encounter #2 — this was pure clinical-modeling design work, still in progress. Other three Encounter #2 design questions (from v1.6) remain open: whether the "push-only imaging" rule applies symmetrically, and how/whether Encounter #1's Task transitions at Encounter #2.

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
