# UC03-I1: A Routine Checkup Finds Something Else

**Corresponds to:** 2026-02-28 (exam, assessment, provider search, referral creation) through approximately 2026-03-05 (scheduling confirmed — the source doc gives this second date as an approximation, not exact).

## What happens

Timothy is at Northeast Medical Group — a Yale New Haven Health pediatric practice — for his well-child visit. He's six, generally up to date on care, and living with Type 1 diabetes — diagnosed a year earlier, in February 2025, now managed with an insulin pump and a continuous glucose monitor. Dr. Smith already has all of that on his chart; today's visit adds something new.

As part of the well-child protocol, Dr. Smith does a pediatric oral health assessment. She finds two missing lower baby teeth, one adult tooth partially in, and Timothy mentions pain around that area. There's noticeable gingivitis. She also notes tobacco smoke exposure in the household. Taken alone, this would be a routine referral. Taken alongside Timothy's diabetes — which impairs immune response and periodontal healing — Dr. Smith is concerned this could progress quickly. She asks if Timothy has a dental home. He doesn't; he's never seen a dentist.

Dr. Smith documents the gingivitis, flags the diabetes as an elevated periodontal risk factor (not just background history — an active clinical signal for whoever sees him next), and creates a structured referral in Epic. The referral doesn't go point-to-point: it's **routed through Connie**, Connecticut's statewide HIE and the hub for this whole workflow, to **BeneCare** — the Administrative Services Organization that runs the HUSKY dental plan (CTDHP) for the state. BeneCare's Plan-Net directory is what identifies a pediatric dentist within 20 miles who takes Husky B and is accepting new patients; they land on **Dr. David Watson** at Cornell Scott-Hill Health Center. The referral is created the same day, already carrying a target appointment window — but the earliest actual opening is three months out, in late May.

At this point this is a referral, not a treatment order — there's no prior-authorization requirement to clear. Timothy's dental benefit is active and the evaluation itself is covered, so no coverage-requirements discovery (CRD) fires here. That comes later: it's only when Dr. Watson plans actual treatment at the dental visit that CRD would surface any documentation requirements, and — if prior authorization applies to a planned procedure — the documentation (DTR) and prior-auth submission (PAS) run downstream through **Gainwell**, the DSS fiscal agent that operates the CT Medical Assistance Program, not through Connie or BeneCare. For this referral, coverage is simply confirmed as active; CRD/PA are out of scope until treatment is planned.

## What Timothy's Guardians See (patient-facing)

📱 **Notification:** *"Referral created — pediatric dental evaluation."*

Timothy is six; this and every subsequent notification in this use case goes to the guardian proxy application his parents access, not to Timothy directly.

## Key resources exchanged in this interaction

- `Encounter` (well-child visit) and `Observation` (the oral health assessment findings — tooth loss, gingivitis, pain) — newly created
- `Condition` — K05.00 (gingivitis) and Z77.22 (tobacco smoke exposure) newly asserted at this visit. **`Condition` E10.9 (Type 1 diabetes) is NOT newly created here** — it already exists from the 2025 diagnosis and is simply referenced/flagged, not re-asserted
- `Flag` — Type 1 diabetes as an elevated periodontal risk factor, newly created by Dr. Smith, referencing the pre-existing E10.9 `Condition`
- `ServiceRequest` (the referral) — `reasonCode` K05.00 + E10.9, `supportingInfo` referencing the `Flag`, `MedicationRequest` (insulin lispro), and `Device` (CGM, insulin pump). Created with `occurrenceDateTime` already set to the target appointment date (2026-05-28), even though that date isn't confirmed until scheduling
- `DocumentReference` wrapping the oral health assessment findings
- The referral itself routed through Connie (the HIE hub) to BeneCare (the dental ASO) — Connie is the routing mechanism, not a passive pass-through
- Read-only query against BeneCare's Plan-Net directory (`PractitionerRole`, `HealthcareService`) — not something this practice creates, just queries
- Dental benefit confirmed active for the covered evaluation — **no CRD/PA at referral** (CRD only fires when treatment is planned at the visit; DTR/PAS, if ever needed then, are Gainwell's downstream). Not a built artifact in I1
- `Appointment` — created around 2026-03-05, but with a start date three months in the future

## Why this matters for testing

This is a compound interaction — assessment, risk flagging, provider search, and referral creation, all close together in time — but it's also the moment that sets up the things that make this use case distinct: a `Flag` carrying an active systemic-disease risk signal (not just problem-list history); a referral whose actual appointment date is already three months out at the moment it's created; and, importantly, a referral that travels **through the state HIE (Connie) to the dental ASO (BeneCare)** rather than point-to-point — exercising Connie's real closed-loop-referral role for Medicaid. Note what is deliberately *not* exercised here: there's no CRD/prior-authorization step, because a covered evaluation referral doesn't trigger one — that responsibility (CRD, then DTR/PAS via Gainwell if a planned procedure needs it) belongs to the treatment visit, not this referral. That three-month gap isn't a scheduling inconvenience being glossed over — it's the clinical setup for what Interaction 3 finds.

## What's deliberately NOT part of this interaction

Any of Timothy's actual medical records — diagnoses, medications, devices, care team — being transmitted to Dr. Watson's practice. That doesn't happen now, even though the referral exists; it happens much later, right before the appointment, in Interaction 2.
