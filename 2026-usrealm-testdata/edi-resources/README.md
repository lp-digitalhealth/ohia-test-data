# EDI Resources — OHIA Connectathon Test Data

**Folder:** `2026-usrealm-testdata/edi-resources/`  
**Dataset Version:** 1.0 · March 2026  
**Related:** [Dataset Root README](../../README.md) · [Use Cases](../use-cases/)

---

## Overview

This folder contains X12 837D (Dental) EDI transaction files and supporting element-level reference materials for the three synthetic patient scenarios used at the OHIA Connectathon. The files are intended for clearinghouse vendors, EDI analysts, and dental IT staff who want to inspect transaction structure, validate adjudication logic, or cross-reference X12 837D representation against the FHIR-based equivalents hosted on the Onyx OnyxOS server.

**These are synthetic test transactions.** All patient names, member IDs, group numbers, and authorization numbers are fabricated for testing purposes only. Provider NPIs and payer EDI IDs are real, publicly available identifiers used solely in a test context.

---

## File Inventory

Each scenario includes one `.txt` file containing all 837D transactions for that patient and one `.csv` per encounter with a complete loop/segment/element breakdown.

### UC01 — Emily Watkins: Routine Preventive Care and Single-Surface Restoration

**Payer:** Delta Dental of Kentucky · EDI Payer ID: `38217`

| File | Type | Encounters Covered |
|------|------|--------------------|
| `uc01-emily-watkins-edi.txt` | X12 837D | Encounter 1 (Mar 12, 2026) and Encounter 2 (May 22, 2026) |
| `uc01-emily-watkins-encounter1-loops-segments-elements.csv` | Reference | Encounter 1 — Preventive visit: D0120, D0274, D1110 |
| `uc01-emily-watkins-encounter2-loops-segments-elements.csv` | Reference | Encounter 2 — Composite restoration, tooth #13: D2391 |

→ Full clinical and billing context: [uc01-Emily-Watkins.md](../use-cases/uc01-Emily-Watkins.md)

---

### UC02 — Jason Morales: Emergency New-Patient Visit with Extraction

**Payer:** Cigna Dental Health of Kentucky · EDI Payer ID: `62308`

| File | Type | Encounters Covered |
|------|------|--------------------|
| `uc02-jason-morales-edi.txt` | X12 837D | Encounter 1 (Apr 8, 2026) |
| `uc02-jason-morales-encounter1-loops-segments-elements.csv` | Reference | Encounter 1 — Emergency exam and extraction, tooth #30: D0140, D0220, D0230, D7140 |

→ Full clinical and billing context: [uc02-Jason-Morales-extraction.md](../use-cases/uc02-Jason-Morales-extraction.md)

---

### UC03 — Laura Jennings: Predetermination, Root Canal Therapy, and Crown

**Payer:** Anthem Blue Cross and Blue Shield of Kentucky · EDI Payer ID: `026033` · EDI Gateway: Availity  
**Authorization Number:** `ANT-PREAUTH-2026-JNG001`

| File | Type | Encounters Covered |
|------|------|--------------------|
| `uc03-laura-jennings-edi.txt` | X12 837D | Encounters 1–3 (Jun 3, Jun 17, Jul 15, 2026) |
| `uc03-laura-jennings-encounter1-loops-segments-elements.csv` | Reference | Encounter 1 — Emergency exam and palliative treatment, tooth #3: D0140, D0220, D0230, D9110 |
| `uc03-laura-jennings-encounter2-loops-segments-elements.csv` | Reference | Encounter 2 — Root canal therapy, tooth #3: D3330 |
| `uc03-laura-jennings-encounter3-loops-segments-elements.csv` | Reference | Encounter 3 — Core buildup and crown, tooth #3: D2393, D2740 |

→ Full clinical and billing context: [uc03-Laura-Jennings-predetermination.md](../use-cases/uc03-Laura-Jennings-predetermination.md)

---

## File Format Details

### `*-edi.txt` — X12 837D Transaction Set

Each `.txt` file is a well-formed X12 837D (Health Care Claim: Dental) transaction using `~` as the segment terminator and `*` as the element separator. Each file contains one transaction set (`ST`/`SE`) per encounter, all within a single ISA/GS envelope. The standard loop structure is as follows:

| Loop | Description | Notes |
|------|-------------|-------|
| ISA/GS | Interchange and functional group envelope | Sender/receiver IDs; payer EDI IDs as listed above |
| ST/SE | Transaction set wrapper | One per encounter within the file |
| Loop 2000A | Billing Provider Hierarchy | Harrodsburg Family Dentistry · NPI 1245734763 |
| Loop 2000B | Subscriber Hierarchy | Patient as subscriber in all three scenarios |
| Loop 2300 | Claim Information | Includes `REF*G1` predetermination reference where required |
| Loop 2400 | Service Line Detail | CDT procedure codes, tooth numbers (TOO segment), surface codes |

The `REF*G1` predetermination reference segment (`ANT-PREAUTH-2026-JNG001`) is present in Loop 2300 on Laura Jennings' Encounter 2 (root canal) and Encounter 3 (crown/buildup) transactions. It is absent from Encounter 1, which predates the authorization.

### `*-loops-segments-elements.csv` — Element-Level Reference

Each `.csv` provides a flat, row-per-element breakdown of every segment in the corresponding 837D encounter. Use these files to inspect any value in context without parsing the raw EDI.

| Column | Description |
|--------|-------------|
| `loop_id` | X12 loop identifier (e.g., `2300`, `2400`) |
| `segment_id` | Segment identifier (e.g., `CLM`, `SV3`, `TOO`) |
| `element_position` | Element position within the segment (1-indexed) |
| `element_name` | Human-readable element name per the 837D implementation guide |
| `element_value` | Value as it appears in the transaction |
| `notes` | Adjudication or implementation notes where relevant |

---

## Scenario Summary

| Patient | Use Case | Payer | EDI Payer ID | Dates of Service | Predetermination | Key EDI Features |
|---------|----------|-------|--------------|------------------|-----------------|------------------|
| Emily Watkins | UC01 | Delta Dental of Kentucky | 38217 | Mar 12, May 22, 2026 | None | Deductible-exempt preventive lines (Enc. 1); deductible + coinsurance on restoration (Enc. 2) |
| Jason Morales | UC02 | Cigna Dental Kentucky | 62308 | Apr 8, 2026 | None | Mixed benefit tiers on a single claim (Basic 80% / Oral Surgery 70%); tooth #30 in TOO segment |
| Laura Jennings | UC03 | Anthem BCBS Kentucky | 026033 | Jun 3, Jun 17, Jul 15, 2026 | Required — `ANT-PREAUTH-2026-JNG001` | `REF*G1` on Enc. 2 and 3; mixed benefit tiers on Enc. 3 (Basic 80% / Major 50%); conditional D2393 authorization |

---

## Validation Reference

### Tooth Number Encoding (TOO Segment)

Tooth numbers appear in the `TOO` segment (Tooth Information) within Loop 2400. The qualifier used is `JP` (Universal Numbering System). Surface codes appear in the third element where applicable.

| Patient | Tooth | CDT | TOO Segment | Surface |
|---------|-------|-----|-------------|---------|
| Emily Watkins | #13 | D2391 | `TOO*JP*13` | `O` (Occlusal) |
| Jason Morales | #30 | D0220 | `TOO*JP*30` | — |
| Jason Morales | #30 | D7140 | `TOO*JP*30` | — |
| Laura Jennings | #3 | D0220, D0230 | `TOO*JP*3` | — |
| Laura Jennings | #3 | D9110 | `TOO*JP*3` | — |
| Laura Jennings | #3 | D3330 | `TOO*JP*3` | — |
| Laura Jennings | #3 | D2393 | `TOO*JP*3` | `MOD` (Mesial, Occlusal, Distal) |
| Laura Jennings | #3 | D2740 | `TOO*JP*3` | — |

Preventive procedure lines for Emily (D0120, D0274, D1110) carry no tooth or surface.

### Predetermination Reference (REF\*G1)

Anthem requires authorization number `ANT-PREAUTH-2026-JNG001` in the `REF*G1` segment in Loop 2300 on Laura Jennings' claims for D3330 and D2740/D2393. Claims submitted without this reference will be denied. The emergency visit claim (Encounter 1) does not carry a predetermination reference — those services do not require prior authorization under this plan.

### Deductible Sequencing

Each scenario applies a $50.00 individual annual deductible to the first eligible service line in the first claim of the plan year. All subsequent lines in the same claim, and all subsequent claims, carry $0 deductible. This sequencing is reflected in the adjudication amounts in the `.csv` notes column and in the use case billing summaries.

| Patient | Deductible Applied On | Remaining After |
|---------|-----------------------|-----------------|
| Emily Watkins | Enc. 2, Line 1 (D2391) — Enc. 1 preventive services are deductible-exempt | $0.00 for plan year 2026 |
| Jason Morales | Enc. 1, Line 1 (D0140) | $0.00 for plan year 2026 |
| Laura Jennings | Enc. 1, Line 1 (D0140) | $0.00 for plan year 2026 |

### Mixed Benefit Tier Claims

Two claims in this dataset contain service lines at different coinsurance rates on the same date of service. If a remittance returns all lines at the same rate, benefit tier assignment should be verified against the plan document.

| Patient | Encounter | Line | CDT | Benefit Category | Rate |
|---------|-----------|------|-----|-----------------|------|
| Jason Morales | Enc. 1 | 1–3 | D0140, D0220, D0230 | Basic | 80% |
| Jason Morales | Enc. 1 | 4 | D7140 | Oral Surgery | 70% |
| Laura Jennings | Enc. 3 | 1 | D2393 | Basic | 80% |
| Laura Jennings | Enc. 3 | 2 | D2740 | Major | 50% |

---

## Relationship to FHIR Resources

These EDI files represent the same clinical and financial events as the FHIR bundles hosted on the Onyx OnyxOS Connectathon server. They are provided as a reference layer for EDI-familiar analysts who want to cross-walk X12 837D transaction structure against CARIN Blue Button with Oral Profile `ExplanationOfBenefit` resources. The table below maps EDI files to their corresponding FHIR bundles.

| EDI File | Encounter | Corresponding FHIR Bundle |
|----------|-----------|---------------------------|
| `uc01-emily-watkins-edi.txt` (Enc. 1) | Mar 12, 2026 | `emily_watkins_fhir_bundle.json` |
| `uc01-emily-watkins-edi.txt` (Enc. 2) | May 22, 2026 | `emily_watkins_encounter2_fhir_bundle.json` |
| `uc02-jason-morales-edi.txt` | Apr 8, 2026 | `jason_morales_encounter1_fhir_bundle.json` |
| `uc03-laura-jennings-edi.txt` (Enc. 1) | Jun 3, 2026 | `laura_jennings_b1_initial_visit.json` |
| `uc03-laura-jennings-edi.txt` (Enc. 2) | Jun 17, 2026 | `laura_jennings_b5_rct.json` |
| `uc03-laura-jennings-edi.txt` (Enc. 3) | Jul 15, 2026 | `laura_jennings_b6_crown.json` |

The FHIR bundles are the primary artifacts for Connectathon test cases — they are pre-loaded on the OnyxOS server and used in the retrieval test workflow. The EDI files in this folder are reference material and are not loaded to the FHIR server.

For the full FHIR bundle inventory, Connectathon test case descriptions, and OnyxOS server access details, see the [dataset root README](../../README.md).

---

*OHIA Connectathon Test Dataset · Version 1.0 · March 2026*  
*Facilitator: Mark Marciante, Leavitt Partners (an HMA Company)*  
*All patient names, member IDs, employer groups, plan identifiers, and authorization numbers are synthetic test data with no real-world counterparts. Provider NPIs and payer EDI IDs are real, publicly available identifiers used here solely in a synthetic test context.*
