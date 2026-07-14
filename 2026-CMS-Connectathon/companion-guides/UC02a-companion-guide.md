# UC02a Companion Guide — Texas Medicaid Surgical Extraction with Prior Authorization

**Status:** covers all five interactions — **I1 (The Prior Authorization Wait), I2 (The Handoff to Oral Surgery), I3 (The Extraction), I4 (Closing the Loop), and I5 (Billing the Extraction)** — the complete UC02a episode, referral through claims-sharing.

**Patient:** Frank Castle, 53, Austin, TX. **Payer:** Texas Medicaid — Adult Dental, administered by DentaQuest (a real organization; the treating clinicians in this use case are fictional). **Referring provider:** Dr. Mary Parker, DDS, South Congress Dental Care (fictional practice). **Receiving provider:** Dr. Alex Maxil, DDS, MD, Austin Oral Surgery (a real, USOSM-partner organization; Dr. Maxil himself is fictional).

---

## 0. Business Overview

Frank has a painful, fractured tooth (#30) that needs surgical extraction. Because Texas Medicaid's adult dental benefit only covers medically-necessary emergency dental work — not routine care — and because this specific procedure requires prior authorization, nothing can move forward until that PA is confirmed. **UC02a-I1** covers the entire PA cycle: Dr. Parker's exam, the automatic coverage-requirements check, the pre-filled documentation, and Texas Medicaid's approval — ending with a PA number that everything downstream depends on. **UC02a-I2** covers what happens once that PA number exists: the referral to Dr. Maxil at Austin Oral Surgery, and same-day scheduling confirmation. **UC02a-I3** is the extraction itself — Dr. Maxil re-verifies coverage and diagnosis rather than assuming a week-old PA still holds, then performs the procedure. **UC02a-I4** closes the loop: the post-operative summary and care plan go back to Dr. Parker the same morning, and the referral formally completes. **UC02a-I5** — this use case's key driver — is where Austin Oral Surgery's own reimbursement gets tested: not a real claim submission, but the interoperable, dental-payer-direction proof point for this project's claims-sharing profile.

See [`../use-cases/UC02-tooth-extraction/interactions/`](../use-cases/UC02-tooth-extraction/interactions/) for the full narrative of all five interactions.

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

1. Expose a CDS Hooks `order-sign` discovery service (see [`cds-hooks-discovery-dentaquest.json`](../fhir-resources/durable/cds-hooks/cds-hooks-discovery-dentaquest.json)) that evaluates an incoming D7210 order and returns a card indicating PA is required.
2. Serve the PA `Questionnaire` ([`questionnaire-dentaquest-d7210-pa-dtr.json`](../fhir-resources/durable/payer-rules/questionnaires/questionnaire-dentaquest-d7210-pa-dtr.json)) correctly when DTR launches.
3. Accept the PAS `Claim` submission and return a `ClaimResponse` — `outcome: complete`, `disposition: Approved`, `preAuthRef` populated, `preAuthPeriod` set to a 90-day window from approval.
4. Confirm your `ClaimResponse` states the standard payment-guarantee caveat (PA confirms medical necessity/eligibility at time of review, not a payment guarantee) — this project treats that as a named test consideration, not a defect to fix.

### 2b. Referring Dental Practice / PMS Providers (relevant to I1 and I2)

1. Load the registry and base tiers first (see Resource Index below).
2. At order entry for D7210, fire the CRD hook and handle the returned card.
3. Launch DTR, retrieve the pre-populated `Questionnaire`, submit the `QuestionnaireResponse`.
4. Submit the PA `Claim` via PAS; on approval, carry the `preAuthRef` (PA number) forward — it must appear on the Interaction 2 referral.
5. At I2: transmit the referral (`ServiceRequest`, `status: active`) to Austin Oral Surgery via CDex push, referencing the diagnosis, the PA number, and the clinical findings already captured at I1 (radiograph, periapical findings) — **don't duplicate the imaging into the referral push itself**; dental-to-dental uses support-a-pull, so the referral just needs to correctly reference what the receiving side will retrieve.

### 2c. Receiving Oral Surgery Practice / PMS Providers (relevant to I2, I3, I4)

1. Receive the referral `ServiceRequest` and resolve its references — retrieve the periapical radiograph via CDex → `ImagingStudy` → DICOM WADO-RS (see [`../CLAUDE.md`](../CLAUDE.md)'s standing imaging instruction, and the Tooling section below; this is the dental-to-dental support-a-pull direction, not UC01's separate-push). The periodontal charting (`DiagnosticReport`) and intraoral images (`DocumentReference`) referenced in the same `supportingInfo` are retrieved the same way — same pull mechanism, three different resources.
2. Create an `Appointment` and return an `AppointmentResponse` to the referring practice's system — confirm this completes within the same business day; UC02a's own timeline has referral-to-confirmation happening in under 35 minutes.
3. Confirm the same `Task` used for PA tracking at I1 is updated here, not replaced — see the single-Task design note in the Resource Index below.
4. **At I3:** re-verify the patient's coverage is still active at time of service — don't just trust the week-old PA. Review medications for surgical risk (`MedicationStatement`) — this is the correct point in the workflow for that review, not I1.
5. Perform and document the procedure (`Procedure`, CDT-coded, tooth-specific) — confirm it's traceable back to the PA number via `Procedure.basedOn` → the referral `ServiceRequest` → its `supportingInfo` → the `ClaimResponse`, not via a redundant direct field.
6. **At I4:** push the post-operative summary (`ClinicalImpression`) and care plan (`CarePlan`) back to the referring practice via CDex, same mechanism as the referral itself but reversed. Update the shared `Task` to `status: completed`, `businessStatus: outcome-final` — this closes the entire episode, not just this interaction.
7. **At I5:** assemble the claims-sharing package (`ExplanationOfBenefit`, `ODEDentalClaim` profile) — CDT only, no KX modifier (that's specifically a CMS dental-billed-to-medical mechanism; this bills a dental plan directly, so it doesn't apply here), PA number carried forward one more time via `supportingInfo`.

### 2d. Patient-Facing App Providers (relevant to I1, I2, I4 — NOT I3 or I5)

The patient-facing app does the same thing throughout — subscribe once, display milestones as the referral progresses — so its full guidance is consolidated in the [**Patient-Facing App Companion Guide**](#5-patient-facing-app-companion-guide-spans-all-interactions) section below (milestone-by-milestone table, what to build, and the explicit I3/I5 non-events), rather than repeated per interaction here.

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

### Registry — [`../fhir-resources/durable/`](../fhir-resources/durable/) — load first; reusable across use cases

| File | Type | Purpose |
|---|---|---|
| [`org-south-congress-dental.json`](../fhir-resources/durable/organizations/org-south-congress-dental.json) | Organization | Dr. Parker's practice (fictional) |
| [`org-austin-oral-surgery.json`](../fhir-resources/durable/organizations/org-austin-oral-surgery.json) | Organization | Dr. Maxil's practice (real, USOSM partner) |
| [`org-dentaquest.json`](../fhir-resources/durable/organizations/org-dentaquest.json) | Organization | Real Texas Medicaid dental administrator |
| [`pract-parker.json`](../fhir-resources/durable/practitioners/pract-parker.json) | Practitioner | Dr. Mary Parker |
| [`pract-maxil.json`](../fhir-resources/durable/practitioners/pract-maxil.json) | Practitioner | Dr. Alex Maxil |
| [`loc-south-congress-dental.json`](../fhir-resources/durable/locations/loc-south-congress-dental.json) | Location | South Congress Dental Care office |
| [`loc-austin-oral-surgery.json`](../fhir-resources/durable/locations/loc-austin-oral-surgery.json) | Location | Austin Oral Surgery, Central Austin office |
| [`endpoint-south-congress-dental.json`](../fhir-resources/durable/endpoints/endpoint-south-congress-dental.json), [`endpoint-austin-oral-surgery.json`](../fhir-resources/durable/endpoints/endpoint-austin-oral-surgery.json), [`endpoint-dentaquest.json`](../fhir-resources/durable/endpoints/endpoint-dentaquest.json) | Endpoint | Interim FHIR server addresses |
| [`insplan-tx-medicaid-adult-dental.json`](../fhir-resources/durable/insurance-plans/insplan-tx-medicaid-adult-dental.json) | InsurancePlan | Texas Medicaid Adult Dental benefit structure |
| [`questionnaire-dentaquest-d7210-pa-dtr.json`](../fhir-resources/durable/payer-rules/questionnaires/questionnaire-dentaquest-d7210-pa-dtr.json) | Questionnaire | PA documentation requirements for D7210 |
| [`lib-dentaquest-d7210-pa-logic.json`](../fhir-resources/durable/payer-rules/libraries/lib-dentaquest-d7210-pa-logic.json) | Library | CQL logic behind the CRD PA determination |
| [`plandef-dentaquest-d7210-pa-rule.json`](../fhir-resources/durable/payer-rules/plan-definitions/plandef-dentaquest-d7210-pa-rule.json) | PlanDefinition | The CRD rule itself |
| [`cds-hooks-discovery-dentaquest.json`](../fhir-resources/durable/cds-hooks/cds-hooks-discovery-dentaquest.json) | (not a FHIR resource) | CDS Hooks discovery document |

### Base — [`../fhir-resources/purpose-built/uc02a-surgical-extraction/base/`](../fhir-resources/purpose-built/uc02a-surgical-extraction/base/) — load second; UC02a-specific

| File | Type | Purpose |
|---|---|---|
| [`patient-frank-castle.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/base/patients/patient-frank-castle.json) | Patient | Frank Castle |
| [`coverage-frank-castle.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/base/coverage/coverage-frank-castle.json) | Coverage | Frank's Texas Medicaid Adult Dental coverage |
| [`role-parker.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/base/practitioner-roles/role-parker.json), [`role-maxil.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/base/practitioner-roles/role-maxil.json) | PractitionerRole | Each provider's role at their respective org |
| [`subscription-frank-castle-referral-status.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/base/subscriptions/subscription-frank-castle-referral-status.json) | Subscription | Patient app subscription, spans every patient-facing milestone (I1, I2, I4) |

### Interaction 1 — [`.../interactions/interaction-01/`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/)

| File | Type | Purpose |
|---|---|---|
| [`encounter-01-limited-oral-eval.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/encounter-01-limited-oral-eval.json) | Encounter | The 2026-07-08 exam |
| [`condition-k04-7-periapical-abscess.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/condition-k04-7-periapical-abscess.json), [`condition-k08-89-nonrestorable.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/condition-k08-89-nonrestorable.json) | Condition | The two diagnoses |
| [`observation-periapical-radiolucency.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/observation-periapical-radiolucency.json), [`observation-vertical-root-fracture.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/observation-vertical-root-fracture.json) | Observation | Exam findings |
| [`diagnosticreport-periapical-radiograph.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/diagnosticreport-periapical-radiograph.json) | DiagnosticReport | LOINC 62443-7 (verified) |
| [`diagnosticreport-periodontal-charting.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/diagnosticreport-periodontal-charting.json) | DiagnosticReport | **Text-only code — no verified LOINC found.** This project's fourth named terminology gap, alongside the DDC dose (UC01) and the pediatric PRA (UC03) |
| [`documentreference-intraoral-images.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/documentreference-intraoral-images.json) | DocumentReference | LOINC 72170-4 (verified) |
| [`imagingstudy-periapical.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/imagingstudy-periapical.json) | ImagingStudy | The radiograph itself — retrieved by Austin Oral Surgery at I2 via support-a-pull, not pushed |
| [`questionnaireresponse-pa-dtr.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/questionnaireresponse-pa-dtr.json) | QuestionnaireResponse | DTR-completed PA documentation |
| [`task-referral-pa-tracking.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/task-referral-pa-tracking.json) | Task | **Single Task, same design as UC01** — `focus` on the `QuestionnaireResponse` (no referral exists yet), `status: in-progress` |
| [`claim-d7210-priorauth.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/claim-d7210-priorauth.json) | Claim | The PA request (PAS) |
| [`claimresponse-d7210-priorauth.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/claimresponse-d7210-priorauth.json) | ClaimResponse | Approval, PA number `TX-MCD-PA-2026-047291` |
| [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/interaction-01-bundle.json) | Bundle | Self-contained: registry + base + I1 (32 resources) |

### Interaction 2 — [`.../interactions/interaction-02/`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-02/)

| File | Type | Purpose |
|---|---|---|
| [`servicerequest-referral.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-02/servicerequest-referral.json) | ServiceRequest | The referral, `status: active` |
| [`task-referral-pa-tracking-updated.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-02/task-referral-pa-tracking-updated.json) | Task | Same `id` as the I1 Task, new version — referral sent and appointment confirmed both reflected here, `owner` set for the first time |
| [`appointment-consultation.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-02/appointment-consultation.json) | Appointment | Created by Austin Oral Surgery |
| [`appointmentresponse-confirmed.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-02/appointmentresponse-confirmed.json) | AppointmentResponse | Returned same-day |
| [`interaction-02-bundle.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-02/interaction-02-bundle.json) | Bundle | Self-contained: registry + base + I1 + I2 (36 resources) |

### Interaction 3 — [`.../interactions/interaction-03/`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-03/)

| File | Type | Purpose |
|---|---|---|
| [`encounter-03-surgical.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-03/encounter-03-surgical.json) | Encounter | The 2026-07-21 surgical visit |
| [`medicationstatement-frank-castle.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-03/medicationstatement-frank-castle.json) | MedicationStatement | Patient-reported, reviewed for surgical risk — the source doc places this review here, not I1; no specific medications given in the source, represented honestly as "none reported" rather than invented |
| [`procedure-extraction-tooth30.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-03/procedure-extraction-tooth30.json) | Procedure | D7210, tooth #30, full operative note; traceable to the PA number via `basedOn` → the referral → its `supportingInfo`, not a redundant direct field |
| [`interaction-03-bundle.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-03/interaction-03-bundle.json) | Bundle | Self-contained: registry + base + I1–I3 (39 resources) |

### Interaction 4 — [`.../interactions/interaction-04/`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-04/)

| File | Type | Purpose |
|---|---|---|
| [`clinicalimpression-postop-summary.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-04/clinicalimpression-postop-summary.json) | ClinicalImpression | The post-operative summary pushed back to Dr. Parker |
| [`careplan-postop.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-04/careplan-postop.json) | CarePlan | Follow-up, future restorative options, hygiene — surfaced to the patient app |
| [`servicerequest-referral-completed.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-04/servicerequest-referral-completed.json) | ServiceRequest | Same `id` as I2's version, new version — `status: completed` |
| [`task-referral-pa-tracking-closed.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-04/task-referral-pa-tracking-closed.json) | Task | Same `id`, final version — `status: completed`, `businessStatus: outcome-final`, `output` now includes every fulfillment artifact across all four interactions |
| [`interaction-04-bundle.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-04/interaction-04-bundle.json) | Bundle | Self-contained: registry + base + I1–I4 (43 resources) |

### Interaction 5 — [`.../interactions/interaction-05/`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-05/)

| File | Type | Purpose |
|---|---|---|
| [`eob-d7210-claims-sharing.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-05/eob-d7210-claims-sharing.json) | ExplanationOfBenefit | `ODEDentalClaim` profile — CDT-only (no KX modifier; that's a CMS medical-billing mechanism, doesn't apply to this dental-to-dental payer relationship), PA number carried forward a final time |
| [`interaction-05-bundle.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-05/interaction-05-bundle.json) | Bundle | Self-contained: registry + base + I1–I5 (44 resources) — the complete episode |

---

## 5. Patient-Facing App Companion Guide (spans all interactions)

Unlike the payer and the two dental practices — whose actions genuinely differ interaction by interaction — Frank's patient-facing app does fundamentally the **same thing** throughout: subscribe once, then receive and display milestone notifications as the referral progresses. It is consolidated here for that reason rather than repeated per interaction.

### What to build

1. **A `Subscription`** to the referral's status changes — matching the shape of [`subscription-frank-castle-referral-status.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/base/subscriptions/subscription-frank-castle-referral-status.json). It is a Backport-IG `rest-hook` subscription whose `criteria` carries the `SubscriptionTopic` canonical (`.../SubscriptionTopic/ode-referral-status`) directly — same pattern as UC01. Built once, early, not re-created per interaction.
2. **A notification handler** that receives the `SubscriptionStatus` payload and translates the underlying `Task.status`/`businessStatus` into plain-language milestones for Frank — he should never see raw FHIR codes.

**Note on where the milestones come from — simpler than UC01:** every patient-visible milestone in UC02a, including *"Prior authorization approved,"* rides the **same** referral `Task` and its one Subscription. There is no separate CARIN Blue Button / PDex channel to also listen to (UC01 needed that only because its PA approval arrived as an `ExplanationOfBenefit` from the medical payer). Here, PA approval is simply a `businessStatus` value on the referral Task.

### Milestone-by-milestone: what the app shows, and what's actually driving it

| When | What Frank sees | What's actually happening (Task field) |
|---|---|---|
| I1 (2026-07-08) | "Prior authorization approved" | [`task-referral-pa-tracking.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/task-referral-pa-tracking.json): `status: in-progress`, `businessStatus: pa-approved` (the PA decision itself is the `ClaimResponse` in `Task.output`) |
| I2 (2026-07-14) — first | "Referral sent to Austin Oral Surgery" | [`task-referral-pa-tracking-updated.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-02/task-referral-pa-tracking-updated.json): `Task.output` gains the referral `ServiceRequest`; `owner` set to Dr. Maxil's `PractitionerRole` for the first time |
| I2 (2026-07-14) — then | "Appointment confirmed" | Same Task version: `businessStatus: appointment-confirmed`; `Task.output` gains the `Appointment` and `AppointmentResponse` |
| I3 (2026-07-21) | **Nothing.** The surgical visit itself is not a patient-app milestone — no Task status change is surfaced. | N/A (see below) |
| I4 (2026-07-21) | "Your referral is complete — summary sent to Dr. Parker" (with the `CarePlan` available) | [`task-referral-pa-tracking-closed.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-04/task-referral-pa-tracking-closed.json): `status: completed`, `businessStatus: outcome-final`; `Task.output` gains the `ClinicalImpression` and `CarePlan` |
| I5 (billing) | **Nothing.** The claims-sharing package is a back-office billing artifact, not patient-facing. | N/A |

**The one thing worth testing deliberately:** whether the app correctly fires on the four real milestones (I1, twice at I2, I4) and correctly stays silent for the two non-events (I3 the surgery, I5 the billing). Firing on the surgical visit or the billing event — or missing the completion notice — are the real failure modes this use case is designed to surface.

### Credentials and stubs

Full Patient Access API testing needs real SMART App Launch registration (client ID/secret, redirect URIs, scopes) against whichever FHIR server holds Frank's data — treat client secrets as real secrets even in a sandbox. For the minimum bar without live upstreams, see the Patient app row in [Section 3](#3-stub-specifications): a stub only needs to display a status string per milestone and must NOT fire for I3/I5.

---

## 6. Tooling — what you need to actually run this

UC02a is **entirely FHIR** — there is no HL7v2/wire-level artifact anywhere in this use case (unlike UC01's referral message), so no MLLP transport, interface engine, or HL7v2 parser is needed. What you do need falls into two buckets: a FHIR server, and — because this use case leans heavily on imaging exchange — an imaging stack.

### 6a. FHIR services

- **A FHIR R4 server** to load resources onto so they can be queried/referenced/evaluated: **HAPI FHIR** (Java, open-source, common for Connectathon testing, Docker-friendly) or **OnyxOS**. Any R4-conformant server works.
- **Loading:** each file has a fixed `id` — `PUT [base]/{ResourceType}/{id}` per the load order (Registry → Base → Interaction), or `POST` an interaction bundle (e.g. [`interaction-05-bundle.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-05/interaction-05-bundle.json) for the whole episode) as a single transaction. Any HTTP client (`curl`, Postman) suffices.
- **Profile validation:** the official **HL7 FHIR Validator CLI** (`validator_cli.jar`) checks a resource against its declared `meta.profile`; **Inferno** covers certification-relevant IGs (US Core, SMART App Launch). Our own checks were structural/cross-reference only — run the validator before the Connectathon if strict conformance will be checked.
- **CRD / DTR / PAS (I1):** all plain HTTP — CDS Hooks is a `POST` with a defined JSON shape; DTR serves a `Questionnaire`; PAS exchanges `Claim`/`ClaimResponse`. No special software beyond an HTTP client and the payer's FHIR server.

### 6b. Imaging — the support-a-pull stack (I2)

This use case's defining exchange: at I2, Austin Oral Surgery **retrieves** the periapical radiograph (and the periodontal charting and intraoral images) that South Congress Dental captured at I1 — it is **not** pushed to them. Per [`../CLAUDE.md`](../CLAUDE.md)'s standing imaging instruction, this dental-to-dental direction uses **support-a-pull**, and the accurate technical stack has three named layers — don't collapse it to "CDex pulls the image":

1. **CDex** (Da Vinci Clinical Data Exchange) — the governed exchange *pattern*; here the receiver pulls, since neither side is a medical EHR with no inbound pull.
2. **`ImagingStudy`** ([`imagingstudy-periapical.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/imagingstudy-periapical.json)) — the FHIR-side **pointer/metadata only**. It does *not* contain pixel data; it references DICOM Study/Series/SOP Instance UIDs and its `ImagingStudy.endpoint` typically points at a **WADO-RS base URL**.
3. **DICOM / WADO-RS** — the actual pixel data lives in DICOM format on a **PACS or DICOMweb server** (e.g. **Orthanc** or **dcm4chee**, both open-source and Connectathon-friendly); retrieval happens over **WADO-RS** (a DICOMweb REST API).

The periodontal-charting [`DiagnosticReport`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/diagnosticreport-periodontal-charting.json) and the intraoral-images [`DocumentReference`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/documentreference-intraoral-images.json) referenced in the same referral `supportingInfo` are retrieved the **same pull way** — one mechanism, three different resource types. To exercise this end-to-end you'll want a DICOMweb server standing in for the referring practice's PACS, with the `ImagingStudy.endpoint` pointed at its WADO-RS base; a DICOM viewer (e.g. OHIF, or Orthanc's built-in viewer) is useful for confirming the pulled study visually.

---

## 7. What to do if something doesn't match

Check this guide's Resource Index and the interaction writeups first. If a resource doesn't match what your system expects, that's either a documented design decision (the single-Task pattern, the support-a-pull imaging direction, the absence of a KX modifier on the I5 claims-sharing package) or genuinely new — flag it rather than silently working around it, consistent with every other use case in this project. If you're wondering why a code looks unusual or missing, check [`diagnosticreport-periodontal-charting.json`](../fhir-resources/purpose-built/uc02a-surgical-extraction/interactions/interaction-01/diagnosticreport-periodontal-charting.json) specifically — its text-only code is a confirmed, named terminology gap, not an oversight.
