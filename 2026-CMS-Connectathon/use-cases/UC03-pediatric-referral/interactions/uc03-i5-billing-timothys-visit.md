# UC03-I5: Billing Timothy's Visit

**Corresponds to:** 2026-05-28, following Interaction 4 — the FHIR-native equivalent of what would otherwise become the 837D Dr. Watson's practice submits to Gainwell (CMAP) — the DSS fiscal agent that adjudicates and pays HUSKY dental claims — on 2026-05-29.

## What happens

Dr. Watson's practice needs to get paid for the evaluation, the scaling and root planing, the chlorhexidine, and the hygiene instruction. In the real world, that's an 837D — routed through a structure worth naming precisely, because it is *not* an MCO chain: Connecticut DSS (the state Medicaid sponsor) contracts **Gainwell Technologies** as its fiscal agent, which runs the MMIS (CMAP) and is the entity that actually **adjudicates and pays** the 837D. The HUSKY dental benefit itself is branded as the **Connecticut Dental Health Partnership (CTDHP)**, which is **administered/facilitated by BeneCare (an ASO)** — BeneCare owns the network, the provider directory, referral coordination, and prior-authorization intake, but it does **not** adjudicate or pay claims. There is **no dental MCO** in this chain. BeneCare is the same party that found Dr. Watson for Timothy's family back in Interaction 1; its role here is network/PA-side, while the claim itself is adjudicated by Gainwell.

What this interaction actually builds is the same claims-ready package this project has already designed (`ODEOralProfessionalEOB`): the four procedures, CDT-coded, the diagnosis, and the referring/rendering provider chain — assembled into one interoperable bundle, not a submitted claim.

**This bills the HUSKY dental benefit (CTDHP), adjudicated by Gainwell (CMAP) as the DSS fiscal agent — not a medical benefit.** CDT is what's actually required here, consistent with the correction already made for UC02: no CPT crosswalk reasoning applies.

## What Timothy's Guardians See (patient-facing)

📱 **Notification:** *(none — back-office billing event, not patient-facing)*

## Key resources exchanged in this interaction

The claims-ready bundle itself: `D0150`, **`D4341` as two line items (one per quadrant, matching the two `Procedure` resources built in Interaction 3)**, `D4381`, `D1330`; diagnosis `K05.211` (aggressive periodontitis, localized, slight; with `E10.9` as supporting context, since D4341 requires medical-necessity documentation for a pediatric patient); the **`preAuthRef` from the I3 prior-authorization** carried on the SRP lines; the referring/rendering provider chain (Dr. Smith as originating referrer, Dr. Watson as rendering). Insurer is **Gainwell** (CMAP fiscal agent); billing provider is **Cornell Scott-Hill** (Dr. Watson's practice).

## Why this matters for testing — and one thing carried forward honestly, not resolved here

This is the third proof point for the claims-sharing profile generalizing across dental-payer contexts — after Medicaid (UC02a) and commercial (UC02b), now a **CHIP program on a fiscal-agent model** (DSS → Gainwell as fiscal agent/claims adjudicator; CTDHP dental plan facilitated by BeneCare as ASO; no MCO), a genuinely different administrative structure than either prior case.

**Resolved this session — `D4341` requires prior authorization.** Rather than leaving PA as an open question, UC03 treats D4341 as PA-required and builds out the full CRD/DTR/PAS cycle at the treatment visit (Interaction 3). The EOB here therefore carries the `preAuthRef` from that approval on its SRP lines — this is a load-bearing part of the use case, not a footnote.

**Still genuinely open — `D4381` coverage.** Whether the localized chlorhexidine delivery (D4381) is covered at all under the HUSKY B pediatric benefit remains unresolved in the source material and is not this project's gap to close. The line is included in the package but explicitly **flagged as coverage-uncertain** — not asserted as a confident coverage determination the source doc itself doesn't make.

## What's deliberately NOT part of this interaction

The well-child visit's own medical billing (Dr. Smith's oral health assessment, billed under the medical benefit, likely CPT 99461 or equivalent) — the source doc explicitly puts this out of scope for this dental Connectathon use case.
