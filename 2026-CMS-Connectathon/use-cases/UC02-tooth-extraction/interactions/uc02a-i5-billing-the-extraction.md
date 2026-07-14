# UC02a-I5: Billing the Extraction

**Corresponds to:** 2026-07-21, following the post-operative summary (Interaction 4) — the FHIR-native equivalent of what would otherwise become the 837D Austin Oral Surgery submits on 2026-07-22.

## What happens

Now that the extraction is done, Austin Oral Surgery needs to get paid. In the real world, that's an 837D to Texas Medicaid's dental plan. What this interaction actually builds instead is the standardized, interoperable claims-ready package this project has already designed (`ODEDentalClaim`): the procedure (D7210, CDT-coded), the PA number carried all the way through from Interaction 1, the diagnosis, and the referring/rendering provider chain — everything a downstream system needs to construct its own 837D, without OHIA having made that construction decision on the practice's behalf.

**This is a dental-to-dental payer relationship — Texas Medicaid's dental plan, billed via 837D — not a medical benefit.** CDT is what's actually required here; there's no CPT crosswalk to reason about the way there was in UC01, where the receiving payer was a medical plan. If a CPT crosswalk is included at all, it's incidental, not load-bearing — the opposite of UC01's direction.

## What Frank Sees (patient-facing)

📱 **Notification:** *(none — this is a back-office billing event between Austin Oral Surgery and the payer; nothing here is patient-facing)*

## Why this matters for testing

This is UC02a's key driver, not an afterthought: it's the first real proof point for whether the claims-sharing package designed for UC01's medical-payer direction genuinely generalizes to a **dental** payer, where CDT alone is sufficient and CPT is unnecessary rather than load-bearing. The test is whether the same profile shape — non-financial, forward-compatible — holds up cleanly when the crosswalk that mattered in UC01 simply isn't needed here.

## What's deliberately NOT part of this interaction

Dr. Parker's own separate claim for the original evaluation and radiograph (D0140, D0220) — a parallel billing event, not modeled here, since it doesn't involve the referral relationship or the claims-sharing profile.
