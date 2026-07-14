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

## UC02 companion guides

- `UC02a-companion-guide.md` — Texas Medicaid surgical extraction **with** prior authorization. Covers all five interactions (I1 PA wait → I5 claims-sharing), organized by stakeholder in a single file with a full Resource Index.
- `UC02b-companion-guide.md` — commercial dental PPO surgical extraction with immediate-implant option, **no** prior authorization. Covers **all five interactions** (I1 coverage/path → I5 two-procedure claims-sharing). Emphasizes the UC02b-specific points: a CRD service returning a negative/no-PA result, benefit-detail verification (waiting period / annual maximum), the referral originating in I1, the dental-to-dental support-a-pull imaging direction, the project's first `Device` resource (the immediate implant, I3) carried through to the restorative provider (I4), and a two-line-item claims-sharing package in the commercial-payer direction (I5).
