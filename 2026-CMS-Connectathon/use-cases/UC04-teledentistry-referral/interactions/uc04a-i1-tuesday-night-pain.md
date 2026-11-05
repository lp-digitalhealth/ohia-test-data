# UC04a-I1: Tuesday Night Pain

**Corresponds to:** 2026-07-14, 19:22–20:05.

## What happens

It's 7:30 PM on a Tuesday. Sarah has had building pain when she bites on her front teeth for days, and now she can't chew or bite with them at all. She doesn't have a dental home. She opens the SMART-enabled app tied to her Aetna Dental PPO teledentistry benefit. The app checks her coverage in real time — active, confirmed — and connects her to Dr. Marcus Webb, a licensed Texas dentist practicing virtually.

Dr. Webb runs a structured virtual assessment: how long has the pain been building, is it sensitive to temperature, does biting down make it worse, does it ache without anything touching it. He confirms she hasn't seen a dentist in some time. He also has Sarah use her phone to capture one or two intraoral photos of the sore front-tooth area through the app, which he reviews on screen. What Sarah describes — and what the photos show — suggests irreversible pulpitis in tooth #9, possibly already involving the tissue around the root. This isn't something a virtual visit can resolve — it needs in-person evaluation, radiographs, and likely a root canal. Dr. Webb documents his findings as structured data, not a dictated note, and creates a referral to an in-network general dentist in Austin, sending her medications and allergies along with it and the photos by reference (ARex), not inline.

## What Sarah Sees (patient-facing)

📱 **Notification:** *"Referral sent."*

## Key resources exchanged in this interaction

- `Coverage` (queried, confirming active Aetna Dental PPO eligibility) and `InsurancePlan` (teledentistry + endodontic benefit detail)
- `Encounter` (virtual, POS 02)
- `Condition` — K04.01 (irreversible pulpitis), newly asserted by Dr. Webb as provisional (suspected)
- `Observation` — the symptom findings themselves (duration, thermal sensitivity, pain on biting, spontaneous aching), tooth-level
- `Observation` — dental history: no dental home, has not seen a dentist in some time (patient-reported)
- `MedicationStatement` — patient-reported medications
- `AllergyIntolerance` — patient-reported allergies
- `DocumentReference` (intraoral photos) — 1–2 patient-submitted phone photos of the tooth #9 region, non-radiographic, correlated to the tooth via `Observation.derivedFrom`, delivered by ARex reference
- ARex manifest (`List`), its `DocumentReference` content entries and a `Provenance` — the photos by reference instead of inline
- `ServiceRequest` (the referral, priority `urgent`) and a second `DocumentReference` wrapping the structured findings bundle — transmitted via CDex provider-to-provider push

**No *radiograph* is exchanged here — but patient photos are.** The originating provider is virtual, so Dr. Webb can't take a radiograph; the diagnostic radiograph (DICOM/PACS) doesn't exist until Interaction 3. What Sarah *can* contribute are intraoral photos snapped on her phone through the app, and those travel with the referral as a US Core `DocumentReference` delivered **by ARex reference** (a manifest of one or two `image/jpeg` content entries, `author` = Patient; nothing inline). Because R4 `DocumentReference` has no body-site element, the affected tooth (#9) is carried on the symptom `Observation` (`bodySite`), which points at the photos via `derivedFrom` — so the receiving practice re-associates the images to the right tooth. This is deliberately distinguished from the DICOM radiograph/`ImagingStudy` layer, which is still a UC01/UC02-style artifact that only appears in-office at Interaction 3.

## Why this matters for testing

This is the first OHIA Connectathon test of a referral **originating from a virtual encounter** rather than an in-office one — clinical findings have to be expressible as discrete FHIR resources from a non-PMS-centric setting, and coverage verification has to happen in real time, mid-session, not as a separate back-office step days earlier the way it did in UC01/UC02.

## What's deliberately NOT part of this interaction

Anyone at the in-office practice seeing this referral yet — that's Interaction 2.
