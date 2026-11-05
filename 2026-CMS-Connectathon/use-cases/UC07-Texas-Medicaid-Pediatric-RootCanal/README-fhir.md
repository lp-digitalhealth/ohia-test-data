# UC07 FHIR Fixtures — DentaQuest Texas: Root Canal, Build-Up, and Crown (Joe Castle)

Loadable FHIR R4 fixtures for UC07, generated from `UC-Pediatric-RootCanal-FHIR-Build-Data.md`. Layout follows `CLAUDE.md` §5 (three tiers). Copy `durable/` into `fhir-resources/durable/` and `purpose-built/uc07-pediatric-rootcanal/` into `fhir-resources/purpose-built/`.

```text
durable/                          organizations, practitioners, locations, endpoints, insurance plan, payer rules, CDS Hooks discovery
purpose-built/uc07-pediatric-rootcanal/
├── base/                         Patient, RelatedPerson, Coverage, PractitionerRole
└── interactions/interaction-01 … interaction-05/   one folder per interaction + a cumulative bundle each
```

## Load order and bundle semantics

- Load **durable → base → interaction N**. Every file has a fixed `id`; load with `PUT [base]/{ResourceType}/{id}`.
- Each `interaction-0N-bundle.json` is a **transaction** Bundle, **cumulative**, all entries `PUT`. It contains durable + base + the *latest version* of every logical resource through interaction N, so each logical ID appears **once** (no duplicate IDs in a transaction). It assumes no other fixtures are pre-loaded; it does **not** include external services (DICOMweb, payer CRD/DTR/PAS endpoints, ARex content server, X12 clearinghouse).
- Resources that change keep their `id` and appear in a new-version file in the interaction that changes them: `task-referral` (I1 `-accepted`, I2 `-appointment-confirmed`, I4 `-closed`), `servicerequest-referral` (I1 active, I4 `-completed`).
- UC07 logical IDs differ from UC02a's, but reuse practitioner/org *names* (Dr. Mary Parker, DentaQuest). Load into an isolated/reset server, per `CLAUDE.md` §6.

## Counts (recompute before claiming parity)

71 JSON files: 17 durable (16 FHIR resources + 1 CDS Hooks discovery config, which is not a FHIR resource), 5 base, 44 interaction resources, 5 bundles; plus 3 ARex placeholder payload files. Bundle entry counts: I1 38, I2 48, I3 55, I4 60, I5 62.

## Decisions made during the build

1. **ARex manifest is a `List`** (profile `arex-manifest`), its entries are `DocumentReference`s (profile `arex-content-entry`), with `arex-digest` (sha-256), `arex-expires`, `arex-requires-access-token`, and `arex-transaction-context`. Verified against the published ARex v0.2.0 pages. Resolves build-data open item 1.
2. **Digests are real** over the three placeholder files in `interaction-02/arex-payloads/` (the URLs in each entry are synthetic). Replace payloads with real objects and recompute digests for a live test.
3. **ARex Provenance has no signature.** The detached JWS must be generated at test time (ARex §arex-5); it is intentionally not faked.
4. **Referral-package documents stay `DocumentReference`** (inline text); only the PA supporting documents use ARex. Resolves build-data open item 2.
5. **WADO-RS endpoints** use the SMART Imaging Access profile and extension `http://fhir.org/argonaut/smart-imaging/StructureDefinition/requires-access-token` (draft CI build). The build data cited a SMART App Launch URL for this extension; that was wrong and is corrected here.
6. **Guardian coding:** `RelatedPerson.relationship` carries v3-RoleCode `MTH` and `GUARD` (the build data cited v2-0131, which has no `MTH`). `Consent.category` is text-only.
7. **Per-line PA outcomes:** `ClaimResponse.item[]` carries the PAS `reviewAction` extension, X12 306 code `A1` ("Certified in total") for each of the three lines.
8. **DICOM UIDs** are deterministic synthetic `2.25.*` values (UUID-derived); no DICOM object exists behind them.
9. **Two Tasks** are kept (`task-referral`, `task-dtr`) because the narrative lists both; `CLAUDE.md` §7 prefers one. Decide before release.
10. **I5 `ExplanationOfBenefit` resources are an addition** to the narrative's resource list, mirroring UC02a-I5 and UC03-I5 (two claims, restorative one carries the PA number). Delete the two files if out of scope.
11. **Synthetic assumptions not in the narrative:** treatment end time 12:30, procedure times within the visit, practice street addresses, and the post-op `ImagingStudy` start time.
12. **DentaQuest** is modeled as a **new** durable `org-dentaquest-tx` (payer type, Payer ID `CX014`, no NPI) rather than reusing the existing `org-dentaquest`, to avoid editing UC02a's durable file. Consolidating the two is a follow-up.

## Not validated against profiles

Checks run: every file parses; expected `resourceType`; no duplicate IDs per bundle; every local reference resolves in each bundle; `PUT` URLs match resource type/id; NPIs pass Luhn (prefix 80840). **Not run:** HL7 FHIR Validator or any IG-profile validation (the package servers were unreachable from the build environment). Run the validator against R4 plus US Core, Da Vinci PAS, SMART Imaging Access, and ARex before use.

## Terminology notes

- CDT codes use `http://www.ada.org/cdt`; display text follows the existing fixtures' precedent. Confirm CDT descriptor publication rules for the public repo.
- ICD-10-CM `K02.53` for MOB decay into the pulp needs dentist confirmation (a smooth-surface code, `K02.63`, may fit better).
- No LOINC anywhere: radiograph `DiagnosticReport`s are coded with CDT (`D0220`, `D0270`).
