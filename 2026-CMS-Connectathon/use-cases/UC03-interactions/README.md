# UC03 Interaction-Level Materials

Clinician-readable writeups for UC03 (Pediatric Periodontitis / Type 1 Diabetes), following the same 5-interaction pattern established for UC01 and UC02. The original flat use case document (`use-cases/UC03-Pediatric-Referral.md`) is unchanged — these writeups live in a new subfolder rather than restructuring the existing file.

- **UC03-I1: A Routine Checkup Finds Something Else** (`uc03-i1-checkup-finds-something-else.md`) — well-child exam, oral health assessment, Plan-Net provider search, referral creation (2026-02-28 – ~03-05)
- **UC03-I2: Records Before the Visit** (`uc03-i2-records-before-visit.md`) — **the use case's own named primary test objective** — medical records delivered via Connie (state HIE) a full week before the appointment (2026-05-21), not concurrent with the referral send the way UC01/UC02's imaging was
- **UC03-I3: Three Months Later** (`uc03-i3-three-months-later.md`) — comprehensive evaluation, PRA, confirmed periodontitis diagnosis, treatment (2026-05-28). **Open modeling question flagged, not resolved:** whether the two-quadrant scaling and root planing (D4341) should be one `Procedure` resource or two
- **UC03-I4: Telling Both Doctors** (`uc03-i4-telling-both-doctors.md`) — two simultaneous summaries, to the pediatrician and the endocrinologist, via Connie (2026-05-28). **Precision note:** two distinct `Flag` resources are needed, pointed in opposite directions (diabetes→periodontal risk vs. periodontal→glycemic risk) — not the same Flag reused
- **UC03-I5: Billing Timothy's Visit** (`uc03-i5-billing-timothys-visit.md`) — third proof point for the claims-sharing profile, this time through a CHIP/MCO-to-plan-administrator chain. **Two coverage questions carried forward from the source doc, not resolved here:** whether D4341 needs PA, and whether D4381 is covered at all under Husky B pediatric benefit

## Not yet built

FHIR resources for any of these 5 interactions — narrative-only, per established discipline.

## Note on scope: no DICOM/imaging framework needed here, unlike UC01/UC02

This use case exchanges structured clinical data (conditions, medications, devices, observations) via CDex/Connie — not radiographs. The DICOM/`ImagingStudy`/WADO-RS standing instruction in `CLAUDE.md` doesn't apply to UC03's resource exchanges; worth noting explicitly so its absence here isn't mistaken for an oversight.
