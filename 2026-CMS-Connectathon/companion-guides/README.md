# Companion Guides

One companion guide per use case, each covering all relevant roles in a single file (rather than separate guides per role), so a firm playing multiple roles — or wanting the full picture — has one document to read.

Each guide states what a system needs to be *capable of* and what data it will *send/receive*, without being prescriptive about internal implementation.

## UC01 companion guide — sections
- EHR (FCCC / oncology side)
- PMS (Penn Dental / dental side)
- Payer (Independence Blue Cross)
- Patient-facing app

Not yet built.

## UC01 readiness checklist — separate document

`UC01-readiness-checklist.md` — built, organized **encounter by encounter** rather than role by role, since responsibilities shift depending on where in the workflow you are. Encounter #1 is fully broken out into two distinct pathways (Request for Treatment / CRD+DTR, and Referral / 360X+bridge), correcting an earlier draft that incorrectly implied the EHR needed FHIR capability for the 360X referral pathway — it only needs HL7v2/C-CDA there; FHIR is entirely the bridge's and PMS's concern for that pathway. Encounters #2–7 not yet built.
