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

**No DICOM radiograph exchange between providers in either use case.** The virtual/teledentistry provider has no way to generate a radiograph — the diagnostic radiograph is captured fresh, in-office, in Interaction 3 of each use case, not pulled or pushed between organizations at referral time the way UC02's was. **Patient-submitted intraoral photos are a different matter:** the patient captures 1–2 phone photos through the teledentistry app during the virtual visit (I1), and those non-radiographic images travel with the referral as a US Core `DocumentReference` (inline `image/jpeg`, `author` = Patient), correlated to the affected tooth via a linked `Observation`. This is deliberately distinguished from the DICOM/PACS radiograph layer, which still does not appear until I3.

**Organizations now have fictional identities, not bare placeholders.** Per user direction, these are slightly-fabricated organizations — not real businesses, but also not generic "(Synthetic)" labels. Barton Springs Dental Group (UC04a, Austin) and Mission Trail Family Dental (UC04b, San Antonio) are grounded in real local flavor (real neighborhoods/landmarks) without naming actual practices. This differs from UC02a's approach (Austin Oral Surgery, a real USOSM partner org) — a deliberate choice, not an oversight; naming small real independent practices without their involvement was judged different from naming a large multi-location group already an OHIA member.

## Build status

**All five UC04a interactions (I1–I5) are built** as FHIR resources — virtual teledentistry referral → in-office scheduling (I1–I2), in-office root canal with the first radiograph (I3, in-office-only, not exchanged), closed-loop outcome summary back to the teledentistry provider (I4), and two-organization claims-sharing (I5) — with a full navigable companion guide (`companion-guides/UC04a-companion-guide.md`). **All of UC04b remains narrative-only**, per established discipline.

**Verification-discipline note (ICD-10):** the source doc labels the periapical finding "K04.5 — Periapical abscess without sinus." K04.5 is actually chronic apical periodontitis; the correct code is **K04.7**, which the built I3/I5 resources use and the main UC04 doc's UC04a appendix has been corrected to reflect.
