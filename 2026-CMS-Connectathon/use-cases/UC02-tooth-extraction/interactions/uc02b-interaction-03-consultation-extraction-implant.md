# UC02b — Interaction 3: Surgical Consultation, Extraction & Immediate Implant Placement

**Corresponds to:** 2026-07-15, 09:00.

## What happens

Frank arrives at Austin Oral Surgery. Dr. Maxil reviews the referral, confirms the diagnosis, reviews medications, and walks Frank through both options in detail — extraction alone with a future implant appointment after healing, or extraction with the implant placed today. They discuss cost, the possibility of needing bone grafting, and what to expect either way. Frank decides: do it in one visit.

Dr. Maxil extracts tooth #30, then immediately places an endosteal implant into the socket — same appointment, same procedure. He documents the extraction, then documents the implant separately: the specific device placed (manufacturer, size, lot number), the placement torque achieved, and that a healing abutment was placed. Frank is instructed on implant care and told to expect three to four months before the site is ready for a crown.

## What Frank Sees (patient-facing)

📱 **Notification:** *(none new during the visit itself — the next notification comes once the summary is sent, in Interaction 4)*

## Why this matters for testing

This is the interaction that gives UC02b its own reason to exist rather than being a minor variant of UC02a: it's the first time this project models a `Device` resource at all. The test is whether implant-specific detail — the kind of information that's historically lived only in the surgeon's own record — can be captured with enough structure (manufacturer, catalog number, placement torque) to actually be useful to someone else later, not just documented for documentation's sake.

## What's deliberately NOT part of this interaction

Getting that `Device` record to Dr. Parker's practice, where it'll actually matter months from now for the crown — that's Interaction 4.
