# UC07 FHIR test data — DentaQuest Texas: root canal, build-up and crown (Joe Castle)

**Status: DRAFT, November connectathon. Interactions 1, 2 and 4 (I1, I2, I4).** I3 and I5 are deferred (owner decision); I4 carries a minimal pull-in from I3. This file describes what is actually committed here. It replaces nothing: `../../../use-cases/UC07-Texas-Medicaid-Pediatric-RootCanal/README-fhir.md` describes a 71-file set that is **not** this folder and is not on any branch of this repository.

Narrative: [`UC07-Texas-Medicaid-Pediatric-RootCanal.md`](../../../use-cases/UC07-Texas-Medicaid-Pediatric-RootCanal/UC07-Texas-Medicaid-Pediatric-RootCanal.md). Test-server roles for the event: section 8 of [`UC07-companion-guide.md`](../../../use-cases/UC07-Texas-Medicaid-Pediatric-RootCanal/UC07-companion-guide.md).

## What is here

| Tier | Location | Files |
|---|---|---:|
| Durable (new, UC07) | `../../durable/` | 13: three organizations, two locations, two practitioners, three endpoints, and the DentaQuest D3320 / D2950 / D2740 prior-authorization rule (`PlanDefinition`, `Library`, `Questionnaire`) |
| Durable (edited) | `../../durable/cds-hooks/cds-hooks-discovery-dentaquest.json` | A second `order-sign` service added next to the D7210 one (the only existing file edited; 10 lines appended) |
| Base | `base/` | 5: `Patient`, `RelatedPerson`, `Coverage`, two `PractitionerRole` |
| Interaction 1 | `interactions/interaction-01/` | 22 resources + `interaction-01-bundle.json` + 2 placeholder image payloads in `arex-payloads/` |
| Interaction 4 | `interactions/interaction-04/` | 14 resources + `interaction-04-bundle.json` + 1 placeholder payload in `arex-payloads/` |
| Interaction 2 | `interactions/interaction-02/` | 11 resources + `interaction-02-bundle.json` + 3 payload files in `arex-payloads/` (two placeholder PNGs, one synthetic clinical note) |

The new durable files are `org-pediatric-dental-tx`, `org-restorative-dental-tx`, `org-dentaquest-tx`, `loc-pediatric-dental-tx`, `loc-restorative-dental-tx`, `pract-mary-parker`, `pract-max-garcia`, `endpoint-pediatric-fhir`, `endpoint-restorative-fhir`, `endpoint-dentaquest-tx`. They are **new records** and no existing durable file was edited: UC02a already has a `pract-parker` (a different clinician, NPI and practice) and an `org-dentaquest` (different endpoint and identifiers).

## I1 content (what the narrative's first interaction needs)

Evaluation record (`encounter-eval`, two diagnoses for tooth #4, two uncoded findings), two radiographs as `ImagingStudy` pointers with CDT-coded `DiagnosticReport`s, clinical notes and treatment plan, three CDT procedures (D0140, D0220, D0270), the referral `ServiceRequest` (`ode-dental-to-dental-referral`), the provider-to-payer `Communication`, the single referral `Task`, a `Provenance`, and an ARex manifest of the two image entries (see below).

## I2 content (prior authorization for D3320, D2950, D2740)

- **Payer rule (durable, synthetic DentaQuest policy, owner-approved):** `plandef-dentaquest-d3320-d2950-d2740-pa-rule`, `lib-dentaquest-d3320-d2950-d2740-pa-logic` (a **stub**: the CQL header only, like the D7210 library; the rule is stated in its description and applied by the test server's CRD service, not by executing CQL) and `questionnaire-dentaquest-d3320-d2950-d2740-pa-dtr`. Rule: the three services on one tooth are one bundled request, decided as one authorization with one result per line; clinical notes and radiographs are required.
- **DTR:** `questionnaireresponse-dentaquest-pa` (answers all eight Questionnaire items) and `task-dtr`, a documentation-requirement `Task` (requester DentaQuest, owner the restorative practice) closed when the authorization is decided, as the narrative says. It is **not** a second coordination Task for the referral: that remains the single `task-referral`.
- **PAS:** `claim-pa-request` (use `preauthorization`, three service lines on tooth #4, K02.53 principal and K04.7) and `claimresponse-pa-approval` (outcome `complete`, PA `TX-DQ-PA-2026-061204`, 2026-07-15 to 2027-01-11 = 180 days, one `A1` "Certified in total" result per Claim line).
- **ARex:** `arex-manifest-pa-docs` with three entries, `arex-entry-pa-periapical`, `arex-entry-pa-bitewing`, `arex-entry-pa-narrative` (real SHA-256 over the files in `arex-payloads/`), and `arex-provenance-pa-docs` (placeholder signature, as in I1). The entry ids carry `-pa-` because I1's `arex-entry-periapical` and `arex-entry-bitewing` are different resources (the referring practice's server); the companion guide listed the I1 ids and has been corrected.
- **Scheduling:** `appointment-consultation` (2026-07-22 09:30) and `task-referral`, updated under the **same id** (see Bundle semantics).

### How the Claim finds the ARex manifest (local convention, owner decision)

ARex defines no link from a `Claim` to a manifest. Two links are used and a check asserts they agree:

1. `Claim.identifier[1]` (`https://restorativedental.example.org/pa-request-id|PA-REQ-2026-UC07-001`) is the same identifier as the manifest's transaction-context `businessIdentifier`, so a payer finds the manifest through ARex's `transaction-identifier` search parameter.
2. `Claim.supportingInfo[2]` references the manifest `List` directly, under the local category `urn:ohia:claim-supporting-info-category|arex-manifest`.

**Why a local category (a PAS finding):** PAS 2.2.1 `profile-claim` restricts the `AdditionalInformation` slice's `value[x]` to a short list of reference targets that does not include `List`. Slicing is open, so a `supportingInfo` entry with a different category falls outside that slice. The HL7 validator reports it as an information message ("does not match any known slice") and one warning (the code is not in the extensible `PASSupportingInfoType`); **no error**.

### PAS findings to feed back to the PAS authors (known errors left in the data on purpose, owner decision)

| # | Finding | Where | Effect on this data |
|---|---|---|---|
| 1 | `Claim.item.productOrService` has a **required** binding to `X12278RequestedServiceType`, which lists CPT, HCPCS, ICD-10, NDC and X12 codes but **not CDT** (`http://www.ada.org/cdt`). PAS allows the `oral` claim type, but an oral PA cannot carry its CDT procedure code without this error. CARIN Blue Button's Oral EOB profile, by contrast, binds the corresponding element to CDT (from a search summary, not read in full). The IG authors have told the owner that PAS should allow CDT; the published 2.2.1, current-build and 2.0.1 value sets do not. | `profile-claim-base`, `Claim.item.productOrService` | The Claim uses CDT only and still claims the PAS profile, so the validator reports **3 errors**, one per service line. The existing UC02a PAS Claims have the same defect (not edited, not validated here). **An interim OHIA overlay profile exists** that differs from PAS only in accepting CDT there (`ohia-fhir-test-server/ig-overlay/`): against it the same Claim has 0 errors. This Claim does not claim the overlay yet (owner to decide). |
| 2 | `AdditionalInformation.value[x]` does not allow a `List`, so there is no profile-conformant way to point a PAS Claim at an ARex manifest in that slice. | `profile-claim`, `Claim.supportingInfo:AdditionalInformation.value[x]` | The local category above. |

### Values in I2 not in the narrative (ASSUMPTIONS)

- PA request identifier `PA-REQ-2026-UC07-001`, claim identifier `PA-CLM-2026-UC07-001`, manifest identifier `MAN-2026-0710-0001`, response identifier `PA-REQ-2026-UC07-001-R1`.
- `QuestionnaireResponse` authored 2026-07-10 08:45 (the narrative gives 08:15 for DTR and 09:00 for submission, nothing between).
- Appointment end 10:00 is the narrative timeline's next event (treatment completed 10:00), not a booked duration.
- The referral `Task` moves directly from `referral-sent` to `appointment-confirmed` and gets its `owner` (Dr. Garcia) at 2026-07-15 15:00: the narrative has no separate "accepted" step.
- X12 codes not in the PAS package and **not verified**: item category `26` (Endodontics) and `25` (Restorative), care-team role `82` (Rendering Provider), report type `OZ`, review action `A1`. The systems and the `HS` / `I` / POS `11` values match the PAS package's own examples.
- The ARex manifest's `requestingOrganization` is DentaQuest (the party that retrieves); in I1 it is the receiving practice.
- The payer-rule canonical URLs use the synthetic base `https://dentaquest.example.org/fhir/`.

## I4 content (closing the loop, 2026-07-22 13:30 to 13:35)

- **The push from Dr. Garcia to Dr. Parker:** `clinicalimpression-posttx-summary` (the narrative's summary text, verbatim, with the three procedures, the post-op `ImagingStudy` and the note as `investigation`), `documentref-postop-clinical-note` (text note, inline like I1's), `careplan-posttx` (the narrative's three recommendations as three activities), and `communication-thank-you` (the narrative's text, verbatim).
- **The thank-you is deliberately separate:** a `Communication` with category "provider-to-provider courtesy communication (non-clinical)". It is referenced by no clinical resource and is not a `Task.output`, so a receiving system can tell courtesy from clinical content (the test in the I4 narrative).
- **Post-op radiograph, by ARex:** `imagingstudy-postop` (pointer) + `arex-manifest-postop` + `arex-entry-postop-periapical` (real SHA-256 over `arex-payloads/radiograph-postop.png`, an 8x8 placeholder) + `arex-provenance-postop` (placeholder signature). The requesting organization is the **pediatric** practice (the party that retrieves).
- **Referral closed (13:35):** `servicerequest-referral` (same id as I1, `completed`) and `task-referral` (same id as I1 and I2, `completed`, `businessStatus` `outcome-final`, the ODE sub-status UC04a and UC02b use for a closed referral). `Task.output` lists the fulfillment set; the thank-you is not in it.

### Minimal pull-in from the deferred I3 (owner decision)

The guide lists the treatment `Encounter` and the three `Procedure`s under I3, which is deferred. At the owner's direction I4 includes `encounter-treatment`, `procedure-d3320`, `procedure-d2950` and `procedure-d2740` so the summary has structured links. The consult `Encounter`, the `Consent` and the eligibility record stay with I3 and are **not** in this data set, so "guardian consent obtained" appears in the summary text only. `Procedure.basedOn` can reference only a `CarePlan` or `ServiceRequest`, so each procedure is `basedOn` the referral and traces the PA number (`TX-DQ-PA-2026-061204`) in its note.

### Consequence of reusing the referral id for the post-op manifest (owner decision, option B)

The I4 manifest and its `ImagingStudy` carry the same business identifier as the I1 radiograph manifest (`urn:ohia:referral-id|REF-2026-UC07-001`). An ARex `transaction-identifier` search for the referral id therefore returns **two** manifests (I1 and I4); the I2 manifest uses the PA request id and is not returned. A consumer tells the two apart by `List.title`, `List.date` and `requestingOrganization`. A check asserts exactly this set.

### Values in I4 not in the narrative (ASSUMPTIONS)

- The treatment `Encounter` starts at 10:00 on 2026-07-22 (the narrative's single timestamp for the three procedures); there is no end time, and the procedures carry the date only.
- The post-op radiograph carries the date only (no time given), and is coded D0220 like the I1 radiographs; it is not billed in this data set.
- The post-op manifest expires 14 days after publication (13:30 on 2026-07-22), borrowed from the other manifests; the manifest identifier `MAN-2026-0722-0001` and the URLs are synthetic.
- `outcome-final` is taken from the sibling scenarios; the ODE profile source is not available here to confirm it.
- The I2 `Appointment` stays `booked` (the narrative does not call for an update after the visit).

## Radiographs: ARex manifest plus `ImagingStudy` pointer

Owner decisions for this event: radiographs are **an ARex manifest of image entries plus an `ImagingStudy` pointer**; WADO-RS is deferred.

- `arex-manifest-radiographs` is a `List` (profile `arex-manifest`) listing `arex-entry-periapical` and `arex-entry-bitewing` (`DocumentReference`, profile `arex-content-entry`). Each entry has an absolute `url`, a `size`, and a SHA-256 `arex-digest` computed over the file in `arex-payloads/`. No inline data.
- **Link convention (decided, not an ARex rule):** each `ImagingStudy.identifier` repeats the manifest's transaction-context `businessIdentifier` (`urn:ohia:referral-id|REF-2026-UC07-001`). A consumer finds the manifest with ARex's `transaction-identifier` search parameter. ARex v0.2.0 does not define any `ImagingStudy` link.
- The payload files are **8x8 placeholder PNGs, not radiographs**. The URLs are synthetic `example.org` addresses; for a live retrieval test the files must be served by an ARex content server.
- `arex-provenance-radiographs` carries a **placeholder signature**: the ARex Provenance profile requires `signature` (min 1), but a valid detached JWS cannot be committed here. `signature.data` is not a valid JWS and must be regenerated at test time.

## Bundle semantics (CLAUDE.md section 6)

**`interaction-04-bundle.json`** is a **transaction** Bundle, **cumulative** (13 UC07 durable files + base + I1 + I2 + I4: 62 entries), every entry a `PUT`, idempotent, and **it contains no I3 resources**. The I4 `servicerequest-referral` and `task-referral` supersede the I1 and I2 versions (same ids), so the earlier versions are not in this Bundle; loading the I2 Bundle then the I4 Bundle replaces them in place.

**`interaction-02-bundle.json`** is a **transaction** Bundle, **cumulative** (13 UC07 durable files + base + I1 + I2: 50 entries), every entry a `PUT`, idempotent. **Supersession:** the I2 `task-referral` has the same id as I1's, so the I2 Bundle contains only the I2 version and does not contain I1's. Loading I1's Bundle then I2's replaces the Task in place. Loading both folders' files individually would collide on that id. Same isolation rule as I1. The CDS Hooks discovery file is not a FHIR resource and is not in the Bundle. Unavailable here: the CRD, DTR and PAS endpoints and the ARex content server.

The I1 description follows.

`interaction-01-bundle.json` is a **transaction** Bundle, **cumulative** (the 10 UC07 durable files + base + I1), every entry a `PUT` to `ResourceType/id`, so loading is **idempotent**. It assumes an empty or reset server (do not load it beside UC02a in one unpartitioned server, per the repository's isolation rule). `fullUrl`s are valid lowercase UUIDs (v5, deterministic); references inside resources stay relative (`Type/id`). It does **not** include external services: the ARex content server, the payer CRD/DTR/PAS endpoints, or any X12 clearinghouse.

## I1 values not in the narrative (ASSUMPTIONS)

- Referral identifier `REF-2026-UC07-001` (the narrative names none).
- Referral `authoredOn` 10:15 (the narrative's transmission time) and notification 10:16; evaluation start 09:30; no encounter end time.
- ARex manifest expiry (14 days after publication, borrowed from the I2 window) and manifest identifier `MAN-2026-0708-0001`.
- Coverage `class` value `TX-MEDICAID-DENTAL`.
- No practice street addresses (the narrative gives none).
- DICOM UIDs are synthetic `2.25.*` values; no DICOM objects exist.

## Modeling choices to confirm

- **Referral code:** the first requested service (D3320) is in `ServiceRequest.code`; D2950 and D2740 are in `orderDetail`. One `ServiceRequest` carries the three-procedure plan, as the narrative describes.
- **ICD-10 K02.53** for the caries finding is as written in the narrative; the project notes it needs a dentist's confirmation (K02.63 may fit better).
- **Tooth code:** ADA Universal `4`, displayed as "Permanent maxillary right second premolar tooth" (the display the terminology requires, per the HL7 validator; UC02a's files display the bare number, and those files were not validated here).
- **Guardian:** `RelatedPerson.relationship` carries v3-RoleCode `MTH` and `GUARD`.
- **Single `Task`**, per CLAUDE.md section 7; `owner` is not set at I1.
- **DiagnosticReport** is coded with CDT (D0220, D0270), not LOINC, per the narrative.

## Notes moved out of resources

R4 `Organization` and `Coverage` have no `note` element, so these were removed from the resources and are recorded here:

- **`Organization/org-pediatric-dental-tx`** — UC07 referring practice (Dr. Mary Parker). Fictional practice; NPI is synthetic (UC07 narrative, Appendix A). Street address is not given in the narrative and is intentionally omitted.
- **`Organization/org-restorative-dental-tx`** — UC07 receiving practice (Dr. Max Garcia). Fictional practice; NPI is synthetic (UC07 narrative, Appendix A). Street address is not given in the narrative and is intentionally omitted.
- **`Organization/org-dentaquest-tx`** — UC07 payer. Real organization used as the payer identity; one of the Texas HHSC-contracted dental plans. Payer ID CX014 is the clearinghouse routing ID per the UC07 narrative. A payer carries no NPI. The endpoint is synthetic. This is a NEW record, separate from the existing org-dentaquest (UC02a), so UC02a's file is not edited; consolidating the two is a follow-up.
- **`Coverage/coverage-joe-castle-dentaquest`** — Medicaid (not CHIP); Texas Health Steps (EPSDT) eligible. Coverage period 2026-01-01 to 2026-12-31, status active (UC07 narrative). The class value TX-MEDICAID-DENTAL is an ASSUMPTION: the narrative gives no plan identifier.

## Validation (what was run, and what was not)

### I4

- **Structural checks** (author's script, not committed; no negative control was run): 62 files parse; file name equals `id`; no duplicate ids in the cumulative scope; all references and canonical references resolve; Bundle entries `PUT` with matching URLs (62 entries); all ARex entries (I1, I2, I4) match their payload files by SHA-256 and size; the post-op manifest, its `ImagingStudy` and the I1 manifest share the referral id and a search by it returns exactly those two manifests; three procedures on tooth #4 with the PA number traced; the `ClinicalImpression` summary and the thank-you text are the narrative's text verbatim; the thank-you is referenced by no clinical resource and is not a `Task.output`; the referral `Task` and `ServiceRequest` close with the same ids; the timeline is in narrative order and the push is five minutes before the referral closes. All passed.
- **HL7 FHIR Validator** (R4 4.0.1, `hl7.fhir.us.core#6.1.0`, the ARex profiles, `hl7.fhir.us.davinci-pas#2.2.1`; terminology **off**; `-allow-example-urls true`) on the cumulative I4 Bundle: **3 errors, 344 warnings, 41 information messages.** The 3 errors are PAS finding 1 (CDT on the I2 `Claim`); **none comes from an I4 resource.** The I4 resources raise only the known classes: CDT not checkable with terminology off, the ODE profiles and sub-status code system not found, the unreachable synthetic `example.org` attachment URL, and no US Core Encounter Type code on the treatment `Encounter` (as on I1's). The ARex manifest, entry and Provenance validate against the ARex profiles with no messages beyond those.
- **NOT validated:** the ODE profiles and the `outcome-final` sub-status; CDT, ICD-10 and DICOM codes; clinical correctness; no ARex content was actually retrieved.

### I2

- **Structural checks** (author's script, not committed; I1's checks plus I2 ones): 50 files parse; file name equals `id`; no duplicate ids in the cumulative scope; all local references and the three canonical references resolve; Bundle entries `PUT` with matching URLs, 50 entries; ARex digests and sizes match the files; the Claim's identifier equals the manifest's `businessIdentifier` and the Claim references the manifest `List`; 3 lines D3320 / D2950 / D2740 on tooth #4 with K02.53 + K04.7; one ClaimResponse result per Claim line; the PA window is exactly 180 days; the timeline is in narrative order; the DTR Task closes at approval; every QuestionnaireResponse `linkId` exists. All passed. These check internal consistency of data I wrote; no negative control (a deliberately broken copy) was run.
- **HL7 FHIR Validator** (R4 4.0.1, `hl7.fhir.us.core#6.1.0`, the ARex profiles, `hl7.fhir.us.davinci-pas#2.2.1` with its dependencies including US Core 7.0.0; terminology **off**; `-allow-example-urls true`) on the cumulative I2 Bundle: **3 errors, 257 warnings, 30 information messages.** The 3 errors are PAS finding 1 (CDT). A first run also found 3 relative-canonical errors in my own files (fixed by giving the `Library` and `Questionnaire` absolute `url`s). Warnings are the I1 classes plus X12 / CDT code systems that cannot be checked with terminology off, the extensible-binding warning from the local category, and two ODE canonicals not found.
- `QuestionnaireResponse` was checked against its `Questionnaire` in a separate run (the validator does not resolve it from inside the Bundle): **0 errors**, one narrative warning.
- **NOT validated:** X12 value sets (category, role, report type, review action, request / certification type) and ICD-10 / CDT codes; the ODE profiles; the PA rule is not executed (stub Library); no CRD, DTR or PAS service was called; the ARex content URLs are synthetic and unreachable, so digests were checked against the local files only. **Clinical correctness** was not assessed.

### I1

- **Structural checks** (author's script, not committed): all files parse; file name equals `id`; no duplicate logical ids; every local reference resolves; Bundle entries are `PUT` with matching URLs; entry count recomputed (37); NPIs pass the Luhn check; ARex digests and sizes match the payload files; each `ImagingStudy.identifier` matches the manifest's business identifier. All passed.
- **HL7 FHIR Validator** (R4 4.0.1, `hl7.fhir.us.core#6.1.0`, the ARex profiles from the IG, terminology **off**, `-allow-example-urls true` because this data is synthetic by design): **0 errors, 169 warnings, 18 information messages.**
- **What the warnings are:** best-practice notes (relative references versus the UUID `fullUrl`s; resources without narrative); code systems that could not be checked with terminology off (including CDT, NUCC taxonomy and BCP-47); two ARex content URLs the validator could not fetch (synthetic hosts).
- **NOT validated:** the **ODE profiles** (`ode-dental-to-dental-referral`, `ode-referral-task`) — the validator could not find them, so the referral and the Task were checked against the base resources only; the ODE profile source is unbuilt FSH. **CDT, NUCC and BCP-47 codes** were not checked. **Clinical correctness** was not assessed.
- `fullUrl` form: UC04a's bundle uses `urn:uuid:Type-id`, the same form the validator rejected as "not a valid UUID" in this folder's first draft. Other bundles were not validated here. UC07 uses valid UUIDs.
