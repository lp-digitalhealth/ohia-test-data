# UC04 Interaction-Level Materials

Clinician-readable writeups for both UC04 sub-use-cases (teledentistry, virtual-to-in-office referral), 5 interactions each, same pattern as UC01–UC03.

## UC04a — Commercial (Sarah Okonkwo / Dr. Webb / Dr. Nair)

- **UC04a-I1: Tuesday Night Pain** (`uc04a-i1-tuesday-night-pain.md`)
- **UC04a-I2: An Appointment by Morning** (`uc04a-i2-appointment-by-morning.md`)
- **UC04a-I3: The Root Canal** (`uc04a-i3-the-root-canal.md`) — **real finding, flagged, not silently propagated:** the source doc's own appendix labels tooth #19 as "FDI 36," contradicting the ADA's direct confirmation (earlier in this project) that FDI notation isn't used for US dental data. Same error pattern already found once in a different dataset's precedent file.
- **UC04a-I4: Reporting Back** (`uc04a-i4-reporting-back.md`)
- **UC04a-I5: Two Bills, One Visit** (`uc04a-i5-two-bills-one-visit.md`) — **two separate claims-ready packages, one per submitting organization** (teledentistry provider, in-office practice), not one combined package

## UC04b — Medicaid (Darius Reyes / Dr. Torres / Dr. Okafor)

- **UC04b-I1: Midnight Pain, A Diabetes Flag** (`uc04b-i1-midnight-pain-diabetes-flag.md`)
- **UC04b-I2: An Appointment Within 48 Hours** (`uc04b-i2-appointment-within-48-hours.md`)
- **UC04b-I3: More Than Expected** (`uc04b-i3-more-than-expected.md`) — scope expansion mid-encounter: two additional decayed teeth found beyond the referred one
- **UC04b-I4: Closing the Loop, Then Checking In** (`uc04b-i4-closing-loop-checking-in.md`) — includes a genuinely new pattern: a next-day, same-provider follow-up `Communication` that is explicitly NOT a new clinical encounter or a reopened referral
- **UC04b-I5: Billing Three Teeth** (`uc04b-i5-billing-three-teeth.md`) — same two-organization pattern as UC04a, with a more complex in-office claim (5 service lines, 3 teeth)

## Two structural notes, carried over from UC03's approach

**No DICOM/imaging exchange between providers in either use case.** The virtual/teledentistry provider has no way to generate a radiograph — imaging is captured fresh, in-office, in Interaction 3 of each use case, not pulled or pushed between organizations at referral time the way UC02's was.

**Organizations now have fictional identities, not bare placeholders.** Per user direction, these are slightly-fabricated organizations — not real businesses, but also not generic "(Synthetic)" labels. Barton Springs Dental Group (UC04a, Austin) and Mission Trail Family Dental (UC04b, San Antonio) are grounded in real local flavor (real neighborhoods/landmarks) without naming actual practices. This differs from UC02a's approach (Austin Oral Surgery, a real USOSM partner org) — a deliberate choice, not an oversight; naming small real independent practices without their involvement was judged different from naming a large multi-location group already an OHIA member.

## Not yet built

FHIR resources for any of these 10 interactions — narrative-only, per established discipline.
