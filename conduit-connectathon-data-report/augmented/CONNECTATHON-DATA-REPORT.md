# OHIA Connectathon 2026 — Augmented Multi-Site Data Transformation Report

**Date:** April 13, 2026
**Platform:** Conduit Data Intelligence Network
**Standard:** FHIR R4, X12 005010X224A2 (EDI 837D Dental Claims)
**Environment:** Conduit Cloud (US East)

---

## Executive Summary

This report documents the end-to-end data transformation pipeline executed for the OHIA 2026 US Realm Dental Connectathon. The pipeline processes FHIR R4 dental data from two independent practice sites — one CDT-coded, one CPT-coded — harmonizes it into a unified Data Intelligence Network (DIN), and exports production-ready EDI X12 837D dental claim files.

This is the **augmented scenario**: the OHIA golden test data is combined with Conduit-authored clinical resources (encounters, procedures, appointments, conditions, locations, schedules, slots) to demonstrate the full breadth of multi-site harmonization across 18 FHIR resource types. For the OHIA-only baseline, see the [basic report](../basic/CONNECTATHON-DATA-REPORT.md). For a detailed provenance breakdown of which files are OHIA vs Conduit-authored, see the [Data Overlap Analysis](../DATA-OVERLAP-ANALYSIS.md).

**Result:** 4 pipeline stages completed with 0 validation errors and 0 unresolved FHIR references. 98 input resources from 2 sites harmonized into 95 unique resources (3 shared entities deduplicated: 1 via Tier 1 NPI match, 2 via Tier 2 resource ID match). EDI 837D export produced 6 billable dental claims across 3 patients and 3 payers.

---

## Pipeline Overview

```
Stage 1                    Stage 2                    Stage 3                    Stage 4
CDT Import (Site A)        CPT Import (Site B)        Harmonization              EDI 837D Export
49 resources               49 resources               95 resources               6 claims
Emily + Jason              Laura                      3 patients unified         X12 interchange
12 input files             15 input files             2 site bundles merged      1 .edi file
CDT codes (AD:)            CPT codes (HC:)            Barsotti merged by NPI     0 validation errors
```

---

## Stage 1: FHIR R4 CDT Import — Lexington Family Dental (Site A)

**Session:** `e652e0cc-af53-4c0b-98d1-6d92446ffaa2`
**Profile:** `fhir-r4-import-cdt`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning

### Input Files (12)

| File | Source | Description |
|------|--------|-------------|
| `uc01-emily_watkins_encounter1_fhir_bundle.json` | OHIA (modified) | Emily preventive visit (D0120, D0274, D1110) — $220 |
| `uc01_emily_watkins_encounter2_fhir_bundle.json` | OHIA (modified) | Emily restoration (D2391, tooth 13) — $180 |
| `uc02-jason_morales_encounter1_fhir_bundle.json` | OHIA (identical) | Jason emergency extraction (D0140, D0220, D0230, D7140, tooth 30) — $335 |
| `site1-lexington-appointments.json` | Conduit-authored | 3 appointment resources |
| `site1-lexington-conditions.json` | Conduit-authored | 2 condition resources |
| `site1-lexington-encounters.json` | Conduit-authored | 3 encounter resources |
| `site1-lexington-locations.json` | Conduit-authored | 2 location resources |
| `site1-lexington-practitioner-roles.json` | Conduit-authored | 2 practitioner role resources |
| `site1-lexington-practitioners.json` | Conduit-authored | 3 practitioner/org resources |
| `site1-lexington-procedures.json` | Conduit-authored | 8 procedure resources |
| `site1-lexington-schedules.json` | Conduit-authored | 2 schedule resources |
| `site1-lexington-slots.json` | Conduit-authored | 10 slot resources |

### Output: 49 FHIR Resources

| Resource Type | Count |
|---------------|-------|
| Patient | 2 |
| Practitioner | 2 |
| Organization | 4 |
| PractitionerRole | 3 |
| Coverage | 2 |
| Claim | 3 |
| ExplanationOfBenefit | 3 |
| Encounter | 3 |
| Procedure | 8 |
| Appointment | 3 |
| Condition | 2 |
| Location | 2 |
| Schedule | 2 |
| Slot | 10 |

**Artifacts:**
- Input: [`artifacts/stage1-cdt-import/input/`](artifacts/stage1-cdt-import/input/) (12 files)
- Output: [`artifacts/stage1-cdt-import/output-bundle.json`](artifacts/stage1-cdt-import/output-bundle.json)

---

## Stage 2: FHIR R4 CPT Import — Harrodsburg Family Dentistry (Site B)

**Session:** `b19c3d59-3bb8-49aa-a23f-739f8a0244a5`
**Profile:** `fhir-r4-import-cpt`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning

### Input Files (15)

| File | Source | Description |
|------|--------|-------------|
| `uc03_laura_jennings_b1_initial_visit_cpt.json` | OHIA (recoded) | Laura initial visit (CPT 99201, 70300, 70310, 99212) — $205 |
| `uc03_laura_jennings_b2_dtr.json` | OHIA (copied unchanged) | DTR Questionnaire + QuestionnaireResponse |
| `uc03_laura_jennings_b3_pas_request_cpt.json` | OHIA (recoded) | PAS pre-authorization request |
| `uc03_laura_jennings_b4_pas_response_cpt.json` | OHIA (recoded) | PAS response (ANT-PREAUTH-2026-JNG001) |
| `uc03_laura_jennings_b5_rct_cpt.json` | OHIA (recoded) | Root canal treatment claim (CPT 41899) — $1,150 |
| `uc03-laura_jennings_b6_crown_cpt.json` | OHIA (recoded) | Crown placement claim (CPT 41899 x2) — $1,600 |
| `site2-harrodsburg-*.json` (9 files) | Conduit-authored | Appointments, conditions, encounters, locations, practitioner-roles, practitioners, procedures, schedules, slots |

### Output: 49 FHIR Resources

| Resource Type | Count |
|---------------|-------|
| Patient | 1 |
| Practitioner | 2 |
| Organization | 2 |
| PractitionerRole | 3 |
| Coverage | 1 |
| Claim | 4 |
| ClaimResponse | 1 |
| Questionnaire | 1 |
| QuestionnaireResponse | 1 |
| ExplanationOfBenefit | 3 |
| DocumentReference | 1 |
| Encounter | 3 |
| Procedure | 7 |
| Appointment | 3 |
| Condition | 2 |
| Location | 2 |
| Schedule | 2 |
| Slot | 10 |

**Artifacts:**
- Input: [`artifacts/stage2-cpt-import/input/`](artifacts/stage2-cpt-import/input/) (15 files)
- Output: [`artifacts/stage2-cpt-import/output-bundle.json`](artifacts/stage2-cpt-import/output-bundle.json)

---

## Stage 3: Multi-Site Harmonization

**Session:** `b3071a50-c746-44fa-b2c5-2a8bcf576f63`
**Profile:** `fhir-r4-harmonization`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning
**DIN ID:** 19

### Input

| Bundle | Site | Resources |
|--------|------|-----------|
| site-192-bundle.json | Lexington Family Dental (CDT) | 49 |
| site-193-bundle.json | Harrodsburg Family Dentistry (CPT) | 49 |
| **Total input** | | **98** |

### Identity Resolution and Deduplication

| Metric | Count |
|--------|-------|
| Total input | 98 |
| Shared across sites | 3 |
| **Harmonized output** | **95** |
| Total references | 232 |
| Unresolved references | **0** |

**Deduplicated entities:**

| Entity | Method | Detail |
|--------|--------|--------|
| Dr. Philip Barsotti | **NPI match (Tier 1)** | Practices at both sites, merged via NPI 1568030203 |
| Barsotti PractitionerRole | Resource ID match (Tier 2) | Same role definition in both sites |
| Harrodsburg Family Dentistry | Resource ID match (Tier 2) | Practice organization referenced by both sites |

### Harmonized Output: 95 Resources

| Resource Type | Site A (CDT) | Site B (CPT) | Harmonized |
|---------------|--------------|--------------|------------|
| Patient | 2 | 1 | **3** |
| Practitioner | 2 | 2 | **3** |
| Organization | 4 | 2 | **5** |
| PractitionerRole | 3 | 3 | **5** |
| Coverage | 2 | 1 | **3** |
| Claim | 3 | 4 | **7** |
| ExplanationOfBenefit | 3 | 3 | **6** |
| Encounter | 3 | 3 | **6** |
| Procedure | 8 | 7 | **15** |
| Appointment | 3 | 3 | **6** |
| Condition | 2 | 2 | **4** |
| Location | 2 | 2 | **4** |
| Schedule | 2 | 2 | **4** |
| Slot | 10 | 10 | **20** |
| ClaimResponse | 0 | 1 | **1** |
| Questionnaire | 0 | 1 | **1** |
| QuestionnaireResponse | 0 | 1 | **1** |
| DocumentReference | 0 | 1 | **1** |

### Validation Rules Passed

| Rule | Check | Result |
|------|-------|--------|
| FHIR_NO_DUPLICATE_IDS | No duplicate resourceType+id | PASS |
| NO_DUPLICATE_TIER1_NPI | No duplicate Practitioner NPIs | PASS |
| NO_DUPLICATE_TIER1_PATIENT | No duplicate Patient identity | PASS |
| ALL_REFERENCES_RESOLVE | All references resolve | PASS |
| FHIR_VALID_RESOURCE_TYPE | resourceType present | PASS |
| FHIR_HAS_ID | id present | PASS |

**Artifact:** [`artifacts/stage3-harmonization/output-bundle.json`](artifacts/stage3-harmonization/output-bundle.json)

---

## Stage 4: EDI X12 837D Export

**Session:** `ddc6e4ea-c4ff-44d3-9fb4-b8aea01005e7`
**Profile:** `edi-837-dental-export`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning
**DIN ID:** 19

### Export Summary

| Metric | Value |
|--------|-------|
| Billable claims exported | 6 |
| Preauthorization claims excluded | 1 |
| Patients in interchange | 3 (Emily, Jason, Laura) |
| Payers in interchange | 3 (Delta Dental KY, Cigna Dental KY, Anthem BCBS KY) |
| Total EDI segments (ST-SE) | 112 |
| Code qualifiers | AD (CDT): Emily + Jason claims; HC (CPT): Laura claims |

**Artifact:** [`artifacts/stage4-edi-export/output.edi`](artifacts/stage4-edi-export/output.edi)

---

## OHIA Use Cases Demonstrated

### UC01: Emily Watkins — Deductible Sequencing (CDT)
Two encounters. Encounter 1: periodic oral exam (D0120), bitewing x-rays (D0274), prophylaxis (D1110) — $220. Encounter 2: one-surface posterior composite on tooth #13 (D2391) — $180.

### UC02: Jason Morales — Mixed Benefit Tiers + Tooth Data (CDT)
Single emergency encounter. Limited oral eval (D0140), periapical x-ray (D0220), local anesthesia (D0230), extraction of tooth #30 (D7140) — $335.

### UC03: Laura Jennings — Predetermination Lifecycle (CPT)
Full Da Vinci DTR/PAS workflow across 6 FHIR bundles: initial visit (99201/70300/70310/99212, $205), DTR questionnaire, PAS request, PAS response (ANT-PREAUTH-2026-JNG001), root canal (41899, $1,150 with preauth ref), crown (41899x2, $1,600 with preauth ref). Preauthorization claim excluded from EDI output.

---

## Validation Summary

| Stage | Session | Profile | Status | Critical | Major | Warning |
|-------|---------|---------|--------|----------|-------|---------|
| 1. CDT Import | `e652e0cc` | fhir-r4-import-cdt | COMPLETED | 0 | 0 | 0 |
| 2. CPT Import | `b19c3d59` | fhir-r4-import-cpt | COMPLETED | 0 | 0 | 0 |
| 3. Harmonization | `b3071a50` | fhir-r4-harmonization | COMPLETED | 0 | 0 | 0 |
| 4. EDI Export | `ddc6e4ea` | edi-837-dental-export | COMPLETED | 0 | 0 | 0 |

---

## Artifacts Index

```
augmented/
  CONNECTATHON-DATA-REPORT.md          (this report)
  artifacts/
    stage1-cdt-import/
      input/                            (12 files: 3 OHIA + 9 Lexington site data)
      output-bundle.json                (49 FHIR resources - Site A, CDT)
    stage2-cpt-import/
      input/                            (15 files: 6 Laura CPT + 9 Harrodsburg site data)
      output-bundle.json                (49 FHIR resources - Site B, CPT)
    stage3-harmonization/
      output-bundle.json                (95 FHIR resources - unified DIN, 0 unresolved refs)
    stage4-edi-export/
      output.edi                        (6-claim X12 837D interchange)
```
