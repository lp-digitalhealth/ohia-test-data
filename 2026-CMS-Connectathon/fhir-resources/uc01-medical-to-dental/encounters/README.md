# UC01 Per-Encounter FHIR Resources

Transactional resources specific to each of UC01's 7 encounters (as opposed to base/registry resources, which live in ../base/ and ../../common/).

## Encounter #1 — IMRT Order & Referral (built, conforms to ODE 360X-adapter spec)

Rebuilt to conform to `spec/api/ode-openapi.yaml`, `spec/mapping/360x-cow-crosswalk.md`, and `ARCHITECTURE.md` (all from `lp-digitalhealth/ode-360x-adapter`).

- `encounter-01-imrt-order.json` — Encounter
- `condition-john-smith-tongue-cancer.json` — Condition (cancer diagnosis, C02.1)
- `allergyintolerance-john-smith-penicillin.json` — AllergyIntolerance (penicillin, RxNorm 7980)
- `medrequest-john-smith-lisinopril.json`, `medrequest-john-smith-atorvastatin.json`, `medrequest-john-smith-oxycodone-apap.json` — MedicationRequest x3
- `list-john-smith-medications.json` — ODEMedicationList (List profile)
- `servicerequest-imrt-order.json` — ServiceRequest (IMRT order, triggers CRD at `order-sign` — corrected from an earlier `order-select` error)
- `servicerequest-dental-referral.json` — ServiceRequest, `ODEMedicalToDentalReferral` profile: `urn:ohia:referral-id`, ICD-10-CM `reasonCode` + `reasonReference` to Condition, CPT `code`, `supportingInfo` pointing to the medication List + AllergyIntolerance
- `task-360x-dental-referral.json` — Task, `ODEReferralTask` profile: task-code `fulfill`, `businessStatus` = `received` (corrected from an earlier incorrect `sent`), `urn:ohia:referral-id` identifier, `Task.input` referencing Condition/List/AllergyIntolerance
- `provenance-dental-referral.json` — **Provenance**, added after `ARCHITECTURE.md` review revealed `referral_fhir.py`'s actual bundle output includes it (a gap the crosswalk document alone didn't surface); US Core Provenance profile, `author`/`transmitter` agent types
- `cds-hooks-discovery-ibx.json` — CDS Hooks discovery config (NOT a FHIR resource) — hook corrected to `order-sign`
- `encounter-01-bundle.json` — self-contained transaction bundle: registry + base + Encounter #1 resources (34 total)

**Note on imaging:** per the ODE spec, medical→dental referrals use the "separate push" pattern (`DocumentReference/$submit-attachment`) rather than support-a-pull. Not yet built — imaging doesn't occur until Encounter #2 (dental exam, radiographs).

**Note on the EHR/FHIR boundary:** per `ARCHITECTURE.md`, FCCC's EHR is expected to be HL7v2/C-CDA native for the 360X referral pathway — the FHIR resources above (`ServiceRequest`, `Task`, etc.) represent what the `ode-360x-adapter` bridge *produces* from FCCC's HL7v2 message, not something FCCC's system generates directly. See `hl7v2/uc01-medical-to-dental/encounter-01/` for the actual wire-level message.

## Encounters #2–7
Not yet built.
