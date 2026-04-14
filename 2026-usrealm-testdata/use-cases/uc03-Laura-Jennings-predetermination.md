# OHIA Connectathon — Dental Interoperability Test Dataset- Use Case #3 
## 3.UC03-Laura Jennings — predetermination, Root Canal Therapy, and Crown

### 3.1 Business Overview

Laura Jennings calls Harrodsburg Family Dentistry reporting worsening pain in her upper right jaw over the past week. She is new to the practice and a recent enrollee on her employer's dental plan. The office brings her in the same day.

Dr. Philip Barsotti examines Laura, takes X-rays, and determines that tooth #3 — the upper right first molar — has irreversible pulpitis. The nerve inside the tooth is dying, which is the source of her pain. Root canal therapy is the appropriate treatment to save the tooth, followed by a porcelain crown to protect what remains of the tooth structure afterward. Because Laura is in significant pain, Dr. Barsotti provides emergency palliative treatment at this first visit to relieve her discomfort while the practice prepares the necessary paperwork.

Laura's plan through Anthem Blue Cross and Blue Shield of Kentucky requires predetermination before root canal therapy and crown procedures can be performed. The practice submits an authorization request to Anthem with supporting X-rays and a clinical narrative, and Anthem approves the root canal and crown within a week. The core buildup — a foundation placed inside the tooth to support the crown if insufficient natural tooth structure remains — is conditionally approved pending confirmation at the time of the crown preparation appointment.

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

### 3.2 Encounter Summary for Clinical Staff

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

Palliative emergency treatment provided to relieve acute pain and stabilize the tooth. predetermination for D3330 (molar root canal therapy), D2740 (porcelain/ceramic crown), and D2393 (core buildup, conditional) to be submitted to Anthem BCBS Kentucky.

**Outcome:** Pain relieved at appointment. Root canal therapy appointment to be scheduled upon receipt of authorization approval.

---

#### predetermination
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

**Clinical Findings:** Patient presents for scheduled root canal therapy on tooth #3 (upper right first molar). predetermination confirmed — ANT-PREAUTH-2026-JNG001. Local anesthesia administered. Rubber dam isolation. Access preparation through existing restoration. All canals negotiated. Working length established radiographically. Canal preparation using rotary files. Irrigation with sodium hypochlorite and EDTA. Canals dried and obturated with gutta-percha and sealer using warm vertical compaction. Post-obturation radiograph confirms acceptable obturation within 0–2 mm of radiographic apex in all canals. Coronal seal placed. Temporary restoration placed. Patient tolerated procedure well. No complications.

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

### 3.3 Claims and Billing Summary for Clearinghouse Submission

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
| predetermination | Not required for these services |
| Visit notes | Same-day emergency appointment. New patient, new enrollee. One-week history of increasing upper right jaw pain. Periapical radiographs taken. Root canal and crown treatment plan established. predetermination to follow. |

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
| **predetermination** | **Required — ANT-PREAUTH-2026-JNG001** |
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

> **Clearinghouse note:** Authorization number ANT-PREAUTH-2026-JNG001 must appear in the predetermination reference field on this claim. Anthem will not process without it. The allowed amount of $975.00 was established at predetermination — do not expect a different allowed amount on adjudication. Post-obturation periapical radiograph should be retained in the patient record to support the crown claim to follow.

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
| **predetermination** | **Required — ANT-PREAUTH-2026-JNG001** |
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

*This document is prepared in support of the OHIA Connectathon. All patient names, member IDs, employer groups, plan identifiers, and authorization numbers are synthetic test data with no real-world counterparts. Provider NPIs and payer EDI IDs are real, publicly available identifiers used here solely in a synthetic test context. OHIA Facilitator: Mark Marciante, Leavitt Partners. Provided for use only as part of OHIA or Connectathon events.*
