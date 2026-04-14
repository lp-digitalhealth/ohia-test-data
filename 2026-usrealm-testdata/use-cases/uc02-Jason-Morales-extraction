# OHIA Connectathon — Dental Interoperability Test Dataset
## Patient Use Cases: Clinical Scenarios, Encounter Summaries, and Claims Data
**Jason Morales** is a new patient in acute pain who presents for a same-day emergency exam and leaves with an extraction. His single visit generates four procedure lines across two different benefit tier rates — basic services at 80% and oral surgery at 70% — with a deductible that exhausts on the first line. His extraction of tooth #30 introduces the dental-specific data element central to the CARIN Blue Button Oral Profile: the ability to record and retrieve a tooth number in a machine-readable field. His scenario tests whether a patient-facing app can display that correctly, and whether a provider app can search across all patients for claims involving a specific tooth.

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

### Test Account Credentials

| Patient | Test Username | Member ID |
|---|---|---|

| Jason Morales |MRL8421137 |

Passwords are distributed via the OHIA coordination channel and are not published in this document.

---

## 1. Jason Morales — Emergency New-Patient Visit with Extraction

### 1.1 Business Overview

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

### 1.2 Encounter Summary for Clinical Staff

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

### 1.3 Claims and Billing Summary for Clearinghouse Submission

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
| predetermination | Not required |
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

