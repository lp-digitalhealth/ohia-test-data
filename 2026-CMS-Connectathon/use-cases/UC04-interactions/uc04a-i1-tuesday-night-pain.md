# UC04a-I1: Tuesday Night Pain

**Corresponds to:** 2026-07-14, 19:22–20:05.

## What happens

It's 7:30 PM on a Tuesday. Sarah has had building pain on her lower left side for days, and now she can't chew on that side at all. Her dentist's office is closed. She opens the SMART-enabled app tied to her Aetna Dental PPO teledentistry benefit. The app checks her coverage in real time — active, confirmed — and connects her to Dr. Marcus Webb, a licensed Texas dentist practicing virtually.

Dr. Webb runs a structured virtual assessment: how long has the pain been building, is it sensitive to temperature, does biting down make it worse, does it ache without anything touching it. What Sarah describes is consistent with irreversible pulpitis in tooth #19, possibly already involving the tissue around the root. This isn't something a virtual visit can resolve — it needs in-person evaluation, radiographs, and likely a root canal. Dr. Webb documents his findings as structured data, not a dictated note, and creates a referral to an in-network general dentist in Austin.

## What Sarah Sees (patient-facing)

📱 **Notification:** *"Referral sent."*

## Key resources exchanged in this interaction

- `Coverage` (queried, confirming active Aetna Dental PPO eligibility) and `InsurancePlan` (teledentistry + endodontic benefit detail)
- `Encounter` (virtual, POS 02)
- `Condition` — K04.01 (irreversible pulpitis), newly asserted by Dr. Webb
- `Observation` — the symptom findings themselves (duration, thermal sensitivity, pain on biting, spontaneous aching), tooth-level
- `MedicationStatement` — patient-reported medications
- `ServiceRequest` (the referral, priority `urgent`) and `DocumentReference` wrapping the structured findings bundle — transmitted via CDex provider-to-provider push

**No imaging is exchanged here, and none exists yet to exchange.** Unlike UC01/UC02, the originating provider is virtual — Dr. Webb has no way to take a radiograph. The clinical findings that travel with this referral are entirely symptom-based (`Condition`/`Observation`/`MedicationStatement`), not imaging. The radiograph doesn't exist until Interaction 3.

## Why this matters for testing

This is the first OHIA Connectathon test of a referral **originating from a virtual encounter** rather than an in-office one — clinical findings have to be expressible as discrete FHIR resources from a non-PMS-centric setting, and coverage verification has to happen in real time, mid-session, not as a separate back-office step days earlier the way it did in UC01/UC02.

## What's deliberately NOT part of this interaction

Anyone at the in-office practice seeing this referral yet — that's Interaction 2.
