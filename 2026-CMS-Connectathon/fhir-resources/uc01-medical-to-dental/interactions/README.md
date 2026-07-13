# UC01 Per-Interaction FHIR Resources

**Gap fixed this session:** a `Subscription` resource (`fhir-resources/uc01-medical-to-dental/base/subscriptions/subscription-john-smith-referral-status.json`) was missing entirely, despite the use case doc's own master resource table explicitly naming `Subscription`/`SubscriptionStatus` as the mechanism for patient-app milestone notifications. Built retroactively, placed in `base/` (not any specific interaction) since it's ongoing infrastructure spanning the whole use case. All three bundle counts increased by 1 as a result (35/39/47).

**Terminology note:** UC01's clinical narrative describes 7 patient *encounters* (still documented in `use-cases/UC01-medical-to-dental-tongue-cancer/`, appendix Section 0 — that enumeration is unchanged and remains the clinical reference). For **test data purposes**, the project is organized around key *interactions* instead — the specific integration points worth testing, since most of the clinical narrative (e.g., the tooth extractions) is "business as usual" and doesn't need its own modeled resources. An interaction may correspond to one clinical encounter, or bridge/skip across several. See `CLAUDE.md` for the full reasoning behind this reframing.

Transactional resources specific to each interaction (as opposed to base/registry resources, which live in `../base/` and `../../common/`).

## Interaction 1 — Request for Radiation + Dental Clearance Referral (built, conforms to ODE 360X-adapter spec)

Corresponds to the clinical Encounter #1 (2026-07-06). Conforms to `spec/api/ode-openapi.yaml`, `spec/mapping/360x-cow-crosswalk.md`, and `ARCHITECTURE.md` (all from `lp-digitalhealth/ode-360x-adapter`).

- `encounter-01-imrt-order.json` — Encounter *(filename/resource `id` intentionally kept as "encounter-01" — this is a legitimate FHIR `Encounter` resource representing the clinical visit; renaming it would mean touching every cross-reference throughout the bundle for no correctness benefit)*
- `condition-john-smith-tongue-cancer.json` — Condition (cancer diagnosis, C02.1)
- `allergyintolerance-john-smith-penicillin.json` — AllergyIntolerance (penicillin, RxNorm 7980)
- `medrequest-john-smith-lisinopril.json`, `medrequest-john-smith-atorvastatin.json`, `medrequest-john-smith-oxycodone-apap.json` — MedicationRequest x3
- `list-john-smith-medications.json` — ODEMedicationList (List profile)
- `servicerequest-imrt-order.json` — ServiceRequest (IMRT order, triggers CRD at `order-sign`)
- `servicerequest-dental-referral.json` — ServiceRequest, `ODEMedicalToDentalReferral` profile: `urn:ohia:referral-id`, ICD-10-CM `reasonCode` + `reasonReference` to Condition, CPT `code`, `supportingInfo` pointing to the medication List + AllergyIntolerance
- `task-360x-dental-referral.json` — Task, `ODEReferralTask` profile: task-code `fulfill`, `businessStatus` = `received`, `urn:ohia:referral-id` identifier, `Task.input` referencing Condition/List/AllergyIntolerance
- `provenance-dental-referral.json` — Provenance (US Core profile, `author`/`transmitter` agent types)
- `cds-hooks-discovery-ibx.json` — CDS Hooks discovery config (NOT a FHIR resource) — hook is `order-sign`
- `interaction-01-bundle.json` — self-contained transaction bundle: registry + base + Interaction 1 resources (34 total)

**Note on the EHR/FHIR boundary:** per `ARCHITECTURE.md`, FCCC's EHR is expected to be HL7v2/C-CDA native for the 360X referral pathway — the FHIR resources above (`ServiceRequest`, `Task`, etc.) represent what the `ode-360x-adapter` bridge *produces* from FCCC's HL7v2 message, not something FCCC's system generates directly. See `hl7v2/uc01-medical-to-dental/interaction-01/` for the actual wire-level message.

## Interaction 2 — Request for Additional Information (dental exam findings + DDC dose inquiry) — built

Corresponds to the clinical Encounter #2 (2026-07-23, dental exam & radiographs). Requires Interaction 1's referral to already be open (this bundle includes it as a prerequisite — 40 resources total).

- `encounter-02-dental-exam.json` — Encounter (the dental exam visit, `basedOn` the referral ServiceRequest from Interaction 1)
- `diagnosticreport-periapical.json` — DiagnosticReport (CDT D0220 / LOINC 62443-7, verified: "Single view Teeth Document XR")
- `diagnosticreport-panoramic.json` — DiagnosticReport (CDT D0330 / LOINC 24828-6)
- `observation-tooth30-radiation-dose.json` — Observation, the LOINC-gap resource (52 Gy at tooth #30) — carries the note documenting the DDC info request/response
- `task-360x-dental-referral-interim.json` — **Task update, same `id` as Interaction 1's Task — fills a previously-flagged gap.** `status: in-progress`, `businessStatus: in-progress`, `owner` set for the first time (Dr. Bellweather's PractitionerRole, correctly populated at acceptance rather than intake), `output` referencing the exam Encounter and both DiagnosticReports. Its note explicitly clarifies this corresponds to **no 360X wire-level transaction** — Interaction 2 is pure FHIR-side Task/note activity by design, not an unbuilt PCC-59.
- `interaction-02-bundle.json` — self-contained bundle: registry + base + Interaction 1 + Interaction 2 (40 resources)
- `interaction-02-delta-bundle.json` — lightweight alternative: just Interaction 2's own 5 new/updated resources, for firms that already have Interaction 1 loaded and want only the delta

**Note on the info request:** the request itself is not a standalone resource. It's captured as `.note` text on the `Observation` — confirmed as a legitimate implementation of the base COW IG's "Requesting additional information" pattern (one of three documented options: RESTful query / letter / instruction — a note maps to "letter").

## Interaction 3 — The Clearance — built (FHIR resources), rigorous QA performed

Corresponds to the clinical Encounter #6 (2026-07-31). Wire-level: IHE 360X PCC-57 (Referral Outcome), `OMG^O19` + C-CDA Consultation Note.

- `procedure-extraction-tooth4.json`, `procedure-extraction-tooth17.json`, `procedure-extraction-implant-tooth30.json` — 3x Procedure, CDT-coded (D7210/D6010, confirmed real)
- `observation-dental-clearance-disposition.json` — coded disposition Observation, **text-only** (see terminology caution below)
- `clinicalimpression-dental-clearance.json` — the clearance attestation, **text-only** assessment code
- `documentreference-dental-clearance-note.json` — C-CDA Consultation Note wrapper, LOINC 11488-4 (verified)
- `servicerequest-dental-referral-completed.json` — snapshot of the referral ServiceRequest (same `id` as Interaction 1's), `status: completed`
- `task-360x-dental-referral-completed.json` — snapshot of the referral Task (same `id` as Interaction 1's), final version: `status: completed`, `businessStatus: outcome-final`, `owner` set, `output` populated
- `interaction-03-bundle.json` — self-contained bundle: registry + base + all three interactions (46 resources), correct temporal order

**Terminology caution:** the use case doc's own "SNOMED CT Clinical Codes" table was found during QA to contain at least one confirmed-invalid code and several more unconfirmed via general web search. All codes originally planned for this interaction are text-only in the actual built resources — see the use case doc Section 6 and the companion guide for full detail.

**Versioning note:** `servicerequest-dental-referral-completed.json` and `task-360x-dental-referral-completed.json` share the same resource `id` as their Interaction 1 counterparts but represent later versions (status/businessStatus progressed). Both files exist as separate snapshots — the Interaction 1 originals were NOT overwritten in place, so the intake-state can still be inspected. A cumulative bundle loads both in temporal order via sequential `PUT`s, which is correct FHIR versioning semantics (later PUT wins).

## Interaction 4 — Ending the Prior Authorization — built

Corresponds to the PA submission/approval cycle (2026-08-01 – 2026-08-03), not tied to a single clinical encounter. Uses Da Vinci PAS (`Claim`/`ClaimResponse`, replacing X12 278 entirely) and Da Vinci PDex PPA profile for patient-facing delivery.

- `claim-imrt-priorauth.json` — `Claim`, `use: preauthorization`, PAS profile. **For the IMRT/radiation service** (same CPT planning codes 77301/77338 as the original Interaction 1 order) — NOT for Dr. Bellweather's dental procedures. `supportingInfo` references the dental clearance (`ClinicalImpression`) and the DTR `Questionnaire` as evidence the prerequisite is satisfied.
- `claimresponse-imrt-priorauth.json` — `ClaimResponse`, PAS profile. `outcome: complete`, `disposition: Approved`, `preAuthRef`/`preAuthPeriod` populated. No `item`/adjudication — the base fields alone convey the non-financial PA decision; avoided asserting an unverified adjudication category code.
- `eob-imrt-priorauth-ppa.json` — `ExplanationOfBenefit`, **verified** PDex PPA profile (`http://hl7.org/fhir/us/davinci-pdex/StructureDefinition/pdex-priorauthorization`). Patient-facing view of the PA decision, delivered via CARIN Blue Button as the access framework. No financial amounts.
- `interaction-04-bundle.json` — self-contained bundle: registry + base + all four interactions (50 resources)

**Explicitly out of scope for this interaction** (per the use case doc itself): the actual reimbursement billing claims (837P for FCCC's IMRT delivery, 837P for Bellweather's medically-billed dental procedures, 835 remittance) — mentioned only as real-world EDI-equivalence context, not modeled as FHIR resources here. That's where the project's separately-designed claims-sharing profile (`ODEOralProfessionalEOB`) would eventually be used — a future interaction, not this one.
