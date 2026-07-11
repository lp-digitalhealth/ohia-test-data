# Reference: 360X ⟷ COW Crosswalk (summary, sourced from lp-digitalhealth/ode-360x-adapter)

**Full source of truth:** https://github.com/lp-digitalhealth/ode-360x-adapter/blob/main/spec/mapping/360x-cow-crosswalk.md

This is a working summary saved locally for quick reference while building sample data. Always check the live file for updates — this repo is under active development ("current 3-week sprint" per its `PROGRAM-PLAN.md`).

## Transaction table (Table 1)

| 360X transaction | v2 message | Task.status | Task.businessStatus |
|---|---|---|---|
| PCC-55 Referral Request | `OMG^O19` | requested | received |
| PCC-56 Status — accept | `OSU^O51` (IP) | accepted / in-progress | accepted |
| PCC-56 Status — decline | `OSU^O51` (CA) | rejected | declined |
| PCC-59 Interim Consultation Note | `OMG^O19` + doc | in-progress | interim-results |
| PCC-57 Referral Outcome | `OMG^O19` + doc | completed | outcome-final |
| PCC-58 Referral Cancellation | `OSU^O51` (CA) | cancelled | cancelled |
| PCC-60 Appointment Notification | `SIU^S12` | in-progress | appointment-booked |
| PCC-61 No-Show Notification | `SIU^S26` | in-progress | appointment-noshow |

## Key rules

- **Referral ID** is the loop key: `ORC-2` (v2 side) = `ServiceRequest.identifier` / `Task.identifier` (FHIR side), system `urn:ohia:referral-id`.
- **Insurance/coverage never travels in v2** — FHIR `Coverage` only.
- **Medications/allergies/conditions** travel as `Task.input` (referencing `Condition`, `ODEMedicationList`, `AllergyIntolerance`) on the FHIR side; on the v2 side, only summary `DG1`/`AL1` segments travel with the order itself — no full medication list in HL7 v2 form.
- **`ServiceRequest.supportingInfo`** → the `ODEMedicationList` (+ allergy). **`ServiceRequest.reasonReference`** → `Condition`.
- Directional referral profiles (medical→dental / dental→dental / dental→medical) each have their own must-support coding rule — see `spec/api/ode-openapi.yaml`.
- Out of scope (deliberately not modeled): Cancellation Request Task, `Task.performer` baton/reassignment, multiple Coordination Tasks per Request, FHIR Subscriptions for workflow polling, `Task.partOf` sub-tasks.

## Gap identified during UC01 Encounter #1 build

No discrete v2 field is documented for naming the *intended receiving clinician* on the initial PCC-55 request (only the receiving *organization*, via MSH-5/6, and later the *accepting* provider via ORC-12 on a PCC-56 accept). Worth raising with the OHIA/adapter maintainers.
