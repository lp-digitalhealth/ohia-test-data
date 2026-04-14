
# OHIA Connectathon — Dental Interoperability Test Dataset-Use Case #1
## UC01-Emily Watkins — Routine Preventive Care and Single-Surface Restoration

### 1.1 Business Overview

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

### 1.2 Encounter Summary for Clinical Staff

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

### 1.3 Claims and Billing Summary for Clearinghouse Submission

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
| predetermination | Not required |

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
| predetermination | Not required |
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
*This document is prepared in support of the OHIA Connectathon and the January 2027 HL7 dental FHIR implementation guide ballot. All patient names, member IDs, employer groups, plan identifiers, and authorization numbers are synthetic test data with no real-world counterparts. Provider NPIs and payer EDI IDs are real, publicly available identifiers used here solely in a synthetic test context. OHIA Facilitator: Mark Marciante, Leavitt Partners.*
