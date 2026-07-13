# UC02 Interaction-Level Materials

Clinician-readable writeups for both UC02 sub-use-cases, following the same pattern established in UC01: 5 key test interactions per use case, not a 1:1 map to every clinical step. See `CLAUDE.md` for the reasoning behind the encounter-vs-interaction split.

## UC02a — Texas Medicaid, Prior Authorization

- `uc02a-interaction-01-prior-authorization-cycle.md` — CRD → DTR → PAS, the first-of-kind PA-in-a-dental-benefit-context test
- `uc02a-interaction-02-referral-send-receipt-scheduling.md` — referral + `Appointment`/`AppointmentResponse`
- `uc02a-interaction-03-surgical-consultation-extraction.md` — the extraction itself
- `uc02a-interaction-04-post-op-summary-referral-closure.md` — closed-loop summary back to Dr. Parker
- `uc02a-interaction-05-claims-sharing.md` — **key driver, not deferred** — proves the `ODEOralProfessionalEOB` claims-sharing profile against a dental Medicaid payer

## UC02b — Commercial, Immediate Implant

- `uc02b-interaction-01-benefit-verification-referral-send.md` — real-time benefit check (not PA), CRD returns negative/no-PA-needed
- `uc02b-interaction-02-referral-receipt-scheduling.md` — same pattern as UC02a's Interaction 2
- `uc02b-interaction-03-consultation-extraction-implant.md` — first use of the `Device` resource anywhere in this project
- `uc02b-interaction-04-post-op-summary-device-referral-closure.md` — `Device` record travels with the summary, for future restorative continuity
- `uc02b-interaction-05-claims-sharing.md` — second proof point for claims-sharing (commercial payer direction). **Open scope question, not yet resolved:** whether this should also anticipate the future crown claim referencing the `Device` record — see the file itself for detail.

## Not yet built

FHIR resources for any of these 10 interactions — this session was narrative-only, per the established discipline of confirming the story before building.
