# OHIA Connectathon — Dental Interoperability Test Dataset

This repository contains synthetic test data for the Oral Health Interoperability Alliance (OHIA) Connectathon. It is used to validate dental interoperability standards — including FHIR R4, X12 837D, and related implementation guides — across three clinical scenarios of increasing complexity.

**Dataset Version:** 1.0 · March 2026  
**OHIA Facilitator:** Mark Marciante, Leavitt Partners (an HMA Company)

> **⚠️ CDT Code Usage Notice**
> All CDT procedure codes in this repository are used with permission from the American Dental Association and are used solely for OHIA Connectathon testing and interoperability demonstration purposes. Any use outside of OHIA testing or HL7 Connectathon events requires prior written approval from ADA and OHIA leadership. Contact [Mark Marciante](mailto:mmarciante@leavittpartners.com) before any use.

---

## Repository Structure

```
2026-usrealm-testdata/
├── use-cases/          # Clinical and billing detail for each patient scenario
├── fhir-resources/     # FHIR R4 bundles pre-loaded on the Onyx OnyxOS server
└── edi-resources/      # X12 837D transactions and element-level reference CSVs
```

## Resources

| Resource | Description |
|----------|-------------|
| [use-cases/](2026-usrealm-testdata/use-cases/) | Full scenario documentation for each patient: clinical findings, CDT service lines, adjudication logic, and billing notes — organized for clinical staff, billing teams, and clearinghouse vendors |
| [fhir-resources/](2026-usrealm-testdata/fhir-resources/) | Nine FHIR R4 bundles covering all encounters, predetermination, and clinical documentation across the three scenarios; includes Connectathon test case details and OnyxOS server access |
| [edi-resources/](2026-usrealm-testdata/edi-resources/) | X12 837D transaction files and per-encounter loop/segment/element CSVs for all three patients; includes validation notes on tooth encoding, mixed benefit tiers, and predetermination references |

## Patient Scenarios

| # | Patient | Scenario | Payer | Encounters |
|---|---------|----------|-------|------------|
| UC01 | Emily Watkins | Routine preventive care and single-surface restoration | Delta Dental of Kentucky | 2 |
| UC02 | Jason Morales | Emergency new-patient visit with extraction (tooth #30) | Cigna Dental Health of Kentucky | 1 |
| UC03 | Laura Jennings | Predetermination, root canal therapy, and crown (tooth #3) | Anthem BCBS Kentucky | 3 |

---

## A Note on Synthetic vs. Real Data

All patient information in this dataset is fabricated — names, dates of birth, member IDs, group numbers, employer names, and authorization numbers have no real-world counterparts and were created solely for testing purposes.

However, **some identifiers are real**: provider NPIs (Harrodsburg Family Dentistry and Dr. Philip Barsotti) and payer EDI IDs (Delta Dental of Kentucky, Cigna Dental Health of Kentucky, and Anthem BCBS Kentucky) are publicly available identifiers included here to produce realistic, validatable transactions. They are used strictly in a synthetic test context and do not represent any actual claims, authorizations, or provider-payer relationships.
