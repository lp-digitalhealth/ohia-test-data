# CMS Connectathon — Dental Interoperability Test Dataset
## Use Case: Pediatric Periodontitis Due to Poorly Managed Type 1 Diabetes
### Well-Child Exam → Oral Health Assessment → Pediatric Dental Referral → Bidirectional Summary Return
### Connecticut CHIP (Husky B) | Connie State HIE | Medical-to-Dental Record Exchange

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
  - [CDT Codes in Scope](#cdt-codes-in-scope)
  - [LOINC Codes in Scope](#loinc-codes-in-scope)
- [Appendix: Data](#appendix-data)
  - [Patient Resource Data](#1-patient-resource-data)
  - [Coverage Resource Data](#2-coverage-resource-data)
  - [Organization Resource Data](#3-organization-resource-data)
  - [Practitioner Resource Data](#4-practitioner-resource-data)
  - [Workflow and Service Data](#5-workflow-and-service-data)
  - [Clinical Codes and Mappings](#6-clinical-codes--mappings)
  - [Timeline and Dates](#7-timeline--dates)

---

## About This Use Case

This use case models a **medical-to-dental referral with bidirectional encounter summary return** for a pediatric patient enrolled in Connecticut's CHIP program (Husky B). It is the first OHIA Connectathon use case to exercise:

- **Connie** (Connecticut Health Information Exchange) as a state HIE routing layer for medical record transmission from a pediatrician to a pediatric dental provider
- **Epic Care Everywhere** as the medical record access mechanism at the originating pediatric practice
- **Husky B** (Connecticut CHIP, covering both medical and dental services) as the coverage context
- A **minor patient with surrogate decision-makers** — grandparents with limited knowledge of the patient's medical history — as the driving context for structured medical record exchange
- **Bidirectional encounter summary return to two medical providers simultaneously** — the pediatrician and the pediatric endocrinologist — reflecting the oral-systemic connection between periodontitis and glycemic control

This use case advances the **Integrate** and **Connect** strategic priorities of the Oral Health Interoperability Alliance: it demonstrates that dental providers can receive structured medical context prior to a clinical encounter, and that dental findings can be returned as structured data to the full medical care team — not just the referring provider.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

## Section I: Business Overview

**Timothy Jones** is a six-year-old male (DOB: 05/05/2019) receiving a well-child exam at **New Haven Pediatric Care Center** in New Haven, Connecticut. Timothy is covered through **Husky B**, Connecticut's CHIP program, which covers both medical and dental services. He is generally up to date on his well-child visits.

On February 28, 2025, Timothy was diagnosed with **Type 1 diabetes** (`ICD-10: E10.9`) during an emergency department visit. He has a **pediatric endocrinologist** and a **registered dietitian** on his care team. His glucose levels are monitored using a **continuous glucose monitor (CGM)**, and he received an insulin pump two months before this encounter. He has been prescribed **insulin lispro**. Managing his diabetes has been challenging since the initial diagnosis, though his glycemic levels have improved since the insulin pump was started.

**Dr. Laura Smith, MD**, Timothy's pediatrician at New Haven Pediatric Care Center, uses the **Yale New Haven Health instance of Epic** with access to **Care Everywhere** — Epic's national patient record sharing network. During the well-child visit, Dr. Smith conducts a **pediatric oral health assessment** as part of the well-child protocol.

Dr. Smith notes:

- Timothy has lost two teeth (both lower central incisors): one site remains edentulous; one adult tooth is partially erupted
- Timothy has complained of pain around the area of the missing teeth
- A significant amount of gingivitis is present on examination
- Timothy's household includes tobacco smoke exposure (`ICD-10: Z77.22`)

Dr. Smith documents **acute gingivitis, plaque-induced** (`ICD-10: K05.00`) and is concerned that without dental intervention it will rapidly progress to periodontitis — a risk substantially elevated by Timothy's poorly controlled Type 1 diabetes, which impairs immune response and periodontal tissue healing. Dr. Smith asks whether Timothy has a dental home. His parents confirm he has never seen a dental provider.

Dr. Smith recommends that Timothy follow up with a **pediatric dental provider** and provides a structured referral. Timothy's parents contact **Benecare**, which handles referral coordination and network directory services for Connecticut Medicaid dental, to identify a participating pediatric dental provider within 20 miles who is accepting new patients enrolled in Husky B. The dental benefit itself is administered through **Connecticut Dental Health Partnership** under the **Connecticut Medicaid MCO** (specific MCO to be confirmed against current Husky B enrollment data). They identify **Dr. David Watson, DDS**, a pediatric dental provider accepting Husky B, and schedule an appointment — which is available **three months** after the well-child visit.

**The records gap:** Timothy's grandparents accompany him to the dental appointment. They have limited knowledge of Timothy's medical history beyond knowing he has Type 1 diabetes and his pediatrician is Dr. Smith. Without structured record exchange, Dr. Watson would begin the encounter with no clinical context — no diabetes management status, no medication list, no glycemic history, no record of the gingivitis finding from the well-child visit.

**With structured record exchange:** Dr. Watson receives Timothy's medical records from New Haven Pediatric Care Center **prior to the dental encounter**, transmitted through **Connie** (Connecticut Health Information Exchange) using a FHIR-based provider-to-provider push via CDex. The records — routed by Connie from the Epic FHIR endpoint at Yale New Haven Health — include Timothy's diagnoses, active medications, CGM device, care team, and the oral health assessment findings documented by Dr. Smith. The records arrive in time for Dr. Watson to review before Timothy's appointment.

**The dental encounter:** Dr. Watson conducts a **comprehensive oral evaluation** (`D0150`) and a **periodontal risk assessment (PRA)**. He finds that Timothy's gingivitis has progressed to **early-stage periodontitis** (`ICD-10: K05.21` — chronic periodontitis, localized, slight) in the three months since the well-child visit — consistent with the accelerated periodontal disease trajectory associated with poorly controlled Type 1 diabetes. Given Timothy's age and dental development, this is a clinically significant finding.

Dr. Watson's treatment plan and actions include:

- **Scaling and root planing** (`D4341` — per quadrant) to remove supragingival and subgingival plaque and calculus
- **Local delivery of chlorhexidine** (`D4381`) to reduce bacterial load at the affected periodontal sites
- **Oral hygiene education** provided by Dr. Watson's dental hygienist to both Timothy and his grandmother, including proper brushing technique, floss instruction, and age-appropriate toothpaste guidance; Timothy is sent home with a toothbrush, toothpaste, and floss

**Bidirectional summary return:** Upon completing the encounter, Dr. Watson transmits a **structured encounter summary** to two members of Timothy's medical care team:

1. **Dr. Smith** (pediatrician) — including the periodontitis diagnosis, treatment performed, and oral hygiene care plan
2. **Timothy's pediatric endocrinologist** — including the periodontitis diagnosis, the documented diabetes-periodontal relationship, chlorhexidine treatment, and a note on the bidirectional oral-systemic risk: periodontitis exacerbates glycemic dysregulation, and poor glycemic control accelerates periodontal disease progression

Both summaries are transmitted as structured FHIR data via CDex provider-to-provider push, through Connie as the routing intermediary.

Timothy's patient record — accessible through the Husky B patient application — updates to show the dental encounter as complete and surfaces the care plan from Dr. Watson.

---

## Section II: Narrative-to-Standards Mapping

| What Happens (Business Language) | Implementation Guide / Standard | Key Transaction |
|---|---|---|
| **Well-child exam with oral health assessment:** Dr. Smith conducts a pediatric oral health assessment and documents gingivitis, tobacco smoke exposure, and diabetes. | US Core / ODE (Under Development) | `Encounter` (well-child, POS 11); `Condition` (K05.00, Z77.22, E10.9); `Observation` (oral health assessment findings — tooth loss, gingivitis, pain); `Flag` (Type 1 diabetes — elevated periodontal risk). |
| **Referral created:** Dr. Smith creates a structured dental referral to a pediatric dental provider. | US Core / ODE (Under Development) | `ServiceRequest` (referral, priority: routine); `DocumentReference` wrapping oral health assessment findings; `Flag` (diabetes, elevated periodontal risk). |
| **Provider directory query:** Timothy's parents contact Benecare (referral coordination and network directory) to identify a Husky B–participating pediatric dental provider accepting new patients within 20 miles. | Da Vinci PDex / Plan-Net IG | `PractitionerRole` and `HealthcareService` queried from Connecticut Dental Health Partnership / Benecare provider directory to confirm network participation, accepting status, and proximity. |
| **Patient notification — referral sent:** Timothy's patient application (or guardian proxy application) receives notification that the referral has been created. | FHIR Subscriptions Backport IG | Subscription event triggered on `ServiceRequest` creation. |
| **Medical records transmitted to dental provider — via Connie:** New Haven Pediatric Care Center transmits Timothy's medical records to Dr. Watson's practice prior to the dental encounter, routed through Connie (Connecticut HIE). | Da Vinci CDex / US Core / Connie HIE | `Bundle` (patient summary): `Patient`, `Condition` (E10.9, K05.00, Z77.22), `MedicationRequest` (insulin lispro), `Device` (CGM, insulin pump), `CareTeam` (pediatrician, endocrinologist, dietitian), `Observation` (oral health findings); transmitted via CDex provider-to-provider push, routed through Connie FHIR endpoint. |
| **Medical records received at dental practice:** Dr. Watson reviews Timothy's full medical context — diabetes status, medications, CGM device, care team, oral health findings — before the encounter begins. | US Core / ODE (Under Development) | `Bundle` received via interim FHIR server at pediatric dental practice; surfaced in dental provider workflow prior to appointment. |
| **Comprehensive oral evaluation and periodontal risk assessment:** Dr. Watson completes a full evaluation and PRA, confirming periodontitis progression. | US Core / ODE (Under Development) | `Encounter` (in-office, POS 11); `Condition` (K05.21 — chronic periodontitis, localized, slight); `Observation` (periodontal findings per site, tooth development status); `DiagnosticReport` (PRA). |
| **Treatment performed:** Dr. Watson performs scaling and root planing and applies local chlorhexidine delivery. | US Core / ODE (Under Development) | `Procedure` (D4341 — scaling and root planing, per quadrant); `Procedure` (D4381 — local delivery of chlorhexidine); `MedicationAdministration` (chlorhexidine 2.5% chip). |
| **Oral hygiene education:** Dental hygienist provides oral hygiene education to patient and grandmother. | US Core / ODE (Under Development) | `Procedure` (D1330 — oral hygiene instructions); `Communication` (education delivered to guardian); oral hygiene supplies documented in encounter notes. |
| **Encounter summary returned to pediatrician — via Connie:** Dr. Watson transmits a structured summary to Dr. Smith at New Haven Pediatric Care Center, routed through Connie. | Da Vinci CDex / ODE (Under Development) / Connie HIE | `ClinicalImpression` (encounter summary); `Condition` (K05.21, confirmed); `Procedure` (completed); `CarePlan` (post-treatment oral hygiene, recall frequency); CDex provider-to-provider push routed through Connie to Epic FHIR endpoint at Yale New Haven Health. |
| **Encounter summary returned to endocrinologist — via Connie:** Dr. Watson transmits a structured summary to Timothy's pediatric endocrinologist, including diabetes-periodontal relationship and chlorhexidine treatment. | Da Vinci CDex / ODE (Under Development) / Connie HIE | Separate `ClinicalImpression` push to endocrinologist FHIR endpoint via Connie; includes diabetes-periodontal bidirectional risk notation; `Flag` recommending glycemic review given periodontal disease progression. |
| **Patient application updated:** Timothy's Husky B patient application (guardian proxy) shows the dental encounter complete with care plan. | FHIR Subscriptions Backport IG / US Core | Subscription event on `ServiceRequest` status change; `CarePlan` surfaced to guardian proxy application via SMART App Launch. |
| **Claims submission:** Pediatric dental practice submits 837D to Benecare for dental services rendered. | X12 837D | 837D: D0150, D4341 ×2 (quadrants), D4381, D1330; POS 11; Dr. Watson as rendering provider; Timothy's Husky B Medicaid ID on claim. |

---

## Section III: Technical Overview

This use case exercises a **medical-to-dental referral with pre-encounter medical record exchange and bidirectional encounter summary return**, spanning a pediatric medical practice (Epic/Yale New Haven Health), a Connecticut state HIE (Connie), a pediatric dental practice management system, a dental ASO (Benecare), and two receiving medical providers (pediatrician and pediatric endocrinologist). The scenario is the first in the OHIA Connectathon test dataset to route provider-to-provider clinical data exchange through a **state HIE intermediary** rather than direct endpoint-to-endpoint transmission.

The core interoperability problem this use case addresses: a pediatric dental provider is expected to treat a medically complex child — Type 1 diabetes, CGM, insulin pump, active gingivitis — but receives the patient accompanied only by grandparents with limited medical knowledge. Without structured record exchange, the dental provider begins the encounter blind. With it, the full medical context arrives before the appointment.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

### Implementation Guides

| Implementation Guide | Purpose in This Use Case |
|---|---|
| **US Core IG** | Defines FHIR profiles for all clinical data exchanged across the pediatric medical practice, pediatric dental practice, Connie HIE, and Benecare; includes pediatric-specific profiles for patient demographics, guardian relationships, and development milestones |
| **Da Vinci Clinical Data Exchange (CDex)** | Three roles: (1) **Provider-to-provider medical record push (pre-encounter)** — structured medical summary transmitted from New Haven Pediatric Care Center through Connie to Dr. Watson's practice before the dental appointment; (2) **Encounter summary return to pediatrician** — structured dental findings and care plan pushed from dental practice through Connie to Dr. Smith's Epic endpoint; (3) **Encounter summary return to endocrinologist** — separate CDex push with diabetes-periodontal clinical summary to endocrinologist FHIR endpoint |
| **Da Vinci PDex / Plan-Net IG** | Provider directory query against Benecare network directory to identify a Husky B–participating pediatric dental provider accepting new patients within 20 miles; `PractitionerRole` and `HealthcareService` queried before referral target is selected |
| **Da Vinci Payer Data Exchange (PDex)** | Enables guardian proxy application to surface Husky B coverage and benefit information; PDex patient access API retrieves `Coverage` and `InsurancePlan` at application access |
| **SMART App Launch IG** | Authorization framework enabling guardian proxy application to connect to Benecare FHIR endpoint and to surface post-encounter `CarePlan`; supports minor patient / guardian proxy authorization model |
| **FHIR Subscriptions Backport IG** | Delivers push notifications to guardian proxy application at referral creation, encounter complete, and care plan available |
| **Oral Health Data Exchange IG (ODE)** | Under development; governs structured exchange of oral health clinical data — periodontal findings, tooth development observations, CDT-coded procedures, PRA, and encounter summary — between the dental practice and the medical care team |
| **Connie Connecticut HIE** | State HIE routing intermediary for all provider-to-provider data exchange in this use case; Connie brokers the CDex push from the Epic FHIR endpoint at Yale New Haven Health to the dental practice interim FHIR server, and the return summaries from the dental practice to both medical providers; Connie's FHIR infrastructure serves as the real-world routing layer replacing direct endpoint-to-endpoint assumptions |
| **Epic Care Everywhere** | Record sharing network at New Haven Pediatric Care Center; Care Everywhere makes Timothy's clinical record accessible to Connie's FHIR query without requiring a separate data extract or portal login; the use case tests whether a Connie-mediated CDex pull from an Epic Care Everywhere–enabled endpoint can surface discrete FHIR resources rather than a PDF document |

---

### Key FHIR Resources Exercised

| FHIR Resource | Source IG / Profile | Purpose in This Use Case |
|---|---|---|
| `Patient` | US Core | Timothy's identity across New Haven Pediatric Care Center (Epic), Connie HIE, Dr. Watson's practice interim FHIR server, and Benecare; minor patient with no independent patient identifier in dental context |
| `RelatedPerson` | US Core | Guardian relationship — Timothy's parents (legal guardians) and grandparents (accompanying caregivers with limited health history knowledge); SMART App Launch proxy authorization for guardian access |
| `Coverage` | US Core / PDex | Husky B (Connecticut CHIP) — Medicaid ID, program, Benecare as dental ASO, benefit details — verified at referral creation and on claim submission |
| `InsurancePlan` | Da Vinci PDex | Benecare plan benefit structure; pediatric dental benefit covered services under Husky B |
| `Practitioner` | US Core | Dr. Laura Smith, MD (pediatrician); Dr. David Watson, DDS (pediatric dental provider); pediatric endocrinologist; dental hygienist |
| `PractitionerRole` | US Core / Plan-Net | Role context for each provider; queried in Benecare Plan-Net directory to confirm Dr. Watson's Husky B network participation and panel status |
| `CareTeam` | US Core | Timothy's full care team — pediatrician, endocrinologist, registered dietitian — transmitted with medical records bundle to dental practice |
| `Organization` | US Core / Plan-Net | New Haven Pediatric Care Center; Yale New Haven Health (Epic instance); pediatric dental practice; Benecare (dental ASO); Connie HIE; pediatric endocrinology practice |
| `Location` | US Core | New Haven Pediatric Care Center (POS 11); pediatric dental practice (POS 11); both in Connecticut |
| `Encounter` | US Core | Well-child exam (New Haven Pediatric Care Center, Dr. Smith, POS 11); dental encounter (pediatric dental practice, Dr. Watson, POS 11) |
| `Condition` | US Core / ODE | E10.9 (Type 1 diabetes, without complications); K05.00 (acute gingivitis, plaque-induced — documented at well-child visit); K05.21 (chronic periodontitis, localized, slight — confirmed at dental encounter); Z77.22 (tobacco smoke exposure) |
| `Flag` | US Core | Type 1 diabetes — elevated periodontal risk flag created by Dr. Smith and transmitted with referral and medical records bundle to dental practice; post-encounter flag from Dr. Watson to endocrinologist noting periodontitis-glycemic dysregulation relationship |
| `Observation` | US Core / ODE | Oral health assessment findings from well-child visit (gingivitis, tooth loss, pain); periodontal findings per site from dental examination; CGM device readings (if available — surfaced from Epic via Care Everywhere); tooth development status (primary vs. permanent tooth eruption) |
| `MedicationRequest` | US Core | Insulin lispro — prescribed medication transmitted in medical records bundle to dental practice; relevant to dental treatment planning (healing risk, infection risk) |
| `Device` | US Core | CGM device and insulin pump — documented in medical records bundle; contextualizes diabetes management status for dental provider |
| `ServiceRequest` | US Core / ODE | Structured referral from Dr. Smith to pediatric dental practice; status lifecycle `active` → `completed` |
| `DocumentReference` | US Core | Oral health assessment findings from well-child visit, transmitted as supporting documentation with referral |
| `DiagnosticReport` | US Core / ODE | Periodontal risk assessment (PRA) completed by Dr. Watson; structured findings supporting periodontitis diagnosis |
| `Procedure` | US Core / ODE | D0150 (comprehensive oral evaluation); D4341 (scaling and root planing, per quadrant ×2); D4381 (local delivery of chlorhexidine); D1330 (oral hygiene instructions) |
| `MedicationAdministration` | US Core | Chlorhexidine 2.5% chip — local delivery at affected periodontal sites; documented in encounter and transmitted in summary to medical providers |
| `ClinicalImpression` | ODE | (1) Structured encounter summary from dental practice to pediatrician — periodontitis diagnosis, treatment, care plan; (2) Separate structured summary to endocrinologist — periodontitis diagnosis, diabetes-periodontal relationship, recommendation for glycemic review |
| `CarePlan` | US Core | Post-treatment plan including oral hygiene regimen, recall frequency, permanent restoration follow-up; surfaced to guardian proxy application |
| `Appointment` / `AppointmentResponse` | US Core | Dental appointment created by practice; response surfaced to guardian proxy application |
| `Task` | CDex | Tracks the open referral as an actionable item at the dental practice; tracks each outbound summary as a task until delivery confirmed by Connie routing layer |
| `Subscription` / `SubscriptionStatus` | FHIR Subscriptions Backport IG | Push notifications to guardian proxy application at referral creation, appointment confirmation, encounter complete |
| `Bundle` | FHIR Core | Pre-encounter medical records bundle (Patient + Condition + MedicationRequest + Device + CareTeam + Observation + Flag); encounter summary bundles to each medical provider |
| `AuditEvent` | US Core | Cross-organizational data access logging; Connie HIE routing events logged for provenance and compliance |
| `Provenance` | US Core | Chain of custody for clinical data across Epic, Connie, dental practice, and receiving medical providers |

---

### Cross-Cutting Test Objectives

1. **State HIE as a routing intermediary for dental record exchange** — Connie brokers all provider-to-provider data exchange in this use case. This is the first OHIA Connectathon test of a state HIE intermediary model: Connie receives the CDex push from the Epic endpoint at Yale New Haven Health, routes it to the dental practice interim FHIR server, and routes return summaries to two separate medical provider endpoints. The test validates whether a state HIE can serve as a practical dental interoperability routing layer without requiring direct endpoint-to-endpoint configuration between every pair of participating organizations.

2. **Epic Care Everywhere as a discrete FHIR resource source** — Care Everywhere has historically surfaced clinical documents (CCDs, PDFs) rather than discrete FHIR resources. This use case tests whether a Connie-mediated CDex pull from a Care Everywhere–enabled Epic endpoint can return discrete FHIR resources — `Condition`, `MedicationRequest`, `Device`, `Observation` — that a dental practice can act on at point of care, rather than a PDF that must be manually reviewed.

3. **Minor patient identity and guardian proxy authorization** — Timothy is a minor with no independent patient identifier in the dental context. US Core `Patient` and `RelatedPerson` resources must correctly express the guardian relationship. SMART App Launch must support guardian proxy authorization for the parent/caregiver application without requiring Timothy to authenticate independently. This is the first OHIA Connectathon use case to test minor patient identity matching across unaffiliated systems.

4. **Pre-encounter medical record delivery as the primary test objective** — Unlike prior use cases where records are exchanged concurrent with or following a referral, this use case explicitly requires that the medical records bundle arrive at the dental practice **before** the appointment — in time for the dental provider to review and incorporate into treatment planning. The test validates whether CDex + Connie can support a pre-encounter delivery timeline for routine (non-urgent) referrals with a multi-week appointment lead time.

5. **`Device` resource for chronic disease management devices** — The CGM and insulin pump are clinically relevant to dental treatment planning (healing risk, infection risk, anesthetic considerations). This use case tests whether `Device` resources for patient-worn chronic disease management devices can be included in a medical records bundle transmitted to a dental provider via CDex.

6. **Bidirectional summary return to two medical providers simultaneously** — Dr. Watson transmits separate `ClinicalImpression` bundles to two distinct medical providers — the pediatrician and the endocrinologist — via Connie. The test validates whether a dental practice can initiate two simultaneous CDex provider-to-provider pushes to two different organizations through a single HIE routing layer, and whether Connie can route them to the correct endpoints.

7. **Diabetes-periodontal clinical relationship as structured data** — The oral-systemic relationship between Type 1 diabetes and accelerated periodontal disease is the clinical core of this use case. The test validates whether this relationship can be expressed as structured FHIR data — a `Flag` resource to the endocrinologist, a `Condition` reference linking K05.21 to E10.9 as a contributing condition — rather than a clinical note paragraph that cannot be acted on by a receiving system.

8. **`MedicationAdministration` for in-office dental treatment** — Local delivery of chlorhexidine is an in-office dental medication administration that must be communicated to both the pediatrician and the endocrinologist (antibiotic stewardship context; clinical coordination). This use case tests whether `MedicationAdministration` resources from a dental encounter can be transmitted in a CDex summary push to medical providers.

9. **Connecticut Dental Health Partnership / Benecare Plan-Net provider directory** — The provider directory query to identify a Husky B–participating pediatric dental provider accepting new patients within 20 miles tests Plan-Net `PractitionerRole` and `HealthcareService` in a Connecticut CHIP / Medicaid context — a coverage context not previously exercised in OHIA Connectathon use cases. Benecare provides the network directory and referral coordination layer; Connecticut Dental Health Partnership is the dental plan administrator and claims adjudicator under the MCO contract.

10. **ODE IG validation for pediatric periodontitis** — This use case exercises ODE profiles in a pediatric context: mixed dentition (primary and permanent teeth simultaneously present), tooth development observations, and periodontal findings in a patient population not typically associated with periodontitis — validating that ODE's oral health profiles can represent the full clinical range of dental findings, including those driven by systemic disease in young patients.

---

## Section IV: EDI Transactions

Timothy's dental services are covered under **Husky B** (Connecticut CHIP). The benefit structure in this use case reflects a three-tier administration model: Connecticut DSS (state Medicaid program sponsor) → **Connecticut Medicaid MCO** (managed care organization — specific MCO to be confirmed against current Husky B enrollment data) → **Connecticut Dental Health Partnership** (dental plan administrator) → **Benecare** (referral coordination and network directory services). Claims are submitted to and adjudicated by Connecticut Dental Health Partnership under the MCO contract, not by Benecare directly. Connecticut Medicaid fee schedule rates apply.

### EDI Transactions in Scope

| X12 Transaction | Trigger | Scope Note |
|---|---|---|
| **270 / 271** — Eligibility & Benefit Inquiry / Response | New Haven Pediatric Care Center verifies Timothy's Husky B dental eligibility at referral creation; Dr. Watson's practice verifies at check-in | Queries Connecticut Dental Health Partnership dental benefit via MCO; confirms active Husky B enrollment, covered pediatric dental services, and annual benefit limits |
| **837D** — Dental Claim (Pediatric Dental Practice) | Dr. Watson's practice submits claim to Connecticut Dental Health Partnership (via MCO) for all dental services rendered | CDT D0150 (comprehensive oral evaluation); D4341 ×2 (scaling and root planing, two quadrants); D4381 (local delivery of chlorhexidine); D1330 (oral hygiene instructions); POS 11; Dr. Watson as rendering provider; Timothy's Husky B Medicaid ID on claim |
| **835** — Remittance Advice | Connecticut Dental Health Partnership adjudicates and returns remittance | Connecticut Medicaid / Husky B fee schedule rates; claim adjustment reason codes; any benefit limitation denials surfaced as named test findings |

> **Note on 278:** No prior authorization is required for the procedures in this encounter under Husky B pediatric dental benefit design. The X12 278 transaction is not in scope for this use case. If D4341 (scaling and root planing) requires PA under the applicable Husky B benefit year — benefit design varies — this use case flags that as an open test finding.

> **Benecare role clarification:** Benecare provides referral coordination and network directory services within the Connecticut Medicaid dental ecosystem. Benecare is not the claims payer and does not adjudicate 837D claims. The Plan-Net provider directory query in this use case is directed at the Connecticut Dental Health Partnership / Benecare network directory; the 837D claim is routed to Connecticut Dental Health Partnership.

> **Medical billing note:** No medical benefit claim is in scope for this use case. All services are billed under the dental benefit. The pediatric oral health assessment performed by Dr. Smith at the well-child visit is billed under the medical benefit (CPT 99461 or equivalent well-child code with oral health component) by New Haven Pediatric Care Center; that transaction is out of scope for this dental Connectathon use case.

### CDT Codes in Scope

| CDT Code | Description | Provider | Husky B Coverage Note |
|---|---|---|---|
| `D0150` | Comprehensive oral evaluation — new or established patient | Pediatric dental practice / Dr. Watson | Covered; once per provider per benefit year |
| `D1330` | Oral hygiene instructions | Pediatric dental practice / Dental hygienist | Covered; confirm frequency limits under Husky B |
| `D4341` | Periodontal scaling and root planing — four or more teeth per quadrant | Pediatric dental practice / Dr. Watson | Covered; unusual for pediatric patient — medical necessity documentation required; flagged as open test finding |
| `D4381` | Localized delivery of antimicrobial agents — per tooth | Pediatric dental practice / Dr. Watson | ⚠️ Coverage uncertain under Husky B pediatric benefit — named open test finding |

### LOINC Codes in Scope

| LOINC Code | Description | FHIR Resource | Use in This Case |
|---|---|---|---|
| `32485-7` | Comprehensive oral examination | `DiagnosticReport` | D0150 comprehensive evaluation — Dr. Watson |
| `72166-2` | Tobacco smoking status | `Observation` | Tobacco smoke exposure documented at well-child visit (Z77.22) |
| `4548-4` | Hemoglobin A1c | `Observation` | HbA1c — surfaced from Epic via Care Everywhere if available; supports diabetes-periodontal clinical context |
| `41995-2` | Blood glucose monitoring device panel | `Observation` | CGM data — surfaced from Epic if available; contextualizes glycemic control for dental provider |
| *(No LOINC code established)* | Periodontal risk assessment score | `Observation` / `DiagnosticReport` | PRA score — **gap: no established LOINC code for a structured PRA; named ODE IG test objective** |

> **LOINC gap:** A structured periodontal risk assessment (PRA) score — a tool routinely used in pediatric dental practice to quantify disease risk — has no established LOINC code. This use case surfaces that gap as an action item for the ODE IG development process.

---

## Appendix: Data

### 1. Patient Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Name** | Timothy Jones | Given: Timothy; Family: Jones |
| **Date of Birth** | 2019-05-05 | Age: 6 |
| **Sex** | Male | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **Epic MRN (Yale New Haven Health)** | `YNHH-MRN-20190505-TJ` | System: `https://yalenewhavenhealth.org/fhir/mrn` |
| **Dental Practice MRN** | `PDENT-CT-2026-0028` | System: `https://pedsdental.example.org/fhir/mrn` |
| **Connecticut Husky B Medicaid ID** | `CT-MCD-HB-0082341` | System: `http://ct.medicaid.gov/beneficiary` |
| **Telecom (Guardian phone)** | (203) 555-0174 | Use: Mobile — parent/guardian |
| **Telecom (Guardian email)** | jones.family.ct@example.com | Use: Home — parent/guardian |
| **Address** | 214 Elm Street, Apt 4, New Haven, CT 06510 | City: New Haven; State: CT; ZIP: 06510 |
| **Language** | English | Preferred language |
| **Active** | True | Patient record is active |

#### Related Person (Guardian)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Relationship** | Parent / Legal Guardian | `http://terminology.hl7.org/CodeSystem/v3-RoleCode` — GUARD |
| **Name** | Jones (parent — name withheld per minor patient convention) | Guardian of record |
| **SMART App Launch Proxy** | Guardian proxy authorization active | Minor patient; parents authorized for patient application access |

#### Related Person (Accompanying Caregiver — Non-Guardian)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Relationship** | Grandparent — accompanying caregiver | `GRNDP` — grandparent role code |
| **Note** | Accompanying caregiver at dental appointment; limited knowledge of patient medical history beyond Type 1 diabetes diagnosis and pediatrician identity | Drives the clinical need for pre-encounter structured medical record exchange |

---

### 2. Coverage Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Program** | Husky B — Connecticut CHIP | Connecticut Children's Health Insurance Program |
| **State Program Sponsor** | Connecticut DSS | Department of Social Services — state Medicaid authority |
| **MCO** | Connecticut Medicaid MCO (Synthetic) | Managed care organization — confirm against current Husky B enrollment data |
| **Dental Plan Administrator** | Connecticut Dental Health Partnership | Dental benefit plan administrator under MCO contract |
| **Referral Coordination / Network Directory** | Benecare | Referral coordination and network directory services; not the claims payer |
| **Medicaid ID** | CT-MCD-HB-0082341 | Connecticut CHIP beneficiary ID |
| **Coverage Period** | 2026-01-01 – 2026-12-31 | Enrollment year |
| **Status** | Active | Coverage confirmed |
| **Dental Network** | Connecticut Dental Health Partnership / Benecare provider network | In-network dental providers |
| **Annual Dental Maximum** | Per Connecticut Medicaid fee schedule | Confirm current Husky B benefit year |
| **Preventive / Diagnostic** | Covered | D0150, D1330 |
| **Periodontal Treatment** | Covered with medical necessity documentation | D4341 — unusual for pediatric patient; medical necessity required |
| **Antimicrobial Agents** | Uncertain | D4381 — named open test finding |
| **Claims Payer EDI ID** | CT-CDHP-EDI | Connecticut Dental Health Partnership — HIPAA X12 claims routing (synthetic) |
| **Claims Payer FHIR Endpoint** | `https://ctdentalpartnership.example.org/fhir/r4` | Synthetic FHIR API — Connecticut Dental Health Partnership |
| **Benecare FHIR Endpoint** | `https://benecare.example.org/fhir/r4` | Synthetic FHIR API — provider directory / referral coordination only |

---

### 3. Organization Resource Data

#### New Haven Pediatric Care Center

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1437823056 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | New Haven Pediatric Care Center | Medical practice |
| **Address** | 20 York Street, New Haven, CT 06510 | New Haven, Connecticut |
| **Phone** | (203) 555-0220 | Synthetic |
| **Type** | Pediatric Medical Practice | Organization type |
| **EHR System** | Epic — Yale New Haven Health instance | Care Everywhere enabled |
| **FHIR Endpoint** | `https://epicfhir.yalenewhavenhealth.org/fhir/r4` | Yale New Haven Health Epic FHIR endpoint (synthetic) |
| **NPI Taxonomy Code** | 208000000X | Pediatrics |

#### Pediatric Dental Practice

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1578293047 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | Pediatric Dental Practice — New Haven (Synthetic) | Test data label |
| **Address** | 450 Congress Avenue, New Haven, CT 06519 | Synthetic practice location |
| **Phone** | (203) 555-0188 | Synthetic |
| **Type** | Pediatric Dental Practice | Organization type |
| **Specialty** | Pediatric Dentistry | Primary services |
| **Practice Management System** | Dental PMS with interim FHIR server | Architecture pattern |
| **FHIR Endpoint** | `https://pedsdental.example.org/fhir/r4` | Interim FHIR server |
| **NPI Taxonomy Code** | 1223P0221X | Pediatric dentist |
| **Husky B Participation** | Active — Connecticut Dental Health Partnership / Benecare network | Confirmed via Plan-Net query |
| **Panel Status** | Accepting new patients | Confirmed via Plan-Net `HealthcareService` query |

#### Connie (Connecticut Health Information Exchange)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | Connie — Connecticut Health Information Exchange | State HIE |
| **Address** | Hartford, Connecticut | State HIE headquarters |
| **Type** | State Health Information Exchange | HIE type |
| **Role in Use Case** | FHIR routing intermediary for all provider-to-provider data exchange | Routes CDex pushes between Epic, dental practice, and endocrinologist |
| **FHIR Endpoint** | `https://conniect.org/fhir/r4` | Connie FHIR routing endpoint (synthetic) |
| **OHIA Role** | Named OHIA member organization | Sector: State HIE |

#### Connecticut Dental Health Partnership

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | Connecticut Dental Health Partnership | Dental plan administrator |
| **Type** | Dental Plan Administrator | Organization type |
| **Program** | Connecticut Medicaid / Husky B — dental benefit | Program administered |
| **Role in Use Case** | Dental plan administrator; claims adjudicator; 837D recipient | Claims submitted to Connecticut Dental Health Partnership via MCO contract |
| **Claims EDI ID** | CT-CDHP-EDI | X12 claims routing (synthetic) |
| **FHIR Endpoint** | `https://ctdentalpartnership.example.org/fhir/r4` | Synthetic FHIR API |

#### Benecare

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | Benecare | Referral coordination and network directory services |
| **Type** | Dental Referral Coordination / Network Directory | Organization type |
| **Program** | Connecticut Medicaid / Husky B | Programs supported |
| **Role in Use Case** | Provider directory queries (Plan-Net); referral coordination; network identification | Not the claims payer; does not adjudicate 837D claims |
| **FHIR Endpoint** | `https://benecare.example.org/fhir/r4` | Synthetic FHIR API — provider directory only |

#### Connecticut Medicaid MCO (Synthetic)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | Connecticut Medicaid MCO (Synthetic) | Managed care organization — specific MCO to be confirmed against current Husky B enrollment data |
| **Type** | Medicaid Managed Care Organization | Organization type |
| **Program** | Connecticut HUSKY B | Medicaid managed care program |
| **Role in Use Case** | MCO contract holder; intermediary between DSS and Connecticut Dental Health Partnership | Claims flow: dental practice → Connecticut Dental Health Partnership under MCO contract |

#### Pediatric Endocrinology Practice

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1689203741 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | Pediatric Endocrinology Practice — Connecticut (Synthetic) | Test data label |
| **Type** | Pediatric Specialty Practice | Organization type |
| **Specialty** | Pediatric Endocrinology | Specialty |
| **FHIR Endpoint** | `https://pedendo.example.org/fhir/r4` | Synthetic FHIR endpoint |
| **NPI Taxonomy Code** | 2080P0202X | Pediatric Endocrinology |

---

### 4. Practitioner Resource Data

#### Dr. Laura Smith, MD — Pediatrician

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1538472091 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Laura Ann Smith, MD | Given: Laura; Family: Smith |
| **Qualification** | MD — Doctor of Medicine | Medical degree |
| **License Number** | CT-MD-047821 | Connecticut medical license (synthetic) |
| **Specialty Code (Taxonomy)** | 208000000X | Pediatrics |
| **Organization** | New Haven Pediatric Care Center | Employment |
| **EHR** | Epic — Yale New Haven Health | Care Everywhere enabled |
| **Place of Service** | 11 — Office | In-office setting |
| **Role in Use Case** | Originating referring provider; recipient of dental encounter summary | Oral health assessment at well-child visit; referral creation; receives summary from Dr. Watson |

#### Dr. David Watson, DDS — Pediatric Dentist

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1649203058 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | David Michael Watson, DDS | Given: David; Family: Watson |
| **Qualification** | DDS — Doctor of Dental Surgery | Dental degree |
| **License Number** | CT-DDS-052917 | Connecticut dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223P0221X | Pediatric dentist |
| **Organization** | Pediatric Dental Practice — New Haven | Employment |
| **Husky B Participation** | Active — Connecticut Dental Health Partnership / Benecare network | Confirmed via Plan-Net |
| **Place of Service** | 11 — Office | In-office setting |
| **Role in Use Case** | Receiving dental provider; sender of bidirectional encounter summaries | Dental evaluation, PRA, treatment; transmits summaries to pediatrician and endocrinologist |

#### Pediatric Endocrinologist (Unnamed — Care Team Member)

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1729384102 | `http://hl7.org/fhir/sid/us-npi` |
| **Qualification** | MD — Pediatric Endocrinology | Specialty |
| **Specialty Code (Taxonomy)** | 2080P0202X | Pediatric Endocrinology |
| **Organization** | Pediatric Endocrinology Practice — Connecticut | Employment |
| **Role in Use Case** | Secondary recipient of dental encounter summary | Receives periodontitis diagnosis and diabetes-periodontal relationship summary from Dr. Watson |

#### Dental Hygienist (Unnamed — Dr. Watson's Practice)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Qualification** | RDH — Registered Dental Hygienist | Credential |
| **Specialty Code (Taxonomy)** | 124Q00000X | Dental hygienist |
| **Organization** | Pediatric Dental Practice — New Haven | Employment |
| **Role in Use Case** | Oral hygiene education delivery to patient and grandmother | D1330 — oral hygiene instructions |

---

### 5. Workflow & Service Data

#### ServiceRequest (Referral — New Haven Pediatric Care Center to Pediatric Dental Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Referral fulfilled |
| **Intent** | Order | Clinical order |
| **Category** | Consultation / Referral | Type |
| **Priority** | Routine | Non-urgent; three-month appointment lead time |
| **Code** | Pediatric dental evaluation and treatment — gingivitis with diabetes-related elevated periodontitis risk | Referral reason |
| **Subject** | Timothy Jones | Patient reference |
| **Requester** | Dr. Laura Smith, MD | Originating pediatric provider |
| **Performer** | Dr. David Watson, DDS | Receiving pediatric dental provider |
| **Reason Code** | K05.00 (acute gingivitis, plaque-induced); E10.9 (Type 1 diabetes — elevated periodontal risk) | ICD-10 presenting diagnoses |
| **Supporting Info** | `Flag`: E10.9 (Type 1 diabetes — elevated infection, healing, and periodontal risk); `MedicationRequest`: insulin lispro; `Device`: CGM, insulin pump | Medical context |
| **Ordered Date** | 2026-02-28 | Well-child visit date |
| **Occurrence DateTime** | 2026-05-28 | Target dental appointment (three months post-referral) |
| **Description** | Six-year-old male with Type 1 diabetes (E10.9), poorly controlled at time of referral, presenting with acute gingivitis (K05.00) at well-child exam. Household tobacco smoke exposure (Z77.22). No dental home established. Diabetes significantly elevates risk of rapid periodontitis progression. Recommend comprehensive pediatric dental evaluation and periodontal risk assessment. Medical records including diabetes management status, medications, devices, and care team to be transmitted via Connie prior to appointment. Patient will be accompanied by grandparents at dental visit — limited caregiver medical history knowledge reinforces need for pre-encounter record delivery. | Referral payload |

#### Pre-Encounter Medical Records Bundle (New Haven Pediatric Care Center → Connie → Pediatric Dental Practice)

| Bundle Component | FHIR Resource | Content |
|---|---|---|
| Patient demographics | `Patient` | Timothy Jones — DOB, identifiers, guardian relationship |
| Diagnoses | `Condition` | E10.9 (Type 1 diabetes); K05.00 (acute gingivitis); Z77.22 (tobacco smoke exposure) |
| Medications | `MedicationRequest` | Insulin lispro — dose, frequency, prescribing provider |
| Devices | `Device` | CGM (model, active status); insulin pump (model, start date) |
| Care team | `CareTeam` | Dr. Smith (pediatrician); endocrinologist (name + NPI + organization); registered dietitian |
| Oral health findings | `Observation` | Gingivitis finding from well-child assessment; tooth loss (two lower central incisors); pain complaint; eruption status |
| Diabetes risk flag | `Flag` | E10.9 — elevated periodontal risk; healing and infection risk; glycemic control context |
| Recent encounter | `Encounter` | Well-child visit 2026-02-28 — summary |

#### Condition (Confirmed — Dental Encounter)

| FHIR Element | Value | Notes |
|---|---|---|
| **Clinical Status** | Active | Condition active |
| **Verification Status** | Confirmed | Confirmed by clinical examination and PRA |
| **Code** | K05.21 — Chronic periodontitis, localized, slight | ICD-10 confirmed dental diagnosis |
| **Body Site** | Lower anterior sextant; primary dentition sites | Affected periodontal sites |
| **Asserter** | Dr. David Watson, DDS | Confirming dental provider |
| **Onset** | Estimated — gingivitis present at 2026-02-28; periodontitis confirmed 2026-05-28 | Progression within three-month referral window |
| **Note** | Periodontal disease progression consistent with accelerated trajectory in poorly controlled Type 1 diabetes. Mixed dentition — primary and partially erupted permanent teeth present. PRA completed and documented. | Clinical note |

#### Procedure (Scaling and Root Planing)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Code** | D4341 (CDT) | Periodontal scaling and root planing — four or more teeth per quadrant |
| **Subject** | Timothy Jones | Patient reference |
| **Performer** | Dr. David Watson, DDS | Performing dental provider |
| **Performed DateTime** | 2026-05-28 | Date of procedure |
| **Body Site** | Two quadrants (lower anterior; upper anterior) | Affected periodontal quadrants |
| **Reason Reference** | K05.21 (chronic periodontitis, localized, slight); E10.9 (Type 1 diabetes — elevated periodontal risk) | Linked diagnoses |
| **Note** | Supragingival and subgingival scaling and root planing completed in two quadrants. Chlorhexidine chip placed at affected sites following SRP. Patient tolerance good. | Operative note |

#### Procedure (Local Antimicrobial Delivery)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Procedure performed |
| **Code** | D4381 (CDT) | Localized delivery of antimicrobial agents — per tooth |
| **Subject** | Timothy Jones | Patient reference |
| **Performer** | Dr. David Watson, DDS | Performing dental provider |
| **Performed DateTime** | 2026-05-28 | Date of procedure |
| **Note** | Chlorhexidine 2.5% chip placed at affected periodontal sites post-SRP to reduce bacterial load. Coverage under Husky B pediatric benefit flagged as open test finding. | Operative and billing note |

#### MedicationAdministration (Chlorhexidine — In-Office)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Administration complete |
| **Medication** | Chlorhexidine gluconate 2.5% chip | Antimicrobial periodontal chip |
| **Subject** | Timothy Jones | Patient reference |
| **Performer** | Dr. David Watson, DDS | Administering provider |
| **Effective DateTime** | 2026-05-28 | Date of administration |
| **Dosage** | Per periodontal site — number of chips documented in operative note | Site-specific |
| **Reason Reference** | K05.21 (chronic periodontitis); E10.9 (diabetes — elevated bacterial risk) | Clinical indication |
| **Note** | Transmitted to pediatrician and endocrinologist in encounter summary for antibiotic stewardship awareness and care coordination. | Coordination note |

#### ClinicalImpression (Encounter Summary — to Pediatrician, via Connie)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Summary complete |
| **Date** | 2026-05-28 | Date of summary |
| **Assessor** | Dr. David Watson, DDS | Dental provider |
| **Recipient** | Dr. Laura Smith, MD — New Haven Pediatric Care Center | Via Connie routing |
| **Summary** | Timothy Jones seen 2026-05-28 per referral from New Haven Pediatric Care Center. Comprehensive oral evaluation and periodontal risk assessment completed. Gingivitis has progressed to early-stage chronic periodontitis (K05.21), localized, slight — consistent with accelerated periodontitis trajectory in Type 1 diabetes. Scaling and root planing performed in two quadrants (D4341 ×2). Chlorhexidine chip placed at affected sites (D4381). Oral hygiene education provided to patient and grandmother (D1330); toothbrush, toothpaste, and floss dispensed. Six-month recall recommended. Permanent restoration of partially erupted lower central incisor to be monitored at recall. | Encounter summary |
| **Recommendations** | 1. Six-month dental recall with periodontal reassessment; 2. Reinforce oral hygiene at medical visits; 3. Periodontal disease and glycemic control are bidirectionally linked — coordination with endocrinologist recommended | Care plan |

#### ClinicalImpression (Encounter Summary — to Endocrinologist, via Connie)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Summary complete |
| **Date** | 2026-05-28 | Date of summary |
| **Assessor** | Dr. David Watson, DDS | Dental provider |
| **Recipient** | Pediatric Endocrinologist — Connecticut | Via Connie routing |
| **Summary** | Timothy Jones, six-year-old male with Type 1 diabetes (E10.9), seen 2026-05-28 for dental evaluation. Chronic periodontitis (K05.21), localized, slight, confirmed. Periodontal disease progression accelerated by poorly controlled glycemia — this relationship is bidirectional: periodontitis also exacerbates glycemic dysregulation and may complicate insulin management. Scaling and root planing performed (D4341 ×2). Chlorhexidine 2.5% chip placed at affected periodontal sites (D4381). Most recent HbA1c requested from chart if available — not available in records received. Recommend glycemic review given periodontal disease burden in the context of ongoing diabetes management. | Encounter summary |
| **Flag Transmitted** | Periodontitis-glycemic dysregulation risk — recommend HbA1c review and diabetes management reassessment | Diabetes-oral health clinical advisory |
| **Recommendations** | 1. Review HbA1c trend in context of periodontitis diagnosis; 2. Advise family on oral-systemic connection — improved glycemic control supports periodontal healing; 3. Coordinate recall with dental provider at six months | Clinical advisory |

---

### 6. Clinical Codes & Mappings

#### ICD-10 Diagnosis Codes

| Code | Description | Application |
|---|---|---|
| E10.9 | Type 1 diabetes mellitus, without complications | Systemic comorbidity; driver of elevated periodontal risk; transmitted to dental provider in pre-encounter medical bundle |
| K05.00 | Acute gingivitis, plaque-induced | Documented at well-child visit by Dr. Smith; transmitted with referral |
| K05.21 | Chronic periodontitis, localized, slight | Confirmed at dental encounter by Dr. Watson; transmitted in bidirectional summaries |
| Z77.22 | Contact with and (suspected) exposure to tobacco smoke | Environmental risk factor documented at well-child visit; transmitted with referral |

#### SNOMED CT Codes

| SNOMED Code | Description | Application |
|---|---|---|
| 73211009 | Diabetes mellitus (disorder) | Systemic comorbidity reference |
| 66383009 | Gingivitis (disorder) | Pre-existing condition at referral |
| 41565005 | Periodontitis (disorder) | Confirmed dental diagnosis |
| 418715001 | Periodontal risk assessment | PRA procedure reference |

#### CDT Codes in Scope

| Code | Description | Provider | Coverage Note |
|---|---|---|---|
| `D0150` | Comprehensive oral evaluation — new or established patient | Dr. Watson | Covered under Husky B |
| `D1330` | Oral hygiene instructions | Dental hygienist | Covered; confirm frequency limits |
| `D4341` | Periodontal scaling and root planing — four or more teeth per quadrant | Dr. Watson | Covered; medical necessity documentation required for pediatric patient |
| `D4381` | Localized delivery of antimicrobial agents — per tooth | Dr. Watson | ⚠️ Open test finding under Husky B |

#### LOINC Codes

| LOINC | Description | FHIR Resource | Status |
|---|---|---|---|
| `72166-2` | Tobacco smoking status | `Observation` | Standard |
| `4548-4` | Hemoglobin A1c | `Observation` | Standard; surfaced from Epic if available |
| `41995-2` | Blood glucose monitoring device panel | `Observation` | Standard; CGM data if available |
| `32485-7` | Comprehensive oral examination | `DiagnosticReport` | Standard |
| *[NO CODE]* | Periodontal risk assessment score | `Observation` / `DiagnosticReport` | **GAP: No established LOINC code — named ODE IG test objective** |

---

### 7. Timeline & Dates

#### Service Timeline

| Event | Date | Actor | System |
|---|---|---|---|
| **Type 1 diabetes diagnosed (ED visit)** | 2025-02-28 | ED team | Hospital EHR |
| **Insulin pump started** | ~2025-12-01 | Endocrinologist | Endocrinology EHR |
| **Well-child exam — oral health assessment** | 2026-02-28 | Dr. Smith | Epic — Yale New Haven Health |
| **Gingivitis documented; referral created** | 2026-02-28 | Dr. Smith | Epic → ServiceRequest |
| **Guardian contacts Benecare; Plan-Net query** | 2026-02-28 | Timothy's parents | Benecare Plan-Net FHIR API |
| **Appointment scheduled with Dr. Watson** | ~2026-03-05 | Practice staff | Dental PMS |
| **Medical records bundle transmitted via Connie** | 2026-05-21 | New Haven Pediatric Care Center | Epic FHIR → Connie → Interim FHIR server |
| **Medical records received at dental practice** | 2026-05-21 | Dental practice system | Interim FHIR server |
| **Dental encounter — evaluation, SRP, chlorhexidine, OHE** | 2026-05-28 | Dr. Watson / Hygienist | Dental PMS |
| **Encounter summary transmitted to Dr. Smith — via Connie** | 2026-05-28 | Dr. Watson | CDex → Connie → Epic FHIR (Yale New Haven Health) |
| **Encounter summary transmitted to endocrinologist — via Connie** | 2026-05-28 | Dr. Watson | CDex → Connie → Endocrinology FHIR endpoint |
| **Guardian proxy application updated — encounter complete** | 2026-05-28 | Patient application | FHIR Subscription event |
| **837D submitted to Connecticut Dental Health Partnership** | 2026-05-29 | Dental practice billing | D0150, D4341 ×2, D4381, D1330 → Connecticut Dental Health Partnership EDI (via MCO) |

#### Key Timeline Constraints

| Constraint | Target | Rationale |
|---|---|---|
| **Pre-encounter record delivery** | At least 7 days before dental appointment | Dental provider review and treatment planning before encounter |
| **Appointment lead time** | Three months from referral | Reflects real-world Husky B pediatric dental access — an access gap this use case is designed to surface |
| **Encounter summary return — pediatrician** | Same day as dental encounter | Enables Dr. Smith to act on periodontitis diagnosis at next medical visit |
| **Encounter summary return — endocrinologist** | Same day as dental encounter | Enables glycemic review in context of periodontal disease burden |

#### Key Access Gap Surfaced by This Use Case

> The three-month gap between referral creation (February 28) and available dental appointment (May 28) reflects a real access constraint in Connecticut's Husky B pediatric dental network — a finding that is itself clinically significant. In a child with poorly controlled Type 1 diabetes, a three-month delay from gingivitis identification to dental treatment is long enough for gingivitis to progress to periodontitis — which is precisely what occurred in this use case. The access gap is not a test artifact; it is the clinical event that this use case is designed to make visible and measurable through structured data.

---

*This dataset is a test and validation vehicle for the Oral Health Data Exchange (ODE) Implementation Guide, developed under HL7 and sponsored by the PIE Work Group (PSS-2714). It is intended for use in connectathon and interoperability testing environments only. oralhealthalliance.net*
