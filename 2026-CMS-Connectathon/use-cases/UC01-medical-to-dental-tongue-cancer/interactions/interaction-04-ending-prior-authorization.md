# Interaction 4: Ending the Prior Authorization

**Corresponds to:** the PA submission and approval, 2026-08-01 through 2026-08-03 — not tied to a single clinical encounter, since this is billing-office activity, not a patient visit.

## What happens

FCCC's billing office now has everything it needs: the completed documentation questionnaire from DTR, and — critically — Dr. Bellweather's dental clearance, which arrived at the end of Interaction 3. They package all of this into a formal prior authorization request and submit it to IBX on 2026-08-01.

**Important distinction:** this request is for the radiation treatment itself — the same IMRT service that was flagged back in Interaction 1 as needing prior authorization. It is not a request for Dr. Bellweather's dental work. The dental clearance is *evidence attached to* the radiation request, proving the prerequisite condition has been satisfied — not something being separately authorized here.

Two days later, on 2026-08-03, IBX approves the request. The response includes a formal authorization number and the specific approved details. Structured data, not a phone call or a letter — sent directly back into FCCC's system.

## What John Sees (patient-facing)

📱 **Notification:** *"Prior authorization approved."*

This is the last milestone in this use case's referral-tracking sequence, but it comes from a **different signal** than every prior notification — those all came from the referral `Task`'s status changing. This one comes from IBX's payer-side systems directly, delivered to John's app as a standardized "prior authorization" record within one business day of the decision, the same way any of his other claims data would reach him.

## Why this matters for testing

This interaction tests whether a full electronic prior authorization cycle — request, review, and approval — can happen entirely through structured data exchange, replacing what used to require a legacy fax-based transaction standard entirely. It also tests something subtler: whether a system correctly keeps *"the radiation is authorized"* and *"the dentist's own procedures were performed"* as two separate facts, even though the second is the reason the first was approved. A firm's system needs to attach the clearance as supporting evidence without confusing it for the thing actually being requested.

## What's still open — for a future iteration, not this one

Getting the radiation authorized isn't the end of the money story. Dr. Bellweather's own procedures still need to be billed to IBX for reimbursement — a separate, later billing event using the medical-payer crosswalk codes documented in this use case's appendix, and the claims-sharing package this project has separately designed for exactly that purpose. That reimbursement claim isn't part of this interaction, and isn't yet built.
