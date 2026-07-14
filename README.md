# OHIA Connectathon — Dental Interoperability Test Dataset

This repository contains synthetic test data for the Oral Health Interoperability Alliance (OHIA) Connectathon. It is used to validate dental interoperability standards — including FHIR R4, X12 837D, and related implementation guides — across three clinical scenarios of increasing complexity.

**Dataset Version:** 1.0 · March 2026  
**OHIA Facilitator:** Mark Marciante, Leavitt Partners (an HMA Company)

> **⚠️ CDT Code Usage Notice**
> All CDT procedure codes in this repository are used with permission from the American Dental Association and are used solely for OHIA Connectathon testing and interoperability demonstration purposes. Any use outside of OHIA testing or HL7 Connectathon events requires prior written approval from ADA and OHIA leadership. Contact [Mark Marciante](mailto:mmarciante@leavittpartners.com) before any use.

---

## Repository Structure

```
2026-usrealm-testdata/ This was used for the U.S. Realm Connectathon in March, 2026
├── use-cases/          # Clinical and billing detail for each patient scenario
├── fhir-resources/     # FHIR R4 bundles pre-loaded on the Onyx OnyxOS server
└── edi-resources/      # X12 837D transactions and element-level reference CSVs
```

2026-CMS-Connectathon
├── companion-guides/   # Guides to help testers at the Connectathon
├── fhir-resources/     # FHIR R4 bundles
├── hl7v2/              # hl7v21 files for testing
├── use-cases/          # Clinical use cases


