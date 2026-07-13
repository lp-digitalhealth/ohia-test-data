# UC03 Interaction-Level Materials

Clinician-readable writeups for UC03 (Pediatric Periodontitis / Type 1 Diabetes), following the same 5-interaction pattern established for UC01 and UC02. The original flat use case document (`use-cases/UC03-Pediatric-Referral.md`) is unchanged — these writeups live in a new subfolder rather than restructuring the existing file.

- `uc03-interaction-01-exam-assessment-referral.md` — well-child exam, oral health assessment, Plan-Net provider search, referral creation (2026-02-28 – ~03-05)
- `uc03-interaction-02-pre-encounter-records-connie.md` — **the use case's own named primary test objective** — medical records delivered via Connie (state HIE) a full week before the appointment (2026-05-21), not concurrent with the referral send the way UC01/UC02's imaging was
- `uc03-interaction-03-dental-encounter.md` — comprehensive evaluation, PRA, confirmed periodontitis diagnosis, treatment (2026-05-28). **Open modeling question flagged, not resolved:** whether the two-quadrant scaling and root planing (D4341) should be one `Procedure` resource or two
- `uc03-interaction-04-bidirectional-summary-return.md` — two simultaneous summaries, to the pediatrician and the endocrinologist, via Connie (2026-05-28). **Precision note:** two distinct `Flag` resources are needed, pointed in opposite directions (diabetes→periodontal risk vs. periodontal→glycemic risk) — not the same Flag reused
- `uc03-interaction-05-claims-sharing.md` — third proof point for the claims-sharing profile, this time through a CHIP/MCO-to-plan-administrator chain. **Two coverage questions carried forward from the source doc, not resolved here:** whether D4341 needs PA, and whether D4381 is covered at all under Husky B pediatric benefit

## Not yet built

FHIR resources for any of these 5 interactions — narrative-only, per established discipline.

## Note on scope: no DICOM/imaging framework needed here, unlike UC01/UC02

This use case exchanges structured clinical data (conditions, medications, devices, observations) via CDex/Connie — not radiographs. The DICOM/`ImagingStudy`/WADO-RS standing instruction in `CLAUDE.md` doesn't apply to UC03's resource exchanges; worth noting explicitly so its absence here isn't mistaken for an oversight.
