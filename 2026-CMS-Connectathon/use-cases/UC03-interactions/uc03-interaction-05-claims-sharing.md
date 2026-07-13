# UC03 — Interaction 5: Claims-Sharing

**Corresponds to:** 2026-05-28, following Interaction 4 — the FHIR-native equivalent of what would otherwise become the 837D Dr. Watson's practice submits to Connecticut Dental Health Partnership on 2026-05-29.

## What happens

Dr. Watson's practice needs to get paid for the evaluation, the scaling and root planing, the chlorhexidine, and the hygiene instruction. In the real world, that's an 837D — but routed through a three-tier structure worth naming precisely: Connecticut DSS (the state Medicaid sponsor) contracts with a Connecticut Medicaid MCO, which contracts with Connecticut Dental Health Partnership (the actual dental plan administrator and claims adjudicator). Benecare, who found Dr. Watson for Timothy's family back in Interaction 1, is not part of this chain at all — they handle referral coordination and network directories, not claims.

What this interaction actually builds is the same claims-ready package this project has already designed (`ODEOralProfessionalEOB`): the four procedures, CDT-coded, the diagnosis, and the referring/rendering provider chain — assembled into one interoperable bundle, not a submitted claim.

**This bills a dental payer — Connecticut Dental Health Partnership — not a medical benefit.** CDT is what's actually required here, consistent with the correction already made for UC02: no CPT crosswalk reasoning applies.

## What Timothy's Guardians See (patient-facing)

📱 **Notification:** *(none — back-office billing event, not patient-facing)*

## Key resources exchanged in this interaction

The claims-ready bundle itself: `D0150`, `D4341` (both quadrants — see Interaction 3's open question about whether this is one or two `Procedure` references here), `D4381`, `D1330`; diagnosis `K05.21` (with `E10.9` as supporting context, since the source doc notes D4341 requires medical-necessity documentation for a pediatric patient); the referring/rendering provider chain (Dr. Smith as originating referrer, Dr. Watson as rendering).

## Why this matters for testing — and two things carried forward honestly, not resolved here

This is the third proof point for the claims-sharing profile generalizing across dental-payer contexts — after Medicaid (UC02a) and commercial (UC02b), now a **CHIP program routed through an MCO-to-plan-administrator chain**, a genuinely different administrative structure than either prior case.

**The source use case document itself flags two coverage questions as unresolved — carried forward here rather than silently assumed one way or the other:**
1. Whether `D4341` requires prior authorization under the applicable Husky B benefit year. The doc states no PA is required *as its primary position*, but explicitly notes benefit design varies year to year and flags this as an open test finding — not fully settled.
2. Whether `D4381` (the chlorhexidine delivery) is covered at all under the Husky B pediatric benefit — the doc marks this with its own warning symbol as uncertain.

Neither of these is this project's gap to close — they're real open questions in the source material, and this interaction should be built to reflect that honestly (e.g., not asserting a confident coverage determination the source doc itself doesn't make).

## What's deliberately NOT part of this interaction

The well-child visit's own medical billing (Dr. Smith's oral health assessment, billed under the medical benefit, likely CPT 99461 or equivalent) — the source doc explicitly puts this out of scope for this dental Connectathon use case.
