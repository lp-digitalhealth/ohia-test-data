# CMS Connectathon — Dental Interoperability Test Dataset
## Use Case: Pediatric Referral for Root Canal Therapy, Build-Up, and Crown on Tooth #4
### Pediatric Dentist Referral → Restorative Dentist Review → Prior Authorization → Treatment → Closed-Loop Summary Return

---

## Table of Contents

- [About This Use Case](#about-this-use-case)
- [Use Case A: DentaQuest Texas — Medically Necessary Root Canal Therapy, Build-Up, and Crown with Prior Authorization](#use-case-a-dentaquest-texas)
  - [Section I: Business Overview](#section-i-business-overview)
  - [Section II: Narrative-to-Standards Mapping](#section-ii-narrative-to-standards-mapping)
  - [Section III: Technical Overview](#section-iii-technical-overview)
  - [Section IV: EDI Transactions](#section-iv-edi-transactions)
  - [Appendix A: Data](#appendix-a-data)

---

## About This Use Case

This use case models a **pediatric dentist–to–general dentist referral** for **root canal therapy, a core build-up, and a full-coverage crown** on a restorable tooth with pulpal decay and periapical infection. A 16-year-old DentaQuest member (Texas Medicaid dental plan) presents to his pediatric dental provider with pain on chewing and cold sensitivity on the upper right. Examination and radiographs show decay extending to the pulp and a periapical infection on tooth #4. Because the tooth is **restorable**, the pediatric provider refers the patient for endodontic and restorative treatment rather than extraction.

Three features distinguish this use case:

- **Diagnostic-quality images are viewed through DICOMweb.** The referral package includes radiographs, and the receiving dentist views the high-quality images in DICOMweb rather than relying on compressed copies embedded in the referral.
- **The referring dentist notifies the payer directly.** In parallel with the provider-to-provider referral, the pediatric practice sends a structured referral notification to DentaQuest so the payer is aware of the coordinated episode of care before a prior authorization or claim arrives, supporting efficient claims payment.
- **Prior authorization covers a bundled treatment plan.** Da Vinci CRD, DTR, and PAS are exercised for root canal therapy, build-up, and crown together, and the supporting clinical notes and images DentaQuest requires are delivered through the Attachment Reference Exchange (ARex).

The use case is set in **Texas**, where Joe is a member of the **DentaQuest** dental plan, one of the dental plans contracted by the Texas Health and Human Services Commission (HHSC) to deliver Medicaid dental benefits. Da Vinci CDex carries the provider-to-provider referral, the provider-to-payer notification, and the post-treatment summary return.

**OHIA Strategic Priorities Exercised:** Connect (dental-to-dental referral with structured clinical data and image exchange); Streamline (prior authorization via CRD/DTR/PAS, payer awareness notification, and attachment exchange that reduce claims friction).

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---
---

# Use Case A: DentaQuest Texas

## Medically Necessary Root Canal Therapy, Build-Up, and Crown on Tooth #4 with Prior Authorization
### DentaQuest | Texas Medicaid Dental | Da Vinci PAS | Dental-to-Dental Referral | Texas

---

## Section I: Business Overview

**Joe Castle** is a 16-year-old male (DOB: 03/22/2010) and a member of **DentaQuest**, his Texas Medicaid dental plan (HHSC Dental Services program). Joe has a Main Dentist (Dr. Mary Parker) who coordinates his dental care and refers him to a contracted specialist or general dentist as needed; no referral authorization is required to see a contracted provider. Joe presents with **pain while chewing on the top right** and **sensitivity to cold**.

**Dr. Mary Parker, DDS**, the pediatric dental provider, performs a **limited oral evaluation** (`D0140`), obtains a **periapical radiograph** (`D0220`), and obtains a **bitewing radiograph** (`D0270`). The examination reveals:

- Mesial-occlusal-buccal (MOB) decay extending to the pulp
- Periapical radiolucency on radiograph
- Periapical infection associated with **tooth #4** (maxillary right second premolar; FDI 15)

After reviewing the findings, Dr. Parker determines that tooth #4 is **restorable** and recommends **root canal therapy** (`D3320`), a **build-up** (`D2950`), and a **crown** (`D2740`).

Dr. Parker refers Joe to **Dr. Max Garcia, DDS**, for root canal therapy and restorative treatment. The **referral package** — clinical notes, radiographs, and the proposed treatment plan — is transmitted electronically. Because the package includes images, Dr. Garcia views the **high-quality images in DICOMweb**. Dr. Parker also sends a **structured referral notification to DentaQuest**. That awareness supports seamless coordination between the treating providers and the payer and helps ensure claims can be paid efficiently.

Upon receiving the referral, Dr. Garcia reviews the clinical documentation, imaging, and recommended treatment plan to confirm the diagnosis and proposed course of care. As part of the coverage determination workflow, his practice invokes **Da Vinci Coverage Requirements Discovery (CRD)** to determine coverage requirements. Upon confirmation that a **prior authorization is needed**, his office uses **Da Vinci Documentation Templates and Rules (DTR)** to determine what is needed to approve the proposed treatment. DentaQuest informs Dr. Garcia's office that, as part of the request, **clinical notes documenting medical necessity and images are required**. His office then electronically submits the **prior authorization** to DentaQuest, which reviews the request and **approves** it.

Dr. Garcia's office sets an appointment with Joe. At the **consultation**, Dr. Garcia reviews Joe's records, confirms the diagnosis, reviews Joe's medical history and current medications for surgical risk, and has his staff confirm that **Joe's DentaQuest coverage remains active** and review benefits used to date. Joe, with his mother and guardian **Linda Castle**, discusses the risks and benefits of the proposed treatment with Dr. Garcia, and Linda provides consent on Joe's behalf.

Dr. Garcia completes the procedures. A **structured post-treatment summary** is transmitted back to Dr. Parker via **CDex provider-to-provider push**, giving the referring practice a complete record of the treatment and healing status. The transmission includes the **post-operative radiograph**, a **clinical note**, and a **separate note thanking Dr. Parker for the referral**.

---

## Section II: Narrative-to-Standards Mapping

| What Happens (Business Language) | Implementation Guide / Standard | Key Transaction |
|---|---|---|
| **Evaluation and radiographs:** Dr. Parker performs a limited oral evaluation and obtains a periapical radiograph and a bitewing. | US Core / ODE (Under Development) | `Encounter` (POS 11); `Procedure` (D0140, D0220, D0270); `ImagingStudy` for each radiograph. |
| **Findings and diagnosis documented:** MOB decay to the pulp, periapical radiolucency, and periapical infection on tooth #4 are recorded. | US Core / ODE (Under Development) | `Observation` (tooth #4 findings, uncoded text); `Condition` (K02.53, K04.7); `DiagnosticReport` per radiograph, coded with CDT. |
| **Restorability determined and treatment recommended:** Dr. Parker concludes tooth #4 is restorable and plans root canal therapy, build-up, and crown. | US Core / ODE (Under Development) | `DocumentReference` (clinical notes, proposed treatment plan). |
| **Structured referral transmitted:** Dr. Parker sends the referral with clinical notes, radiographs, and treatment plan to Dr. Garcia. | US Core / ODE (Under Development) / Da Vinci CDex | `ServiceRequest` (referral, priority: routine); `DocumentReference`; `ImagingStudy`; `Condition`; `Bundle`; CDex provider-to-provider push to Dr. Garcia's interim FHIR server. |
| **High-quality image viewing:** Dr. Garcia views the radiographs in DICOMweb rather than compressed embedded copies. | IHE PCC Supplement 360X (referral delivery of the imaging reference) + SMART Imaging Access (retrieval pattern) | `ImagingStudy.endpoint` → WADO-RS `Endpoint` (`requires-access-token: true`); images retrieved from the referring practice's DICOMweb service and rendered in a DICOM-capable viewer. |
| **Payer awareness notification:** Dr. Parker sends a structured referral notification to DentaQuest. | Da Vinci CDex (provider-to-payer) | `Communication` referencing the `ServiceRequest`, pushed to DentaQuest's FHIR endpoint ahead of the PA and claims. |
| **Clinical review of the referral:** Dr. Garcia reviews documentation, imaging, and plan to confirm diagnosis and course of care. | US Core / ODE (Under Development) | `ServiceRequest` received via interim FHIR server; `Task` (open referral) tracked. |
| **Coverage requirements discovered:** Dr. Garcia's EHR determines that prior authorization is needed. | Da Vinci Coverage Requirements Discovery (CRD) | CDS Hook (`order-sign`) at treatment-plan order entry; returns PA requirement and documentation needs for D3320, D2950, D2740. |
| **Documentation requirements identified:** DTR determines what is needed for approval; DentaQuest requires clinical notes documenting medical necessity and images. | Da Vinci Documentation Templates and Rules (DTR) | `Questionnaire` retrieved from DentaQuest; `QuestionnaireResponse` pre-populated from EHR data; `Task` (documentation requirement). |
| **Prior authorization submitted:** Dr. Garcia's office submits the PA electronically to DentaQuest with the required notes and images. | Da Vinci PAS + Attachment Reference Exchange (ARex) | `Claim` (use: preauthorization) with CDT codes, tooth number, and diagnoses; supporting notes and images delivered as an ARex Manifest referenced from the `Claim`. |
| **Prior authorization approved:** DentaQuest reviews and approves. | Da Vinci PAS | `ClaimResponse` with PA number, approved services, and validity period; DTR `Task` closed. |
| **Appointment set:** Dr. Garcia's office schedules Joe. | US Core | `Appointment`. |
| **Consultation:** Dr. Garcia reviews records, confirms the diagnosis, reviews history and medications for surgical risk, and has staff confirm active coverage and benefits used. | US Core / ODE (Under Development) | `Encounter` (consultation, POS 11); `MedicationStatement`; `Condition` confirmed; eligibility re-verified via 270/271. |
| **Guardian consent:** Joe and Linda Castle discuss risks and benefits; Linda consents. | US Core | `RelatedPerson` (Linda Castle); `Consent` referencing the proposed procedures. |
| **Treatment completed:** Dr. Garcia completes root canal therapy, build-up, and crown. | US Core / ODE (Under Development) | `Procedure` (D3320, D2950, D2740; tooth #4, FDI 15); `Encounter` (POS 11). |
| **Post-treatment summary returned:** Dr. Garcia pushes a structured summary, post-op radiograph, clinical note, and a separate thank-you note to Dr. Parker. | Da Vinci CDex / ODE (Under Development) | `ClinicalImpression` (treatment and healing status); `ImagingStudy` (post-op radiograph); `DocumentReference` (clinical note); `Communication` (thank-you); `CarePlan`; CDex push to Dr. Parker's FHIR endpoint. |
| **Referral closed:** Dr. Parker's practice reviews the summary; referral marked complete. | US Core / Da Vinci CDex | `ServiceRequest` → `completed`; `Task` closed. |
| **Claims submission:** Each practice bills DentaQuest for its services. | X12 837D | 837D (pediatric practice): D0140, D0220, D0270; 837D (restorative practice): D3320, D2950, D2740 with PA number. |

---

## Section III: Technical Overview

This use case exercises a **dental-to-dental referral with prior authorization, DICOMweb image viewing, and payer awareness notification**, spanning a pediatric dental practice, a general dental practice, and DentaQuest as Joe's dental plan. It tests the full lifecycle from structured referral through coverage discovery, documentation, prior authorization, treatment, and closed-loop summary return — for a **bundled, multi-procedure CDT treatment plan** whose supporting evidence is clinical notes and images.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

### Implementation Guides

| Implementation Guide | Purpose in This Use Case |
|---|---|
| **US Core IG** | FHIR profiles for clinical data exchanged between the two practices and DentaQuest |
| **Da Vinci Clinical Data Exchange (CDex)** | Three roles: (1) provider-to-provider referral push from the pediatric practice to the restorative practice; (2) provider-to-payer referral notification to DentaQuest; (3) post-treatment summary return to the pediatric practice |
| **IHE PCC Supplement 360X** | Delivery of the imaging reference (`ImagingStudy`) as part of the referral package |
| **SMART Imaging Access (Argonaut Project)** | Retrieval pattern for diagnostic-quality images: the receiving dentist queries `ImagingStudy` and pulls DICOM data from a WADO-RS endpoint using the authorization already granted for the referral, with no separate imaging login. Draft CI build; canonical `http://fhir.org/argonaut/smart-imaging/ImplementationGuide/fhir.argonaut.smart-imaging` |
| **Da Vinci Coverage Requirements Discovery (CRD)** | Fired at treatment-plan order entry in Dr. Garcia's EHR; determines that PA is required and what is needed for D3320, D2950, and D2740 |
| **Da Vinci Documentation Templates and Rules (DTR)** | Retrieves DentaQuest's questionnaire, pre-populates it from EHR data, and identifies that clinical notes and images are required |
| **Da Vinci Prior Authorization Support (PAS)** | Submits the PA request to DentaQuest and receives the `ClaimResponse` with PA approval and PA number |
| **Attachment Reference Exchange (ARex)** (Onyx Technology; draft/provisional; canonical `http://fhir.onyxhealth.io/us/arex/ImplementationGuide/onyx.fhir.us.arex`) | Delivers the PA's supporting notes and images out-of-band as a signed, digest-verified manifest of individually retrievable content objects, avoiding inline base64 attachments in the PAS transaction |
| **Oral Health Data Exchange IG (ODE)** | Under development; governs structured exchange of tooth-level findings, CDT-coded procedures, radiographic findings, and the post-treatment summary between the two dental practices |

---

### Key FHIR Resources Exercised

| FHIR Resource | Source IG / Profile | Purpose in This Use Case |
|---|---|---|
| `Patient` | US Core | Joe Castle's identity across the pediatric practice, restorative practice, and DentaQuest |
| `RelatedPerson` | US Core | Linda Castle, mother and guardian; consenting party for a minor |
| `Consent` | US Core | Guardian consent for root canal therapy, build-up, and crown |
| `Coverage` | US Core | DentaQuest Texas Medicaid dental plan |
| `Practitioner` / `PractitionerRole` | US Core | Dr. Parker (pediatric dentistry); Dr. Garcia (general dentist) |
| `Organization` | US Core | Pediatric practice; restorative practice; DentaQuest (payer) |
| `Location` / `Endpoint` | US Core | Practice locations (POS 11); FHIR and WADO-RS endpoints |
| `Encounter` | US Core | Limited oral evaluation; consultation; treatment |
| `Condition` | US Core / ODE | K02.53; K04.7 (tooth #4) |
| `Observation` | US Core / ODE | MOB decay and periapical radiolucency findings |
| `DiagnosticReport` | US Core / ODE | Periapical and bitewing reports, coded with CDT |
| `ImagingStudy` | US Core / SMART Imaging Access | Periapical, bitewing, and post-op radiographs retrieved via WADO-RS |
| `DocumentReference` | US Core | Clinical notes, proposed treatment plan, post-treatment clinical note |
| `MedicationStatement` | US Core | Current medications reviewed for surgical risk |
| `ServiceRequest` | US Core / ODE | Dental-to-dental referral; lifecycle `active` → `completed` |
| `Communication` | US Core / CDex | Payer awareness notification; thank-you note to the referring dentist |
| `Questionnaire` / `QuestionnaireResponse` | Da Vinci DTR | DentaQuest documentation requirements and pre-populated responses |
| `Claim` (PA) | Da Vinci PAS | PA request for D3320, D2950, D2740 |
| `ClaimResponse` | Da Vinci PAS | PA approval with PA number |
| ARex Manifest and Provenance | ARex | Supporting notes and images for the PA; signed manifest |
| `Appointment` | US Core | Restorative consultation and treatment appointment |
| `Procedure` | US Core / ODE | D0140, D0220, D0270, D3320, D2950, D2740 |
| `ClinicalImpression` | ODE | Post-treatment summary with treatment and healing status |
| `CarePlan` | US Core | Post-treatment follow-up |
| `Task` | Da Vinci DTR / CDex | Open DTR requirement; open referral; both closed on completion |
| `Bundle` | FHIR Core | Referral package; post-treatment summary package |
| `AuditEvent` / `Provenance` | US Core | Cross-organizational access logging, including image retrieval; chain of custody |

---

### Cross-Cutting Test Objectives

1. **DICOMweb image viewing in a dental referral** — Tests whether a receiving dental practice can retrieve and render diagnostic-quality radiographs from a WADO-RS endpoint referenced by an `ImagingStudy` (reference delivered via 360X, retrieval per SMART Imaging Access) instead of relying on compressed images embedded in a `DocumentReference`.

2. **Direct provider-to-payer referral notification** — Tests whether a structured notification sent to DentaQuest in parallel with the provider-to-provider referral is received and later associated with the PA request and claims, validating a pattern intended to reduce claims friction.

3. **CRD, DTR, and PAS for a bundled CDT treatment plan** — Tests whether Da Vinci CRD, DTR, and PAS evaluate and adjudicate root canal therapy, build-up, and crown as one coordinated authorization for a dental benefit, rather than three independent procedure-level requests.

4. **Attachment exchange for PA supporting documentation** — Tests whether clinical notes and images required by DentaQuest can be delivered through an ARex manifest referenced from the PAS `Claim`, retrieved by the payer with per-object digest verification.

5. **PA number carried through to the claim** — The PA number returned in the `ClaimResponse` must appear on the restorative practice's 837D, validating PA approved → PA number on 837D → claim adjudicated with PA reference.

6. **Dental-to-dental referral with full clinical and imaging package** — Tests whether a CDex push can carry clinical notes, treatment plan, and DICOMweb-referenced imaging so the receiving dentist does not repeat diagnostic imaging.

7. **Closed-loop return with a distinct courtesy communication** — Tests whether a structured summary, post-op radiograph, and clinical note can travel with a separate, non-clinical thank-you `Communication` in the same CDex push and be correctly distinguished by the receiving system.

8. **Guardian consent for a minor** — Tests `RelatedPerson` and `Consent` for a 16-year-old whose guardian consents to treatment.

9. **ODE IG validation for endodontic and restorative referral** — Exercises ODE profiles for tooth-level findings, CDT-coded procedures, and post-treatment summary exchange for a workflow not previously tested with the full ODE profile suite.

---

## Section IV: EDI Transactions

Joe's dental plan is **DentaQuest** (Texas Medicaid dental program, administered under contract with HHSC). All dental services are billed via 837D. The prior authorization workflow uses Da Vinci PAS (FHIR-native).

### EDI Transactions in Scope

| X12 Transaction | Trigger | Scope Note |
|---|---|---|
| **270 / 271** — Eligibility & Benefit Inquiry / Response | Dr. Garcia's staff confirm DentaQuest coverage remains active and review benefits used to date at the consultation | Confirms active enrollment, benefit limits used, and covered services |
| **837D** — Dental Claim (Pediatric Practice) | Pediatric practice bills DentaQuest for the evaluation and radiographs | CDT D0140, D0220, D0270; tooth #4; POS 11 |
| **837D** — Dental Claim (Restorative Practice) | Restorative practice bills DentaQuest for root canal therapy, build-up, and crown | CDT D3320, D2950, D2740; tooth #4; POS 11; PA number on claim |
| **835** — Remittance Advice | DentaQuest adjudicates and pays both claims | Texas Medicaid dental fee schedule rates; adjustment reason codes |

> **Payer routing note:** DentaQuest's clearinghouse Payer ID for electronic dental claims is `CX014`, as published in DentaQuest's Texas provider manuals. DentaQuest is a payer and does not carry an NPI.

> **DentaQuest Texas note:** Per DentaQuest's Texas prior authorization guidance, standard requests are decided within 3 business days (expedited: 1 business day), incomplete requests trigger notice within 3 business days, and approved authorizations are valid for 180 days. Specific documentation rules for D3320, D2950, and D2740 should be confirmed against the current TX HHSC Provider Office Reference Manual and Authorization Catalog at implementation time.

### CDT Codes in Scope

| CDT Code | Description | Provider | POS | Medicaid Coverage Note |
|---|---|---|---|---|
| `D0140` | Limited oral evaluation — problem focused | Pediatric dental practice | 11 | Covered |
| `D0220` | Periapical radiographic image — first | Pediatric dental practice | 11 | Covered |
| `D0270` | Bitewing — single radiographic image | Pediatric dental practice | 11 | Covered |
| `D3320` | Endodontic therapy, premolar tooth (excluding final restoration) | Restorative dental practice | 11 | Covered — medically necessary; PA required |
| `D2950` | Core buildup, including any pins when required | Restorative dental practice | 11 | Covered; PA required as part of bundled plan |
| `D2740` | Crown — porcelain/ceramic | Restorative dental practice | 11 | Covered; PA required as part of bundled plan |

### DiagnosticReport Coding — CDT, Not LOINC

This is a dental-benefit-only episode with no medical-benefit submission, so **LOINC is not used anywhere in this workflow**. `DiagnosticReport.code` carries an extensible LOINC binding in US Core, which permits system-specific codes when no suitable LOINC concept exists; CDT (`http://www.ada.org/cdt`) is the HIPAA-mandated dental code set and the vocabulary dental practice systems actually use. Each radiographic `DiagnosticReport` is therefore coded with the same CDT code as its corresponding `Procedure` (`D0220` periapical; `D0270` bitewing). LOINC would become relevant only if a procedure were submitted for adjudication under a medical benefit.

---

## Appendix A: Data

### 1. Patient Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Name** | Joe Castle | Given: Joe; Family: Castle |
| **Date of Birth** | 2010-03-22 | Age: 16 |
| **Sex** | Male | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **Pediatric Practice MRN** | `PEDDENT-TX-2026-0019` | System: `https://pediatricdental.example.org/fhir/mrn` |
| **Restorative Practice MRN** | `RESTORE-TX-2026-0026` | System: `https://restorativedental.example.org/fhir/mrn` |
| **Texas Medicaid ID** | `TX-MCD-0038211` | System: `http://texas.medicaid.gov/beneficiary` |
| **Guardian** | Linda Castle (mother) | See `RelatedPerson` below |
| **Telecom (Phone)** | (512) 555-0198 | Use: Mobile — guardian contact |
| **Telecom (Email)** | linda.castle@example.com | Use: Home — guardian contact |
| **Address** | 918 South Congress Avenue, Apt 6, Austin, TX 78704 | City: Austin; State: TX; ZIP: 78704 |
| **Language** | English | Preferred language |
| **Active** | True | Patient record is active |

### RelatedPerson — Linda Castle (Guardian)

| FHIR Element | Value | Notes |
|---|---|---|
| **Relationship** | Mother / Legal Guardian | `http://terminology.hl7.org/CodeSystem/v2-0131` |
| **Name** | Linda Castle | Given: Linda; Family: Castle |
| **Telecom (Phone)** | (512) 555-0198 | Mobile |
| **Role in Use Case** | Consenting party for treatment | Minor patient |

---

### 2. Coverage Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Plan** | DentaQuest — Texas Medicaid dental plan (TX HHSC Dental Services) | Medicaid (not CHIP); Texas Health Steps (EPSDT) eligible |
| **Dental Plan (Payer)** | DentaQuest USA Insurance Company, Inc. | Real legal entity; one of the Texas HHSC-contracted dental plans administering the Medicaid/CHIP dental carve-out |
| **Medicaid ID** | TX-MCD-0038211 | Texas Medicaid beneficiary ID |
| **Coverage Period** | 2026-01-01 – 2026-12-31 | Benefit year |
| **Status** | Active | Re-confirmed at consultation |
| **Prior Authorization Required** | Yes — D3320, D2950, D2740 (bundled plan) | Confirmed via CRD at order entry |
| **Payer ID** | `CX014` | DentaQuest clearinghouse Payer ID (X12 837D routing) |
| **Payer FHIR Endpoint** | `https://dentaquest-tx.example.org/fhir/r4` | Synthetic FHIR API |

---

### 3. Organization Resource Data

#### Pediatric Dental Practice (Texas)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1847736208 | `http://hl7.org/fhir/sid/us-npi` (synthetic, Luhn-valid, Type 2) |
| **Organization Name** | Pediatric Dental Practice — Texas (Synthetic) | Test data label |
| **Type** | Pediatric Dental Practice | Organization type |
| **Care Setting** | Place of Service 11 — Office | In-office |
| **Practice Management System** | Dental PMS with interim FHIR server and DICOMweb (WADO-RS) service | Architecture pattern |
| **FHIR Endpoint** | `https://pediatricdental.example.org/fhir/r4` | Interim FHIR server |
| **DICOMweb Endpoint** | `https://pediatricdental.example.org/dicomweb` | WADO-RS base URL for the referral radiographs; `requires-access-token: true` |
| **NPI Taxonomy Code** | 1223P0221X | Pediatric dentistry |

#### Restorative Dental Practice (Texas)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 2936518473 | `http://hl7.org/fhir/sid/us-npi` (synthetic, Luhn-valid, Type 2) |
| **Organization Name** | Restorative Dental Practice — Texas (Synthetic) | Test data label |
| **Type** | General Dental Practice (Restorative/Endodontic) | Organization type |
| **Care Setting** | Place of Service 11 — Office | In-office |
| **Practice Management System** | Dental PMS with interim FHIR server and DICOMweb (WADO-RS) service | Architecture pattern |
| **FHIR Endpoint** | `https://restorativedental.example.org/fhir/r4` | Interim FHIR server |
| **DICOMweb Endpoint** | `https://restorativedental.example.org/dicomweb` | WADO-RS base URL for the post-op radiograph; `requires-access-token: true` |
| **NPI Taxonomy Code** | 1223G0001X | General dentist |

#### DentaQuest USA Insurance Company, Inc. (Payer)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | DentaQuest USA Insurance Company, Inc. | Real legal entity, used as the payer identity |
| **Type** | Payer (`pay`) | `http://terminology.hl7.org/CodeSystem/organization-type`; payers carry no NPI |
| **Identifier — Payer ID** | `CX014` | Clearinghouse Payer ID; no universal FHIR system URI exists for payer IDs |
| **FHIR Endpoint** | `https://dentaquest-tx.example.org/fhir/r4` | Synthetic FHIR API (not a real DentaQuest endpoint) |

---

### 4. Practitioner Resource Data

#### Pediatric Dental Provider — Dr. Mary Parker, DDS

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1720384753 | `http://hl7.org/fhir/sid/us-npi` (synthetic, Luhn-valid, Type 1) |
| **Full Name** | Mary Elizabeth Parker, DDS | Given: Mary; Family: Parker |
| **Qualification** | DDS — Pediatric Dentistry | Dental degree with pediatric specialty |
| **License Number** | TX-DDS-061204 | Texas dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223P0221X | Pediatric dentistry |
| **Organization** | Pediatric Dental Practice — Texas | Employment |
| **Role in Use Case** | Referring provider; recipient of post-treatment summary | Evaluation; radiographs; referral; payer notification |

#### Restorative Dentist — Dr. Max Garcia, DDS

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1839204769 | `http://hl7.org/fhir/sid/us-npi` (synthetic, Luhn-valid, Type 1) |
| **Full Name** | Maximilian Garcia, DDS | Given: Max; Family: Garcia |
| **Qualification** | DDS — Doctor of Dental Surgery | General dentist |
| **License Number** | TX-DDS-073392 | Texas dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223G0001X | General dentist |
| **Organization** | Restorative Dental Practice — Texas | Employment |
| **Role in Use Case** | Receiving provider; submits PA; performs treatment; sends summary | CRD/DTR/PAS; consultation; treatment |

---

### 5. Workflow & Service Data

#### ServiceRequest (Referral — Pediatric Practice to Restorative Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Referral fulfilled (set `active` at transmission) |
| **Intent** | Order | Clinical order |
| **Category** | Consultation / Referral | Type |
| **Priority** | Routine | Non-urgent |
| **Code** | Root canal therapy, build-up, and crown — tooth #4 | Referral reason |
| **Subject** | Joe Castle | Patient reference |
| **Requester** | Dr. Mary Parker, DDS | Pediatric dental provider |
| **Performer** | Dr. Max Garcia, DDS | Restorative dentist |
| **Reason Code** | K02.53; K04.7 | ICD-10 diagnoses |
| **Supporting Info** | `ImagingStudy` (periapical, bitewing — WADO-RS retrievable); `DocumentReference` (clinical notes, proposed treatment plan) | Referral package |
| **Authored On** | 2026-07-08 | Referral date |
| **Description** | MOB decay extending to the pulp and periapical infection on tooth #4; tooth determined restorable. Package includes clinical notes, periapical and bitewing radiographs, and proposed treatment plan (D3320, D2950, D2740). Receiving dentist to confirm diagnosis, review history and medications, and proceed with treatment. | Referral payload |

#### Communication (Referral Notification — Pediatric Practice to DentaQuest)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Delivered |
| **Category** | Care coordination notification | Not a claim or PA request |
| **Subject** | Joe Castle | Patient reference |
| **Sender** | Dr. Mary Parker, DDS (Pediatric Dental Practice) | Referring provider |
| **Recipient** | DentaQuest USA Insurance Company, Inc. | Payer |
| **Based On** | `ServiceRequest` (referral) | Links notification to referral |
| **Payload** | "Patient referred to Dr. Max Garcia, DDS for root canal therapy and restorative treatment on tooth #4." | Structured awareness note |
| **Sent** | 2026-07-08 | Same day as referral |

#### Claim (Prior Authorization — Restorative Practice to DentaQuest)

| FHIR Element | Value | Notes |
|---|---|---|
| **Use** | Preauthorization | PA request, not a claim for payment |
| **Status** | Active | Submitted and pending |
| **Patient** | Joe Castle | Patient reference |
| **Insurer** | DentaQuest USA Insurance Company, Inc. | Payer reference |
| **Provider** | Dr. Max Garcia, DDS (Restorative Dental Practice) | Requesting provider |
| **Priority** | Normal | Routine PA |
| **Procedure Codes** | D3320; D2950; D2740 | Bundled treatment plan |
| **Tooth** | Tooth #4 (FDI 15) | Maxillary right second premolar |
| **Diagnosis** | K02.53; K04.7 | Supporting diagnoses |
| **Supporting Info** | Reference to ARex Manifest (below) | Clinical notes documenting medical necessity and images; not inlined |
| **Submitted Date** | 2026-07-10 | PA submission date |

#### ARex Manifest (PA Supporting Documentation)

| FHIR Element | Value | Notes |
|---|---|---|
| **Profile** | ARex Manifest | `http://fhir.onyxhealth.io/us/arex/StructureDefinition/arex-manifest` |
| **Status** | Active | Content available for retrieval |
| **Transaction Context** | PA request identifier | Links manifest to the `Claim` |
| **Content Entries** | (1) Periapical radiograph (CDT D0220); (2) Bitewing radiograph (CDT D0270); (3) Clinical notes documenting medical necessity | Each individually addressable `Binary` with declared digest; no inline `attachment.data` |
| **Provenance** | ARex Provenance with detached JWS over the manifest | DentaQuest verifies before acting |
| **Availability Window** | 2026-07-10 – 2026-07-24 (14 days) | Declared expiry |
| **Retrieval** | DentaQuest fetches each object under a manifest-scoped grant and verifies each digest | Grant scoped to this one PA |

#### ClaimResponse (Prior Authorization Approval)

| FHIR Element | Value | Notes |
|---|---|---|
| **Use** | Preauthorization | PA response |
| **Outcome** | Complete | PA approved |
| **Disposition** | Approved — D3320, D2950, D2740, tooth #4, Dr. Max Garcia | Approved services |
| **PA Number** | TX-DQ-PA-2026-061204 | Carried onto the restorative practice's 837D |
| **Validity Period** | 2026-07-15 – 2027-01-11 | 180-day authorization window (per DentaQuest Texas) |
| **Insurer** | DentaQuest USA Insurance Company, Inc. | Payer reference |

#### Consent (Guardian Consent for Treatment)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Active | Consent granted |
| **Category** | Treatment consent | Root canal therapy, build-up, crown |
| **Patient** | Joe Castle | Minor patient |
| **Consenting Party** | Linda Castle (mother/guardian) | `RelatedPerson` reference |
| **Provisions** | Consent to D3320, D2950, D2740 after risk/benefit discussion | Discussed at consultation |
| **Date** | 2026-07-22 | Consultation date |

#### ClinicalImpression (Post-Treatment Summary — Restorative Practice to Pediatric Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Summary complete |
| **Date** | 2026-07-22 | Date of summary |
| **Assessor** | Dr. Max Garcia, DDS | Restorative dentist |
| **Summary** | Joe Castle seen 2026-07-22 per referral from Dr. Mary Parker. Pulpal caries (K02.53) and periapical infection (K04.7) confirmed on tooth #4. Guardian consent obtained. Root canal therapy (D3320), core build-up (D2950), and crown (D2740) completed without complication. Post-operative radiograph shows adequate obturation and crown seating. Healing status: no complications at completion. | Post-treatment summary |
| **Supporting Info** | Post-operative periapical radiograph (`ImagingStudy`); clinical note (`DocumentReference`) | Sent in the same push |
| **Recommendations** | 1. Routine follow-up at the pediatric practice at next recall; 2. Monitor for post-restorative sensitivity; 3. Continue routine pediatric preventive care | Follow-up plan |

#### Communication (Referral Thank-You — Restorative Practice to Pediatric Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Delivered with the clinical summary |
| **Category** | Provider-to-provider courtesy communication | Non-clinical |
| **Sender** | Dr. Max Garcia, DDS | Restorative dentist |
| **Recipient** | Dr. Mary Parker, DDS | Referring provider |
| **Payload** | "Thank you for referring Joe Castle. Treatment was completed successfully and Joe is doing well. We appreciate the complete clinical and imaging package." | Distinct from the `ClinicalImpression` |
| **Sent** | 2026-07-22 | Same push as the summary |

---

### 6. Clinical Codes & Mappings

#### ICD-10 Diagnosis Codes

| Code | Description | Application |
|---|---|---|
| K02.53 | Dental caries on pit and fissure surface penetrating into the pulp | MOB decay extending to the pulp, tooth #4 |
| K04.7 | Periapical abscess without sinus | Periapical infection, tooth #4 |

#### CDT Codes in Scope

| Code | Description | Provider | POS |
|---|---|---|---|
| `D0140` | Limited oral evaluation — problem focused | Pediatric practice | 11 |
| `D0220` | Periapical radiographic image — first | Pediatric practice | 11 |
| `D0270` | Bitewing — single radiographic image | Pediatric practice | 11 |
| `D3320` | Endodontic therapy, premolar tooth (excluding final restoration) | Restorative practice | 11 |
| `D2950` | Core buildup, including any pins when required | Restorative practice | 11 |
| `D2740` | Crown — porcelain/ceramic | Restorative practice | 11 |

#### DiagnosticReport Codes (CDT — LOINC Not Applicable)

| Code | Description | FHIR Resource |
|---|---|---|
| `D0220` | Periapical radiographic image | `DiagnosticReport`, `ImagingStudy` |
| `D0270` | Bitewing radiographic image | `DiagnosticReport`, `ImagingStudy` |

#### Tooth Designation

| Universal | FDI | Description | Code System |
|---|---|---|---|
| #4 | 15 | Maxillary right second premolar | `http://terminology.hl7.org/CodeSystem/ADAUniversalToothDesignationSystem` |

---

### 7. Timeline & Dates

| Event | Date | Time | Actor | System |
|---|---|---|---|---|
| **Limited oral evaluation, radiographs, diagnosis, treatment plan** | 2026-07-08 | 09:30 | Dr. Parker | Pediatric dental PMS |
| **Structured referral transmitted (clinical notes, images, plan)** | 2026-07-08 | 10:15 | Dr. Parker's staff | CDex push → Restorative practice FHIR server |
| **Referral notification sent to DentaQuest** | 2026-07-08 | 10:16 | Pediatric practice system | CDex push → DentaQuest FHIR endpoint |
| **Images retrieved and viewed in DICOMweb; referral reviewed** | 2026-07-08 | 10:30 | Dr. Garcia | WADO-RS → Restorative practice DICOM viewer |
| **CRD — PA required** | 2026-07-09 | 08:00 | Restorative practice EHR | CRD → DentaQuest FHIR API |
| **DTR — notes and images required** | 2026-07-09 | 08:15 | Restorative practice EHR | DTR → DentaQuest FHIR API |
| **Prior authorization submitted; ARex manifest published** | 2026-07-10 | 09:00 | Restorative practice staff | PAS → DentaQuest; ARex |
| **DentaQuest retrieves manifest content** | 2026-07-10 | 09:05 | DentaQuest | ARex `Binary` retrieval |
| **Prior authorization approved** | 2026-07-15 | 14:00 | DentaQuest | PAS `ClaimResponse` |
| **Appointment set** | 2026-07-15 | 15:00 | Restorative practice staff | Dental PMS |
| **Consultation; eligibility re-verified; guardian consent** | 2026-07-22 | 09:30 | Dr. Garcia and staff | 270/271; Restorative practice PMS |
| **Root canal, build-up, and crown completed** | 2026-07-22 | 10:00 | Dr. Garcia | Restorative practice PMS |
| **Post-treatment summary, post-op radiograph, clinical note, thank-you note sent** | 2026-07-22 | 13:30 | Restorative practice system | CDex push → Pediatric practice FHIR server |
| **Referral closed** | 2026-07-22 | 13:35 | Pediatric practice system | `ServiceRequest` → completed |
| **837D submitted — pediatric practice** | 2026-07-23 | 08:00 | Billing | D0140, D0220, D0270 → DentaQuest |
| **837D submitted — restorative practice** | 2026-07-23 | 08:30 | Billing | D3320, D2950, D2740 + PA number → DentaQuest |

#### Key Timeline Constraints

| Constraint | Target | Rationale |
|---|---|---|
| **Referral transmission** | Same day as evaluation | Avoids repeat imaging |
| **Payer notification** | Same window as referral | Payer visibility ahead of PA and claims |
| **CRD/DTR** | Next business day after referral receipt | Confirms PA and documentation needs before scheduling |
| **PA turnaround** | Within 5 business days of submission | Routine PA |
| **Treatment** | Within 10 days of PA approval | Routine; pain manageable |
| **Summary return** | Same day as treatment | Closes the referral loop |
