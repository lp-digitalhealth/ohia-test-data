# OHIA Connectathon — Data Overlap Analysis

> **Date**: 2026-04-13
>
> **Purpose**: Document exactly which OHIA files Conduit uses in each data transformation report, what was modified, and what was augmented.

---

## OHIA Source Data (9 Bundles)

The OHIA 2026 US Realm test data repository contains 9 FHIR R4 bundles across 3 patient scenarios:

| # | File | Patient | Use Case | Key Resource Types |
|---|------|---------|----------|-------------------|
| 1 | `uc01-emily_watkins_encounter1_fhir_bundle.json` | Emily Watkins | UC01: Preventive + Restoration | Patient, Practitioner, Organization, PractitionerRole, Coverage, Claim, EOB |
| 2 | `uc01_emily_watkins_encounter2_fhir_bundle.json` | Emily Watkins | UC01: Restoration (follow-up) | Patient, Practitioner, Organization, PractitionerRole, Coverage, Claim, EOB |
| 3 | `uc02-jason_morales_encounter1_fhir_bundle.json` | Jason Morales | UC02: Emergency + Extraction | Patient, Practitioner, Organization, PractitionerRole, Coverage, Claim, EOB |
| 4 | `uc03_laura_jennings_b1_initial_visit.json` | Laura Jennings | UC03: Initial visit | Patient, Practitioner, Organization, PractitionerRole, Coverage, Claim, EOB |
| 5 | `uc03_laura_jennings_b2_dtr.json` | Laura Jennings | UC03: DTR | Questionnaire, QuestionnaireResponse, Condition, DocumentReference |
| 6 | `uc03_laura_jennings_b3_pas_request.json` | Laura Jennings | UC03: PAS request | Claim (preauthorization), Patient, Coverage, Condition, DocumentReference, QuestionnaireResponse |
| 7 | `uc03_laura_jennings_b4_pas_response.json` | Laura Jennings | UC03: PAS response | ClaimResponse |
| 8 | `uc03_laura_jennings_b5_rct.json` | Laura Jennings | UC03: RCT treatment | Claim, EOB |
| 9 | `uc03-laura_jennings_b6_crown.json` | Laura Jennings | UC03: Crown | Claim, EOB |

All 9 bundles use **CDT codes** (ADA `http://www.ada.org/cdt`), single practice (Harrodsburg Family Dentistry), single provider (Dr. Philip Barsotti, NPI 1568030203).

**Source location**: `ohia-test-data/2026-usrealm-testdata/fhir-resources/`

---

## Report 1: Basic Data Transformation Report

**Report**: `conduit-connectathon-data-report/basic/CONNECTATHON-DATA-REPORT.md`

### Data Used

Uses all 9 OHIA bundles as source input; 8 are byte-identical and 1 has one documented correction. Single practice, all CDT, no fabricated entities.

**Input location**: `conduit-connectathon-data-report/basic/artifacts/ohia-input/`

### File-by-File Comparison with OHIA Source

| OHIA File | Status | Detail |
|-----------|--------|--------|
| uc01-emily_watkins_encounter1_fhir_bundle.json | **Byte-identical** | No changes |
| uc01_emily_watkins_encounter2_fhir_bundle.json | **1 correction applied** | See below |
| uc02-jason_morales_encounter1_fhir_bundle.json | **Byte-identical** | No changes |
| uc03_laura_jennings_b1_initial_visit.json | **Byte-identical** | No changes |
| uc03_laura_jennings_b2_dtr.json | **Byte-identical** | No changes |
| uc03_laura_jennings_b3_pas_request.json | **Byte-identical** | No changes |
| uc03_laura_jennings_b4_pas_response.json | **Byte-identical** | No changes |
| uc03_laura_jennings_b5_rct.json | **Byte-identical** | No changes |
| uc03-laura_jennings_b6_crown.json | **Byte-identical** | No changes |

**Result: 8 of 9 files byte-identical to OHIA source. 1 file has a documented correction.**

### Correction: Emily Watkins Encounter 2

The OHIA file `uc01_emily_watkins_encounter2_fhir_bundle.json` contains a cross-claim reference `urn:uuid:claim-emily-watkins` (line 386) that points to a Claim ID not present in any OHIA bundle. The actual Emily encounter 1 Claim resource uses the ID `claim-emily-watkins-20260312`.

**Change**: `urn:uuid:claim-emily-watkins` → `urn:uuid:claim-emily-watkins-20260312`

The remaining differences between the OHIA source and our copy are JSON serialization artifacts (no semantic change):
- Array indentation formatting (e.g., `["Emily"]` → `[\n  "Emily"\n]`)
- Float precision (`180.00` → `180.0`)
- Unicode encoding of em dashes (`—` → `\u2014`)

These occur because the file was round-tripped through a JSON parser. The FHIR content is semantically identical.

### Pipeline Stages (Basic Report)

| Stage | Profile | Input | Output |
|-------|---------|-------|--------|
| 1. Site A CDT Import | `fhir-r4-import-cdt` | Emily (2 bundles) + Jason (1 bundle) | `stage1-site-a/output-bundle.json` |
| 2. Site B CDT Import | `fhir-r4-import-cdt` | Laura (6 bundles) | `stage2-site-b/output-bundle.json` |
| 3. Harmonization | `fhir-r4-harmonization` | Site A export + Site B export | `stage3-harmonization/output-bundle.json` |
| 4. EDI 837D Export | `edi-837-dental-export` | Harmonized FHIR Bundle | `stage4-edi-export/` (pending) |

### Data Findings During Processing

1. **Practitioner ID inconsistency (OHIA data)**: Emily encounter 1 uses `practitioner-philip-barsotti` while all other bundles use `practitioner-barsotti` — both with NPI 1568030203. Our Tier 1 NPI-based identity resolution correctly merged these into a single Practitioner record.

2. **Cross-claim reference error (OHIA data)**: Emily encounter 2 references `claim-emily-watkins` which does not exist. Corrected to `claim-emily-watkins-20260312` as documented above.

---

## Report 2: Augmented Multi-Site Data Transformation Report

**Report**: `conduit-connectathon-data-report/augmented/CONNECTATHON-DATA-REPORT.md`

### Purpose

Demonstrates Conduit's Data Intelligence Network capabilities beyond the single-practice OHIA baseline:
- Cross-site identity resolution across practices with **different coding systems** (CDT vs CPT)
- Cross-site identity resolution across practices with **different EHR-assigned resource IDs**
- Multi-site harmonization merging clinical, financial, and administrative data

### Data Used

Two data feeds, each combining OHIA data with augmented clinical resources:

**Site A — Lexington Family Dental (CDT-coded)**:
- Emily Watkins: 2 OHIA bundles (encounter 1 + encounter 2)
- Jason Morales: 1 OHIA bundle (encounter 1)
- Augmented: appointments, encounters, procedures, conditions, locations, practitioner roles, practitioners, schedules, slots

**Site B — Harrodsburg Family Dentistry (CPT-coded)**:
- Laura Jennings: 6 OHIA bundles converted to CPT equivalents
- Augmented: appointments, encounters, procedures, conditions, locations, practitioner roles, practitioners, schedules, slots

### What Is OHIA Data vs What Is Augmented

| Data | Source | Specific Changes |
|------|--------|-----------------|
| Emily encounter 1 (CDT) | **OHIA — modified** | Practitioner ID `practitioner-philip-barsotti` → `practitioner-barsotti` (all references); member ID system URL `memberid` → `member-id` |
| Emily encounter 2 (CDT) | **OHIA — modified** | Payer org identifier system changed from `http://hl7.org/fhir/sid/us-npi` to `https://www.deltadentalky.com`; license identifier code `MD` → `SL`, system `dental-license` → `dental/license`; cross-claim reference `claim-emily-watkins` → `claim-emily-watkins-20260312` |
| Jason encounter 1 (CDT) | **OHIA — identical** | No changes |
| Laura bundles 1, 3, 4, 5, 6 (CPT) | **OHIA — recoded** | CDT procedure codes replaced with CPT equivalents, coding system URLs changed from `ada.org/cdt` to `ama-assn.org/cpt` |
| Laura bundle 2 DTR | **OHIA — copied unchanged** | DTR resources (Questionnaire, QuestionnaireResponse, Condition, DocumentReference) contain no procedure codes; file is byte-identical to OHIA source |
| Lexington site master data (9 files) | **Conduit-authored** | Appointments, encounters, procedures, conditions, locations, practitioners, practitioner roles, schedules, slots for Lexington Family Dental practice |
| Harrodsburg site master data (9 files) | **Conduit-authored** | Same resource types for Harrodsburg Family Dentistry practice — demo data anchored on Harrodsburg/Barsotti identifiers reused from OHIA and publicly verifiable via NPPES |
| Lexington practice metadata | **Conduit-authored** | Practice name, address, Dr. Sarah Chen — not verified against NPPES |
| Harrodsburg practice metadata | **OHIA/NPPES-verified identifiers** | Harrodsburg Family Dentistry, NPI 1245734763, Dr. Philip Barsotti, NPI 1568030203 — identifiers from OHIA data, verifiable via NPPES |

### Pipeline Stages (Augmented Report)

| Stage | Profile | Input | Output |
|-------|---------|-------|--------|
| 1. CDT Import | `fhir-r4-import-cdt` | Emily + Jason (OHIA) + Lexington site data (augmented) | `stage1-cdt-import/output-bundle.json` |
| 2. CPT Import | `fhir-r4-import-cpt` | Laura CPT variants (recoded) + Harrodsburg site data (augmented) | `stage2-cpt-import/output-bundle.json` |
| 3. Harmonization | `fhir-r4-harmonization` | CDT export + CPT export | `stage3-harmonization/output-bundle.json` |
| 4. EDI 837D Export | `edi-837-dental-export` | Harmonized FHIR Bundle | `stage4-edi-export/output.edi` |

### Why We Augmented

The OHIA bundles cover financial, administrative, and prior-authorization resources (Claims, EOBs, Coverage, Questionnaire, QuestionnaireResponse, ClaimResponse, Condition, DocumentReference) but lack the scheduling and clinical encounter workflow that Conduit maps from EHRs (Encounter, Procedure, Appointment, Location, Schedule, Slot). The augmented data adds these resource types to demonstrate the full breadth of harmonization.

The CPT-coded variants demonstrate cross-coding-system harmonization. As Mark noted, dentists rarely use CPT codes in practice (except for Medicare billing or physician referrals). The CPT scenario was designed to stress-test the pipeline's terminology handling, not to represent a typical dental workflow. A more realistic cross-system scenario (such as the dental clearance use case Dr. Ryan Lee is creating) would be valuable for future testing.

---

## What to Review

This branch (`conduit-connectathon-data-report`) is a self-contained report package. Everything needed to review the results is in this directory:

- **OHIA source bundles**: `2026-usrealm-testdata/fhir-resources/` (already in the repo, unchanged)
- **Basic report inputs**: `conduit-connectathon-data-report/basic/artifacts/ohia-input/` (copies of the 9 OHIA bundles, verifiable against the source directory above)
- **Basic report outputs**: `conduit-connectathon-data-report/basic/artifacts/stage1-site-a/` through `stage4-edi-export/`
- **Augmented report inputs**: `conduit-connectathon-data-report/augmented/artifacts/stage1-cdt-import/input/` (12 files) and `stage2-cpt-import/input/` (15 files) — includes the CPT-recoded OHIA bundles and Conduit-authored site master data
- **Augmented report outputs**: `conduit-connectathon-data-report/augmented/artifacts/stage1-cdt-import/` through `stage4-edi-export/`
- **Provenance documentation**: This file (DATA-OVERLAP-ANALYSIS.md) with file-by-file comparison tables and the appendix listing the 24 CPT-derived and Conduit-authored input files (the 3 OHIA bundles used in Stage 1 are documented in the Report 2 delta table above)

---

## File Placement Summary

```
ohia-test-data/
├── 2026-usrealm-testdata/fhir-resources/          ← 9 OHIA source bundles (canonical)
│
└── conduit-connectathon-data-report/
    ├── README.md                                    ← Overview + links
    ├── DATA-OVERLAP-ANALYSIS.md                     ← This document
    │
    ├── basic/                                       ← Basic Report (OHIA-only)
    │   ├── CONNECTATHON-DATA-REPORT.md
    │   └── artifacts/
    │       ├── ohia-input/                          ← 9 OHIA bundles (8 identical + 1 corrected)
    │       ├── stage1-site-a/                       ← CDT import output (Emily + Jason)
    │       ├── stage2-site-b/                       ← CDT import output (Laura)
    │       ├── stage3-harmonization/                ← Harmonized FHIR Bundle
    │       └── stage4-edi-export/                   ← EDI 837D output
    │
    └── augmented/                                   ← Augmented Report (OHIA + Conduit-authored)
        ├── CONNECTATHON-DATA-REPORT.md
        └── artifacts/
            ├── stage1-cdt-import/
            │   ├── input/                           ← 12 files (3 OHIA + 9 Lexington site data)
            │   └── output-bundle.json
            ├── stage2-cpt-import/
            │   ├── input/                           ← 15 files (6 Laura CPT + 9 Harrodsburg site data)
            │   └── output-bundle.json
            ├── stage3-harmonization/                ← Harmonized FHIR Bundle (cross-site)
            └── stage4-edi-export/                   ← EDI 837D output
```

### Augmented Input Files

All raw input files for the augmented report are included in this branch under:
- `augmented/artifacts/stage1-cdt-import/input/` — 12 files (3 OHIA bundles + 9 Lexington site master data)
- `augmented/artifacts/stage2-cpt-import/input/` — 15 files (6 Laura CPT-recoded + 9 Harrodsburg site master data)

---

## Appendix: Complete File Inventory for Augmented Report

### CPT-Derived Files (6 files — from OHIA Laura bundles; 5 recoded, 1 copied unchanged)

| File | Size | OHIA Source | Change |
|------|------|------------|--------|
| `uc03_laura_jennings_b1_initial_visit_cpt.json` | 32K | `uc03_laura_jennings_b1_initial_visit.json` | CDT → CPT procedure codes |
| `uc03_laura_jennings_b2_dtr.json` | 14K | `uc03_laura_jennings_b2_dtr.json` | Byte-identical (no procedure codes to recode) |
| `uc03_laura_jennings_b3_pas_request_cpt.json` | 20K | `uc03_laura_jennings_b3_pas_request.json` | CDT → CPT procedure codes |
| `uc03_laura_jennings_b4_pas_response_cpt.json` | 15K | `uc03_laura_jennings_b4_pas_response.json` | CDT → CPT procedure codes |
| `uc03_laura_jennings_b5_rct_cpt.json` | 14K | `uc03_laura_jennings_b5_rct.json` | CDT → CPT procedure codes |
| `uc03-laura_jennings_b6_crown_cpt.json` | 20K | `uc03-laura_jennings_b6_crown.json` | CDT → CPT procedure codes |

### Lexington Site Master Data (9 files — Conduit-authored, in `fhir-r4-import-cdt/input/`)

| File | Resource Types | Size |
|------|---------------|------|
| `site1-lexington-appointments.json` | Appointment | 3.4K |
| `site1-lexington-conditions.json` | Condition | 4.0K |
| `site1-lexington-encounters.json` | Encounter | 7.1K |
| `site1-lexington-locations.json` | Location | 2.1K |
| `site1-lexington-practitioner-roles.json` | PractitionerRole | 2.2K |
| `site1-lexington-practitioners.json` | Practitioner | 5.2K |
| `site1-lexington-procedures.json` | Procedure | 9.2K |
| `site1-lexington-schedules.json` | Schedule | 1.3K |
| `site1-lexington-slots.json` | Slot | 3.5K |

### Harrodsburg Site Master Data (9 files — Conduit-authored, in `fhir-r4-import-cpt/input/`)

| File | Resource Types | Size |
|------|---------------|------|
| `site2-harrodsburg-appointments.json` | Appointment | 3.1K |
| `site2-harrodsburg-conditions.json` | Condition | 1.5K |
| `site2-harrodsburg-encounters.json` | Encounter | 7.0K |
| `site2-harrodsburg-locations.json` | Location | 2.1K |
| `site2-harrodsburg-practitioner-roles.json` | PractitionerRole | 2.6K |
| `site2-harrodsburg-practitioners.json` | Practitioner | 3.7K |
| `site2-harrodsburg-procedures.json` | Procedure | 8.8K |
| `site2-harrodsburg-schedules.json` | Schedule | 1.3K |
| `site2-harrodsburg-slots.json` | Slot | 3.5K |

**Total augmented files: 24** (6 CPT-derived + 9 Lexington + 9 Harrodsburg)

---

## Verification Commands

### Basic Report (runnable from this branch)

These commands can be run directly from the `ohia-test-data` repository root on this branch:

```bash
cd ohia-test-data

# Compare basic report inputs against OHIA source (expect 8 identical, 1 modified)
for f in 2026-usrealm-testdata/fhir-resources/*.json; do
  fname=$(basename "$f")
  diff -q "$f" "conduit-connectathon-data-report/basic/artifacts/ohia-input/$fname"
done

# Show the one semantic change in Emily encounter 2
diff 2026-usrealm-testdata/fhir-resources/uc01_emily_watkins_encounter2_fhir_bundle.json \
     conduit-connectathon-data-report/basic/artifacts/ohia-input/uc01_emily_watkins_encounter2_fhir_bundle.json \
     | grep "claim-emily"
# Expected: < "reference": "urn:uuid:claim-emily-watkins"
#           > "reference": "urn:uuid:claim-emily-watkins-20260312"

# Verify output bundle resource counts
python3 -c "import json; d=json.load(open('conduit-connectathon-data-report/basic/artifacts/stage1-site-a/output-bundle.json')); print(f'Stage 1: {len(d[\"entry\"])} resources')"
python3 -c "import json; d=json.load(open('conduit-connectathon-data-report/basic/artifacts/stage2-site-b/output-bundle.json')); print(f'Stage 2: {len(d[\"entry\"])} resources')"
python3 -c "import json; d=json.load(open('conduit-connectathon-data-report/basic/artifacts/stage3-harmonization/output-bundle.json')); print(f'Stage 3: {len(d[\"entry\"])} resources')"
grep -c 'CLM\*' conduit-connectathon-data-report/basic/artifacts/stage4-edi-export/output.edi
# Expected: Stage 1: 16, Stage 2: 18, Stage 3: 30, CLM count: 6
```

### Augmented Report (runnable from this branch)

All augmented input files are included in this branch. These commands verify both inputs and outputs:

```bash
# Verify input file counts
echo "Stage 1 inputs: $(ls conduit-connectathon-data-report/augmented/artifacts/stage1-cdt-import/input/*.json | wc -l) files"
echo "Stage 2 inputs: $(ls conduit-connectathon-data-report/augmented/artifacts/stage2-cpt-import/input/*.json | wc -l) files"
# Expected: Stage 1: 12, Stage 2: 15

# Verify CPT-recoded files differ from OHIA CDT originals (5 recoded, 1 DTR identical)
for cpt in conduit-connectathon-data-report/augmented/artifacts/stage2-cpt-import/input/uc03*_cpt.json; do
  fname=$(basename "$cpt" | sed 's/_cpt\.json/.json/')
  ohia="2026-usrealm-testdata/fhir-resources/$fname"
  if [ -f "$ohia" ]; then
    diff -q "$ohia" "$cpt" > /dev/null 2>&1 && echo "IDENTICAL: $(basename $cpt)" || echo "RECODED:   $(basename $cpt)"
  fi
done
# DTR bundle should be identical to OHIA source
diff -q 2026-usrealm-testdata/fhir-resources/uc03_laura_jennings_b2_dtr.json \
     conduit-connectathon-data-report/augmented/artifacts/stage2-cpt-import/input/uc03_laura_jennings_b2_dtr.json
# Expected: no output (files are identical)

# Verify output bundle resource counts
python3 -c "import json; d=json.load(open('conduit-connectathon-data-report/augmented/artifacts/stage1-cdt-import/output-bundle.json')); print(f'Stage 1: {len(d[\"entry\"])} resources')"
python3 -c "import json; d=json.load(open('conduit-connectathon-data-report/augmented/artifacts/stage2-cpt-import/output-bundle.json')); print(f'Stage 2: {len(d[\"entry\"])} resources')"
python3 -c "import json; d=json.load(open('conduit-connectathon-data-report/augmented/artifacts/stage3-harmonization/output-bundle.json')); print(f'Stage 3: {len(d[\"entry\"])} resources')"
grep -c 'CLM\*' conduit-connectathon-data-report/augmented/artifacts/stage4-edi-export/output.edi
# Expected: Stage 1: 49, Stage 2: 49, Stage 3: 95, CLM count: 6
```
