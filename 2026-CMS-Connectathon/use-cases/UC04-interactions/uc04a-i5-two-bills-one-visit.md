# UC04a-I5: Two Bills, One Visit

**Corresponds to:** 2026-07-16, 08:00 (teledentistry) and 08:30 (in-office) — the FHIR-native equivalent of the two separate 837Ds the source doc names explicitly at these times.

## What happens

Two different organizations need to bill the same payer for the same episode of care, thirty minutes apart. Dr. Webb's teledentistry organization bills for the virtual consultation itself — D9995, place of service 02. Separately, Dr. Nair's in-office practice bills for the evaluation, radiograph, and root canal — D0220 and D3330, place of service 11. Real-world billing means two 837Ds. What this interaction builds instead is **two separate claims-ready packages**, one per organization — this is a genuine design decision, not an oversight: each organization is its own biller with its own NPI and its own rendering relationship to the payer, so a single combined package wouldn't reflect how the billing actually works.

**Both bill a commercial dental payer (Aetna Dental) — CDT is what's required, same reasoning already established for UC02.**

## What Sarah Sees (patient-facing)

📱 **Notification:** *(none — back-office billing, not patient-facing)*

## Key resources exchanged in this interaction

Two `ODEOralProfessionalEOB`-shaped bundles:
1. Teledentistry package: `D9995`, POS 02, Dr. Webb's organization as biller
2. In-office package: `D0220` + `D3330`, POS 11, Dr. Nair's organization as biller, referencing the same referral ID as evidence of the coordinated episode

## Why this matters for testing

This is the first time this project's claims-sharing profile has needed to represent **two independently-billing organizations for one coordinated episode of care**, rather than one organization billing for everything it did. The test is whether the profile's shape holds up unchanged when used twice in parallel, tied together only by a shared referral reference, rather than needing a different structure to represent "this is part of something bigger."

## What's deliberately NOT part of this interaction

Any reconciliation between the two claims — they're independent submissions to the same payer, not a bundled joint claim.
