# UC07 Companion Guide — DentaQuest Texas: Root Canal, Build-Up, and Crown with Prior Authorization

**Status:** covers all five interactions — **I1 (The Handoff), I2 (Three Procedures, One Authorization), I3 (Linda Says Yes), I4 (Closing the Loop), and I5 (Billing Two Practices)** — the complete UC07 episode, referral through claims. **FHIR fixtures are built** (see `fhir-resources/purpose-built/uc07-pediatric-rootcanal/` and its README); the Resource Index in §4 lists them by logical ID. File links in §4 should be added once the fixtures are committed to the repo.

**Patient:** Joe Castle, 16, Texas. **Guardian:** Linda Castle (mother). **Payer:** DentaQuest — Texas Medicaid dental plan (a real organization, DentaQuest USA Insurance Company, Inc.; the treating clinicians and practices in this use case are fictional). **Referring provider:** Dr. Mary Parker, DDS, pediatric dentistry (fictional practice; Joe's Main Dentist). **Receiving provider:** Dr. Max Garcia, DDS, general dentistry (fictional practice).

---

## 0. Business Overview

Joe has pain on chewing and cold sensitivity at the upper right. Dr. Parker's evaluation and radiographs show decay into the pulp and a periapical infection on tooth #4, a restorable tooth. She refers him to Dr. Garcia for root canal therapy (D3320), a build-up (D2950), and a crown (D2740). **UC07-I1** covers the evaluation, the CDex referral push, the structured notification to DentaQuest, and Dr. Garcia viewing the radiographs over DICOMweb. **UC07-I2** covers the prior authorization for the whole three-procedure plan: CRD, DTR, and PAS, with supporting notes and images delivered by ARex. **UC07-I3** is the consultation and treatment: Dr. Garcia re-verifies coverage rather than trusting a week-old authorization, Linda consents on Joe's behalf, and the work is done. **UC07-I4** closes the loop with a summary, post-operative radiograph, clinical note, and a separate thank-you note back to Dr. Parker. **UC07-I5** is the billing: both practices bill DentaQuest, and the authorization number must appear on the restorative claim.

See [`../use-cases/UC07-Texas-Medicaid-Pediatric-RootCanal/interactions/`](../use-cases/UC07-Texas-Medicaid-Pediatric-RootCanal/interactions/) for the full narrative of all five interactions.

---

## 1. Which IGs Apply

| Interaction | IGs in play |
|---|---|
| **I1 — The Handoff** | Da Vinci CDex (provider-to-provider referral push, **and** provider-to-payer notification to DentaQuest), IHE PCC 360X (delivery of the imaging reference), SMART Imaging Access (retrieval of diagnostic-quality images via WADO-RS; draft CI build), US Core, ODE (under development) |
| **I2 — Three Procedures, One Authorization** | Da Vinci CRD (fires at treatment-plan order entry), Da Vinci DTR (retrieves and pre-populates DentaQuest's questionnaire), Da Vinci PAS (submits the bundled request, receives the `ClaimResponse`), ARex (Onyx Technology; draft/provisional v0.2.0 — delivers notes and images as a signed manifest) |
| **I3 — Linda Says Yes** | US Core (`Encounter`, `Procedure`, `MedicationStatement`, `RelatedPerson`, `Consent`); X12 270/271 eligibility re-check at time of service |
| **I4 — Closing the Loop** | Da Vinci CDex (post-treatment push, same mechanism as I1's referral, reversed), SMART Imaging Access (post-op radiograph retrieved by Dr. Parker), ODE (under development) |
| **I5 — Billing Two Practices** | X12 837D / 835 (the real wire transactions in this use case, because the narrative bills DentaQuest by 837D); US Core `Procedure` data supporting the claims |

**Not in scope for any interaction:** patient-facing apps and subscriptions (the UC07 narrative defines none), pre-referral Plan-Net provider search, and HL7 v2 messaging (see §6).

**Draft-IG caveat:** ARex and SMART Imaging Access are both draft specifications. A conformance failure on either is a finding about the draft, not necessarily a defect in a participant's system.

---

## 2. Step-by-Step by Stakeholder

### 2a. Payer — DentaQuest (relevant to I1, I2, I5)

1. **I1:** Expose a FHIR endpoint that accepts a CDex provider-to-payer `Communication` referencing the referral `ServiceRequest`. Store it and make it retrievable later by referral identifier, so it can be associated with the PA request and the claims.
2. **I2:** Expose a CDS Hooks `order-sign` service that evaluates an order for D3320, D2950, and D2740 together and returns a card indicating PA is required.
3. Serve the DTR `Questionnaire` that states the documentation requirement: clinical notes documenting medical necessity, and images.
4. Accept the PAS `Claim` (`use: preauthorization`) with three service lines. When the `Claim` references an ARex manifest, retrieve each content object and **verify its digest** before relying on it.
5. Return a `ClaimResponse` — `outcome: complete`, `disposition: Approved`, `preAuthRef` populated, and a validity period of 180 days from approval. DentaQuest's published Texas standard for PA turnaround is 3 business days (expedited: 1), and the UC07 timeline has approval 3 business days after submission.
6. Confirm your `ClaimResponse` carries the standard caveat that authorization is not a payment guarantee — a named test consideration in this project, not a defect.
7. **I5:** Accept both 837Ds (route by clearinghouse Payer ID `CX014`), match the restorative claim's PA reference to the `ClaimResponse`, adjudicate, and return a 835 for each. DentaQuest is a payer and carries **no NPI**.

### 2b. Referring Practice — Dr. Parker's pediatric practice (relevant to I1, I4, I5)

1. Load the registry and base tiers first (see §4).
2. At I1, record the evaluation, findings, and diagnoses; produce the periapical and bitewing `ImagingStudy` resources, each with an `endpoint` pointing at your WADO-RS service.
3. Send the referral to Dr. Garcia by CDex push — `ServiceRequest` (priority routine), clinical notes, treatment plan, `Condition`, and `ImagingStudy` pointers. **Do not embed the images in the push.** Dental-to-dental uses support-a-pull.
4. Within the same window, send the structured referral notification to DentaQuest (`Communication` referencing the `ServiceRequest`).
5. Your WADO-RS endpoint must be reachable by Dr. Garcia's viewer and must honor the access grant (`requires-access-token: true`). Log image retrieval as an `AuditEvent`.
6. At I4, receive the post-treatment push. Distinguish the clinical items (`ClinicalImpression`, `ImagingStudy`, `DocumentReference`) from the courtesy `Communication`, file each appropriately, and mark the referral complete.
7. At I5, submit an 837D for D0140, D0220, and D0270 on tooth #4.

### 2c. Receiving Practice — Dr. Garcia's restorative practice (relevant to I1–I5)

1. **I1:** Receive the referral and resolve its `ImagingStudy` pointers by calling the WADO-RS endpoint on Dr. Parker's service; render the radiographs in a DICOM-capable viewer. Open a `Task` for the referral.
2. **I2:** At treatment-plan order entry, fire CRD, handle the returned card, launch DTR, and submit the completed `QuestionnaireResponse`. Publish the notes and images as an ARex manifest (with signed `Provenance`) and submit the PAS `Claim` referencing it. Close the DTR `Task` on approval. Create the `Appointment`.
3. **I3:** Run a 270/271 eligibility check at time of service. Review medications for surgical risk. Obtain guardian consent as a `Consent` naming Linda Castle's `RelatedPerson` as the consenting actor and referencing the authorized procedures. Record `Procedure` for D3320, D2950, and D2740, each on tooth #4 and each traceable to the PA.
4. **I4:** Push the post-treatment package to Dr. Parker by CDex — `ClinicalImpression` (treatment and healing status), the post-op `ImagingStudy` (your WADO-RS endpoint), a `DocumentReference` clinical note, and a separate thank-you `Communication`. Include a `CarePlan` for follow-up.
5. **I5:** Submit an 837D for D3320, D2950, and D2740, **with the `preAuthRef` from the `ClaimResponse` on the claim**.

---

## 3. Stub Specifications

| Role | Minimum bar |
|---|---|
| **Payer stub (DentaQuest)** | Accept and store a `Communication` notification; return a fixed "PA required" CDS card for the D3320 + D2950 + D2740 order; serve a static `Questionnaire`; accept a `Claim` with an ARex manifest reference (retrieving at least one object and checking its digest); return a fixed-approved `ClaimResponse` with a PA number and a 180-day period; accept two 837Ds and match the PA reference on the restorative claim |
| **Referring practice stub** | Send a `ServiceRequest` with a placeholder `ImagingStudy` reference and a diagnosis; send the payer notification; serve at least one DICOM instance over WADO-RS (an Orthanc instance is sufficient); accept a post-treatment push and correctly separate the thank-you `Communication` from clinical content |
| **Receiving practice stub** | Accept a referral and resolve one `ImagingStudy` via WADO-RS; return a fixed CRD/DTR sequence; produce an ARex manifest for at least one object; record three `Procedure` resources and one `Consent` naming a `RelatedPerson`; push a fixed post-treatment package |

---

## 4. Resource Index

Logical IDs below match the generated fixtures; the build specification is `UC-Pediatric-RootCanal-FHIR-Build-Data.md`. Per `CLAUDE.md`, resources are organized into three tiers; the proposed folder is `fhir-resources/purpose-built/uc07-pediatric-rootcanal/`.

### Registry (durable) — load first; reusable across use cases

| Logical ID | Type | Purpose |
|---|---|---|
| `org-pediatric-dental-tx`, `org-restorative-dental-tx` | Organization | The two practices (fictional) |
| `org-dentaquest-tx` | Organization | DentaQuest, type `pay`, Payer ID `CX014`, no NPI |
| `loc-pediatric-dental-tx`, `loc-restorative-dental-tx` | Location | Office locations (POS 11) |
| `pract-mary-parker`, `pract-max-garcia` | Practitioner | Synthetic, Luhn-valid NPIs |
| `endpoint-pediatric-fhir`, `endpoint-restorative-fhir`, `endpoint-dentaquest-tx` | Endpoint | One FHIR endpoint per organization (WADO-RS is deferred for this event) |
| `plandef-dentaquest-d3320-d2950-d2740-pa-rule`, `lib-dentaquest-d3320-d2950-d2740-pa-logic`, `questionnaire-dentaquest-d3320-d2950-d2740-pa-dtr` | PlanDefinition / Library (stub) / Questionnaire | DentaQuest's prior-authorization rule for the bundled plan (synthetic policy) |
| `cds-hooks-discovery-dentaquest.json` (service `dentaquest-d3320-d2950-d2740-pa-check`) | (non-FHIR) | CDS Hooks discovery for the CRD `order-sign` call |

### Base — load second; UC07-specific

| Logical ID | Type | Purpose |
|---|---|---|
| `patient-joe-castle` | Patient | Joe Castle |
| `relatedperson-linda-castle` | RelatedPerson | Mother and guardian |
| `coverage-joe-castle-dentaquest` | Coverage | DentaQuest Texas Medicaid dental plan |
| `practrole-mary-parker`, `practrole-max-garcia` | PractitionerRole | Each clinician at their practice |

### Interaction 1 — The Handoff (2026-07-08)

`encounter-eval`; `condition-caries-tooth4`, `condition-periapical-abscess-tooth4`; `observation-mob-decay`, `observation-periapical-radiolucency`; `imagingstudy-periapical`, `imagingstudy-bitewing`; `diagnosticreport-periapical`, `diagnosticreport-bitewing` (CDT-coded, not LOINC — see §7); `documentref-clinical-notes`, `documentref-treatment-plan`; `procedure-d0140`, `procedure-d0220`, `procedure-d0270`; `servicerequest-referral`; `communication-payer-notification`; `task-referral`.

### Interaction 2 — Three Procedures, One Authorization (2026-07-09 – 07-15)

`questionnaireresponse-dentaquest-pa`; `task-dtr`; `claim-pa-request`; `arex-manifest-pa-docs` (a `List`), three ARex content entries (`arex-entry-pa-periapical`, `arex-entry-pa-bitewing`, `arex-entry-pa-narrative`; the `-pa-` ids differ from I1's entries, which are different resources), `arex-provenance-pa-docs`; `claimresponse-pa-approval` (PA `TX-DQ-PA-2026-061204`, valid 2026-07-15 to 2027-01-11); `appointment-consultation`; `task-referral` (same id as I1, new version). Files: [`interaction-02/`](../../fhir-resources/purpose-built/uc07-pediatric-rootcanal/interactions/interaction-02/).

### Interaction 3 — Linda Says Yes (2026-07-22)

`encounter-consult`, `encounter-treatment`; `consent-joe-castle-treatment`; `MedicationStatement` (none reported — represent honestly, do not invent); `procedure-d3320`, `procedure-d2950`, `procedure-d2740`.

### Interaction 4 — Closing the Loop (2026-07-22)

`clinicalimpression-posttx-summary`; `careplan-posttx`; `imagingstudy-postop` (a pointer to the ARex manifest `arex-manifest-postop`, with its entry `arex-entry-postop-periapical` and `arex-provenance-postop`); `documentref-postop-clinical-note`; `communication-thank-you`; `servicerequest-referral` (same id as I1, new version, `completed`); `task-referral` (same id, new version, `completed` / `outcome-final`). **Pulled in from the deferred I3 at the owner's direction (minimal):** `encounter-treatment`, `procedure-d3320`, `procedure-d2950`, `procedure-d2740`; the consult `Encounter` and the `Consent` remain with I3. Files: [`interaction-04/`](../../fhir-resources/purpose-built/uc07-pediatric-rootcanal/interactions/interaction-04/).

### Interaction 5 — Billing Two Practices (2026-07-23)

Two 837D transactions (pediatric: D0140, D0220, D0270; restorative: D3320, D2950, D2740 plus the PA number) and the 835 responses, plus two claims-sharing `ExplanationOfBenefit` fixtures (`eob-pediatric-claims-sharing`, `eob-restorative-claims-sharing`). The EOBs were **added beyond the narrative's resource list** to mirror UC02a-I5 and UC03-I5; remove them if out of scope.

---

## 5. Patient-Facing App

None. The UC07 narrative defines no patient or guardian application, subscription, or milestone notification, so this guide has no patient-app section and no stub for one. If one is added later, follow the UC02a pattern and start from the single referral `Task`.

---

## 6. Tooling — what you need to actually run this

UC07 is **FHIR plus DICOMweb and X12**. There is no HL7 v2 artifact in this use case, so no MLLP transport or interface engine is needed.

### 6a. FHIR services

- **A FHIR R4 server** (HAPI FHIR or OnyxOS; any R4-conformant server works). Load by `PUT [base]/{ResourceType}/{id}` in the order Registry → Base → Interaction.
- **Profile validation:** the HL7 FHIR Validator CLI against the declared profiles and the exact IG package versions in use. Run it before the Connectathon if strict conformance will be checked.
- **CRD / DTR / PAS (I2):** CDS Hooks is an HTTP `POST` with a defined JSON shape; DTR serves a `Questionnaire`; PAS exchanges `Claim` and `ClaimResponse`.

### 6b. Imaging — the support-a-pull stack (I1 and I4)

At I1, Dr. Garcia **retrieves** the radiographs from Dr. Parker's service; they are not pushed. At I4 the direction reverses for the post-op radiograph. Three layers, none of which should be collapsed into "CDex pulls the image":

1. **CDex / 360X** carry the referral and the imaging reference.
2. **`ImagingStudy`** is the FHIR pointer: metadata, DICOM Study/Series/SOP Instance UIDs, and an `endpoint` to a WADO-RS base URL, flagged `requires-access-token`. It contains no pixel data.
3. **DICOM / WADO-RS** moves the pixels from a PACS or DICOMweb server (e.g. Orthanc or dcm4chee). Use a DICOM viewer (OHIF, or Orthanc's built-in viewer) to confirm retrieval visually.

Each practice needs its own DICOMweb endpoint (pediatric for the referral studies, restorative for the post-op study). Study UIDs for synthetic studies must be generated.

### 6c. Attachments — ARex (I2)

Publish the supporting notes and images as signed, individually retrievable objects, with a digest per object and a time-limited grant scoped to the manifest. The payer retrieves each object and verifies it. Exercise at least one failure case: digest mismatch, expired grant, or unreachable manifest.

### 6d. Claims and eligibility (I3, I5)

270/271 and 837D/835 are X12 and need an X12 translator or clearinghouse stub. Route DentaQuest claims by Payer ID `CX014`.

---

## 7. What to do if something doesn't match

Check this guide's Resource Index and the interaction write-ups first. If a resource doesn't match what your system expects, it's either a documented design decision or genuinely new — flag it rather than silently working around it. Known decisions and open items:

- **No LOINC on radiograph reports.** LOINC is not used in US dentistry; `DiagnosticReport` is coded with CDT (D0220, D0270). This is a documented FHIR/US Core gap for dental, not an oversight.
- **Payers carry no NPI.** DentaQuest is `Organization.type: pay` with Payer ID `CX014` and no `us-npi` identifier.
- **Two Tasks.** The build data has a DTR documentation `Task` and a referral `Task`. `CLAUDE.md` §7 prefers a single coordination Task per request. Decide before building whether the DTR Task is a Da Vinci artifact that justifies a separate Task.
- **Guardian coding.** The `RelatedPerson` relationship code (`MTH` vs `GUARD`) and the `Consent.category` coding are unresolved.
- **Bundled PA.** The narrative treats root canal, build-up, and crown as one three-line authorization. DentaQuest's actual rule for these CDT codes is not confirmed; check the TX HHSC Provider Office Reference Manual and Authorization Catalog.
- **ARex** is draft/provisional. The manifest is a `List` with `DocumentReference` content entries (verified against ARex v0.2.0). The Provenance signature is left to test time, and digests cover placeholder payloads only.
- **I5 EOBs** are an addition to the narrative (see §4); keep or delete.
- **Not validated.** The fixtures passed structural and reference checks only; run the HL7 FHIR Validator with the relevant IG packages before use.
- **CDT display text.** CDT code descriptors are ADA-copyrighted; confirm what display text may be published in this public repository.
- **K02.53 vs K02.63.** The caries code for MOB decay into the pulp needs a dentist's confirmation.

---

## 8. Test Server Roles — November Connectathon (DRAFT for owner review)

> **Status (2026-11-04):** the OHIA test server is **not deployed yet**. Everything marked **Planned** is intended behavior, not tested behavior. Everything marked **TBD** is undecided and is not a default. This section does not change §1–§7; where it conflicts with them, the conflict is called out below.

### 8.0 Purpose and precedence

For the November connectathon, **the interactions in this section override the use-case narrative wherever they differ.** Their purpose is to **get initial connectivity working** between participants and the test server. The fuller capabilities described elsewhere in this guide (for example WADO-RS imaging, the consultation and consent in I3, eligibility checks, and X12 billing in I5) are **not tested in this iteration and will be added in later iterations.**

### 8.1 What the test server is

One FHIR R4 test server (HAPI FHIR on PostgreSQL), synthetic data only, that plays **one party in each interaction** so that a participant only has to implement their own side. Public base URL(s): **TBD** (published before the event). Authentication: **TBD**.

### 8.2 Who plays what

| Interaction | You play | The test server plays | Where your steps are in this guide |
|---|---|---|---|
| **I1 — referral** | Referring practice (Dr. Parker's PMS) | Receiving practice (Dr. Garcia's PMS) | §2b step 3; §2c step 1 |
| **I1 — payer notification** | Referring practice (Dr. Parker's PMS) | Payer (DentaQuest) | §2b step 4; §2a step 1 |
| **I2 — CRD, DTR, PAS** | Receiving practice's PMS (Dr. Garcia) | Payer (DentaQuest) | §2c step 2; §2a steps 2–5 |
| **I4 — closed loop** | Receiving practice's PMS (Dr. Garcia) | Referring practice (Dr. Parker's PMS) | §2c step 4; §2b step 6 |

**Not exercised against the test server:** I3 (consultation, eligibility, consent) and I5 (837D/835 billing).

### 8.3 Interaction by interaction

**I1 — referral to the receiving practice.**
- *You do:* send the referral package as described in §2b step 3 — `ServiceRequest` (routine), clinical notes, treatment plan, `Condition`, and the imaging reference — as a CDex provider-to-provider push to the test server's receiving-practice endpoint (a `POST` of a transaction Bundle). Do not embed images.
- *The test server does (Planned):* accepts and stores the package, opens the referral `Task` (§2c step 1), and returns validation feedback (see 8.4).
- *Success looks like:* the transaction response reports each entry created; the resources are readable by `GET`; the referral `Task` exists.
- *Images (owner's decision):* for this event the radiographs travel as an **ARex manifest of image entries, plus an `ImagingStudy` pointer**. This replaces the WADO-RS endpoint described in §2b/§6b for this iteration; WADO-RS imaging comes in a later iteration. ARex does not define how an `ImagingStudy` points at a manifest, so this event uses a **local convention** (not an ARex rule): `ImagingStudy.identifier` carries the manifest's transaction-context identifier, and the consumer finds the manifest through ARex's `arex-manifest-transaction-identifier` search parameter. ARex is for fixed, immutable objects, not live imaging retrieval.

**I1 — notification to the payer.**
- *You do:* send the provider-to-payer `Communication` referencing the referral `ServiceRequest` (§2a step 1; §2b step 4).
- *The test server does (Planned):* accepts and stores it, retrievable later by referral identifier. The ODE referral and this notification use **one endpoint** (owner's decision).

**I2 — CRD, DTR and PAS to the payer.**
- *You do, in order:* (1) call the CRD `order-sign` service with the three-procedure order (D3320, D2950, D2740 on tooth #4); (2) retrieve the DTR documentation requirement; (3) publish your supporting notes and images as an ARex manifest and submit the PAS `Claim` (`use: preauthorization`, three service lines) referencing it (§2c step 2).
- *The test server does (Planned):* returns a fixed "prior authorization required" card; serves a fixed `Questionnaire`; retrieves each ARex object and verifies its digest; returns a `ClaimResponse` with `outcome: complete`, an approved disposition, and a PA number and 180-day validity period as in §2a step 5 and the §3 payer stub bar. The test server can also **publish ARex manifests for testing** (owner's decision), so you can test retrieving from it as well as being retrieved from.
- *How the Claim points at the manifest (local convention, not an ARex or PAS rule):* `Claim.identifier` repeats the manifest's transaction-context business identifier, and `Claim.supportingInfo` also references the manifest `List` directly under a local category, because the PAS `Claim` profile does not allow a `List` in its standard supporting-information slice. See the [UC07 data README](../../fhir-resources/purpose-built/uc07-pediatric-rootcanal/README.md).
- *Known PAS conformance error in the test data (kept on purpose, and feedback for the PAS authors):* the PAS `Claim` profile requires `item.productOrService` to come from a value set that has no CDT codes, so the validator reports an error on each of the three CDT service lines. This is expected. An interim OHIA overlay profile that differs from PAS only in accepting CDT there is in `ohia-fhir-test-server/ig-overlay/` (draft, not part of PAS); whether the I2 `Claim` claims it is an open owner decision.
- *Failure cases worth exercising* (from the I2 narrative): digest mismatch, expired grant, unreachable manifest. The test server's behavior for each is **TBD**.
- *TBD:* the CRD service URL, how the DTR requirement is retrieved, the PAS submit path, and the ARex retrieval authorization.

**I4 — closed loop to the referring practice.**
- *You do:* push the post-treatment package to the test server (§2c step 4): `ClinicalImpression`, the post-op imaging reference (an `ImagingStudy` pointer plus an ARex manifest of the radiograph, whose business identifier is the **same referral id** as the I1 manifest, so a search by referral id returns both manifests), a `DocumentReference` clinical note, a **separate** thank-you `Communication`, and a `CarePlan`.
- *The test server does (Planned):* stores the package, files the clinical items as clinical content and the thank-you as a courtesy communication (the test in the I4 narrative), then marks the referral `ServiceRequest` completed and closes the `Task` (§2b step 6).

### 8.4 Validation feedback

For ODE referral content the test server **validates against the draft ODE profiles but always accepts and stores the submission, and returns the validation results in the response**. A validation error is a finding about the draft, not a rejection. The response format is **TBD**; loading the draft profiles is **Planned**.

### 8.5 Patient view of prior authorizations (CMS-0057) — OPTIONAL, owner-directed addition

**Optional for this event.** Under CMS-0057 the payer's Patient Access API must let the patient see their prior authorizations. **Planned:** the test server, as payer, exposes the approved PA to the patient using the PDex Prior Authorization profile (`ExplanationOfBenefit`, `use: preauthorization`) through a patient-scoped SMART standalone launch. All details are **TBD**. This is **not in the UC07 narrative, and §5 above says UC07 has no patient-facing app**; §5 would need to change if this is kept.

### 8.6 What you must prepare

- The test data you send. **UC07 test data exists for I1, I2 and I4** (DRAFT): see [`purpose-built/uc07-pediatric-rootcanal/`](../../fhir-resources/purpose-built/uc07-pediatric-rootcanal/), which includes a cumulative Bundle per interaction. I3 and I5 are not authored (deferred); I4 includes a minimal treatment `Encounter` and the three `Procedure`s that the guide lists under I3, so its Bundle has no consult `Encounter` or `Consent`. `README-fhir.md` describes a 71-file set that is not on any branch and does not describe this folder. For the interactions not yet authored, build your payloads from the Resource Index in §4 and the interaction write-ups.
- Anything the test server must call (for example your ARex content endpoint in I2): the URL and its authorization, **TBD**.
- The test server's base URL(s) and credentials, **TBD**, to be published before the event.

### 8.7 Open items on this section

| Item | Owner | Status |
|---|---|---|
| Base URLs and authentication | Test server team | TBD |
| The WADO-RS model in §6b and `CLAUDE.md` §8 is deferred, not removed (the `ImagingStudy`-to-manifest link is decided: see 8.3) | Owner | Deferred |
| CRD, DTR, PAS paths and failure-case behavior | Test server team | TBD |
| Patient Access PA view (8.5), and its effect on §5 if kept | Owner | Optional |
| UC07 test data: I1, I2 and I4 present (DRAFT; I4 holds a minimal pull-in from I3), I3 and I5 deferred | Owner | Partly open |
| PAS `Claim.item.productOrService` binding excludes CDT, and `Claim.supportingInfo` cannot reference an ARex `List` (kept as known errors / a local convention) | Owner to raise with the PAS authors | Open |
