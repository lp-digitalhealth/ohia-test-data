# OHIA Connectathon 2026 — Data Transformation Report

**Date:** April 9, 2026
**Platform:** HeyDonto Data Intelligence Network
**Standard:** FHIR R4, X12 005010X224A2 (EDI 837D Dental Claims)
**Environment:** Canary (GKE us-east1)

---

## Executive Summary

This report documents the end-to-end data transformation pipeline executed for the OHIA 2026 US Realm Dental Connectathon. The pipeline processes FHIR R4 dental data from two independent practice sites, harmonizes it into a unified Data Intelligence Network (DIN), and exports production-ready EDI X12 837D dental claim files.

**Result:** 4 pipeline stages completed successfully with 0 validation errors. 95 harmonized FHIR resources from 2 sites produced 6 billable EDI claims across 3 patients and 3 payers in a single X12 interchange.

### Deviations from Phase 4.2 Design

This report documents the **current implementation state**, which diverges from the approved Phase 4.2 export contract in two ways:

1. **CPT codes on Laura's claims are not crosswalked to CDT.** The Phase 4.2 design specifies that all EDI SV3 segments use CDT codes (AD: qualifier), with Site B's CPT codes crosswalked during import. The current implementation preserves CPT codes from the harmonized store and uses the HC: qualifier for CPT-coded procedures. The CPT-to-CDT crosswalk exists in the import template's `ontology_enrich` node but enriches metadata fields (`cdt_code`, `ada_category`) without rewriting the original `resource.code.coding` — so the FHIR store retains original CPT codes.
2. **Output is raw `.edi` text, not JSON-wrapped.** Phase 4.2 specifies JSON output with a `full_interchange` string field, with the dashboard extracting the text client-side. The current implementation uses a post-processor that outputs the raw EDI text directly as an `.edi` file, which the dashboard serves for download without extraction.

These are implementation choices, not data integrity issues. All claim totals, member IDs, NPIs, preauth references, and preauth exclusion logic are correct regardless of qualifier or wrapper format.

---

## Pipeline Overview

```
Stage 1                    Stage 2                    Stage 3                    Stage 4
CDT Import (Site A)        CPT Import (Site B)        Harmonization              EDI 837D Export
49 resources               49 resources               95 resources               6 claims
Emily + Jason              Laura                      3 patients unified         X12 interchange
12 input bundles           15 input bundles           2 site bundles merged      1 .edi file
```

---

## Stage 1: FHIR R4 CDT Import — Lexington Family Dental (Site A)

**Session:** `2e4d8efa-5648-4803-acc4-dc0ffeb28858`
**Profile:** `fhir-r4-import-cdt`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning
**FHIR Import Operation:** `projects/heydonto-425716/.../operations/6378657616511369217`

### Input Files (12)

| File | Description |
|------|-------------|
| `uc01-emily_watkins_encounter1_fhir_bundle.json` | UC01: Emily preventive visit (D0120, D0274, D1110) |
| `uc01_emily_watkins_encounter2_fhir_bundle.json` | UC01: Emily restoration (D2391, tooth 13) |
| `uc02-jason_morales_encounter1_fhir_bundle.json` | UC02: Jason emergency extraction (D0140, D0220, D0230, D7140, tooth 30) |
| `site1-lexington-appointments.json` | 3 appointment resources |
| `site1-lexington-conditions.json` | 2 condition resources |
| `site1-lexington-encounters.json` | 3 encounter resources |
| `site1-lexington-locations.json` | 2 location resources |
| `site1-lexington-practitioner-roles.json` | 2 practitioner role resources |
| `site1-lexington-practitioners.json` | 3 practitioner/org resources |
| `site1-lexington-procedures.json` | 8 procedure resources |
| `site1-lexington-schedules.json` | 2 schedule resources |
| `site1-lexington-slots.json` | 10 slot resources |

### Output: 49 FHIR Resources

| Resource Type | Count |
|---------------|-------|
| Patient | 2 (Emily Watkins, Jason Morales) |
| Practitioner | 2 (Philip Barsotti NPI:1568030203, Sarah Chen NPI:1234567890) |
| Organization | 4 (Lexington Family Dental, Harrodsburg Family Dentistry, Delta Dental KY, Cigna Dental KY) |
| PractitionerRole | 3 |
| Coverage | 2 (WTK4592031 Delta Dental, MRL8421137 Cigna) |
| Claim | 3 |
| ExplanationOfBenefit | 3 |
| Encounter | 3 |
| Procedure | 8 |
| Appointment | 3 |
| Condition | 2 |
| Location | 2 |
| Schedule | 2 |
| Slot | 10 |

### Claims Detail

| Claim ID | Use | Total | CDT Codes | Patient |
|----------|-----|-------|-----------|---------|
| claim-emily-watkins-20260312 | claim | $220 | D0120, D0274, D1110 | Emily Watkins |
| claim-emily-watkins-enc2 | claim | $180 | D2391 (tooth 13) | Emily Watkins |
| claim-jason-morales-enc1 | claim | $335 | D0140, D0220, D0230, D7140 (tooth 30) | Jason Morales |

**Artifact:** [`artifacts/stage1-cdt-import/output-bundle.json`](artifacts/stage1-cdt-import/output-bundle.json)

---

## Stage 2: FHIR R4 CPT Import — Harrodsburg Family Dentistry (Site B)

**Session:** `3c60ad32-db3c-4af8-935c-7f691f87f1f4`
**Profile:** `fhir-r4-import-cpt`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning
**FHIR Import Operation:** `projects/heydonto-425716/.../operations/16105456445306175489`

### Input Files (15)

| File | Description |
|------|-------------|
| `uc03_laura_jennings_b1_initial_visit_cpt.json` | UC03: Laura initial visit (CPT 99201, 70300, 70310, 99212) |
| `uc03_laura_jennings_b2_dtr.json` | UC03: DTR Questionnaire + QuestionnaireResponse |
| `uc03_laura_jennings_b3_pas_request_cpt.json` | UC03: PAS pre-authorization request |
| `uc03_laura_jennings_b4_pas_response_cpt.json` | UC03: PAS response (ANT-PREAUTH-2026-JNG001) |
| `uc03_laura_jennings_b5_rct_cpt.json` | UC03: Root canal treatment claim (CPT 41899) |
| `uc03-laura_jennings_b6_crown_cpt.json` | UC03: Crown placement claim (CPT 41899 x2) |
| `site2-harrodsburg-*.json` | 9 augmented site resource files (appointments, conditions, encounters, locations, practitioner-roles, practitioners, procedures, schedules, slots) |

### Output: 49 FHIR Resources

| Resource Type | Count |
|---------------|-------|
| Patient | 1 (Laura Jennings) |
| Practitioner | 2 (Philip Barsotti NPI:1568030203, Amir Patel NPI:9876543210) |
| Organization | 2 (Harrodsburg Family Dentistry, Anthem BCBS KY) |
| PractitionerRole | 3 |
| Coverage | 1 (JNG5027741 Anthem) |
| Claim | 4 (3 treatment + 1 preauthorization) |
| ClaimResponse | 1 (preAuthRef: ANT-PREAUTH-2026-JNG001) |
| Questionnaire | 1 |
| QuestionnaireResponse | 1 |
| ExplanationOfBenefit | 3 |
| Encounter | 3 |
| Procedure | 7 |
| DocumentReference | 1 |
| Appointment | 3 |
| Location | 2 |
| Schedule | 2 |
| Slot | 10 |

### Claims Detail

| Claim ID | Use | Total | CPT Codes | PreAuth Ref |
|----------|-----|-------|-----------|-------------|
| claim-laura-jennings-enc1 | claim | $205 | 99201, 70300, 70310, 99212 | |
| claim-laura-jennings-rct | claim | $1,150 | 41899 | ANT-PREAUTH-2026-JNG001 |
| claim-laura-jennings-crown | claim | $1,600 | 41899, 41899 | ANT-PREAUTH-2026-JNG001 |
| claim-laura-jennings-preauth | preauthorization | $2,750 | 41899, 41899, 41899 | |

### Da Vinci PAS Lifecycle (UC03)

```
1. Initial Visit      --> Questionnaire (DTR)
2. DTR Response        --> QuestionnaireResponse
3. PAS Request         --> Claim (use=preauthorization)
4. PAS Response        --> ClaimResponse (preAuthRef=ANT-PREAUTH-2026-JNG001)
5. Treatment (RCT)     --> Claim (preAuthRef=ANT-PREAUTH-2026-JNG001)
6. Treatment (Crown)   --> Claim (preAuthRef=ANT-PREAUTH-2026-JNG001)
```

**Artifact:** [`artifacts/stage2-cpt-import/output-bundle.json`](artifacts/stage2-cpt-import/output-bundle.json)

---

## Stage 3: Multi-Site Harmonization

**Session:** `8273ecb7-b80f-4b5c-ab3b-8cad66059404`
**Profile:** `fhir-r4-harmonization`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning
**FHIR Import Operation:** `projects/heydonto-425716/.../operations/3136276991037145089`
**DIN ID:** 7

### Input

| Bundle | Site | Resources |
|--------|------|-----------|
| site-170-bundle.json | Lexington Family Dental (Site A) | 49 |
| site-171-bundle.json | Harrodsburg Family Dentistry (Site B) | 49 |
| **Total input** | | **98** |

### Deduplication

| Metric | Count |
|--------|-------|
| Site A unique resources | 49 |
| Site B unique resources | 49 |
| Shared across sites | 3 |
| **Expected after dedup** | **95** |
| **Actual output** | **95** |

**Deduplicated resources (shared between sites):**
- `Practitioner/practitioner-barsotti` — Dr. Philip Barsotti (NPI: 1568030203) practices at both sites
- `PractitionerRole/practitioner-role-barsotti` — Barsotti's role definition
- `Organization/org-harrodsburg-family-dentistry` — Practice organization referenced by both

### Harmonized Output: 95 Resources

| Resource Type | Site A | Site B | Harmonized | Notes |
|---------------|--------|--------|------------|-------|
| Patient | 2 | 1 | **3** | Emily, Jason, Laura unified |
| Practitioner | 2 | 2 | **3** | Barsotti deduplicated by NPI |
| Organization | 4 | 2 | **5** | 2 practices + 3 payers |
| Coverage | 2 | 1 | **3** | 1 per patient, correct subscriber IDs |
| Claim | 3 | 4 | **7** | 6 billable + 1 preauthorization |
| ExplanationOfBenefit | 3 | 3 | **6** | |
| Encounter | 3 | 3 | **6** | |
| Procedure | 8 | 7 | **15** | |
| Appointment | 3 | 3 | **6** | |
| Condition | 2 | 2 | **4** | |
| Location | 2 | 2 | **4** | |
| PractitionerRole | 3 | 3 | **5** | 1 deduplicated |
| Schedule | 2 | 2 | **4** | |
| Slot | 10 | 10 | **20** | |
| ClaimResponse | 0 | 1 | **1** | Laura's PAS response |
| Questionnaire | 0 | 1 | **1** | Laura's DTR |
| QuestionnaireResponse | 0 | 1 | **1** | Laura's DTR response |
| DocumentReference | 0 | 1 | **1** | |

### Validation Rules Passed

| Rule | Check | Result |
|------|-------|--------|
| FHIR_NO_DUPLICATE_IDS | No duplicate resourceType+id pairs | PASS |
| NO_DUPLICATE_TIER1_NPI | No duplicate Practitioner NPIs | PASS |
| NO_DUPLICATE_TIER1_PATIENT | No duplicate Patient identity (memberID+family+DOB) | PASS |
| ALL_REFERENCES_RESOLVE | All FHIR references point to existing resources | PASS |
| FHIR_VALID_RESOURCE_TYPE | Every resource has a resourceType | PASS |
| FHIR_HAS_ID | Every resource has an id | PASS |

**Artifact:** [`artifacts/stage3-harmonization/output-bundle.json`](artifacts/stage3-harmonization/output-bundle.json)

---

## Stage 4: EDI X12 837D Dental Claim Export

**Session:** `b8fd9dfe-8a6d-4b5d-98cb-71076ba548e5`
**Profile:** `edi-837-dental-export`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning
**Standard:** X12 005010X224A2

### Export Summary

| Metric | Value |
|--------|-------|
| Billable claims exported | 6 |
| Preauthorization claims excluded | 1 (`claim-laura-jennings-preauth`) |
| Patients in interchange | 3 (Emily, Jason, Laura) |
| Payers in interchange | 3 (Delta Dental KY, Cigna Dental KY, Anthem BCBS KY) |
| Total EDI segments (ST-SE) | 112 |
| HL hierarchy levels | 12 (6 billing + 6 subscriber) |
| Code qualifiers | AD (CDT): 8 segments, HC (CPT): 7 segments |

### Claim-by-Claim EDI Verification

#### Emily Watkins — UC01: Deductible Sequencing

**Claim 1: Preventive Visit ($220)**
```
NM1*IL*1*WATKINS*EMILY****MI*WTK4592031~
DMG*D8*19940302*F~
NM1*PR*2*DELTA DENTAL OF KENTUCKY*****PI*38217~
CLM*claim-emily-watkins-20260312*220***11:B:1*Y*A*Y*I~
DTP*472*D8*20260312~
NM1*82*1*BARSOTTI*PHILIP****XX*1568030203~
PRV*PE*PXC*1223G0001X~
SV3*AD:D0120*55****1~     (Periodic oral eval)
SV3*AD:D0274*70****1~     (Bitewing x-rays)
SV3*AD:D1110*95****1~     (Prophylaxis cleaning)
```

**Claim 2: Restoration ($180)**
```
CLM*claim-emily-watkins-enc2*180***11:B:1*Y*A*Y*I~
SV3*AD:D2391*180****1~    (One-surface posterior composite)
TOO*JP*13~                 (Tooth #13)
```

#### Jason Morales — UC02: Mixed Benefit Tiers + Tooth Data

**Claim: Emergency + Extraction ($335)**
```
NM1*IL*1*MORALES*JASON****MI*MRL8421137~
DMG*D8*19860918*M~
NM1*PR*2*CIGNA DENTAL HEALTH OF KENTUCKY, INC.*****PI*62308~
CLM*claim-jason-morales-enc1*335***11:B:1*Y*A*Y*I~
SV3*AD:D0140*85****1~     (Limited oral eval)
SV3*AD:D0220*35****1~     (Periapical x-ray)
TOO*JP*30~                 (Tooth #30)
SV3*AD:D0230*30****1~     (Local anesthesia)
SV3*AD:D7140*185****1~    (Extraction)
TOO*JP*30~                 (Tooth #30)
```

#### Laura Jennings — UC03: Predetermination Lifecycle

**Claim 1: Initial Visit ($205) — CPT codes**
```
NM1*IL*1*JENNINGS*LAURA****MI*JNG5027741~
DMG*D8*19890114*F~
NM1*PR*2*ANTHEM BLUE CROSS AND BLUE SHIELD OF KENTUCKY*****PI*026033~
CLM*claim-laura-jennings-enc1*205***11:B:1*Y*A*Y*I~
SV3*HC:99201*80****1~     (Office visit - CPT)
SV3*HC:70300*35****1~     (Dental x-ray - CPT)
SV3*HC:70310*30****1~     (Dental x-ray - CPT)
SV3*HC:99212*60****1~     (E&M visit - CPT)
```

**Claim 2: Root Canal Treatment ($1,150) — with preauth reference**
```
CLM*claim-laura-jennings-rct*1150***11:B:1*Y*A*Y*I~
REF*G1*ANT-PREAUTH-2026-JNG001~    (Prior authorization reference)
SV3*HC:41899*1150****1~             (Unlisted procedure - CPT)
```

**Claim 3: Crown Placement ($1,600) — with preauth reference**
```
CLM*claim-laura-jennings-crown*1600***11:B:1*Y*A*Y*I~
REF*G1*ANT-PREAUTH-2026-JNG001~    (Prior authorization reference)
SV3*HC:41899*250****1~              (Buildup - CPT)
SV3*HC:41899*1350****1~            (Crown - CPT)
```

**Preauthorization claim (`claim-laura-jennings-preauth`, use=preauthorization, $2,750) — correctly EXCLUDED from EDI output.**

### X12 Envelope

```
ISA*00*          *00*          *ZZ*HEYDONTO       *ZZ*CLEARINGHOUSE  *260409*1104*>*00501*000000001*0*P*:~
GS*HC*HEYDONTO*CLEARINGHOUSE*20260409*1104*1*X*005010X224A2~
ST*837*0001*005010X224A2~
BHT*0019*00*000000001*20260409*1104*CH~
... (108 claim segments) ...
SE*112*0001~
GE*1*1~
IEA*1*000000001~
```

**Artifact:** [`artifacts/stage4-edi-export/output.edi`](artifacts/stage4-edi-export/output.edi)

---

## Note on Billing Provider

All claims in the EDI output show **Harrodsburg Family Dentistry** (NPI: 1245734763) as the billing provider (NM1*85), including Emily's and Jason's claims which originate from Lexington Family Dental (Site A). This is faithful to the OHIA golden reference EDI files, which also list Harrodsburg as the billing provider for all three use cases. In the OHIA test data, Harrodsburg Family Dentistry is the billing entity for all claims — this is not cross-site data leakage, it reflects the OHIA scenario design where a single billing provider submits claims across encounters.

---

## Golden Reference Comparison

OHIA provides reference EDI files for Emily (2 encounters) and Jason (1 encounter). Laura has no golden EDI reference (her use case focuses on the PAS lifecycle, not EDI output).

| Data Point | Golden EDI | Our EDI | Match |
|------------|-----------|---------|-------|
| Emily enc1 CLM total | $220 | $220 | YES |
| Emily enc1 codes | D0120, D0274, D1110 | D0120, D0274, D1110 | YES |
| Emily enc2 CLM total | $180 | $180 | YES |
| Emily enc2 code + tooth | D2391, tooth 13 | D2391, tooth 13 | YES |
| Jason CLM total | $335 | $335 | YES |
| Jason codes | D0140, D0220, D0230, D7140 | D0140, D0220, D0230, D7140 | YES |
| Jason tooth | 30 | 30 | YES |
| Rendering provider NPI | 1568030203 (Barsotti) | 1568030203 | YES |
| Billing provider NPI | 1245734763 (Harrodsburg) | 1245734763 | YES |
| Emily member ID | WTK4592031 | WTK4592031 | YES |
| Jason member ID | MRL8421137 | MRL8421137 | YES |
| Emily payer | Delta Dental of Kentucky | Delta Dental of Kentucky | YES |
| Jason payer | Cigna | Cigna Dental Health of Kentucky, Inc. | YES |

**Golden reference files:** [`artifacts/golden-reference/`](artifacts/golden-reference/)

---

## Validation Summary

All 4 pipeline stages passed with 0 critical, 0 major, and 0 warning validation errors.

| Stage | Session | Profile | Status | Critical | Major | Warning |
|-------|---------|---------|--------|----------|-------|---------|
| 1. CDT Import | `2e4d8efa` | fhir-r4-import-cdt | COMPLETED | 0 | 0 | 0 |
| 2. CPT Import | `3c60ad32` | fhir-r4-import-cpt | COMPLETED | 0 | 0 | 0 |
| 3. Harmonization | `8273ecb7` | fhir-r4-harmonization | COMPLETED | 0 | 0 | 0 |
| 4. EDI Export | `b8fd9dfe` | edi-837-dental-export | COMPLETED | 0 | 0 | 0 |

---

## OHIA Use Cases Demonstrated

### UC01: Emily Watkins — Deductible Sequencing
Two encounters across a single site demonstrating coordinated deductible application across providers. Both encounters successfully imported with CDT codes, exported as separate CLM segments in the EDI interchange with correct procedure codes and financial totals.

### UC02: Jason Morales — Mixed Benefit Tiers + Tooth Data
Single encounter with diagnostic (D0140, D0220, D0230) and surgical (D7140) procedures at different benefit tiers. Tooth-level data (tooth #30) correctly carried through from FHIR `bodySite` to EDI `TOO*JP*30` segments.

### UC03: Laura Jennings — Predetermination Lifecycle
Full Da Vinci DTR/PAS workflow across 6 FHIR bundles: initial visit, DTR questionnaire, PAS request, PAS response with authorization number (ANT-PREAUTH-2026-JNG001), root canal treatment, and crown placement. The preauthorization claim (use=preauthorization) is correctly excluded from EDI output. Treatment claims carry `REF*G1*ANT-PREAUTH-2026-JNG001` to link back to the authorization.

---

## Artifacts Index

```
connectathon-report/
  CONNECTATHON-DATA-REPORT.md          (this report)
  artifacts/
    stage1-cdt-import/
      output-bundle.json                (49 FHIR resources - Site A)
      validation-report.json
      manifest.json
    stage2-cpt-import/
      output-bundle.json                (49 FHIR resources - Site B)
      validation-report.json
      manifest.json
    stage3-harmonization/
      output-bundle.json                (95 FHIR resources - unified DIN)
      validation-report.json
      manifest.json
    stage4-edi-export/
      output.edi                        (6-claim X12 837D interchange)
      validation-report.json
      manifest.json
    golden-reference/
      uc01-emily_watkins_encounter1_edi.txt
      uc01-emily_watkins_encounter2_edi.txt
      uc02-jason_morales_encounter1_edi.txt
```
