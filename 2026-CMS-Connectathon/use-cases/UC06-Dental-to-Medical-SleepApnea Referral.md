# CMS Connectathon — Dental Interoperability Test Dataset
## Use Case: AI-Assisted OSA Screening at a Dental Visit → Sleep Medicine Referral → Oral Appliance Therapy
### Dental Practice as a Health Screening Entry Point | Medical Benefit Billing via DME | Ohio

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
  - [Coding in Scope](#coding-in-scope)
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

This use case models a **dental-to-medical referral originating from an AI-assisted oral health screening** at a routine dental visit. It is the first OHIA Connectathon use case to exercise:

- **A dental practice as a health screening entry point** for a systemic condition — obstructive sleep apnea (OSA) — that is typically identified only after years of symptoms and specialist referral friction
- **AI-assisted facial scan screening** as the triggering clinical event, generating a structured risk score that initiates a FHIR-based referral workflow
- **Dental-to-medical referral** — the inverse of the medical-to-dental referral pattern tested in prior use cases; the dental provider is the originator, the sleep medicine physician is the receiver
- **Cross-benefit billing**: the dental practice performs the screening; the oral appliance is billed under the **medical benefit as Durable Medical Equipment (DME)** using HCPCS code E0486 — not under the dental benefit — requiring the dental provider to be enrolled as a DME supplier and to transmit clinical documentation to the medical payer
- **Structured bidirectional summary return from sleep medicine to the dental practice**, enabling the dental provider to monitor the patient's oral appliance treatment, appliance fit, and follow-up status as part of ongoing dental care

This use case advances the **Integrate** and **Connect** strategic priorities of the Oral Health Interoperability Alliance. It demonstrates that the dental visit — one of the most frequent touchpoints in the healthcare system — can serve as a structured, standards-based gateway to identifying and routing patients with undiagnosed systemic conditions.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

## Section I: Business Overview

**Robert Vasquez** is a 47-year-old male (DOB: 08/22/1978) presenting for a **routine dental cleaning and examination** at a general dental practice in Columbus, Ohio. Robert has commercial medical insurance through his employer and a separate commercial dental plan. He has no established relationship with a sleep medicine provider and has never been evaluated for sleep apnea. His wife has commented on his snoring for years. He reports daytime fatigue but has attributed it to work stress.

**Dr. Christine Lee, DDS**, the treating general dental provider, uses an **AI-powered OSA screening platform** integrated into the dental practice workflow. As part of the intake process, Robert completes a brief digital questionnaire (Epworth Sleepiness Scale) and undergoes a **30-second facial scan** using the platform on a tablet in the operatory. The AI model analyzes craniofacial morphology associated with OSA risk — including jaw position, neck circumference estimation, and airway geometry indicators — and returns a **high-risk OSA score**.

Dr. Lee reviews the AI screening result alongside the Epworth score and Robert's reported symptoms. She documents the screening finding in the practice management system and has a brief chair-side conversation with Robert about sleep apnea, its association with cardiovascular disease and hypertension, and the importance of a diagnostic evaluation. Robert reports he has a regular primary care physician but has never discussed sleep concerns with her.

Dr. Lee creates a **structured dental-to-medical referral** to a **sleep medicine physician** at a sleep medicine practice in Columbus, Ohio, transmitting the referral via FHIR-based CDex provider-to-provider push. The sleep medicine practice uses **athenaHealth** as its EHR. The referral package includes the AI screening result (risk score and Epworth score), Robert's reported symptoms, his dental clinical findings, and a clinical note from Dr. Lee recommending evaluation for OSA. Robert is notified through his **patient-facing application** that the referral has been sent.

Robert is also offered an **optional copy of the referral to his primary care physician**, Dr. Angela Morris, MD — closing the loop with his existing medical care team without requiring a separate manual communication. Dr. Morris also uses **athenaHealth**. Dr. Lee's practice transmits a secondary notification to Dr. Morris's athenaHealth FHIR endpoint via the Ohio Health Information Network, flagging the OSA screening finding for inclusion in Robert's longitudinal medical record.

At the **sleep medicine consultation**, Dr. Marcus Webb, MD, reviews Robert's dental referral and screening data. He orders a **home sleep test (HST)** which Robert completes at home. The HST confirms **moderate obstructive sleep apnea** (`ICD-10: G47.33` — obstructive sleep apnea, adult). Dr. Webb evaluates Robert for oral appliance therapy as a CPAP alternative — Robert has previously tried CPAP and discontinued due to intolerance. Dr. Webb issues a **written prescription for a custom oral appliance** (mandibular advancement device) and determines that Robert meets the medical necessity criteria for coverage under his commercial medical plan.

With the physician prescription in hand, Dr. Lee's dental practice — enrolled as a **DME supplier** — fabricates a **custom mandibular advancement device** (`HCPCS: E0486`) for Robert. The appliance is billed to Robert's **medical plan** as durable medical equipment, not to his dental plan. The claim includes the physician's written order, the HST documentation confirming the OSA diagnosis, and a letter of medical necessity.

Dr. Webb transmits a **structured post-fitting summary** back to Dr. Lee including the confirmed OSA diagnosis, sleep study results, the oral appliance prescription, and recommended follow-up protocol. Dr. Lee monitors Robert's appliance fit and occlusal changes at subsequent dental visits, with findings transmitted back to the sleep medicine practice via CDex. Robert's patient application provides real-time updates on referral status, sleep study results, and appliance coverage status throughout the episode.

---

## Section II: Narrative-to-Standards Mapping

| What Happens (Business Language) | Implementation Guide / Standard | Key Transaction |
|---|---|---|
| **AI-assisted OSA screening at dental visit:** Robert undergoes a 30-second facial scan using the AI-powered OSA screening platform; the AI model returns a high-risk OSA score alongside an Epworth Sleepiness Scale score. | US Core / ODE (Under Development) | `Observation` (AI risk score; Epworth score); `RiskAssessment` (OSA risk — high); `Encounter` (routine dental visit, POS 11); screening result documented in practice management system. |
| **Screening finding documented:** Dr. Lee documents the OSA screening result and symptom history as discrete FHIR resources. | US Core / ODE (Under Development) | `Condition` (provisional: R06.83 — snoring; Z13.89 — screening for other specified conditions); `Observation` (daytime fatigue, snoring duration, Epworth score); `Flag` (high OSA risk — recommend sleep medicine evaluation). |
| **Dental-to-medical referral created:** Dr. Lee creates a structured referral to a sleep medicine physician, including the AI screening result, Epworth score, and clinical note. | US Core / CDex | `ServiceRequest` (referral, priority: routine); `DocumentReference` (AI screening report, clinical note); `Observation` (AI risk score, Epworth score); CDex provider-to-provider push to sleep medicine practice athenaHealth FHIR endpoint. |
| **Secondary notification to primary care physician:** Dr. Lee's practice transmits a copy of the OSA screening finding to Dr. Morris's athenaHealth EHR via the Ohio Health Information Network. | CDex / Ohio Health Information Network | `Communication` (OSA screening finding flagged for primary care longitudinal record); CDex push routed through Ohio HIN to Dr. Morris's athenaHealth FHIR endpoint. |
| **Patient notified — referral sent:** Robert's patient application receives notification that the sleep medicine referral has been sent. | FHIR Subscriptions Backport IG | Subscription event triggered on `ServiceRequest` creation. |
| **Sleep medicine consultation:** Dr. Webb reviews the dental referral and screening data and orders a home sleep test. | US Core | `Encounter` (sleep medicine consultation, POS 11); `ServiceRequest` (home sleep test order); referral reviewed and acknowledged; `AppointmentResponse` returned to dental practice. |
| **Home sleep test completed:** Robert completes an HST at home; results confirm moderate OSA. | US Core | `DiagnosticReport` (HST results); `Observation` (AHI — apnea-hypopnea index, oxygen desaturation nadir, respiratory disturbance index); `Condition` updated to confirmed G47.33 (obstructive sleep apnea, adult, moderate). |
| **Patient notified — sleep study results available:** Robert's application receives HST results and confirmed diagnosis. | FHIR Subscriptions Backport IG | Subscription event on `DiagnosticReport` status change; `Condition` (confirmed G47.33) surfaced to patient application. |
| **Oral appliance prescribed:** Dr. Webb issues a written prescription for a custom mandibular advancement device, determining Robert meets DME medical necessity criteria. | US Core | `MedicationRequest` (oral appliance prescription — written order); `DocumentReference` (letter of medical necessity); coverage verification via medical payer FHIR API confirming DME benefit for E0486. |
| **Coverage verified — medical DME benefit:** Dental practice (as DME supplier) verifies Robert's medical plan DME benefit for oral appliance therapy prior to fabrication. | US Core / Da Vinci PDex | `Coverage` queried against commercial medical payer FHIR API; `InsurancePlan` returned confirming E0486 DME coverage, prior authorization requirements, and patient cost-sharing. |
| **Prior authorization submitted — medical benefit:** Dental practice submits PA request to medical payer for E0486 (custom oral appliance as DME). | Da Vinci PAS | `Claim` (PA request); supporting documentation: physician written order, HST `DiagnosticReport`, letter of medical necessity, CPAP intolerance documentation; submitted to medical payer FHIR endpoint. |
| **PA approved:** Medical payer returns PA approval for E0486. | Da Vinci PAS | `ClaimResponse` returned; PA number issued; validity period confirmed. |
| **Custom appliance fabricated and delivered:** Dr. Lee's practice fabricates and delivers the mandibular advancement device. | US Core / ODE (Under Development) | `Device` (mandibular advancement device — manufacturer, model, lot number); `Procedure` (D9947 — custom sleep apnea appliance fitting); `Encounter` (appliance delivery visit, POS 11). |
| **Post-fitting summary returned to dental practice:** Dr. Webb transmits structured summary including confirmed diagnosis, sleep study results, and appliance follow-up protocol to Dr. Lee. | Da Vinci CDex / US Core | `ClinicalImpression` (summary: confirmed G47.33, HST results, appliance prescription, follow-up protocol); `CarePlan` (follow-up: dental monitoring at 1, 3, 6 months; sleep physician review at 3 months); CDex push to dental practice FHIR endpoint. |
| **Ongoing dental monitoring:** Dr. Lee monitors appliance fit and occlusal changes at subsequent dental visits, transmitting findings to sleep medicine practice. | US Core / ODE (Under Development) | `Observation` (appliance fit assessment; occlusal change monitoring); CDex push from dental practice to sleep medicine FHIR endpoint at each monitoring visit. |
| **DME claim submitted to medical payer:** Dental practice (as DME supplier) submits medical claim for E0486. | X12 837P / CMS-1500 | 837P: HCPCS E0486 (custom mandibular advancement device); physician written order on file; HST documentation; PA number; dental practice as DME supplier billing under NPI; medical payer EDI routing. |
| **Patient application updated throughout episode:** Robert's application surfaces referral status, HST results, confirmed diagnosis, PA approval, and post-fitting care plan. | FHIR Subscriptions Backport IG / US Core / PDex | Subscription events at each milestone; `CarePlan` surfaced via SMART App Launch. |

---

## Section III: Technical Overview

This use case exercises a **dental-to-medical referral originating from an AI-assisted screening** at a routine dental visit, spanning a general dental practice, a sleep medicine practice (athenaHealth), a primary care physician (athenaHealth), a commercial medical payer, and the Ohio Health Information Network. The scenario is structurally novel across the OHIA Connectathon test dataset in three ways:

**First:** The dental practice is the originating screening site — not the referral destination. The workflow runs in the opposite direction from all prior use cases: dental to medical, not medical to dental.

**Second:** The oral appliance is a DME device billed under the medical benefit, not a dental procedure billed under the dental benefit. The dental practice must be enrolled as a DME supplier. The prior authorization is submitted to the commercial medical payer using HCPCS E0486 and supported by a physician written order and a sleep study diagnostic report. This cross-benefit billing complexity is one of the principal administrative barriers to widespread adoption of dental sleep medicine — and it is the specific gap that structured FHIR-based data exchange can address.

**Third:** The AI screening tool generates a structured risk output that must be expressible as discrete FHIR resources — `Observation` and `RiskAssessment` — transmitted in the referral payload to a sleep medicine physician. This tests whether AI-generated clinical screening scores from a dental-integrated platform can serve as the triggering event for a standards-based medical referral workflow.

> **No paper forms, portal logins, or fax transmissions are used at any point in the workflow.**

---

### Implementation Guides

| Implementation Guide | Purpose in This Use Case |
|---|---|
| **US Core IG** | Defines FHIR profiles for all clinical data exchanged across the dental practice, sleep medicine practice, primary care physician, and medical payer; includes `RiskAssessment`, `Observation`, `DiagnosticReport`, `Device`, and `CarePlan` resources specific to this use case |
| **Da Vinci Coverage Requirements Discovery (CRD)** | Fired at DME order entry in the dental practice; surfaces PA requirement for E0486 under the commercial medical plan's DME benefit in real time |
| **Da Vinci Documentation Templates and Rules (DTR)** | Retrieves medical payer PA questionnaire for DME oral appliance; pre-populates with physician written order reference, HST results, CPAP intolerance documentation |
| **Da Vinci Prior Authorization Support (PAS)** | Submits PA request for E0486 to commercial medical payer; receives `ClaimResponse` with PA approval; PA number carried into medical claim |
| **Da Vinci Clinical Data Exchange (CDex)** | Three roles: (1) **Dental-to-sleep-medicine referral push** — structured referral with AI screening results transmitted to sleep medicine practice; (2) **Post-fitting summary return** — sleep medicine transmits structured summary back to dental practice; (3) **Ongoing monitoring push** — dental practice transmits appliance fit and occlusal monitoring findings to sleep medicine at each follow-up visit |
| **Da Vinci PDex** | Real-time DME benefit verification — `Coverage` and `InsurancePlan` queried against commercial medical payer to confirm E0486 coverage, PA requirements, and patient cost-sharing before appliance fabrication begins |
| **SMART App Launch IG** | Authorization framework enabling Robert's patient application to connect to medical payer FHIR endpoint and dental practice FHIR endpoint; surfaces PA status, sleep study results, and post-fitting care plan |
| **FHIR Subscriptions Backport IG** | Push notifications to Robert's patient application at referral creation, HST results available, PA approval, and post-fitting care plan available |
| **Ohio Health Information Network** | Routing intermediary for the secondary notification to Dr. Morris (primary care); dental practice transmits OSA screening finding via CDex through the Ohio HIN to Dr. Morris's athenaHealth FHIR endpoint, ensuring the finding is captured in Robert's longitudinal medical record |
| **Oral Health Data Exchange IG (ODE)** | Under development; governs structured exchange of dental sleep medicine clinical data — AI screening results as `RiskAssessment`, appliance fit monitoring as `Observation`, and appliance specifications as `Device` — between the dental practice and the sleep medicine practice |

---

### Key FHIR Resources Exercised

| FHIR Resource | Source IG / Profile | Purpose in This Use Case |
|---|---|---|
| `Patient` | US Core | Patient identity across dental practice, sleep medicine practice, primary care EHR, and commercial medical payer |
| `Coverage` | US Core / PDex | Commercial medical plan DME benefit — member ID, group, DME coverage for E0486, PA requirement — verified before appliance fabrication; commercial dental plan — separate coverage for dental exam |
| `InsurancePlan` | Da Vinci PDex | Commercial medical plan DME benefit structure; E0486 coverage confirmation, PA requirement, patient cost-sharing |
| `RiskAssessment` | US Core | AI-generated OSA risk score — structured output of the facial scan algorithm, including risk level (high/moderate/low) and contributing craniofacial indicators; transmitted in referral payload |
| `Observation` | US Core / ODE | Epworth Sleepiness Scale score; reported symptoms (snoring duration, daytime fatigue); HST results (AHI, oxygen desaturation nadir, RDI); appliance fit monitoring findings at follow-up visits |
| `Questionnaire` / `QuestionnaireResponse` | US Core | Epworth Sleepiness Scale administered via the AI screening platform at dental visit; completed by patient; transmitted with referral |
| `Condition` | US Core / ODE | Provisional screening finding (R06.83 — snoring; Z13.89 — encounter for screening); confirmed diagnosis (G47.33 — obstructive sleep apnea, adult, moderate) after HST |
| `Flag` | US Core | High OSA risk flag created by Dr. Lee at dental visit; transmitted with referral and secondary notification to primary care |
| `DiagnosticReport` | US Core | Home sleep test report — AHI, oxygen desaturation, RDI, sleep staging; confirms OSA diagnosis; transmitted to dental practice in post-fitting summary |
| `ServiceRequest` | US Core | Dental-to-medical referral from Dr. Lee to Dr. Webb (sleep medicine); home sleep test order from Dr. Webb; status lifecycle `active` → `completed` |
| `DocumentReference` | US Core | AI screening report; clinical note from Dr. Lee; physician written order (Dr. Webb) for oral appliance; letter of medical necessity |
| `MedicationRequest` | US Core | Oral appliance prescription — physician written order from Dr. Webb; required for DME coverage under medical benefit |
| `Device` | US Core / ODE | Mandibular advancement device — manufacturer, model, lot number, adjustment specifications; documented at delivery and transmitted in post-fitting summary; enables ongoing monitoring and future appliance replacement continuity |
| `Practitioner` | US Core | Dr. Christine Lee, DDS (general dentist — dental practice); Dr. Marcus Webb, MD (sleep medicine physician); Dr. Angela Morris, MD (primary care physician) |
| `PractitionerRole` | US Core | Role context for each provider; dental practice DME supplier enrollment status confirmed before PA submission |
| `Organization` | US Core | Dental practice (also enrolled as DME supplier); sleep medicine practice (athenaHealth); primary care practice (athenaHealth); commercial medical payer; Ohio Health Information Network |
| `Communication` | US Core | Secondary notification of OSA screening finding transmitted to Dr. Morris's athenaHealth EHR via Ohio Health Information Network |
| `Encounter` | US Core | Routine dental exam with OSA screening (dental practice, POS 11); sleep medicine consultation (POS 11); appliance delivery visit (dental practice, POS 11); follow-up monitoring visits (dental practice, POS 11) |
| `Questionnaire` / `QuestionnaireResponse` | Da Vinci DTR | Medical payer PA questionnaire for E0486 DME coverage; pre-populated with physician order reference, HST results, CPAP intolerance documentation |
| `Claim` (PA) | Da Vinci PAS | Prior authorization request for E0486 submitted to commercial medical payer |
| `ClaimResponse` | Da Vinci PAS | Medical payer PA approval — PA number, validity period, approved DME code |
| `ClinicalImpression` | ODE | Post-fitting structured summary from sleep medicine to dental practice — confirmed diagnosis, HST results, appliance prescription, follow-up protocol |
| `CarePlan` | US Core | Post-fitting care plan — dental monitoring at 1, 3, 6 months; sleep physician review at 3 months with follow-up sleep testing; surfaced to patient application |
| `Appointment` / `AppointmentResponse` | US Core | Sleep medicine consultation appointment; appliance delivery appointment; follow-up monitoring appointments |
| `Task` | CDex / DTR | Tracks open referral (CDex Task); open PA documentation requirement (DTR Task); each closed on completion |
| `Subscription` / `SubscriptionStatus` | FHIR Subscriptions Backport IG | Push notifications to patient application at each key milestone |
| `Bundle` | FHIR Core | Referral packet (ServiceRequest + RiskAssessment + Observation + QuestionnaireResponse + Flag + DocumentReference); post-fitting summary bundle |
| `AuditEvent` | US Core | Cross-organizational data access logging including Ohio Health Information Network routing events |
| `Provenance` | US Core | Chain of custody across dental practice, sleep medicine (athenaHealth), Ohio Health Information Network, primary care (athenaHealth), and medical payer FHIR endpoints |

---

### Cross-Cutting Test Objectives

1. **AI screening output as a FHIR `RiskAssessment` resource** — The AI-powered OSA screening platform produces a structured OSA risk score from a craniofacial facial scan. This use case tests whether that output can be expressed as a FHIR `RiskAssessment` resource — with risk level, probability, contributing basis (craniofacial indicators), and performing device reference — that a receiving sleep medicine physician can act on in their athenaHealth EHR without manual re-entry. This is the first OHIA Connectathon use case to test AI-generated clinical scoring output as a discrete FHIR resource in a referral payload.

2. **Dental-to-medical referral direction** — All prior OHIA use cases have exercised medical-to-dental referrals (oncologist to dentist, pediatrician to pediatric dentist) or dental-to-dental referrals (general dentist to oral surgeon). This use case exercises the reverse: dental provider to medical specialist. The test validates whether CDex provider-to-provider push can route a structured referral from a dental practice FHIR endpoint to a sleep medicine practice FHIR endpoint, and whether the receiving medical provider's system can ingest and surface dental-originated FHIR data.

3. **Cross-benefit billing pathway — DME under medical benefit** — The oral appliance (E0486) is billed under the commercial **medical** plan's DME benefit, not the dental benefit. The dental practice must be enrolled as a DME supplier. The claim requires a physician written order, HST documentation, and PA approval. This use case tests whether FHIR-based data exchange — CRD, DTR, PAS — can support the DME prior authorization workflow for a dental-placed device billed under a medical benefit, a workflow that today requires extensive manual documentation and phone coordination between dental practices, sleep physicians, and medical payers.

4. **`RiskAssessment` + `QuestionnaireResponse` as referral payload components** — The referral includes both the AI-generated `RiskAssessment` (OSA risk score) and the patient-completed `QuestionnaireResponse` (Epworth Sleepiness Scale). The test validates whether these resources can be bundled in a CDex referral push alongside standard `Condition`, `Observation`, and `DocumentReference` resources, and whether the receiving athenaHealth system can surface all components in a coherent clinical view.

5. **Secondary notification to primary care via state HIN** — The dental practice transmits a secondary OSA screening notification to the patient's primary care physician through the Ohio Health Information Network. This tests the state HIN as a routing intermediary for a dental-originated clinical finding — a pattern that has significant policy implications for population health surveillance, care gap identification, and dental-medical integration at the state level.

6. **`Device` resource for a patient-worn oral appliance** — The mandibular advancement device is documented as a FHIR `Device` resource at the time of delivery, including manufacturer, model, and adjustment specifications. This enables ongoing fit monitoring at the dental practice and future appliance replacement without a separate records request to the fabricating laboratory. This is the second OHIA Connectathon use case to introduce the `Device` resource (after the dental implant in Frank Castle Use Case B), but the first to use it for a patient-worn therapeutic device with ongoing monitoring requirements.

7. **DME coverage verification for a dental-placed device** — `Coverage` and `InsurancePlan` are queried against the commercial **medical** payer (not the dental payer) to verify DME benefit availability for E0486 before appliance fabrication. This tests whether a dental practice's FHIR-enabled workflow can distinguish between dental and medical benefit coverage contexts for the same patient and route coverage queries to the appropriate payer endpoint — a capability that requires understanding of cross-benefit benefit design that dental practice management systems do not currently handle natively.

8. **ODE IG validation for dental sleep medicine** — This use case exercises ODE profiles in a dental sleep medicine context: AI screening results as structured `Observation` and `RiskAssessment`, oral appliance fitting as a `Procedure`, appliance specifications as `Device`, and ongoing monitoring observations transmitted from dental to medical provider. None of these workflows have been tested in prior OHIA Connectathons, and several require ODE profile extensions or new profiles to be validated.

9. **Ongoing bidirectional monitoring loop** — Unlike prior use cases where the referral closes with a single post-operative or post-encounter summary, this use case models an **ongoing monitoring relationship** between the dental practice and the sleep medicine physician. Dental monitoring findings (appliance fit, occlusal changes) are transmitted to sleep medicine at each follow-up visit. The test validates whether CDex can support a recurring, multi-event monitoring transmission pattern rather than a single closed-loop summary.

---

## Section IV: EDI Transactions

Robert's oral appliance therapy is billed under his **commercial medical plan** as durable medical equipment — not under his dental plan. The dental practice must be enrolled as a DME supplier under its NPI to submit this claim. The clinical dental visit (exam, X-rays) is billed to the dental plan separately.

### EDI Transactions in Scope

| X12 Transaction | Trigger | Scope Note |
|---|---|---|
| **270 / 271** — Eligibility & Benefit Inquiry / Response (Medical) | Dental practice verifies Robert's commercial medical plan DME benefit before appliance fabrication | Queries medical plan; confirms E0486 DME coverage, PA requirement, patient deductible and coinsurance; dental practice queries medical payer — cross-benefit query not typically supported by dental PMS; named test finding |
| **270 / 271** — Eligibility & Benefit Inquiry / Response (Dental) | Dental practice verifies dental plan for exam and X-rays | Queries dental benefit; confirms exam and radiograph coverage; separate from medical benefit query |
| **837D** — Dental Claim (Dental Practice — Dental Benefit) | Dental practice bills dental plan for routine exam and screening visit | CDT D0120 (periodic oral evaluation); D0274 (bitewing radiographs); D9999 (unlisted dental procedure — OSA screening, if billable under dental benefit); POS 11 |
| **837P / CMS-1500** — Professional Medical Claim (Dental Practice as DME Supplier) | Dental practice (as DME supplier) bills commercial medical plan for custom oral appliance | HCPCS E0486 (custom mandibular advancement device); PA number on claim; physician written order on file; HST DiagnosticReport on file; letter of medical necessity; dental practice billing under NPI as enrolled DME supplier |
| **835** — Remittance Advice (Medical) | Commercial medical payer adjudicates and pays DME claim | Patient deductible and coinsurance applied; adjustment reason codes; any coverage limitation denials surfaced as named test findings |
| **835** — Remittance Advice (Dental) | Dental plan adjudicates and pays dental exam claim | Standard dental adjudication |

> **Note on 278 / PAS:** Da Vinci PAS is used for the medical plan PA for E0486. The X12 278 is not in scope. The DME PA workflow via PAS is tested for the first time in this use case — a dental-placed device submitted to a medical payer is a novel PAS context not previously exercised in OHIA Connectathons.

> **Cross-benefit billing note:** Oral appliance therapy for OSA is almost universally covered under the medical DME benefit, not the dental benefit. The dental practice must be enrolled as a DME supplier under Medicare and private payer programs to submit the E0486 claim. This enrollment requirement, combined with the need for a physician written order and sleep study documentation, creates significant administrative friction that FHIR-based data exchange directly addresses — the physician order, sleep study results, and PA documentation can all be transmitted as structured FHIR resources, eliminating the manual fax-and-phone workflow that currently characterizes this pathway.

> **D9947 / D9948 / D9949 note:** These CDT codes (oral appliance for sleep apnea — new/adjustment/follow-up) are generally not covered under dental benefit plans and are excluded from most commercial dental plan coverage. The dental benefit claim in this use case uses standard exam and radiograph codes only. D9947 is listed as a reference code in the Coding section below but is not expected to generate dental plan reimbursement.

### Coding in Scope

#### HCPCS (Medical DME Claim)

| HCPCS Code | Description | Payer | Coverage Note |
|---|---|---|---|
| `E0486` | Oral device/appliance, custom fabricated, used to reduce upper airway collapsibility; adjustable or nonadjustable; includes fitting and adjustment | Commercial medical plan (DME benefit) | Covered — requires physician written order, sleep study documentation, PA; patient deductible and coinsurance apply |

#### CDT (Dental Claim)

| CDT Code | Description | Dental Plan Coverage Note |
|---|---|---|
| `D0120` | Periodic oral evaluation — established patient | Covered |
| `D0274` | Bitewing radiographic images — four images | Covered; frequency limits may apply |
| `D9947` | Custom sleep apnea appliance, construction and placement | Generally not covered under dental benefit; reference only |
| `D9948` | Adjustment of custom sleep apnea appliance | Generally not covered under dental benefit; reference only |
| `D9999` | Unspecified dental procedure — by report | Optional; for documentation of OSA screening at dental visit if billable under dental plan; open test finding |

#### ICD-10 / Screening Codes

| Code | Type | Description | Application |
|---|---|---|---|
| `Z13.89` | ICD-10 | Encounter for screening for other specified conditions | Dental visit OSA screening code |
| `R06.83` | ICD-10 | Snoring | Provisional symptom code at dental screening visit |
| `G47.33` | ICD-10 | Obstructive sleep apnea, adult | Confirmed diagnosis after HST; primary diagnosis on medical DME claim |
| `Z87.39` | ICD-10 | Personal history of other specified conditions — CPAP intolerance | Supporting documentation for oral appliance as CPAP alternative |

### LOINC Codes in Scope

| LOINC Code | Description | FHIR Resource | Use in This Case |
|---|---|---|---|
| `60155-3` | Epworth Sleepiness Scale | `QuestionnaireResponse`, `Observation` | Patient-completed at dental visit via Soliish platform |
| `28636-0` | AHI — Apnea-hypopnea index | `Observation` | HST result — confirms OSA diagnosis and severity |
| `59408-5` | Oxygen saturation by pulse oximetry | `Observation` | HST oxygen desaturation nadir |
| *(No LOINC established)* | AI-generated OSA facial scan risk score | `RiskAssessment` / `Observation` | Soliish AI screening output — **gap: no established LOINC code for AI craniofacial OSA risk score; named ODE IG test objective** |

> **LOINC gap:** The AI-generated OSA risk score produced by craniofacial morphology analysis (facial scan) has no established LOINC code. This use case surfaces that gap as an action item for the ODE IG development process and the PIE Work Group.

---

## Appendix: Data

### 1. Patient Resource Data

| FHIR Element | Value | System / Note |
|---|---|---|
| **Name** | Robert Vasquez | Given: Robert; Family: Vasquez |
| **Date of Birth** | 1978-08-22 | Age: 47 |
| **Sex** | Male | `http://hl7.org/fhir/ValueSet/administrative-gender` |
| **Dental Practice MRN** | `GDENT-OH-2026-0092` | System: `https://generaldental-oh.example.org/fhir/mrn` |
| **Sleep Medicine MRN** | `OSMI-2026-0047` | System: `https://ohsleepmed.example.org/fhir/mrn` |
| **Commercial Medical Member ID** | `MED-OH-00472918` | System: commercial medical payer member ID |
| **Commercial Dental Member ID** | `DENT-OH-00472918` | System: commercial dental payer member ID |
| **Telecom (Phone)** | (614) 555-0183 | Use: Mobile |
| **Telecom (Email)** | robert.vasquez@example.com | Use: Home |
| **Address** | 2847 High Street, Apt 5, Columbus, OH 43202 | City: Columbus; State: OH; ZIP: 43202 |
| **Language** | English | Preferred language |
| **Active** | True | Patient record is active |

---

### 2. Coverage Resource Data

#### Commercial Medical Plan (DME Benefit — Oral Appliance)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Payer** | Commercial Medical Payer (Synthetic) | Test data label — to be filled with actual payer |
| **Plan Type** | PPO | Preferred Provider Organization |
| **Member ID** | MED-OH-00472918 | Medical plan member ID |
| **Coverage Period** | 2026-01-01 – 2026-12-31 | Plan year |
| **Status** | Active | Coverage confirmed |
| **DME Benefit** | Covered — E0486 (custom oral appliance for OSA) | Requires physician written order, qualifying sleep study, PA |
| **Prior Authorization Required** | Yes — E0486 | Confirmed via CRD |
| **Patient Deductible** | $1,500 individual | Annual deductible — partially met at time of claim |
| **DME Coinsurance** | 20% after deductible | In-network DME supplier |
| **Medical Payer EDI ID** | MED-OH-PPO-EDI | HIPAA X12 claims routing (synthetic) |
| **Medical Payer FHIR Endpoint** | `https://medical-payer-oh.example.org/fhir/r4` | Synthetic FHIR API |

#### Commercial Dental Plan (Dental Exam — Separate Benefit)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Payer** | Commercial Dental Payer (Synthetic) | Test data label — separate from medical payer |
| **Plan Type** | PPO | Preferred Provider Organization |
| **Member ID** | DENT-OH-00472918 | Dental plan member ID |
| **Coverage Period** | 2026-01-01 – 2026-12-31 | Plan year |
| **Preventive / Diagnostic** | 100% covered | Exam and radiographs |
| **Dental Payer EDI ID** | DENT-OH-PPO-EDI | HIPAA X12 claims routing (synthetic) |
| **Dental Payer FHIR Endpoint** | `https://dental-payer-oh.example.org/fhir/r4` | Synthetic FHIR API |

---

### 3. Organization Resource Data

#### General Dental Practice — Ohio (DME Supplier)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1467823205 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | General Dental Practice — Ohio (Synthetic) | Test data label — to be filled with actual organization |
| **Type** | General Dental Practice; DME Supplier | Dual role — dental practice and enrolled DME supplier |
| **DME Supplier Enrollment** | Active — Medicare and commercial medical plans | Required for E0486 billing |
| **Care Setting** | Place of Service 11 — Office | In-office |
| **Practice Management System** | Dental PMS with interim FHIR server; Soliish integration | Architecture |
| **FHIR Endpoint** | `https://generaldental-oh.example.org/fhir/r4` | Interim FHIR server |
| **NPI Taxonomy Code** | 1223G0001X | General dentist |

#### Ohio Sleep Medicine Institute (Sleep Medicine Practice)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization NPI** | 1578293290 | `http://hl7.org/fhir/sid/us-npi` |
| **Organization Name** | Ohio Sleep Medicine Institute | Named Soliish partner organization |
| **Address** | Columbus, Ohio | Practice location |
| **Type** | Sleep Medicine Practice | Organization type |
| **Specialty** | Sleep Medicine | Primary specialty |
| **FHIR Endpoint** | `https://ohsleepmed.example.org/fhir/r4` | Synthetic FHIR endpoint |
| **NPI Taxonomy Code** | 2084A2900X | Sleep Medicine |

#### Ohio Health Information Network (HIN)

| FHIR Element | Value | System / Note |
|---|---|---|
| **Organization Name** | Ohio Health Information Network (Synthetic) | State HIN routing intermediary |
| **Type** | Health Information Network | HIN type |
| **Role in Use Case** | Routes secondary OSA screening notification from dental practice to primary care EHR | CDex push intermediary |
| **FHIR Endpoint** | `https://ohhin.example.org/fhir/r4` | Synthetic FHIR routing endpoint |

---

### 4. Practitioner Resource Data

#### Dr. Christine Lee, DDS — General Dentist (Dental Practice)

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1538476391 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Christine Ann Lee, DDS | Given: Christine; Family: Lee |
| **Qualification** | DDS — Doctor of Dental Surgery | Dental degree |
| **License Number** | OH-DDS-047382 | Ohio dental license (synthetic) |
| **Specialty Code (Taxonomy)** | 1223G0001X | General dentist |
| **Organization** | General Dental Practice — Ohio | Employment |
| **Place of Service** | 11 — Office | In-office |
| **Role in Use Case** | OSA screening; dental-to-medical referral originator; DME supplier for appliance fabrication; ongoing appliance monitoring | Primary dental provider throughout the episode |

#### Dr. Marcus Webb, MD — Sleep Medicine Physician

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1649204027 | `http://hl7.org/fhir/sid/us-npi` |
| **Full Name** | Marcus James Webb, MD | Given: Marcus; Family: Webb |
| **Qualification** | MD — Doctor of Medicine | Medical degree |
| **Specialty Code (Taxonomy)** | 2084A2900X | Sleep Medicine |
| **Organization** | Ohio Sleep Medicine Institute | Employment |
| **Place of Service** | 11 — Office | In-office |
| **Role in Use Case** | Sleep medicine consultant; HST ordering; oral appliance prescribing; post-fitting summary; ongoing sleep monitoring | Receiving medical specialist |

#### Dr. Angela Morris, MD — Primary Care Physician

| FHIR Element | Value | System / Note |
|---|---|---|
| **NPI** | 1729384213 | `http://hl7.org/fhir/sid/us-npi` |
| **Qualification** | MD — Doctor of Medicine | Medical degree |
| **Specialty Code (Taxonomy)** | 207Q00000X | Family Medicine |
| **Role in Use Case** | Secondary notification recipient — OSA screening finding; longitudinal medical record update | Not the referral target; informed via Ohio HIN |

---

### 5. Workflow & Service Data

#### RiskAssessment (Soliish AI OSA Screening)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Final | Screening complete |
| **Method** | AI craniofacial morphology analysis — Soliish facial scan platform | AI screening modality |
| **Subject** | Robert Vasquez | Patient reference |
| **Performer** | Dr. Christine Lee, DDS (supervising dental provider) | Dental provider supervising AI screening |
| **Occurrence DateTime** | 2026-07-08 | Date of screening |
| **Basis** | `Observation` (Epworth score: 14/24); `Observation` (reported snoring — years duration); `Observation` (daytime fatigue); craniofacial scan output | Clinical basis for risk estimate |
| **Prediction — Outcome** | High risk for obstructive sleep apnea | Risk classification |
| **Prediction — Probability** | 0.82 | Soliish model output (82% probability of clinically significant OSA) |
| **Note** | AI-generated OSA risk score based on craniofacial morphology analysis. No established LOINC code for this observation type — flagged as ODE IG test objective. Epworth Sleepiness Scale score 14/24 (borderline excessive daytime sleepiness). Screening conducted using Soliish platform, version [to be confirmed]. | Screening documentation |

#### ServiceRequest (Referral — Dental Practice to Sleep Medicine)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Referral fulfilled |
| **Intent** | Order | Clinical order |
| **Category** | Consultation / Referral | Type |
| **Priority** | Routine | Non-urgent |
| **Code** | Sleep medicine evaluation — high-risk OSA identified at dental screening; oral appliance therapy candidate | Referral reason |
| **Subject** | Robert Vasquez | Patient reference |
| **Requester** | Dr. Christine Lee, DDS | Dental provider — originating referral |
| **Performer** | Dr. Marcus Webb, MD | Sleep medicine physician |
| **Reason Code** | Z13.89 (encounter for OSA screening); R06.83 (snoring); G47.00 (insomnia — provisional, pending evaluation) | Presenting codes |
| **Supporting Info** | `RiskAssessment` (Soliish AI score — 0.82 high risk); `QuestionnaireResponse` (Epworth score 14/24); `Flag` (high OSA risk); `Observation` (reported symptoms) | Referral payload |
| **Ordered Date** | 2026-07-08 | Dental visit date |
| **Description** | Patient presents for routine dental visit. AI-assisted facial scan screening (Soliish) and Epworth Sleepiness Scale administered. Soliish AI risk score: 0.82 (high risk for OSA). Epworth score: 14/24 (borderline excessive daytime sleepiness). Patient reports years of snoring confirmed by partner; daytime fatigue attributed to work stress. No prior sleep evaluation. No established sleep medicine provider. Patient reports prior CPAP trial approximately 5 years ago — discontinued due to intolerance (mask discomfort, claustrophobia). Patient is a potential oral appliance therapy candidate pending formal OSA diagnosis. Referral package includes AI screening report, Epworth results, symptom history, and clinical note. | Referral payload |

#### Claim (Prior Authorization — Dental Practice to Medical Payer — E0486)

| FHIR Element | Value | Notes |
|---|---|---|
| **Use** | Preauthorization | DME PA request |
| **Status** | Active | Submitted pending decision |
| **Patient** | Robert Vasquez | Patient reference |
| **Insurer** | Commercial Medical Payer | Medical plan — DME benefit |
| **Provider** | General Dental Practice — Ohio (as DME Supplier) | Submitting as enrolled DME supplier |
| **Procedure Code** | HCPCS E0486 | Custom oral appliance for OSA |
| **Diagnosis** | G47.33 (obstructive sleep apnea, adult, moderate); Z87.39 (history of CPAP intolerance) | Supporting diagnoses |
| **Supporting Info** | Physician written order (Dr. Webb); HST `DiagnosticReport` (AHI 22.4 — moderate OSA); letter of medical necessity; CPAP intolerance documentation | DME coverage documentation |
| **Submitted Date** | 2026-08-15 | PA submission date |

#### Device (Mandibular Advancement Device)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Active | Device in use |
| **Type** | Custom mandibular advancement device — oral appliance for OSA | Device type |
| **Manufacturer** | Oral Appliance Manufacturer (Synthetic) | To be filled with actual manufacturer |
| **Model** | Custom MAD — titratable | Device model |
| **Lot Number** | MAD-2026-08291 | Manufacturing lot (synthetic) |
| **Body Site** | Maxillary and mandibular arches | Placement |
| **Patient** | Robert Vasquez | Patient reference |
| **Note** | Transmitted to sleep medicine practice and patient application. Device specifications enable follow-up titration adjustments and future replacement without separate records request. Ongoing monitoring of occlusal changes required per AADSM guidelines. | Clinical and continuity note |

#### ClinicalImpression (Post-Fitting Summary — Sleep Medicine to Dental Practice)

| FHIR Element | Value | Notes |
|---|---|---|
| **Status** | Completed | Summary complete |
| **Date** | 2026-08-28 | Appliance delivery date |
| **Assessor** | Dr. Marcus Webb, MD | Sleep medicine physician |
| **Summary** | Robert Vasquez, 47M. HST confirmed moderate obstructive sleep apnea (G47.33; AHI 22.4 events/hour; O2 nadir 84%). Oral appliance therapy selected as primary treatment given documented CPAP intolerance. Custom mandibular advancement device prescribed and fabricated (E0486). Device delivered 2026-08-28 — see Device record for specifications. Initial titration setting: 65% maximum protrusion. Follow-up sleep testing recommended at 3 months to confirm therapeutic efficacy. Dental monitoring for occlusal changes and appliance fit at 1, 3, and 6 months per AADSM guidelines. Patient counseled on appliance care, morning jaw exercises, and symptom monitoring. | Post-fitting summary |
| **Recommendations** | 1. Dental appliance fit and occlusal check at 1 month; 2. Follow-up sleep study at 3 months to confirm AHI reduction; 3. Titration adjustment as needed based on symptom response; 4. Annual sleep physician review; 5. Ongoing dental monitoring per AADSM protocol | Follow-up plan |

---

### 6. Clinical Codes & Mappings

#### ICD-10 Diagnosis Codes

| Code | Description | Application |
|---|---|---|
| Z13.89 | Encounter for screening for other specified conditions | Dental visit screening encounter code |
| R06.83 | Snoring | Presenting symptom at dental screening |
| G47.33 | Obstructive sleep apnea, adult | Confirmed diagnosis — primary code on E0486 DME claim |
| Z87.39 | Personal history of other specified conditions | CPAP intolerance — supports OAT as primary treatment |

#### HCPCS / CDT Codes

| Code | System | Description | Application |
|---|---|---|---|
| `E0486` | HCPCS | Oral device/appliance, custom fabricated, for OSA | Medical DME claim — primary billing code |
| `D0120` | CDT | Periodic oral evaluation | Dental claim — routine exam |
| `D0274` | CDT | Bitewing radiographic images — four images | Dental claim — routine radiographs |
| `D9947` | CDT | Custom sleep apnea appliance, construction and placement | Reference only — generally not covered by dental plan |
| `D9948` | CDT | Adjustment of custom sleep apnea appliance | Reference only — follow-up adjustment visits |

#### LOINC Codes

| LOINC | Description | FHIR Resource | Status |
|---|---|---|---|
| `60155-3` | Epworth Sleepiness Scale | `QuestionnaireResponse`, `Observation` | Standard |
| `28636-0` | Apnea-hypopnea index | `Observation` | Standard |
| `59408-5` | Oxygen saturation — pulse oximetry | `Observation` | Standard |
| *[NO CODE]* | AI craniofacial OSA risk score | `RiskAssessment` | **GAP: Named ODE IG test objective** |

---

### 7. Timeline & Dates

| Event | Date | Actor | System |
|---|---|---|---|
| **Routine dental visit — OSA screening** | 2026-07-08 | Dr. Lee / Robert | Dental PMS + Soliish platform |
| **RiskAssessment + Epworth documented** | 2026-07-08 | Dr. Lee | Dental PMS → interim FHIR server |
| **Dental-to-medical referral transmitted** | 2026-07-08 | Dr. Lee's staff | CDex → Sleep medicine FHIR endpoint |
| **Secondary notification to PCP — Ohio HIN** | 2026-07-08 | Dental practice system | CDex → Ohio HIN → Dr. Morris EHR |
| **Patient notified — referral sent** | 2026-07-08 | Patient application | FHIR Subscription event |
| **Sleep medicine consultation** | 2026-07-15 | Dr. Webb / Robert | Sleep medicine EHR |
| **Home sleep test ordered** | 2026-07-15 | Dr. Webb | Sleep medicine EHR |
| **Home sleep test completed** | 2026-07-18 | Robert (at home) | HST device |
| **HST results available — G47.33 confirmed** | 2026-07-22 | Dr. Webb | Sleep medicine EHR → patient app |
| **Oral appliance prescribed** | 2026-07-22 | Dr. Webb | Physician written order → dental practice |
| **DME benefit verified (CRD / PDex)** | 2026-07-23 | Dental practice | Medical payer FHIR API |
| **PA submitted (PAS)** | 2026-07-24 | Dental practice billing | PAS → Medical payer FHIR endpoint |
| **PA approved (ClaimResponse)** | 2026-08-01 | Medical payer | ClaimResponse → Dental practice |
| **Patient notified — PA approved** | 2026-08-01 | Patient application | FHIR Subscription event |
| **Appliance fabricated and delivered** | 2026-08-28 | Dr. Lee / Robert | Dental practice |
| **Post-fitting summary transmitted** | 2026-08-28 | Dr. Webb | CDex → Dental practice FHIR |
| **Patient application updated — care plan available** | 2026-08-28 | Patient application | FHIR Subscription event |
| **1-month dental monitoring visit** | 2026-09-28 | Dr. Lee / Robert | Dental practice → CDex → Sleep medicine |
| **3-month sleep study (efficacy confirmation)** | 2026-11-22 | Dr. Webb / Robert | Sleep medicine |
| **837P submitted — E0486 DME claim** | 2026-08-29 | Dental practice billing | E0486 + PA number → Medical payer EDI |
| **837D submitted — dental exam claim** | 2026-07-09 | Dental practice billing | D0120, D0274 → Dental payer EDI |

#### Key Timeline Constraints

| Constraint | Target | Rationale |
|---|---|---|
| **Referral transmission** | Same day as dental screening visit | Maintains momentum; patient is engaged at point of screening |
| **Sleep medicine consultation** | Within 1 week of referral | Routine; non-urgent; standard access |
| **HST completion** | Within 3 days of ordering | Home test; no scheduling barrier |
| **HST results available** | Within 5 days of test completion | Scoring and physician review |
| **PA submission** | Within 2 business days of physician order | Begins DME coverage clock |
| **PA decision** | Within 5–7 business days | Standard commercial medical PA timeline |
| **Appliance delivery** | Within 4 weeks of PA approval | Fabrication and fitting |
| **1-month monitoring** | 4 weeks post-delivery | First occlusal and fit check per AADSM guidelines |
| **3-month efficacy sleep study** | 12 weeks post-delivery | Confirm AHI reduction; titration adjustment as needed |

---

*This dataset is a test and validation vehicle for the Oral Health Data Exchange (ODE) Implementation Guide, developed under HL7 and sponsored by the PIE Work Group (PSS-2714). It is intended for use in connectathon and interoperability testing environments only. oralhealthalliance.net*
