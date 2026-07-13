# UC02a — Interaction 1: The Prior Authorization Cycle

**Corresponds to:** 2026-07-08, 10:00 (evaluation) through 2026-07-14, 14:01 (patient notified of approval).

## What happens

Frank comes to Dr. Parker's Austin general dental practice with pain and swelling on the lower right side. Dr. Parker examines him and takes a periapical radiograph, confirming what she suspected: the root canal on tooth #30 has failed, there's a vertical fracture below the gumline, and the tooth can't be saved. It needs to come out.

The moment Dr. Parker enters the extraction order, two things happen automatically, within minutes: the system checks Frank's Texas Medicaid dental benefit and flags that this specific procedure requires prior authorization, and it pulls up the exact documentation the plan will need, pre-filling as much as possible from what Dr. Parker already has on file — the diagnosis, the radiograph findings, the tooth number.

Two days later, on July 10th, Dr. Parker's staff submits the completed request. On July 14th, the plan responds: approved, with an authorization number attached.

## What Frank Sees (patient-facing)

📱 **Notification:** *"Prior authorization approved for your dental procedure."*

This is the only thing Frank actually sees in this entire interaction — nothing fires during the evaluation, the CRD check, or the DTR pre-population, since none of that is patient-facing. One notification represents the whole cycle collapsing down to a single plain-language fact: he's cleared to move forward.

## Why this matters for testing

This is the highest-novelty piece of UC02a: the first time this Connectathon exercises Da Vinci's coverage-discovery, documentation, and prior-authorization standards against a *dental* benefit plan and CDT procedure codes, rather than the medical-benefit context they were originally built and tested for. A firm's system needs to correctly evaluate PA requirements for a CDT code, pre-populate a dental-specific questionnaire, and carry the resulting PA number forward — nothing downstream in this use case works without it.

## What's deliberately NOT part of this interaction

The referral to Dr. Maxil doesn't happen yet — that's Interaction 2, and it can't start until this PA number exists.
