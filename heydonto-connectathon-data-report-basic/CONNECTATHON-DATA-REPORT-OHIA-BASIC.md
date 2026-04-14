# OHIA Connectathon 2026 — Basic Data Transformation Report

**Date:** April 10, 2026
**Platform:** HeyDonto Data Intelligence Network
**Standard:** FHIR R4, X12 005010X224A2 (EDI 837D Dental Claims)
**Environment:** Canary (GKE us-east1)

---

## Executive Summary

This report documents the end-to-end transformation of the **OHIA 2026 US Realm test data** through the HeyDonto Data Intelligence Network. All 9 original OHIA FHIR bundles were used as input, with one correction: a broken cross-claim reference in Emily encounter 2 was fixed (see Data Quality Findings below). No files were added, no entities were fabricated, no coding systems were changed. All CDT codes and OHIA-verified provider/practice metadata are preserved as-is.

**Result:** 3 pipeline stages completed with 0 validation errors and 0 unresolved FHIR references. 34 input resources from 2 data feeds were harmonized into 30 unique resources (4 deduplicated, including a Tier 1 NPI-based Practitioner merge across feeds with different resource IDs). EDI export pending.

---

## Input: Unmodified OHIA Test Data

All 9 input files are the original OHIA 2026 US Realm FHIR bundles. No files were added, no entities were fabricated, no coding systems were changed, no additional provider or practice metadata was created.

**One correction was applied:** `uc01_emily_watkins_encounter2_fhir_bundle.json` contained a cross-claim reference (`urn:uuid:claim-emily-watkins`) pointing to a Claim ID that does not exist in any OHIA bundle. This was corrected to `urn:uuid:claim-emily-watkins-20260312` to match the actual UC01 encounter 1 Claim resource ID. The corrected file is included in `artifacts/ohia-input/`. This finding has been communicated to the OHIA team.

### Provider and Practice Identifiers (OHIA-verified)

| Entity | Name | Identifier | Verified Against |
|--------|------|------------|------------------|
| Rendering provider | Philip Barsotti, DMD | NPI 1568030203 | NPPES Registry |
| Practice organization | Harrodsburg Family Dentistry | NPI 1245734763 | NPPES Registry |
| KY Dental License | Philip Barsotti, DMD | License 10615 | NPPES Registry |
| NUCC taxonomy | General Dentist | 1223G0001X | NUCC |
| Practice address | 517 Legion Dr, Harrodsburg, KY 40330 | | NPPES Registry |

### Data Feed Configuration

The 9 OHIA bundles were loaded as two data feeds. Both feeds represent the same Harrodsburg Family Dentistry practice — no second practice was created, no additional provider metadata was synthesized. The two feeds are purely a partitioning of OHIA use cases to demonstrate multi-feed harmonization.

| Feed | OHIA Use Cases | Bundles | Patients |
|------|---------------|---------|----------|
| **Site A** (site-183) | UC01 + UC02 | 3 (Emily enc1, Emily enc2, Jason enc1) | Emily Watkins, Jason Morales |
| **Site B** (site-184) | UC03 | 6 (Laura b1-b6) | Laura Jennings |

All bundles use `http://www.ada.org/cdt` (CDT) coding exclusively.

---

## Pipeline Overview

```
Stage 1                    Stage 2                    Stage 3                    Stage 4
CDT Import (Site A)        CDT Import (Site B)        Harmonization              EDI 837D Export
3 OHIA bundles             6 OHIA bundles             2 site bundles merged      6 billable claims
16 resources               18 resources               30 resources (4 deduped)   AD: CDT only
Emily + Jason              Laura (full PAS lifecycle) Barsotti merged by NPI     0 unresolved refs
```

---

## Stage 1: FHIR R4 CDT Import — Site A (UC01 + UC02)

**Session:** `72c7c749-ddbb-4611-8f78-33cdab738f0a`
**Profile:** `fhir-r4-import-cdt`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning

### Input: 3 OHIA bundles

| File | Description |
|------|-------------|
| `uc01-emily_watkins_encounter1_fhir_bundle.json` | Emily preventive visit (D0120, D0274, D1110) — $220 |
| `uc01_emily_watkins_encounter2_fhir_bundle.json` | Emily restoration (D2391, tooth 13) — $180 |
| `uc02-jason_morales_encounter1_fhir_bundle.json` | Jason emergency + extraction (D0140, D0220, D0230, D7140, tooth 30) — $335 |

### Output: 16 FHIR Resources

| Resource Type | Count |
|---------------|-------|
| Patient | 2 |
| Practitioner | 2 |
| Organization | 3 |
| PractitionerRole | 1 |
| Coverage | 2 |
| Claim | 3 |
| ExplanationOfBenefit | 3 |

**Note:** Site A contains two Practitioner records for Dr. Barsotti with different resource IDs (`practitioner-philip-barsotti` in Emily enc1, `practitioner-barsotti` in Emily enc2 and Jason). Both carry NPI 1568030203. This naming inconsistency in the OHIA data is resolved during harmonization via Tier 1 NPI-based identity resolution.

**Artifact:** [`artifacts/stage1-site-a/output-bundle.json`](artifacts/stage1-site-a/output-bundle.json)

---

## Stage 2: FHIR R4 CDT Import — Site B (UC03)

**Session:** `90e225c4-3559-44a0-8710-8698f0382a70`
**Profile:** `fhir-r4-import-cdt`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning

### Input: 6 OHIA bundles

| File | Description |
|------|-------------|
| `uc03_laura_jennings_b1_initial_visit.json` | Laura initial visit (D0140, D0220, D0230, D9110) — $205 |
| `uc03_laura_jennings_b2_dtr.json` | DTR Questionnaire + QuestionnaireResponse |
| `uc03_laura_jennings_b3_pas_request.json` | PAS pre-authorization request (D3330, D2740, D2393) |
| `uc03_laura_jennings_b4_pas_response.json` | PAS response (ANT-PREAUTH-2026-JNG001) |
| `uc03_laura_jennings_b5_rct.json` | Root canal treatment (D3330) — $1,150 |
| `uc03-laura_jennings_b6_crown.json` | Crown placement (D2393, D2740) — $1,600 |

### Output: 18 FHIR Resources

| Resource Type | Count |
|---------------|-------|
| Patient | 1 |
| Practitioner | 1 |
| Organization | 2 |
| PractitionerRole | 1 |
| Coverage | 1 |
| Claim | 4 |
| ExplanationOfBenefit | 3 |
| ClaimResponse | 1 |
| Condition | 1 |
| DocumentReference | 1 |
| Questionnaire | 1 |
| QuestionnaireResponse | 1 |

**Artifact:** [`artifacts/stage2-site-b/output-bundle.json`](artifacts/stage2-site-b/output-bundle.json)

---

## Stage 3: Multi-Feed Harmonization

**Session:** `9f24acbd-d37c-4d35-a744-9cecaafb9a5c`
**Profile:** `fhir-r4-harmonization`
**Status:** COMPLETED | 0 critical | 0 major | 0 warning
**DIN ID:** 14

### Input

| Bundle | Data Feed | Resources |
|--------|-----------|-----------|
| site-183-bundle.json | Site A (UC01 + UC02) | 16 |
| site-184-bundle.json | Site B (UC03) | 18 |
| **Total** | | **34** |

### Identity Resolution and Deduplication

| Metric | Count |
|--------|-------|
| Total input | 34 |
| Deduplicated | 4 |
| **Harmonized output** | **30** |
| Unresolved references | **0** |

**Deduplicated entities:**

| Entity | Method | Detail |
|--------|--------|--------|
| Dr. Philip Barsotti | **NPI match (Tier 1)** | `practitioner-philip-barsotti` (Site A enc1) and `practitioner-barsotti` (Site A enc2, Site B) merged via NPI 1568030203 |
| Harrodsburg Family Dentistry | Resource ID match | Same ID in both feeds |
| Barsotti PractitionerRole | Resource ID match | Same ID in both feeds |
| Emily Watkins (within-site) | Resource ID match | Appeared in both Emily enc1 and enc2 bundles within Site A |

The Barsotti Practitioner merge is the key identity resolution result: the OHIA data uses two different resource IDs (`practitioner-philip-barsotti` and `practitioner-barsotti`) for the same provider. The harmonization layer's Tier 1 NPI-based canonical key computation recognized them as the same entity and merged to a single record.

### Harmonized Output: 30 Resources

| Resource Type | Site A | Site B | Harmonized |
|---------------|--------|--------|------------|
| Patient | 2 | 1 | **3** |
| Practitioner | 2 | 1 | **1** |
| Organization | 3 | 2 | **4** |
| PractitionerRole | 1 | 1 | **1** |
| Coverage | 2 | 1 | **3** |
| Claim | 3 | 4 | **7** |
| ExplanationOfBenefit | 3 | 3 | **6** |
| ClaimResponse | 0 | 1 | **1** |
| Condition | 0 | 1 | **1** |
| DocumentReference | 0 | 1 | **1** |
| Questionnaire | 0 | 1 | **1** |
| QuestionnaireResponse | 0 | 1 | **1** |

### Reference Rewriting

After identity resolution and deduplication, all internal FHIR references were rewritten to use canonical resource IDs. The post-processor:
1. Built a rewrite map from all original IDs to canonical IDs
2. Updated `resource.id` on each FHIR resource to match the canonical form
3. Rewrote all `reference` strings inside resources to point to canonical IDs

**Result: 0 unresolved references** in the harmonized output. All `Reference.reference` values point to resources that exist in the harmonized Bundle.

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

**Profile:** `edi-837-dental-export`
**Status:** Pending — awaiting EDI export trigger from DIN dashboard

EDI export has not yet been run for this harmonization session. Once triggered, the expected output is: 6 billable claims (preauth excluded), all `AD:` CDT qualifier, Barsotti NPI 1568030203 on rendering provider, Harrodsburg Family Dentistry on billing provider.

This section and the `artifacts/stage4-edi-export/` directory will be updated with verified EDI output and segment-level comparison against the OHIA reference EDI files.

**Artifact slot:** [`artifacts/stage4-edi-export/`](artifacts/stage4-edi-export/)

---

## OHIA Use Cases Demonstrated

### UC01: Emily Watkins — Deductible Sequencing
Two encounters. Encounter 1: periodic oral exam (D0120), bitewing x-rays (D0274), prophylaxis (D1110) — $220. Encounter 2: one-surface posterior composite on tooth #13 (D2391) — $180.

### UC02: Jason Morales — Mixed Benefit Tiers + Tooth Data
Single emergency encounter. Limited oral eval (D0140), periapical x-ray (D0220), local anesthesia (D0230), extraction of tooth #30 (D7140) — $335.

### UC03: Laura Jennings — Predetermination Lifecycle
Full Da Vinci DTR/PAS workflow across 6 FHIR bundles: initial visit (D0140/D0220/D0230/D9110, $205), DTR questionnaire, PAS request (D3330/D2740/D2393), PAS response (ANT-PREAUTH-2026-JNG001), root canal (D3330, $1,150 with preauth ref), crown (D2393/D2740, $1,600 with preauth ref). Preauthorization claim excluded from EDI output.

---

## Data Quality Findings

During processing, the harmonization pipeline identified two data quality issues in the OHIA test data:

1. **Practitioner ID inconsistency:** `practitioner-philip-barsotti` (Emily enc1) vs `practitioner-barsotti` (all other bundles) for the same provider (NPI 1568030203). Resolved by Tier 1 NPI-based identity resolution.

2. **Broken cross-claim reference:** Emily enc2's Claim contained `related.claim.reference = "urn:uuid:claim-emily-watkins"` — a reference to a Claim ID that does not exist in any OHIA bundle. The actual Emily enc1 Claim ID is `claim-emily-watkins-20260312`. Corrected in our input copy.

Both findings have been communicated to the OHIA team.

---

## Validation Summary

| Stage | Session | Profile | Status | Critical | Major | Warning |
|-------|---------|---------|--------|----------|-------|---------|
| 1. CDT Import (Site A) | `72c7c749` | fhir-r4-import-cdt | COMPLETED | 0 | 0 | 0 |
| 2. CDT Import (Site B) | `90e225c4` | fhir-r4-import-cdt | COMPLETED | 0 | 0 | 0 |
| 3. Harmonization | `9f24acbd` | fhir-r4-harmonization | COMPLETED | 0 | 0 | 0 |
| 4. EDI Export | pending | edi-837-dental-export | Pending | — | — | — |

---

## Artifacts Index

```
connectathon-report-ohia-basic/
  CONNECTATHON-DATA-REPORT-OHIA-BASIC.md    (this report)
  artifacts/
    ohia-input/                              (9 OHIA FHIR bundles used as input)
      uc01-emily_watkins_encounter1_fhir_bundle.json
      uc01_emily_watkins_encounter2_fhir_bundle.json
      uc02-jason_morales_encounter1_fhir_bundle.json
      uc03_laura_jennings_b1_initial_visit.json
      uc03_laura_jennings_b2_dtr.json
      uc03_laura_jennings_b3_pas_request.json
      uc03_laura_jennings_b4_pas_response.json
      uc03_laura_jennings_b5_rct.json
      uc03-laura_jennings_b6_crown.json
    stage1-site-a/
      output-bundle.json                     (16 FHIR resources)
    stage2-site-b/
      output-bundle.json                     (18 FHIR resources)
    stage3-harmonization/
      output-bundle.json                     (30 FHIR resources, 0 unresolved refs)
    stage4-edi-export/
      output.edi                             (pending)
    golden-reference/
      uc01-emily_watkins_encounter1_edi.txt  (OHIA reference EDI)
      uc01-emily_watkins_encounter2_edi.txt  (OHIA reference EDI)
      uc02-jason_morales_encounter1_edi.txt  (OHIA reference EDI)
```
