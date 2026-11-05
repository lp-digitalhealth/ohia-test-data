# CMS Connectathon — Dental Interoperability Test Dataset
## Use Case: Pediatric Restorative Referral for Root Canal Therapy on Tooth #4
### Pediatric Dentist Referral → Endodontic/Restorative Consultation → Prior Authorization → Closed-Loop Summary Return

---

## Table of Contents

- [About This Use Case](#about-this-use-case)
- [Use Case A: Texas Medicaid — Medically Necessary Root Canal Therapy with Prior Authorization](#use-case-a-texas-medicaid)
  - [Section I: Business Overview](#section-i-business-overview)
  - [Section II: Narrative-to-Standards Mapping](#section-ii-narrative-to-standards-mapping)
  - [Section III: Technical Overview](#section-iii-technical-overview)
  - [Section IV: EDI Transactions](#section-iv-edi-transactions)
  - [Appendix A: Data](#appendix-a-data)

---

## About This Use Case

This use case models a **pediatric general dentist–to–general dentist (restorative/endodontic) referral** for **root canal therapy, core build-up, and a full-coverage crown** on a restorable but infected tooth — one of the most common referral pathways in pediatric and general dental care. A 16-year-old patient presents to his pediatric dental provider with pain on chewing and cold sensitivity on the upper right side. Examination and radiographs reveal decay extending to the pulp and a periapical infection on tooth #4. Because the tooth is determined to be **restorable**, the pediatric provider refers the patient — rather than extracting the tooth — to a general dentist for endodontic and restorative treatment.

This use case is distinguished from the companion tooth-extraction use case set by three features:

- The referral package includes **diagnostic-quality radiographic images exchanged via DICOMweb**, which the receiving provider views directly in a high-fidelity image viewer rather than relying on embedded/compressed images in the clinical document package.
- The referring provider sends a **structured referral awareness notification directly to the dental payer (DentaQuest)**, in parallel with the provider-to-provider referral, so the payer has visibility into the coordinated episode of care before a claim is filed — supporting downstream claims efficiency.
- The patient is a **minor**, so consent for treatment, coverage inquiries, and portions of patient-facing notification are exercised through a **parent/guardian**, testing the represented-patient pattern for FHIR resources and SMART App Launch proxy access.

The use case is set in **Texas** and is administered under **Texas Medicaid**, with **DentaQuest** as the dental benefit administrator. **Da Vinci CRD, DTR, and PAS** govern the prior authorization workflow, and **Da Vinci CDex** carries both the provider-to-provider referral/summary exchange and the provider-to-payer notification.

**OHIA Strategic Priorities Exercised:** Connect (dental-to-dental provider referral with structured data and image exchange); Streamline (real-time eligibility verification, prior authorization via PAS, and payer awareness notification to reduce claims friction); Empower (guardian/patient application tracking of referral status, prior authorization status, and clinical/claims updates for a pediatric beneficiary).

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---
---

# Use Case A: Texas Medicaid

## Medically Necessary Root Canal Therapy, Build-Up, and Crown on Tooth #4 with Prior Authorization
### Texas Medicaid | DentaQuest | Da Vinci PAS | Dental-to-Dental Referral | Texas

---

## Section I: Business Overview

**Joe Castle** is a 16-year-old male (DOB: 03/22/2010) enrolled in **Texas Medicaid**, with dental benefits administered by **DentaQuest**. Joe is accompanied by his mother and guardian, **Linda Castle**. Joe presents to his pediatric dental provider with **pain while chewing on the upper right side** and **sensitivity to cold**.

**Dr. Mary Parker, DDS**, the pediatric dental provider, performs a **limited oral evaluation** (`D0140`), obtains a **periapical radiograph** (`D0220`), and obtains a **bitewing radiograph** (`D0270`). The examination reveals:

- Mesial-occlusal-buccal (MOB) decay extending to the pulp
- Periapical radiolucency on radiograph
- Periapical infection associated with **tooth #4** (maxillary right first premolar; FDI 15)

After reviewing the findings, Dr. Parker determines that **tooth #4 is restorable** and recommends **root canal therapy** (`D3320`), a **core build-up** (`D2950`), and a **crown** (`D2740`) rather than extraction.

Dr. Parker refers Joe to **Dr. Max Garcia, DDS**, for root canal therapy and restorative treatment. The **referral package** — including clinical notes, radiographs, and the proposed treatment plan — is transmitted electronically. Because the package includes diagnostic images, Dr. Garcia's practice retrieves and views the **high-quality radiographic images via DICOMweb** rather than relying on compressed images embedded in the document package. In parallel, Dr. Parker's practice sends a **structured referral awareness notification directly to DentaQuest**, so the payer has visibility into the coordinated episode before any claim is filed, supporting efficient claims adjudication for both practices.

Upon receiving the referral, Dr. Garcia reviews the clinical documentation, imaging, and recommended treatment plan to confirm the diagnosis and proposed course of care. As part of the coverage determination workflow, his practice invokes **Da Vinci Coverage Requirements Discovery (CRD)** to determine coverage requirements for the proposed procedures. Upon confirmation that a **prior authorization is required**, his office submits **Da Vinci Documentation Templates and Rules (DTR)** to determine what supporting documentation is needed. DentaQuest informs Dr. Garcia's practice that, as part of the request, **clinical notes documenting medical necessity and diagnostic images** are required. His office electronically submits the **prior authorization** to DentaQuest, which reviews and **approves** the request.

Dr. Garcia's office schedules Joe for a consultation. At the visit, Dr. Garcia reviews Joe's records, confirms the diagnosis, reviews Joe's medical history and current medications for anesthesia/sedation risk, and has staff confirm that **Medicaid/DentaQuest coverage remains active** and review benefits used to date. Joe's guardian, Linda Castle, and Dr. Garcia discuss the risks and benefits of root canal therapy and restorative treatment, and Linda provides consent on Joe's behalf.

Dr. Garcia completes the root canal therapy, core build-up, and crown placement. A **structured post-treatment summary** is transmitted back to Dr. Parker via **CDex provider-to-provider push**, giving the pediatric practice a complete record of the endodontic and restorative treatment. The transmission includes a **post-operative radiograph**, a **clinical note**, and a **separate note thanking Dr. Parker for the referral**.

---

## Section II: Narrative-to-Standards Mapping

| What Happens (Business Language) | Implementation Guide / Standard | Key Transaction |
|---|---|---|
| **Limited oral evaluation and radiographs:** Dr. Parker examines Joe and captures a periapical radiograph and a bitewing. | US Core / ODE (Under Development) | `Procedure` (D0140, D0220, D0270); `Encounter` (POS 11); `ImagingStudy` for each radiograph. |
| **Findings and diagnosis documented:** Decay to the pulp, periapical radiolucency, and periapical infection on tooth #4 are recorded; tooth determined restorable. | US Core / ODE (Under Development) | `Observation` (radiographic findings, tooth #4); `Condition` (K02.53, K04.7); `DiagnosticReport` (radiographic report). |
| **Real-time eligibility verification:** Dr. Parker's practice verifies Joe's Texas Medicaid/DentaQuest dental eligibility and confirms Dr. Garcia's plan participation. | US Core / Da Vinci PDex / Plan-Net | `Coverage` queried against DentaQuest FHIR API; `InsurancePlan` returned with pediatric dental benefit details; `PractitionerRole` queried to confirm Dr. Garcia's DentaQuest participation. |
| **Structured referral transmitted with imaging:** Dr. Parker transmits the referral, clinical notes, radiographs, and treatment plan to Dr. Garcia. | US Core / ODE (Under Development) / CDex | `ServiceRequest` (referral, priority: routine); `DocumentReference` (clinical notes, treatment plan); `ImagingStudy` (DICOMweb-retrievable radiographs); `Condition`; CDex provider-to-provider push to Dr. Garcia's interim FHIR server. |
| **High-fidelity image retrieval:** Dr. Garcia's practice retrieves and views diagnostic-quality images rather than embedded/compressed copies. | IHE PCC — Supplement 360X (Cross-Community/DICOMweb imaging exchange for referrals) | `ImagingStudy.endpoint` referencing a DICOMweb (WADO-RS) endpoint; images rendered in a DICOM-capable viewer at the receiving practice. |
| **Structured referral awareness notification sent to payer:** Dr. Parker's practice notifies DentaQuest of the coordinated referral in parallel with the provider-to-provider push. | Da Vinci CDex (provider-to-payer notification) | `Communication` / `Task` referencing the `ServiceRequest`, pushed to DentaQuest's FHIR endpoint ahead of claims submission. |
| **Coverage requirements discovered:** Dr. Garcia's EHR surfaces a prior authorization requirement for the proposed endodontic/restorative procedures under DentaQuest. | Da Vinci Coverage Requirements Discovery (CRD) | CDS Hook (`order-sign`) triggered at treatment-plan order entry; returns PA requirement and documentation needs for D3320, D2950, and D2740. |
| **Documentation requirements identified:** Practice retrieves the PA questionnaire and pre-populates clinical data; DentaQuest specifies clinical notes documenting medical necessity and images are required. | Da Vinci Documentation Templates and Rules (DTR) | `Questionnaire` retrieved from DentaQuest; pre-populated with EHR data (diagnosis, radiographic findings, tooth number, clinical justification). |
| **Prior authorization submitted:** Dr. Garcia's practice submits the PA request to DentaQuest. | Da Vinci Prior Authorization Support (PAS) | `Claim` (PA request) submitted to DentaQuest FHIR endpoint; includes diagnosis codes, CDT codes (D3320, D2950, D2740), tooth number, and supporting clinical documentation and images. |
| **Prior authorization approved:** DentaQuest returns PA approval with a PA number. | Da Vinci PAS | `ClaimResponse` returned; PA number included; approved service details confirmed; `Task` (DTR documentation requirement) closed. |
| **Guardian/patient notified — PA approved:** Linda Castle's proxy application receives notification of PA approval on Joe's behalf. | FHIR Subscriptions Backport IG / SMART App Launch (represented-patient/proxy access) | Subscription event on `ClaimResponse` receipt; PA status surfaced in guardian-facing application. |
| **Consultation:** Dr. Garcia reviews records, confirms diagnosis, reviews medical history and medications for anesthesia/sedation risk, confirms active coverage. | US Core / ODE (Under Development) | `Encounter` (consultation, POS 11); eligibility re-verified via 270/271; `MedicationStatement`; `Condition` confirmed. |
| **Guardian consent obtained:** Linda Castle discusses risks and benefits with Dr. Garcia and consents to treatment on Joe's behalf. | US Core (RelatedPerson / Consent) | `RelatedPerson` (Linda Castle, relationship: mother/guardian); `Consent` referencing the proposed `Procedure`s. |
| **Treatment completed:** Dr. Garcia performs root canal therapy, core build-up, and crown placement. | US Core / ODE (Under Development) | `Procedure` (D3320, D2950, D2740; tooth #4, FDI 15); `Encounter` (restorative, POS 11). |
| **Post-treatment summary returned:** Dr. Garcia transmits a structured summary, post-op radiograph, and a separate thank-you note to Dr. Parker. | Da Vinci CDex / ODE (Under Development) | `ClinicalImpression` (post-treatment summary); `ImagingStudy` (post-op radiograph); `Communication` (referral acknowledgment/thank-you); CDex provider-to-provider push to Dr. Parker's FHIR endpoint. |
| **Referral closed:** Dr. Parker's practice reviews the summary; referral marked complete. | US Core / CDex | `ServiceRequest` status updated to `completed`; `Task` closed. |
| **Guardian/patient application updated:** Application shows referral complete with post-treatment summary and follow-up guidance. | FHIR Subscriptions Backport IG / US Core | Subscription event on `ServiceRequest` status change; `CarePlan` surfaced to guardian-facing application. |
| **Claims submission:** Both practices submit 837D claims to DentaQuest/Texas Medicaid. | X12 837D | 837D (restorative practice): D3320, D2950, D2740, PA number included; 837D (pediatric practice): D0140, D0220, D0270. |

---

## Section III: Technical Overview

This use case exercises a **dental-to-dental referral with prior authorization, image exchange, and payer awareness notification**, spanning a pediatric dental practice, a general/restorative dental practice, and DentaQuest (Texas Medicaid dental administrator). It extends the prior authorization pattern proven in the tooth-extraction use case set by adding **DICOMweb-based diagnostic image exchange** and a **direct provider-to-payer notification** running in parallel with the clinical referral — testing whether payer awareness of a coordinated referral, established ahead of claims submission, improves downstream claims efficiency for both practices. Because the patient is a minor, the use case also exercises **represented-patient (guardian) consent, coverage verification, and notification patterns**.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

### Implementation Guides

| Implementation Guide | Purpose in This Use Case |
|---|---|
| **US Core IG** | Defines FHIR profiles for all clinical data exchanged between the pediatric practice, the restorative practice, and DentaQuest |
| **Da Vinci Coverage Requirements Discovery (CRD)** | Fired at treatment-plan order entry in Dr. Garcia's EHR; surfaces PA requirement for D3320, D2950, and D2740 under the DentaQuest pediatric dental benefit in real time |
| **Da Vinci Documentation Templates and Rules (DTR)** | Retrieves DentaQuest's PA questionnaire; pre-populates EHR data including diagnosis, tooth number, and clinical justification; identifies that clinical notes and images are required |
| **Da Vinci Prior Authorization Support (PAS)** | Submits the completed PA request for D3320/D2950/D2740 to DentaQuest; receives `ClaimResponse` with PA approval and PA number; PA number carried forward into the claim |
| **Da Vinci Clinical Data Exchange (CDex)** | Three roles: (1) **Provider-to-provider referral push** — structured referral with clinical package and imaging references transmitted from the pediatric practice to the restorative practice; (2) **Provider-to-payer notification** — structured referral awareness notification pushed to DentaQuest ahead of claims submission; (3) **Post-treatment summary return** — structured summary, post-op image, and thank-you note pushed from the restorative practice back to the pediatric practice |
| **IHE PCC Supplement 360X** | Governs DICOMweb-based exchange and retrieval of diagnostic-quality radiographic images between the referring and receiving practices, referenced from the `ImagingStudy` resource rather than embedded as compressed images |
| **Da Vinci PDex / Plan-Net IG** | Real-time eligibility verification and confirmation of Dr. Garcia's DentaQuest network participation before the referral is created |
| **SMART App Launch IG (represented-patient/proxy access)** | Authorization framework enabling Linda Castle, as Joe's guardian, to connect a proxy application to DentaQuest's FHIR endpoint and surface PA status, referral status, and post-treatment care plan on Joe's behalf |
| **FHIR Subscriptions Backport IG** | Push notifications to the guardian-facing application at PA approval, referral creation, appointment confirmation, and referral closure |
| **Oral Health Data Exchange IG (ODE)** | Under development; governs structured exchange of oral health clinical data — tooth-level findings, CDT-coded procedures, radiographic findings, and post-treatment summary — between the two dental practices |

---

### Key FHIR Resources Exercised

| FHIR Resource | Source IG / Profile | Purpose in This Use Case |
|---|---|---|
| `Patient` | US Core | Joe Castle's identity across the pediatric practice, restorative practice interim FHIR server, and DentaQuest |
| `RelatedPerson` | US Core | Linda Castle, mother/guardian, exercised for represented-patient consent and proxy notification |
| `Consent` | US Core | Guardian consent for root canal therapy, core build-up, and crown placement, referencing the proposed `Procedure`s |
| `Coverage` | US Core / PDex | Texas Medicaid pediatric dental benefit administered by DentaQuest — Medicaid ID, plan details, benefit limitations |
| `InsurancePlan` | Da Vinci PDex | DentaQuest pediatric dental benefit structure; covered services, exclusions, and prior authorization requirements |
| `Practitioner` | US Core | Pediatric dental provider (Dr. Parker); restorative/endodontic provider (Dr. Garcia) |
| `PractitionerRole` | US Core / Plan-Net | Role context for each provider; Dr. Garcia's DentaQuest participation confirmed via Plan-Net query before the referral target is selected |
| `Organization` | US Core | Pediatric dental practice; restorative dental practice; DentaQuest |
| `Encounter` | US Core | Limited oral evaluation (pediatric practice); consultation and restorative encounter (restorative practice) |
| `Condition` | US Core / ODE | K02.53 (dental caries penetrating into pulp, tooth #4); K04.7 (periapical abscess without sinus) |
| `Observation` | US Core / ODE | Periapical radiolucency finding; MOB decay finding; tooth #4 clinical findings |
| `DiagnosticReport` | US Core / ODE | Periapical and bitewing radiograph reports |
| `ImagingStudy` | US Core | Periapical and bitewing images (referral); post-operative radiograph (summary) — retrieved via DICOMweb per IHE 360X |
| `MedicationStatement` | US Core | Patient-reported medications reviewed by Dr. Garcia for anesthesia/sedation risk assessment |
| `ServiceRequest` | US Core / ODE | Structured dental-to-dental referral for root canal therapy and restorative treatment; status lifecycle `active` → `completed` |
| `DocumentReference` | US Core | Clinical notes and proposed treatment plan transmitted as supporting documentation in the referral package |
| `Communication` | US Core / CDex | Payer awareness notification to DentaQuest; separate thank-you note returned from Dr. Garcia to Dr. Parker |
| `Questionnaire` / `QuestionnaireResponse` | Da Vinci DTR | DentaQuest PA documentation requirements; pre-populated from EHR data at DTR launch |
| `Claim` (PA) | Da Vinci PAS | Prior authorization request for D3320, D2950, and D2740 submitted to DentaQuest |
| `ClaimResponse` | Da Vinci PAS | DentaQuest PA approval response — PA number, approved services, validity period |
| `Appointment` / `AppointmentResponse` | US Core | Restorative consultation and treatment appointment created and confirmed; surfaced to guardian application |
| `Procedure` | US Core / ODE | D3320 (root canal therapy — bicuspid), D2950 (core build-up), D2740 (crown); D0140, D0220, D0270 |
| `ClinicalImpression` | ODE | Post-treatment summary from the restorative practice; includes procedure details, healing status, and follow-up recommendations |
| `CarePlan` | US Core | Post-treatment instructions and follow-up timeline; surfaced to guardian application |
| `Task` | Da Vinci DTR / CDex | Tracks open PA documentation requirement (DTR); tracks open referral (CDex); both closed on completion |
| `Subscription` / `SubscriptionStatus` | FHIR Subscriptions Backport IG | Push notifications to guardian application at PA approval, referral creation, appointment confirmation, referral closure |
| `Bundle` | FHIR Core | Referral package bundle (`ServiceRequest` + `Condition` + `Observation` + `DiagnosticReport` + `DocumentReference` + `ImagingStudy`); post-treatment summary bundle |
| `AuditEvent` | US Core | Cross-organizational data access logging, including DICOMweb image retrieval |
| `Provenance` | US Core | Chain of custody across the pediatric practice, restorative practice, and DentaQuest FHIR endpoints |

---

### Cross-Cutting Test Objectives

1. **DICOMweb image exchange in a dental referral (IHE 360X)** — Tests whether a receiving dental practice can retrieve and render diagnostic-quality radiographic images directly via a DICOMweb (WADO-RS) endpoint referenced from an `ImagingStudy` resource, rather than relying on compressed images embedded in a `DocumentReference` — a capability not previously exercised in OHIA Connectathons.

2. **Direct provider-to-payer referral awareness notification** — Tests whether a structured notification of a coordinated referral, sent to the payer in parallel with the provider-to-provider push and ahead of claims submission, is correctly received and associated with the eventual PA request and claims — validating a pattern intended to reduce claims friction and denials tied to care-coordination gaps.

3. **CRD/DTR/PAS for a multi-procedure restorative treatment plan** — Tests whether Da Vinci CRD, DTR, and PAS can correctly evaluate and adjudicate a **bundled treatment plan** (endodontic therapy, build-up, and crown) as a coordinated prior authorization rather than three independent procedure-level requests.

4. **Represented-patient (guardian) consent and notification** — Because Joe is a minor, this use case tests `RelatedPerson`, `Consent`, and SMART App Launch proxy-access patterns for a guardian acting on the patient's behalf across eligibility inquiry, consent, and application notifications.

5. **PA number carried through referral and claim** — The PA number returned in the `ClaimResponse` must be carried forward into the `ServiceRequest` (referral) and the 837D claim, validating the chain of custody: PA approved → PA number on referral → PA number on 837D → claim adjudicated with PA reference.

6. **Dental-to-dental referral with full clinical and imaging package** — Validates whether a CDex provider-to-provider push can carry a multi-resource clinical package — including DICOMweb-referenced imaging — that eliminates the need for the receiving provider to repeat diagnostic imaging.

7. **Closed-loop return with a distinct courtesy communication** — Tests whether a `ClinicalImpression`-based clinical summary and a separate, non-clinical `Communication` (thank-you/acknowledgment) can both be transmitted in the same CDex push and correctly distinguished by the receiving system.

8. **ODE IG validation for restorative/endodontic referral** — Exercises ODE profiles for tooth-level clinical findings, CDT-coded restorative and endodontic procedures, and post-treatment summary exchange — a workflow not previously tested in OHIA Connectathons with the full ODE profile suite.

---

## Section IV: EDI Transactions

Joe's dental benefit is administered by **DentaQuest** under **Texas Medicaid**. All dental services are billed via 837D under the Texas Medicaid pediatric dental fee schedule. The prior authorization workflow uses Da Vinci PAS (FHIR-native) rather than the legacy X12 278.

### EDI Transactions in Scope

| X12 Transaction | Trigger | Scope Note |
|---|---|---|
| **270 / 271** — Eligibility & Benefit Inquiry / Response | Pediatric practice verifies Joe's Texas Medicaid/DentaQuest eligibility at point of care; restorative practice re-verifies at consultation check-in | Confirms active enrollment, covered services, benefit limits used to date, and PA requirement for D3320/D2950/D2740 |
| **837D** — Dental Claim (Pediatric Practice) | Pediatric practice bills DentaQuest for the limited oral evaluation and radiographs | CDT D0140, D0220, D0270; tooth #4; POS 11 |
| **837D** — Dental Claim (Restorative Practice) | Restorative practice bills DentaQuest for root canal therapy, build-up, and crown | CDT D3320, D2950, D2740; tooth #4; POS 11; PA number included on claim |
| **835** — Remittance Advice | DentaQuest adjudicates and pays both claims | DentaQuest fee schedule rates; adjustment reason codes; guardian-facing patient responsibility (if any) |

> **Note on 278 / PAS:** Da Vinci PAS uses FHIR `Claim` and `ClaimResponse` resources for prior authorization. The X12 278 request and response are **not** exercised in this use case.

> **DentaQuest note:** DentaQuest's PA requirements and documentation rules for D3320/D2950/D2740 should be confirmed against the current DentaQuest Texas Medicaid Dental Provider Manual at time of implementation.

### CDT Codes in Scope

| CDT Code | Description | Provider | POS | Medicaid Coverage Note |
|---|---|---|---|---|
| `D0140` | Limited oral evaluation — problem focused | Pediatric dental practice | 11 | Covered |
| `D0220` | Periapical radiographic image | Pediatric dental practice | 11 | Covered |
| `D0270` | Bitewing radiographic image | Pediatric dental practice | 11 | Covered |
| `D3320` | Endodontic therapy, bicuspid tooth (excluding final restoration) | Restorative dental practice | 11 | Covered — medically necessary; PA required |
| `D2950` | Core build-up, including any pins when required | Restorative dental practice | 11 | Covered; PA required as part of bundled plan |
| `D2740` | Crown — porcelain/ceramic | Restorative dental practice | 11 | Covered; PA required as part of bundled plan |

### LOINC Codes in Scope

| LOINC Code | Description | FHIR Resource | Use in This Case |
|---|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport`, `ImagingStudy` | Periapical radiograph — pediatric practice |
| `62441-1` | Bitewing intraoral X-ray | `DiagnosticReport`, `ImagingStudy` | Bitewing radiograph — pediatric practice |

---

## Appendix A: Data

### 1. Patient Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Name** | Joe Castle | Given: Joe; Family: Castle |
| **Date of Birth** | 2010-03-22 | Age: 16 |
| **Sex** | Male | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **Pediatric Dental Practice MRN** | `PEDDENT-TX-2026-0019` | System: `https://pediatricdental.example.org/fhir/mrn` |
| **Restorative Dental Practice MRN** | `RESTORE-TX-2026-0026` | System: `https://restorativedental.example.org/fhir/mrn` |
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
| **Authorized For** | Consent; eligibility inquiry; proxy application access | Represented-patient pattern |

---

### 2. Coverage Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Program** | Texas Medicaid — Pediatric Dental (EPSDT) | Medicaid pediatric dental benefit |
| **Dental Benefit Administrator** | DentaQuest | Third-party dental benefit administrator |
| **Medicaid ID** | TX-MCD-0038211 | Texas Medicaid beneficiary ID |
| **Coverage Period** | 2026-01-01 – 2026-12-31 | Benefit year |
| **Status** | Active | Coverage confirmed |
| **Network** | DentaQuest Texas Medicaid Dental Provider Network | In-network providers |
| **Prior Authorization Required** | Yes — D3320, D2950, D2740 (bundled restorative/endodontic plan) | Confirmed via CRD at order entry |
| **Payer EDI ID** | TX-DQ-DENTAL-EDI | HIPAA X12 claims routing (synthetic) |
| **Payer FHIR Endpoint** | `https://dentaquest-tx.example.org/fhir/r4` | Synthetic DentaQuest FHIR API |

---

### 3. Organization Resource Data

#### Pediatric Dental Practice (Texas)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1720384756 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | Pediatric Dental Practice — Texas (Synthetic) | Test data label — to be filled with actual organization |
| **Type** | Pediatric Dental Practice | Organization type |
| **Care Setting** | Place of Service 11 — Office | In-office |
| **Practice Management System** | Dental PMS with interim FHIR server | Architecture pattern |
| **FHIR Endpoint** | `https://pediatricdental.example.org/fhir/r4` | Interim FHIR server |
| **NPI Taxonomy Code** | 1223P0221X | Pediatric dentistry |
| **DentaQuest Participation** | Active | Confirmed |

#### Restorative Dental Practice (Texas)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1839204765 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | Restorative Dental Practice — Texas (Synthetic) | Test data label — to be filled with actual organization |
| **Type** | General Dental Practice (Restorative/Endodontic) | Organization type |
| **Care Setting** | Place of Service 11 — Office | In-office |
| **Practice Management System** | Dental PMS with interim FHIR server and DICOMweb (WADO-RS) endpoint | Architecture pattern |
| **FHIR Endpoint** | `https://restorativedental.example.org/fhir/r4` | Interim FHIR server |
| **DICOMweb Endpoint** | `https://restorativedental.example.org/dicomweb` | WADO-RS image retrieval per IHE 360X |
| **NPI Taxonomy Code** | 1223G0001X | General dentist |
| **DentaQuest Participation** | Active | Confirmed via Plan-Net query before referral created |

#### DentaQuest — Texas Medicaid Dental Plan

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | DentaQuest — Texas Medicaid Dental Plan (Synthetic) | Test data label |
| **Type** | State Medicaid Dental Benefit Administrator | Organization type |
| **Payer EDI ID** | TX-DQ-DENTAL-EDI | X12 claims routing (synthetic) |
| **FHIR Endpoint** | `https://dentaquest-tx.example.org/fhir/r4` | Synthetic FHIR API |

---

### 4. Practitioner Resource Data

#### Pediatric Dental Provider — Dr. Mary Parker, DDS

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1720384756 | `http://hl7.org/fhir/sid/us-npi` (Practitioner-level NPI, synthetic; distinct from Organization NPI above in production data) |
| **Full Name** | Mary Elizabeth Parker, DDS | Given: Mary; Family: Parker |
| **Qualification** | DDS — Doctor of Dental Surgery, Pediatric Dentistry | Dental degree with pediatric specialty |
| **License Number** | TX-DDS-061204 | Texas dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223P0221X | Pediatric dentistry |
| **Organization** | Pediatric Dental Practice — Texas | Employment |
| **Place of Service** | 11 — Office | In-office |
| **Role in Use Case** | Originating referring provider; recipient of post-treatment summary | Limited oral evaluation; radiographs; referral creation; payer notification; receives summary from Dr. Garcia |

#### Restorative/Endodontic Dentist — Dr. Max Garcia, DDS

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1839204765 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Maximilian Garcia, DDS | Given: Max; Family: Garcia |
| **Qualification** | DDS — Doctor of Dental Surgery | General dentist performing endodontic and restorative treatment |
| **License Number** | TX-DDS-073392 | Texas dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223G0001X | General dentist |
| **Organization** | Restorative Dental Practice — Texas | Employment |
| **DentaQuest Participation** | Active | Confirmed via Plan-Net |
| **Place of Service** | 11 — Office | In-office |
| **Role in Use Case** | Receiving restorative/endodontic provider; sender of post-treatment summary | CRD/DTR/PAS submission; consultation; treatment; transmits summary to Dr. Parker |

---

### 5. Workflow & Service Data

#### ServiceRequest (Referral — Pediatric Practice to Restorative Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Referral fulfilled |
| **Intent** | Order | Clinical order |
| **Category** | Consultation / Referral | Type |
| **Priority** | Routine | Non-urgent; pain manageable |
| **Code** | Root canal therapy, core build-up, and crown — tooth #4 | Referral reason |
| **Subject** | Joe Castle | Patient reference |
| **Requester** | Dr. Mary Parker, DDS | Pediatric dental provider |
| **Performer** | Dr. Max Garcia, DDS | Restorative dentist |
| **Reason Code** | K02.53 (dental caries penetrating into pulp); K04.7 (periapical abscess without sinus) | ICD-10 diagnoses |
| **Supporting Info** | `ImagingStudy` (periapical, bitewing — DICOMweb-retrievable); `DocumentReference` (clinical notes, proposed treatment plan) | Referral clinical package |
| **Description** | Patient presents with MOB decay extending to the pulp and periapical infection on tooth #4. Tooth determined restorable. Referral package includes periapical and bitewing radiographs (DICOMweb-retrievable), clinical notes, and proposed treatment plan (D3320, D2950, D2740). Restorative provider to confirm diagnosis, review medical history and medications, obtain guardian consent, and proceed with treatment. | Referral payload |

#### Communication (Referral Awareness Notification — Pediatric Practice to DentaQuest)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Notification delivered |
| **Category** | Care coordination notification | Not a claim or PA request |
| **Subject** | Joe Castle | Patient reference |
| **Sender** | Dr. Mary Parker, DDS (Pediatric Dental Practice) | Originating provider |
| **Recipient** | DentaQuest | Payer |
| **Based On** | `ServiceRequest` (referral) | Links notification to the referral |
| **Payload** | "Patient referred to Dr. Max Garcia, DDS for root canal therapy and restorative treatment on tooth #4, pending prior authorization." | Structured awareness note |
| **Sent** | 2026-07-08 | Same day as referral transmission |

#### Claim (Prior Authorization — Restorative Practice to DentaQuest)

| FHIR Element | Value | Notes |
|---|---|---|
| **Use** | Preauthorization | PA request, not a claim for payment |
| **Status** | Active | Submitted and pending |
| **Patient** | Joe Castle | Patient reference |
| **Insurer** | DentaQuest — Texas Medicaid Dental Plan | Payer reference |
| **Provider** | Dr. Max Garcia, DDS (Restorative Dental Practice) | Requesting provider |
| **Priority** | Normal | Routine PA |
| **Procedure Codes** | D3320 (endodontic therapy, bicuspid); D2950 (core build-up); D2740 (crown — porcelain/ceramic) | Bundled treatment plan |
| **Tooth** | Tooth #4 (FDI: 15) | Maxillary right first premolar |
| **Diagnosis** | K02.53 (caries penetrating into pulp); K04.7 (periapical abscess without sinus) | Supporting diagnoses |
| **Supporting Info** | Periapical radiograph (LOINC 62443-7); bitewing radiograph (LOINC 62441-1); clinical narrative documenting medical necessity | Required per DTR/DentaQuest documentation rules |
| **Submitted Date** | 2026-07-11 | PA submission date |

#### ClaimResponse (Prior Authorization Approval)

| FHIR Element | Value | Notes |
|---|---|---|
| **Use** | Preauthorization | PA response |
| **Outcome** | Complete | PA approved |
| **Disposition** | Approved — D3320, D2950, D2740, tooth #4, Dr. Max Garcia | Approved bundled service details |
| **PA Number** | TX-DQ-PA-2026-061204 | PA reference number — carried into claim |
| **Validity Period** | 2026-07-15 – 2026-10-15 | 90-day authorization window |
| **Insurer** | DentaQuest — Texas Medicaid Dental Plan | Payer reference |

#### Consent (Guardian Consent for Treatment)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Active | Consent granted |
| **Category** | Treatment consent | Root canal therapy, build-up, and crown |
| **Patient** | Joe Castle | Minor patient |
| **Consenting Party** | Linda Castle (mother/guardian) | `RelatedPerson` reference |
| **Provisions** | Consent to D3320, D2950, D2740 following risk/benefit discussion | Discussed at consultation |
| **Date** | 2026-07-22 | Date of consultation |

#### ClinicalImpression (Post-Treatment Summary — Restorative Practice to Pediatric Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Summary complete |
| **Date** | 2026-07-22 | Date of summary |
| **Assessor** | Dr. Max Garcia, DDS | Restorative dentist |
| **Summary** | Joe Castle seen 2026-07-22 per referral from Dr. Mary Parker. Periapical infection (K04.7) and caries penetrating into pulp (K02.53) confirmed on tooth #4. Guardian consent obtained. Root canal therapy (D3320), core build-up (D2950), and crown placement (D2740) completed without complication. Post-operative radiograph confirms adequate obturation and crown seating. Patient tolerated the procedure well; no anesthesia/sedation complications noted. | Post-treatment summary |
| **Supporting Info** | Post-operative periapical radiograph (`ImagingStudy`) | Confirms treatment outcome |
| **Recommendations** | 1. Routine follow-up at pediatric practice at next recall visit; 2. Monitor for any post-restorative sensitivity; 3. Continue routine pediatric preventive care | Follow-up plan |

#### Communication (Referral Thank-You — Restorative Practice to Pediatric Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Delivered alongside clinical summary |
| **Category** | Provider-to-provider courtesy communication | Non-clinical |
| **Sender** | Dr. Max Garcia, DDS (Restorative Dental Practice) | Originating provider |
| **Recipient** | Dr. Mary Parker, DDS (Pediatric Dental Practice) | Referring provider |
| **Payload** | "Thank you for referring Joe Castle. Treatment was completed successfully and Joe is doing well. We appreciate the complete clinical and imaging package sent with the referral." | Distinct from the clinical `ClinicalImpression` |
| **Sent** | 2026-07-22 | Same transmission as post-treatment summary |

---

### 6. Clinical Codes & Mappings

#### ICD-10 Diagnosis Codes

| Code | Description | Application |
|---|---|---|
| K02.53 | Dental caries on pit and fissure surface penetrating into the pulp | Presenting diagnosis — decay to pulp, tooth #4 |
| K04.7 | Periapical abscess without sinus | Periapical infection associated with tooth #4 |

#### CDT Codes in Scope

| Code | Description | Provider | POS | Medicaid Coverage Note |
|---|---|---|---|---|
| `D0140` | Limited oral evaluation — problem focused | Pediatric dental practice | 11 | Covered |
| `D0220` | Periapical radiographic image | Pediatric dental practice | 11 | Covered |
| `D0270` | Bitewing radiographic image | Pediatric dental practice | 11 | Covered |
| `D3320` | Endodontic therapy, bicuspid tooth (excluding final restoration) | Restorative dental practice | 11 | Covered; PA required |
| `D2950` | Core build-up, including any pins when required | Restorative dental practice | 11 | Covered; PA required |
| `D2740` | Crown — porcelain/ceramic | Restorative dental practice | 11 | Covered; PA required |

#### LOINC Codes

| LOINC | Description | FHIR Resource |
|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport`, `ImagingStudy` |
| `62441-1` | Bitewing intraoral X-ray | `DiagnosticReport`, `ImagingStudy` |

---

### 7. Timeline & Dates

| Event | Date | Time | Actor | System |
|---|---|---|---|---|
| **Limited oral evaluation and radiographs** | 2026-07-08 | 09:30 | Dr. Parker | Pediatric dental PMS |
| **Real-time eligibility verification** | 2026-07-08 | 09:45 | Pediatric practice staff | PDex → DentaQuest FHIR API |
| **Structured referral transmitted (with imaging)** | 2026-07-08 | 10:15 | Dr. Parker's staff | CDex push → Restorative practice interim FHIR server |
| **Referral awareness notification sent to payer** | 2026-07-08 | 10:16 | Pediatric practice system | CDex push → DentaQuest FHIR endpoint |
| **DICOMweb image retrieval and review** | 2026-07-08 | 10:30 | Restorative practice staff | WADO-RS → Restorative practice DICOM viewer |
| **CRD hook — PA required confirmed** | 2026-07-09 | 08:00 | Restorative practice EHR | CRD → DentaQuest FHIR API |
| **DTR — documentation requirements identified** | 2026-07-09 | 08:15 | Restorative practice EHR | DTR → DentaQuest FHIR API |
| **Prior authorization submitted** | 2026-07-11 | 09:00 | Restorative practice staff | PAS → DentaQuest FHIR API |
| **Prior authorization approved** | 2026-07-15 | 14:00 | DentaQuest | PAS `ClaimResponse` |
| **Guardian application notified — PA approved** | 2026-07-15 | 14:05 | Guardian proxy application | FHIR Subscription event |
| **Consultation, consent, and treatment** | 2026-07-22 | 10:00 | Dr. Garcia | Restorative practice PMS |
| **Post-treatment summary + post-op image + thank-you note transmitted** | 2026-07-22 | 13:30 | Restorative practice system | CDex push → Pediatric dental practice FHIR |
| **Referral closed** | 2026-07-22 | 13:35 | Pediatric practice system | `ServiceRequest` → completed |
| **Guardian application updated** | 2026-07-22 | 13:35 | Guardian proxy application | FHIR Subscription event |
| **837D submitted — pediatric practice** | 2026-07-23 | 08:00 | Billing | D0140, D0220, D0270 → DentaQuest EDI |
| **837D submitted — restorative practice** | 2026-07-23 | 08:30 | Billing | D3320, D2950, D2740 → DentaQuest EDI |

#### Key Timeline Constraints

| Constraint | Target | Rationale |
|---|---|---|
| **Referral transmission (with imaging)** | Same day as evaluation | Avoids repeat imaging at receiving practice |
| **Payer awareness notification** | Same transmission window as referral | Establishes payer visibility ahead of PA and claims |
| **CRD/DTR at order entry** | Next business day after referral receipt | Confirms PA and documentation requirements before consult scheduling |
| **PA turnaround** | Within 5 business days of submission | Routine pediatric restorative PA |
| **Consultation and treatment appointment** | Within 7 days of PA approval | Routine; pain manageable |
| **Post-treatment summary + image + thank-you return** | Same day as treatment encounter | Closes referral loop |

---

*This dataset is a test and validation vehicle for the Oral Health Data Exchange (ODE) Implementation Guide, developed under HL7 and sponsored by the PIE Work Group (PSS-2714). It is intended for use in connectathon and interoperability testing environments only. oralhealthalliance.net*
