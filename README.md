# OHIA Connectathon — Dental Interoperability Test Dataset
## Patient Use Cases: Clinical Scenarios, Encounter Summaries, and Claims Data


**Practice:** Harrodsburg Family Dentistry · 517 Legion Dr, Harrodsburg, KY 40330 · (859) 734-7709
**Rendering Provider:** Dr. Philip Barsotti, DMD · NPI: 1568030203 · KY Dental License: 10615
**Organization NPI:** 1245734763
**Dataset Version:** 1.0 · March 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [How to Use This Document](#2-how-to-use-this-document)
3. [Dataset Infrastructure](#3-dataset-infrastructure)
4. [Emily Watkins — Routine Preventive Care and Single-Surface Restoration](#4-emily-watkins)
   - 4.1 [Business Overview](#41-business-overview)
   - 4.2 [Encounter Summary for Clinical Staff](#42-encounter-summary-for-clinical-staff)
   - 4.3 [Claims and Billing Summary for Clearinghouse Submission](#43-claims-and-billing-summary-for-clearinghouse-submission)
5. [Jason Morales — Emergency New-Patient Visit with Extraction](#5-jason-morales)
   - 5.1 [Business Overview](#51-business-overview)
   - 5.2 [Encounter Summary for Clinical Staff](#52-encounter-summary-for-clinical-staff)
   - 5.3 [Claims and Billing Summary for Clearinghouse Submission](#53-claims-and-billing-summary-for-clearinghouse-submission)
6. [Laura Jennings — Prior Authorization, Root Canal Therapy, and Crown](#6-laura-jennings)
   - 6.1 [Business Overview](#61-business-overview)
   - 6.2 [Encounter Summary for Clinical Staff](#62-encounter-summary-for-clinical-staff)
   - 6.3 [Claims and Billing Summary for Clearinghouse Submission](#63-claims-and-billing-summary-for-clearinghouse-submission)
7. [Dataset Reference Summary](#7-dataset-reference-summary)

---

## 1. Executive Summary

This document describes three synthetic but clinically realistic patient scenarios created for use at the Oral Health Interoperability Alliance (OHIA) Connectathon. Each scenario is pre-loaded into an Onyx OnyxOS FHIR server and used to test whether patient-facing and provider-centric applications can correctly retrieve dental claims, encounter data, and prior authorization information using open FHIR standards — without proprietary interfaces, custom integrations, or phone calls to an insurance company.

All three patients receive care at the same Kentucky dental practice from the same dental provider. Each carries a different commercial dental PPO through a different payer, and each scenario exercises a distinct and progressively complex set of administrative and clinical workflows. Together they represent the full arc of dental administrative complexity — from a straightforward preventive visit through a multi-month prior authorization and treatment sequence.

**Emily Watkins** is the baseline scenario. She receives routine preventive care at no cost to her, followed by a simple filling that requires applying a deductible and coinsurance. Her story tests whether a patient-facing app can retrieve two dental claims, display the correct out-of-pocket amounts, distinguish between preventive services (exempt from deductible) and basic restorative services (subject to it), and compute her year-to-date deductible accumulation from FHIR data alone. These are the foundational capabilities any dental patient app must get right before it is useful to anyone.

**Jason Morales** is a new patient in acute pain who presents for a same-day emergency exam and leaves with an extraction. His single visit generates four procedure lines across two different benefit tier rates — basic services at 80% and oral surgery at 70% — with a deductible that exhausts on the first line. His extraction of tooth #30 introduces the dental-specific data element central to the CARIN Blue Button Oral Profile: the ability to record and retrieve a tooth number in a machine-readable field. His scenario tests whether a patient-facing app can display that correctly, and whether a provider app can search across all patients for claims involving a specific tooth.

**Laura Jennings** is the most complex scenario in the dataset. She presents as an emergency patient, is diagnosed with irreversible pulpitis on tooth #3, and requires root canal therapy followed by a porcelain crown. Her plan requires prior authorization before treatment can proceed. The authorization workflow spans three FHIR implementation guides — CARIN Blue Button for claims access, Da Vinci Prior Authorization Support for the authorization exchange, and Da Vinci Documentation Templates and Rules for the clinical evidence submitted in support of the request. Her story runs from June through July 2026 across three encounters, six FHIR resource bundles, and three different benefit tier rates. One of her approved procedures carries a conditional authorization that requires clinical documentation to release — testing whether apps can parse and surface that condition to the patient before their appointment.

**The question these scenarios answer:** Can a patient open an app and see their dental claims history, understand what they owe and why, track a prior authorization from submission through approval, and confirm that the authorization number carried through to their treatment claims — all without calling their insurance company? And can a dental practice system query that same data at the population level, retrieve clinical documentation, and trace the full prior authorization chain across FHIR namespaces?



**What this dataset produces for the HL7 ballot process:** Ten specific interoperability findings — five from patient-facing app tests and five from provider-centric app tests — that the OHIA working group will submit as structured input to the January 2027 HL7 dental FHIR implementation guide ballot. Each finding is a specific yes/no question with a corresponding FHIR test case, expected response, and observed behavior. The goal is not to declare success but to identify exactly where the standards work, where they need extension, and where the dental ecosystem needs additional guidance.

---

## 2. How to Use This Document

This document is organized into three sections for each patient, each written for a different audience.

**The business overview** tells the patient's story in plain language. No clinical terminology, no CDT codes, no FHIR. It describes what happened, why it happened, and what the financial outcome was. This section is appropriate for practice administrators, payer stakeholders, and anyone evaluating the Connectathon dataset without a technical background.

**The encounter summary** is written for dental professionals. It describes what happened clinically at each visit — examination findings, procedures performed, and outcomes — using standard dental terminology, CDT codes in context, and tooth-level specifics. It reads the way a clinical note or treatment record would.

**The claims and billing summary** is written for clearinghouse vendors and dental billing staff. It provides the structured data needed to generate, validate, or adjudicate a dental claim — payer IDs, NPIs, service lines with tooth and surface, expected adjudication line by line, and billing notes flagging anything unusual. FHIR details are intentionally minimized in this section.

---

## 3. Dataset Infrastructure

All nine FHIR bundles in this dataset are pre-loaded into the Onyx OnyxOS FHIR server at the Connectathon tenant. The following identifiers are used consistently across all bundles.

### Provider and Practice Identifiers

| Entity | Name | Identifier | Verified Against |
|---|---|---|---|
| Rendering provider | Philip Barsotti, DMD | NPI 1568030203 | NPPES Registry |
| Practice organization | Harrodsburg Family Dentistry | NPI 1245734763 | NPPES Registry |
| KY Dental License | Philip Barsotti, DMD | License 10615 | NPPES Registry |
| NUCC taxonomy | General Dentist | 1223G0001X | NUCC |
| Practice address | 517 Legion Dr, Harrodsburg, KY 40330 | | NPPES Registry |
| Practice phone | (859) 734-7709 | | NPPES Registry |

### Payer Identifiers

| Patient | Payer | EDI Payer ID | Verified Against |
|---|---|---|---|
| Emily Watkins | Delta Dental of Kentucky | 38217 | NEA / Patterson payer lists |
| Jason Morales | Cigna Dental Health of Kentucky, Inc. | 62308 | Cigna provider documentation |
| Laura Jennings | Anthem Blue Cross and Blue Shield of Kentucky | 026033 | NEA / Patterson payer lists |

### FHIR Standards in Use

| Standard | Namespace | Used For |
|---|---|---|
| CARIN Blue Button® with Oral Profile | /carin-bb/fhir/ | All patient-facing EOBs and claims access |
| Da Vinci Prior Authorization Support (PAS) | /davinci-pas/fhir/ | Prior authorization request and ClaimResponse |
| Da Vinci Documentation Templates and Rules (DTR) | /davinci-dtr/fhir/ | Clinical documentation supporting prior authorization |
| US Core | Shared | Patient demographics, Condition, Organization |

### Test Account Credentials

| Patient | Test Username | Member ID |
|---|---|---|
| Emily Watkins | WTK4592031 |
| Jason Morales |MRL8421137 |
| Laura Jennings | JNG5027741 |

Passwords are distributed via the OHIA coordination channel and are not published in this document.

---

## 4. Emily Watkins — Routine Preventive Care and Single-Surface Restoration

### 4.1 Business Overview

Emily Watkins schedules her semiannual preventive dental visit at Harrodsburg Family Dentistry. Dr. Philip Barsotti completes her routine examination, professional cleaning, and bitewing X-rays. Emily is covered under a Delta Dental PPO plan through her employer, KY River Health Cooperative. The office confirms she is active on the plan and that preventive services are covered at 100% with no deductible. The claim is submitted, processed without issue, and Emily receives an Explanation of Benefits showing no out-of-pocket cost.

Two months later, Emily returns for a follow-up. A small area of decay noted during her March visit has progressed, and Dr. Barsotti places a one-surface tooth-colored filling on the upper left second premolar. Emily's plan covers this type of service at 80% after her annual deductible. Since she has not yet used any benefits that require a deductible this year, her full $50 annual deductible is applied first, and she pays the remaining coinsurance balance of $22. The filling is completed in a single appointment without complications.

Emily's total out-of-pocket expense for the year — covering two visits, one cleaning, four X-rays, one exam, and one filling — is $72.

| | |
|---|---|
| **Patient** | Emily Watkins · DOB March 2, 1994 |
| **Payer** | Delta Dental of Kentucky · Member ID WTK4592031 |
| **Employer group** | KY River Health Cooperative · Group KYRHC-2026-001 |
| **Encounters** | 2 (March 12, 2026 and May 22, 2026) |
| **Total submitted** | $400.00 |
| **Total plan paid** | $308.00 |
| **Total patient paid** | $72.00 |

---

### 4.2 Encounter Summary for Clinical Staff

#### Encounter 1 — Routine Preventive Visit
**Date of Service:** March 12, 2026
**Visit Type:** Semiannual examination and cleaning — new patient to this practice

**Services Performed:**

| CDT | Description |
|---|---|
| D0120 | Periodic oral evaluation |
| D0274 | Bitewing radiographic images — four images |
| D1110 | Prophylaxis — adult |

**Clinical Findings:** Dentition generally healthy. Soft tissue examination unremarkable. Bitewing radiographs reviewed. Early interproximal and occlusal carious lesion noted on tooth #13 (upper left second premolar). Lesion appears limited to enamel at this time with no radiographic evidence of pulpal involvement. No immediate restoration indicated. Monitoring elected. Patient counseled on findings and oral hygiene instruction provided. Follow-up recommended at next semiannual appointment or sooner if sensitivity develops.

**Outcome:** All preventive services completed without complication. No treatment concerns beyond monitoring of tooth #13.

---

#### Encounter 2 — Single-Surface Posterior Restoration
**Date of Service:** May 22, 2026
**Visit Type:** Restorative follow-up — decay on tooth #13

**Services Performed:**

| CDT | Description | Tooth | Surface |
|---|---|---|---|
| D2391 | Resin-based composite restoration — one surface, posterior | #13 | Occlusal |

**Clinical Findings:** Patient returned as scheduled. Carious lesion on tooth #13 has progressed since March visit. Radiographic and clinical assessment confirms dentin involvement. Restoration indicated. Resin-based composite placed on the occlusal surface of tooth #13 under local anesthesia. Single appointment, no complications. Margins acceptable. Occlusion verified. Tooth restored to full function.

**Outcome:** Restoration complete. No further treatment indicated for tooth #13 at this time. Continue with routine preventive care schedule.

---

### 4.3 Claims and Billing Summary for Clearinghouse Submission

#### Claim 1 of 2 — Routine Preventive Visit

| Field | Value |
|---|---|
| Patient name | Emily Watkins |
| Date of birth | March 2, 1994 |
| Member ID | WTK4592031 |
| Subscriber | Emily Watkins (self) |
| Employer group | KY River Health Cooperative |
| Group number | KYRHC-2026-001 |
| Payer | Delta Dental of Kentucky |
| EDI payer ID | 38217 |
| Rendering provider | Philip Barsotti, DMD · NPI 1568030203 |
| Billing organization | Harrodsburg Family Dentistry · NPI 1245734763 |
| Practice address | 517 Legion Dr, Harrodsburg, KY 40330 |
| Date of service | March 12, 2026 |
| Place of service | Office (11) |
| Prior authorization | Not required |

**Service Lines:**

| Line | CDT | Description | Tooth | Surface | Fee |
|---|---|---|---|---|---|
| 1 | D0120 | Periodic oral evaluation | — | — | $55.00 |
| 2 | D0274 | Bitewing radiographs, four images | — | — | $70.00 |
| 3 | D1110 | Prophylaxis — adult | — | — | $95.00 |
| | | **Total billed** | | | **$220.00** |

**Expected Adjudication:**

| | Amount |
|---|---|
| Total submitted | $220.00 |
| PPO write-off | $0.00 |
| Allowed | $220.00 |
| Deductible applied | $0.00 — preventive services are deductible-exempt under this plan |
| Plan paid (100%) | $220.00 |
| Patient responsibility | $0.00 |
| Payment type | Complete |

---

#### Claim 2 of 2 — Single-Surface Restoration

| Field | Value |
|---|---|
| Patient name | Emily Watkins |
| Date of birth | March 2, 1994 |
| Member ID | WTK4592031 |
| Subscriber | Emily Watkins (self) |
| Employer group | KY River Health Cooperative |
| Group number | KYRHC-2026-001 |
| Payer | Delta Dental of Kentucky |
| EDI payer ID | 38217 |
| Rendering provider | Philip Barsotti, DMD · NPI 1568030203 |
| Billing organization | Harrodsburg Family Dentistry · NPI 1245734763 |
| Practice address | 517 Legion Dr, Harrodsburg, KY 40330 |
| Date of service | May 22, 2026 |
| Place of service | Office (11) |
| Prior authorization | Not required |
| Related claim | Claim 1 of 2 above — decay first noted at March 12, 2026 visit |

**Service Lines:**

| Line | CDT | Description | Tooth | Surface | Fee |
|---|---|---|---|---|---|
| 1 | D2391 | Resin-based composite — one surface, posterior | #13 | Occlusal | $180.00 |
| | | **Total billed** | | | **$180.00** |

**Expected Adjudication:**

| | Amount |
|---|---|
| Submitted | $180.00 |
| PPO contractual write-off | −$20.00 |
| Allowed | $160.00 |
| Annual deductible applied | −$50.00 |
| Post-deductible eligible | $110.00 |
| Plan paid (80% of $110.00) | $88.00 |
| Patient coinsurance (20% of $110.00) | $22.00 |
| **Total patient responsibility** | **$72.00** |
| Payment type | Partial |

> **Clearinghouse note:** The $50 deductible applied here represents Emily's full individual annual deductible for plan year 2026. No deductible has been applied on any prior claim this year — the March 12 preventive visit was deductible-exempt. After this claim processes, Emily's deductible balance is $0 for the remainder of plan year 2026.

> **Billing note:** The most common adjudication error on this type of claim is applying the 80% plan rate to the full allowed amount of $160 before subtracting the deductible, yielding an incorrect plan benefit of $128. The correct sequence is: subtract the $50 deductible first ($160 − $50 = $110), then apply 80% to the remainder ($88). If a remittance posts a plan benefit of $128, the deductible logic was not applied correctly.

**Year-to-Date Summary — Emily Watkins:**

| Encounter | Date | Submitted | Write-Off | Allowed | Plan Paid | Patient Paid |
|---|---|---|---|---|---|---|
| Preventive visit | Mar 12, 2026 | $220.00 | $0.00 | $220.00 | $220.00 | $0.00 |
| Composite restoration | May 22, 2026 | $180.00 | $20.00 | $160.00 | $88.00 | $72.00 |
| **Year total** | | **$400.00** | **$20.00** | **$380.00** | **$308.00** | **$72.00** |

---

## 5. Jason Morales — Emergency New-Patient Visit with Extraction

### 5.1 Business Overview

Jason Morales calls Harrodsburg Family Dentistry seeking an emergency appointment. He has been in severe pain for three days — lower right jaw, swelling, and difficulty chewing. The office schedules him same-day as a new patient.

Dr. Philip Barsotti examines Jason, takes periapical X-rays of the affected area, and determines that tooth #30 — the lower right first molar — has a fracture extending below the gum line that cannot be repaired. The only treatment option is extraction. Jason agrees, the tooth is removed at the same appointment, and he leaves without pain.

Jason is covered through a Cigna Dental PPO at his employer, Ohio River Manufacturing. His plan covers the exam, X-rays, and similar basic services at 80% after the deductible. Extractions, however, fall under the oral surgery benefit category, which is covered at 70%. This means two different rates apply to the same visit. Jason has not used any dental benefits this year, so his $50 annual deductible also applies at this visit. His total out-of-pocket for the day is $114.

| | |
|---|---|
| **Patient** | Jason Morales · DOB September 18, 1986 |
| **Payer** | Cigna Dental Health of Kentucky · Member ID MRL8421137 |
| **Employer group** | Ohio River Manufacturing · Group ORM-2026-001 |
| **Encounters** | 1 (April 8, 2026) |
| **Total submitted** | $335.00 |
| **Total plan paid** | $176.00 |
| **Total patient paid** | $114.00 |

---

### 5.2 Encounter Summary for Clinical Staff

#### Encounter 1 — Emergency Examination and Extraction
**Date of Service:** April 8, 2026
**Visit Type:** Same-day emergency examination — new patient

**Services Performed:**

| CDT | Description | Tooth | Surface |
|---|---|---|---|
| D0140 | Limited oral evaluation — problem focused | — | — |
| D0220 | Periapical radiographic image — first image | #30 | — |
| D0230 | Periapical radiographic image — each additional image | — | — |
| D7140 | Extraction, erupted tooth or exposed root (elevation and/or forceps removal) | #30 | — |

**Clinical Findings:** Patient presented with a three-day history of severe pain, swelling, and cold sensitivity in the lower right quadrant. New patient to this practice. Periapical radiographs taken of tooth #30 (lower right first molar). Radiographic and clinical examination confirms subgingival fracture extending below the cementoenamel junction on the mesial aspect. Crown-to-root ratio compromised. Tooth #30 is non-restorable. No periapical pathology noted at this time, though prognosis is poor without intervention. All findings discussed with patient. Treatment options reviewed including future implant or fixed bridge for tooth #30 site. Informed consent obtained for extraction.

Extraction performed under local anesthesia. Uncomplicated forceps removal of tooth #30. Tooth removed intact. Alveolar bone intact. Socket irrigated. Gauze placed. Patient tolerated procedure well. Postoperative instructions provided verbally and in writing. Patient advised to follow up in two weeks for healing assessment and discussion of tooth replacement options.

**Outcome:** Tooth #30 extracted without complication. Patient discharged in stable condition. Pain fully resolved at appointment.

---

### 5.3 Claims and Billing Summary for Clearinghouse Submission

#### Claim 1 of 1 — Emergency Examination and Extraction

| Field | Value |
|---|---|
| Patient name | Jason Morales |
| Date of birth | September 18, 1986 |
| Member ID | MRL8421137 |
| Subscriber | Jason Morales (self) |
| Employer group | Ohio River Manufacturing |
| Group number | ORM-2026-001 |
| Payer | Cigna Dental Health of Kentucky, Inc. |
| EDI payer ID | 62308 |
| Rendering provider | Philip Barsotti, DMD · NPI 1568030203 |
| Billing organization | Harrodsburg Family Dentistry · NPI 1245734763 |
| Practice address | 517 Legion Dr, Harrodsburg, KY 40330 |
| Date of service | April 8, 2026 |
| Place of service | Office (11) |
| Prior authorization | Not required |
| Visit notes | Same-day emergency appointment. New patient. Three-day history of severe lower right pain, swelling, and cold sensitivity. |

**Service Lines:**

| Line | CDT | Description | Tooth | Surface | Benefit Category | Fee |
|---|---|---|---|---|---|---|
| 1 | D0140 | Limited oral evaluation — problem focused | — | — | Basic | $85.00 |
| 2 | D0220 | Periapical radiograph — first image | #30 | — | Basic | $35.00 |
| 3 | D0230 | Periapical radiograph — additional image | — | — | Basic | $30.00 |
| 4 | D7140 | Extraction, erupted tooth — simple | #30 | — | Oral Surgery | $185.00 |
| | | **Total billed** | | | | **$335.00** |

**Expected Adjudication — Line by Line:**

| Line | CDT | Submitted | Write-Off | Allowed | Deductible | Rate | Plan Paid | Patient |
|---|---|---|---|---|---|---|---|---|
| 1 | D0140 | $85.00 | $10.00 | $75.00 | $50.00 | 80% | $20.00 | $55.00 |
| 2 | D0220 | $35.00 | $5.00 | $30.00 | $0.00 | 80% | $24.00 | $6.00 |
| 3 | D0230 | $30.00 | $5.00 | $25.00 | $0.00 | 80% | $20.00 | $5.00 |
| 4 | D7140 | $185.00 | $25.00 | $160.00 | $0.00 | 70% | $112.00 | $48.00 |
| | **Total** | **$335.00** | **$45.00** | **$290.00** | **$50.00** | | **$176.00** | **$114.00** |

> **Clearinghouse note — deductible sequencing:** The full $50 annual individual deductible is applied to line 1 (D0140) only. Lines 2, 3, and 4 carry $0 deductible because the deductible is fully met on line 1. Maintain service line order on submission so adjudication sequencing reflects this correctly.

> **Clearinghouse note — mixed benefit tiers:** Lines 1, 2, and 3 (D0140, D0220, D0230) are Basic services covered at 80% under this Cigna plan. Line 4 (D7140) is Oral Surgery, covered at 70%. These are two different coinsurance rates on the same claim date. This is expected and correct. If a remittance returns all four lines at the same rate, verify benefit tier assignment against the plan document.

> **Clearinghouse note — new patient:** Jason has no prior claims history with this practice or this payer for plan year 2026. His $50 annual individual deductible had not previously been applied. After this claim processes, his deductible balance is $0 for the remainder of plan year 2026.

---

## 6. Laura Jennings — Prior Authorization, Root Canal Therapy, and Crown

### 6.1 Business Overview

Laura Jennings calls Harrodsburg Family Dentistry reporting worsening pain in her upper right jaw over the past week. She is new to the practice and a recent enrollee on her employer's dental plan. The office brings her in the same day.

Dr. Philip Barsotti examines Laura, takes X-rays, and determines that tooth #3 — the upper right first molar — has irreversible pulpitis. The nerve inside the tooth is dying, which is the source of her pain. Root canal therapy is the appropriate treatment to save the tooth, followed by a porcelain crown to protect what remains of the tooth structure afterward. Because Laura is in significant pain, Dr. Barsotti provides emergency palliative treatment at this first visit to relieve her discomfort while the practice prepares the necessary paperwork.

Laura's plan through Anthem Blue Cross and Blue Shield of Kentucky requires prior authorization before root canal therapy and crown procedures can be performed. The practice submits an authorization request to Anthem with supporting X-rays and a clinical narrative, and Anthem approves the root canal and crown within a week. The core buildup — a foundation placed inside the tooth to support the crown if insufficient natural tooth structure remains — is conditionally approved pending confirmation at the time of the crown preparation appointment.

The root canal is completed two weeks after the initial visit. The following month, Dr. Barsotti prepares the tooth for the crown, confirms that the buildup is clinically necessary, documents this in a narrative submitted with the claim, and seats the final crown at the same appointment. The conditional authorization is satisfied. All three treatment services are processed by Anthem under the original authorization number.

Laura's total out-of-pocket cost for the year across all three dental visits is $835.

| | |
|---|---|
| **Patient** | Laura Jennings · DOB January 14, 1989 |
| **Payer** | Anthem Blue Cross and Blue Shield of Kentucky · Member ID JNG5027741 |
| **Employer group** | Ohio River Logistics · Group ORL-2026-001 |
| **Encounters** | 3 (June 3, June 17, and July 15, 2026) |
| **Authorization number** | ANT-PREAUTH-2026-JNG001 *(synthetic)* |
| **Total submitted** | $2,955.00 |
| **Total plan paid** | $1,565.00 |
| **Total patient paid** | $835.00 |

---

### 6.2 Encounter Summary for Clinical Staff

#### Encounter 1 — Emergency Examination and Palliative Treatment
**Date of Service:** June 3, 2026
**Visit Type:** Same-day emergency examination — new patient to this practice

**Services Performed:**

| CDT | Description | Tooth |
|---|---|---|
| D0140 | Limited oral evaluation — problem focused | — |
| D0220 | Periapical radiographic image — first image | #3 |
| D0230 | Periapical radiographic image — each additional image | #3 |
| D9110 | Palliative (emergency) treatment of dental pain — minor procedure | #3 |

**Clinical Findings:** Patient presented with a one-week history of increasing spontaneous pain in the upper right quadrant with lingering cold sensitivity and percussion sensitivity on tooth #3. New patient to this practice. Periapical radiographs taken of tooth #3 (upper right first molar) from multiple angles.

Radiographic and clinical findings: Existing composite restoration on tooth #3, mesio-occlusal-distal extent. Significant carious lesion involving mesial and occlusal surfaces beneath existing restoration. Periapical radiolucency at root apex consistent with early pulpal necrosis. Tooth #3 non-responsive to cold reversal following prolonged cold testing. Diagnosis: irreversible pulpitis with early periapical periodontitis (ICD-10-CM: K04.01). Root canal therapy indicated. Full-coverage crown required post-endodontic treatment to protect remaining tooth structure and restore occlusal function.

Palliative emergency treatment provided to relieve acute pain and stabilize the tooth. Prior authorization for D3330 (molar root canal therapy), D2740 (porcelain/ceramic crown), and D2393 (core buildup, conditional) to be submitted to Anthem BCBS Kentucky.

**Outcome:** Pain relieved at appointment. Root canal therapy appointment to be scheduled upon receipt of authorization approval.

---

#### Prior Authorization
**Submitted:** June 4, 2026
**Approved:** June 10, 2026
**Authorization Number:** ANT-PREAUTH-2026-JNG001
**Valid Through:** December 31, 2026

Supporting documentation submitted: periapical radiographs from June 3 visit (D0220 and D0230), completed clinical narrative, ICD-10-CM diagnosis K04.01 (irreversible pulpitis), tooth #3.

**Authorization Decisions:**

| CDT | Description | Allowed Amount | Benefit Category | Decision |
|---|---|---|---|---|
| D3330 | Root canal therapy, molar | $975.00 | Basic — 80% | Approved (A1) |
| D2740 | Crown, porcelain/ceramic substrate | $1,050.00 | Major — 50% | Approved (A1) |
| D2393 | Resin-based composite core buildup, posterior | $200.00 | Basic — 80% | Conditional (A3) |

**Condition on D2393:** Approved contingent upon submission of clinical documentation at the crown preparation appointment confirming insufficient remaining tooth structure for crown retention without buildup.

> **Clinical note — D2393 billing sequence:** D2393 must not be billed on the same date of service as the root canal (D3330). Anthem will deny the buildup as inclusive of the endodontic fee if same-day. Bill D2393 at the crown preparation appointment (D2740), with supporting clinical narrative confirming remaining tooth structure assessment.

---

#### Encounter 2 — Root Canal Therapy
**Date of Service:** June 17, 2026
**Visit Type:** Endodontic treatment

**Services Performed:**

| CDT | Description | Tooth |
|---|---|---|
| D3330 | Endodontic therapy, molar tooth (excluding final restoration) | #3 |

**Clinical Findings:** Patient presents for scheduled root canal therapy on tooth #3 (upper right first molar). Prior authorization confirmed — ANT-PREAUTH-2026-JNG001. Local anesthesia administered. Rubber dam isolation. Access preparation through existing restoration. All canals negotiated. Working length established radiographically. Canal preparation using rotary files. Irrigation with sodium hypochlorite and EDTA. Canals dried and obturated with gutta-percha and sealer using warm vertical compaction. Post-obturation radiograph confirms acceptable obturation within 0–2 mm of radiographic apex in all canals. Coronal seal placed. Temporary restoration placed. Patient tolerated procedure well. No complications.

**Outcome:** Root canal therapy complete on tooth #3. Post-operative instructions provided. Crown preparation to be scheduled in four to six weeks.

---

#### Encounter 3 — Crown Preparation, Core Buildup, and Crown Delivery
**Date of Service:** July 15, 2026
**Visit Type:** Crown preparation and delivery — same appointment

**Services Performed:**

| CDT | Description | Tooth | Surface |
|---|---|---|---|
| D2393 | Resin-based composite core buildup, posterior | #3 | MO, D |
| D2740 | Crown, porcelain/ceramic substrate | #3 | — |

**Clinical Findings:** Patient returns for crown preparation on tooth #3. Periapical radiograph confirms successful obturation from June 17. Healing progressing normally. Crown preparation initiated. Assessment of remaining coronal tooth structure following endodontic access and removal of carious and undermined structure: approximately 35% of original coronal structure remaining. Insufficient retention form without buildup. Core buildup with resin composite placed to restore adequate height and retention form for crown preparation. Crown preparation completed. Final impressions taken. Permanent porcelain/ceramic crown returned from laboratory and seated at this appointment. Pre-cementation fit and occlusion verified. Crown cemented with resin-modified glass ionomer. Occlusal contacts confirmed in centric and lateral excursions. Margins visually acceptable.

Conditional authorization requirement satisfied: clinical narrative documenting remaining tooth structure (approximately 35%) submitted with claim. Crown seat date: July 15, 2026.

**Outcome:** Crown seated and cemented on tooth #3. Core buildup documented and billed. Treatment for tooth #3 complete. Patient to continue with routine preventive care.

---

### 6.3 Claims and Billing Summary for Clearinghouse Submission

#### Claim 1 of 3 — Emergency Examination and Palliative Treatment

| Field | Value |
|---|---|
| Patient name | Laura Jennings |
| Date of birth | January 14, 1989 |
| Member ID | JNG5027741 |
| Subscriber | Laura Jennings (self) |
| Employer group | Ohio River Logistics |
| Group number | ORL-2026-001 |
| Payer | Anthem Blue Cross and Blue Shield of Kentucky |
| EDI payer ID | 026033 |
| EDI gateway | Availity (Anthem's designated EDI partner) |
| Rendering provider | Philip Barsotti, DMD · NPI 1568030203 |
| Billing organization | Harrodsburg Family Dentistry · NPI 1245734763 |
| Practice address | 517 Legion Dr, Harrodsburg, KY 40330 |
| Date of service | June 3, 2026 |
| Place of service | Office (11) |
| Prior authorization | Not required for these services |
| Visit notes | Same-day emergency appointment. New patient, new enrollee. One-week history of increasing upper right jaw pain. Periapical radiographs taken. Root canal and crown treatment plan established. Prior authorization to follow. |

**Service Lines:**

| Line | CDT | Description | Tooth | Surface | Benefit Category | Fee |
|---|---|---|---|---|---|---|
| 1 | D0140 | Limited oral evaluation — problem focused | — | — | Basic | $80.00 |
| 2 | D0220 | Periapical radiograph — first image | #3 | — | Basic | $35.00 |
| 3 | D0230 | Periapical radiograph — additional image | #3 | — | Basic | $30.00 |
| 4 | D9110 | Palliative emergency treatment of dental pain | #3 | — | Basic | $60.00 |
| | | **Total billed** | | | | **$205.00** |

**Expected Adjudication:**

| | Amount |
|---|---|
| Submitted | $205.00 |
| PPO contractual write-off | −$30.00 |
| Allowed | $175.00 |
| Deductible applied | −$50.00 (full annual individual deductible applied to line 1) |
| Post-deductible eligible | $125.00 |
| Plan paid (80% of $125.00) | $100.00 |
| Patient responsibility | $75.00 |
| Payment type | Partial |

> **Clearinghouse note:** Full $50 annual individual deductible applied to line 1 (D0140) only. Lines 2, 3, and 4 carry $0 deductible — fully exhausted on line 1. Laura is a new enrollee with no prior claims this plan year. After this claim, her deductible balance is $0 for plan year 2026.

---

#### Claim 2 of 3 — Root Canal Therapy

| Field | Value |
|---|---|
| Patient name | Laura Jennings |
| Date of birth | January 14, 1989 |
| Member ID | JNG5027741 |
| Subscriber | Laura Jennings (self) |
| Employer group | Ohio River Logistics |
| Group number | ORL-2026-001 |
| Payer | Anthem Blue Cross and Blue Shield of Kentucky |
| EDI payer ID | 026033 |
| EDI gateway | Availity |
| Rendering provider | Philip Barsotti, DMD · NPI 1568030203 |
| Billing organization | Harrodsburg Family Dentistry · NPI 1245734763 |
| Practice address | 517 Legion Dr, Harrodsburg, KY 40330 |
| Date of service | June 17, 2026 |
| Place of service | Office (11) |
| **Prior authorization** | **Required — ANT-PREAUTH-2026-JNG001** |
| Related claim | Claim 1 of 3 — initial emergency visit June 3, 2026 |

**Service Lines:**

| Line | CDT | Description | Tooth | Surface | Benefit Category | Fee |
|---|---|---|---|---|---|---|
| 1 | D3330 | Endodontic therapy, molar tooth | #3 | — | Basic | $1,150.00 |
| | | **Total billed** | | | | **$1,150.00** |

**Expected Adjudication:**

| | Amount |
|---|---|
| Submitted | $1,150.00 |
| PPO contractual write-off | −$175.00 |
| Allowed (per predetermination) | $975.00 |
| Deductible applied | $0.00 — met on June 3 |
| Plan paid (80%) | $780.00 |
| Patient coinsurance (20%) | $195.00 |
| **Patient responsibility** | **$195.00** |
| Payment type | Partial |

> **Clearinghouse note:** Authorization number ANT-PREAUTH-2026-JNG001 must appear in the prior authorization reference field on this claim. Anthem will not process without it. The allowed amount of $975.00 was established at predetermination — do not expect a different allowed amount on adjudication. Post-obturation periapical radiograph should be retained in the patient record to support the crown claim to follow.

---

#### Claim 3 of 3 — Crown Preparation, Core Buildup, and Crown Delivery

| Field | Value |
|---|---|
| Patient name | Laura Jennings |
| Date of birth | January 14, 1989 |
| Member ID | JNG5027741 |
| Subscriber | Laura Jennings (self) |
| Employer group | Ohio River Logistics |
| Group number | ORL-2026-001 |
| Payer | Anthem Blue Cross and Blue Shield of Kentucky |
| EDI payer ID | 026033 |
| EDI gateway | Availity |
| Rendering provider | Philip Barsotti, DMD · NPI 1568030203 |
| Billing organization | Harrodsburg Family Dentistry · NPI 1245734763 |
| Practice address | 517 Legion Dr, Harrodsburg, KY 40330 |
| Date of service | July 15, 2026 |
| Place of service | Office (11) |
| **Prior authorization** | **Required — ANT-PREAUTH-2026-JNG001** |
| Related claim | Claim 2 of 3 — root canal June 17, 2026 |
| Crown seat date | July 15, 2026 |

**Service Lines:**

| Line | CDT | Description | Tooth | Surface | Benefit Category | Fee |
|---|---|---|---|---|---|---|
| 1 | D2393 | Resin-based composite core buildup, posterior | #3 | MO, D | Basic | $250.00 |
| 2 | D2740 | Crown, porcelain/ceramic substrate | #3 | — | Major | $1,350.00 |
| | | **Total billed** | | | | **$1,600.00** |

**Expected Adjudication — Line by Line:**

| Line | CDT | Submitted | Write-Off | Allowed | Deductible | Rate | Plan Paid | Patient |
|---|---|---|---|---|---|---|---|---|
| 1 | D2393 | $250.00 | $50.00 | $200.00 | $0.00 | 80% | $160.00 | $40.00 |
| 2 | D2740 | $1,350.00 | $300.00 | $1,050.00 | $0.00 | 50% | $525.00 | $525.00 |
| | **Total** | **$1,600.00** | **$350.00** | **$1,250.00** | **$0.00** | | **$685.00** | **$565.00** |

> **Clearinghouse note — D2393 conditional authorization:** Anthem's approval for D2393 was conditional. A clinical narrative must accompany this claim confirming that insufficient tooth structure remains for crown retention without buildup. Suggested narrative: *"Endodontic therapy completed 2026-06-17 on tooth #3. Approximately 35% of original coronal tooth structure remaining following endodontic access and caries excavation. Retention form insufficient for crown without core buildup. Resin composite buildup placed July 15, 2026 prior to crown preparation."* D2393 will be denied without this documentation regardless of the authorization on file.

> **Clearinghouse note — billing sequence:** Both D2393 and D2740 are billed on July 15, 2026 — the crown appointment date. This is correct. Billing D2393 on the same date as D3330 (June 17) would result in a denial. The buildup is treated as inclusive of the root canal fee when billed same-day.

> **Clearinghouse note — mixed benefit tiers:** D2393 is Basic, covered at 80%. D2740 is Major, covered at 50%. Two different rates on the same claim. This is expected and correct.

**Year-to-Date Summary — Laura Jennings:**

| Encounter | Date | Submitted | Write-Off | Allowed | Plan Paid | Patient Paid |
|---|---|---|---|---|---|---|
| Emergency exam | Jun 3, 2026 | $205.00 | $30.00 | $175.00 | $100.00 | $75.00 |
| Root canal | Jun 17, 2026 | $1,150.00 | $175.00 | $975.00 | $780.00 | $195.00 |
| Crown and buildup | Jul 15, 2026 | $1,600.00 | $350.00 | $1,250.00 | $685.00 | $565.00 |
| **Year total** | | **$2,955.00** | **$555.00** | **$2,400.00** | **$1,565.00** | **$835.00** |

*Annual deductible: $50.00 — fully met at Encounter 1 on June 3. No deductible applied to Encounters 2 or 3.*

---

## 7. Dataset Reference Summary

### FHIR Bundle Inventory

| Bundle File | Patient | Standard(s) | Contents |
|---|---|---|---|
| emily_watkins_fhir_bundle.json | Emily Watkins | CARIN BB Oral | Encounter 1 claim and EOB — preventive visit |
| emily_watkins_encounter2_fhir_bundle.json | Emily Watkins | CARIN BB Oral | Encounter 2 claim and EOB — composite restoration |
| jason_morales_encounter1_fhir_bundle.json | Jason Morales | CARIN BB Oral | Encounter 1 claim and EOB — emergency exam and extraction |
| laura_jennings_b1_initial_visit.json | Laura Jennings | CARIN BB Oral | Encounter 1 claim and EOB — emergency exam |
| laura_jennings_b2_dtr.json | Laura Jennings | Da Vinci DTR | Questionnaire, QuestionnaireResponse, Condition K04.01, DocumentReference |
| laura_jennings_b3_pas_request.json | Laura Jennings | Da Vinci PAS | Prior authorization Claim (use: preauthorization) |
| laura_jennings_b4_pas_response.json | Laura Jennings | Da Vinci PAS | ClaimResponse with preAuthRef ANT-PREAUTH-2026-JNG001 |
| laura_jennings_b5_rct.json | Laura Jennings | CARIN BB Oral | Encounter 2 claim and EOB — root canal therapy |
| laura_jennings_b6_crown.json | Laura Jennings | CARIN BB Oral | Encounter 3 claim and EOB — crown and buildup |

### Patient Financial Summary

| Patient | Payer | Encounters | Submitted | Plan Paid | Patient Paid |
|---|---|---|---|---|---|
| Emily Watkins | Delta Dental of Kentucky | 2 | $400.00 | $308.00 | $72.00 |
| Jason Morales | Cigna Dental Health of Kentucky | 1 | $335.00 | $176.00 | $114.00 |
| Laura Jennings | Anthem BCBS Kentucky | 3 | $2,955.00 | $1,565.00 | $835.00 |
| **Dataset total** | | **6** | **$3,690.00** | **$2,049.00** | **$1,021.00** |

### Key CDT Codes in This Dataset

| CDT | Description | Patient(s) | Benefit Category |
|---|---|---|---|
| D0120 | Periodic oral evaluation | Emily | Preventive |
| D0140 | Limited oral evaluation — problem focused | Jason, Laura | Basic |
| D0220 | Periapical radiograph — first image | Jason, Laura | Basic |
| D0230 | Periapical radiograph — additional image | Jason, Laura | Basic |
| D0274 | Bitewing radiographs — four images | Emily | Preventive |
| D1110 | Prophylaxis — adult | Emily | Preventive |
| D2391 | Resin composite — one surface, posterior | Emily | Basic |
| D2393 | Resin composite core buildup, posterior | Laura | Basic |
| D2740 | Crown, porcelain/ceramic substrate | Laura | Major |
| D3330 | Endodontic therapy, molar tooth | Laura | Basic |
| D7140 | Extraction, erupted tooth — simple | Jason | Oral Surgery |
| D9110 | Palliative emergency treatment of dental pain | Laura | Basic |

### Synthetic Test Identifiers

The following identifiers are created solely for testing purposes and have no real-world counterparts.

| Patient | Identifier | Value |
|---|---|---|
| Emily | Group number | KYRHC-2026-001 |
| Emily | Member ID | WTK4592031 |
| Jason | Group number | ORM-2026-001 |
| Jason | Member ID | MRL8421137 |
| Laura | Group number | ORL-2026-001 |
| Laura | Member ID | JNG5027741 |
| Laura | Authorization number | ANT-PREAUTH-2026-JNG001 |

### Verification Links

```
Harrodsburg Family Dentistry — Practice NPI 1245734763:
  https://npiregistry.cms.hhs.gov/search?number=1245734763

Dr. Philip Barsotti, DMD — Provider NPI 1568030203:
  https://npiregistry.cms.hhs.gov/search?number=1568030203

Onyx OnyxOS API Documentation:
  https://docs.safhir.io/onyxos_api_documentation.html

Onyx Developer Portal:
  https://portal.safhir.io
```

---

*This document is prepared in support of the OHIA Connectathon and the January 2027 HL7 dental FHIR implementation guide ballot. All patient names, member IDs, employer groups, plan identifiers, and authorization numbers are synthetic test data with no real-world counterparts. Provider NPIs and payer EDI IDs are real, publicly available identifiers used here solely in a synthetic test context. OHIA Facilitator: Mark Marciante, Leavitt Partners.*
