# CMS Connectathon — Dental Interoperability Test Dataset
## Use Case: Head & Neck Cancer — Prior Authorization, Dental Clearance, and Pre-Radiation Dental Treatment

---

## Table of Contents

- [Section I: Business Overview](#section-i-business-overview)
- [Section II: Narrative-to-Standards Mapping](#section-ii-narrative-to-standards-mapping)
- [Section III: Technical Overview](#section-iii-technical-overview)
  - [Implementation Guides](#implementation-guides)
  - [Key FHIR Resources Exercised](#key-fhir-resources-exercised)
  - [Cross-Cutting Test Objectives](#cross-cutting-test-objectives)
- [Section IV: EDI Transactions](#section-iv-edi-transactions)
  - [EDI Transactions in Scope](#edi-transactions-in-scope)
  - [CDT-to-CPT Crosswalk for Medical Billing](#cdt-to-cpt-crosswalk-for-medical-billing)
  - [LOINC Codes in Scope](#loinc-codes-in-scope)
- [Appendix: Data](#appendix-data)

---

## Section I: Business Overview

**Patient:** John Smith  
**Date of Birth:** 11/14/1962 (Age: 63)  
**Diagnosis:** Stage IV squamous cell carcinoma of the lateral border of the tongue (`ICD-10: C02.1`)  
**Treatment Center:** Fox Chase Cancer Center (FCCC)  
**Insurance:** Independence Blue Cross (IBX) Medicare Advantage — Member ID: `H1234567800`

### Care Team

| Role | Provider |
|---|---|
| Surgical Oncology | Dr. Cecelia Schmalbach, Chair of Surgical Oncology, FCCC |
| Head & Neck Radiation Oncology | Dr. Thomas Galloway, Service Chief, FCCC |
| Medical Physicist | Dr. Teh Lin, FCCC |
| Oral Oncology / Dental Clearance | Dr. Thomas Sollecito, Penn Dental Family Practice |

---

### Clinical Narrative

Dr. Galloway's back office used their **Oracle Health (Cerner) EHR** to check John's IBX Medicare Advantage plan. The system indicated that a prior authorization (PA) was required for the planned course of **intensity-modulated radiation therapy (IMRT)** — delivered five days a week over six to seven weeks — and flagged a **dental clearance as a mandatory prerequisite**. This policy is essential to mitigate the risk of **osteoradionecrosis** caused by high-dose radiation to the jaw.

Dr. Galloway referred John to **Dr. Thomas Sollecito at Penn Dental Family Practice**, a specialist in oral oncology. The referral and John's oncology records were transmitted directly into Dr. Sollecito's **Eaglesoft** system. John was notified via his **patient app**, which presented a unified view of his FCCC and Penn Dental records.

> **Timeline constraint:** Dr. Sollecito had fewer than **21 days** to evaluate John and return a clearance to FCCC.

Dr. Sollecito examined John **15 days before** the planned radiation start. After examination and radiographs (`D0220`, `D0330`), he identified three teeth requiring extraction:

- **Tooth #4** — standard extraction
- **Tooth #17** — impacted wisdom tooth
- **Tooth #30** — complex; required site-specific radiation dose data before a plan could be finalized

Dr. Sollecito submitted a request for **Dosimetric Dental Contouring (DDC)** data from Dr. Galloway's team. The request was routed to **Dr. Teh Lin, Medical Physicist**, who extracted the site-specific dose from the radiation planning system. Two days later, FCCC transmitted the planned dose for the tooth #30 site: **52 Gray (Gy)**.

Because 52 Gy exceeds the safe healing threshold, Dr. Sollecito elected to:

- Extract tooth #30 (`D7210`)
- Place a dental implant (`D6010`) immediately
- Request a **14-day delay** to the radiation start date to allow for healing — agreed to by Dr. Galloway

Once the extractions were complete, Dr. Sollecito transmitted the **dental clearance** back to FCCC as structured clinical data (`SNOMED 146328D`). John's app updated to confirm the clearance was received and the prior authorization was approved. Dr. Galloway's office submitted the final authorization to IBX, and John began treatment on the revised start date.

---

## Section II: Narrative-to-Standards Mapping

The table below maps each key business event in John's care journey to the underlying implementation guide or standard enabling it. Steps marked **"Dental Interoperability (Under Development)"** identify transactions governed by the **Oral Health Data Exchange (OHDE) IG** — the new standard this use case is designed to test and validate.

| What Happens (Business Language) | Implementation Guide / Standard | Key Transaction |
|---|---|---|
| **Check Insurance Coverage:** Dr. Galloway's office checks John's IBX plan for IMRT coverage and rules. | Da Vinci Coverage Requirements Discovery (CRD) | CDS Hook (`order-sign`) triggered in Cerner; returns coverage requirements. |
| **Identify Documentation Needs:** EHR flags that a dental clearance is required before IMRT can be authorized. | Da Vinci Documentation Templates and Rules (DTR) | Questionnaire retrieved and pre-populated to surface the clearance requirement. |
| **Refer to Specialist:** Dr. Galloway sends the referral and oncology records to Dr. Sollecito. | US Core / OHDE (Under Development) | `ServiceRequest` (referral) and `DocumentReference` (records) sent to Penn Dental. |
| **Patient Notification:** John receives notification that his referral was sent and received. | FHIR Subscriptions Backport IG | Subscription event triggered on `ServiceRequest` creation. |
| **Consolidated Patient View:** John views his FCCC and Penn Dental records in a single app. | US Core / SMART App Launch | US Core Patient Access API for provider clinical records from FCCC and Penn Dental; SMART App Launch as the authorization framework. |
| **Request Radiation Data:** Dr. Sollecito requests the radiation dose (Gy) at the tooth #30 site. | US Core / OHDE (Under Development) | `CommunicationRequest` sent from Penn Dental to the FCCC Medical Physicist. |
| **Send Dosimetry Data:** Dr. Teh Lin sends the 52 Gray dose map for tooth #30. | US Core / OHDE (Under Development) | `Observation` (radiation dose) wrapped in a `DiagnosticReport` sent to Dr. Sollecito. |
| **Request Treatment Delay:** Dr. Sollecito asks Dr. Galloway to push the radiation start date back 14 days. | US Core / OHDE (Under Development) | `Communication` sent to FCCC; updates the `CarePlan` and `ServiceRequest` start dates. |
| **Document Procedures:** Dr. Sollecito records extractions (#4, #17, #30) and implant placement. | US Core / OHDE (Under Development) | `Procedure` resources (CDT codes) + `Observation` (`bodySite`: tooth numbering). |
| **Submit Dental Clearance:** Dr. Sollecito sends the final "Orally Fit" attestation to FCCC. | OHDE (Under Development) / CDex | `ClinicalImpression` (attestation) pushed from Penn Dental to FCCC via CDex provider-to-provider structured data exchange; CDex Task closed on clearance receipt. |
| **Submit Prior Auth:** Dr. Galloway's office submits the final IMRT request with dental data attached. | Da Vinci PAS / CDex | `Claim` (PA) submitted to IBX via PAS; dental clearance bundle transmitted to IBX as a CDex unsolicited attachment via the `$submit-attachment` operation, referenced in `Claim.supportingInfo`. |
| **Final Approval:** IBX approves the treatment; John's app shows "Approved." | Da Vinci PAS / Da Vinci PDex (PPA Profile) / CARIN Blue Button | `ClaimResponse` returned via PAS; `ExplanationOfBenefit` (`use = preauthorization`) made available to John via PDex PPA Profile within one business day of PA decision; patient-facing app developer implements CARIN Blue Button as the patient access API framework to query IBX's endpoint. |

---

## Section III: Technical Overview

This use case exercises a **multi-system, multi-organization clinical workflow** spanning an oncology EHR, a private dental practice management system, a health plan, and a patient-facing application. The scenario tests the full lifecycle of a prior authorization workflow with an embedded cross-organizational clinical data exchange — from coverage discovery at point of order entry through structured clearance return and PA approval.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

### Implementation Guides

| Implementation Guide | Purpose in This Use Case |
|---|---|
| **US Core IG** | Defines FHIR profiles for patient, condition, encounter, procedure, referral, and clinical data exchanged across all organizations |
| **Da Vinci Coverage Requirements Discovery (CRD)** | Fired at IMRT order entry; returns PA requirement and dental clearance prerequisite in real time without a portal |
| **Da Vinci Documentation Templates and Rules (DTR)** | Retrieves payer questionnaire, pre-populates EHR data, and surfaces dental clearance as an open documentation requirement |
| **Da Vinci Prior Authorization Support (PAS)** | Submits the completed PA request to the health plan after structured dental clearance is received and the DTR documentation package is complete |
| **Da Vinci Clinical Data Exchange (CDex)** | Three roles in this use case: (1) **Task-based workflow** — tracks the open dental clearance documentation requirement as a Task, opened at DTR launch and closed when the structured clearance is returned by Dr. Sollecito; (2) **Provider-to-provider data push** — governs structured exchange of the clearance from Penn Dental to FCCC; (3) **Unsolicited attachment to payer** — the `$submit-attachment` operation transmits the dental clearance bundle to IBX in support of the PAS prior authorization submission |
| **Da Vinci Payer Data Exchange (PDex)** | Enables John's patient app to access payer-held clinical and coverage data from IBX; the PDex Prior Authorization (PPA) profile delivers the `ExplanationOfBenefit` (`use = preauthorization`) to John's app within one business day of the PA decision |
| **CARIN Blue Button (CARIN BB)** | Defines the patient access API framework that John's patient-facing app implements to query IBX's endpoint; within the PA approval scope of this use case, this is the mechanism through which the PDex PPA profile (`ExplanationOfBenefit` with `use = preauthorization`) is surfaced to John |
| **SMART App Launch IG** | Authorization framework enabling John's patient app to securely connect to FCCC, Penn Dental's interim FHIR server, and the health plan without separate logins |
| **FHIR Subscriptions Backport IG** | Delivers proactive push notifications to John's patient app at each key workflow milestone |
| **Oral Health Data Exchange IG (OHDE)** | New IG under development; this use case serves as a primary test and validation vehicle for OHDE, governing structured exchange of oral health clinical data — findings, diagnoses, procedures, and clearance attestation — between Penn Dental and FCCC |

---

### Key FHIR Resources Exercised

| FHIR Resource | Source IG / Profile | Purpose in This Use Case |
|---|---|---|
| `Patient` | US Core | Cross-organizational patient identity matching between FCCC EHR, Eaglesoft interim FHIR server, and health plan |
| `Coverage` | US Core / CRD | John's insurance plan information — member ID, group, payer — passed to the CRD server at order entry to evaluate coverage requirements; also surfaced in patient app via PDex |
| `InsurancePlan` | Da Vinci PDex | Health plan product and benefit structure referenced by the Coverage resource |
| `Practitioner` | US Core / CRD | Dr. Galloway (ordering provider) and Dr. Sollecito (rendering provider) identity and credentials |
| `PractitionerRole` | US Core / CRD | Role context for Dr. Galloway (radiation oncology at FCCC) and Dr. Sollecito (dentist, private practice) — required by CRD for coverage evaluation |
| `Organization` | US Core / CRD | FCCC (ordering organization), Penn Dental (rendering organization), and IBX (payer organization) |
| `Location` | US Core / CRD | Physical location of FCCC radiation oncology department and Penn Dental — required by CRD for place-of-service coverage rules |
| `Encounter` | US Core | Each clinical encounter — oncology visits and dental visits — providing context for all procedures and observations |
| `ServiceRequest` | US Core / OHDE | Referral from FCCC to Penn Dental; IMRT order triggering CRD; updated to reflect revised IMRT start date |
| `CarePlan` | US Core | Oncology treatment plan (IMRT + possible surgical resection); dental treatment plan for teeth #4, #17, and #30 |
| `DocumentReference` | US Core | Oncology records transmitted with referral — pathology report, treatment plan, simulation parameters |
| `Condition` | US Core / OHDE | Oncologic diagnosis (`C02.1`) and dental diagnoses for teeth #4, #17, and #30; updated to resolved after treatment |
| `Observation` | US Core / OHDE | Dental clinical findings per tooth; pulp vitality test results; radiation dose data (52 Gy at tooth #30 site) |
| `DiagnosticReport` | US Core / OHDE | DDC report wrapping the radiation dose observation from FCCC physics team |
| `ImagingStudy` | US Core | Dental radiographic images — periapical and panoramic X-rays — referenced in clinical findings and clearance |
| `Procedure` | US Core / OHDE | Dental procedures performed — extractions ×3 (`D7210`), implant placement (`D6010`); also IMRT delivery procedure at FCCC |
| `ClinicalImpression` | OHDE | Dr. Sollecito's structured dental clearance attestation — the structured data equivalent of the dental clearance form |
| `Appointment` / `AppointmentResponse` | US Core | Dental appointment scheduling for John at Penn Dental; surfaced in patient app via FHIR Subscriptions |
| `Communication` / `CommunicationRequest` | US Core / OHDE | DDC data request from Penn Dental to FCCC; DDC response; IMRT delay request and authorization between providers |
| `Task` | Da Vinci DTR / CDex | Tracks the open dental clearance documentation requirement as an actionable item; closed when structured clearance is returned |
| `Questionnaire` / `QuestionnaireResponse` | Da Vinci DTR | Payer's dental clearance documentation requirements and completed provider responses pre-populated from EHR data |
| `Claim` (PA) | Da Vinci PAS | Prior authorization request submitted to health plan after DTR documentation package is complete |
| `ClaimResponse` | Da Vinci PAS | Health plan PA approval response — includes PA number and approved service details |
| `ExplanationOfBenefit` | CARIN Blue Button | John's app displays claim submissions, adjudication results, and patient cost responsibility as claims process through the health plan |
| `Subscription` / `SubscriptionStatus` | FHIR Subscriptions Backport IG | Event notifications pushed to John's patient app at each key workflow milestone — referral sent, appointment scheduled, DDC received, clearance transmitted, PA approved |
| `Bundle` | FHIR Core | Transaction and document bundles wrapping multi-resource exchanges — referral packet, DDC report, PA submission, and dental clearance return |
| `AuditEvent` | US Core | Logging of cross-organizational data access events for compliance and provenance tracking |
| `Provenance` | US Core | Records the chain of custody for clinical data — who created, transmitted, and received each resource throughout the workflow |

---

### Cross-Cutting Test Objectives

1. **Patient matching across unaffiliated systems** — FCCC EHR, Eaglesoft via interim FHIR server, and the health plan must resolve John's identity without a shared master patient index.

2. **Coverage and plan data at point of order** — `Coverage` and `InsurancePlan` resources must be available in the EHR at the moment the IMRT order is placed for CRD to evaluate requirements correctly.

3. **Provider and organization context for CRD** — `Practitioner`, `PractitionerRole`, `Organization`, and `Location` must all be correctly populated for the CRD server to apply the right coverage rules for place of service and ordering provider type.

4. **Interim FHIR server as a dental interoperability bridge** — Eaglesoft's lack of native FHIR capability is addressed through an interim server; this use case tests whether that architecture can support both inbound referral receipt and outbound structured clinical data return.

5. **Structured data as the clearance** — No PDF or paper form is used; the dental clearance is composed entirely of discrete FHIR resources, testing whether a payer can accept and adjudicate a PA based on structured clinical data alone.

6. **DDC as a novel FHIR observation type** — Site-specific radiation dose data transmitted from a radiation planning system to a dental EHR has no established LOINC code; this use case surfaces that gap for the OHDE IG development process.

7. **OHDE IG validation** — This use case is a primary test vehicle for the Oral Health Data Exchange IG, published through HL7 and sponsored by the PIE Work Group (PSS-2714), exercising its profiles for oral health findings, procedures, and clearance attestation in a live connectathon environment.

8. **Task lifecycle for documentation requirements** — The `Task` resource tracking the open dental clearance requirement must correctly open at DTR launch and close upon receipt of the structured clearance, triggering PAS submission.

9. **Patient app as a real-time participant** — John's app receives data from three independent sources and surfaces a coherent care timeline, testing PDex, CARIN BB, US Core, SMART on FHIR, and FHIR Subscriptions in a single patient-facing scenario.

---

## Section IV: EDI Transactions

Because John's IBX plan is a **Medicare Advantage medical benefit**, all services in this use case — including Dr. Sollecito's dental examination, radiographs, extractions, and implant placement — are billed as **medically necessary** under the medical benefit. No dental benefit claim (837D) is in scope. Dr. Sollecito bills as a specialty provider on a professional medical claim.

This use case is built on a FHIR-native prior authorization workflow using **Da Vinci PAS**, which replaces the legacy X12 278 transaction with FHIR `Claim` and `ClaimResponse` resources. The X12 278 is therefore not in scope.

### EDI Transactions in Scope

| X12 Transaction | Trigger | Scope Note |
|---|---|---|
| **270 / 271** — Eligibility & Benefit Inquiry / Response | Dr. Galloway's office checks John's IBX medical benefit at IMRT order entry | Queries medical benefit; service type codes for radiation oncology and medically necessary oral surgery |
| **837P** — Professional Medical Claim (FCCC) | FCCC bills for IMRT planning and delivery | CPT codes 77385/77386 (IMRT delivery) + 77387 (IGRT); Place of Service 22 (outpatient hospital) |
| **837P** — Professional Medical Claim (Penn Dental) | Dr. Sollecito bills for exam, radiographs, extractions, and implant as medically necessary | CDT codes billed on medical claim; see crosswalk note below |
| **835** — Remittance Advice | IBX adjudicates and pays both claims | Claim adjustment reason codes; patient responsibility |
| **FHIR-native clearance transmission (CDex)** | Dental clearance documentation transmitted from Dr. Sollecito to FCCC and to IBX in support of the PA submission | No 275 claim attachment transaction; clearance is transmitted as FHIR resources — `ClinicalImpression`, `DocumentReference`, or a purpose-built OHDE resource — via CDex provider-to-provider data push (Penn Dental → FCCC) and CDex `$submit-attachment` operation (FCCC → IBX). Resource type and `Claim.supportingInfo` reference structure are open design questions for the OHDE IG. |

> **Note on 278:** Da Vinci PAS uses FHIR `Claim` and `ClaimResponse` resources for prior authorization. The X12 278 request and response are **not** exercised in this use case.

---

### CDT-to-CPT Crosswalk for Medical Billing

When Dr. Sollecito bills Penn Dental's procedures on an 837P medical claim, the claim may require CPT codes in place of — or alongside — CDT codes. The mapping below reflects the best available cross-coding guidance; confidence levels are noted explicitly.

> ⚠️ **Implementation note:** Multiple billing authorities note that many medical payers will accept CDT codes directly on medical claims when medical necessity is established and documented. Whether IBX requires CPT crosscodes or will accept CDT codes on the 837P is an **open question** this use case should surface as a named test finding. The crosswalk below is provided for reference, not as a definitive billing requirement.

| CDT Code | Procedure | CPT Cross-Code | CPT Description | Confidence |
|---|---|---|---|---|
| `D0220` | Periapical radiographic image | `70300` | Radiologic examination, teeth; single view | ✅ Confirmed |
| `D0330` | Panoramic radiographic image | *Unconfirmed* | No authoritative cross-code identified; `70355` is sometimes cited but not verified | ⚠️ Unconfirmed — flag as test finding |
| `D7210` | Surgical extraction ×3 | `41899` | Unlisted procedure, dentoalveolar structures | ✅ Confirmed — **requires narrative report**; no direct CPT equivalent exists |
| `D6010` | Surgical placement of implant body | `21248` | Reconstruction of mandible or maxilla, endosteal implant (partial) | ✅ Confirmed |

> **On `41899` (unlisted):** Because there is no direct CPT equivalent for surgical tooth extraction, `41899` is an unlisted procedure code. Claims submitted with unlisted codes require a detailed operative narrative and supporting clinical documentation. This is a practical barrier to medical billing for dental procedures and is itself a meaningful test finding for this use case.

---

### LOINC Codes in Scope

LOINC codes appear in `Observation.code`, `DiagnosticReport.code`, and `DocumentReference.type` in FHIR resources. The following LOINC codes are applicable to clinical data generated in this use case.

| LOINC Code | Description | FHIR Resource | Use in This Case |
|---|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport`, `ImagingStudy` | D0220 periapical radiograph — Dr. Sollecito's exam |
| `24828-6` | XR tomography Mandible Panoramic | `DiagnosticReport`, `ImagingStudy` | D0330 panoramic radiograph — Dr. Sollecito's exam |
| `46386-9` | XR Teeth Bitewing Views | `DiagnosticReport` | Supplemental radiographic reference if bitewings taken |
| *(No LOINC code established)* | Site-specific radiation dose (Gy) at tooth site | `Observation` | 52 Gy DDC data from Dr. Teh Lin — **gap surfaced by this use case; a named OHDE IG test objective** |

> **LOINC gap:** The site-specific dosimetric dental contouring (DDC) observation — radiation dose in Gray at a specific tooth site — has no established LOINC code. This use case is designed to surface that gap as an action item for the OHDE IG development process and the PIE Work Group.

---

## Appendix: Data

### Patient

| Field | Value |
|---|---|
| Name | John Smith |
| Date of Birth | 11/14/1962 |
| Age | 63 |
| Sex | Male |
| Insurance | Independence Blue Cross (IBX) Medicare Advantage |
| Member ID | H1234567800 |
| Diagnosis | Stage IV SCC, lateral border of tongue |
| ICD-10 | C02.1 |

### Providers

| Provider | Role | Organization | System |
|---|---|---|---|
| Dr. Thomas Galloway | Service Chief, Head & Neck Radiation Oncology | Fox Chase Cancer Center (FCCC) | Oracle Health (Cerner) |
| Dr. Cecelia Schmalbach | Chair, Surgical Oncology | Fox Chase Cancer Center (FCCC) | Oracle Health (Cerner) |
| Dr. Teh Lin | Medical Physicist | Fox Chase Cancer Center (FCCC) | — |
| Dr. Thomas Sollecito | Oral Oncology / Dental Clearance | Penn Dental Family Practice | Eaglesoft (interim FHIR server) |

### CDT Codes Referenced

| Code | Description |
|---|---|
| `D0220` | Periapical radiographic image |
| `D0330` | Panoramic radiographic image |
| `D7210` | Extraction of erupted tooth requiring removal of bone and/or sectioning of tooth |
| `D6010` | Surgical placement of implant body |

### Key Clinical Values

| Data Point | Value |
|---|---|
| Radiation dose at tooth #30 | 52 Gray (Gy) |
| Dental clearance code | SNOMED `146328D` |
| Clearance deadline | 21 days from referral |
| Days before planned start (exam) | 15 days |
| Radiation delay requested | 14 days |

---

*This dataset is a test and validation vehicle for the Oral Health Data Exchange (OHDE) Implementation Guide, developed under HL7 and sponsored by the PIE Work Group (PSS-2714). It is intended for use in connectathon and interoperability testing environments only.*