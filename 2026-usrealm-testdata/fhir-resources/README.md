# FHIR Resources — OHIA Connectathon Test Data

**Folder:** `2026-usrealm-testdata/fhir-resources/`  
**Dataset Version:** 1.0 · March 2026  
**Related:** [Repository Root README](../../README.md) · [Use Cases](../use-cases/)

---

## Overview

This folder contains nine FHIR R4 bundles covering all encounters, predetermination events, and supporting clinical documentation across the three OHIA Connectathon patient scenarios. The bundles are pre-loaded on the Onyx OnyxOS FHIR server at the Connectathon tenant and are used to test whether patient-facing and provider-centric applications can authenticate, query, and retrieve dental claims and authorization data using open standards — without proprietary interfaces or phone calls to a payer.

The Connectathon exercise is retrieval-only: **authenticate → query → verify**. No write operations are expected from participants.

For full clinical and billing context behind each scenario, see the [`use-cases/`](../use-cases/) folder.

---

## Standards in Use

| Standard | Version | Used For |
|----------|---------|----------|
| CARIN Blue Button® with Oral Profile | R4 | Patient-facing EOBs and claims access for all three patients |
| Da Vinci Prior Authorization Support (PAS) | R4 | Predetermination request and ClaimResponse for Laura Jennings |
| Da Vinci Documentation Templates and Rules (DTR) | R4 | Clinical documentation (Questionnaire, QuestionnaireResponse) supporting Laura Jennings' predetermination |
| US Core | 6.1 | Patient demographics, Condition, Organization — shared across all bundles |

---

## Bundle Inventory

Nine bundles are included across the three scenarios. Each bundle is scoped to a single encounter or workflow event.

### UC01 — Emily Watkins

**Payer:** Delta Dental of Kentucky · 2 encounters · No predetermination  
Full scenario: [uc01-Emily-Watkins.md](../use-cases/uc01-Emily-Watkins.md)

| File | Standard | Contents |
|------|----------|----------|
| `emily_watkins_fhir_bundle.json` | CARIN BB Oral | Encounter 1 — Claim and EOB, preventive visit (Mar 12, 2026): D0120, D0274, D1110 |
| `emily_watkins_encounter2_fhir_bundle.json` | CARIN BB Oral | Encounter 2 — Claim and EOB, composite restoration (May 22, 2026): D2391, tooth #13 |

---

### UC02 — Jason Morales

**Payer:** Cigna Dental Health of Kentucky · 1 encounter · No predetermination  
Full scenario: [uc02-Jason-Morales-extraction.md](../use-cases/uc02-Jason-Morales-extraction.md)

| File | Standard | Contents |
|------|----------|----------|
| `jason_morales_encounter1_fhir_bundle.json` | CARIN BB Oral | Encounter 1 — Claim and EOB, emergency exam and extraction (Apr 8, 2026): D0140, D0220, D0230, D7140, tooth #30 |

---

### UC03 — Laura Jennings

**Payer:** Anthem BCBS Kentucky · 3 encounters · Predetermination required  
**Authorization:** `ANT-PREAUTH-2026-JNG001`  
Full scenario: [uc03-Laura-Jennings-predetermination.md](../use-cases/uc03-Laura-Jennings-predetermination.md)

| File | Standard | Contents |
|------|----------|----------|
| `laura_jennings_b1_initial_visit.json` | CARIN BB Oral | Encounter 1 — Claim and EOB, emergency exam and palliative treatment (Jun 3, 2026): D0140, D0220, D0230, D9110, tooth #3 |
| `laura_jennings_b2_dtr.json` | Da Vinci DTR | Predetermination clinical documentation: Questionnaire, QuestionnaireResponse, Condition (K04.01 irreversible pulpitis), DocumentReference |
| `laura_jennings_b3_pas_request.json` | Da Vinci PAS | Predetermination Claim (`use: preauthorization`) submitted Jun 4, 2026 for D3330, D2740, D2393 |
| `laura_jennings_b4_pas_response.json` | Da Vinci PAS | ClaimResponse with `preAuthRef ANT-PREAUTH-2026-JNG001`; includes conditional authorization on D2393 |
| `laura_jennings_b5_rct.json` | CARIN BB Oral | Encounter 2 — Claim and EOB, root canal therapy (Jun 17, 2026): D3330, tooth #3 |
| `laura_jennings_b6_crown.json` | CARIN BB Oral | Encounter 3 — Claim and EOB, core buildup and crown (Jul 15, 2026): D2393, D2740, tooth #3 |

---

## Server Access

All nine bundles are pre-loaded on the Onyx OnyxOS FHIR server at the Connectathon tenant.

| Resource | URL |
|----------|-----|
| OnyxOS API Documentation | https://docs.safhir.io/onyxos_api_documentation.html |
| Onyx Developer Portal | https://portal.safhir.io |

### Test Account Credentials

| Patient | Test Username | Member ID |
|---------|---------------|-----------|
| Emily Watkins | WTK4592031 | |
| Jason Morales | MRL8421137 | |
| Laura Jennings | JNG5027741 | |

Passwords are distributed via the OHIA coordination channel and are not published in this repository.

---

## Retrieval Workflow

The Connectathon exercise is read-only. The expected sequence for each test case is:

1. **Authenticate** using SMART on FHIR with the test account credentials above
2. **Query** the OnyxOS server for the relevant resource type and patient
3. **Verify** that the response matches the expected data documented in the use-case file for that scenario

### Payer Namespaces

Each patient's bundles are scoped to a separate payer namespace on the server. Queries should be directed to the appropriate namespace.

| Patient | Payer | Namespace |
|---------|-------|-----------|
| Emily Watkins | Delta Dental of Kentucky | `/carin-bb/fhir/` |
| Jason Morales | Cigna Dental Health of Kentucky | `/carin-bb/fhir/` |
| Laura Jennings | Anthem BCBS Kentucky | `/carin-bb/fhir/` (claims) · `/davinci-pas/fhir/` (authorization) · `/davinci-dtr/fhir/` (clinical docs) |

### Key Resource Types by Test Goal

| Goal | Resource Type | Relevant Bundles |
|------|--------------|-----------------|
| Retrieve patient claims and EOBs | `ExplanationOfBenefit` | All CARIN BB bundles |
| Retrieve authorization status | `ClaimResponse` | `laura_jennings_b4_pas_response.json` |
| Retrieve predetermination request | `Claim` (`use: preauthorization`) | `laura_jennings_b3_pas_request.json` |
| Retrieve supporting clinical documentation | `Questionnaire`, `QuestionnaireResponse`, `DocumentReference` | `laura_jennings_b2_dtr.json` |
| Retrieve tooth-level procedure detail | `ExplanationOfBenefit.item` with oral profile extensions | Jason Morales and Laura Jennings bundles |

---

## Relationship to EDI Resources

These FHIR bundles represent the same clinical and financial events as the X12 837D transaction files in the [`edi-resources/`](../edi-resources/) folder. The FHIR bundles are the primary artifacts for Connectathon test cases. The EDI files are provided as a reference layer for analysts who want to cross-walk FHIR representation against X12 837D transaction structure.

---

*OHIA Connectathon Test Dataset · Version 1.0 · March 2026*  
*Facilitator: Mark Marciante, Leavitt Partners (an HMA Company)*  
*All patient names, member IDs, employer groups, plan identifiers, and authorization numbers are synthetic test data with no real-world counterparts. Provider NPIs and payer EDI IDs are real, publicly available identifiers used here solely in a synthetic test context.*
