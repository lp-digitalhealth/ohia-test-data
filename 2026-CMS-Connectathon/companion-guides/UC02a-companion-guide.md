# UC02a Companion Guide — Texas Medicaid Surgical Extraction with Prior Authorization

**Status:** covers all five interactions — **I1 (The Prior Authorization Wait), I2 (The Handoff to Oral Surgery), I3 (The Extraction), I4 (Closing the Loop), and I5 (Billing the Extraction)** — the complete UC02a episode, referral through claims-sharing.

**Patient:** Frank Castle, 53, Austin, TX. **Payer:** Texas Medicaid — Adult Dental, administered by DentaQuest (a real organization; the treating clinicians in this use case are fictional). **Referring provider:** Dr. Mary Parker, DDS, South Congress Dental Care (fictional practice). **Receiving provider:** Dr. Alex Maxil, DDS, MD, Austin Oral Surgery (a real, USOSM-partner organization; Dr. Maxil himself is fictional).

---

## 0. Business Overview

Frank has a painful, fractured tooth (#30) that needs surgical extraction. Because Texas Medicaid's adult dental benefit only covers medically-necessary emergency dental work — not routine care — and because this specific procedure requires prior authorization, nothing can move forward until that PA is confirmed. **UC02a-I1** covers the entire PA cycle: Dr. Parker's exam, the automatic coverage-requirements check, the pre-filled documentation, and Texas Medicaid's approval — ending with a PA number that everything downstream depends on. **UC02a-I2** covers what happens once that PA number exists: the referral to Dr. Maxil at Austin Oral Surgery, and same-day scheduling confirmation. **UC02a-I3** is the extraction itself — Dr. Maxil re-verifies coverage and diagnosis rather than assuming a week-old PA still holds, then performs the procedure. **UC02a-I4** closes the loop: the post-operative summary and care plan go back to Dr. Parker the same morning, and the referral formally completes. **UC02a-I5** — this use case's key driver — is where Austin Oral Surgery's own reimbursement gets tested: not a real claim submission, but the interoperable, dental-payer-direction proof point for this project's claims-sharing profile.

See `use-cases/UC02-tooth-extraction/interactions/` for the full narrative of all five interactions.

---

## 1. Which IGs Apply

| Interaction | IGs in play |
|---|---|
| **I1 — The Prior Authorization Wait** | Da Vinci CRD (fires at order entry, flags PA requirement), Da Vinci DTR (retrieves and pre-populates the PA questionnaire, tracks it as a `Task`), Da Vinci PAS (submits the PA request, receives the `ClaimResponse`) |
| **I2 — The Handoff to Oral Surgery** | Da Vinci CDex (referral push, dental-to-dental — **support-a-pull** for imaging, not the separate-push pattern UC01 used, since neither side here is a medical EHR), Da Vinci PDex/Plan-Net (oral surgeon Medicaid network participation, confirmed before referral target is selected — already done narratively in this use case, not re-modeled as its own resource), US Core (all clinical content), FHIR Subscriptions Backport IG (patient notifications) |
| **I3 — The Extraction** | US Core (Procedure, Encounter, MedicationStatement) — no new IGs; this is the core clinical event, not an interoperability-standard test in itself |
| **I4 — Closing the Loop** | Da Vinci CDex (post-operative summary push, same mechanism as I2's referral push, reversed direction), FHIR Subscriptions Backport IG |
| **I5 — Billing the Extraction** | The project's own draft claims-sharing profile (`ODEDentalClaim`, derived from CARIN Blue Button Professional/NonClinician Basis) — this use case's key driver, proving the profile's dental-payer direction |

**Not in scope for any interaction:** X12 278 (replaced entirely by PAS), the actual 837D EDI submission (I5 builds the FHIR-native interoperable equivalent, not the wire-level transaction itself).

---

## 2. Step-by-Step by Stakeholder

### 2a. Payer / DTR Service Providers (relevant to I1)

1. Expose a CDS Hooks `order-sign` discovery service (see `common/cds-hooks-discovery-dentaquest.json`) that evaluates an incoming D7210 order and returns a card indicating PA is required.
2. Serve the PA `Questionnaire` (`common/payer-rules/questionnaires/questionnaire-dentaquest-d7210-pa-dtr.json`) correctly when DTR launches.
3. Accept the PAS `Claim` submission and return a `ClaimResponse` — `outcome: complete`, `disposition: Approved`, `preAuthRef` populated, `preAuthPeriod` set to a 90-day window from approval.
4. Confirm your `ClaimResponse` states the standard payment-guarantee caveat (PA confirms medical necessity/eligibility at time of review, not a payment guarantee) — this project treats that as a named test consideration, not a defect to fix.

### 2b. Referring Dental Practice / PMS Providers (relevant to I1 and I2)

1. Load the registry and base tiers first (see Resource Index below).
2. At order entry for D7210, fire the CRD hook and handle the returned card.
3. Launch DTR, retrieve the pre-populated `Questionnaire`, submit the `QuestionnaireResponse`.
4. Submit the PA `Claim` via PAS; on approval, carry the `preAuthRef` (PA number) forward — it must appear on the Interaction 2 referral.
5. At I2: transmit the referral (`ServiceRequest`, `status: active`) to Austin Oral Surgery via CDex push, referencing the diagnosis, the PA number, and the clinical findings already captured at I1 (radiograph, periapical findings) — **don't duplicate the imaging into the referral push itself**; dental-to-dental uses support-a-pull, so the referral just needs to correctly reference what the receiving side will retrieve.

### 2c. Receiving Oral Surgery Practice / PMS Providers (relevant to I2, I3, I4)

1. Receive the referral `ServiceRequest` and resolve its references — retrieve the periapical radiograph via CDex → `ImagingStudy` → DICOM WADO-RS (see `CLAUDE.md`'s standing imaging instruction; this is the dental-to-dental support-a-pull direction, not UC01's separate-push). The periodontal charting (`DiagnosticReport`) and intraoral images (`DocumentReference`) referenced in the same `supportingInfo` are retrieved the same way — same pull mechanism, three different resources.
2. Create an `Appointment` and return an `AppointmentResponse` to the referring practice's system — confirm this completes within the same business day; UC02a's own timeline has referral-to-confirmation happening in under 35 minutes.
3. Confirm the same `Task` used for PA tracking at I1 is updated here, not replaced — see the single-Task design note in the Resource Index below.
4. **At I3:** re-verify the patient's coverage is still active at time of service — don't just trust the week-old PA. Review medications for surgical risk (`MedicationStatement`) — this is the correct point in the workflow for that review, not I1.
5. Perform and document the procedure (`Procedure`, CDT-coded, tooth-specific) — confirm it's traceable back to the PA number via `Procedure.basedOn` → the referral `ServiceRequest` → its `supportingInfo` → the `ClaimResponse`, not via a redundant direct field.
6. **At I4:** push the post-operative summary (`ClinicalImpression`) and care plan (`CarePlan`) back to the referring practice via CDex, same mechanism as the referral itself but reversed. Update the shared `Task` to `status: completed`, `businessStatus: outcome-final` — this closes the entire episode, not just this interaction.
7. **At I5:** assemble the claims-sharing package (`ExplanationOfBenefit`, `ODEDentalClaim` profile) — CDT only, no KX modifier (that's specifically a CMS dental-billed-to-medical mechanism; this bills a dental plan directly, so it doesn't apply here), PA number carried forward one more time via `supportingInfo`.

### 2d. Patient-Facing App Providers (relevant to I1, I2, I4 — NOT I3 or I5)

1. Subscribe to Frank's referral `Task` (see `base/subscriptions/subscription-frank-castle-referral-status.json`).
2. Milestones this guide covers: *"Prior authorization approved"* (I1), *"Referral sent to Austin Oral Surgery"* and *"Appointment confirmed"* (I2, both from the same interaction, in sequence), *"Your referral is complete — summary sent to Dr. Parker"* with the `CarePlan` attached (I4).
3. Nothing fires during the exam, the CRD check, the DTR pre-population, the surgical visit itself (I3), or the billing event (I5) — I3 and I5 are entirely non-patient-facing, confirmed against both interaction writeups.

---

## 3. Stub Specifications

| Role | Minimum bar |
|---|---|
| **Payer/DTR stub** | Return a fixed "PA required" CDS card for D7210; serve a static `Questionnaire`; accept a `Claim` and return a fixed-approved `ClaimResponse` with a PA number |
| **Referring practice stub** | Send a `ServiceRequest` referencing a PA number and a diagnosis; doesn't need real imaging behind it — a placeholder `ImagingStudy` reference is sufficient for testing the referral mechanics; accept a `ClinicalImpression`/`CarePlan` push back at I4 |
| **Receiving practice stub** | Accept a `ServiceRequest`, return a fixed `Appointment`/`AppointmentResponse` pair; return a fixed `Procedure` at I3; push a fixed `ClinicalImpression`/`CarePlan` at I4; produce one `ExplanationOfBenefit` at I5 |
| **Patient app stub** | Display a status string for each of the four patient-visible milestones (I1, twice at I2, I4); doesn't need working OAuth for this minimum bar; confirm it does NOT fire anything for I3 or I5 |

---

## 4. Resource Index

### Registry — `fhir-resources/common/` — load first; reusable across use cases

| File | Type | Purpose |
|---|---|---|
| `organizations/org-south-congress-dental.json` | Organization | Dr. Parker's practice (fictional) |
| `organizations/org-austin-oral-surgery.json` | Organization | Dr. Maxil's practice (real, USOSM partner) |
| `organizations/org-dentaquest.json` | Organization | Real Texas Medicaid dental administrator |
| `practitioners/pract-parker.json` | Practitioner | Dr. Mary Parker |
| `practitioners/pract-maxil.json` | Practitioner | Dr. Alex Maxil |
| `locations/loc-south-congress-dental.json` | Location | South Congress Dental Care office |
| `locations/loc-austin-oral-surgery.json` | Location | Austin Oral Surgery, Central Austin office |
| `endpoints/endpoint-south-congress-dental.json`, `endpoint-austin-oral-surgery.json`, `endpoint-dentaquest.json` | Endpoint | Interim FHIR server addresses |
| `insurance-plans/insplan-tx-medicaid-adult-dental.json` | InsurancePlan | Texas Medicaid Adult Dental benefit structure |
| `payer-rules/questionnaires/questionnaire-dentaquest-d7210-pa-dtr.json` | Questionnaire | PA documentation requirements for D7210 |
| `payer-rules/libraries/lib-dentaquest-d7210-pa-logic.json` | Library | CQL logic behind the CRD PA determination |
| `payer-rules/plan-definitions/plandef-dentaquest-d7210-pa-rule.json` | PlanDefinition | The CRD rule itself |
| `cds-hooks-discovery-dentaquest.json` | (not a FHIR resource) | CDS Hooks discovery document |

### Base — `fhir-resources/uc02a-surgical-extraction/base/` — load second; UC02a-specific

| File | Type | Purpose |
|---|---|---|
| `patients/patient-frank-castle.json` | Patient | Frank Castle |
| `coverage/coverage-frank-castle.json` | Coverage | Frank's Texas Medicaid Adult Dental coverage |
| `practitioner-roles/role-parker.json`, `role-maxil.json` | PractitionerRole | Each provider's role at their respective org |
| `subscriptions/subscription-frank-castle-referral-status.json` | Subscription | Patient app subscription, spans every patient-facing milestone (I1, I2, I4) |

### Interaction 1 — `.../interactions/interaction-01/`

| File | Type | Purpose |
|---|---|---|
| `encounter-01-limited-oral-eval.json` | Encounter | The 2026-07-08 exam |
| `condition-k04-7-periapical-abscess.json`, `condition-k08-89-nonrestorable.json` | Condition | The two diagnoses |
| `observation-periapical-radiolucency.json`, `observation-vertical-root-fracture.json` | Observation | Exam findings |
| `diagnosticreport-periapical-radiograph.json` | DiagnosticReport | LOINC 62443-7 (verified) |
| `diagnosticreport-periodontal-charting.json` | DiagnosticReport | **Text-only code — no verified LOINC found.** This project's fourth named terminology gap, alongside the DDC dose (UC01) and the pediatric PRA (UC03) |
| `documentreference-intraoral-images.json` | DocumentReference | LOINC 72170-4 (verified) |
| `imagingstudy-periapical.json` | ImagingStudy | The radiograph itself — retrieved by Austin Oral Surgery at I2 via support-a-pull, not pushed |
| `questionnaireresponse-pa-dtr.json` | QuestionnaireResponse | DTR-completed PA documentation |
| `task-referral-pa-tracking.json` | Task | **Single Task, same design as UC01** — `focus` on the `QuestionnaireResponse` (no referral exists yet), `status: in-progress` |
| `claim-d7210-priorauth.json` | Claim | The PA request (PAS) |
| `claimresponse-d7210-priorauth.json` | ClaimResponse | Approval, PA number `TX-MCD-PA-2026-047291` |
| `interaction-01-bundle.json` | Bundle | Self-contained: registry + base + I1 (30 resources) |

### Interaction 2 — `.../interactions/interaction-02/`

| File | Type | Purpose |
|---|---|---|
| `servicerequest-referral.json` | ServiceRequest | The referral, `status: active` |
| `task-referral-pa-tracking-updated.json` | Task | Same `id` as the I1 Task, new version — referral sent and appointment confirmed both reflected here, `owner` set for the first time |
| `appointment-consultation.json` | Appointment | Created by Austin Oral Surgery |
| `appointmentresponse-confirmed.json` | AppointmentResponse | Returned same-day |
| `interaction-02-bundle.json` | Bundle | Self-contained: registry + base + I1 + I2 (36 resources) |

### Interaction 3 — `.../interactions/interaction-03/`

| File | Type | Purpose |
|---|---|---|
| `encounter-03-surgical.json` | Encounter | The 2026-07-21 surgical visit |
| `medicationstatement-frank-castle.json` | MedicationStatement | Patient-reported, reviewed for surgical risk — the source doc places this review here, not I1; no specific medications given in the source, represented honestly as "none reported" rather than invented |
| `procedure-extraction-tooth30.json` | Procedure | D7210, tooth #30, full operative note; traceable to the PA number via `basedOn` → the referral → its `supportingInfo`, not a redundant direct field |
| `interaction-03-bundle.json` | Bundle | Self-contained: registry + base + I1–I3 (39 resources) |

### Interaction 4 — `.../interactions/interaction-04/`

| File | Type | Purpose |
|---|---|---|
| `clinicalimpression-postop-summary.json` | ClinicalImpression | The post-operative summary pushed back to Dr. Parker |
| `careplan-postop.json` | CarePlan | Follow-up, future restorative options, hygiene — surfaced to the patient app |
| `servicerequest-referral-completed.json` | ServiceRequest | Same `id` as I2's version, new version — `status: completed` |
| `task-referral-pa-tracking-closed.json` | Task | Same `id`, final version — `status: completed`, `businessStatus: outcome-final`, `output` now includes every fulfillment artifact across all four interactions |
| `interaction-04-bundle.json` | Bundle | Self-contained: registry + base + I1–I4 (43 resources) |

### Interaction 5 — `.../interactions/interaction-05/`

| File | Type | Purpose |
|---|---|---|
| `eob-d7210-claims-sharing.json` | ExplanationOfBenefit | `ODEDentalClaim` profile — CDT-only (no KX modifier; that's a CMS medical-billing mechanism, doesn't apply to this dental-to-dental payer relationship), PA number carried forward a final time |
| `interaction-05-bundle.json` | Bundle | Self-contained: registry + base + I1–I5 (44 resources) — the complete episode |

---

## 5. What to do if something doesn't match

Check this guide's Resource Index and the interaction writeups first. If a resource doesn't match what your system expects, that's either a documented design decision (the single-Task pattern, the support-a-pull imaging direction, the absence of a KX modifier on the I5 claims-sharing package) or genuinely new — flag it rather than silently working around it, consistent with every other use case in this project. If you're wondering why a code looks unusual or missing, check `diagnosticreport-periodontal-charting.json` specifically — its text-only code is a confirmed, named terminology gap, not an oversight.
