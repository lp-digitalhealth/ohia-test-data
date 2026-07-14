# UC02 Interaction-Level Materials

Clinician-readable writeups for both UC02 sub-use-cases, following the same pattern established in UC01: 5 key test interactions per use case, not a 1:1 map to every clinical step. See `CLAUDE.md` for the reasoning behind the encounter-vs-interaction split.

## UC02a — Texas Medicaid, Prior Authorization

- **UC02a-I1: The Prior Authorization Wait** (`uc02a-i1-prior-authorization-wait.md`) — CRD → DTR → PAS, the first-of-kind PA-in-a-dental-benefit-context test
- **UC02a-I2: The Handoff to Oral Surgery** (`uc02a-i2-handoff-to-oral-surgery.md`) — referral + `Appointment`/`AppointmentResponse`
- **UC02a-I3: The Extraction** (`uc02a-i3-the-extraction.md`) — the extraction itself
- **UC02a-I4: Closing the Loop** (`uc02a-i4-closing-the-loop.md`) — closed-loop summary back to Dr. Parker
- **UC02a-I5: Billing the Extraction** (`uc02a-i5-billing-the-extraction.md`) — **key driver, not deferred** — proves the `ODEOralProfessionalEOB` claims-sharing profile against a dental Medicaid payer

## UC02b — Commercial, Immediate Implant

- **UC02b-I1: Checking Coverage, Choosing a Path** (`uc02b-i1-checking-coverage-choosing-path.md`) — real-time benefit check (not PA), CRD returns negative/no-PA-needed
- **UC02b-I2: The Handoff to Oral Surgery** (`uc02b-i2-handoff-to-oral-surgery.md`) — same pattern as UC02a-I2
- **UC02b-I3: Extraction and Implant, Same Day** (`uc02b-i3-extraction-implant-same-day.md`) — first use of the `Device` resource anywhere in this project
- **UC02b-I4: Closing the Loop, Implant Included** (`uc02b-i4-closing-the-loop-implant.md`) — `Device` record travels with the summary, for future restorative continuity
- **UC02b-I5: Billing for Two Procedures** (`uc02b-i5-billing-two-procedures.md`) — second proof point for claims-sharing (commercial payer direction). **Open scope question, not yet resolved:** whether this should also anticipate the future crown claim referencing the `Device` record — see the file itself for detail.

## Build status

- **UC02a:** all five interactions built as FHIR resources (`fhir-resources/uc02a-surgical-extraction/`), plus a companion guide (`companion-guides/UC02a-companion-guide.md`).
- **UC02b:** all five interactions built as FHIR resources (`fhir-resources/uc02b-commercial-implant/`), plus a companion guide covering all five (`companion-guides/UC02b-companion-guide.md`). I3 introduces the project's first `Device` resource (the immediate implant); I5 is the commercial-payer direction of the claims-sharing profile with a two-line-item `ExplanationOfBenefit`.
