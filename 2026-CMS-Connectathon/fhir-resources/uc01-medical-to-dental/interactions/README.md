# UC01 Per-Interaction FHIR Resources

**Terminology note:** UC01's clinical narrative describes 7 patient *encounters* (still documented in `use-cases/UC01-medical-to-dental-tongue-cancer/`, appendix Section 0 — that enumeration is unchanged and remains the clinical reference). For **test data purposes**, the project is organized around 4 key *interactions* instead — the specific integration points worth testing, since most of the clinical narrative (e.g., the tooth extractions) is "business as usual" and doesn't need its own modeled resources. An interaction may correspond to one clinical encounter, or bridge/skip across several. See `CLAUDE.md` for the full reasoning behind this reframing.

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

Corresponds to the clinical Encounter #2 (2026-07-23, dental exam & radiographs). Requires Interaction 1's referral to already be open (this bundle includes it as a prerequisite — 38 resources total, 34 from Interaction 1 + 4 new).

- `encounter-02-dental-exam.json` — Encounter (the dental exam visit, `basedOn` the referral ServiceRequest from Interaction 1)
- `diagnosticreport-periapical.json` — DiagnosticReport (CDT D0220 / LOINC 62443-7, verified: "Single view Teeth Document XR")
- `diagnosticreport-panoramic.json` — DiagnosticReport (CDT D0330 / LOINC 24828-6)
- `observation-tooth30-radiation-dose.json` — Observation, the LOINC-gap resource (52 Gy at tooth #30) — carries the note documenting the DDC info request/response, per the locked-in design decision (modeled as a note, not a formal resource — see `CLAUDE.md` Section 3 for the full COW-pattern justification)
- `interaction-02-bundle.json` — self-contained bundle: registry + base + Interaction 1 + Interaction 2 (38 resources)

**Note on the info request:** the request itself is not a standalone resource. It's captured as `.note` text on both the `Encounter` and the `Observation` — confirmed as a legitimate implementation of the base COW IG's "Requesting additional information" pattern (one of three documented options: RESTful query / letter / instruction — a note maps to "letter").

## Interaction 3 — Communication of Final Treatment Plan + Extension Request

Not yet designed in detail. Corresponds to content already earmarked in the use case's "Key FHIR Resources Exercised" table under `Communication`/`CommunicationRequest` (the IMRT delay/extension request between providers).

## Interaction 4 — Packaging Treatment for Submission to Medical Payer

Not yet designed in detail. The PA `Claim`/`ClaimResponse` submission, using the DTR-collected documentation package from Interaction 1's CRD/DTR pathway.
