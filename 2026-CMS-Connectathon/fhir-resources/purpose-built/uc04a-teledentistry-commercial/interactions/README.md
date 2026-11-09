# UC04a Per-Interaction FHIR Resources

Commercial **teledentistry** referral for **Sarah Okonkwo** (age 34, acute front-tooth pain on biting, no dental home), covered by an employer-sponsored **Aetna Dental PPO**, from a virtual-care platform (**Meridian Teledental**, Dr. Webb) to an in-office general practice (**Barton Springs Dental Group**, Dr. Nair). **All five interactions (I1–I5) are built as FHIR resources** (see [`../../../../use-cases/UC04-teledentistry-referral/interactions/README.md`](../../../../use-cases/UC04-teledentistry-referral/interactions/README.md) for the business writeups).

Transactional resources specific to each interaction live here; base/registry resources live in [`../base/`](../base/) and the durable registry [`../../../durable/`](../../../durable/).

## What makes UC04a structurally different (don't pattern-match from UC01/UC02/UC03)

- **Virtual originating provider.** Dr. Webb sees Sarah over synchronous video (POS 02) and cannot take a radiograph — so there is **no diagnostic radiograph, no `ImagingStudy`, no DICOM/WADO-RS/PACS at referral**. The radiograph first appears in-office at I3.
- **Patient-submitted intraoral photos, by ARex reference.** The one image artifact at I1 is 1–2 phone photos Sarah captures through the app: an ARex manifest (`arex-manifest-intraoral-photos.json`, a `List`) of two content entries (`arex-entry-photo-1.json`, `arex-entry-photo-2.json`: US Core-style `DocumentReference`, `image/jpeg`, absolute `url`, SHA-256 digest, `author` = Patient) with a placeholder-signed `Provenance` — nothing inline; **not** an R4 `Media`, and **not** DICOM. Rationale: ONC's R4 → R6 path (skipping R5) removes `Media` but keeps `DocumentReference`; US Core profiles `DocumentReference` and CDex uses it; through a 360X/C-CDA bridge the bytes survive either way. Because R4 `DocumentReference` has no `bodySite`, the affected tooth (#9) is carried on the symptom `Observation` (`bodySite` + `derivedFrom` → the photos).
- **Dental-to-dental CDex provider-to-provider push.** The referral travels **directly** to the in-office practice's **interim FHIR server** — not HIE-routed like UC03's Connie, not a 360X bridge like UC01/UC02. The photos travel **by ARex reference** (the receiver retrieves each entry and verifies its digest; no DICOM support-a-pull like UC02).
- **No CRD/DTR/PAS.** The commercial plan requires no prior authorization for the virtual consult (D9995), radiograph (D0220), root canal (D3310), or composite restoration (D2330). Coverage is verified active in real time at I1 — a benefit lookup, not a PA cycle. No `Claim`/`ClaimResponse` PA, no CDS-Hooks/PlanDefinition.
- **No Plan-Net.** The commercial patient is referred to a known in-network practice; the provider-directory query is UC04b's (Medicaid) test.
- **No HL7v2.** UC04 is entirely FHIR.
- **Adult self-authorization.** Sarah is an adult — the patient-app `Subscription` (in `base/`) is a straightforward self-auth SMART flow, no guardian proxy (contrast UC03).

## Interaction 1 — Tuesday Night Pain (built) — 2026-07-14 virtual encounter (19:32–19:58)

After-hours virtual visit: coverage verified active, Dr. Webb documents symptoms + reviews patient photos, and creates a `priority: urgent` dental-to-dental referral pushed via CDex to Barton Springs.

- `encounter-01-virtual.json` — Encounter (`class: VR`, POS 02; Dr. Webb, Meridian)
- `condition-k04-01-pulpitis.json` — Condition (ICD-10-CM **K04.01** irreversible pulpitis, tooth #9 Universal — **no FDI**; **provisional** (suspected) — radiographic confirmation deferred to I3)
- `observation-symptoms.json` — Observation (symptom components: duration, pain on biting, thermal sensitivity, spontaneous aching; `bodySite` tooth #9; **`derivedFrom` → the two ARex photo entries** — the R4 tooth-correlation work-around; **text-only code**)
- `observation-tobacco-status.json` — Observation (`us-core-smokingstatus`, LOINC 72166-2, SNOMED "Never smoked tobacco")
- `medicationstatement-ibuprofen.json` — MedicationStatement (patient-reported OTC ibuprofen; RxNorm ingredient 5640)
- `documentreference-virtual-findings.json` — DocumentReference (text clinical-note wrapper — **not an image**)
- `observation-dental-home.json` — Observation (patient-reported dental history: **no dental home**, has not seen a dentist in some time; text only, no date asserted)
- `arex-manifest-intraoral-photos.json` — List, ARex manifest of the two photos; business identifier = the referral id; expiry assumed 14 days after publication
- `arex-entry-photo-1.json`, `arex-entry-photo-2.json` — DocumentReference (ARex content entries; `image/jpeg`; real SHA-256 over `arex-payloads/intraoral-photo-*.jpg`, which are 8x8 **placeholder** JPEGs; `author` = Patient; **not DICOM**)
- `arex-provenance-intraoral-photos.json` — Provenance (signs the manifest; **placeholder** signature, regenerate the detached JWS at test time)
- **Not yet authored:** the referral's `AllergyIntolerance`. The narrative says the referral carries allergies but names none; it waits for the owner's allergy.
- `servicerequest-referral.json` — ServiceRequest, `ode-dental-to-dental-referral`: `urn:ohia:referral-id` `REF-2026-UC04A-001`, `priority: urgent`, `reasonCode` K04.01 + `reasonReference` → Condition, `bodySite` tooth #9, `supportingInfo` → 3 Observations (symptoms, tobacco, dental home) / MedicationStatement / the findings DocumentReference / the ARex manifest, `insurance` → Coverage, `occurrenceDateTime` 2026-07-15. **No PA; photos travel by ARex reference.**
- `task-referral-tracking.json` — Task, `ode-referral-task`: task-code `fulfill`, `businessStatus: referral-sent`, `focus` → referral, no `owner` yet. Note reflects **CDex provider-to-provider push, no HIE/360X**
- `provenance-referral.json` — Provenance (author Dr. Webb/Meridian; transmitter Meridian, CDex push)
- `interaction-01-bundle.json` — self-contained transaction bundle: registry + base + I1 (**30 entries**)

## Interaction 2 — An Appointment by Morning (built) — 2026-07-14 same-evening scheduling (20:06–20:47)

Barton Springs' interim FHIR server receives the referral within a minute, and staff book Sarah for the next morning, returning an `AppointmentResponse` to Meridian.

- `appointment-inoffice.json` — Appointment (`status: booked`, `basedOn` the referral, `start` 2026-07-15 10:00; Sarah + Dr. Nair + location; created 20:47)
- `appointmentresponse-inoffice.json` — AppointmentResponse (accepted, returned to Meridian via CDex the same evening)
- `task-referral-tracking-accepted.json` — Task (**snapshot** of the I1 referral Task → `businessStatus: appointment-confirmed`, `owner` = Dr. Nair; same `id` — version history)
- `provenance-appointment.json` — Provenance (author Dr. Nair/Barton Springs; transmitter Barton Springs, CDex back to Meridian)
- `interaction-02-bundle.json` — self-contained transaction bundle: registry + base + I1 + I2 (**33 entries**; the I2 Task snapshot overrides the I1 Task by shared `id`)

**This** milestone (appointment confirmed) fires to Sarah's app; the referral-sent milestone fired at I1. No patient-facing event for the provider-to-provider mechanics themselves.

## Interaction 3 — The Root Canal (built) — 2026-07-15 in-office visit (10:00–12:15)

The **first — and only — radiograph** in UC04a appears here, generated **in-office** and **not exchanged** back to Meridian. Dr. Nair confirms the diagnosis and completes a single-visit root canal.

- `encounter-03-inoffice.json` — Encounter (`class: AMB`, POS 11; Dr. Nair, Barton Springs; `basedOn` the referral)
- `imagingstudy-periapical.json` — ImagingStudy (modality IO, tooth #9; `endpoint` → `endpoint-barton-springs` as **WADO-RS** — DICOM/pointer metadata only; **in-office-only, not exchanged**)
- `diagnosticreport-periapical.json` — DiagnosticReport (LOINC 62443-7 / CDT D0220; `imagingStudy` → above; conclusion = periapical rarefaction consistent with abscess)
- `observation-periapical-findings.json` — Observation (radiographic findings, tooth #9; `derivedFrom` → the DiagnosticReport; text-only components)
- `condition-k04-01-pulpitis-confirmed.json` — Condition **snapshot** of the I1 pulpitis Condition (same `id`) → `verificationStatus: confirmed`, encounter/asserter → in-office
- `condition-k04-7-periapical-abscess.json` — Condition (new in-office diagnosis, **K04.7** periapical abscess without sinus, tooth #9 — source's "K04.5" corrected per verification discipline)
- `procedure-d3310-rootcanal.json` — Procedure (CDT **D3310** root canal, anterior, tooth #9 Universal — **no FDI**; completed 2026-07-15; `reasonReference` → both Conditions)
- `procedure-d2330-composite.json` — Procedure (CDT **D2330** single-surface direct composite, lingual, tooth #9; same visit; restores the access — a crown is still indicated)
- `interaction-03-bundle.json` — self-contained transaction bundle: registry + base + I1 + I2 + I3 (**40 entries**; confirmed Condition and appointment-confirmed Task override earlier versions by shared `id`)

## Interaction 4 — Reporting Back (built) — 2026-07-15 closed-loop summary (12:35)

Dr. Nair pushes a structured encounter summary back to Meridian via CDex — a **single recipient** (contrast UC03's dual fan-out) — closing the referral loop.

- `clinicalimpression-summary.json` — ClinicalImpression (Dr. Nair → Dr. Webb; `problem` K04.01/K04.7, `investigation` → D3310 and D2330 Procedures + periapical report, full summary text)
- `careplan-posttreatment.json` — CarePlan (definitive crown by a dentist she establishes as her dental home, 6-month follow-up radiograph, ibuprofen PRN)
- `servicerequest-referral-completed.json` — ServiceRequest **snapshot** (same `id`) → `status: completed`
- `task-referral-tracking-completed.json` — Task **snapshot** (same `id`) → `status: completed`, `businessStatus: outcome-final`, `output` → summary + care plan + confirmed Condition + Procedure
- `task-summary-delivery.json` — Task (single CDex summary-delivery, Barton Springs → Meridian; `focus` → the ClinicalImpression)
- `provenance-summary.json` — Provenance (author Dr. Nair/Barton Springs; transmitter Barton Springs, CDex push to Meridian)
- `auditevent-summary.json` — AuditEvent (cross-org access log for the summary push, Barton Springs → Meridian)
- `interaction-04-bundle.json` — self-contained transaction bundle: registry + base + I1–I4 (**45 entries**; completed Task/ServiceRequest override earlier versions by shared `id`)

The referral-complete milestone ("visit summary available") fires to Sarah's app via the base-tier `Subscription`.

## Interaction 5 — Two Bills, One Visit (built) — 2026-07-16 two-organization claims-sharing

Two **independent** claims-sharing packages, one per submitting organization — the first time this project's profile represents two billing organizations for one coordinated episode.

- `procedure-d9995-teledentistry.json` — Procedure (CDT **D9995** synchronous teledentistry, POS 02, Dr. Webb, `encounter` → the I1 virtual Encounter) — the billable virtual consult underlying EOB #1; filed here (the billing interaction) rather than churning the committed I1 bundles
- `eob-teledentistry-claims-sharing.json` — ExplanationOfBenefit **#1** (`ode-dental-claim`): insurer Aetna, provider Meridian, rendering Dr. Webb, one line **D9995** (POS 02), diagnosis K04.01, `supportingInfo` → referral; **no PA ref**
- `eob-inoffice-claims-sharing.json` — ExplanationOfBenefit **#2** (`ode-dental-claim`): insurer Aetna, provider Barton Springs, referring Dr. Webb + rendering Dr. Nair, three lines **D0220 + D3310 + D2330** (POS 11, tooth #9), diagnoses K04.01 + K04.7, `supportingInfo` → same referral; **no PA ref**
- `interaction-05-bundle.json` — self-contained transaction bundle: registry + base + I1–I5 (**48 entries**)

The two EOBs are tied together only by the shared referral-id (`REF-2026-UC04A-001`), not a joint claim — CDT-only, no CPT crosswalk (dental payer), non-financial (no adjudication) by profile design.

**Known limitation — the EOBs don't validate against `ode-dental-claim`, so the I5 bundle is rejected when sent with profile validation.** `ode-dental-claim` (ohia-fhirr4-scratchpad `profiles/claims.fsh`) derives from CARIN Blue Button's `C4BB-ExplanationOfBenefit-Professional-NonClinician-Basis`, and the two conflict: CARIN's required claim-type binding doesn't allow `oral`, and CARIN requires `item.adjudication` (with `benefitpaymentstatus`), while this EOB is non-financial by design. No conforming instance is possible until the profile changes there. The scratchpad's `sushi-config.yaml` also pins CARIN BB 2.0.0, which doesn't contain that parent profile; 2.1.0 is the first version that does. Validated against CARIN BB 2.1.0, the EOBs also lack `billablePeriod`, `diagnosis.type`, the `uniqueclaimid` identifier and `meta.lastUpdated`, send `item.location` as a Reference (the profile expects `locationCodeableConcept`), and EOB #1's line has no tooth `bodySite`. These were left as they are until the profile is settled. I1–I4 validate with no errors.

## Verification

**2026-11-05 R4 and profile validation.** The I1–I5 bundles were validated against FHIR R4 with US Core 6.1.0, the OHIA ODE profiles, ARex 0.2.0, Subscriptions Backport 1.1.0 and CARIN BB 2.1.0. Fixes made to pass:
- `note`, which R4 doesn't define on Organization, Location, InsurancePlan, Coverage, Subscription or ExplanationOfBenefit, was moved into each resource's narrative (`text`, status `additional`). This covers the UC04 durable organizations, location and plan too.
- `ImagingStudy.series.bodySite` is now a single `Coding`.
- The referral's `bodySite` carries the `ode-tooth` extension.
- The Conditions (category `encounter-diagnosis`) declare `us-core-condition-encounter-diagnosis`.
- The periapical `DiagnosticReport` has the category LOINC LP29684-5 Radiology.
- The virtual-findings `DocumentReference` has the type LOINC 34109-9 Note and a short text attachment.

Result: every profiled resource passes except the two EOBs (see the Interaction 5 known limitation). The I1–I4 transaction bundles load with profile validation on.

The data was last re-verified programmatically on 2026-11-04 after the UC04 narrative change (tooth #9, D3310 + D2330, photos by ARex reference, no dental home: 6 resources added, the inline photo document removed and the D3310 procedure renamed D3310; the bundles now hold **30 / 33 / 40 / 45 / 48** entries, and the older 39-resource tally below predates that update). Checks:  JSON validity, cross-reference id resolution (every `reference` resolves), and date/code consistency; all five transaction bundles were assembled and validated (**30 / 33 / 40 / 45 / 48** entries — later interactions include the earlier resources, with snapshot versions of the referral `Task`, `ServiceRequest`, and pulpitis `Condition` overriding earlier versions by shared `id`). Per project discipline, codes not confidently verified are **text-only** (no `coding`): the symptom `Observation` code, the periapical-findings `Observation` components, and the `MedicationStatement` carries only the RxNorm ingredient (the OTC product was patient-reported). Standard codes used: ICD-10-CM **K04.01** and **K04.7** (the "periapical abscess without sinus" code — the source's "K04.5" is a mislabel for chronic apical periodontitis, corrected here), LOINC 72166-2 / 72170-4 / 62443-7, SNOMED 448337001 / 266919005 / 26643006 / 225365006, CDT D0220 / D3310 / D2330 / D9995, DICOM modality IO, RxNorm 5640, ADA Universal tooth #9, and NUCC taxonomy 1223G0001X. The intraoral photos are modeled as US Core-style `DocumentReference` entries of an ARex manifest (not R4 `Media`) per the settled R4 → R6 / US-Core / 360X standards decision. The I3 radiograph is a first-class `ImagingStudy` + `DiagnosticReport` (DICOM/WADO-RS pointer) generated in-office and **not** exchanged between organizations.
