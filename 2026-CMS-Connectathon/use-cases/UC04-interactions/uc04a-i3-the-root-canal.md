# UC04a-I3: The Root Canal

**Corresponds to:** 2026-07-15, 10:00–12:15.

## What happens

Sarah sees Dr. Priya Nair the next morning. Dr. Nair already has Dr. Webb's findings — she's not starting from scratch. She takes a periapical radiograph, which confirms what the virtual assessment suspected: irreversible pulpitis, and now with visible early periapical pathology. This is where the actual imaging in this use case first appears — captured in-office, not exchanged beforehand, since Dr. Webb had no way to generate it virtually. Dr. Nair completes root canal therapy on tooth #19 in a single visit.

## What Sarah Sees (patient-facing)

📱 **Notification:** *(none fires during the visit itself)*

## Key resources exchanged in this interaction

- `Encounter` (in-office, POS 11)
- `DiagnosticReport` (LOINC 62443-7, the periapical radiograph report) and `ImagingStudy` (the image itself referenced from it — DICOM/WADO-RS underlies this the same way it does in UC02, even though it wasn't relevant to Interaction 1 here)
- `Condition` updated — K04.01 confirmed, K04.5 (periapical pathology) newly added
- `Observation` — the periapical findings
- `Procedure` — D3330, tooth #19 (FDI notation 36 per the source doc's own appendix — worth flagging: this use case uses FDI notation for the procedure record, which contradicts the ADA's direct confirmation from earlier in this project that FDI isn't used for US dental data. This is a real inconsistency in the source document worth correcting, not silently following.)

## Why this matters for testing

This is where imaging genuinely enters the picture for the first time in this use case — and it's worth being precise that it arrives differently than in UC02: not pulled from another provider's system, but generated fresh, in-office, informed by (but not replacing) the virtual assessment that preceded it.

## What's deliberately NOT part of this interaction

Telling Dr. Webb what happened — that's Interaction 4.
