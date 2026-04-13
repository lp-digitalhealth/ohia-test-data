# Conduit Connectathon Data Transformation Reports

OHIA 2026 US Realm Dental Connectathon — data transformation reports produced by the Conduit Data Intelligence Network.

## Reports

### [Basic Report](basic/CONNECTATHON-DATA-REPORT.md)
Uses all 9 OHIA FHIR bundles as source input (8 byte-identical, 1 with a documented cross-claim correction). Single practice (Harrodsburg Family Dentistry), all CDT codes, no fabricated entities.

- **Input**: 9 OHIA bundles (8 byte-identical, 1 with documented cross-claim correction)
- **Output**: 30 harmonized FHIR resources, 0 unresolved references, 6 EDI claims
- **Validation**: 0 critical / 0 major / 0 warning across all 4 stages

### [Augmented Report](augmented/CONNECTATHON-DATA-REPORT.md)
Extends the OHIA data with Conduit-authored clinical resources (encounters, procedures, appointments, conditions, locations) and CPT-coded variants to demonstrate multi-site, cross-coding-system harmonization.

- **Input**: 27 files (OHIA + CPT-recoded + Conduit-authored site master data)
- **Output**: 95 harmonized FHIR resources, 0 unresolved references, 6 EDI claims
- **Validation**: 0 critical / 0 major / 0 warning across all 4 stages

### [Data Overlap Analysis](DATA-OVERLAP-ANALYSIS.md)
Documents exactly which files are OHIA originals, which were modified, and which were authored by Conduit. Includes file-by-file provenance, byte-level comparison results, and verification commands.

## Pipeline Stages

Both reports follow the same 4-stage pipeline:

1. **FHIR R4 Import** — Ingest FHIR bundles into site-specific FHIR stores
2. **Multi-Site Harmonization** — Merge resources across sites with identity resolution (NPI, member ID, TIN) and reference rewriting
3. **EDI 837D Export** — Generate X12 005010X224A2 dental claim interchange from harmonized FHIR data
4. **Validation** — Automated checks at each stage (duplicate IDs, referential integrity, NPI uniqueness, patient identity)

## OHIA Use Cases Covered

| Use Case | Patient | Scenario | Bundles |
|----------|---------|----------|---------|
| UC01 | Emily Watkins | Preventive + Restoration (deductible sequencing) | 2 |
| UC02 | Jason Morales | Emergency + Extraction (mixed benefit tiers, tooth data) | 1 |
| UC03 | Laura Jennings | Predetermination lifecycle (DTR → PAS → RCT → Crown) | 6 |
