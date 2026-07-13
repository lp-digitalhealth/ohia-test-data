# UC04b-I5: Billing Three Teeth

**Corresponds to:** 2026-07-24, 08:00 (teledentistry) and 08:30 (in-office) — both submitted before Dr. Torres's 09:00 follow-up message the same morning.

## What happens

Same two-organization pattern as UC04a: Dr. Torres's teledentistry organization bills the Texas Medicaid dental benefit manager for the virtual consultation (D9995, POS 02). Separately, Dr. Okafor's in-office practice bills for everything it actually did — the extraction, both radiographs, and both interim restorations (D0220, D0274, D7210, D2940 ×2, POS 11). Two organizations, two independent claims-ready packages, tied together only by the shared referral reference.

**This bills a dental benefit manager under Texas Medicaid — CDT is what's required, same as UC04a and consistent with UC02's established reasoning.**

## What Darius Sees (patient-facing)

📱 **Notification:** *(none — back-office billing, not patient-facing)*

## Key resources exchanged in this interaction

Two `ODEOralProfessionalEOB`-shaped bundles:
1. Teledentistry package: `D9995`, POS 02
2. In-office package: `D0220`, `D0274`, `D7210`, `D2940` ×2, POS 11 — covering all three teeth treated, not just the one originally referred

## Why this matters for testing

Fourth proof point for the claims-sharing profile — now through a Medicaid DBM, with a genuinely more complex in-office package than UC04a's (five service lines across three teeth, not two lines on one). The test is whether the profile handles that complexity without needing a different shape than the simpler case did.

## What's deliberately NOT part of this interaction

Any reconciliation between the two claims, same as UC04a.
