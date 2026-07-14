# UC03-I4: Telling Both Doctors

**Corresponds to:** 2026-05-28, same day as the encounter.

## What happens

Dr. Watson doesn't just document what happened — he tells the two medical providers who actually need to know, at the same time, through Connie. One summary goes to Dr. Smith, the pediatrician who referred Timothy in the first place: the periodontitis diagnosis, what was done about it, the home-care plan. A second, different summary goes to Timothy's pediatric endocrinologist — someone who was never part of the referral relationship at all, but who needs to know because periodontitis and glycemic control run in both directions. Poor glucose control accelerated this periodontal disease; the periodontal disease can now, in turn, make glucose control harder to manage. Dr. Watson's summary to the endocrinologist says as much directly, and recommends a review of Timothy's HbA1c in that light.

Timothy's guardian proxy app updates to show the visit is done, with Dr. Watson's care plan attached.

## What Timothy's Guardians See (patient-facing)

📱 **Notification:** *"Dental visit complete — care plan available."*

## Key resources exchanged in this interaction

**Two separate `ClinicalImpression` resources**, not one resource sent twice — different recipients, different emphasis:

- To Dr. Smith: diagnosis, treatment performed, oral hygiene care plan, a recommendation to reinforce hygiene at medical visits
- To the endocrinologist: diagnosis, the diabetes-periodontal relationship explicitly stated, the chlorhexidine administration (for antibiotic-stewardship awareness), and a recommendation to review HbA1c

**Two distinct `Flag` resources, pointed in opposite directions — worth being precise about, since they're easy to conflate:** Interaction 1's `Flag` said *diabetes elevates periodontal risk* (medical condition informing dental risk). This interaction creates a **new, separate** `Flag`, going the other way — *periodontal disease may be complicating glycemic control* — sent specifically to the endocrinologist. These are not the same resource reused; they're two different clinical claims, in opposite directions, and should be modeled as two distinct `Flag` resources.

Also: `CarePlan` (surfaced to the guardian app), `Procedure` marked completed, `MedicationAdministration` referenced in both summaries, `ServiceRequest.status` updated to `completed`, `Task` closure for both outbound pushes once Connie confirms delivery, and `Provenance`/`AuditEvent` entries for both routed transmissions.

## Why this matters for testing

This is its own named cross-cutting test objective in the source doc, distinct from the encounter itself: whether a dental practice can fire two simultaneous CDex pushes to two different organizations through Connie as the central HIE routing hub, and whether Connie correctly routes each to the right endpoint. It's also the interaction where the diabetes-periodontal relationship has to become genuinely structured data — a `Flag`, not a sentence in a note — since that's the whole clinical point of sending anything to the endocrinologist at all.

## What's deliberately NOT part of this interaction

Getting Dr. Watson's practice paid — that's Interaction 5.
