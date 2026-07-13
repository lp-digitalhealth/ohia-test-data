# CMS Connectathon — Dental Interoperability Test Dataset
## Use Case Set: Extraction of Tooth #30 Following Root Canal Failure
### General Dentist Referral → Oral Surgeon Consultation → Surgical Extraction → Closed-Loop Summary Return

---

## Table of Contents

- [About This Use Case Set](#about-this-use-case-set)
- [Use Case A: Texas Medicaid — Medically Necessary Surgical Extraction with Prior Authorization](#use-case-a-texas-medicaid)
- [Use Case B: Commercial — Surgical Extraction with Immediate Implant Placement](#use-case-b-commercial)

---

## About This Use Case Set

These two use cases model a **general dentist–to–oral surgeon referral** for the surgical extraction of a non-restorable tooth following root canal failure — one of the most common referral pathways in dental care. The clinical scenario is identical in both cases: a patient presents to a general dental practice with recurrent infection and a vertical root fracture on tooth #30, determined to be non-restorable, and is referred to an oral surgeon for surgical extraction. The coverage context and resulting treatment decision distinguish the two use cases:

- **Use Case A** exercises the workflow under **Texas Medicaid**, where the covered episode is the medically necessary extraction. A **Da Vinci PAS prior authorization workflow** is required before the surgical consultation can proceed. The referral and prior authorization run in parallel tracks — FHIR-based for clinical data exchange, PAS for coverage approval.
- **Use Case B** exercises the same referral workflow under **commercial dental coverage**, where Frank elects extraction with **immediate implant placement**. Pre-service review is a benefit verification exercise — not a formal prior authorization — and the workflow focuses on real-time coverage verification, structured referral transmission, and closed-loop post-operative summary return.

Both use cases are set in **Texas**. Both exercise the dental-to-dental referral pattern that was demonstrated as a first-of-its-kind milestone at the OHIA May 2026 quarterly meeting.

**OHIA Strategic Priorities Exercised:** Connect (dental-to-dental provider referral with structured data exchange); Streamline (real-time eligibility verification, prior authorization via PAS — Use Case A); Empower (patient application tracking of referral status, prior authorization status, and clinical and claims updates).

> **No paper forms, portal logins, or fax transmissions are used at any point in either workflow.**

---

---

# Use Case A: Texas Medicaid

## Medically Necessary Surgical Extraction of Tooth #30 with Prior Authorization
### Texas Medicaid | Da Vinci PAS | Dental-to-Dental Referral | Texas

---

## Section I: Business Overview

**Frank Castle** is a 53-year-old male (DOB: 03/17/1972) enrolled in **Texas Medicaid**. He receives routine dental care at a general dental practice in Texas. Frank has a history of root canal treatment on tooth #30 (lower right first molar) and presents with increasing pain, swelling, and discomfort while chewing on the lower right side.

**Dr. Mary Parker, DDS**, the treating general dental provider, performs a **limited oral evaluation** (`D0140`) and obtains **periapical radiographs** (`D0220`). The examination reveals:

- Recurrent periapical infection associated with tooth #30
- Periapical radiolucency on radiograph
- Vertical root fracture extending below the cemento-enamel junction

Based on these findings, Dr. Parker determines that tooth #30 is **non-restorable** and that **surgical extraction is medically necessary** to relieve pain and control infection (`ICD-10: K04.7` — periapical abscess without sinus; `K08.89` — other specified disorder of teeth).

Dr. Parker's team performs **real-time Medicaid eligibility verification** via a FHIR `Coverage` query, confirms the oral surgeon participates in Texas Medicaid, reviews applicable exclusions and benefit limitations, and prepares a **prior authorization request** for the surgical extraction. Because this is a Texas Medicaid case, prior authorization is required before the surgical consultation can proceed.

Dr. Parker's practice submits the prior authorization request to the Texas Medicaid dental plan using **Da Vinci PAS** — transmitting a FHIR `Claim` (PA request) with supporting clinical documentation including the diagnosis, radiographic findings, and treatment recommendation. The `ClaimResponse` is returned with the PA approval, including the PA number and approved service details.

With prior authorization approved, Dr. Parker electronically transmits the **structured referral** to **Dr. Alex Maxil, DDS, MD**, an oral and maxillofacial surgeon participating in Texas Medicaid. The referral package — transmitted via CDex provider-to-provider push — includes the `ServiceRequest`, periapical radiographs, periodontal charting, intraoral images, confirmed diagnosis, and treatment recommendation. Frank is notified through his **patient-facing application** that the referral has been sent and prior authorization approved.

At the **surgical consultation**, Dr. Maxil reviews Frank's records, confirms the diagnosis, reviews his medical history and current medications for surgical risk, and has his staff confirm that Medicaid coverage remains active and review benefits used to date. Frank and Dr. Maxil discuss the risks and benefits of extraction. Frank elects to proceed.

Dr. Maxil completes the **surgical extraction of tooth #30** (`D7210` — surgical extraction of erupted tooth). He documents the procedure, anesthesia used, post-operative findings, and discharge instructions. A **structured post-operative summary** is transmitted back to Dr. Parker via CDex provider-to-provider push, giving the general practice a complete record of the surgical intervention and healing status.

At follow-up, healing is assessed and care is returned to Dr. Parker for ongoing dental management. Frank's patient-facing application provides real-time updates on referral status, prior authorization status, appointment confirmation, and available clinical and claims information throughout the episode.

---

## Section II: Narrative-to-Standards Mapping

| What Happens (Business Language) | Implementation Guide / Standard | Key Transaction |
|---|---|---|
| **Real-time eligibility verification:** Dr. Parker's practice verifies Frank's Texas Medicaid dental eligibility and confirms the oral surgeon's Medicaid participation. | US Core / Da Vinci PDex | `Coverage` queried against Texas Medicaid FHIR API; `InsurancePlan` returned with dental benefit details, exclusions, and limitations; oral surgeon Medicaid participation confirmed via Plan-Net `PractitionerRole` query. |
| **Coverage requirements discovered:** EHR surfaces prior authorization requirement for surgical extraction under Texas Medicaid. | Da Vinci Coverage Requirements Discovery (CRD) | CDS Hook (`order-sign`) triggered at procedure order entry in general practice EHR; returns PA requirement and documentation needs for D7210 under Texas Medicaid. |
| **Documentation requirements identified:** Practice retrieves PA questionnaire and pre-populates clinical data. | Da Vinci Documentation Templates and Rules (DTR) | `Questionnaire` retrieved from Texas Medicaid payer; pre-populated with EHR data (diagnosis, radiographic findings, tooth number, clinical justification). |
| **Prior authorization submitted:** Dr. Parker's practice submits PA request to Texas Medicaid. | Da Vinci Prior Authorization Support (PAS) | `Claim` (PA request) submitted to Texas Medicaid payer FHIR endpoint; includes diagnosis codes, CDT procedure code (D7210), tooth number, supporting clinical documentation. |
| **Prior authorization approved:** Texas Medicaid returns PA approval with PA number. | Da Vinci PAS | `ClaimResponse` returned; PA number included; approved service details confirmed; `Task` (DTR documentation requirement) closed. |
| **Patient notified — PA approved:** Frank's patient application receives notification of PA approval. | FHIR Subscriptions Backport IG | Subscription event on `ClaimResponse` receipt; PA status surfaced in patient application. |
| **Structured referral transmitted:** Dr. Parker transmits referral with full clinical package to oral surgeon. | US Core / ODE (Under Development) / CDex | `ServiceRequest` (referral, priority: routine); `DocumentReference` (radiographs, periodontal charting, intraoral images); `Condition` (K04.7, K08.89); CDex provider-to-provider push to oral surgeon interim FHIR server; PA number included in referral. |
| **Referral received at oral surgery practice:** Dr. Maxil's practice receives referral and clinical package; schedules Frank. | US Core / ODE (Under Development) | `ServiceRequest` received via interim FHIR server; `Appointment` created and linked to referral; `AppointmentResponse` returned to general practice. |
| **Patient notified — referral sent and appointment confirmed:** Frank's application receives notifications at referral creation and appointment confirmation. | FHIR Subscriptions Backport IG | Subscription events on `ServiceRequest` creation and `AppointmentResponse`. |
| **Surgical consultation:** Dr. Maxil reviews records, confirms diagnosis, reviews medical history and medications, confirms active Medicaid coverage. | US Core / ODE (Under Development) | `Encounter` (consultation, POS 11); eligibility re-verified via 270/271; `MedicationStatement` (patient-reported medications reviewed for surgical risk); `Condition` confirmed. |
| **Surgical extraction performed:** Dr. Maxil extracts tooth #30. | US Core / ODE (Under Development) | `Procedure` (D7210, tooth #30, FDI 46); `Encounter` (surgical, POS 11); anesthesia documented; discharge instructions documented. |
| **Post-operative summary returned:** Dr. Maxil transmits structured summary to Dr. Parker. | Da Vinci CDex / ODE (Under Development) | `ClinicalImpression` (post-operative summary); `Procedure` (completed); `CarePlan` (post-operative instructions, healing timeline, follow-up recommended); CDex provider-to-provider push to general practice FHIR endpoint. |
| **Referral closed:** General practice reviews summary; referral marked complete. | US Core / CDex | `ServiceRequest` status updated to `completed`; `Task` closed. |
| **Patient application updated:** Frank's application shows referral complete with post-operative summary and follow-up guidance. | FHIR Subscriptions Backport IG / US Core | Subscription event on `ServiceRequest` status change; `CarePlan` surfaced to patient application. |
| **Claims submission:** Oral surgery practice submits 837D to Texas Medicaid; general practice submits separately for evaluation and radiographs. | X12 837D | 837D (oral surgery): D7210, tooth #30, POS 11; PA number on claim; 837D (general practice): D0140, D0220. |

---

## Section III: Technical Overview

This use case exercises a **dental-to-dental referral with prior authorization** spanning a general dental practice, an oral surgery practice, and Texas Medicaid. The scenario tests the full lifecycle of a prior authorization workflow embedded within a dental-to-dental referral — from real-time coverage discovery at point of order entry through PA approval, structured referral transmission, surgical encounter, and closed-loop post-operative summary return.

This is the first OHIA Connectathon use case to exercise **Da Vinci CRD, DTR, and PAS in a dental-to-dental referral context** — prior authorization workflows that have been well-tested in the medical benefit space but not yet exercised for dental procedure codes (CDT) and dental benefit plans.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

### Implementation Guides

| Implementation Guide | Purpose in This Use Case |
|---|---|
| **US Core IG** | Defines FHIR profiles for all clinical data exchanged between general dental practice, oral surgery practice, and Texas Medicaid |
| **Da Vinci Coverage Requirements Discovery (CRD)** | Fired at procedure order entry in the general practice EHR; surfaces PA requirement for D7210 under Texas Medicaid dental benefit in real time without a portal lookup |
| **Da Vinci Documentation Templates and Rules (DTR)** | Retrieves Texas Medicaid PA questionnaire; pre-populates EHR data including diagnosis, tooth number, and clinical justification; tracks open PA documentation requirement as a `Task` |
| **Da Vinci Prior Authorization Support (PAS)** | Submits the completed PA request for D7210 to Texas Medicaid; receives `ClaimResponse` with PA approval and PA number; PA number carried forward into referral and claim |
| **Da Vinci Clinical Data Exchange (CDex)** | Two roles: (1) **Provider-to-provider referral push** — structured referral with full clinical package transmitted from general dental practice to oral surgery practice interim FHIR server; (2) **Post-operative summary return** — structured summary pushed from oral surgery practice back to general dental practice |
| **Da Vinci PDex / Plan-Net IG** | Real-time eligibility verification and oral surgeon Medicaid network participation confirmation before referral is created |
| **SMART App Launch IG** | Authorization framework enabling Frank's patient application to connect to Texas Medicaid FHIR endpoint and surface PA status, referral status, and post-operative care plan |
| **FHIR Subscriptions Backport IG** | Push notifications to Frank's patient application at PA approval, referral creation, appointment confirmation, and referral closure |
| **Oral Health Data Exchange IG (ODE)** | Under development; governs structured exchange of oral health clinical data — tooth-level findings, CDT-coded procedures, periodontal charting, radiographic findings, and post-operative summary — between the general dental practice and the oral surgery practice |

---

### Key FHIR Resources Exercised

| FHIR Resource | Source IG / Profile | Purpose in This Use Case |
|---|---|---|
| `Patient` | US Core | Patient identity across general dental practice, oral surgery practice interim FHIR server, and Texas Medicaid |
| `Coverage` | US Core / PDex | Texas Medicaid dental benefit — Medicaid ID, plan details, benefit limitations — verified at eligibility check and referenced in PA request and claim |
| `InsurancePlan` | Da Vinci PDex | Texas Medicaid dental plan benefit structure; covered services, exclusions, and prior authorization requirements |
| `Practitioner` | US Core | General dental provider (Dr. Parker); oral and maxillofacial surgeon (Dr. Maxil) |
| `PractitionerRole` | US Core / Plan-Net | Role context for each provider; oral surgeon Medicaid participation confirmed via Plan-Net query before referral target is selected |
| `Organization` | US Core | General dental practice; oral surgery practice; Texas Medicaid dental plan |
| `Encounter` | US Core | Limited oral evaluation (general dental practice); surgical consultation (oral surgery practice); surgical encounter (oral surgery practice) |
| `Condition` | US Core / ODE | K04.7 (periapical abscess without sinus); K08.89 (other specified disorder of teeth — vertical root fracture, non-restorable) |
| `Observation` | US Core / ODE | Periapical radiolucency finding; vertical root fracture finding; tooth #30 clinical findings |
| `DiagnosticReport` | US Core / ODE | Periapical radiograph report (LOINC 62443-7); periodontal charting report |
| `ImagingStudy` | US Core | Periapical radiographic image — transmitted with referral package |
| `MedicationStatement` | US Core | Patient-reported medications reviewed by Dr. Maxil for surgical risk assessment |
| `ServiceRequest` | US Core / ODE | Structured dental-to-dental referral from general dental practice to oral surgery practice; includes PA number; status lifecycle `active` → `completed` |
| `DocumentReference` | US Core | Radiographs, periodontal charting, and intraoral images transmitted as supporting documentation in referral package |
| `Questionnaire` / `QuestionnaireResponse` | Da Vinci DTR | Texas Medicaid PA documentation requirements; pre-populated from EHR data at DTR launch |
| `Claim` (PA) | Da Vinci PAS | Prior authorization request for D7210 submitted to Texas Medicaid |
| `ClaimResponse` | Da Vinci PAS | Texas Medicaid PA approval response — PA number, approved service, validity period |
| `Appointment` / `AppointmentResponse` | US Core | Oral surgery appointment created and confirmed; surfaced to patient application |
| `Procedure` | US Core / ODE | D7210 (surgical extraction, tooth #30, FDI 46); D0140 (limited oral evaluation); D0220 (periapical radiograph) |
| `ClinicalImpression` | ODE | Post-operative summary from oral surgery practice; includes procedure details, anesthesia, healing status, and discharge instructions |
| `CarePlan` | US Core | Post-operative care instructions and follow-up timeline; surfaced to patient application |
| `Task` | Da Vinci DTR / CDex | Tracks open PA documentation requirement (DTR); tracks open referral (CDex); both closed on completion |
| `Subscription` / `SubscriptionStatus` | FHIR Subscriptions Backport IG | Push notifications to patient application at PA approval, referral creation, appointment confirmation, referral closure |
| `Bundle` | FHIR Core | Referral package bundle (ServiceRequest + Condition + Observation + DiagnosticReport + DocumentReference); post-operative summary bundle |
| `AuditEvent` | US Core | Cross-organizational data access logging |
| `Provenance` | US Core | Chain of custody across general dental practice, oral surgery practice, and Texas Medicaid FHIR endpoints |

---

### Cross-Cutting Test Objectives

1. **CRD in a dental benefit context** — CDS Hook (`order-sign`) fired at dental procedure order entry is tested for the first time against a dental benefit plan (Texas Medicaid dental) rather than a medical benefit plan. The test validates whether CRD can return correct PA requirements for CDT procedure codes (D7210) and dental benefit plan rules — a capability not previously exercised in OHIA Connectathons.

2. **DTR pre-population from a dental EHR** — DTR questionnaire pre-population is tested against a dental practice management system's FHIR endpoint rather than a medical EHR. The test validates whether dental EHR data — tooth number, CDT code, periapical radiographic findings, diagnosis — can pre-populate a payer PA questionnaire via DTR without manual data entry.

3. **PAS for a CDT-coded dental procedure** — Da Vinci PAS is tested with CDT procedure codes (D7210) and dental benefit plan prior authorization rules. This is the first OHIA Connectathon use of PAS in a dental-only benefit context. The test validates whether the `Claim` (PA) resource can correctly carry a CDT code, tooth number (FDI notation), and dental diagnosis in a format that a dental benefit payer can adjudicate.

4. **PA number carried through referral and claim** — The PA number returned in the `ClaimResponse` must be carried forward into the `ServiceRequest` (referral) and the 837D claim. The test validates this chain of custody: PA approved → PA number in referral → PA number on 837D → claim adjudicated with PA reference.

5. **Dental-to-dental referral with full clinical package** — The referral payload in this use case is richer than a simple `ServiceRequest`: it includes radiographs (`ImagingStudy`), periodontal charting (`DiagnosticReport`), intraoral images (`DocumentReference`), and confirmed diagnosis (`Condition`). The test validates whether a dental-to-dental CDex provider-to-provider push can carry a multi-resource clinical package that eliminates the need for the receiving oral surgeon to repeat basic diagnostic work.

6. **Oral surgeon Medicaid participation verification before referral** — Plan-Net `PractitionerRole` and `HealthcareService` are queried to confirm oral surgeon Medicaid network participation before the referral is created — preventing the referral from being sent to a non-participating provider and protecting the patient from unexpected out-of-pocket cost.

7. **Patient application as real-time PA and referral tracker** — Frank's patient application surfaces PA status, referral status, appointment confirmation, and post-operative care plan from three independent data sources (general dental practice, Texas Medicaid, oral surgery practice) — testing SMART App Launch, PDex, and FHIR Subscriptions in a dental episode-of-care context.

8. **ODE IG validation in an oral surgery referral context** — This use case exercises ODE profiles for tooth-level clinical findings, CDT-coded surgical procedures, and post-operative summary exchange in an oral surgery referral — a workflow not previously tested in OHIA Connectathons with the full ODE profile suite.

---

## Section IV: EDI Transactions

Frank's dental benefit is administered through **Texas Medicaid**. All dental services are billed via 837D under the Texas Medicaid dental fee schedule. The prior authorization workflow uses Da Vinci PAS (FHIR-native) rather than the legacy X12 278.

### EDI Transactions in Scope

| X12 Transaction | Trigger | Scope Note |
|---|---|---|
| **270 / 271** — Eligibility & Benefit Inquiry / Response | General dental practice verifies Frank's Texas Medicaid dental eligibility at point of care; oral surgery practice re-verifies at consultation check-in | Confirms active enrollment, covered services, benefit limits used to date, and PA requirement for D7210 |
| **837D** — Dental Claim (General Dental Practice) | General dental practice bills Texas Medicaid for limited oral evaluation and radiographs | CDT D0140 (limited oral evaluation); D0220 (periapical radiograph, tooth #30); POS 11 |
| **837D** — Dental Claim (Oral Surgery Practice) | Oral surgery practice bills Texas Medicaid for surgical extraction | CDT D7210 (surgical extraction, tooth #30); POS 11; PA number included on claim; Texas Medicaid fee schedule rate applies |
| **835** — Remittance Advice | Texas Medicaid adjudicates and pays both claims | Texas Medicaid fee schedule rates; adjustment reason codes; patient responsibility |

> **Note on 278 / PAS:** Da Vinci PAS uses FHIR `Claim` and `ClaimResponse` resources for prior authorization. The X12 278 request and response are **not** exercised in this use case. This use case tests whether a Texas Medicaid dental payer can accept and adjudicate a FHIR-native PA request for a CDT-coded dental procedure — a named test objective.

> **Texas Medicaid note:** Texas Medicaid adult dental benefits cover medically necessary extractions. PA requirements for D7210 should be confirmed against the current Texas Medicaid Dental Provider Procedures Manual at time of implementation.

### CDT Codes in Scope

| CDT Code | Description | Provider | POS | Medicaid Coverage Note |
|---|---|---|---|---|
| `D0140` | Limited oral evaluation — problem focused | General dental practice | 11 | Covered |
| `D0220` | Periapical radiographic image | General dental practice | 11 | Covered |
| `D7210` | Surgical extraction — erupted tooth requiring elevation and/or forceps removal | Oral surgery practice | 11 | Covered — medically necessary; PA required |

### LOINC Codes in Scope

| LOINC Code | Description | FHIR Resource | Use in This Case |
|---|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport`, `ImagingStudy` | Periapical radiograph — general dental practice |

---

## Appendix A: Data

### 1. Patient Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Name** | Frank Castle | Given: Frank; Family: Castle |
| **Date of Birth** | 1972-03-17 | Age: 53 |
| **Sex** | Male | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **General Dental Practice MRN** | `GDENT-TX-2026-0047` | System: `https://generaldental.example.org/fhir/mrn` |
| **Oral Surgery Practice MRN** | `ORALSURG-TX-2026-0031` | System: `https://oralsurgery.example.org/fhir/mrn` |
| **Texas Medicaid ID** | `TX-MCD-0091847` | System: `http://texas.medicaid.gov/beneficiary` |
| **Telecom (Phone)** | (512) 555-0147 | Use: Mobile |
| **Telecom (Email)** | frank.castle@example.com | Use: Home |
| **Address** | 918 South Congress Avenue, Apt 6, Austin, TX 78704 | City: Austin; State: TX; ZIP: 78704 |
| **Language** | English | Preferred language |
| **Active** | True | Patient record is active |

---

### 2. Coverage Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Program** | Texas Medicaid — Adult Dental | Medicaid dental benefit |
| **Medicaid ID** | TX-MCD-0091847 | Texas Medicaid beneficiary ID |
| **Coverage Period** | 2026-01-01 – 2026-12-31 | Benefit year |
| **Status** | Active | Coverage confirmed |
| **Network** | Texas Medicaid Dental Provider Network | In-network providers |
| **Prior Authorization Required** | Yes — D7210 (surgical extraction) | Confirmed via CRD at order entry |
| **Payer EDI ID** | TX-MCD-DENTAL-EDI | HIPAA X12 claims routing (synthetic) |
| **Payer FHIR Endpoint** | `https://txmedicaid-dental.example.org/fhir/r4` | Synthetic Texas Medicaid dental FHIR API |

---

### 3. Organization Resource Data

#### General Dental Practice (Texas)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1467823094 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | General Dental Practice — Texas (Synthetic) | Test data label — to be filled with actual organization |
| **Type** | General Dental Practice | Organization type |
| **Care Setting** | Place of Service 11 — Office | In-office |
| **Practice Management System** | Dental PMS with interim FHIR server | Architecture pattern |
| **FHIR Endpoint** | `https://generaldental.example.org/fhir/r4` | Interim FHIR server |
| **NPI Taxonomy Code** | 1223G0001X | General dentist |
| **Medicaid Participation** | Active — Texas Medicaid dental | Confirmed |

#### Oral Surgery Practice (Texas)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1578293148 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | Oral Surgery Practice — Texas (Synthetic) | Test data label — to be filled with actual organization |
| **Type** | Oral and Maxillofacial Surgery Practice | Organization type |
| **Care Setting** | Place of Service 11 — Office | In-office |
| **Practice Management System** | Dental PMS with interim FHIR server | Architecture pattern |
| **FHIR Endpoint** | `https://oralsurgery.example.org/fhir/r4` | Interim FHIR server |
| **NPI Taxonomy Code** | 1223X0400X | Oral and maxillofacial surgeon |
| **Medicaid Participation** | Active — Texas Medicaid dental | Confirmed via Plan-Net query before referral created |

#### Texas Medicaid Dental Plan

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | Texas Medicaid Dental Plan (Synthetic) | Test data label |
| **Type** | State Medicaid Dental Benefit | Organization type |
| **Payer EDI ID** | TX-MCD-DENTAL-EDI | X12 claims routing (synthetic) |
| **FHIR Endpoint** | `https://txmedicaid-dental.example.org/fhir/r4` | Synthetic FHIR API |

---

### 4. Practitioner Resource Data

#### General Dental Provider — Dr. Mary Parker, DDS

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1538476284 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Mary Elizabeth Parker, DDS | Given: Mary; Family: Parker |
| **Qualification** | DDS — Doctor of Dental Surgery | Dental degree |
| **License Number** | TX-DDS-047291 | Texas dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223G0001X | General dentist |
| **Organization** | General Dental Practice — Texas | Employment |
| **Place of Service** | 11 — Office | In-office |
| **Role in Use Case** | Originating referring provider; recipient of post-operative summary | Limited oral evaluation; PA submission; referral creation; receives summary from Dr. Maxil |

#### Oral and Maxillofacial Surgeon — Dr. Alex Maxil, DDS, MD

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1649203912 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Alex James Maxil, DDS, MD | Given: Alex; Family: Maxil |
| **Qualification** | DDS, MD — Dual degree oral and maxillofacial surgeon | Dental and medical degrees |
| **License Number** | TX-DDS-052841; TX-MD-091023 | Texas dental and medical licenses (synthetic) |
| **Specialty Code (Taxonomy)** | 1223X0400X | Oral and maxillofacial surgery |
| **Organization** | Oral Surgery Practice — Texas | Employment |
| **Medicaid Participation** | Active — Texas Medicaid dental | Confirmed via Plan-Net |
| **Place of Service** | 11 — Office | In-office |
| **Role in Use Case** | Receiving surgical provider; sender of post-operative summary | Surgical consultation; extraction; transmits summary to Dr. Parker |

---

### 5. Workflow & Service Data

#### Claim (Prior Authorization — General Dental Practice to Texas Medicaid)

| FHIR Element | Value | Notes |
|---|---|---|
| **Use** | Preauthorization | PA request, not a claim for payment |
| **Status** | Active | Submitted and pending |
| **Patient** | Frank Castle | Patient reference |
| **Insurer** | Texas Medicaid Dental Plan | Payer reference |
| **Provider** | Dr. Mary Parker, DDS (General Dental Practice) | Requesting provider |
| **Priority** | Normal | Routine PA |
| **Procedure Code** | D7210 — Surgical extraction, erupted tooth | CDT code |
| **Tooth** | Tooth #30 (FDI: 46) | Lower right first molar |
| **Diagnosis** | K04.7 (periapical abscess without sinus); K08.89 (non-restorable tooth — vertical root fracture) | Supporting diagnoses |
| **Supporting Info** | Periapical radiograph (LOINC 62443-7); clinical narrative (vertical root fracture, periapical radiolucency, failed endodontic treatment); prior endodontic history | Clinical justification |
| **Submitted Date** | 2026-07-10 | PA submission date |

#### ClaimResponse (Prior Authorization Approval)

| FHIR Element | Value | Notes |
|---|---|---|
| **Use** | Preauthorization | PA response |
| **Outcome** | Complete | PA approved |
| **Disposition** | Approved — D7210, tooth #30, Dr. Alex Maxil (oral surgeon) | Approved service details |
| **PA Number** | TX-MCD-PA-2026-047291 | PA reference number — carried into ServiceRequest and 837D |
| **Validity Period** | 2026-07-14 – 2026-10-14 | 90-day authorization window |
| **Insurer** | Texas Medicaid Dental Plan | Payer reference |

#### ServiceRequest (Referral — General Dental Practice to Oral Surgery Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Referral fulfilled |
| **Intent** | Order | Clinical order |
| **Category** | Consultation / Referral | Type |
| **Priority** | Routine | Non-urgent; pain controlled |
| **Code** | Surgical extraction — tooth #30; non-restorable following root canal failure | Referral reason |
| **Subject** | Frank Castle | Patient reference |
| **Requester** | Dr. Mary Parker, DDS | General dental provider |
| **Performer** | Dr. Alex Maxil, DDS, MD | Oral surgeon |
| **Reason Code** | K04.7 (periapical abscess without sinus); K08.89 (non-restorable tooth) | ICD-10 diagnoses |
| **Insurance** | Coverage reference — Texas Medicaid; PA Number: TX-MCD-PA-2026-047291 | PA number carried in referral |
| **Ordered Date** | 2026-07-14 | PA approval date |
| **Occurrence DateTime** | 2026-07-21 | Surgical consultation date |
| **Description** | Patient presents with recurrent periapical infection and vertical root fracture on tooth #30 following prior root canal treatment. Tooth determined non-restorable. Texas Medicaid PA approved (PA# TX-MCD-PA-2026-047291). Referral package includes periapical radiograph, periodontal charting, intraoral images, diagnosis, and treatment recommendation. Oral surgeon to confirm diagnosis, review medical history and medications, and proceed with surgical extraction. | Referral payload |

#### Procedure (Surgical Extraction — Oral Surgery Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Code** | D7210 (CDT) | Surgical extraction — erupted tooth requiring elevation |
| **Subject** | Frank Castle | Patient reference |
| **Performer** | Dr. Alex Maxil, DDS, MD | Oral surgeon |
| **Performed DateTime** | 2026-07-21 | Date of procedure |
| **Body Site** | Tooth #30 (FDI: 46) | Lower right first molar |
| **Reason Reference** | K04.7 (periapical abscess, confirmed); K08.89 (non-restorable, vertical root fracture confirmed) | Confirmed diagnoses |
| **Note** | Surgical extraction completed without complication. Flap reflected; tooth sectioned for removal. Socket curetted; irrigated. Primary closure achieved. Local anesthesia: inferior alveolar nerve block + long buccal block, 2% lidocaine with 1:100,000 epinephrine. Post-operative instructions provided; follow-up in 1 week. | Operative note |

#### ClinicalImpression (Post-Operative Summary — Oral Surgery Practice to General Dental Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Summary complete |
| **Date** | 2026-07-21 | Date of summary |
| **Assessor** | Dr. Alex Maxil, DDS, MD | Oral surgeon |
| **Summary** | Frank Castle seen 2026-07-21 per referral from general dental practice. Diagnosis of periapical abscess (K04.7) and non-restorable tooth #30 confirmed. Vertical root fracture confirmed intraoperatively. Surgical extraction of tooth #30 completed without complication (D7210). Socket curetted; primary closure achieved. Post-operative instructions provided. Follow-up in 1 week to assess healing. Patient tolerated procedure well. Case returned to general dental provider for ongoing management and future restorative planning. | Post-operative summary |
| **Finding** | Confirmed: K04.7 (periapical abscess); K08.89 (non-restorable — vertical root fracture confirmed intraoperatively) | Confirmed diagnoses |
| **Recommendations** | 1. Follow-up at 1 week for healing assessment; 2. Future restorative options (implant, bridge, or space maintenance) to be discussed with general dental provider after healing; 3. Patient advised to maintain oral hygiene at extraction site | Post-operative plan |

---

### 6. Clinical Codes & Mappings

#### ICD-10 Diagnosis Codes

| Code | Description | Application |
|---|---|---|
| K04.7 | Periapical abscess without sinus | Presenting diagnosis; confirmed intraoperatively |
| K08.89 | Other specified disorders of teeth | Non-restorable tooth — vertical root fracture below CEJ |

#### CDT Codes in Scope

| Code | Description | Provider | POS |
|---|---|---|---|
| `D0140` | Limited oral evaluation — problem focused | General dental practice | 11 |
| `D0220` | Periapical radiographic image | General dental practice | 11 |
| `D7210` | Surgical extraction — erupted tooth requiring elevation and/or forceps removal | Oral surgery practice | 11 |

#### LOINC Codes

| LOINC | Description | FHIR Resource |
|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport`, `ImagingStudy` |

---

### 7. Timeline & Dates

| Event | Date | Time | Actor | System |
|---|---|---|---|---|
| **Limited oral evaluation and radiograph** | 2026-07-08 | 10:00 | Dr. Parker | General dental PMS |
| **CRD hook fired — PA requirement identified** | 2026-07-08 | 10:30 | General dental EHR | CRD / payer FHIR API |
| **DTR questionnaire retrieved and pre-populated** | 2026-07-08 | 10:35 | Dr. Parker's staff | DTR / payer FHIR API |
| **PA submitted (PAS)** | 2026-07-10 | 09:00 | Dr. Parker's staff | PAS → Texas Medicaid FHIR endpoint |
| **PA approved (ClaimResponse)** | 2026-07-14 | 14:00 | Texas Medicaid | ClaimResponse → General dental practice |
| **Patient notified — PA approved** | 2026-07-14 | 14:01 | Patient application | FHIR Subscription event |
| **Structured referral transmitted** | 2026-07-14 | 14:30 | Dr. Parker's staff | CDex push → Oral surgery interim FHIR server |
| **Patient notified — referral sent** | 2026-07-14 | 14:30 | Patient application | FHIR Subscription event |
| **Referral received; appointment scheduled** | 2026-07-14 | 15:00 | Oral surgery staff | Dental PMS |
| **AppointmentResponse returned** | 2026-07-14 | 15:05 | Oral surgery system | Interim FHIR → General dental practice FHIR |
| **Patient notified — appointment confirmed** | 2026-07-14 | 15:05 | Patient application | FHIR Subscription event |
| **Surgical consultation and extraction** | 2026-07-21 | 09:00 | Dr. Maxil | Oral surgery PMS |
| **Post-operative summary transmitted** | 2026-07-21 | 11:30 | Oral surgery system | CDex push → General dental practice FHIR |
| **Referral closed** | 2026-07-21 | 11:31 | General dental system | ServiceRequest → completed |
| **Patient application updated** | 2026-07-21 | 11:31 | Patient application | FHIR Subscription event |
| **837D submitted — general dental practice** | 2026-07-22 | 08:00 | Billing | D0140, D0220 → Texas Medicaid EDI |
| **837D submitted — oral surgery practice** | 2026-07-22 | 08:30 | Billing | D7210 + PA number → Texas Medicaid EDI |

#### Key Timeline Constraints

| Constraint | Target | Rationale |
|---|---|---|
| **PA submission after evaluation** | Same day or next business day | Clinical data available; DTR pre-populated |
| **PA decision** | Within standard Medicaid PA processing timeline | Routine (non-urgent) PA |
| **Referral transmission** | Same day as PA approval | PA number required in referral |
| **Surgical appointment** | Within 7 days of referral | Routine; pain controlled |
| **Post-operative summary return** | Same day as surgical encounter | Closes referral loop; enables follow-up planning |

---
---

# Use Case B: Commercial

## Surgical Extraction of Tooth #30 with Immediate Implant Placement
### Commercial Dental PPO | Benefit Verification | Dental-to-Dental Referral | Texas

---

## Section I: Business Overview

**Frank Castle** is a 53-year-old male (DOB: 03/17/1972) with **commercial dental PPO coverage** through his employer. He presents to a general dental practice in Texas with recurrent pain and swelling associated with tooth #30 (lower right first molar), previously treated endodontically.

**Dr. Mary Parker, DDS**, performs a **limited oral evaluation** (`D0140`) and obtains **periapical radiographs** (`D0220`). The examination reveals a failing root canal with recurrent infection, periapical radiolucency, and a vertical root fracture below the cemento-enamel junction. Tooth #30 is non-restorable.

Because Frank has commercial coverage with implant benefits, Dr. Parker discusses two treatment options: (1) extraction alone, with future implant placement at a separate appointment after healing; (2) surgical extraction with **immediate implant placement** at the same surgical visit. Dr. Parker's team performs **real-time benefit verification** via a FHIR `Coverage` query, confirming Frank's dental plan benefits including implant coverage, any applicable waiting periods, annual maximum remaining, and any exclusions. No prior authorization is required for the procedures under this commercial plan design.

Dr. Parker transmits the **structured referral** to **Dr. Alex Maxil, DDS, MD**, an oral and maxillofacial surgeon in the commercial PPO network. The referral package — transmitted via CDex provider-to-provider push — includes the `ServiceRequest`, periapical radiographs, periodontal charting, intraoral images, confirmed diagnosis, and both treatment options for Dr. Maxil's review. Frank is notified through his **patient-facing application** that the referral has been sent and his appointment is confirmed.

At the **surgical consultation**, Dr. Maxil reviews Frank's records, confirms the diagnosis, reviews his medical history and medications for surgical risk, and discusses both options including immediate implant placement, possible bone grafting needs, costs, and informed consent. Frank elects to proceed with **surgical extraction with immediate implant placement**.

Dr. Maxil completes the **surgical extraction of tooth #30** (`D7210`) and **immediate placement of an endosteal implant** (`D6010`) at the same appointment. He documents the procedure, implant details (manufacturer, size, placement torque), anesthesia used, post-operative findings, and discharge instructions. A **structured post-operative summary** — including implant specifications — is transmitted back to Dr. Parker via CDex provider-to-provider push, supporting future restorative follow-up (crown placement) at the general practice.

Frank's patient-facing application provides real-time updates on referral status, appointment confirmation, and available clinical and claims information throughout the episode.

---

## Section II: Narrative-to-Standards Mapping

| What Happens (Business Language) | Implementation Guide / Standard | Key Transaction |
|---|---|---|
| **Real-time benefit verification:** Dr. Parker's practice verifies Frank's commercial dental plan benefits — implant coverage, waiting periods, annual maximum remaining, exclusions. | US Core / Da Vinci PDex | `Coverage` queried against commercial payer FHIR API; `InsurancePlan` returned with plan details including implant benefit, waiting period status, and annual maximum. |
| **Coverage requirements discovered:** EHR confirms no PA is required for D7210 or D6010 under this commercial plan. | Da Vinci Coverage Requirements Discovery (CRD) | CDS Hook (`order-sign`) triggered; returns no PA requirement; confirms coverage active and benefits available. |
| **Structured referral transmitted:** Dr. Parker transmits referral with clinical package and both treatment options to oral surgeon. | US Core / ODE (Under Development) / CDex | `ServiceRequest` (referral); `DocumentReference` (radiographs, charting, images); `Condition` (K04.7, K08.89); CDex provider-to-provider push to oral surgery practice interim FHIR server. |
| **Referral received; appointment confirmed:** Oral surgery practice receives referral and schedules Frank. | US Core / ODE (Under Development) | `ServiceRequest` received; `Appointment` created; `AppointmentResponse` returned to general practice. |
| **Patient notified — referral sent and appointment confirmed:** Frank's application receives notifications at referral creation and appointment confirmation. | FHIR Subscriptions Backport IG | Subscription events on `ServiceRequest` creation and `AppointmentResponse`. |
| **Surgical consultation:** Dr. Maxil reviews records, confirms diagnosis, reviews medical history and medications, discusses treatment options including immediate implant placement. | US Core / ODE (Under Development) | `Encounter` (consultation, POS 11); `MedicationStatement` reviewed; informed consent documented. |
| **Surgical extraction and immediate implant placement performed:** Dr. Maxil extracts tooth #30 and places implant at same visit. | US Core / ODE (Under Development) | `Procedure` (D7210, tooth #30, FDI 46); `Procedure` (D6010, tooth #30 site, FDI 46); `Device` (implant specifications — manufacturer, size, lot number); `Encounter` (surgical, POS 11). |
| **Post-operative summary returned:** Dr. Maxil transmits structured summary including implant specifications to Dr. Parker. | Da Vinci CDex / ODE (Under Development) | `ClinicalImpression` (post-operative summary with implant detail); `Procedure` (completed); `Device` (implant record); `CarePlan` (osseointegration timeline, restorative follow-up); CDex push to general dental practice FHIR endpoint. |
| **Referral closed:** General practice reviews summary and implant record; referral marked complete. | US Core / CDex | `ServiceRequest` → completed; `Task` closed. |
| **Patient application updated:** Frank's application shows referral complete with post-operative summary and restorative follow-up timeline. | FHIR Subscriptions Backport IG / US Core | Subscription event; `CarePlan` surfaced to patient application. |
| **Claims submission:** Oral surgery practice submits 837D to commercial payer; general practice submits separately. | X12 837D | 837D (oral surgery): D7210 + D6010, tooth #30, POS 11; 837D (general practice): D0140, D0220. |

---

## Section III: Technical Overview

This use case exercises a **dental-to-dental referral with benefit verification and immediate implant placement**, spanning a general dental practice, an oral surgery practice, and a commercial dental PPO payer. The scenario is structurally similar to Use Case A but removes the prior authorization workflow and introduces the `Device` resource for implant specification tracking — a capability that enables downstream restorative continuity at the referring general dental practice.

The key interoperability problem this use case addresses: the oral surgeon places an implant with specific manufacturer, size, and placement specifications. Today, those specifications are documented in the surgeon's record and communicated to the restorative dentist — who will eventually place the crown — by whatever means is available (phone, fax, PDF). With structured exchange, the implant `Device` record travels with the post-operative summary to the general practice FHIR endpoint, where it is available at the time of crown placement without a separate records request.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

### Implementation Guides

| Implementation Guide | Purpose in This Use Case |
|---|---|
| **US Core IG** | Defines FHIR profiles for all clinical data exchanged between general dental practice, oral surgery practice, and commercial payer |
| **Da Vinci Coverage Requirements Discovery (CRD)** | Fired at procedure order entry; confirms no PA requirement for D7210 or D6010 under the commercial plan; confirms benefits available |
| **Da Vinci Clinical Data Exchange (CDex)** | Two roles: (1) **Provider-to-provider referral push** — structured referral and clinical package transmitted to oral surgery practice; (2) **Post-operative summary return** — structured summary including implant `Device` record pushed back to general dental practice |
| **Da Vinci PDex** | Real-time benefit verification — `Coverage` and `InsurancePlan` queried at point of care to confirm implant coverage, waiting period status, and annual maximum |
| **SMART App Launch IG** | Authorization framework for patient application |
| **FHIR Subscriptions Backport IG** | Push notifications to patient application at referral creation, appointment confirmation, and referral closure |
| **Oral Health Data Exchange IG (ODE)** | Under development; governs tooth-level clinical findings, CDT-coded procedures, implant `Device` record, and post-operative summary exchange |

---

### Key FHIR Resources Exercised

| FHIR Resource | Source IG / Profile | Purpose in This Use Case |
|---|---|---|
| `Patient` | US Core | Patient identity across general dental practice, oral surgery practice, and commercial payer |
| `Coverage` | US Core / PDex | Commercial dental PPO — plan details, implant coverage, waiting periods, annual maximum — verified at benefit check |
| `InsurancePlan` | Da Vinci PDex | Commercial plan benefit structure; implant benefit confirmation |
| `Practitioner` | US Core | General dental provider (Dr. Parker); oral surgeon (Dr. Maxil) |
| `PractitionerRole` | US Core | Role context; oral surgeon commercial PPO network participation confirmed |
| `Organization` | US Core | General dental practice; oral surgery practice; commercial dental payer |
| `Encounter` | US Core | Limited oral evaluation (general dental practice); surgical consultation and surgical encounter (oral surgery practice) |
| `Condition` | US Core / ODE | K04.7 (periapical abscess without sinus); K08.89 (non-restorable — vertical root fracture) |
| `Observation` | US Core / ODE | Periapical radiolucency; vertical root fracture; failing endodontic treatment |
| `DiagnosticReport` | US Core / ODE | Periapical radiograph (LOINC 62443-7); periodontal charting |
| `ImagingStudy` | US Core | Periapical radiographic image |
| `MedicationStatement` | US Core | Patient-reported medications reviewed for surgical risk |
| `ServiceRequest` | US Core / ODE | Dental-to-dental referral; status lifecycle `active` → `completed` |
| `DocumentReference` | US Core | Radiographs, periodontal charting, intraoral images in referral package |
| `Procedure` | US Core / ODE | D7210 (surgical extraction, tooth #30, FDI 46); D6010 (immediate endosteal implant placement, tooth #30 site) |
| `Device` | US Core | Implant specifications — manufacturer, catalog number, size (diameter and length), lot number, placement torque — documented at time of placement and transmitted in post-operative summary to general dental practice for restorative continuity |
| `ClinicalImpression` | ODE | Post-operative summary including implant detail, osseointegration timeline, and restorative follow-up guidance |
| `CarePlan` | US Core | Post-operative care instructions; osseointegration timeline; restorative follow-up (crown placement) at general practice |
| `Appointment` / `AppointmentResponse` | US Core | Oral surgery appointment and confirmation |
| `Task` | CDex | Tracks open referral; closed on receipt of post-operative summary |
| `Subscription` / `SubscriptionStatus` | FHIR Subscriptions Backport IG | Push notifications to patient application |
| `Bundle` | FHIR Core | Referral package; post-operative summary bundle including `Device` |
| `AuditEvent` | US Core | Cross-organizational data access logging |
| `Provenance` | US Core | Chain of custody |

---

### Cross-Cutting Test Objectives

1. **CRD confirming no PA required** — CRD is tested in the scenario where the hook fires and returns a negative result: no PA required, benefits confirmed available. This validates CRD as a bidirectional signal — not just a PA trigger, but a benefit confirmation mechanism that eliminates unnecessary PA submissions and manual benefit calls.

2. **`Device` resource for implant specification tracking** — This is the first OHIA Connectathon use case to introduce the `Device` resource for a dental implant. The test validates whether implant specifications — manufacturer, catalog number, diameter, length, lot number, placement torque — can be documented as a FHIR `Device` resource at time of placement and transmitted in a CDex post-operative summary to the referring general dental practice, where they are available for restorative planning without a separate records request.

3. **Dual-procedure referral payload** — The referral package in this use case transmits two treatment options (extraction alone vs. extraction with immediate implant) rather than a single treatment recommendation. The test validates whether `ServiceRequest` and supporting documentation can carry multiple treatment scenarios for the receiving surgeon's review.

4. **Commercial plan implant benefit verification** — Real-time `Coverage` and `InsurancePlan` query confirming implant benefit coverage, waiting period status, and annual maximum is tested against a commercial dental PPO — a benefit structure with significantly more variability than Medicaid. The test surfaces implant benefit design complexity as a named area for ODE IG guidance.

5. **Restorative continuity via structured implant record** — The implant `Device` record transmitted in the post-operative summary enables the general practice to plan the crown restoration (D6065 or D6066) at the correct timing without repeating a records request to the oral surgeon. This is the core interoperability value proposition of Use Case B beyond the referral workflow itself.

6. **Closed-loop post-operative summary without PA workflow** — Use Case B validates that the CDex provider-to-provider referral and summary return pattern functions independently of the PA workflow — confirming that dental-to-dental referral interoperability does not require a PA workflow to operate.

7. **ODE IG validation for implant placement in an oral surgery context** — `D6010` (endosteal implant placement) with associated `Device` resource is tested in ODE profiles for the first time, validating that the IG can represent both the procedure and the device-level specifications needed for downstream restorative care.

---

## Section IV: EDI Transactions

Frank's dental benefit is a **commercial dental PPO**. All services are billed via 837D. No prior authorization is required under this plan design.

### EDI Transactions in Scope

| X12 Transaction | Trigger | Scope Note |
|---|---|---|
| **270 / 271** — Eligibility & Benefit Inquiry / Response | General dental practice verifies Frank's commercial dental benefits at point of care; oral surgery practice re-verifies at check-in | Confirms active coverage, implant benefit, waiting period status, and annual maximum remaining |
| **837D** — Dental Claim (General Dental Practice) | General dental practice bills commercial payer for limited oral evaluation and radiographs | CDT D0140 (limited oral evaluation); D0220 (periapical radiograph, tooth #30); POS 11 |
| **837D** — Dental Claim (Oral Surgery Practice) | Oral surgery practice bills commercial payer for surgical extraction and immediate implant placement | CDT D7210 (surgical extraction, tooth #30); D6010 (endosteal implant placement, tooth #30 site); POS 11; commercial fee schedule |
| **835** — Remittance Advice | Commercial payer adjudicates and pays both claims | Adjustment reason codes; patient cost-sharing per plan design; any benefit limitation denials surfaced as named test findings |

> **Note on 278:** No prior authorization is required for D7210 or D6010 under this commercial plan design. The X12 278 transaction is not in scope for this use case.

> **Implant coverage note:** Commercial dental plan implant coverage varies significantly. Waiting periods (commonly 12–24 months), annual maximum impact, and coverage percentages for D6010 differ by plan. This use case treats implant coverage as active with no waiting period; if the real-world plan has a waiting period, this is a named open test finding at benefit verification.

### CDT Codes in Scope

| CDT Code | Description | Provider | POS | Commercial Coverage Note |
|---|---|---|---|---|
| `D0140` | Limited oral evaluation — problem focused | General dental practice | 11 | Covered |
| `D0220` | Periapical radiographic image | General dental practice | 11 | Covered |
| `D7210` | Surgical extraction — erupted tooth requiring elevation and/or forceps removal | Oral surgery practice | 11 | Covered; major service cost-sharing applies |
| `D6010` | Surgical placement of implant body — endosteal implant | Oral surgery practice | 11 | Covered — confirm waiting period and annual maximum impact; variable by plan |

### LOINC Codes in Scope

| LOINC Code | Description | FHIR Resource | Use in This Case |
|---|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport`, `ImagingStudy` | Periapical radiograph — general dental practice |

---

## Appendix B: Data

### 1. Patient Resource Data

*(Identical to Use Case A except for coverage identifiers)*

| FHIR Element | Value | System / Note |
|---|---|---|
| **Name** | Frank Castle | Given: Frank; Family: Castle |
| **Date of Birth** | 1972-03-17 | Age: 53 |
| **Sex** | Male | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **General Dental Practice MRN** | `GDENT-TX-2026-0047` | System: `https://generaldental.example.org/fhir/mrn` |
| **Oral Surgery Practice MRN** | `ORALSURG-TX-2026-0031` | System: `https://oralsurgery.example.org/fhir/mrn` |
| **Commercial Member ID** | `COMM-TX-00819472` | System: commercial payer member ID |
| **Group Number** | 582047 | Employer group |
| **Telecom (Phone)** | (512) 555-0147 | Use: Mobile |
| **Telecom (Email)** | frank.castle@example.com | Use: Home |
| **Address** | 918 South Congress Avenue, Apt 6, Austin, TX 78704 | City: Austin; State: TX; ZIP: 78704 |
| **Language** | English | Preferred language |
| **Active** | True | Patient record is active |

---

### 2. Coverage Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Payer** | Commercial Dental PPO (Synthetic) | Test data label |
| **Plan Type** | PPO | Preferred Provider Organization |
| **Member ID** | COMM-TX-00819472 | Member identifier |
| **Group Number** | 582047 | Employer group |
| **Coverage Period** | 2026-01-01 – 2026-12-31 | Plan year |
| **Status** | Active | Coverage confirmed |
| **Annual Maximum** | $2,000 | Per member, per plan year |
| **Remaining Annual Maximum** | $1,720 | At time of benefit verification |
| **Basic Services (Extractions)** | 80% covered after deductible | In-network |
| **Major Services (Implants — D6010)** | 50% covered after deductible | In-network; confirm waiting period |
| **Implant Waiting Period** | None — waived (plan year 3+) | Confirmed at benefit verification |
| **Prior Authorization Required** | None for D7210 or D6010 | Confirmed via CRD |
| **Payer EDI ID** | COMM-TX-PPO-EDI | HIPAA X12 claims routing (synthetic) |
| **Payer FHIR Endpoint** | `https://commercial-dental.example.org/fhir/r4` | Synthetic commercial payer FHIR API |

---

### 3. Organization Resource Data

*(General dental practice and oral surgery practice identical to Use Case A)*

#### Commercial Dental Payer

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | Commercial Dental PPO (Synthetic) | Test data label — to be filled with actual payer |
| **Type** | Commercial Dental Plan | Organization type |
| **Payer EDI ID** | COMM-TX-PPO-EDI | X12 claims routing (synthetic) |
| **FHIR Endpoint** | `https://commercial-dental.example.org/fhir/r4` | Synthetic FHIR API |

---

### 4. Practitioner Resource Data

*(Identical to Use Case A — Dr. Mary Parker and Dr. Alex Maxil)*

---

### 5. Workflow & Service Data

#### ServiceRequest (Referral — General Dental Practice to Oral Surgery Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Referral fulfilled |
| **Intent** | Order | Clinical order |
| **Category** | Consultation / Referral | Type |
| **Priority** | Routine | Non-urgent |
| **Code** | Surgical extraction tooth #30 with option for immediate implant placement — non-restorable following root canal failure | Referral reason |
| **Subject** | Frank Castle | Patient reference |
| **Requester** | Dr. Mary Parker, DDS | General dental provider |
| **Performer** | Dr. Alex Maxil, DDS, MD | Oral surgeon |
| **Reason Code** | K04.7 (periapical abscess without sinus); K08.89 (non-restorable tooth) | ICD-10 diagnoses |
| **Insurance** | Coverage reference — Commercial Dental PPO; no PA required | Benefit verification confirmed |
| **Ordered Date** | 2026-07-08 | Referral date |
| **Occurrence DateTime** | 2026-07-15 | Surgical consultation date |
| **Description** | Patient presents with recurrent periapical infection and vertical root fracture on tooth #30 following prior root canal treatment. Tooth non-restorable. No PA required under commercial plan. Benefits verified — implant coverage active, annual maximum $1,720 remaining. Two options discussed: (1) extraction only (D7210); (2) extraction with immediate implant placement (D7210 + D6010). Final treatment election deferred to surgical consultation. Referral package includes periapical radiograph, periodontal charting, intraoral images, and confirmed diagnosis. | Referral payload |

#### Procedure (Surgical Extraction — Oral Surgery Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Code** | D7210 (CDT) | Surgical extraction |
| **Subject** | Frank Castle | Patient reference |
| **Performer** | Dr. Alex Maxil, DDS, MD | Oral surgeon |
| **Performed DateTime** | 2026-07-15 | Date of procedure |
| **Body Site** | Tooth #30 (FDI: 46) | Lower right first molar |
| **Note** | Surgical extraction completed. Flap reflected; tooth sectioned; vertical root fracture confirmed. Socket prepared for immediate implant placement. | Operative note |

#### Procedure (Immediate Implant Placement — Oral Surgery Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Code** | D6010 (CDT) | Surgical placement of implant body — endosteal implant |
| **Subject** | Frank Castle | Patient reference |
| **Performer** | Dr. Alex Maxil, DDS, MD | Oral surgeon |
| **Performed DateTime** | 2026-07-15 | Same visit as extraction |
| **Body Site** | Tooth #30 site (FDI: 46) | Lower right first molar region |
| **Device** | Implant specifications — see Device resource below | Implant record |
| **Note** | Immediate implant placed following extraction. Bone density adequate; primary stability achieved. Placement torque: 35 Ncm. Healing abutment placed. Patient instructed on implant care. Osseointegration period: 3–4 months before restorative phase. | Operative note |

#### Device (Implant Specifications)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Active | Implant in situ |
| **Type** | Endosteal dental implant | Device type |
| **Manufacturer** | Implant Manufacturer (Synthetic) | To be filled with actual manufacturer |
| **Catalog Number** | IMPL-4.0-11.5-SYN | Diameter 4.0mm; length 11.5mm (synthetic catalog number) |
| **Lot Number** | LOT-2026-04821 | Manufacturing lot (synthetic) |
| **Manufacture Date** | 2025-11-01 | Manufacturing date |
| **Body Site** | Tooth #30 site (FDI: 46) | Placement location |
| **Patient** | Frank Castle | Patient reference |
| **Placement Torque** | 35 Ncm | Primary stability metric |
| **Note** | Transmitted to general dental practice in post-operative summary to support future restorative phase (crown placement). Restorative provider will need implant specifications to select appropriate abutment and crown components. | Restorative continuity note |

#### ClinicalImpression (Post-Operative Summary — Oral Surgery Practice to General Dental Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Summary complete |
| **Date** | 2026-07-15 | Date of summary |
| **Assessor** | Dr. Alex Maxil, DDS, MD | Oral surgeon |
| **Summary** | Frank Castle seen 2026-07-15 per referral from general dental practice. Periapical abscess (K04.7) and non-restorable tooth #30 confirmed; vertical root fracture confirmed intraoperatively. Surgical extraction of tooth #30 completed (D7210). Immediate endosteal implant placed (D6010) — see Device record for full specifications. Primary stability achieved at 35 Ncm placement torque. Healing abutment placed. Post-operative instructions provided. Anticipated osseointegration period: 3–4 months. Patient to return to general dental provider for restorative phase (implant crown) after osseointegration confirmed at follow-up. | Post-operative summary |
| **Device Reference** | Implant Device resource — full specifications included | Transmitted for restorative continuity |
| **Recommendations** | 1. Follow-up at oral surgery in 1 week for healing check; 2. Restorative phase (D6065 or D6066 crown) at general dental practice approximately 4 months post-placement, pending osseointegration; 3. Implant specifications transmitted — abutment and crown components to be selected by restorative provider using Device record | Restorative plan |

---

### 6. Clinical Codes & Mappings

#### ICD-10 Diagnosis Codes

| Code | Description | Application |
|---|---|---|
| K04.7 | Periapical abscess without sinus | Presenting diagnosis; confirmed intraoperatively |
| K08.89 | Other specified disorders of teeth | Non-restorable — vertical root fracture confirmed |

#### CDT Codes in Scope

| Code | Description | Provider | POS | Commercial Coverage Note |
|---|---|---|---|---|
| `D0140` | Limited oral evaluation — problem focused | General dental practice | 11 | Covered |
| `D0220` | Periapical radiographic image | General dental practice | 11 | Covered |
| `D7210` | Surgical extraction — erupted tooth | Oral surgery practice | 11 | Covered; 80% after deductible |
| `D6010` | Surgical placement of implant body — endosteal implant | Oral surgery practice | 11 | Covered; 50% after deductible; waiting period confirmed waived |

#### LOINC Codes

| LOINC | Description | FHIR Resource |
|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport`, `ImagingStudy` |

---

### 7. Timeline & Dates

| Event | Date | Time | Actor | System |
|---|---|---|---|---|
| **Limited oral evaluation and radiograph** | 2026-07-08 | 10:00 | Dr. Parker | General dental PMS |
| **Real-time benefit verification** | 2026-07-08 | 10:30 | General dental staff | PDex → Commercial payer FHIR API |
| **CRD hook — no PA required confirmed** | 2026-07-08 | 10:32 | General dental EHR | CRD → commercial payer FHIR API |
| **Structured referral transmitted** | 2026-07-08 | 11:00 | Dr. Parker's staff | CDex push → Oral surgery interim FHIR server |
| **Patient notified — referral sent** | 2026-07-08 | 11:00 | Patient application | FHIR Subscription event |
| **Referral received; appointment scheduled** | 2026-07-08 | 11:30 | Oral surgery staff | Dental PMS |
| **AppointmentResponse returned** | 2026-07-08 | 11:35 | Oral surgery system | Interim FHIR → General dental practice FHIR |
| **Patient notified — appointment confirmed** | 2026-07-08 | 11:35 | Patient application | FHIR Subscription event |
| **Surgical consultation and procedures** | 2026-07-15 | 09:00 | Dr. Maxil | Oral surgery PMS |
| **Post-operative summary + Device record transmitted** | 2026-07-15 | 11:45 | Oral surgery system | CDex push → General dental practice FHIR |
| **Referral closed** | 2026-07-15 | 11:46 | General dental system | ServiceRequest → completed |
| **Patient application updated** | 2026-07-15 | 11:46 | Patient application | FHIR Subscription event |
| **837D submitted — general dental practice** | 2026-07-16 | 08:00 | Billing | D0140, D0220 → commercial payer EDI |
| **837D submitted — oral surgery practice** | 2026-07-16 | 08:30 | Billing | D7210, D6010 → commercial payer EDI |

#### Key Timeline Constraints

| Constraint | Target | Rationale |
|---|---|---|
| **Benefit verification** | Same visit as evaluation | Informs treatment discussion with patient |
| **Referral transmission** | Same day as evaluation | No PA delay; commercial coverage confirmed |
| **Surgical appointment** | Within 7 days of referral | Routine; pain managed |
| **Post-operative summary + Device record return** | Same day as surgical encounter | Closes referral loop; Device record available for restorative planning |
| **Restorative phase (crown)** | 4 months post-implant | Osseointegration period |

---

*This dataset is a test and validation vehicle for the Oral Health Data Exchange (ODE) Implementation Guide, developed under HL7 and sponsored by the PIE Work Group (PSS-2714). It is intended for use in connectathon and interoperability testing environments only. oralhealthalliance.net*
