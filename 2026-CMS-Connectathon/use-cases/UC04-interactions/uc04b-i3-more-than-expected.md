# UC04b-I3: More Than Expected

**Corresponds to:** 2026-07-23, 10:00–12:45.

## What happens

Dr. James Okafor sees Darius the next morning, already knowing about the diabetes and the elevated risk it carries. He takes both a periapical and a bitewing radiograph. What he finds confirms the virtual assessment — irreversible pulpitis, non-restorable secondary caries on tooth #3 — but he also finds more than what Darius came in for: **two additional teeth with moderate decay**, discovered only because he was actually looking. Given Darius's diabetes and the elevated periodontal risk that comes with it, Dr. Okafor extracts tooth #3 rather than attempting to save it, and places interim restorations on the two newly-found teeth, with permanent restorations planned for a follow-up visit.

## What Darius Sees (patient-facing)

📱 **Notification:** *(none fires during the visit itself)*

## Key resources exchanged in this interaction

- `Encounter` (in-office, POS 11)
- `DiagnosticReport` ×2 (LOINC 62443-7 periapical, LOINC 46386-9 bitewing) and `ImagingStudy` for each
- `Condition` updated with confirmed diagnoses, plus **new** `Condition` entries for the two newly-discovered decayed teeth — these weren't part of the original referral's problem list
- `Procedure` — D7210 (extraction, tooth #3) and D2940 ×2 (interim restorations, the two additional teeth)

## Why this matters for testing

This interaction tests something UC04a didn't need to: **scope expansion mid-encounter.** The referral was for one tooth; the actual treatment covers three. A firm's system needs to correctly add new findings and new procedures that weren't anticipated in the original referral, without losing the connection back to it — this isn't a separate, unrelated encounter, it's the same visit finding more than expected.

## What's deliberately NOT part of this interaction

Telling Dr. Torres what actually happened, including the two extra teeth — that's Interaction 4.
