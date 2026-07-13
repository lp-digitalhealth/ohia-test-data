# UC02b — Interaction 5: Claims-Sharing

**Corresponds to:** 2026-07-15, following the post-operative summary and Device record (Interaction 4) — the FHIR-native equivalent of what would otherwise become the 837D Austin Oral Surgery submits on 2026-07-16.

## What happens

Austin Oral Surgery needs to get paid for both the extraction and the implant placement. In the real world, that's an 837D to the commercial dental payer. What this interaction actually builds is the same interoperable claims-ready package (`ODEOralProfessionalEOB`): both procedures (D7210 and D6010, CDT-coded), the diagnosis, and the referring/rendering provider chain, assembled into one standardized bundle any downstream system can convert into its own 837D.

**Same correction as UC02a applies here: this is a dental-to-dental payer relationship — a commercial dental PPO, billed via 837D — not a medical benefit.** CDT is what's actually required; there's no CPT crosswalk doing real work here, unlike UC01's medical-payer direction.

## What Frank Sees (patient-facing)

📱 **Notification:** *(none — back-office billing event, not patient-facing)*

## Why this matters for testing

This is the second proof point for the claims-sharing profile generalizing across dental-payer contexts — here against a **commercial** dental PPO rather than Medicaid, with no PA number to carry forward and genuinely variable coverage rules (waiting periods, annual maximums) that don't exist the same way under Medicaid.

**One thing still genuinely open, not yet decided:** this interaction's scope, as built, covers only the *immediate* extraction+implant billing — mirroring UC02a. But UC02b's own source narrative names *"restorative continuity via structured implant record"* as its core value proposition, which points toward something broader: does the claims-sharing package also need to anticipate the *future* crown claim at Dr. Parker's practice, months from now, referencing this same `Device` record? That's a real design question for a later session, not resolved here — this interaction as built is the narrower, UC02a-parallel scope only.

## What's deliberately NOT part of this interaction

Dr. Parker's own separate claim for the original evaluation and radiograph — not modeled here, same as UC02a. The future crown claim (see the open question above) is also not part of this interaction as currently scoped.
