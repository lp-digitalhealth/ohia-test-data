# UC04b-I4: Closing the Loop, Then Checking In

**Corresponds to:** 2026-07-23, 13:15–13:16 (summary and closure), plus 2026-07-24, 09:00 (Dr. Torres's follow-up — the next day, not the same event).

## What happens

Half an hour after finishing, Dr. Okafor's system sends the full summary back to Dr. Torres — the extraction, the two additional restorations, and a care plan explicitly connecting the dots: Darius needs a complete periodontal evaluation and regular preventive care, and his diabetes is part of why that matters. Dr. Torres closes the referral.

The next morning, she follows up with Darius directly through the app — not a new clinical encounter, just a message reinforcing why regular dental care matters given his diabetes, and pointing him toward how to actually use his Medicaid dental benefit going forward, since he clearly hadn't been before.

## What Darius Sees (patient-facing)

📱 **Notification (07-23):** *"Referral complete — care plan available."*
📱 **Message (07-24, from Dr. Torres):** *A personal follow-up on his diabetes and dental care, and guidance on using his Medicaid dental benefit for preventive visits.*

## Key resources exchanged in this interaction

- `ClinicalImpression`, `Procedure` (completed), `CarePlan` (periodontal evaluation + preventive care frequency, explicitly tied to the diabetes context) — pushed to Dr. Torres's FHIR endpoint
- `ServiceRequest.status` → `completed`, `Task` closed
- The next-day follow-up itself is a `Communication`, not a new clinical resource — it's Dr. Torres acting on what she already received, a full day later, not a new encounter

## Why this matters for testing

Same closed-loop pattern as UC04a, but with a genuine addition: a same-provider, next-day follow-up that isn't itself a referral event or a new encounter, just a `Communication` referencing the already-closed referral. The test is whether a system correctly represents this as *not* reopening anything — Darius's care plan and referral are already complete; this is relationship continuity, not a new clinical thread.

## What's deliberately NOT part of this interaction

Billing — that's Interaction 5, and it happens the same morning as the follow-up, just earlier.
