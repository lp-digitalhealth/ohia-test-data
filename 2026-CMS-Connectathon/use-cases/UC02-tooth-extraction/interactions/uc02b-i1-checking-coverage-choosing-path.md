# UC02b-I1: Checking Coverage, Choosing a Path

**Corresponds to:** 2026-07-08, 10:00–11:00.

## What happens

Frank comes in with the same pain and swelling as in UC02a — but this time he has commercial dental PPO coverage through his employer, not Medicaid. Dr. Parker finds the same failed root canal, the same vertical fracture, the same non-restorable tooth #30. This time, though, there are two real options to discuss: extraction alone, or extraction with an implant placed the same day.

Before that conversation can be meaningful, Dr. Parker's staff checks Frank's actual benefits in real time — not a guess, an actual query to the plan: does he have implant coverage, is he past any waiting period, how much of his annual maximum is left. The system also checks whether this specific procedure needs prior authorization under this plan. It doesn't — commercial coverage here works differently than Medicaid's PA-gated pathway in UC02a.

With that information in hand, Dr. Parker sends the referral to Dr. Maxil that same morning — no PA delay, no waiting days for an answer.

## What Frank Sees (patient-facing)

📱 **Notification:** *"Referral sent to Austin Oral Surgery."*

## Why this matters for testing

This interaction deliberately tests the CRD hook returning a *negative* result — no PA needed, coverage confirmed — rather than always testing the PA-required path UC02a exercises. A system that only knows how to handle "PA required" isn't actually solving the coverage-discovery problem; it needs to correctly and confidently say "you're clear to proceed" too, and it needs to check something UC02a's binary PA check doesn't: benefit-specific detail like waiting periods and remaining annual maximum.

## What's deliberately NOT part of this interaction

Which treatment Frank actually chooses — extraction alone, or extraction with implant — isn't decided yet. Both options travel in the referral for Dr. Maxil's review; the decision happens at the consultation, in Interaction 3.
