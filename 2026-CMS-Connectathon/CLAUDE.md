# CLAUDE.md — OHIA CMS Connectathon Test Data

**Doc version:** 1.0
**Last updated:** 2026-07-11 (by: claude.ai chat)
**Repo:** `lp-digitalhealth/ohia-test-data`, folder `2026-CMS-Connectathon/`

> This file is the single source of truth for this project's decisions, structure, and state. It lives in the repo, not in any one chat. Whoever works on this project next — claude.ai chat or Claude Code — reads this file first, and updates it (including the Session Log at the bottom) before finishing a session.
>
> **Where we actually are:** only **Encounter #1 of UC01** (7 encounters total) is built. Most of the project's real decisions — about UC01's remaining 6 encounters, and all of UC02–05 — have not been made yet. This is early-stage design work, not an execution backlog. Don't let Claude Code batch-generate encounters #2–7 or UC02–05 from pattern-matching alone; each needs the same design discussion Encounter #1 got.

---

## 1. What this project is

Loadable FHIR test data + supporting artifacts for the OHIA (Oral Health Interoperability Alliance) CMS Connectathon, so participating firms can read a use case, pick which encounter(s) to test, and load exactly what they need. UC01 (Medical-to-Dental Referral, Head & Neck Cancer, patient John Smith) is the model use case.

**Repo caveat:** this GitHub repo also contains a separate, pre-existing, unrelated dataset at `2026-usrealm-testdata/` (different patients — Emily Watkins, Jason Morales, Laura Jennings; different payers — Delta Dental/Cigna Dental/Anthem BCBS of Kentucky). Not part of this project.

---

## 2. Repository structure

```
2026-CMS-Connectathon/
├── CLAUDE.md              This file.
├── use-cases/             Clinician-readable narrative docs — no FHIR jargon.
│                          Per use case, broken into numbered encounters.
├── fhir-resources/        Loadable FHIR R4 JSON — the actual test data.
├── hl7v2/                 Sample HL7 v2 wire-level messages.
└── companion-guides/      Prep guidance + readiness checklists per use case.
```

**Design principle:** `use-cases/` explains the clinical story to a clinician; `fhir-resources/`+`hl7v2/` are the complete parts inventory for engineers; `companion-guides/` ties the two together with concrete prep instructions per encounter — without over-prescribing internal implementation. Guides/checklists are organized **encounter by encounter**, not role by role. One combined guide per use case (not separate guides per role).

### FHIR resource tiers (settled — don't re-litigate without a real reason)

| Tier | Location | Contents | Reusable across use cases? |
|---|---|---|---|
| **Registry** | `fhir-resources/common/` | Organization, Practitioner, Location, InsurancePlan, Endpoint, payer CRD/DTR rules (PlanDefinition/Library/Questionnaire) | Yes — tied to the real-world institution/clinician/plan, not the story |
| **Use-case base** | `fhir-resources/uc01-.../base/` | Patient, Coverage, Consent, **PractitionerRole** | No — specific to this patient's episode. PractitionerRole is deliberately NOT in the registry: the role *pairing* (clinician+org+specialty+location) can vary by use case even when the underlying Practitioner doesn't |
| **Per-encounter** | `fhir-resources/uc01-.../encounters/encounter-0N/` | Encounter, Condition, ServiceRequest, Task, Provenance, etc. | No — tied to that specific moment in the story |

---

## 3. UC01: 7 encounters (fixed, decided — not a range)

| # | Date | Encounter | Status |
|---|---|---|---|
| 1 | 2026-07-06 | Oncology visit — IMRT order & referral | ✅ Built + verified |
| 2 | 2026-07-23 | Dental exam & radiographs | ⬜ Not designed |
| 3 | 2026-07-27 | Extraction #4 | ⬜ Not designed |
| 4 | 2026-07-28 | Extraction #17 | ⬜ Not designed |
| 5 | 2026-07-29 | Extraction #30 + implant placement | ⬜ Not designed |
| 6 | 2026-07-31 | Dental clearance visit | ⬜ Not designed |
| 7 | 2026-08-24 | Revised IMRT start | ⬜ Not designed |

Full breakdown and the 6-vs-7 decision reasoning: `use-cases/UC01-medical-to-dental-tongue-cancer/UC01-Medical-to-Dental-Tongue-Cancer.md`, Appendix Section 0.

**Known design questions for #2 and #6 specifically** (from the `ode-360x-adapter` transaction lifecycle — see Section 5): Encounter #2 likely needs a PCC-59 (interim consultation note) artifact; Encounter #6 likely needs a PCC-57 (referral outcome, closes the loop) artifact; the PCC-56 accept + PCC-60 appointment transactions happen *between* encounters #1 and #2 and aren't yet modeled anywhere. These need actual design decisions, not just pattern-copying from #1.

---

## 4. Encounter #1 — complete (the template/pattern, not a rubber stamp for #2-7)

**34 FHIR resources** in `fhir-resources/uc01-medical-to-dental/encounters/encounter-01/` (plus registry/base dependencies), cross-referenced programmatically — every identifier, date, and code checked to match exactly across resources.

- Encounter, Condition (tongue cancer, ICD-10-CM C02.1)
- AllergyIntolerance (penicillin, RxNorm 7980) + 3× MedicationRequest (lisinopril, atorvastatin, oxycodone/acetaminophen) + medication List (`ODEMedicationList`)
- 2× ServiceRequest (IMRT order; dental referral, `ode-medical-to-dental-referral` profile) + Task (360X referral tracking, `ode-referral-task` profile) + Provenance
- CDS Hooks discovery config for the payer's `order-sign` service (not a FHIR resource — flagged as such in-file)
- Self-contained transaction bundle combining all of the above

**1 HL7 v2 message** in `hl7v2/uc01-medical-to-dental/encounter-01/`: the PCC-55 referral request (`OMG^O19`), built field-by-field against HL7 v2.5.1, cross-verified against the FHIR resources. QA notes file documents verified-vs-illustrative parts and revision history — **read it before modifying the message.**

**1 companion checklist**: `companion-guides/UC01-readiness-checklist.md` — Encounter #1 only, broken into the two distinct technical pathways (payer coverage check vs. referral transmission). Not built for encounters #2–7. No full step-by-step companion guide yet (only this checklist).

---

## 5. Critical external dependency: `lp-digitalhealth/ode-360x-adapter`

Separate GitHub repo — reference implementation bridging IHE 360X (HL7v2/C-CDA over Direct/XDM) and "ODE Native" FHIR. Its `spec/` folder is the conformance contract. Facts below are confirmed from primary sources, not assumed:

- **Architecture**: ports-and-adapters. Three ports: `FhirBackend`, `IheCodec`, `IheOutboundTransport`. Symmetric/bidirectional — direction depends on who initiates.
- **Critical EHR/FHIR boundary**: the medical EHR (FCCC) is HL7v2 + C-CDA native for the 360X referral pathway — **no FHIR capability needed there at all**. The FHIR resources are the bridge's *output* for the dental side. FCCC's FHIR involvement is limited to the separate CRD/DTR (prior auth) pathway. (Modeled wrong initially; corrected.)
- **PCC-55 (Referral Request) = `OMG^O19`**, NOT `REF^I12` (error made and corrected). Structure: `MSH → PID → {AL1} → {ORC → OBR → {DG1}...}`. Referral ID in `ORC-2`/`OBR-2`, matching FHIR `urn:ohia:referral-id`. **No `IN1` segment** — insurance lives only in FHIR `Coverage` (caught as a regression once — watch for it).
- **`ServiceRequest`**: directional profile (`ode-medical-to-dental-referral` / `ode-dental-to-dental-referral` / `ode-dental-to-medical-referral`). ICD-10-CM `reasonCode` + `reasonReference` to Condition (both required), CPT/HCPCS `code` (CDT dropped for medical-side directions, kept dental-to-dental), `supportingInfo` → medication List + AllergyIntolerance.
- **`Task`**: profile `ode-referral-task`. `code.coding` = task-code `fulfill`. `businessStatus` from `ode-referral-sub-status` (`received`, `accepted`, `declined`, `interim-results`, `outcome-final`, `appointment-booked`...). PCC-55 intake stamps `received`. `Task.input` references the referral package.
- **`Provenance`** required in the referral bundle (from `referral_fhir.py`, not the crosswalk doc — easy to miss).
- **Transaction lifecycle**: PCC-55 (request) → PCC-56 (accept) → PCC-60 (appointment) → PCC-59 (interim note, optional) → PCC-57 (outcome, closes loop) → PCC-58 (cancel, optional) → PCC-61 (no-show, optional).
- **Explicitly out of scope, don't over-build**: `Task.partOf` sub-tasks, performer reassignment/baton-passing, multiple Coordination Tasks per Request.
- **CDS Hooks**: this use case's narrative specifies `order-sign` (not `order-select` — corrected).

---

## 6. Verification discipline (an instruction — follow this, don't just read it as history)

This project has repeatedly caught real errors by checking codes/facts against actual sources instead of asserting from memory: 2 wrong SNOMED codes, a wrong NUCC taxonomy code, a wrong v3-ActCode, a wrong CDS Hooks trigger name, a wrong MSH Processing ID, a wrong HL7v2 message type entirely, a real-world credential correction (Dr. Sollecito's title/board cert, confirmed against his actual Penn Dental faculty page), and an `IN1` segment regression caught via cross-check against prior QA notes.

**Rule: verify codes/facts via search before finalizing. Flag anything unverifiable as text-only/uncoded rather than guessing. Before rebuilding any file, check it against its own existing QA notes so fixes don't silently regress.**

---

## 7. Working preferences

- Markdown only; no Word/Excel/PPTX unless explicitly requested
- Companion guides/checklists: capabilities needed, not rigid implementation steps
- One thing at a time when reviewing/fixing — don't bundle multiple changes into one pass
- Source of truth is this repo — no local zip exports

## 7a. How work is split between claude.ai chat and Claude Code

This project is deliberately worked in **two modes**, and each session should know which mode it's in:

- **Design/decision mode (claude.ai chat):** working out *what* an encounter should contain, resolving ambiguity in the narrative, researching external specs, making judgment calls (like the 6-vs-7 encounter decision, or the registry/base tiering split). Exploratory, back-and-forth, one thing at a time.
- **Execution mode (Claude Code):** once a pattern is settled (as it now is for Encounter #1), building the actual files — FHIR JSON, HL7v2 messages, companion guide sections — against that settled pattern, with real repo/git access.

**Claude Code should not use pattern-matching from Encounter #1 to auto-generate Encounters #2–7.** Each encounter has its own clinical content, its own 360X transaction (if any), and its own open questions (see Section 3). Claude Code's job is to implement *decisions already made in this file*, not to make new ones by extrapolation. If Claude Code hits a genuine design gap (something not covered in this file), it should stop and flag it rather than guessing — the same verification discipline in Section 6 applies regardless of which mode is active.

**Handoff protocol:**
1. Decisions get made in chat → this file gets updated (relevant section + Session Log) → committed to the repo.
2. Claude Code reads this file at session start, executes against it, updates this file (status table + Session Log) before finishing, commits.
3. Since claude.ai chat cannot reliably read this repo directly (GitHub project-sync has not worked reliably as of this writing — confirmed via direct test), **paste the current CLAUDE.md content into the first message of a new chat session** to resume design work. If specific built files need review in chat (not just the summary), paste/attach those too.

---

## 8. Not yet built

- Encounters #2–7 (FHIR resources, HL7v2 samples, clinician writeups) for UC01 — **design work needed first, not just execution**
- Full companion guide with step-by-step prep instructions (only the readiness checklist exists, Encounter #1 only)
- Encounter-level test scripts (human-readable + ideally FHIR `TestScript`)
- 360X response transactions: accept (PCC-56), interim note (PCC-59), outcome/clearance (PCC-57), optional cancel (PCC-58) / no-show (PCC-61)
- UC02–UC05 entirely (currently placeholder/synthetic organizations and practitioners in the source use-case docs; need the same real-entity research UC01 received)

## 9. Open questions (unresolved, worth raising externally)

- Whether ODE defines its own patient-facing FHIR profile for referral/appointment status, or whether that rides on the standard Patient Access API surface.
- No discrete field for the *receiving* clinician's identity in the `OMG^O19` message structure — worked around via free text (`NTE`); worth raising to the OHIA/`ode-360x-adapter` maintainers as a possible real gap.

---

## Session Log

*Append-only. Newest entry at the top. Every session (chat or Code) adds one entry before finishing.*

### 2026-07-11 — claude.ai chat
Restructured the standalone continuity doc into this repo-resident `CLAUDE.md`, added the mode-split protocol (Section 7a) and this Session Log. No new project content built this session — this was a tooling/workflow session. Confirmed (via a Claude Code test, reported by user) that GitHub project-sync into claude.ai chat is not working reliably — chat cannot see this repo's files directly as of this writing. Established convention: user pastes this file's contents into new chat sessions to resume design work.
