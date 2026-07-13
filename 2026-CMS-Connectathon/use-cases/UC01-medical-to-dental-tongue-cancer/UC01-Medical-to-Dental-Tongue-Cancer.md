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
  - [Encounter Enumeration](#0-encounter-enumeration)
  - [Coverage Details](#appendix-coverage-details)
  - [Provider Data](#appendix-provider-data)
  - [Clinical Values](#appendix-clinical-values)

---

## Section I: Business Overview

John Smith is a 63-year-old male (DOB: 11/14/1962) diagnosed with **Stage IV squamous cell carcinoma of the lateral border of the tongue** (`ICD-10: C02.1`). His care at **Fox Chase Cancer Center (FCCC)** is led by a multidisciplinary team including **Dr. Renata Osei**, Chair of Surgical Oncology, and **Dr. Marcus Whitfield**, Service Chief of Head and Neck Radiation Oncology.

The integrated treatment plan developed by the team calls for a course of **intensity-modulated radiation therapy (IMRT)** overseen by Dr. Whitfield — delivered five days a week over six to seven weeks — followed by possible surgical resection performed by Dr. Osei.

Dr. Whitfield's back office used their **Oracle Health (Cerner) EHR** to check John's **Independence Blue Cross (IBX) Medicare Advantage plan** (Personal Choice 65 PPO, CMS Plan H3909; Member ID: `H1234567800`). The system indicated that a **prior authorization was required for the IMRT** and launched a documentation tool flagging a **dental clearance as a mandatory prerequisite**. This policy is essential to mitigate the risk of **osteoradionecrosis** caused by high-dose radiation to the jaw.

Dr. Whitfield refers John to **Dr. Andrew Bellweather at Penn Dental Family Practice**, a specialist in oral oncology. The referral and John's oncology records are transmitted directly into Dr. Bellweather's **Eaglesoft** system. John is notified via his **patient app**, which shows a unified view of his FCCC and Penn Dental records. **The clock is tight: Dr. Bellweather has fewer than 21 days to evaluate John and return a clearance to FCCC.**

Dr. Bellweather sees John **15 days before** the planned radiation start. After a thorough examination and radiographs (`D0220` periapical, `D0330` panoramic), he finds three teeth requiring extraction: **tooth #4** (standard extraction), **an impacted wisdom tooth (#17)**, and a more complicated situation on **tooth #30**. Dr. Bellweather cannot finalize the treatment plan for #30 without knowing the specific radiation dosage for that site. John monitors this information request in real time through his app.

Dr. Bellweather requests the radiation dose data from Dr. Whitfield's team. The request is routed to **Dr. Priya Nandakumar, a Medical Physicist at FCCC**, who extracts the specific **Dosimetric Dental Contouring (DDC)** data from the radiation planning system. Two days later, FCCC transmits the planned dose for the tooth #30 site: **52 Gray (Gy)**. Because this **exceeds the safe healing threshold of 45 Gy**, Dr. Bellweather elects to:

- Extract tooth #30 (`D7210` — extraction requiring bone removal)
- Place a dental implant (`D6010` — surgical placement of implant body) immediately to maintain vertical bone support
- Request a **14-day delay** to the planned radiation start date to allow for extraction healing and implant osseointegration — agreed to by Dr. Whitfield

Once the extractions are complete, Dr. Bellweather sends the **dental clearance** back to FCCC as **structured clinical data**. John's app updates to show the clearance is received and the prior authorization is approved. Dr. Whitfield's office submits the final authorization to IBX, and John begins treatment on the revised start date **14 days later than originally planned**.

Separately, Dr. Bellweather's own practice still needs to be paid for the extractions and implant it performed. Because John has no standalone dental plan — only IBX's medical coverage — this billing has to travel through the medical benefit, under the same CMS "inextricably linked" exception that made the dental clearance a covered prerequisite in the first place. **This use case does not model the actual claim submission.** Instead, it defines a single, standardized, interoperable data package — assembled from the clinical trail already established across the referral, the dosimetric findings, and the clearance itself — that any dental practice management system can hand off for automatic conversion into whatever format a given payer or CMS requires. The goal is not to solve billing for this one claim, but to establish an interoperable shape the industry can converge on, so that translating dental-as-medical billing into any payer's required format becomes a mechanical, automated step rather than manual, payer-specific work.

---

## Section II: Narrative-to-Standards Mapping

The table below maps each key business event in John's care journey to the underlying implementation guide or standard enabling it. Steps marked **"Dental Interoperability (Under Development)"** identify transactions governed by the **Oral Health Data Exchange (ODE) IG** — the new standard this use case is designed to test and validate.

| What Happens (Business Language) | Implementation Guide / Standard | Key Transaction |
|---|---|---|
| **Check Insurance Coverage:** Dr. Whitfield's office checks John's IBX plan for IMRT coverage and rules. | Da Vinci Coverage Requirements Discovery (CRD) | CDS Hook (`order-sign`) triggered in Cerner; returns coverage requirements. |
| **Identify Documentation Needs:** EHR flags that a dental clearance is required before IMRT can be authorized. | Da Vinci Documentation Templates and Rules (DTR) | Questionnaire retrieved and pre-populated to surface the clearance requirement. |
| **Refer to Specialist:** Dr. Whitfield sends the referral and oncology records to Dr. Bellweather. | US Core / ODE (Under Development) | `ServiceRequest` (referral) and `DocumentReference` (records) sent to Penn Dental. |
| **Patient Notification:** John receives notification that his referral was sent and received. | FHIR Subscriptions Backport IG | Subscription event triggered on `ServiceRequest` creation. |
| **Consolidated Patient View:** John views his FCCC and Penn Dental records in a single app. | US Core / SMART App Launch | US Core Patient Access API for provider clinical records from FCCC and Penn Dental; SMART App Launch as the authorization framework. |
| **Request Radiation Data:** Dr. Bellweather requests the radiation dose (Gy) at the tooth #30 site. | US Core / ODE (Under Development) | `CommunicationRequest` sent from Penn Dental to the FCCC Medical Physicist. |
| **Send Dosimetry Data:** Dr. Priya Nandakumar sends the 52 Gray dose map for tooth #30. | US Core / ODE (Under Development) | `Observation` (radiation dose) wrapped in a `DiagnosticReport` sent to Dr. Bellweather. |
| **Request Treatment Delay:** Dr. Bellweather asks Dr. Whitfield to push the radiation start date back. | US Core / ODE (Under Development) | **Correction:** not a formal `Communication` resource — modeled as an informal inter-provider note, the same mechanism as the DDC dose request (see Interaction 2 appendix). The resulting revised start date is captured formally via updates to `ServiceRequest`/`CarePlan`. |
| **Document Procedures:** Dr. Bellweather records extractions (#4, #17, #30) and implant placement. | US Core / ODE (Under Development) | `Procedure` resources (CDT codes) + `Observation` (`bodySite`: tooth numbering). |
| **Submit Dental Clearance:** Dr. Bellweather sends the final "Orally Fit" attestation to FCCC. | ODE (Under Development) / CDex | `ClinicalImpression` (attestation) pushed from Penn Dental to FCCC via CDex provider-to-provider structured data exchange; closes out via the **same referral Task** established at Interaction 1 (see below — not a second Task). |
| **Submit Prior Auth:** Dr. Whitfield's office submits the final IMRT request with dental data attached. | Da Vinci PAS / CDex | `Claim` (PA) submitted to IBX via PAS; dental clearance bundle transmitted to IBX as a CDex unsolicited attachment via the `$submit-attachment` operation, referenced in `Claim.supportingInfo`. |
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
| **Da Vinci Clinical Data Exchange (CDex)** | Three roles in this use case: (1) **Task-based workflow** — tracks the open dental clearance documentation requirement as a Task, opened at DTR launch and closed when the structured clearance is returned by Dr. Bellweather; (2) **Provider-to-provider data push** — governs structured exchange of the clearance from Penn Dental to FCCC; (3) **Unsolicited attachment to payer** — the `$submit-attachment` operation transmits the dental clearance bundle to IBX in support of the PAS prior authorization submission |
| **Da Vinci Payer Data Exchange (PDex)** | Enables John's patient app to access payer-held clinical and coverage data from IBX; the PDex Prior Authorization (PPA) profile delivers the `ExplanationOfBenefit` (`use = preauthorization`) to John's app within one business day of the PA decision |
| **CARIN Blue Button (CARIN BB)** | Defines the patient access API framework that John's patient-facing app implements to query IBX's endpoint; within the PA approval scope of this use case, this is the mechanism through which the PDex PPA profile (`ExplanationOfBenefit` with `use = preauthorization`) is surfaced to John |
| **SMART App Launch IG** | Authorization framework enabling John's patient app to securely connect to FCCC, Penn Dental's interim FHIR server, and the health plan without separate logins |
| **FHIR Subscriptions Backport IG** | Delivers proactive push notifications to John's patient app at each key workflow milestone |
| **Oral Health Data Exchange IG (ODE)** | New IG under development; this use case serves as a primary test and validation vehicle for ODE, governing structured exchange of oral health clinical data — findings, diagnoses, procedures, and clearance attestation — between Penn Dental and FCCC |

---

### Key FHIR Resources Exercised

| FHIR Resource | Source IG / Profile | Purpose in This Use Case |
|---|---|---|
| `Patient` | US Core | Cross-organizational patient identity matching between FCCC EHR, Eaglesoft interim FHIR server, and health plan |
| `Coverage` | US Core / CRD | John's insurance plan information — member ID, group, payer — passed to the CRD server at order entry to evaluate coverage requirements; also surfaced in patient app via PDex |
| `InsurancePlan` | Da Vinci PDex | Health plan product and benefit structure referenced by the Coverage resource |
| `Practitioner` | US Core / CRD | Dr. Whitfield (ordering provider) and Dr. Bellweather (rendering provider) identity and credentials |
| `PractitionerRole` | US Core / CRD | Role context for Dr. Whitfield (radiation oncology at FCCC) and Dr. Bellweather (dentist, private practice) — required by CRD for coverage evaluation |
| `Organization` | US Core / CRD | FCCC (ordering organization), Penn Dental (rendering organization), and IBX (payer organization) |
| `Location` | US Core / CRD | Physical location of FCCC radiation oncology department and Penn Dental — required by CRD for place-of-service coverage rules |
| `Encounter` | US Core | Each clinical encounter — oncology visits and dental visits — providing context for all procedures and observations |
| `ServiceRequest` | US Core / ODE | Referral from FCCC to Penn Dental; IMRT order triggering CRD; updated to reflect revised IMRT start date |
| `CarePlan` | US Core | Oncology treatment plan (IMRT + possible surgical resection); dental treatment plan for teeth #4, #17, and #30 |
| `DocumentReference` | US Core | Oncology records transmitted with referral — pathology report, treatment plan, simulation parameters |
| `Condition` | US Core / ODE | Oncologic diagnosis (`C02.1`) and dental diagnoses for teeth #4, #17, and #30; updated to resolved after treatment |
| `Observation` | US Core / ODE | Dental clinical findings per tooth; pulp vitality test results; radiation dose data (52 Gy at tooth #30 site) |
| `DiagnosticReport` | US Core / ODE | DDC report wrapping the radiation dose observation from FCCC physics team |
| `ImagingStudy` | US Core | Dental radiographic images — periapical and panoramic X-rays — referenced in clinical findings and clearance |
| `Procedure` | US Core / ODE | Dental procedures performed — extractions ×3 (`D7210`), implant placement (`D6010`); also IMRT delivery procedure at FCCC |
| `ClinicalImpression` | ODE | Dr. Bellweather's structured dental clearance attestation — the structured data equivalent of the dental clearance form |
| `Appointment` / `AppointmentResponse` | US Core | Dental appointment scheduling for John at Penn Dental; surfaced in patient app via FHIR Subscriptions |
| `Communication` / `CommunicationRequest` | US Core / ODE | IMRT delay request and authorization between providers (later encounter). **Correction:** the DDC data request/response between Dr. Bellweather and Dr. Nandakumar is *not* modeled as `Communication`/`CommunicationRequest` — see Encounter #2 appendix; it's an informal inter-provider note, not a formal resource, since it's a request for existing information (not an order) between practitioners already in an established referral relationship. |
| `Task` | Da Vinci DTR / CDex / IHE 360X | **Correction:** a single Task tracks both the referral relationship AND the payer's dental-clearance documentation requirement together — not two separate Task resources. Per base COW's own guidance, one Coordination Task per Request is the preferred pattern, with `Task.output` absorbing all fulfillment artifacts (the `ClinicalImpression` clearance included) and `businessStatus` progressing to reflect documentation status. "Multiple Coordination Tasks per Request" is explicitly out of scope for the 360X-adopted COW subset this project follows (see `ode-360x-adapter` crosswalk). |
| `Questionnaire` / `QuestionnaireResponse` | Da Vinci DTR | Payer's dental clearance documentation requirements and completed provider responses pre-populated from EHR data |
| `Claim` (PA) | Da Vinci PAS | Prior authorization request submitted to health plan after DTR documentation package is complete |
| `ClaimResponse` | Da Vinci PAS | Health plan PA approval response — includes PA number and approved service details |
| `ExplanationOfBenefit` | CARIN Blue Button | Two distinct uses, not to be conflated: (1) `use: preauthorization` — John's app displays the PA decision (PDex PPA profile); (2) **new**, `use: claim` — a non-financial, oral-optimized profile (`ODEOralProfessionalEOB`, derived from C4BB Professional/NonClinician Basis) representing the interoperable claims-ready bundle for Dr. Bellweather's dental procedures billed to IBX's medical benefit. See the new subsection below this table for detail. |
| `Subscription` / `SubscriptionStatus` | FHIR Subscriptions Backport IG | Event notifications pushed to John's patient app at each key workflow milestone — referral sent, appointment scheduled, DDC received, clearance transmitted, PA approved |
| `Bundle` | FHIR Core | Transaction and document bundles wrapping multi-resource exchanges — referral packet, DDC report, PA submission, and dental clearance return |
| `AuditEvent` | US Core | Logging of cross-organizational data access events for compliance and provenance tracking |
| `Provenance` | US Core | Records the chain of custody for clinical data — who created, transmitted, and received each resource throughout the workflow |

---

### The Oral-Optimized Claims-Sharing Profile (`ODEOralProfessionalEOB`)

This use case surfaces a real gap in existing FHIR IGs: **there is no single ExplanationOfBenefit profile that is simultaneously CMS-1500-compatible and dentally-aware.** CARIN Blue Button defines five EOB profile families — Inpatient, Outpatient, Pharmacy, Oral, and Professional/NonClinician — but each is scoped to one claim type. Professional/NonClinician is the profile structurally proven to map to CMS-1500 (its `careTeam.role: referring` element confirms directly to CMS-1500 Box 17; `diagnosis[]` to Box 21; `supportingInfo[servicefacility]` to Box 32); but it has no concept of a tooth. Oral has the tooth (`item.bodySite`, dual CDT/CPT-capable coding); but it maps to the ADA Dental Claim Form, not CMS-1500.

`ODEOralProfessionalEOB` is derived from CARIN BB's **Professional/NonClinician Basis** profile (the non-financial variant, intended by CARIN BB itself for exactly this kind of external-IG reuse), extended with the oral must-support elements borrowed from Oral's own pattern:

- `item.bodySite` required, using the **ADA Universal Tooth Designation System** only (confirmed directly with the ADA that FDI/ISO 3950 notation is not used for US dental data — this resolves a previously-open item in the ODE interface's own deferred-gaps list)
- `item.productOrService` must carry **CDT always** (a HIPAA requirement for any dental claim, regardless of which payer receives it) **and CPT/HCPCS wherever a crosswalk is knowable**, so the same package works whether the receiving payer is medical or dental

**Deliberately non-financial in this iteration**: `status: draft`, `outcome: queued`, no `unitPrice`/`net`/`total`/`adjudication`. This is not an oversight — the profile is structured so pricing and adjudication can be layered onto the identical shape in a future Connectathon without redesigning anything, matching CARIN BB's own convention for its "Basis" profiles.

**Dual-purpose by design, not by accident:** this use case (UC01) exercises the profile in its medical-payer direction — Dr. Bellweather's dental procedures, billed to IBX's medical benefit under the CMS "inextricably linked" exception, with the CPT crosswalk populated. UC02 (dental-to-dental) is expected to exercise the same profile's dental-payer direction — CDT-only, no crosswalk needed, submitted to an actual dental plan. One profile, both directions, proving the shape generalizes rather than being use-case-specific.

**Explicit scope boundary:** this profile defines the interoperable *package*, not a claim submission. Converting the package into any specific payer's required format — CDT-with-modifier, CPT-crosswalked, CMS-1500 fields, an 837D or 837P — is downstream work performed by the receiving PMS or a clearinghouse, not something this use case's resources produce or perform. The goal is industry consensus on one interoperable shape upstream of that conversion, not a solved claim for this one patient.

---

### Cross-Cutting Test Objectives

1. **Patient matching across unaffiliated systems** — FCCC EHR, Eaglesoft via interim FHIR server, and the health plan must resolve John's identity without a shared master patient index.

2. **Coverage and plan data at point of order** — `Coverage` and `InsurancePlan` resources must be available in the EHR at the moment the IMRT order is placed for CRD to evaluate requirements correctly.

3. **Provider and organization context for CRD** — `Practitioner`, `PractitionerRole`, `Organization`, and `Location` must all be correctly populated for the CRD server to apply the right coverage rules for place of service and ordering provider type.

4. **Interim FHIR server as a dental interoperability bridge** — Eaglesoft's lack of native FHIR capability is addressed through an interim server; this use case tests whether that architecture can support both inbound referral receipt and outbound structured clinical data return.

5. **Structured data as the clearance** — No PDF or paper form is used; the dental clearance is composed entirely of discrete FHIR resources, testing whether a payer can accept and adjudicate a PA based on structured clinical data alone.

6. **DDC as a novel FHIR observation type** — Site-specific radiation dose data transmitted from a radiation planning system to a dental EHR has no established LOINC code; this use case surfaces that gap for the ODE IG development process.

7. **ODE IG validation** — This use case is a primary test vehicle for the Oral Health Data Exchange IG, published through HL7 and sponsored by the PIE Work Group (PSS-2714), exercising its profiles for oral health findings, procedures, and clearance attestation in a live connectathon environment.

8. **Task lifecycle for documentation requirements** — The `Task` resource tracking the open dental clearance requirement must correctly open at DTR launch and close upon receipt of the structured clearance, triggering PAS submission.

9. **Patient app as a real-time participant** — John's app receives data from three independent sources and surfaces a coherent care timeline, testing PDex, CARIN BB, US Core, SMART on FHIR, and FHIR Subscriptions in a single patient-facing scenario.

---

## Section IV: EDI Transactions

Because John's IBX plan is a **Medicare Advantage medical benefit**, all services in this use case — including Dr. Bellweather's dental examination, radiographs, extractions, and implant placement — are billed as **medically necessary** under the medical benefit. No dental benefit claim (837D) is in scope. Dr. Bellweather bills as a specialty provider on a professional medical claim.

This use case is built on a FHIR-native prior authorization workflow using **Da Vinci PAS**, which replaces the legacy X12 278 transaction with FHIR `Claim` and `ClaimResponse` resources. The X12 278 is therefore not in scope.

### EDI Transactions in Scope

| X12 Transaction | Trigger | Scope Note |
|---|---|---|
| **270 / 271** — Eligibility & Benefit Inquiry / Response | Dr. Whitfield's office checks John's IBX medical benefit at IMRT order entry | Queries medical benefit; service type codes for radiation oncology and medically necessary oral surgery |
| **837P** — Professional Medical Claim (FCCC) | FCCC bills for IMRT planning and delivery | CPT codes 77385/77386 (IMRT delivery) + 77387 (IGRT); Place of Service 22 (outpatient hospital) |
| **837P** — Professional Medical Claim (Penn Dental) | Dr. Bellweather bills for exam, radiographs, extractions, and implant as medically necessary | CDT codes billed on medical claim; see crosswalk note below |
| **835** — Remittance Advice | IBX adjudicates and pays both claims | Claim adjustment reason codes; patient responsibility |
| **FHIR-native clearance transmission (CDex)** | Dental clearance documentation transmitted from Dr. Bellweather to FCCC and to IBX in support of the PA submission | No 275 claim attachment transaction; clearance is transmitted as FHIR resources — `ClinicalImpression`, `DocumentReference`, or a purpose-built ODE resource — via CDex provider-to-provider data push (Penn Dental → FCCC) and CDex `$submit-attachment` operation (FCCC → IBX). Resource type and `Claim.supportingInfo` reference structure are open design questions for the ODE IG. |

> **Note on 278:** Da Vinci PAS uses FHIR `Claim` and `ClaimResponse` resources for prior authorization. The X12 278 request and response are **not** exercised in this use case.

---

### CDT-to-CPT Crosswalk for Medical Billing

When Dr. Bellweather bills Penn Dental's procedures on an 837P medical claim, the claim may require CPT codes in place of — or alongside — CDT codes. The mapping below reflects the best available cross-coding guidance; confidence levels are noted explicitly.

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
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport`, `ImagingStudy` | D0220 periapical radiograph — Dr. Bellweather's exam |
| `24828-6` | XR tomography Mandible Panoramic | `DiagnosticReport`, `ImagingStudy` | D0330 panoramic radiograph — Dr. Bellweather's exam |
| `46386-9` | XR Teeth Bitewing Views | `DiagnosticReport` | Supplemental radiographic reference if bitewings taken |
| *(No LOINC code established)* | Site-specific radiation dose (Gy) at tooth site | `Observation` | 52 Gy DDC data from Dr. Priya Nandakumar — **gap surfaced by this use case; a named ODE IG test objective** |

> **LOINC gap:** The site-specific dosimetric dental contouring (DDC) observation — radiation dose in Gray at a specific tooth site — has no established LOINC code. This use case is designed to surface that gap as an action item for the ODE IG development process and the PIE Work Group.

---

## Appendix: Data

### 0. Encounter Enumeration

The narrative timeline (Section 7) implies the following distinct patient-facing encounters. This use case document does not otherwise enumerate `Encounter` resources explicitly, so this list is derived from the timeline and should be treated as the authoritative encounter count for base-resource and workflow-resource construction.

| # | Date | Encounter | Location | Class |
|---|---|---|---|---|
| 1 | 2026-07-06 | Oncology visit — IMRT order placed | FCCC | Ambulatory |
| 2 | 2026-07-23 | Dental exam & radiographs | Penn Dental | Ambulatory |
| 3 | 2026-07-27 | Extraction #4 | Penn Dental | Ambulatory |
| 4 | 2026-07-28 | Extraction #17 | Penn Dental | Ambulatory |
| 5 | 2026-07-29 | Extraction #30 + implant placement | Penn Dental | Ambulatory |
| 6 | 2026-07-31 | Dental clearance visit/exam | Penn Dental | Ambulatory |
| 7 | 2026-08-24 | Revised IMRT start (radiation begins) | FCCC | Ambulatory |

**Total: 7 encounters** (2 oncology, 5 dental). This is the fixed, authoritative count for this use case — treat as decided, not as a range.

**Resolution of two borderline timeline entries, decided for testability:**

- **2026-07-25 ("Treatment Plan Finalized")** is **not** a separate encounter. This is chart/data review — Dr. Bellweather finalizing the treatment plan from the DDC data received from FCCC — with no patient visit required.
- **2026-07-31 ("Dental Clearance Documented")** **is** its own encounter, distinct from the 2026-07-29 extraction/implant visit. Clinically, clearance for high-dose radiation requires a physical post-operative exam confirming healing is on track before clearance is granted — this cannot be paperwork alone from the prior visit.

Any `Encounter` resources built for this use case must match this 7-encounter enumeration exactly.

### 1. Patient Resource Data

#### Demographics & Identifiers

| FHIR Element | Value | System/Note |
|---|---|---|
| **Name** | John Smith | Given: John; Family: Smith |
| **Date of Birth** | 1962-11-14 | Age: 63 |
| **Sex** | Male | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **Medical Record Number (MRN)** | `JS-2026-4582` | System: `http://foxchasecancercenter.org/fhir/mrn` (FCCC MRN) |
| **Medicare Beneficiary Identifier (MBI)** | `H1234567800` | System: `http://cms.gov/beneficiary` |
| **Telecom (Phone)** | (215) 555-0147 | Use: Mobile |
| **Telecom (Email)** | john.smith.1962@email.com | Use: Home |
| **Address** | 1847 Spruce Street, Apt 3B, Philadelphia, PA 19103 | City: Philadelphia; State: PA; ZIP: 19103 |
| **Marital Status** | Married | `http://hl7.org/fhir/ValueSet/marital-status` |
| **Language** | English | Preferred language |
| **Race** | Asked, Declined to Answer | US Core Race extension; `data-absent-reason` = `asked-declined` (patient declined to disclose) |
| **Ethnicity** | Asked, Declined to Answer | US Core Ethnicity extension; `data-absent-reason` = `asked-declined` (patient declined to disclose) |
| **Active** | True | Patient record is active |

---

### 2. Coverage Resource Data

#### Plan Information & Identifiers

| FHIR Element | Value | System/Note |
|---|---|---|
| **Payer** | Independence Blue Cross | Organization reference |
| **Plan Name** | Personal Choice 65 PPO | Commercial product name |
| **Plan Type** | PPO | Preferred Provider Organization |
| **CMS Plan ID** | H3909 | System: `http://cms.gov/cmsid` |
| **Member ID** | H1234567800 | Primary member identifier |
| **Policy Number** | 3909-101167 | System: `http://ibx.com/policyid` |
| **Group Number** | 847560 | System: `http://ibx.com/groupid` |
| **Subscriber** | John Smith | Self (same as member) |
| **Relationship** | Self | Member is subscriber |
| **Coverage Period Start** | 2026-01-01 | Plan year begins |
| **Coverage Period End** | 2026-12-31 | Plan year ends |
| **Status** | Active | Coverage is in effect |
| **Network Affiliation** | Preferred Provider Network | In-network status |

#### Cost-Sharing Details

| Category | Amount | Notes |
|---|---|---|
| **Medical Deductible** | $250 | Individual; waived for preventive/diagnostic |
| **Specialist Copay** | $50/visit | In-network |
| **Imaging Copay** | $0 | Preventive/diagnostic waived |
| **Surgical Coinsurance** | 20% | After deductible |
| **Out-of-Pocket Maximum** | $6,700 | Individual; federally capped for MA |

#### Prior Authorization & Coverage Rules

| Service | PA Required | Coverage | Notes |
|---|---|---|---|
| IMRT | **Yes** | Covered | Mandatory PA before service delivery |
| Extraction (D7210) | No | Covered | Medically necessary, at medical rate |
| Implant (D6010) | No | Covered | Medically necessary, at medical rate |
| Diagnostic Imaging | No | Covered | $0 copay for preventive/diagnostic |

#### Payer Identifiers

| Identifier | Value | System | Purpose |
|---|---|---|---|
| **Tax ID (EIN)** | 23-0370270 | IRS | Organization tax ID |
| **CMS Medicare Contract** | H3909 | CMS HPMS | MA plan contract ID |
| **Payer ID (EDI)** | 54704 | HIPAA X12 | Claims routing for 837P/837I |
| **Claims Address** | P.O. Box 211184, Eagan, MN 55121 | Postal | Electronic & paper claims |

---

### 3. Organization Resource Data

#### Fox Chase Cancer Center (FCCC)

| FHIR Element | Value | System/Note |
|---|---|---|
| **Organization NPI** | 1437423514 | System: `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | Fox Chase Cancer Center Medical Group, Inc | Legal name |
| **Alias** | Fox Chase Cancer Center; FCCC | Common usage |
| **Address** | 333 Cottman Avenue, Philadelphia, PA 19111 | Main campus |
| **Phone** | (215) 728-6900 | Main line |
| **Fax** | (215) 728-1185 | Claims fax |
| **Type** | Hospital | Organization type: Hospital/Comprehensive Cancer Center |
| **Specialty** | Oncology | NCI-designated Comprehensive Cancer Center |
| **EHR System** | Oracle Health (Cerner EHR) | Epic alternative, cerner.com |
| **FHIR Endpoint** | https://fhir.foxchasecancercenter.org/r4 | Hypothetical FHIR server |
| **Tax ID (EIN)** | 23-1234567 | Example format |
| **State License** | PA-001 | Pennsylvania hospital license |
| **NPI Taxonomy Code** | 284300000X | Oncology specialty |

#### Penn Dental Family Practice (University of Pennsylvania School of Dental Medicine)

| FHIR Element | Value | System/Note |
|---|---|---|
| **Organization NPI** | 1205234382 | System: `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | Penn Dental Medicine | Official name |
| **Alias** | Penn Dental Family Practice; PDFP; Penn Dental | Usage variants |
| **Parent Organization** | University of Pennsylvania Health System | Academic affiliation |
| **Address** | 240 South 40th Street, Philadelphia, PA 19104 | Robert Schattner Center |
| **Phone** | (215) 898-4615 | Main clinic |
| **Phone (Appointments)** | (215) 898-8965 | Scheduling line |
| **Type** | Dentist / Dental Practice | Organization type |
| **Specialty** | General Dentistry, Oral Oncology | Primary & specialty services |
| **EHR System** | Eaglesoft (Patterson Dental EHR) | Plus interim FHIR server for Connectathon |
| **FHIR Endpoint** | https://fhir-interim.dental.upenn.edu/r4 | Test/interim FHIR server |
| **State License** | PA-DS038838 | Pennsylvania dental license |
| **NPI Taxonomy Code** | 1223G0001X | General dentist |
| **Clinical Hours** | M,W: 8am-8pm; T,Th,F: 8am-5pm | See website for holiday closures |

#### Independence Blue Cross (IBX)

| FHIR Element | Value | System/Note |
|---|---|---|
| **Organization NPI** | Not applicable | Payers do not have NPIs |
| **Organization Name** | Independence Blue Cross, Inc | Legal entity |
| **Alias** | IBX; Independence | Common usage |
| **Address** | 1901 Market Street, Philadelphia, PA 19103 | Corporate headquarters |
| **Phone** | 1-888-718-3333 | Medicare Advantage member services |
| **Type** | Insurance Company / Health Plan | Organization type |
| **Specialty** | Medicare Advantage, Commercial, Medicaid | Product lines |
| **Tax ID (EIN)** | 23-0370270 | IRS identifier |
| **CMS Medicare Contract ID** | H3909 | For Personal Choice 65 PPO |
| **Payer ID (EDI)** | 54704 | Claims routing |
| **Claims Mailing Address** | P.O. Box 211184, Eagan, MN 55121 | Electronic & paper submission |
| **Electronic Claims (EDI)** | Smart Data Solutions gateway | HIPAA-compliant EDI processor |
| **FHIR Endpoint** | https://api.ibx.com/fhir/r4 | Hypothetical payer API |

---

### 4. Practitioner Resource Data

#### Dr. Marcus Whitfield — Radiation Oncology

| FHIR Element | Value | System/Note |
|---|---|---|
| **NPI** | 1000000021 | System: `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Thomas Mark Whitfield, MD | Given: Thomas; Middle: Mark; Family: Whitfield |
| **Title** | Service Chief, Head & Neck Radiation Oncology | Official title |
| **Gender** | Male | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **Qualification License** | MD (Medical Doctor) | License type |
| **License Number** | PA-MD-000101 | Pennsylvania medical license |
| **Specialty Code (Taxonomy)** | 2070AM0800X | Radiation Oncology; Primary taxonomy |
| **Organization** | Fox Chase Cancer Center | Employment at FCCC |
| **Telecom (Phone)** | (215) 728-6900 ext 2847 | FCCC main line + extension |
| **Telecom (Email)** | marcus.whitfield@example-cancercenter.org | Professional email |
| **Address** | 333 Cottman Avenue, Philadelphia, PA 19111 | FCCC address |
| **Board Certification** | American Board of Radiology (ABR) | Radiation Oncology certification |

#### Dr. Renata Osei — Surgical Oncology

| FHIR Element | Value | System/Note |
|---|---|---|
| **NPI** | 1000000034 | System: `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Cecelia Marie Osei, MD, FACS | Given: Cecelia; Middle: Marie; Suffix: FACS |
| **Title** | Chair, Department of Surgical Oncology | Official title |
| **Gender** | Female | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **Qualification License** | MD (Medical Doctor) | License type |
| **License Number** | PA-MD-000114 | Pennsylvania medical license |
| **Specialty Code (Taxonomy)** | 2092S0080X | Head and Neck Surgery; Primary taxonomy |
| **Sub-specialty** | Surgical Oncology | Secondary focus |
| **Organization** | Fox Chase Cancer Center | Employment at FCCC |
| **Telecom (Phone)** | (215) 728-6900 ext 2951 | FCCC main + extension |
| **Telecom (Email)** | renata.osei@example-cancercenter.org | Professional email |
| **Address** | 333 Cottman Avenue, Philadelphia, PA 19111 | FCCC address |
| **Board Certification** | American Board of Surgery (ABS) | General Surgery & Surgical Oncology |
| **Fellow Status** | FACS (Fellow, American College of Surgeons) | Senior credential |

#### Dr. Andrew Bellweather — Oral Oncology / Dental Clearance

| FHIR Element | Value | System/Note |
|---|---|---|
| **NPI** | 1000000047 | System: `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Thomas Paul Bellweather, DMD, MMSc | Given: Thomas; Middle: Paul; Suffix: MMSc |
| **Title** | Professor and Chair, Department of Oral Medicine; Oral Oncology Specialist | Academic & clinical title — confirmed current per Penn Dental Medicine |
| **Gender** | Male | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **Qualification License** | DMD (Doctor of Medical Dentistry) | Dental degree |
| **License Number** | PA-DDS-000123 | Pennsylvania dental license |
| **Specialty Code (Taxonomy)** | 125Q00000X | Oral Medicine; Primary taxonomy (NUCC) |
| **Sub-specialty** | Oral Oncology; Oral Medicine | Clinical focus |
| **Organization** | Penn Dental Family Practice (PDFP) / University of Pennsylvania | Affiliation |
| **Telecom (Phone)** | (215) 898-4615 | Penn Dental main line |
| **Telecom (Email)** | andrew.bellweather@example-dental.edu | University email |
| **Address** | 240 South 40th Street, Philadelphia, PA 19104 | Robert Schattner Center, Penn Dental |
| **Board Certification** | American Board of Oral Medicine (Diplomate, 1993); American Board of Special Care Dentistry (Diplomate, 2005) | Specialty certification — confirmed per Penn faculty record |
| **Academic Appointment** | University of Pennsylvania School of Dental Medicine | Faculty rank: Professor and Chair, Department of Oral Medicine |

#### Dr. Priya Nandakumar — Medical Physicist

| FHIR Element | Value | System/Note |
|---|---|---|
| **NPI** | 1000000050 | System: `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Priya Nandakumar, MS, FACMP | Given: Teh; Family: Nandakumar |
| **Title** | Medical Physicist, Head & Neck Radiation Oncology | Professional title |
| **Gender** | Not specified | — |
| **Qualification** | MS (Master of Science) | Physics degree |
| **Specialty Code (Taxonomy)** | 1649P1900X | Medical Physicist; Radiation Physics |
| **Certification** | FACMP (Fellow, American College of Medical Physics) | Professional credential |
| **Organization** | Fox Chase Cancer Center | Employment at FCCC |
| **Telecom (Phone)** | (215) 728-6900 ext 2865 | FCCC physics department |
| **Telecom (Email)** | priya.nandakumar@example-cancercenter.org | Professional email |
| **Address** | 333 Cottman Avenue, Philadelphia, PA 19111 | FCCC address |
| **Role in Use Case** | Dosimetric Dental Contouring (DDC) data provider | Extracts site-specific radiation dose |

---

### 5. Workflow & Service Data

#### ServiceRequest (Referral from FCCC to Penn Dental)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Active | Ongoing referral |
| **Intent** | Order | Clinical order |
| **Category** | Consultation | Type of service request |
| **Priority** | Urgent | High priority due to timeline |
| **Code** | Dental consultation for pre-radiation clearance | Referral reason |
| **Subject** | John Smith | Patient reference |
| **Requester** | Dr. Marcus Whitfield (FCCC) | Ordering provider |
| **Performer** | Dr. Andrew Bellweather (Penn Dental) | Receiving provider |
| **Reason Code** | Pre-operative dental clearance | Clinical justification |
| **Reason Reference** | Condition: Stage IV SCC C02.1 | Linked diagnosis |
| **Ordered Date** | 2026-07-06 | Order placement date |
| **Occurrence DateTime** | 2026-07-23 | Appointment/exam date |
| **Description** | Comprehensive dental evaluation, imaging, and clearance assessment prior to head & neck IMRT. Provide site-specific dosimetric dental contouring (DDC) data for tooth #30 to determine extraction vs. preservation strategy. |  Detailed instructions |

#### Dosimetric Dental Contouring (DDC) Information Request — modeled as a note, not a formal order

**Correction:** this was originally modeled as a `ServiceRequest`. That's clinically wrong — Dr. Bellweather isn't ordering FCCC to *perform* a service; he's asking a colleague to share information (dose data) that already exists as a byproduct of the IMRT plan Dr. Whitfield ordered in Encounter #1. This is an informal inter-provider information request between two practitioners already in an established clinical relationship (via the open referral from Encounter #1) — it does not warrant a formal order resource, a new 360X transaction, or a directional ODE referral profile. It's captured as a **note/annotation** on the relevant Encounter #2 resources, not as a standalone `ServiceRequest` or `CommunicationRequest`.

| Element | Value | Notes |
|---|---|---|
| **Nature** | Informal information request (note), not a formal order | Requester and performer already in an established referral relationship |
| **From** | Dr. Andrew Bellweather (Penn Dental) | Requesting clinician |
| **To** | Dr. Priya Nandakumar (FCCC Medical Physics) | Has access to the IMRT dose planning data |
| **Requested** | 2026-07-23 | During the dental exam encounter |
| **Fulfilled** | 2026-07-25 | Data transmission date — not its own encounter (see Appendix Section 0) |
| **Body Site** | Tooth #30 (FDI notation) | Specific tooth location |
| **Content** | Site-specific radiation dose (Gray) at tooth #30, extracted from the IMRT treatment plan, to inform dental extraction vs. preservation decision. Safe threshold: < 45 Gy; Plan dose: 52 Gy. | The resulting dose value is still captured formally as an `Observation` — only the *request/response mechanism* is downgraded to a note, not the resulting clinical data itself. |

#### Procedure (Tooth Extractions & Implant Placement)

##### Extraction #1: Tooth #4

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Category** | Dental | Procedure type |
| **Code** | D7210 (CDT) / 41899 (CPT) | Extraction with bone removal |
| **Subject** | John Smith | Patient reference |
| **Performer** | Dr. Andrew Bellweather (DMD) | Performing dentist |
| **Performed DateTime** | 2026-07-27 | Date of procedure |
| **Body Site** | Tooth #4 (FDI: 14) | Upper right first premolar |
| **Reason** | Pre-radiation dental clearance; tooth with compromised prognosis | Clinical indication |

##### Extraction #2: Tooth #17

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Category** | Dental | Procedure type |
| **Code** | D7210 (CDT) / 41899 (CPT) | Extraction; impacted tooth |
| **Subject** | John Smith | Patient reference |
| **Performer** | Dr. Andrew Bellweather (DMD) | Performing dentist |
| **Performed DateTime** | 2026-07-28 | Date of procedure |
| **Body Site** | Tooth #17 (FDI: 28) | Lower left third molar |
| **Reason** | Pre-radiation dental clearance; impacted wisdom tooth | Clinical indication |

##### Extraction #3: Tooth #30

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Category** | Dental | Procedure type |
| **Code** | D7210 (CDT) / 41899 (CPT) | Extraction; requires bone removal |
| **Subject** | John Smith | Patient reference |
| **Performer** | Dr. Andrew Bellweather (DMD) | Performing dentist |
| **Performed DateTime** | 2026-07-29 | Date of procedure |
| **Body Site** | Tooth #30 (FDI: 46) | Lower right first molar |
| **Outcome Code** | *Unverified — see Section 6 caution* | Tooth extraction (text-only in built resources) |
| **Reason** | Excessive radiation dose (52 Gy exceeds 45 Gy threshold); high osteoradionecrosis risk. Scheduled immediate implant placement. | Clinical indication |

##### Implant Placement: Tooth #30

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Category** | Dental Surgery | Procedure type |
| **Code** | D6010 (CDT) / 21248 (CPT) | Surgical placement of implant body |
| **Subject** | John Smith | Patient reference |
| **Performer** | Dr. Andrew Bellweather (DMD) | Performing dentist |
| **Performed DateTime** | 2026-07-29 | Same-day as extraction |
| **Body Site** | Tooth #30 site (FDI: 46) | Lower right first molar region |
| **Reason** | Immediate implant placement following extraction; maintains vertical bone support; improves post-radiation oral function. | Clinical indication |
| **Outcome Code** | *Unverified — see Section 6 caution* | Implant placement successful (text-only in built resources) |

#### Observation (Dosimetric Dental Contouring Data)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Final | Observation complete |
| **Category** | Diagnostic result; Planning data | Type |
| **Code** | **LOINC gap:** No established code | Site-specific radiation dose at tooth site |
| **Subject** | John Smith | Patient reference |
| **Performer** | Dr. Priya Nandakumar (Medical Physicist, FCCC) | Data source |
| **Effective DateTime** | 2026-07-25 | Date of dosimetric extraction |
| **Value (Quantity)** | 52 Gy | Radiation dose magnitude |
| **Unit** | Gray (Gy) | International System of Units |
| **Reference Range Low** | 0 Gy | Lower bound |
| **Reference Range High** | 45 Gy | Clinically safe threshold for tooth preservation |
| **Interpretation** | Exceeds safe threshold (critical high) | Clinical significance |
| **Body Site** | Tooth #30 (FDI: 46) | Specific tooth location |
| **Related Observations** | Treatment plan (IMRT course) | DICOM dose reference |
| **Comment** | Extracted due to dose threshold exceedance. Immediate implant placed same day. | Clinical summary |

#### DiagnosticReport (Imaging Studies)

##### Periapical Radiograph (D0220)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Final | Report complete |
| **Category** | Imaging | Report type |
| **Code** | D0220 (CDT) / LOINC 62443-7 | Periapical radiographic image |
| **Subject** | John Smith | Patient reference |
| **Performer** | Dr. Andrew Bellweather (Dentist) | Ordering & interpreting provider |
| **Effective DateTime** | 2026-07-23 | Date of imaging |
| **Issued** | 2026-07-23 | Report issue date |
| **Conclusion** | Three teeth identified with pre-radiation compromise: #4 (standard extraction), #17 (impacted), #30 (high-dose site requiring DDC consultation). | Radiographic findings |

##### Panoramic Radiograph (D0330)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Final | Report complete |
| **Category** | Imaging | Report type |
| **Code** | D0330 (CDT) / LOINC 24828-6 | Panoramic radiograph (orthopantomogram) |
| **Subject** | John Smith | Patient reference |
| **Performer** | Dr. Andrew Bellweather (Dentist) | Ordering & interpreting provider |
| **Effective DateTime** | 2026-07-23 | Date of imaging |
| **Issued** | 2026-07-23 | Report issue date |
| **Conclusion** | Full-mouth assessment confirms three teeth requiring extraction; no other significant findings. Mandible and maxilla without fracture or advanced pathology. | Full-mouth overview |

#### ClinicalImpression (Dental Clearance)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Assessment complete |
| **Assessment Code** | *Unverified — see Section 6 caution* | Dental clearance (general) (text-only in built resources) |
| **Subject** | John Smith | Patient reference |
| **Date** | 2026-07-31 | Clearance date |
| **Assessor** | Dr. Andrew Bellweather (DMD, Oral Oncology) | Assessing provider |
| **Summary** | **DENTAL CLEARANCE APPROVED for head & neck IMRT.** Patient evaluated and treated for pre-radiation dental risk. Three teeth (#4, #17, #30) extracted. Tooth #30: immediate implant placed due to DDC-identified high-dose site (52 Gy > 45 Gy threshold). Remaining dentition assessed as suitable for radiation support therapy. Patient counseled on osteoradionecrosis risk, hygiene protocols, and follow-up imaging. No contraindications to IMRT initiation. | Clinical assessment summary |
| **Finding** | Diagnosis: Pre-radiation dental risk assessment—MANAGED | Primary finding |
| **Problem List** | – Teeth #4, #17, #30 extraction completed; – Implant #30 immediately placed; – Remaining dentition suitable for radiation; – Osteoradionecrosis prevention protocol initiated | Problem list |
| **Recommendations** | 1. Clearance transmitted to FCCC Radiation Oncology; 2. Recommend 14-day healing window for extractions; 3. Dental follow-up imaging at 6, 12, 24 months post-IMRT | Recommendations |

---

### 6. Clinical Codes & Mappings

#### ICD-10 Diagnosis Codes

| Code | Description | Application |
|---|---|---|
| C02.1 | Lateral border of tongue, malignant neoplasm | Primary diagnosis: Stage IV SCC |
| K08.13 | Complete loss of teeth due to trauma | Post-extraction status (code for procedures if needed) |

#### SNOMED CT Clinical Codes

**⚠️ CAUTION — this table has not been verified and should not be trusted as-is.** During Interaction 3's build, `146328D` was found to be an invalid SNOMED CT identifier (SNOMED identifiers are purely numeric; this one has a trailing letter). Attempts to verify the other four codes below via general web search were inconclusive-to-contradictory: `394839003` and `234223000` returned no confirmation, and a different code (`55162003`) surfaced instead for "tooth extraction." General web search is a poor tool for verifying SNOMED concepts specifically (SNOMED's browser content isn't well-indexed by search engines), so this may reflect a tooling limitation rather than confirmation that all five codes are wrong — but none should be used in production or test resources until checked against an actual SNOMED terminology browser (e.g. `browser.ihtsdotools.org`).

**Resolution used in this project's built FHIR resources:** all of the codes below are represented as **text-only** (`code.text`, no `coding`) in Interaction 3's `Procedure`, `Observation`, and `ClinicalImpression` resources, pending a proper terminology browser lookup by someone with SNOMED access.

| SNOMED Code (as originally written — UNVERIFIED) | Description | Application |
|---|---|---|
| ~~146328D~~ | Dental clearance | **Confirmed invalid** (not a real SNOMED format) |
| ~~234223000~~ | Implant placement successful | Unconfirmed |
| ~~394839003~~ | Tooth extraction (procedure) | Unconfirmed — `55162003` surfaced instead in search |
| ~~276339004~~ | Osteoradionecrosis | Unconfirmed — `109716001` ("Osteoradionecrosis of the mandible") surfaced instead, not yet confirmed as the right match |
| ~~52474006~~ | Intensity-modulated radiation therapy (IMRT) | Not checked yet |

#### CDT (Current Dental Terminology) Codes

| Code | Description | Unit Type |
|---|---|---|
| D0220 | Periapical radiographic image | Diagnostic |
| D0330 | Panoramic radiographic image | Diagnostic |
| D7210 | Extraction of erupted tooth; elevation and/or forceps removal | Surgical |
| D6010 | Surgical placement of implant body: endosteal implant | Surgical/Prosthodontic |

#### CPT (Current Procedural Terminology) Cross-Map

| CDT | CPT | Descriptor | Confidence |
|---|---|---|---|
| D0220 | 70300 | Intraoral - periapical first radiographic image | High |
| D0330 | (No direct CPT) | Panoramic radiograph (facility code 70210 if billed as hospital service) | Medium |
| D7210 | 41899 | Unlisted orthodontic procedure, by report | High (requires narrative) |
| D6010 | 21248 | Reconstruction of mandible or maxilla, endosteal implant; with soft tissue graft procedure | High |

#### LOINC Codes

| LOINC | Description | FHIR Resource | Status |
|---|---|---|---|
| 62443-7 | Single view Teeth Document XR | DiagnosticReport | Standard |
| 24828-6 | XR tomography Mandible Panoramic | DiagnosticReport | Standard |
| 46386-9 | XR Teeth Bitewing Views | DiagnosticReport | Standard (if applicable) |
| *[NO CODE]* | Site-specific radiation dose (Gy) at tooth | Observation | **GAP: No LOINC code established; named ODE IG test objective** |

---

### 7. Timeline & Dates

#### Service Timeline (July–August 2026)

| Event | Date | Time | Actor(s) | System(s) |
|---|---|---|---|---|
| **IMRT Order & CRD Trigger** | 2026-07-06 | 09:00 | Dr. Whitfield (FCCC) | Oracle Health (Cerner); CRD hook |
| **Referral Sent to Penn Dental** | 2026-07-06 | 10:30 | FCCC EHR | Cerner → Eaglesoft (direct or HL7 v2) |
| **Referral Received & Scheduled** | 2026-07-07 | 08:00 | Penn Dental Reception | Eaglesoft |
| **Dental Exam & Radiographs** | 2026-07-23 | 14:00 | Dr. Bellweather | Eaglesoft + imaging devices |
| **DDC Request Sent to FCCC** | 2026-07-23 | 15:30 | Dr. Bellweather | Eaglesoft → FCCC (via secure message) |
| **DDC Data Extracted & Transmitted** | 2026-07-25 | 11:00 | Dr. Priya Nandakumar (FCCC Physics) | FCCC planning system → Penn Dental |
| **Treatment Plan Finalized** | 2026-07-25 | 14:00 | Dr. Bellweather | Eaglesoft |
| **Extraction #4** | 2026-07-27 | 10:00 | Dr. Bellweather | Eaglesoft |
| **Extraction #17** | 2026-07-28 | 10:30 | Dr. Bellweather | Eaglesoft |
| **Extraction #30 + Implant Placement** | 2026-07-29 | 09:00 | Dr. Bellweather | Eaglesoft |
| **Dental Clearance Documented** | 2026-07-31 | 16:00 | Dr. Bellweather | Eaglesoft |
| **Clearance Transmitted to FCCC** | 2026-07-31 | 16:30 | Penn Dental EHR | Eaglesoft → Cerner (CDex push) |
| **PA Submitted to IBX** | 2026-08-01 | 09:00 | FCCC Billing/RCM | Cerner → IBX (FHIR `Claim` via Da Vinci PAS — corrected; this row previously said "837P via clearinghouse," which is the reimbursement billing transaction type, not the prior-auth request type this use case actually exercises) |
| **14-Day Healing Window** | 2026-08-01 through 2026-08-14 | — | Patient | — |
| **PA Approved by IBX** | 2026-08-03 | 13:00 | IBX Medical Review | IBX system → FCCC (ClaimResponse) |
| **Original IMRT Start (Moved)** | 2026-08-10 | — | — | — |
| **Revised IMRT Start** | 2026-08-24 | 08:00 | Dr. Whitfield | FCCC treatment planning |

#### Key Timeline Constraints

| Constraint | Deadline | Rationale |
|---|---|---|
| **Dental Clearance Window** | 21 days from referral (by 2026-07-27) | Osteoradionecrosis risk mitigation |
| **DDC Request Response** | Within 3 days of request | Supports treatment planning |
| **Extraction Healing** | Minimum 14 days post-extraction | Bone remodeling & wound closure before high-dose radiation |
| **IMRT Delay Approval** | Same-day or next business day | Expedited due to patient tolerance & clinical need |
| **PA Processing** | 3 business days by law | CMS standard for expedited review |

---

*This dataset is a test and validation vehicle for the Oral Health Data Exchange (ODE) Implementation Guide, developed under HL7 and sponsored by the PIE Work Group (PSS-2714). It is intended for use in connectathon and interoperability testing environments only.*
