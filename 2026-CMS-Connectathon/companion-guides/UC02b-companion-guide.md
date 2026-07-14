# UC02b Companion Guide — Commercial Dental PPO, Surgical Extraction with Immediate Implant Option

**Status:** covers all five interactions — **I1 (Checking Coverage, Choosing a Path)**, **I2 (The Handoff to Oral Surgery)**, **I3 (Extraction and Implant, Same Day)**, **I4 (Closing the Loop, Implant Included)**, and **I5 (Billing for Two Procedures)**. FHIR resources and companion-guide sections are built for all five.

**Patient:** Frank Castle, 53, Austin, TX. **Payer:** Commercial Dental PPO (a synthetic placeholder — unlike UC02a's real DentaQuest, no real commercial payer is named here; deliberate). **Referring provider:** Dr. Mary Parker, DDS, South Congress Dental Care (fictional practice). **Receiving provider:** Dr. Alex Maxil, DDS, MD, Austin Oral Surgery (a real, USOSM-partner organization; Dr. Maxil himself is fictional).

> **Same patient, different coverage than UC02a.** UC02b is the deliberate commercial-coverage counterpart to UC02a's Medicaid scenario — same clinical picture (fractured, non-restorable tooth #30), same providers, but a commercial dental PPO that requires **no prior authorization**. Load UC02b's own bundles; don't mix them with UC02a's on the same server if you want each scenario clean (both define `Patient/patient-frank-castle`, but with different coverage identifiers).

---

## 0. Business Overview

Frank has the same painful, fractured tooth (#30) as in UC02a, but this time he's covered by a commercial dental PPO through his employer, not Medicaid. That changes the opening move. **UC02b-I1** is about coverage discovery and decision-making: Dr. Parker's exam, a **real-time benefit verification** (does Frank have implant coverage, is he past the waiting period, how much annual maximum is left), and a coverage-requirements check that comes back **negative — no prior authorization needed**. Because nothing is gated on a PA, the referral to Dr. Maxil goes out **that same morning**, carrying *both* treatment options (extraction alone, or extraction plus an immediate implant) for the surgeon to weigh. **UC02b-I2** is the handoff: Austin Oral Surgery receives the referral, retrieves the imaging via support-a-pull, and books the consultation — confirmation back to Dr. Parker within minutes.

At the **UC02b-I3** consultation (2026-07-15), Dr. Maxil confirms the plan with Frank and, in a single visit, extracts tooth #30 (D7210) and places an immediate endosteal implant into the socket (D6010) — the point where UC02b diverges most from UC02a, which had an extraction only. That implant is captured as the project's first `Device` resource. **UC02b-I4** closes the loop: a post-operative summary naming both procedures and the implant goes back to Dr. Parker's practice, the referral `Task` closes (`outcome-final`), and — the UC02b-specific twist — the implant `Device` record travels with the summary so the general practice has the exact specifications for the crown restoration months later. **UC02b-I5** assembles the interoperable claims-sharing package: a single `ExplanationOfBenefit` with **two** line items (D7210 + D6010), billed to the commercial dental PPO — the commercial-payer counterpart to UC02a's Medicaid direction, again with **no PA number** anywhere on it.

The big things UC02b proves that UC02a doesn't: a CRD service returning a **negative** (no-PA) result correctly and confidently, **benefit-detail verification** (waiting period, remaining annual maximum) beyond UC02a's binary "PA required?" check, an **immediate-implant `Device`** record carried through to the restorative provider, and a **two-line-item** claims-sharing package.

See `use-cases/UC02-tooth-extraction/interactions/uc02b-i1-checking-coverage-choosing-path.md` through `uc02b-i5-billing-two-procedures.md` for the full narrative.

---

## 1. Which IGs Apply

| Interaction | IGs in play |
|---|---|
| **I1 — Checking Coverage, Choosing a Path** | Da Vinci CRD (fires at order entry and returns a **negative** — no PA required for D7210/D6010 — the case UC02b is built to test), Da Vinci PDex (real-time benefit verification: implant coverage, waiting-period status, remaining annual maximum), Da Vinci PDex/Plan-Net (oral surgeon commercial-network participation, confirmed before the referral target is selected — done narratively, not re-modeled), Da Vinci CDex (the referral goes out this same morning — dental-to-dental, **support-a-pull** for imaging), US Core (all clinical content), FHIR Subscriptions Backport IG (patient notification: "referral sent") |
| **I2 — The Handoff to Oral Surgery** | Da Vinci CDex (referral receipt; imaging retrieval via **support-a-pull** → `ImagingStudy` → DICOM WADO-RS, since neither side is a medical EHR), US Core, FHIR Subscriptions Backport IG (patient notification: "appointment confirmed") |
| **I3 — Extraction and Implant, Same Day** | US Core (surgical `Encounter`, two `Procedure`s — D7210 extraction + D6010 immediate implant, `MedicationStatement`), FHIR R4 `Device` (the implant record — first `Device` in this project). **No** patient-app notification fires here (the surgical visit itself is not a milestone) |
| **I4 — Closing the Loop, Implant Included** | Da Vinci CDex (closed-loop post-op summary pushed back to the referring practice, carrying the `Device` record), US Core (`ClinicalImpression`, `CarePlan`), the referral `Task` closes (`outcome-final`), FHIR Subscriptions Backport IG (patient notification: "referral complete") |
| **I5 — Billing for Two Procedures** | The project's claims-sharing profile (`ODEDentalClaim` / `ODEOralProfessionalEOB`) — a two-line-item `ExplanationOfBenefit` (D7210 + D6010) in the **commercial-payer** direction. **No** patient-app notification fires here |

**Notably NOT in scope for UC02b (unlike UC02a):** Da Vinci **DTR** and **PAS** — there is no prior authorization here, so there is no DTR `Questionnaire`/`QuestionnaireResponse` and no PAS `Claim`/`ClaimResponse`, and the I5 claims-sharing package carries **no PA number**. This is the structural point of the use case.

---

## 2. Step-by-Step by Stakeholder

### 2a. Payer / Benefit-Verification Service Providers (relevant to I1)

1. Expose a CDS Hooks `order-sign` discovery service (see `common/cds-hooks-discovery-commercial.json`) that evaluates an incoming D7210 (and/or D6010) order and returns an informational card confirming **no prior authorization is required** and benefits are active — the negative-result CRD case. Do **not** launch DTR or expect a PAS submission.
2. Support a real-time benefit query (PDex-style) that returns benefit *detail*, not just a yes/no: implant (major-services) coverage percentage, waiting-period status (waived here), and remaining annual maximum. In this scenario the plan pays basic 80% / major 50%, annual max $2,000 with **$1,720 remaining** at the time of the check. The fixed plan structure is on `common/insurance-plans/insplan-commercial-dental-ppo.json`; the member- and point-in-time-specific detail (remaining max, waiting period) is narrated on the Coverage resource, since in the real world it comes back on the benefit response rather than being stored on `Coverage`.

### 2b. Referring Dental Practice / PMS Providers (relevant to I1 and I2)

1. Load the registry and base tiers first (see Resource Index below).
2. At order entry for D7210 (with D6010 as an option), fire the CRD hook and handle the **negative** card — confirm your system treats "no PA required, benefits confirmed" as a green light to proceed, not as an error or an unhandled case.
3. Run the real-time benefit verification and surface the detail (implant %, waiting period, remaining max) to the clinician so the extraction-alone vs. extraction-plus-implant conversation with Frank is grounded in actual coverage.
4. **Still at I1:** transmit the referral (`ServiceRequest`, `status: active`, `ode-dental-to-dental-referral` profile) to Austin Oral Surgery via CDex push **that same morning** — there's no PA to wait for. The referral carries **both** treatment options in its `code`/`note` (D7210 alone, or D7210 + D6010); the decision is deferred to the consultation (I3). Reference the diagnosis and clinical findings; **don't duplicate imaging into the push** — dental-to-dental uses support-a-pull, so the referral just references what the receiving side will retrieve.
5. Open the referral-tracking `Task` (`ode-referral-task`) at the same time, `focus` pointing at the referral `ServiceRequest` itself (there's no PA `QuestionnaireResponse` to focus on, unlike UC02a). `businessStatus: referral-sent`; leave `owner` unset until the surgery accepts.

### 2c. Receiving Oral Surgery Practice / PMS Providers (relevant to I2–I5)

1. Receive the referral `ServiceRequest` and resolve its references — retrieve the periapical radiograph via CDex → `ImagingStudy` → DICOM WADO-RS (see `CLAUDE.md`'s standing imaging instruction; dental-to-dental support-a-pull, not UC01's separate-push). The periodontal charting (`DiagnosticReport`) and intraoral images (`DocumentReference`) in the same `supportingInfo` are retrieved the same way — one pull mechanism, three different resources.
2. Confirm your system correctly ingests a referral carrying **two candidate procedures** (D7210 and D6010), not one — the extra option is the UC02b-specific wrinkle worth exercising.
3. Create an `Appointment` and return an `AppointmentResponse` to the referring practice — confirm this completes within the same business day; UC02b's timeline has referral (11:00) → confirmation (11:35) in about 35 minutes.
4. Confirm the same `Task` opened at I1 is **updated, not replaced**, here — `owner` set to Dr. Maxil's `PractitionerRole` for the first time, `businessStatus` advanced to `appointment-confirmed`, `output` gaining the `Appointment` and `AppointmentResponse`. See the single-Task design note in the Resource Index.
5. **At I3 (the surgical visit, 2026-07-15):** record the surgical `Encounter`, a reviewed `MedicationStatement`, and **two** `Procedure`s at the same encounter — the D7210 extraction and the D6010 immediate implant. Create the implant `Device` record (manufacturer, model, lot, manufacture date, placement torque 35 Ncm) and link it from the implant `Procedure` via `Procedure.focalDevice` (`action: implanted`). Confirm your system handles a `Device` — this is the project's first — and that the tooth site stays on the `Procedure` (**R4 `Device` has no `bodySite`**).
6. **At I4 (closing the loop, 2026-07-15):** push a closed-loop post-operative summary back to Dr. Parker's practice via CDex — a `ClinicalImpression` naming both procedures and the implant, plus a `CarePlan` for osseointegration and the future crown phase. **Carry the implant `Device` record with the summary** (referenced from `CarePlan.supportingInfo` and `Task.output`, and named in the `ClinicalImpression.summary`, since R4 `ClinicalImpression.investigation.item` and `CarePlan` cannot reference a `Device` as a first-class link) so the general practice has the exact specifications for the crown. Close the shared referral `Task`: `status: completed`, `businessStatus: outcome-final`, `output` absorbing both Procedures, the Device, the summary, and the care plan.
7. **At I5 (billing, 2026-07-15):** assemble the interoperable claims-sharing package — a single `ExplanationOfBenefit` (`ODEDentalClaim` profile) with **two** line items (D7210 + D6010, both tooth #30). Bill the commercial dental PPO directly. Confirm **no** PA number is carried (none exists), CDT-only (no CPT crosswalk, no KX modifier), and the profile's non-financial design (no `unitPrice`/`net`/`adjudication`). The future implant crown claim (D6065/D6066) is deliberately out of scope.

### 2d. Patient-Facing App Providers (relevant to I1, I2, I4 — NOT I3 or I5)

1. Subscribe to Frank's referral `Task` (see `base/subscriptions/subscription-frank-castle-referral-status.json`).
2. Milestones this guide covers: *"Referral sent to Austin Oral Surgery"* (I1), *"Appointment confirmed with Dr. Maxil — July 15"* (I2), and *"Your referral is complete"* (I4, when the `Task` closes at `outcome-final`).
3. **Nothing fires** during the exam, the benefit verification, or the CRD check (I1), during the surgical visit itself (I3), or during billing (I5) — a patient app that surfaces the benefit-check, CRD chatter, or backend billing as a notification is doing the wrong thing, and that's a real failure mode worth testing for. (There is also no "PA approved" milestone here at all, unlike UC02a — there's no PA.)

---

## 3. Stub Specifications

| Role | Minimum bar |
|---|---|
| **Payer / benefit-verification stub** | Return a fixed "no PA required, benefits active" CDS card for D7210/D6010; answer a benefit query with fixed detail (implant covered 50%, waiting period waived, $1,720 of $2,000 remaining). No `Questionnaire`, no `Claim` handling — those don't exist in UC02b |
| **Referring practice stub** | Handle the negative CRD card as a proceed signal; send a `ServiceRequest` referencing a diagnosis and carrying **both** treatment options; a placeholder `ImagingStudy` reference is sufficient — no real DICOM needed to test referral mechanics |
| **Receiving practice stub** | Accept a `ServiceRequest` (including its two candidate procedures), return a fixed `Appointment`/`AppointmentResponse` pair, update the shared `Task` (`owner` set, `businessStatus: appointment-confirmed`); then record two `Procedure`s + a `Device` (I3), push a closed-loop summary carrying the `Device` and close the `Task` at `outcome-final` (I4), and produce a two-line-item claims-sharing `ExplanationOfBenefit` (I5). A placeholder `Device` (fixed manufacturer/model/lot) is sufficient — no real UDI needed |
| **Patient app stub** | Display a status string for the three patient-visible milestones (referral sent, appointment confirmed, referral complete); confirm it fires **nothing** for the exam, benefit check, CRD check, the surgical visit, or billing |

---

## 4. Resource Index

### Registry — `fhir-resources/common/` — load first; reusable across use cases

| File | Type | Purpose |
|---|---|---|
| `organizations/org-south-congress-dental.json` | Organization | Dr. Parker's practice (fictional; shared with UC02a) |
| `organizations/org-austin-oral-surgery.json` | Organization | Dr. Maxil's practice (real, USOSM partner; shared with UC02a) |
| `organizations/org-commercial-dental-ppo.json` | Organization | **UC02b's payer** — synthetic commercial dental PPO placeholder |
| `practitioners/pract-parker.json` | Practitioner | Dr. Mary Parker (shared with UC02a) |
| `practitioners/pract-maxil.json` | Practitioner | Dr. Alex Maxil (shared with UC02a) |
| `locations/loc-south-congress-dental.json`, `loc-austin-oral-surgery.json` | Location | The two practice offices (shared with UC02a) |
| `endpoints/endpoint-south-congress-dental.json`, `endpoint-austin-oral-surgery.json` | Endpoint | Interim FHIR server addresses (shared with UC02a) |
| `endpoints/endpoint-commercial-dental-ppo.json` | Endpoint | **UC02b's payer** endpoint |
| `insurance-plans/insplan-commercial-dental-ppo.json` | InsurancePlan | Commercial PPO benefit structure: annual max $2,000, basic 80% / major (implant) 50%, implant waiting period waived |
| `payer-rules/libraries/lib-commercial-noauth-logic.json` | Library | CQL logic behind the CRD **no-PA** determination (stub declaration, same convention as UC02a) |
| `payer-rules/plan-definitions/plandef-commercial-noauth-rule.json` | PlanDefinition | The CRD rule itself — returns no-PA / benefits-active, launches no DTR |
| `cds-hooks-discovery-commercial.json` | (not a FHIR resource) | CDS Hooks discovery document for the commercial `order-sign` service |

### Base — `fhir-resources/uc02b-commercial-implant/base/` — load second; UC02b-specific

| File | Type | Purpose |
|---|---|---|
| `patients/patient-frank-castle.json` | Patient | Frank Castle — commercial member ID `COMM-TX-00819472` (no Medicaid ID in this scenario) |
| `coverage/coverage-frank-castle-commercial.json` | Coverage | Commercial dental PPO; `type` = v3-ActCode `DENTAL`; group `582047`; benefit detail (annual max/remaining, implant %, waiting period waived, no PA) narrated |
| `practitioner-roles/role-parker.json`, `role-maxil.json` | PractitionerRole | Each provider's role at their org (Dr. Maxil's note references commercial-network, not Medicaid, participation) |
| `subscriptions/subscription-frank-castle-referral-status.json` | Subscription | Patient app subscription; spans referral-sent (I1), appointment-confirmed (I2), referral-complete (I4, not yet built) — **no "PA approved" milestone** |

### Interaction 1 — `.../interactions/interaction-01/`

| File | Type | Purpose |
|---|---|---|
| `encounter-01-limited-oral-eval.json` | Encounter | The 2026-07-08 exam (10:00) |
| `condition-k04-7-periapical-abscess.json`, `condition-k08-89-nonrestorable.json` | Condition | The two diagnoses (ICD-10-CM K04.7, K08.89) |
| `observation-periapical-radiolucency.json`, `observation-vertical-root-fracture.json` | Observation | Exam findings |
| `diagnosticreport-periapical-radiograph.json` | DiagnosticReport | LOINC 62443-7 (verified) |
| `diagnosticreport-periodontal-charting.json` | DiagnosticReport | **Text-only code — no verified LOINC.** Same named terminology gap flagged in UC02a; carried, not re-litigated |
| `documentreference-intraoral-images.json` | DocumentReference | LOINC 72170-4 (verified) |
| `imagingstudy-periapical.json` | ImagingStudy | DICOM pointer; retrieved by Austin Oral Surgery at I2 via support-a-pull |
| `servicerequest-referral.json` | ServiceRequest | The referral, `status: active`, `ode-dental-to-dental-referral`, referral-id `REF-2026-UC02B-001`, **no PA number**, `insurance` → commercial Coverage, carries **both** D7210 and D6010 options |
| `task-referral-tracking.json` | Task | **Single Task, same design as UC01/UC02a** — `focus` on the referral `ServiceRequest` from the start (no PA cycle precedes it), `businessStatus: referral-sent`, no `owner` yet |
| `interaction-01-bundle.json` | Bundle | Self-contained: registry + base + I1 (29 resources) |

### Interaction 2 — `.../interactions/interaction-02/`

| File | Type | Purpose |
|---|---|---|
| `appointment-consultation.json` | Appointment | Created by Austin Oral Surgery (2026-07-08 11:30); consult 2026-07-15; carries both candidate procedures |
| `appointmentresponse-confirmed.json` | AppointmentResponse | Returned by 11:35, same business day |
| `task-referral-tracking-updated.json` | Task | Same `id` as the I1 Task, new version — `owner` set for the first time (Dr. Maxil), `businessStatus: appointment-confirmed`, `output` gains Appointment/AppointmentResponse |
| `interaction-02-bundle.json` | Bundle | Self-contained: registry + base + I1 + I2 (32 resources; the referral Task is included in both its I1 and I2 versions to apply version history in order) |

### Interaction 3 — `.../interactions/interaction-03/`

| File | Type | Purpose |
|---|---|---|
| `encounter-03-surgical.json` | Encounter | The surgical consultation + procedures, 2026-07-15 09:00–11:30, at Austin Oral Surgery, `basedOn` the referral |
| `medicationstatement-frank-castle.json` | MedicationStatement | No current meds reported; reviewed for surgical risk at the consultation |
| `procedure-extraction-tooth30.json` | Procedure | **D7210** surgical extraction, tooth #30; socket prepared for immediate implant |
| `procedure-implant-tooth30.json` | Procedure | **D6010** immediate endosteal implant; links the `Device` via `Procedure.focalDevice` (`action: implanted`); note carries 35 Ncm torque / healing abutment / 3–4 mo osseointegration |
| `device-implant-tooth30.json` | Device | **Project's first `Device`** — the implant: synthetic manufacturer, model `IMPL-4.0-11.5-SYN`, lot `LOT-2026-04821`, manufacture date 2025-11-01, placement torque 35 Ncm as a structured `Device.property` (UCUM `N.cm`). **Text-only `type`** (no verified SNOMED); no `bodySite` (R4 has none — site is on the Procedure); no `us-core-implantable-device` profile asserted (no UDI, text-only type) |
| `interaction-03-bundle.json` | Bundle | Self-contained: registry + base + I1 + I2 + I3 (37 resources) |

### Interaction 4 — `.../interactions/interaction-04/`

| File | Type | Purpose |
|---|---|---|
| `clinicalimpression-postop-summary.json` | ClinicalImpression | Closed-loop post-op summary; `investigation.item` references both Procedures; the implant `Device` is named in `summary` text (R4 can't reference `Device` from `investigation.item`) |
| `careplan-postop.json` | CarePlan | Osseointegration + future crown (D6065/D6066, text-only, out of scope); carries the implant `Device` via `CarePlan.supportingInfo` for restorative-phase component selection |
| `servicerequest-referral-completed.json` | ServiceRequest | Same `id` as the I1 referral, new version — `status: completed`, keeps both D7210 + D6010, still **no PA number** |
| `task-referral-tracking-closed.json` | Task | Same `id`, final version — `status: completed`, `businessStatus: outcome-final`, `owner` Dr. Maxil, `output` absorbs both Procedures + Device + ClinicalImpression + CarePlan |
| `interaction-04-bundle.json` | Bundle | Self-contained: registry + base + I1–I4 (41 resources; referral Task in all three versions, ServiceRequest in both versions, for version history in order) |

### Interaction 5 — `.../interactions/interaction-05/`

| File | Type | Purpose |
|---|---|---|
| `eob-extraction-implant-claims-sharing.json` | ExplanationOfBenefit | Claims-sharing package, `ode-dental-claim` profile, `use: claim`, `outcome: queued`, id `CS-2026-UC02B-001`; **two** line items (D7210 + D6010, tooth #30, 2026-07-15); commercial payer + Coverage; `supportingInfo` → the referral only (**no PA reference**); CDT-only, non-financial; future crown claim flagged out of scope |
| `interaction-05-bundle.json` | Bundle | Self-contained: registry + base + I1–I5 — the complete episode (42 resources) |

---

## 5. What to do if something doesn't match

Check this guide's Resource Index and the interaction writeups first. If a resource doesn't match what your system expects, it's either a documented design decision — the single-Task pattern, the support-a-pull imaging direction, the **absence** of any DTR/PAS/PA-number in UC02b, the referral originating in I1 rather than I2 — or genuinely new, in which case flag it rather than silently working around it. A few specific things to expect rather than treat as errors:

- **The implant `Device` (I3)** has a **text-only `type`** (no verified SNOMED code — same discipline as the periodontal-charting gap), **no `bodySite`** (R4 `Device` has none; the tooth #30 site lives on `Procedure.focalDevice`'s parent Procedure), placement torque as a `Device.property` in UCUM `N.cm`, and **no `us-core-implantable-device` profile** asserted (synthetic record, no UDI). If your validator wants that profile, note that it's a deliberate omission, not a miss.
- **The claims-sharing `ExplanationOfBenefit` (I5)** uses profile canonical `ode-dental-claim` — the same profile UC02a uses — even though the UC02b narrative refers to it as `ODEOralProfessionalEOB`. This is one profile shape proving it generalizes across payer directions, not two profiles; the naming discrepancy is flagged in-file rather than resolved by inventing a second profile.
- **No PA number anywhere**, including on the I5 claim — unlike UC02a, whose claims-sharing package carries a PA number forward via `supportingInfo`.

If a code looks unusual or missing, check `diagnosticreport-periodontal-charting.json` and `device-implant-tooth30.json` specifically — both are confirmed text-only choices, not oversights. The commercial payer, plan, member, and implant manufacturer/lot identifiers are all synthetic placeholders; if a real commercial payer is chosen later, `Organization/org-commercial-dental-ppo` is the single place to update the name.
