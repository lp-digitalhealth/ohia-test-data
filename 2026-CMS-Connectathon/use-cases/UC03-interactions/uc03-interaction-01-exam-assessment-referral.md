# UC03 — Interaction 1: Well-Child Exam, Oral Health Assessment & Referral Creation

**Corresponds to:** 2026-02-28 (exam, assessment, provider search, referral creation) through approximately 2026-03-05 (scheduling confirmed — the source doc gives this second date as an approximation, not exact).

## What happens

Timothy is at New Haven Pediatric Care Center for his well-child visit. He's six, generally up to date on care, and living with Type 1 diabetes — diagnosed a year earlier, in February 2025, now managed with an insulin pump and a continuous glucose monitor. Dr. Smith already has all of that on his chart; today's visit adds something new.

As part of the well-child protocol, Dr. Smith does a pediatric oral health assessment. She finds two missing lower baby teeth, one adult tooth partially in, and Timothy mentions pain around that area. There's noticeable gingivitis. She also notes tobacco smoke exposure in the household. Taken alone, this would be a routine referral. Taken alongside Timothy's diabetes — which impairs immune response and periodontal healing — Dr. Smith is concerned this could progress quickly. She asks if Timothy has a dental home. He doesn't; he's never seen a dentist.

Dr. Smith documents the gingivitis, flags the diabetes as an elevated periodontal risk factor (not just background history — an active clinical signal for whoever sees him next), and creates a referral. Timothy's parents contact Benecare, which handles referral coordination and network directory services for Connecticut's Medicaid dental program, to find a pediatric dentist within 20 miles who takes Husky B and is accepting new patients. They land on Dr. David Watson. The referral is created the same day, already carrying a target appointment window — but the earliest actual opening is three months out, in late May.

## What Timothy's Guardians See (patient-facing)

📱 **Notification:** *"Referral created — pediatric dental evaluation."*

Timothy is six; this and every subsequent notification in this use case goes to the guardian proxy application his parents access, not to Timothy directly.

## Key resources exchanged in this interaction

- `Encounter` (well-child visit) and `Observation` (the oral health assessment findings — tooth loss, gingivitis, pain) — newly created
- `Condition` — K05.00 (gingivitis) and Z77.22 (tobacco smoke exposure) newly asserted at this visit. **`Condition` E10.9 (Type 1 diabetes) is NOT newly created here** — it already exists from the 2025 diagnosis and is simply referenced/flagged, not re-asserted
- `Flag` — Type 1 diabetes as an elevated periodontal risk factor, newly created by Dr. Smith, referencing the pre-existing E10.9 `Condition`
- `ServiceRequest` (the referral) — `reasonCode` K05.00 + E10.9, `supportingInfo` referencing the `Flag`, `MedicationRequest` (insulin lispro), and `Device` (CGM, insulin pump). Created with `occurrenceDateTime` already set to the target appointment date (2026-05-28), even though that date isn't confirmed until scheduling
- `DocumentReference` wrapping the oral health assessment findings
- Read-only query against Benecare's Plan-Net directory (`PractitionerRole`, `HealthcareService`) — not something this practice creates, just queries
- `Appointment` — created around 2026-03-05, but with a start date three months in the future

## Why this matters for testing

This is a compound interaction — assessment, risk flagging, provider search, and referral creation, all close together in time — but it's also the moment that sets up the two things that make this use case distinct: a `Flag` carrying an active systemic-disease risk signal (not just problem-list history), and a referral whose actual appointment date is already three months out at the moment it's created. That three-month gap isn't a scheduling inconvenience being glossed over — it's the clinical setup for what Interaction 3 finds.

## What's deliberately NOT part of this interaction

Any of Timothy's actual medical records — diagnoses, medications, devices, care team — being transmitted to Dr. Watson's practice. That doesn't happen now, even though the referral exists; it happens much later, right before the appointment, in Interaction 2.
