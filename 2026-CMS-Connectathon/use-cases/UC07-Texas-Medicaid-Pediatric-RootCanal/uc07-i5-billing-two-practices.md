# UC07-I5: Billing Two Practices

**Corresponds to:** 2026-07-23, 08:00 (pediatric practice claim) and 08:30 (restorative practice claim).

## What happens

The next morning, each practice bills DentaQuest for its own work. Dr. Parker's practice submits an 837D for the evaluation and radiographs (D0140, D0220, D0270). Dr. Garcia's practice submits an 837D for the root canal, build-up, and crown (D3320, D2950, D2740), with **the authorization number from Interaction 2 on the claim**. DentaQuest adjudicates both claims and pays through a remittance advice.

DentaQuest is a **payer, not a provider**. Claims route by DentaQuest's clearinghouse Payer ID (`CX014`), and DentaQuest carries no NPI.

## Why this matters for testing

- **The PA number carries through.** The number DentaQuest issued at approval has to appear on the restorative claim, or the claim has nothing tying it to the authorization. The sequence is PA approved, PA number on the 837D, claim adjudicated with the PA reference.
- **Two claims, one referral relationship.** Both practices bill the same payer for the same tooth, days apart, and the payer's earlier referral notification from Interaction 1 should let it connect them.
- **CDT is sufficient.** This is a dental benefit paid by a dental plan, so CDT alone drives the claim. No CPT crosswalk is needed or load-bearing, unlike UC01's medical-payer direction.

## What's deliberately NOT part of this interaction

Prior authorization, which is already finished.
