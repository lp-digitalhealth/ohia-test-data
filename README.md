# OHIA Interoperability Test Data

Synthetic test data and implementation artifacts for Oral Health Interoperability Alliance (OHIA) Connectathon testing.

The repository supports dental and medical-dental interoperability workflows using FHIR R4, Da Vinci implementation guides, HL7 v2, X12 dental transactions, CDS Hooks, SMART App Launch, and DICOM-oriented imaging exchange patterns.

> **Synthetic data only:** The people, identifiers, clinical events, and organizations represented as test fixtures are synthetic, fictionalized, or used solely for interoperability testing. Do not treat this repository as a source of real patient data.

> **CDT code usage notice:** CDT procedure codes in this repository are used with permission from the American Dental Association solely for OHIA Connectathon testing and interoperability demonstrations. Use outside OHIA testing or HL7 Connectathon events requires prior written approval from ADA and OHIA leadership. Contact [Mark Marciante](mailto:mmarciante@leavittpartners.com) before reuse.

## Datasets

### `2026-CMS-Connectathon/`

The active CMS Connectathon dataset. It contains clinical narratives, participant preparation guides, FHIR R4 test fixtures, CDS Hooks configurations, HL7 v2 examples, and interaction-level transaction Bundles.

Current scenario variants:

| Scenario | Description | Modeled interactions |
|---|---|---:|
| UC01 | Medical-to-dental referral for head and neck cancer treatment | 4 |
| UC02a | Dental referral for surgical extraction | 5 |
| UC02b | Commercial dental implant workflow | 5 |
| UC03 | Pediatric medical-to-dental referral | 5 |
| UC04a | Commercial teledentistry referral | 5 |

The repository also contains narrative material for UC05; loadable UC05 fixtures are not currently represented under `fhir-resources/purpose-built/`.

### `2026-usrealm-testdata/`

Test material created for the March 2026 U.S. Realm Connectathon. This is a separate dataset with its own patients, scenarios, FHIR resources, X12 837D artifacts, and implementation reports.

## Repository structure

```text
ohia-test-data/
├── README.md
├── LICENSE
├── 2026-CMS-Connectathon/
│   ├── CLAUDE.md
│   ├── README.md
│   ├── companion-guides/
│   ├── fhir-resources/
│   │   ├── durable/
│   │   └── purpose-built/
│   ├── hl7v2/
│   └── use-cases/
└── 2026-usrealm-testdata/
    ├── use-cases/
    ├── fhir-resources/
    ├── edi-resources/
    └── *-connectathon-data-report*/
```

## CMS dataset organization

The CMS dataset distinguishes a **clinical encounter** from a **test interaction**:

- An **encounter** is a real visit or event in the clinical narrative.
- An **interaction** is a specific interoperability exchange worth testing.

Not every encounter becomes a test interaction. An interaction can also span more than one clinical event.

FHIR fixtures use three tiers:

| Tier | Location | Purpose |
|---|---|---|
| Durable | `fhir-resources/durable/` | Reusable organizations, practitioners, locations, endpoints, plans, payer rules, and CDS Hooks discovery data |
| Use-case base | `fhir-resources/purpose-built/<scenario>/base/` | Patient- and episode-specific resources shared across the scenario |
| Interaction | `fhir-resources/purpose-built/<scenario>/interactions/interaction-0N/` | Resources and Bundles for a specific exchange |

This design allows a participant to load an entire interaction Bundle or assemble fixtures from the durable, base, and interaction layers.

## FHIR and imaging model

FHIR content is authored for **FHIR R4**. Scenario-specific resources may exercise profiles and workflows from implementation guides including:

- Da Vinci CRD, DTR, PAS, and CDex
- 360X and ODE referral patterns
- SMART App Launch
- CARIN Blue Button and payer/provider access patterns
- US Core and related U.S. Realm profiles

Dental imaging is modeled as a layered workflow:

```text
CDex exchange workflow
        ↓
FHIR ImagingStudy and DocumentReference metadata
        ↓
DICOM / DICOMweb / WADO-RS retrieval of image content
```

`ImagingStudy` describes and locates imaging data; it does not contain the DICOM pixel data itself.

The transport pattern depends on the participants:

- Medical-involved referrals use a separate attachment push when the medical endpoint does not support inbound pull.
- Dental-to-dental referrals use a support-a-pull pattern in which the receiver retrieves the requested content.

## Using the test data

1. Start with the clinical narrative in `2026-CMS-Connectathon/use-cases/`.
2. Review the matching file in `companion-guides/` and the stakeholder matrix.
3. Load durable resources required by the scenario.
4. Load the scenario's `base/` fixtures.
5. Load or submit the desired interaction Bundle.
6. Validate the resources against FHIR R4 and the package versions required by the selected test track.

Interaction Bundles are intended as test fixtures, but external services such as CDS Hooks endpoints, payer systems, DICOMweb servers, and SMART authorization servers may still need to be stubbed or configured by participants.

### Loading isolation

Some scenario variants intentionally reuse logical resource IDs. To avoid collisions, use one of these approaches:

- load each scenario into an isolated FHIR server or tenant;
- reset the server between scenarios; or
- rewrite fixture IDs as part of a local test harness.

Do not assume that every scenario can be loaded concurrently into one unpartitioned server without conflicts.

## Validation expectations

At minimum, contributions should satisfy all of the following:

- Every JSON file parses successfully.
- Every FHIR resource declares the intended `resourceType`.
- Local references resolve within the fixture set or are intentionally external.
- Transaction Bundle entries contain appropriate request methods and URLs.
- Profile declarations match the implementation-guide versions used for the test track.
- Terminology warnings and accepted exceptions are documented rather than silently ignored.
- No credentials, secrets, production endpoints, or protected health information are committed.

The exact validator package versions should be recorded with a release or test event because implementation-guide snapshots can change validation results.

## Contributing

Keep changes scoped to test data and supporting Connectathon documentation. Proposals for external repositories should be tracked in those repositories rather than added here.

When adding or changing a scenario:

1. Update the clinical narrative.
2. Update the companion guide and stakeholder matrix.
3. Add or revise durable, base, and interaction resources.
4. Rebuild affected Bundles.
5. Validate JSON, references, profiles, and expected resource counts.
6. Update `2026-CMS-Connectathon/CLAUDE.md` when a durable design decision or project-state change is made.

## License

See [LICENSE](LICENSE). Additional restrictions apply to CDT-coded content as described above.
