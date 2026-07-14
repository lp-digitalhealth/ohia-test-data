# CLAUDE.md — OHIA CMS Connectathon Test Data

**Document version:** 7.0  
**Updated:** 2026-07-14  
**Scope:** `2026-CMS-Connectathon/`

This file is the working guide for AI-assisted contributions to the CMS Connectathon dataset. Read it before making changes. Update it only when project state, durable architecture, or a settled modeling decision changes.

Git history is the authoritative record of prior edits. Do not use this file as an exhaustive session transcript.

## 1. Project purpose

This folder contains loadable interoperability test data and supporting artifacts for OHIA CMS Connectathon scenarios. A participant should be able to:

1. read a clinician-friendly use case;
2. identify the interaction they want to test;
3. load the required fixtures;
4. execute or simulate the exchange; and
5. validate the expected FHIR, HL7 v2, CDS Hooks, payer, and imaging behavior.

FHIR content targets **FHIR R4**.

The separate `2026-usrealm-testdata/` folder at the repository root is not part of this dataset and must not be modified as a side effect of CMS scenario work.

## 2. Current project state

Loadable purpose-built FHIR fixtures currently exist for five scenario variants:

| Scenario | Folder | Interactions present |
|---|---|---:|
| UC01 | `uc01-medical-to-dental/` | 4 |
| UC02a | `uc02a-surgical-extraction/` | 5 |
| UC02b | `uc02b-commercial-implant/` | 5 |
| UC03 | `uc03-pediatric-referral/` | 5 |
| UC04a | `uc04a-teledentistry-commercial/` | 5 |

The CMS folder currently contains 287 JSON files and 26 files whose names identify them as Bundles. Treat those numbers as descriptive, not contractual; recompute them before publishing a release or claiming parity.

UC05 has narrative content but no corresponding folder under `fhir-resources/purpose-built/` at the time of this update.

Do not describe the repository as early-stage or claim that only UC01 Interaction 1 is built. Those statements are obsolete.

## 3. Repository structure

```text
2026-CMS-Connectathon/
├── CLAUDE.md
├── README.md
├── companion-guides/
│   ├── stakeholder-matrix.md
│   ├── UC01-companion-guide.md
│   ├── UC01-readiness-checklist.md
│   ├── UC02a-companion-guide.md
│   ├── UC02b-companion-guide.md
│   ├── UC03-companion-guide.md
│   └── UC04a-companion-guide.md
├── fhir-resources/
│   ├── durable/
│   └── purpose-built/
├── hl7v2/
└── use-cases/
```

Cross-repository proposals do not belong here. Changes for repositories such as `ode-360x-adapter` or `ohia-fhirr4-scratchpad` must be delivered and tracked in those repositories.

## 4. Encounter and interaction are different concepts

Never use these terms interchangeably.

- **Encounter:** a real clinical visit or event in the narrative.
- **Interaction:** a testable interoperability exchange.

The clinical story can contain encounters that do not need dedicated test fixtures. A single interaction can also span more than one encounter.

Use-case documents explain the clinical story. FHIR and HL7 v2 folders are organized by interaction. Companion guides connect the narrative to the technical fixtures.

## 5. FHIR fixture tiers

The three-tier structure is settled:

| Tier | Location | Contents | Reusable? |
|---|---|---|---|
| Durable | `fhir-resources/durable/` | Organizations, practitioners, locations, endpoints, insurance plans, payer rules, CDS Hooks discovery configurations, and other reusable infrastructure | Yes |
| Use-case base | `fhir-resources/purpose-built/<scenario>/base/` | Patient, coverage, consent, PractitionerRole, subscriptions, and other episode-level state | No |
| Interaction | `fhir-resources/purpose-built/<scenario>/interactions/interaction-0N/` | Encounter, ServiceRequest, Task, Observation, Condition, Provenance, Bundles, and other exchange-specific resources | No |

`PractitionerRole` is normally use-case base data, not durable data, because the clinician-organization-specialty-location relationship can vary by scenario even when the Practitioner is reusable.

## 6. Bundle conventions

Interaction Bundles should make their intended execution semantics explicit.

Before adding or rebuilding a Bundle, confirm:

- the Bundle type;
- whether it is cumulative or contains only the current interaction;
- whether it assumes durable and base fixtures are already loaded;
- how earlier versions of the same logical resource are superseded;
- whether request entries use `POST`, `PUT`, conditional create, or another method;
- whether the Bundle is intended to be idempotent; and
- which external services remain outside the Bundle.

Do not call a Bundle “self-contained” without qualifying what that means. A Bundle can include all required FHIR metadata while still depending on external CDS Hooks, SMART, payer, DICOMweb, or messaging services.

Some scenario variants reuse logical IDs. Assume scenarios must be loaded into isolated servers or reset environments unless the fixture set explicitly guarantees global ID uniqueness.

## 7. Referral and Task modeling

A referral request and its coordination state are distinct but related concepts:

- `ServiceRequest` represents the requested clinical service.
- `Task` represents coordination, fulfillment, and workflow state.

Do not create multiple coordination Tasks for one request merely to represent every sub-step. Existing scenarios generally use a single coordination Task whose status, business status, output, notes, and ownership evolve over time.

`Task.owner` should represent the responsible accepting party only when ownership is established. Do not populate it prematurely at initial intake.

Use `PractitionerRole` when requester or performer context depends on both clinician and organization.

Not every informal clinician exchange deserves a standalone `Communication` or `CommunicationRequest`. A note or annotation can be the more faithful model when the exchange is informal and embedded in an established workflow. Preserve discrete clinical results as formal resources when appropriate.

## 8. Dental imaging architecture

Imaging is a first-class test pattern, not an incidental attachment.

The standing technical model is:

```text
CDex exchange pattern
        ↓
FHIR ImagingStudy / DocumentReference metadata
        ↓
DICOM / DICOMweb / WADO-RS image retrieval
```

Important rules:

- `ImagingStudy` does not contain image pixel data.
- DICOM Study, Series, and SOP Instance UIDs identify the imaging objects.
- `ImagingStudy.endpoint` can identify a DICOMweb or WADO-RS endpoint.
- `DocumentReference` can describe radiographs, periodontal charts, intraoral images, and related documents, but it must not be used to pretend that large DICOM studies are embedded when they are not.

Transport is direction-dependent:

- **Medical-involved exchange:** use a separate attachment push when the medical participant exposes no inbound pull capability.
- **Dental-to-dental exchange:** use support-a-pull, allowing the receiver to retrieve the requested content.

Do not re-derive this choice for every scenario. Confirm the participants and apply the established direction rule.

## 9. Implementation-guide discipline

Do not infer profile behavior from resource names or from a different implementation guide.

For every profile-dependent change:

1. identify the exact FHIR and package version;
2. verify the profile, extension, cardinality, terminology binding, and invariant in the published package or official source;
3. distinguish required conformance from local test conventions;
4. document accepted warnings or known limitations; and
5. avoid fabricating elements that do not exist in FHIR R4.

Implementation guides exercised across the repository can include US Core, CRD, DTR, PAS, CDex, 360X, ODE, SMART App Launch, CARIN Blue Button, and payer/provider access patterns. Not every guide applies to every interaction.

The stakeholder matrix is the cross-use-case index for relevance. Keep it synchronized with scenario content.

## 10. Terminology and identifiers

Use standard terminology when the code is verified and appropriate. Otherwise, use clearly labeled text rather than an invented or weakly supported code.

When adding coded data:

- verify the system URI and code;
- use display text consistent with the selected code system version;
- document local or proprietary terminology;
- preserve CDT usage restrictions; and
- do not treat a warning-free validator run as proof of clinical correctness.

Identifiers must be synthetic and deterministic enough for testing. Never commit real member IDs, provider credentials, secrets, access tokens, or protected health information.

## 11. Validation requirements

Every change to FHIR content must be checked at multiple levels.

### Minimum automated checks

- Parse every changed JSON file.
- Confirm the expected `resourceType`.
- Resolve local references across durable, base, and interaction fixtures.
- Check Bundle entry request methods and URLs.
- Detect duplicate logical IDs in the intended load scope.
- Recompute Bundle entry counts after rebuilding.
- Validate against FHIR R4 and the exact implementation-guide packages used by the test track.

### Review requirements

- Compare the fixtures with the clinical narrative.
- Confirm dates and status transitions form a coherent timeline.
- Confirm payer, provider, HIE, and administrator roles match the scenario's real administrative model.
- Confirm imaging metadata points to plausible DICOM retrieval infrastructure.
- Confirm no dependency is implied to be bundled when it actually requires a stub or external endpoint.

Never report “all references resolve” or “validation passed” without running the relevant check on the current files.

## 12. Documentation synchronization

A scenario change is incomplete until all affected layers agree:

- use-case narrative;
- durable resource registry;
- base fixtures;
- interaction fixtures;
- transaction or collection Bundles;
- HL7 v2 examples, when applicable;
- companion guide;
- readiness checklist, when applicable;
- stakeholder matrix; and
- relevant README files.

Use relative links and verify that every documented file path resolves.

Do not preserve stale status text in the main guidance. Historical details belong in Git history, release notes, or a dedicated changelog.

## 13. Working rules for AI-assisted changes

- Read the relevant use case, companion guide, and existing interaction before creating resources.
- Prefer extending an established scenario pattern, but do not copy it blindly when payer, direction, transport, or clinical context differs.
- Keep edits scoped. Do not refactor unrelated scenarios during a focused change.
- State assumptions in documentation or resource notes when they affect test behavior.
- Do not batch-generate clinically meaningful interactions from naming patterns alone.
- Do not invent external API behavior, profile constraints, or code-system values.
- Preserve user-authored material unless the requested change requires editing it.
- Use Git history for provenance; do not append long conversational session logs to this file.

## 14. Definition of done

A change is complete when:

1. the clinical and administrative intent is clear;
2. resources are placed in the correct tier;
3. references and Bundles are rebuilt and verified;
4. profile and terminology choices are supported;
5. documentation and stakeholder mappings are synchronized;
6. synthetic-data and credential safeguards are satisfied; and
7. the repository can be used by a participant without relying on undocumented chat context.

## 15. Current maintenance priorities

The next repository-wide improvements should focus on:

1. adding machine-readable manifests for scenarios and interactions;
2. documenting exact FHIR package versions per Connectathon release;
3. adding repeatable CI validation for JSON, references, Bundles, and profiles;
4. recording accepted validator warnings;
5. making load isolation and logical-ID collision behavior explicit; and
6. separating current project state from historical change logs.
