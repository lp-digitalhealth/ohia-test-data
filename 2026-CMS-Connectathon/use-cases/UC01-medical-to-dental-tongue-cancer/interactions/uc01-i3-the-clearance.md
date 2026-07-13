# UC01-I3: The Clearance

**Corresponds to:** clinical Encounter #6 (dental clearance visit, 2026-07-31).

## What happens

By 2026-07-31, John has had all three problem teeth addressed: #4 and #17 extracted, and #30 — the tooth sitting in the high-dose radiation field — extracted with an implant placed immediately, based on the dose data Dr. Bellweather got back from Dr. Nandakumar earlier in the process.

Dr. Bellweather examines John one more time to confirm everything is healing as expected. Satisfied, he formally documents his conclusion: **John is cleared for radiation.** His written assessment says, in effect: three teeth removed, one immediately replaced with an implant because of the radiation dose it would have received, the rest of his teeth are fine to proceed, no reason to hold off on treatment — plus his aftercare instructions: give it 14 days to heal, and get follow-up dental imaging at 6, 12, and 24 months out.

Thirty minutes later, that clearance goes to FCCC. Not as a phone call, not as a fax, not as a PDF — as structured data his system sends directly into Dr. Whitfield's. This is the moment the entire dental detour that started with Interaction 1's referral comes to a close: the thing FCCC was waiting on to move forward with radiation now exists, in a form Dr. Whitfield's system can actually read and act on rather than a human having to retype it.

## What John Sees (patient-facing)

📱 **Notification:** *"Clearance sent to your cancer care team."*

This is the last milestone this particular referral-status Subscription tracks — the next notification John gets (prior authorization approved) comes from a different signal entirely (the payer's side, Interaction 4), not this same referral Task.

**Two things close out at this same moment, from two different angles**, even though from John's perspective it's just "the dentist sent his clearance to the cancer center" — and even though both are tracked by the same underlying record, not two separate ones:

1. **The referral itself is now finished.** Dr. Bellweather did what was asked of him back in Interaction 1 and has reported back — the loop that opened when Dr. Whitfield sent the referral is now closed.
2. **The payer's specific paperwork requirement is now satisfied.** Back at Interaction 1, IBX's system flagged that a dental clearance had to be documented before it would approve the radiation. That open requirement is now checked off, at the same moment as the referral closing.

## Why this matters for testing

This interaction tests whether structured clinical data — not a PDF, not a phone call — can travel from a dental practice management system directly into an oncology EHR, and be understood as a genuine clearance to proceed. It's also the one moment in this use case where two things a system cares about (the referral relationship, and the payer's documentation requirement) both resolve at once, from a single clinical action, tracked by a single underlying record. A firm's system needs to correctly recognize that one real-world event — the clearance being sent — closes out both things it's tracking, without needing two separate resources to do it.

## Technical mechanics (for firms building against this interaction)

This corresponds to the IHE 360X **PCC-57 (Referral Outcome)** transaction — the wire-level message is `OMG^O19` accompanied by a C-CDA Consultation Note. On the FHIR side: the referral's `Task` (the same one opened in Interaction 1, now in its final version) transitions to `status: completed`, `businessStatus: outcome-final`, and gains an `owner` (Dr. Bellweather's `PractitionerRole`) reflecting who ultimately accepted and fulfilled the referral. `Task.output` gains references to the `ClinicalImpression` (the clearance attestation), three `Procedure` resources (the extractions and implant), a coded disposition `Observation`, and a `DocumentReference` representing the C-CDA document. The referral's `ServiceRequest` also moves to `status: completed`.

## What happens right after, but belongs to a different interaction

FCCC's billing office takes this clearance and packages it up to actually submit the prior authorization request to IBX. That's Interaction 4, not this one — Interaction 3 ends the moment the clearance lands at FCCC.
