# UC03 Interaction-Level Materials

Clinician-readable writeups for UC03 (Pediatric Periodontitis / Type 1 Diabetes), following the same 5-interaction pattern established for UC01 and UC02. These writeups live in this `interactions/` subfolder alongside the main use case document ([`../UC03-Pediatric-Referral.md`](../UC03-Pediatric-Referral.md)), matching the nested `use-cases/UC0X-.../` structure UC01 and UC02 use; both share the same corrected Connecticut ecosystem model (Connie hub, BeneCare ASO, Gainwell fiscal agent, CTDHP dental plan, DSS sponsor — no MCO).

- **UC03-I1: A Routine Checkup Finds Something Else** (`uc03-i1-checkup-finds-something-else.md`) — well-child exam, oral health assessment, Plan-Net provider search, referral creation (2026-02-28 – ~03-05)
- **UC03-I2: Records Before the Visit** (`uc03-i2-records-before-visit.md`) — **the use case's own named primary test objective** — medical records delivered via Connie (state HIE) a full week before the appointment (2026-05-21), not concurrent with the referral send the way UC01/UC02's imaging was
- **UC03-I3: Three Months Later** (`uc03-i3-three-months-later.md`) — comprehensive evaluation, PRA, confirmed **aggressive periodontitis (K05.211)** diagnosis, treatment (2026-05-28). **Resolved:** the two-quadrant scaling and root planing (D4341) is modeled as **two `Procedure` resources** (one per quadrant → two EOB lines), and D4341 **requires prior authorization**, so the full CRD → DTR → PAS cycle fires at this treatment visit
- **UC03-I4: Telling Both Doctors** (`uc03-i4-telling-both-doctors.md`) — two simultaneous summaries, to the pediatrician and the endocrinologist, via Connie (2026-05-28). **Precision note:** two distinct `Flag` resources are needed, pointed in opposite directions (diabetes→periodontal risk vs. periodontal→glycemic risk) — not the same Flag reused
- **UC03-I5: Billing Timothy's Visit** (`uc03-i5-billing-timothys-visit.md`) — third proof point for the claims-sharing profile, this time on a CHIP fiscal-agent model (DSS → Gainwell adjudicates/pays; CTDHP dental plan facilitated by BeneCare as ASO; no MCO). **Coverage status:** D4341 **requires PA** (resolved — built at I3); **D4381 (chlorhexidine) coverage remains a genuinely open question**, carried honestly on the EOB as coverage-uncertain rather than asserted covered

## Build status

**All five interactions are built as FHIR resources** — see [`../../../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/README.md`](../../../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/README.md) for the per-interaction resource lists and the [`UC03 companion guide`](../../../companion-guides/UC03-companion-guide.md) for load order and stakeholder guidance.

## Note on scope: no DICOM/imaging framework needed here, unlike UC01/UC02

This use case exchanges structured clinical data (conditions, medications, devices, observations) via CDex/Connie — not radiographs. The DICOM/`ImagingStudy`/WADO-RS standing instruction in `CLAUDE.md` doesn't apply to UC03's resource exchanges; worth noting explicitly so its absence here isn't mistaken for an oversight.
