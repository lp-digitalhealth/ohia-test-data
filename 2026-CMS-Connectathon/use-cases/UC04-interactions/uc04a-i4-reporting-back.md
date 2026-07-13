# UC04a-I4: Reporting Back

**Corresponds to:** 2026-07-15, 12:35–12:36.

## What happens

Twenty minutes after finishing, Dr. Nair's system sends a structured summary back to Dr. Webb — confirmed diagnoses, what was done, CDT codes, a post-treatment care plan. Dr. Webb reviews it and closes the loop. Unlike UC03, there's only one recipient here — Dr. Webb, the originating provider — not a fan-out to multiple parties.

## What Sarah Sees (patient-facing)

📱 **Notification:** *"Referral complete — treatment summary and recovery guidance available."*

## Key resources exchanged in this interaction

- `ClinicalImpression` (the encounter summary), `Procedure` (marked completed), `CarePlan` (post-treatment instructions) — pushed from the in-office practice to Dr. Webb's FHIR endpoint via CDex
- `ServiceRequest.status` updated to `completed`
- `Task` closed
- `Provenance`/`AuditEvent` for the routed transmission

## Why this matters for testing

This is the direct analog of UC01's Interaction 3 and UC02's Interaction 4 — the same closed-loop pattern, now proven a third time, in a virtual-to-in-office direction rather than dental-to-dental or medical-to-dental. The single-recipient shape here is worth noting as the baseline case, in contrast to UC03's two-recipient version.

## What's deliberately NOT part of this interaction

Getting either practice paid — that's Interaction 5.
