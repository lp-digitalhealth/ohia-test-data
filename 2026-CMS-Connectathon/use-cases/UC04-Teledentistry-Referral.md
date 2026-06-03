# CMS Connectathon — Dental Interoperability Test Dataset
## Use Case Set: Teledentistry Provider-to-In-Office Dental Referral with Closed-Loop Encounter Summary

---

## Table of Contents

- [About This Use Case Set](#about-this-use-case-set)
- [Use Case A: Commercial — Teledentistry Referral, Acute Dental Pain (Employer-Sponsored PPO, Texas)](#use-case-a-commercial)
- [Use Case B: Medicaid — Teledentistry Referral, Acute Dental Pain with Diabetes Comorbidity (Texas Medicaid Managed Care)](#use-case-b-medicaid)

---

## About This Use Case Set

These two use cases model a **provider-to-provider referral originating from a teledentistry encounter** — a workflow pattern that is increasingly common in dental care delivery but has no established standards-based implementation today. In both scenarios, a licensed dental provider conducts a synchronous virtual encounter (Place of Service 02), determines that in-office care is required, and transmits a structured referral with clinical context to an in-office dental provider (Place of Service 11). The in-office provider completes treatment and returns a structured encounter summary to the originating teledentistry provider. The patient receives real-time status updates throughout via a SMART-enabled patient-facing application.

The use cases are distinguished by payer context:

- **Use Case A** exercises the workflow under a **commercial employer-sponsored dental PPO**, testing standard FHIR coverage verification, referral transmission, and encounter summary return.
- **Use Case B** exercises the same workflow under **Texas Medicaid managed care**, adding a **FHIR-based provider directory query** (Plan-Net) to confirm Medicaid network participation before referral creation, and a **`Flag` resource** to communicate a diabetes comorbidity from the virtual assessment to the in-office care team.

Both scenarios are set in **Texas**, where the Medicaid managed care structure (STAR program) is well-established and representative of referral complexity in public coverage programs, and where teledentistry services are actively reimbursed under both commercial and Medicaid benefit designs.

**OHIA Strategic Priorities Exercised:** Connect (provider-to-provider data exchange); Empower (patient access to referral status and care plan); Locate (FHIR-based provider directory query to identify network-participating in-office providers — Use Case B).

> **No paper forms, portal logins, or fax transmissions are used at any point in either workflow.**

---

---

# Use Case A: Commercial

## Teledentistry Referral — Acute Dental Pain
### Employer-Sponsored Dental PPO | Texas | Place of Service 02 → 11

---

## Section I: Business Overview

**Sarah Okonkwo** is a 34-year-old woman (DOB: 03/17/1991) living in Austin, Texas. She carries employer-sponsored dental coverage through **Aetna Dental PPO** (Group: 847221; Member ID: `AET-TX-00284711`).

On a Tuesday evening, Sarah develops sharp pain when biting down on her lower left side. The pain has been building for several days and she is now unable to chew on that side. It is 7:30 PM. Her dental provider's office is closed.

Sarah opens a **SMART-enabled patient application** associated with her teledentistry benefit. The application verifies her Aetna Dental eligibility in real time via a FHIR `Coverage` query. She is connected to **Dr. Marcus Webb, DDS**, a licensed Texas dental provider practicing in a virtual care setting (Place of Service 02).

Dr. Webb conducts a structured synchronous virtual assessment. Based on Sarah's symptom history — duration, thermal sensitivity, pain on biting, and spontaneous aching — he documents clinical indicators consistent with **irreversible pulpitis of tooth #19** (`ICD-10: K04.01`) with possible periapical involvement. He records these findings as discrete FHIR resources within the teledentistry platform.

This presentation requires in-office evaluation with radiographs and likely endodontic treatment. Dr. Webb creates a **structured referral** targeting an in-office general dental practice participating in the Aetna Dental PPO network in Austin. The referral is transmitted as a FHIR `ServiceRequest` with supporting `Condition`, `Observation`, and `MedicationStatement` resources via CDex provider-to-provider push.

Sarah receives an in-application notification that her referral has been sent. The in-office practice receives the referral via an interim FHIR server and contacts Sarah within the hour to schedule a next-day appointment.

**Dr. Priya Nair, DDS**, at the in-office practice sees Sarah the following morning. She takes a periapical radiograph (`D0220`) and confirms irreversible pulpitis with early periapical pathology (`ICD-10: K04.01`, `K04.5`). She completes root canal therapy on tooth #19 (`D3330`) in a single visit.

Dr. Nair documents the encounter and transmits a **structured encounter summary** back to the originating teledentistry provider via CDex provider-to-provider push. The summary includes the confirmed diagnoses, procedures performed with CDT codes, and a post-treatment care plan. Dr. Webb reviews the closed referral. Sarah's application updates to show the referral as complete and surfaces a summary of treatment and recovery guidance.

The in-office practice submits an 837D to Aetna Dental for the in-office services. The teledentistry provider submits a separate 837D for the virtual consultation under `D9995`.

---

## Section II: Narrative-to-Standards Mapping

| What Happens (Business Language) | Implementation Guide / Standard | Key Transaction |
|---|---|---|
| **Verify Coverage:** The patient application verifies Aetna Dental eligibility and benefit status at session initiation. | US Core / Da Vinci PDex | `Coverage` resource queried against payer FHIR API; `InsurancePlan` returned with benefit details including teledentistry and endodontic coverage. |
| **Virtual Assessment:** Dr. Webb conducts a structured synchronous virtual evaluation (POS 02) and documents clinical findings as discrete FHIR resources. | US Core / ODE (Under Development) | `Encounter` (virtual, POS 02); `Condition` (K04.01); `Observation` (symptom findings, tooth-level); `MedicationStatement` (patient-reported medications). |
| **Patient Notification — Referral Sent:** Patient is notified in-application that the referral has been transmitted. | FHIR Subscriptions Backport IG | Subscription event triggered on `ServiceRequest` creation. |
| **Structured Referral Transmitted:** Dr. Webb transmits a structured referral with clinical context to the in-office dental provider. | US Core / ODE (Under Development) / CDex | `ServiceRequest` (referral, priority: urgent); `DocumentReference` wrapping structured findings bundle; transmitted via CDex provider-to-provider push to in-office practice interim FHIR server. |
| **Referral Received at In-Office Practice:** In-office practice receives referral and clinical context; schedules the patient. | US Core / ODE (Under Development) | `ServiceRequest` received and acknowledged; `Appointment` created and linked to referral; `AppointmentResponse` returned to teledentistry provider. |
| **Patient Notification — Appointment Confirmed:** Patient receives in-application confirmation of appointment time and location. | FHIR Subscriptions Backport IG | Subscription event triggered on `AppointmentResponse`. |
| **In-Office Evaluation & Imaging:** Dr. Nair takes a periapical radiograph and confirms diagnosis. | US Core / ODE (Under Development) | `DiagnosticReport` (LOINC 62443-7); `Condition` updated with confirmed diagnoses (K04.01, K04.5); `Observation` (periapical findings). |
| **Treatment Performed:** Dr. Nair completes root canal therapy on tooth #19. | US Core / ODE (Under Development) | `Procedure` (D3330, tooth #19, FDI 36); `Encounter` (in-office, POS 11). |
| **Encounter Summary Returned:** Dr. Nair transmits a structured post-treatment summary to the teledentistry provider. | Da Vinci CDex / ODE (Under Development) | `ClinicalImpression` (encounter summary); `Procedure` (completed); `CarePlan` (post-treatment instructions); CDex provider-to-provider push from in-office practice to teledentistry provider FHIR endpoint. |
| **Referral Closed:** Dr. Webb reviews the encounter summary; referral marked complete. | US Core / CDex | `ServiceRequest` status updated to `completed`; open `Task` closed. |
| **Patient Application Updated:** Patient application shows referral complete with treatment summary and recovery guidance. | FHIR Subscriptions Backport IG / US Core | Subscription event on `ServiceRequest` status change; `CarePlan` surfaced to patient application via SMART App Launch. |
| **Claims Submission:** In-office practice submits 837D to Aetna Dental; teledentistry provider submits 837D separately. | X12 837D | 837D (in-office): D0220, D3330, tooth #19, POS 11; 837D (teledentistry): D9995, POS 02. |

---

## Section III: Technical Overview

This use case exercises a **virtual-to-in-office provider referral** spanning a teledentistry provider system, an in-office dental practice management system, and a commercial dental payer. The scenario tests the full lifecycle of a structured dental referral — from real-time coverage verification at point of virtual encounter through closed-loop encounter summary return — without paper, fax, or portal login at any step.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

### Implementation Guides

| Implementation Guide | Purpose in This Use Case |
|---|---|
| **US Core IG** | Defines FHIR profiles for patient, condition, encounter, procedure, referral, medication, and all clinical data exchanged between the teledentistry provider and the in-office dental practice |
| **Da Vinci Coverage Requirements Discovery (CRD)** | Optional hook at virtual encounter initiation; confirms teledentistry benefit coverage and surfaces any documentation requirements for the commercial dental plan |
| **Da Vinci Clinical Data Exchange (CDex)** | Two roles: (1) **Provider-to-provider referral push** — structured referral and clinical context transmitted from teledentistry provider to in-office practice interim FHIR server; (2) **Provider-to-provider encounter summary return** — structured post-treatment summary pushed from in-office practice back to teledentistry provider |
| **Da Vinci Payer Data Exchange (PDex)** | Enables the patient application to surface coverage and claims data from the commercial payer; PDex patient access API retrieves `Coverage` and benefit information at session initiation |
| **SMART App Launch IG** | Authorization framework enabling the patient application to connect to the payer FHIR endpoint for coverage verification and to surface post-treatment `CarePlan` data |
| **FHIR Subscriptions Backport IG** | Delivers real-time push notifications to the patient application at key milestones: referral sent, appointment confirmed, referral complete |
| **Oral Health Data Exchange IG (ODE)** | Under development; governs structured exchange of oral health clinical data — virtual assessment findings, tooth-level observations, CDT-coded procedures, and encounter summary — between the teledentistry provider and the in-office dental practice |

---

### Key FHIR Resources Exercised

| FHIR Resource | Source IG / Profile | Purpose in This Use Case |
|---|---|---|
| `Patient` | US Core | Patient identity across teledentistry provider system, in-office practice interim FHIR server, and commercial payer |
| `Coverage` | US Core / PDex | Commercial dental PPO coverage — member ID, group, plan type, benefit details — verified at session initiation and referenced throughout |
| `InsurancePlan` | Da Vinci PDex | Commercial plan benefit structure; teledentistry and endodontic coverage confirmation |
| `Practitioner` | US Core | Teledentistry provider (POS 02); in-office dental provider (POS 11) |
| `PractitionerRole` | US Core | Role context for teledentistry provider (virtual setting, POS 02) and in-office provider (general dentistry, POS 11) |
| `Organization` | US Core | Teledentistry provider organization; in-office dental practice; commercial payer |
| `Location` | US Core | Teledentistry virtual location (POS 02); in-office dental practice physical location (POS 11, Austin, TX) |
| `Encounter` | US Core | Virtual encounter (teledentistry provider, POS 02); in-office encounter (dental practice, POS 11) |
| `Condition` | US Core / ODE | Presenting condition (K04.01) documented in virtual encounter; confirmed diagnoses (K04.01, K04.5) updated by in-office provider |
| `Observation` | US Core / ODE | Symptom findings from virtual encounter (pain on biting, thermal sensitivity, duration); periapical findings from in-office imaging |
| `MedicationStatement` | US Core | Patient-reported medications captured during virtual assessment; transmitted with referral |
| `ServiceRequest` | US Core / ODE | Structured referral from teledentistry provider to in-office dental provider; status lifecycle `active` → `completed` |
| `DocumentReference` | US Core | Clinical findings bundle from virtual encounter, transmitted as supporting documentation with referral |
| `Appointment` / `AppointmentResponse` | US Core | In-office appointment created by receiving practice; response returned to teledentistry provider and surfaced to patient application |
| `DiagnosticReport` | US Core / ODE | Periapical radiograph report (LOINC 62443-7) from in-office evaluation |
| `ImagingStudy` | US Core | Periapical radiographic image referenced in `DiagnosticReport` |
| `Procedure` | US Core / ODE | Root canal therapy (D3330, tooth #19, FDI 36) performed by in-office provider; teledentistry encounter (D9995) |
| `ClinicalImpression` | ODE | Structured post-treatment encounter summary transmitted from in-office practice to teledentistry provider via CDex |
| `CarePlan` | US Core | Post-treatment care instructions; surfaced to patient application |
| `Task` | CDex | Tracks the open referral as an actionable item; closed on receipt of encounter summary |
| `Subscription` / `SubscriptionStatus` | FHIR Subscriptions Backport IG | Push notifications to patient application at referral creation, appointment confirmation, and referral closure |
| `Bundle` | FHIR Core | Transaction bundles wrapping referral packet (ServiceRequest + Condition + Observation + MedicationStatement + DocumentReference) and encounter summary return |
| `AuditEvent` | US Core | Cross-organizational data access logging for compliance and provenance |
| `Provenance` | US Core | Chain of custody for clinical data across teledentistry provider, in-office practice, and payer FHIR endpoints |

---

### Cross-Cutting Test Objectives

1. **Patient matching across unaffiliated systems** — Teledentistry provider system, in-office practice interim FHIR server, and commercial payer must resolve the patient's identity without a shared master patient index, using demographic matching against US Core `Patient` profile elements.

2. **Real-time coverage verification at virtual care entry** — `Coverage` and `InsurancePlan` resources must be queryable at session initiation within the patient application, confirming teledentistry benefit eligibility before the virtual encounter begins.

3. **Structured virtual assessment as a referral payload** — Clinical findings documented by a dental provider in a virtual encounter must be expressible as discrete FHIR resources — `Condition`, `Observation`, `MedicationStatement` — rather than as a PDF or free-text note, enabling the receiving in-office practice to act on structured data at point of care.

4. **Interim FHIR server as a dental interoperability bridge** — The in-office practice management system's lack of native FHIR capability is addressed through an interim FHIR server, mirroring the architecture pattern established in prior OHIA Connectathon use cases. This use case tests whether that pattern can support both inbound referral receipt and outbound encounter summary return in a teledentistry referral context.

5. **Referral status lifecycle** — `ServiceRequest` must transition correctly through `draft` → `active` → `completed`, with each status change triggering a patient-facing notification via FHIR Subscriptions.

6. **Closed-loop encounter summary** — The in-office practice must transmit a structured `ClinicalImpression` and `Procedure` bundle back to the originating teledentistry provider via CDex, closing the referral loop without a portal login or phone call.

7. **CDT codes across care settings** — Both the teledentistry encounter (`D9995`, POS 02) and the in-office procedure (`D3330`, POS 11) must be expressible using ODE-profiled `Procedure` resources with CDT codes in `Procedure.code`, enabling downstream 837D claims submission from discrete FHIR data.

8. **Multi-organization patient application coherence** — The patient application surfaces data from two independent provider organizations and the payer, testing SMART App Launch, PDex, and FHIR Subscriptions in a single patient-facing view without requiring separate logins.

9. **ODE IG validation in a teledentistry originating context** — This use case exercises ODE profiles where the originating encounter occurs in a virtual setting — a workflow not previously tested in OHIA Connectathons — validating that tooth-level `Observation` and `Condition` resources are expressible from a non-PMS-centric clinical encounter.

---

## Section IV: EDI Transactions

Sarah's Aetna Dental PPO is a **commercial dental benefit**. All services are billed under the dental benefit using standard 837D transactions. No medical benefit crossover is in scope.

### EDI Transactions in Scope

| X12 Transaction | Trigger | Scope Note |
|---|---|---|
| **270 / 271** — Eligibility & Benefit Inquiry / Response | Teledentistry provider verifies patient Aetna Dental eligibility at session initiation | Queries dental benefit; confirms teledentistry (D9995) coverage, annual maximum remaining, and endodontic benefit |
| **837D** — Dental Claim (Teledentistry Provider) | Teledentistry provider bills Aetna Dental for the synchronous virtual consultation | CDT D9995 (teledentistry — synchronous); POS 02; teledentistry provider as rendering provider |
| **837D** — Dental Claim (In-Office Dental Practice) | In-office practice bills Aetna Dental for evaluation, imaging, and endodontic treatment | CDT D0220 (periapical radiograph); D3330 (molar root canal, tooth #19); POS 11; in-office provider as rendering provider; referral number included |
| **835** — Remittance Advice | Aetna Dental adjudicates and pays both claims | Adjustment reason codes; patient cost responsibility per plan design |

> **Note on 278:** No prior authorization is required for D9995 or D3330 under this plan design. The X12 278 transaction is not in scope for this use case.

### CDT Codes in Scope

| CDT Code | Description | Care Setting | Provider Role |
|---|---|---|---|
| `D9995` | Teledentistry — synchronous; real-time encounter | POS 02 — Telehealth | Teledentistry provider |
| `D0120` | Periodic oral evaluation — established patient | POS 11 — Office | In-office dental provider |
| `D0220` | Periapical radiographic image | POS 11 — Office | In-office dental provider |
| `D3330` | Endodontic therapy, molar tooth (excl. final restoration) | POS 11 — Office | In-office dental provider |

### LOINC Codes in Scope

| LOINC Code | Description | FHIR Resource | Use in This Case |
|---|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport`, `ImagingStudy` | Periapical radiograph — in-office evaluation |
| `72166-2` | Tobacco smoking status | `Observation` | Patient history captured in virtual assessment |

---

## Appendix A: Data

### 1. Patient Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Name** | Sarah Okonkwo | Given: Sarah; Family: Okonkwo |
| **Date of Birth** | 1991-03-17 | Age: 34 |
| **Sex** | Female | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **Teledentistry Provider Patient ID** | `TELE-TX-10047823` | System: `https://teledentistry-provider.example.org/fhir/patient-id` |
| **In-Office Practice MRN** | `INOFF-2026-0091` | System: `https://inoffice-dental.example.org/fhir/mrn` |
| **Telecom (Phone)** | (512) 555-0184 | Use: Mobile |
| **Telecom (Email)** | sarah.okonkwo@example.com | Use: Home |
| **Address** | 4412 Barton Creek Blvd, Apt 7, Austin, TX 78735 | City: Austin; State: TX; ZIP: 78735 |
| **Language** | English | Preferred language |
| **Active** | True | Patient record is active |

---

### 2. Coverage Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Payer** | Commercial Dental Payer | Organization reference |
| **Plan Name** | Employer Dental PPO | Commercial group dental plan |
| **Plan Type** | PPO | Preferred Provider Organization |
| **Member ID** | AET-TX-00284711 | Primary member identifier |
| **Group Number** | 847221 | Employer group |
| **Coverage Period** | 2026-01-01 – 2026-12-31 | Plan year |
| **Status** | Active | Coverage confirmed |
| **Network** | PPO In-Network | In-network status |
| **Annual Maximum** | $2,000 | Per member, per plan year |
| **Deductible** | $50 | Individual; applies to basic and major services |
| **Preventive / Diagnostic** | 100% covered | No deductible; in-network |
| **Basic Services (Endodontics)** | 80% covered | After deductible; in-network |
| **Teledentistry Benefit** | Covered | D9995; subject to basic service cost-sharing |
| **Remaining Annual Maximum** | $1,850 | At time of encounter |
| **Payer EDI ID** | 60054 | HIPAA X12 claims routing |
| **Payer FHIR Endpoint** | `https://payer.example.org/fhir/r4` | Synthetic payer FHIR API |

---

### 3. Organization Resource Data

#### Teledentistry Provider Organization

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1982734561 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | Teledentistry Provider Organization (Synthetic) | Test data label |
| **Type** | Virtual Dental Care Provider | Organization type |
| **Care Setting** | Place of Service 02 — Telehealth | Virtual care setting |
| **NPI Taxonomy Code** | 1223G0001X | General dentist (group) |
| **FHIR Endpoint** | `https://teledentistry-provider.example.org/fhir/r4` | Synthetic FHIR server |
| **Licensed States** | Texas (and others per licensure) | Jurisdiction |

#### In-Office Dental Practice

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1467823059 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | In-Office Dental Practice (Synthetic) | Test data label |
| **Address** | 3801 South Lamar Blvd, Suite 200, Austin, TX 78704 | Synthetic practice location |
| **Phone** | (512) 555-0210 | Synthetic |
| **Type** | Dental Practice | Organization type |
| **Care Setting** | Place of Service 11 — Office | In-office setting |
| **Practice Management System** | Dental PMS with interim FHIR server | Architecture pattern |
| **FHIR Endpoint** | `https://inoffice-dental.example.org/fhir/r4` | Interim FHIR server |
| **NPI Taxonomy Code** | 1223G0001X | General dentist |
| **Network** | Commercial PPO In-Network | Payer participation |

#### Commercial Dental Payer

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | Commercial Dental Payer (Synthetic) | Test data label |
| **Type** | Commercial Dental Plan | Organization type |
| **Payer EDI ID** | 60054 | X12 claims routing |
| **FHIR Endpoint** | `https://payer.example.org/fhir/r4` | Synthetic payer FHIR API |

---

### 4. Practitioner Resource Data

#### Teledentistry Provider — Dr. Marcus Webb, DDS

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1538476201 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Marcus James Webb, DDS | Given: Marcus; Family: Webb |
| **Qualification** | DDS — Doctor of Dental Surgery | Dental degree |
| **License Number** | TX-DDS-047821 | Texas dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223G0001X | General dentist |
| **Organization** | Teledentistry Provider Organization | Employment |
| **Place of Service** | 02 — Telehealth | Virtual care setting |

#### In-Office Dental Provider — Dr. Priya Nair, DDS

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1649203847 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Priya Anand Nair, DDS | Given: Priya; Family: Nair |
| **Qualification** | DDS — Doctor of Dental Surgery | Dental degree |
| **License Number** | TX-DDS-052394 | Texas dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223G0001X | General dentist |
| **Organization** | In-Office Dental Practice | Employment |
| **Place of Service** | 11 — Office | In-office setting |

---

### 5. Workflow & Service Data

#### ServiceRequest (Referral — Teledentistry Provider to In-Office Dental Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Referral fulfilled |
| **Intent** | Order | Clinical order |
| **Category** | Consultation / Referral | Type |
| **Priority** | Urgent | Acute pain; next-day appointment indicated |
| **Code** | In-office dental evaluation and endodontic treatment — irreversible pulpitis, tooth #19 | Referral reason |
| **Subject** | Sarah Okonkwo | Patient reference |
| **Requester** | Dr. Marcus Webb, DDS | Teledentistry provider |
| **Performer** | Dr. Priya Nair, DDS | In-office dental provider |
| **Reason Code** | K04.01 — Irreversible pulpitis | ICD-10 presenting diagnosis |
| **Ordered Date** | 2026-07-14 | Virtual encounter date |
| **Occurrence DateTime** | 2026-07-15 | Target in-office appointment |
| **Description** | Patient presents via synchronous teledentistry encounter with acute pain on biting, thermal sensitivity, and three-day symptom duration, lower left quadrant. Clinical presentation consistent with irreversible pulpitis, tooth #19. Periapical involvement possible. Radiographic evaluation and endodontic assessment indicated. Patient medication list attached. No known drug allergies reported. | Referral payload |

#### Encounter (Virtual — Teledentistry Provider, POS 02)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Finished | Complete |
| **Class** | Virtual (VR) | Teledentistry |
| **Type** | Consultation | Encounter type |
| **Subject** | Sarah Okonkwo | Patient reference |
| **Participant** | Dr. Marcus Webb, DDS | Teledentistry provider |
| **Period** | 2026-07-14T19:32:00-05:00 – 2026-07-14T19:58:00-05:00 | 26 minutes |
| **Location** | POS 02 — Telehealth | Virtual |
| **Reason Code** | K04.01 | Presenting complaint |

#### Condition (Virtual Assessment Finding)

| FHIR Element | Value | Notes |
|---|---|---|
| **Clinical Status** | Active | Condition active |
| **Verification Status** | Provisional | Assessed; radiographic confirmation required |
| **Code** | K04.01 — Irreversible pulpitis | ICD-10 |
| **Body Site** | Tooth #19 (FDI: 36) | Lower left first molar |
| **Asserter** | Dr. Marcus Webb, DDS | Documenting provider |
| **Onset** | Approximately 3 days prior to encounter | Patient-reported |
| **Note** | Acute pain on biting, thermal sensitivity to cold, spontaneous aching. Possible periapical involvement. Radiographic confirmation required. | Clinical note |

#### Procedure (Root Canal Therapy — In-Office Practice, POS 11)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Code** | D3330 (CDT) | Endodontic therapy, molar tooth |
| **Subject** | Sarah Okonkwo | Patient reference |
| **Performer** | Dr. Priya Nair, DDS | In-office dental provider |
| **Performed DateTime** | 2026-07-15 | Date of procedure |
| **Body Site** | Tooth #19 (FDI: 36) | Lower left first molar |
| **Reason Reference** | K04.01 (confirmed); K04.5 (periapical abscess without sinus) | Confirmed diagnoses |
| **Note** | Three canals instrumented and obturated. Pre-operative periapical radiograph confirmed periapical rarefaction. Post-operative radiograph taken. Patient tolerated procedure well. Final restoration to be placed by patient's regular dental provider. | Operative note |

#### DiagnosticReport (Periapical Radiograph)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Final | Complete |
| **Code** | D0220 (CDT) / LOINC 62443-7 | Periapical radiographic image |
| **Performer** | Dr. Priya Nair, DDS | In-office dental provider |
| **Effective DateTime** | 2026-07-15 | Date of imaging |
| **Conclusion** | Tooth #19: periapical rarefaction consistent with periapical abscess. Three-canal anatomy. No root fracture. Endodontic treatment completed same visit. | Radiographic findings |

#### ClinicalImpression (Encounter Summary — In-Office Practice to Teledentistry Provider)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Summary complete |
| **Date** | 2026-07-15 | Date of summary |
| **Assessor** | Dr. Priya Nair, DDS | In-office dental provider |
| **Summary** | Patient seen 2026-07-15 per referral from teledentistry provider. Periapical radiograph confirmed irreversible pulpitis with periapical abscess, tooth #19. Root canal therapy completed in single visit (D3330). Three canals instrumented and obturated. Patient tolerated procedure well. Final restoration (crown) indicated; patient advised to contact primary dental provider. Follow-up periapical radiograph recommended at 6 months. | Encounter summary |
| **Finding** | Confirmed: K04.01; K04.5 | Confirmed diagnoses |
| **Recommendations** | 1. Final restoration (crown) by patient's regular dental provider; 2. Periapical radiograph follow-up at 6 months; 3. Ibuprofen 400mg PRN for post-operative discomfort | Post-treatment plan |

---

### 6. Clinical Codes & Mappings

#### ICD-10 Diagnosis Codes

| Code | Description | Application |
|---|---|---|
| K04.01 | Irreversible pulpitis | Presenting diagnosis (virtual); confirmed (in-office) |
| K04.5 | Periapical abscess without sinus | Confirmed in-office (radiographic) |

#### CDT Codes in Scope

| Code | Description | Care Setting |
|---|---|---|
| `D9995` | Teledentistry — synchronous; real-time encounter | POS 02 |
| `D0120` | Periodic oral evaluation | POS 11 |
| `D0220` | Periapical radiographic image | POS 11 |
| `D3330` | Endodontic therapy, molar tooth (excl. final restoration) | POS 11 |

#### LOINC Codes

| LOINC | Description | FHIR Resource |
|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport` |
| `72166-2` | Tobacco smoking status | `Observation` |

---

### 7. Timeline & Dates

| Event | Date | Time (Central) | Actor | System |
|---|---|---|---|---|
| **Coverage Verified (FHIR)** | 2026-07-14 | 19:22 | Patient application | Payer FHIR API → `Coverage` |
| **Virtual Encounter — POS 02** | 2026-07-14 | 19:32–19:58 | Dr. Webb / Patient | Teledentistry provider system |
| **Structured Referral Transmitted** | 2026-07-14 | 20:05 | Dr. Webb | CDex push → In-office interim FHIR server |
| **Patient Notified — Referral Sent** | 2026-07-14 | 20:05 | Patient application | FHIR Subscription event |
| **Referral Received at In-Office Practice** | 2026-07-14 | 20:06 | In-office system | Interim FHIR server |
| **Appointment Scheduled** | 2026-07-14 | 20:45 | In-office staff | Dental PMS |
| **AppointmentResponse Returned** | 2026-07-14 | 20:47 | In-office system | Interim FHIR → Teledentistry provider FHIR |
| **Patient Notified — Appointment Confirmed** | 2026-07-14 | 20:47 | Patient application | FHIR Subscription event |
| **In-Office Evaluation, Radiograph & Root Canal — POS 11** | 2026-07-15 | 10:00–12:15 | Dr. Nair / Patient | Dental PMS |
| **Encounter Summary Transmitted** | 2026-07-15 | 12:35 | In-office system | CDex push → Teledentistry provider FHIR |
| **Referral Closed** | 2026-07-15 | 12:36 | Teledentistry provider system | `ServiceRequest` → completed |
| **Patient Application Updated** | 2026-07-15 | 12:36 | Patient application | FHIR Subscription event |
| **837D Submitted — Teledentistry Provider** | 2026-07-16 | 08:00 | Billing | D9995, POS 02 → Payer EDI |
| **837D Submitted — In-Office Practice** | 2026-07-16 | 08:30 | Billing | D0220, D3330, POS 11 → Payer EDI |

#### Key Timeline Constraints

| Constraint | Target | Rationale |
|---|---|---|
| **Referral Transmission** | Same session as virtual encounter | Acute pain presentation |
| **Appointment Confirmation** | Within 2 hours of referral receipt | Urgency flag on `ServiceRequest` |
| **In-Office Appointment** | Next business day | Acute presentation with possible abscess |
| **Encounter Summary Return** | Same day as in-office visit | Closes referral loop; enables originating provider review |

---
---

# Use Case B: Medicaid

## Teledentistry Referral — Acute Dental Pain with Diabetes Comorbidity
### Texas Medicaid Managed Care (STAR Program) | Place of Service 02 → 11

---

## Section I: Business Overview

**Darius Reyes** is a 28-year-old man (DOB: 09/04/1997) living in San Antonio, Texas. He is enrolled in **Texas Medicaid** through the **STAR program**, administered through a Medicaid managed care organization (MCO). Dental benefits are administered through a **dental benefit manager (DBM)**. His Medicaid ID is `TX-MCD-0047832`.

Darius has not seen a dental provider in over three years. He has been experiencing intermittent pain in his upper right area for several weeks but has not sought care — he is unfamiliar with his dental benefit, does not have a regular dental provider, and does not know which providers near him accept Medicaid. The pain has become persistent enough that he cannot sleep.

At 11:45 PM, Darius accesses a **SMART-enabled patient application** associated with his Medicaid dental benefit. The application verifies his Texas Medicaid eligibility and dental benefit in real time via a FHIR `Coverage` query. His coverage is confirmed active. He is connected to **Dr. Angela Torres, DDS**, a licensed Texas dental provider practicing in a virtual care setting (Place of Service 02).

Before creating a referral, the teledentistry provider system performs a **FHIR-based provider directory query** (Plan-Net) against the DBM's network directory to identify an in-office dental practice in San Antonio that is currently active in the Medicaid network and accepting new patients. This check — which today requires a phone call or a static PDF directory — is performed as a structured `PractitionerRole` and `HealthcareService` query and returns a confirmed in-network in-office practice.

Dr. Torres conducts a structured synchronous virtual assessment. Darius describes throbbing pain in the upper right, sensitivity to sweets, and pain that has kept him awake. He reports he is currently taking metformin for **Type 2 diabetes** (`ICD-10: E11.9`). Dr. Torres documents these findings and creates a **`Flag` resource** communicating elevated infection and healing risk due to diabetes — a clinically relevant signal that must travel with the referral to inform the in-office care team.

Based on the assessment, Dr. Torres identifies clinical indicators consistent with **irreversible pulpitis of tooth #3** (`ICD-10: K04.01`) with probable secondary caries. She creates a **structured referral** to the identified in-office dental practice, transmitting the referral as a FHIR `ServiceRequest` with supporting `Condition`, `Observation`, `MedicationStatement`, and `Flag` resources via CDex provider-to-provider push.

Darius receives an in-application notification that his referral has been sent. The in-office practice receives the referral via an interim FHIR server and contacts Darius that morning to schedule an appointment within 48 hours — consistent with Texas Medicaid urgent care access standards.

**Dr. James Okafor, DDS**, at the in-office practice sees Darius two days later. He takes periapical and bitewing radiographs (`D0220`, `D0274`) and confirms irreversible pulpitis with non-restorable secondary caries on tooth #3 and identifies two additional teeth with moderate decay. Given Darius's diabetes, Dr. Okafor notes elevated periodontal risk. He performs a surgical extraction on tooth #3 (`D7210`) and places interim restorations on the two additional teeth (`D2940` ×2), with a planned follow-up for permanent restorations.

Dr. Okafor documents the encounter and transmits a **structured encounter summary** back to the teledentistry provider via CDex. The summary includes confirmed diagnoses, procedures performed, CDT codes, and a care plan recommending a complete periodontal evaluation and regular preventive care — explicitly connecting the diabetes-oral health relationship.

Dr. Torres reviews the closed referral and follows up with Darius through the patient application — reinforcing the importance of regular dental care given his diabetes and providing guidance on using his Medicaid dental benefit for ongoing preventive visits.

The in-office practice submits an 837D to the DBM for in-office services. The teledentistry provider submits a separate 837D for the virtual consultation under `D9995`.

---

## Section II: Narrative-to-Standards Mapping

| What Happens (Business Language) | Implementation Guide / Standard | Key Transaction |
|---|---|---|
| **Verify Coverage:** Patient application verifies Texas Medicaid dental eligibility and DBM benefit at session initiation. | US Core / Da Vinci PDex | `Coverage` queried against DBM FHIR API; `InsurancePlan` returned with adult dental benefit details and annual maximum. |
| **Provider Directory Check:** Teledentistry provider system queries DBM provider directory to identify a Medicaid-participating in-office dental practice accepting new patients in San Antonio. | Da Vinci PDex / Plan-Net IG | `PractitionerRole` and `HealthcareService` queried from DBM Plan-Net FHIR API; confirms network participation and open panel status before referral is created. |
| **Virtual Assessment:** Dr. Torres conducts a structured synchronous evaluation (POS 02); documents clinical findings and flags diabetes comorbidity. | US Core / ODE (Under Development) | `Encounter` (POS 02); `Condition` (K04.01, K02.9); `Observation` (symptom findings, tooth-level); `MedicationStatement` (metformin); `Flag` (diabetes — elevated infection and healing risk). |
| **Patient Notification — Referral Sent:** Patient notified in-application that referral has been transmitted. | FHIR Subscriptions Backport IG | Subscription event on `ServiceRequest` creation. |
| **Structured Referral Transmitted:** Dr. Torres transmits structured referral with clinical context and diabetes flag to in-office dental practice. | US Core / ODE (Under Development) / CDex | `ServiceRequest` (urgent); `DocumentReference` (findings bundle); `Flag` (diabetes); `MedicationStatement`; CDex provider-to-provider push to in-office practice interim FHIR server. |
| **Referral Received at In-Office Practice:** In-office practice receives referral via interim FHIR server; contacts patient for urgent appointment. | US Core / ODE (Under Development) | `ServiceRequest` received; `Appointment` created; `AppointmentResponse` returned. |
| **Patient Notification — Appointment Confirmed:** Patient receives in-application confirmation of appointment. | FHIR Subscriptions Backport IG | Subscription event on `AppointmentResponse`. |
| **In-Office Evaluation & Imaging:** Dr. Okafor takes periapical and bitewing radiographs; confirms diagnoses. | US Core / ODE (Under Development) | `DiagnosticReport` (LOINC 62443-7, 46386-9); `Condition` updated with confirmed diagnoses; additional caries conditions documented. |
| **Treatment Performed:** Dr. Okafor extracts tooth #3 and places interim restorations on two additional teeth. | US Core / ODE (Under Development) | `Procedure` (D7210, tooth #3, FDI 16); `Procedure` (D2940 ×2); `Encounter` (POS 11). |
| **Encounter Summary Returned:** Dr. Okafor transmits structured post-treatment summary — including diabetes-dental connection — to teledentistry provider. | Da Vinci CDex / ODE (Under Development) | `ClinicalImpression`; `Procedure` (completed); `CarePlan` (periodontal evaluation; preventive care frequency given diabetes); CDex push to teledentistry provider FHIR endpoint. |
| **Referral Closed; Follow-Up by Dr. Torres:** Dr. Torres reviews encounter summary; follows up with patient in-application on diabetes-dental care. | US Core / CDex | `ServiceRequest` → completed; `Task` closed; in-application follow-up communication. |
| **Patient Application Updated:** Application shows referral complete with care plan; guidance on Medicaid preventive dental benefit surfaced. | FHIR Subscriptions Backport IG / US Core | Subscription event; `CarePlan` surfaced to patient application via SMART App Launch. |
| **Claims Submission:** In-office practice submits 837D to DBM; teledentistry provider submits 837D separately. | X12 837D | 837D (in-office): D0220, D0274, D7210, D2940 ×2, POS 11; 837D (teledentistry): D9995, POS 02; Texas Medicaid fee schedule applied. |

---

## Section III: Technical Overview

This use case exercises a **virtual-to-in-office provider referral in a Medicaid managed care context**, spanning a teledentistry provider system, an in-office dental practice management system, a Medicaid dental benefit manager, and a Medicaid MCO. The scenario adds two capabilities not present in Use Case A: **FHIR-based provider directory lookup** (Plan-Net) to identify Medicaid-network-participating in-office dental providers, and the **`Flag` resource** to communicate a clinically relevant comorbidity (diabetes) from the virtual assessment to the in-office care team.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

### Implementation Guides

| Implementation Guide | Purpose in This Use Case |
|---|---|
| **US Core IG** | Defines FHIR profiles for all clinical data exchanged between teledentistry provider, in-office practice, DBM, and MCO |
| **Da Vinci PDex / Plan-Net IG** | Provider directory query to confirm in-office dental practice is active in Medicaid network and accepting new patients — replacing static PDF directories and phone-based verification; also enables patient application to surface coverage and benefit data from DBM |
| **Da Vinci Clinical Data Exchange (CDex)** | Two roles: (1) **Provider-to-provider referral push** — structured referral, clinical context, and diabetes flag from teledentistry provider to in-office practice interim FHIR server; (2) **Provider-to-provider encounter summary return** — post-treatment summary from in-office practice to teledentistry provider |
| **SMART App Launch IG** | Authorization framework for patient application to connect to DBM FHIR endpoint for coverage verification and to surface post-treatment `CarePlan` |
| **FHIR Subscriptions Backport IG** | Push notifications to patient application at referral creation, appointment confirmation, and referral closure |
| **Oral Health Data Exchange IG (ODE)** | Under development; governs structured exchange of oral health clinical data including `Flag` (comorbidity) as a referral payload element — a capability being validated for the first time in this use case |

---

### Key FHIR Resources Exercised

| FHIR Resource | Source IG / Profile | Purpose in This Use Case |
|---|---|---|
| `Patient` | US Core | Patient identity across teledentistry provider, in-office practice interim FHIR server, and DBM; Medicaid ID as primary identifier |
| `Coverage` | US Core / PDex | Texas Medicaid dental benefit — Medicaid ID, MCO, DBM, benefit details — verified at session initiation |
| `InsurancePlan` | Da Vinci PDex | DBM plan benefit structure; adult dental benefit limitations and covered services under Texas Medicaid |
| `Organization` | US Core / Plan-Net | Teledentistry provider organization; in-office dental practice; DBM; MCO |
| `PractitionerRole` | US Core / Plan-Net | Queried against DBM Plan-Net directory to confirm in-office provider Medicaid network participation and panel status before referral creation |
| `HealthcareService` | Da Vinci Plan-Net | In-office practice dental services — queried to confirm open panel status for Medicaid patients |
| `Practitioner` | US Core | Teledentistry provider (POS 02); in-office dental provider (POS 11) |
| `Location` | US Core / Plan-Net | Teledentistry virtual location (POS 02); in-office practice physical location (San Antonio, TX; POS 11) |
| `Encounter` | US Core | Virtual encounter (POS 02); in-office encounter (POS 11) |
| `Condition` | US Core / ODE | K04.01, K02.9 documented in virtual encounter; confirmed and expanded by in-office provider; E11.9 referenced as comorbidity |
| `Flag` | US Core | Diabetes comorbidity alert — elevated infection and healing risk — created by teledentistry provider; transmitted with referral to alert in-office care team |
| `MedicationStatement` | US Core | Metformin captured in virtual assessment; transmitted with referral |
| `Observation` | US Core / ODE | Symptom findings from virtual encounter; periapical and bitewing findings from in-office imaging |
| `ServiceRequest` | US Core / ODE | Structured referral; status lifecycle `active` → `completed` |
| `DocumentReference` | US Core | Clinical findings bundle from virtual encounter |
| `Appointment` / `AppointmentResponse` | US Core | In-office appointment and confirmation |
| `DiagnosticReport` | US Core / ODE | Periapical (LOINC 62443-7) and bitewing (LOINC 46386-9) radiograph reports |
| `Procedure` | US Core / ODE | D7210 (tooth #3); D2940 ×2; D9995 (teledentistry encounter) |
| `ClinicalImpression` | ODE | Post-treatment encounter summary with diabetes-dental connection and ongoing care plan; transmitted via CDex |
| `CarePlan` | US Core | Post-treatment plan including periodontal evaluation and preventive care frequency; surfaced to patient application |
| `Task` | CDex | Tracks open referral; closed on receipt of encounter summary |
| `Subscription` / `SubscriptionStatus` | FHIR Subscriptions Backport IG | Push notifications to patient application at key milestones |
| `Bundle` | FHIR Core | Referral packet and encounter summary return |
| `AuditEvent` | US Core | Cross-organizational data access logging |
| `Provenance` | US Core | Chain of custody across all participating systems |

---

### Cross-Cutting Test Objectives

1. **Patient matching in a Medicaid context** — Teledentistry provider system, in-office practice interim FHIR server, and DBM must resolve the patient's identity using Medicaid ID as the primary identifier without a shared master patient index.

2. **Real-time Medicaid coverage verification at virtual care entry** — `Coverage` and `InsurancePlan` must be queryable at session initiation, confirming active Texas Medicaid dental benefit eligibility and DBM enrollment before the virtual encounter begins.

3. **FHIR-based provider directory as a Medicaid network check** — This use case introduces Plan-Net directory queries as a pre-referral step: confirming target in-office practice is active in the Medicaid network and accepting patients before `ServiceRequest` creation. This replaces static PDF directories and phone verification that characterize Medicaid referral workflows today.

4. **`Flag` resource for clinically relevant comorbidity** — The `Flag` resource (diabetes) created in the virtual encounter must travel with the referral and be surfaced to the in-office provider at the point of care, testing whether clinically relevant flags from a virtual assessment can be transmitted as structured data in a FHIR referral payload.

5. **Interim FHIR server as a dental interoperability bridge** — In-office PMS lack of native FHIR capability is addressed through an interim FHIR server, mirroring the architecture pattern established in prior OHIA Connectathon use cases, testing both inbound referral receipt and outbound encounter summary return.

6. **Referral status lifecycle** — `ServiceRequest` must transition correctly through `draft` → `active` → `completed`, with each status change triggering a patient-facing notification via FHIR Subscriptions.

7. **Closed-loop encounter summary in a Medicaid context** — In-office practice must transmit a structured `ClinicalImpression` and `Procedure` bundle back to the originating teledentistry provider via CDex, including the diabetes-dental connection and ongoing care plan, without portal login or phone call.

8. **Medicaid-specific benefit constraints at claims submission** — CDT codes on the 837D must reflect applicable Texas Medicaid adult dental benefit limitations, surfacing benefit design constraints as named test findings where ODE-transmitted procedure data and Medicaid claims adjudication intersect.

9. **ODE IG validation with comorbidity context** — This use case introduces the `Flag` resource into an ODE-profiled referral payload, validating that clinically relevant medical context from a virtual dental assessment can be expressed and transmitted as structured data — essential for the oral-systemic integration goals of the OHIA Connect and Integrate strategic priorities.

10. **Patient application as care navigation tool** — The patient application experience — from coverage verification through referral completion and provider follow-up — tests SMART App Launch, PDex, and FHIR Subscriptions as the infrastructure for care navigation for a Medicaid patient who lacked a regular dental provider, validating the OHIA Empower and Locate strategic priorities in a real-world access gap scenario.

---

## Section IV: EDI Transactions

Darius's dental benefits are administered through a **dental benefit manager (DBM)** under Texas Medicaid STAR managed care. All dental services are billed to the DBM via 837D. Texas Medicaid adult dental benefits are limited; applicable fee schedule rates and covered procedure restrictions are applied at adjudication.

### EDI Transactions in Scope

| X12 Transaction | Trigger | Scope Note |
|---|---|---|
| **270 / 271** — Eligibility & Benefit Inquiry / Response | Teledentistry provider verifies patient Texas Medicaid dental eligibility at session initiation | Queries DBM dental benefit; confirms active enrollment, annual maximum, and covered procedures for Texas Medicaid adults |
| **837D** — Dental Claim (Teledentistry Provider) | Teledentistry provider bills DBM for synchronous virtual consultation | CDT D9995 (teledentistry — synchronous); POS 02; teledentistry provider as rendering provider; Medicaid fee schedule rate applies |
| **837D** — Dental Claim (In-Office Dental Practice) | In-office practice bills DBM for evaluation, radiographs, extraction, and interim restorations | CDT D0220, D0274, D7210 (tooth #3), D2940 ×2; POS 11; in-office provider as rendering provider; referral number included; Texas Medicaid adult benefit limitations applied at adjudication |
| **835** — Remittance Advice | DBM adjudicates and pays both claims | Texas Medicaid fee schedule rates; adjustment reason codes; any non-covered procedure denials surfaced as named test findings |

> **Texas Medicaid Note:** Texas Medicaid adult dental benefits are limited in scope. Covered services for adults (age 21+) under Texas STAR include emergency extractions, oral examinations, and a limited set of restorative procedures. Benefit limitations, annual maximums, and prior authorization requirements for specific CDT codes should be confirmed against the current Texas Medicaid Dental Provider Procedures Manual at time of implementation. D9995 and D7210 are treated as covered under the emergency/urgent dental service benefit in this use case. D2940 (interim restoration) coverage under Texas Medicaid adult benefit is flagged as an open test finding.

### CDT Codes in Scope

| CDT Code | Description | Care Setting | Medicaid Coverage Note |
|---|---|---|---|
| `D9995` | Teledentistry — synchronous; real-time encounter | POS 02 | Covered in Texas Medicaid; confirm current fee schedule |
| `D0120` | Periodic oral evaluation | POS 11 | Covered |
| `D0220` | Periapical radiographic image | POS 11 | Covered |
| `D0274` | Bitewing radiographic images — four images | POS 11 | Covered; frequency limitations may apply |
| `D7210` | Surgical extraction — erupted tooth | POS 11 | Covered under emergency dental benefit |
| `D2940` | Protective restoration (interim) | POS 11 | ⚠️ Coverage uncertain for Texas Medicaid adults — named open test finding |

### LOINC Codes in Scope

| LOINC Code | Description | FHIR Resource | Use in This Case |
|---|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport`, `ImagingStudy` | Periapical radiograph — in-office evaluation |
| `46386-9` | XR Teeth Bitewing Views | `DiagnosticReport`, `ImagingStudy` | Bitewing radiographs — in-office evaluation |
| `72166-2` | Tobacco smoking status | `Observation` | Patient history captured in virtual assessment |
| `4548-4` | Hemoglobin A1c / Hemoglobin.total in Blood | `Observation` | Most recent HbA1c surfaced if available; supports diabetes-oral health care coordination |

---

## Appendix B: Data

### 1. Patient Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Name** | Darius Reyes | Given: Darius; Family: Reyes |
| **Date of Birth** | 1997-09-04 | Age: 28 |
| **Sex** | Male | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **Teledentistry Provider Patient ID** | `TELE-TX-10052914` | System: `https://teledentistry-provider.example.org/fhir/patient-id` |
| **Texas Medicaid ID** | `TX-MCD-0047832` | System: `http://texas.medicaid.gov/beneficiary` |
| **In-Office Practice MRN** | `INOFF-SA-2026-0047` | System: `https://inoffice-dental.example.org/fhir/mrn` |
| **Telecom (Phone)** | (210) 555-0193 | Use: Mobile |
| **Telecom (Email)** | darius.reyes97@example.com | Use: Home |
| **Address** | 718 West Commerce Street, Apt 12, San Antonio, TX 78207 | City: San Antonio; State: TX; ZIP: 78207 |
| **Language** | English; Spanish | Preferred: English |
| **Active** | True | Patient record is active |

---

### 2. Coverage Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Payer** | Dental Benefit Manager (DBM) — Texas Medicaid | Organization reference |
| **MCO** | Medicaid Managed Care Organization (MCO) — Texas STAR | MCO reference |
| **Program** | Texas Medicaid — STAR | Medicaid managed care program |
| **Member ID** | TX-MCD-0047832 | Texas Medicaid beneficiary ID |
| **Coverage Period** | 2026-01-01 – 2026-12-31 | Enrollment year |
| **Status** | Active | Coverage confirmed |
| **Network** | DBM Texas Medicaid Network | In-network providers |
| **Annual Maximum** | $1,000 | Per member, per plan year (adult dental) |
| **Preventive / Diagnostic** | Covered | Oral evaluation, radiographs |
| **Extractions** | Covered | Emergency/urgent; D7210 |
| **Teledentistry** | Covered | D9995; confirm current fee schedule |
| **Restorations (Interim)** | Uncertain | D2940 — named open test finding |
| **Remaining Annual Maximum** | $1,000 | No prior claims in plan year |
| **DBM Payer EDI ID** | 65978 | HIPAA X12 claims routing |
| **DBM FHIR Endpoint** | `https://dbm.example.org/fhir/r4` | Synthetic DBM FHIR API |

---

### 3. Organization Resource Data

#### Teledentistry Provider Organization
*(Identical role to Use Case A; synthetic NPI and FHIR endpoint carry over)*

#### In-Office Dental Practice (San Antonio)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1578234096 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | In-Office Dental Practice — San Antonio (Synthetic) | Test data label |
| **Address** | 2210 Fredericksburg Road, San Antonio, TX 78201 | Synthetic practice location |
| **Phone** | (210) 555-0247 | Synthetic |
| **Type** | Dental Practice | Organization type |
| **Care Setting** | Place of Service 11 — Office | In-office setting |
| **Practice Management System** | Dental PMS with interim FHIR server | Architecture pattern |
| **FHIR Endpoint** | `https://inoffice-dental-sa.example.org/fhir/r4` | Interim FHIR server |
| **NPI Taxonomy Code** | 1223G0001X | General dentist |
| **Medicaid Participation** | Active — Texas Medicaid (STAR); DBM network | Confirmed via Plan-Net query |
| **Panel Status** | Accepting new patients | Confirmed via Plan-Net `HealthcareService` query |

#### Dental Benefit Manager (DBM) — Texas Medicaid

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | Dental Benefit Manager — Texas Medicaid (Synthetic) | Test data label |
| **Type** | Dental Benefit Manager | Organization type |
| **Program Lines** | Medicaid Dental; CHIP Dental | Programs administered |
| **Payer EDI ID** | 65978 | X12 claims routing |
| **FHIR Endpoint** | `https://dbm.example.org/fhir/r4` | Synthetic FHIR API |

#### Medicaid MCO — Texas STAR

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | Medicaid Managed Care Organization — Texas STAR (Synthetic) | Test data label |
| **Type** | Medicaid MCO | Organization type |
| **Program** | Texas STAR | Medicaid managed care |

---

### 4. Practitioner Resource Data

#### Teledentistry Provider — Dr. Angela Torres, DDS

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1729384056 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Angela Maria Torres, DDS | Given: Angela; Family: Torres |
| **Qualification** | DDS — Doctor of Dental Surgery | Dental degree |
| **License Number** | TX-DDS-059104 | Texas dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223G0001X | General dentist |
| **Organization** | Teledentistry Provider Organization | Employment |
| **Languages** | English; Spanish | Clinical languages |
| **Place of Service** | 02 — Telehealth | Virtual care setting |

#### In-Office Dental Provider — Dr. James Okafor, DDS

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1839204758 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | James Emeka Okafor, DDS | Given: James; Family: Okafor |
| **Qualification** | DDS — Doctor of Dental Surgery | Dental degree |
| **License Number** | TX-DDS-048293 | Texas dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223G0001X | General dentist |
| **Organization** | In-Office Dental Practice — San Antonio | Employment |
| **Medicaid Participation** | Active — Texas STAR / DBM | Confirmed via Plan-Net |
| **Place of Service** | 11 — Office | In-office setting |

---

### 5. Workflow & Service Data

#### ServiceRequest (Referral — Teledentistry Provider to In-Office Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Referral fulfilled |
| **Intent** | Order | Clinical order |
| **Category** | Consultation / Referral | Type |
| **Priority** | Urgent | Within-48-hour appointment target per Texas Medicaid access standards |
| **Code** | In-office dental evaluation and treatment — irreversible pulpitis with secondary caries, tooth #3; diabetes comorbidity | Referral reason |
| **Subject** | Darius Reyes | Patient reference |
| **Requester** | Dr. Angela Torres, DDS | Teledentistry provider |
| **Performer** | Dr. James Okafor, DDS | In-office dental provider |
| **Reason Code** | K04.01 — Irreversible pulpitis; K02.9 — Caries, unspecified | ICD-10 presenting diagnoses |
| **Supporting Info** | `Flag`: E11.9 (Type 2 diabetes — elevated infection and healing risk); `MedicationStatement`: Metformin 500mg daily | Comorbidity and medication context |
| **Ordered Date** | 2026-07-21 | Virtual encounter date |
| **Occurrence DateTime** | 2026-07-23 | Target in-office appointment (within 48 hours) |
| **Description** | Patient presents via synchronous teledentistry encounter at 11:45 PM with acute throbbing pain, upper right, sweet sensitivity, sleep disruption. Clinical presentation consistent with irreversible pulpitis, tooth #3, with probable secondary caries. Patient has Type 2 diabetes (E11.9) — elevated infection and healing risk; on metformin 500mg daily. No known drug allergies. Last dental visit > 3 years. Radiographic evaluation and in-office assessment indicated. Network verification confirmed — in-office practice active in DBM Medicaid network, accepting new patients. | Referral payload |

#### Flag (Diabetes Comorbidity Alert)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Active | Flag active |
| **Category** | Clinical | Clinical alert |
| **Code** | E11.9 — Type 2 diabetes mellitus, without complications | Condition driving the flag |
| **Subject** | Darius Reyes | Patient reference |
| **Author** | Dr. Angela Torres, DDS | Flagging provider |
| **Period Start** | 2026-07-21 | Date flag created |
| **Description** | Patient has Type 2 diabetes. Elevated risk for delayed healing and post-extraction infection. Consider prophylactic measures per clinical judgment. Confirm recent HbA1c if available. | Clinical advisory |

#### Procedure (Surgical Extraction — In-Office Practice, POS 11)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Code** | D7210 (CDT) | Surgical extraction — erupted tooth requiring elevation |
| **Subject** | Darius Reyes | Patient reference |
| **Performer** | Dr. James Okafor, DDS | In-office dental provider |
| **Performed DateTime** | 2026-07-23 | Date of procedure |
| **Body Site** | Tooth #3 (FDI: 16) | Upper right first molar |
| **Reason Reference** | K04.01 (confirmed); K02.9 (non-restorable caries) | Confirmed diagnoses |
| **Note** | Patient's diabetes noted; prophylactic antibiotic prescribed. Ibuprofen 400mg PRN; amoxicillin 500mg TID × 7 days. Procedure completed without complication. Patient counseled on elevated infection risk and monitoring. | Operative note |

#### Procedure (Interim Restorations — In-Office Practice, POS 11)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedures performed |
| **Code** | D2940 (CDT) × 2 | Protective restoration (sedative/interim) |
| **Subject** | Darius Reyes | Patient reference |
| **Performer** | Dr. James Okafor, DDS | In-office dental provider |
| **Performed DateTime** | 2026-07-23 | Date of procedures |
| **Body Sites** | Tooth #4 (FDI: 14); Tooth #12 (FDI: 25) | Upper right second premolar; upper left first premolar |
| **Reason** | Moderate caries with pulpal proximity; interim restorations placed pending definitive restoration | Clinical indication |
| **Note** | Permanent restorations indicated; patient advised to return for follow-up. D2940 coverage under Texas Medicaid adult benefit flagged as open test finding at claims submission. | Clinical and billing note |

#### ClinicalImpression (Encounter Summary — In-Office Practice to Teledentistry Provider)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Summary complete |
| **Date** | 2026-07-23 | Date of summary |
| **Assessor** | Dr. James Okafor, DDS | In-office dental provider |
| **Summary** | Patient seen 2026-07-23 per referral from teledentistry provider. Periapical and bitewing radiographs confirmed irreversible pulpitis with non-restorable caries, tooth #3; moderate caries on teeth #4 and #12. Surgical extraction completed, tooth #3 (D7210). Interim restorations placed, teeth #4 and #12 (D2940 ×2). Diabetes noted — prophylactic antibiotic prescribed per clinical judgment. Patient has no established dental provider; not seen in > 3 years. Given systemic diabetes-oral health connection, regular preventive dental care is strongly indicated. | Encounter summary |
| **Finding** | Confirmed: K04.01 (resolved by extraction); K02.9 (multiple sites); E11.9 (comorbidity) | Confirmed diagnoses |
| **Recommendations** | 1. Permanent restorations, teeth #4 and #12 (4–6 weeks); 2. Complete periodontal evaluation; 3. Preventive care every 6 months given diabetes; 4. Patient education on diabetes-oral health relationship; 5. HbA1c coordination with primary care provider recommended | Care plan |

---

### 6. Clinical Codes & Mappings

#### ICD-10 Diagnosis Codes

| Code | Description | Application |
|---|---|---|
| K04.01 | Irreversible pulpitis | Presenting diagnosis (virtual); confirmed (in-office); resolved by extraction |
| K02.9 | Dental caries, unspecified | Secondary caries tooth #3; moderate caries teeth #4 and #12 |
| E11.9 | Type 2 diabetes mellitus, without complications | Comorbidity; `Flag` resource; elevated healing and infection risk |

#### CDT Codes in Scope

| Code | Description | Care Setting | Medicaid Note |
|---|---|---|---|
| `D9995` | Teledentistry — synchronous | POS 02 | Covered |
| `D0120` | Periodic oral evaluation | POS 11 | Covered |
| `D0220` | Periapical radiographic image | POS 11 | Covered |
| `D0274` | Bitewing radiographic images — four images | POS 11 | Covered; frequency limits may apply |
| `D7210` | Surgical extraction — erupted tooth | POS 11 | Covered (emergency/urgent) |
| `D2940` | Protective restoration (interim) | POS 11 | ⚠️ Open test finding |

#### LOINC Codes

| LOINC | Description | FHIR Resource |
|---|---|---|
| `62443-7` | Single view Teeth Document XR | `DiagnosticReport` |
| `46386-9` | XR Teeth Bitewing Views | `DiagnosticReport` |
| `72166-2` | Tobacco smoking status | `Observation` |
| `4548-4` | Hemoglobin A1c | `Observation` |

---

### 7. Timeline & Dates

| Event | Date | Time (Central) | Actor | System |
|---|---|---|---|---|
| **Coverage Verified (FHIR)** | 2026-07-21 | 23:47 | Patient application | DBM FHIR API → `Coverage` |
| **Provider Directory Query (Plan-Net)** | 2026-07-21 | 23:48 | Teledentistry provider system | DBM Plan-Net FHIR API → `PractitionerRole`, `HealthcareService` |
| **Virtual Encounter — POS 02** | 2026-07-22 | 00:05–00:31 | Dr. Torres / Patient | Teledentistry provider system |
| **Structured Referral + Flag Transmitted** | 2026-07-22 | 00:38 | Dr. Torres | CDex push → In-office interim FHIR server |
| **Patient Notified — Referral Sent** | 2026-07-22 | 00:38 | Patient application | FHIR Subscription event |
| **Referral Received at In-Office Practice** | 2026-07-22 | 00:39 | In-office system | Interim FHIR server |
| **Appointment Scheduled; Patient Contacted** | 2026-07-22 | 08:15 | In-office staff | Dental PMS |
| **AppointmentResponse Returned** | 2026-07-22 | 08:18 | In-office system | Interim FHIR → Teledentistry provider FHIR |
| **Patient Notified — Appointment Confirmed** | 2026-07-22 | 08:18 | Patient application | FHIR Subscription event |
| **In-Office Evaluation, Radiographs, Extraction, Restorations — POS 11** | 2026-07-23 | 10:00–12:45 | Dr. Okafor / Patient | Dental PMS |
| **Encounter Summary Transmitted** | 2026-07-23 | 13:15 | In-office system | CDex push → Teledentistry provider FHIR |
| **Referral Closed** | 2026-07-23 | 13:16 | Teledentistry provider system | `ServiceRequest` → completed |
| **Patient Application Updated** | 2026-07-23 | 13:16 | Patient application | FHIR Subscription event |
| **Originating Provider Follow-Up to Patient** | 2026-07-24 | 09:00 | Dr. Torres | In-application message |
| **837D Submitted — Teledentistry Provider** | 2026-07-24 | 08:00 | Billing | D9995, POS 02 → DBM EDI |
| **837D Submitted — In-Office Practice** | 2026-07-24 | 08:30 | Billing | D0220, D0274, D7210, D2940 ×2, POS 11 → DBM EDI |

#### Key Timeline Constraints

| Constraint | Target | Rationale |
|---|---|---|
| **Referral Transmission** | Same session as virtual encounter | Acute pain presentation |
| **Provider Directory Query** | Completed before referral creation | Confirms Medicaid network status before `ServiceRequest` is generated |
| **Appointment Confirmation** | Next business morning | Referral received overnight |
| **In-Office Appointment** | Within 48 hours of referral | Texas Medicaid urgent care access standard |
| **Encounter Summary Return** | Same day as in-office visit | Closes referral loop; enables originating provider follow-up |
| **Originating Provider Follow-Up** | Within 24 hours of encounter summary receipt | Patient engagement and diabetes-dental care reinforcement |

---

*This dataset is a test and validation vehicle for the Oral Health Data Exchange (ODE) Implementation Guide, developed under HL7 and sponsored by the PIE Work Group (PSS-2714). It is intended for use in connectathon and interoperability testing environments only. oralhealthalliance.net*
