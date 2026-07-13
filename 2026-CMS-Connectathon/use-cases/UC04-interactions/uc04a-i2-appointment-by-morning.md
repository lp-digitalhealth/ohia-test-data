# UC04a-I2: An Appointment by Morning

**Corresponds to:** 2026-07-14, 20:06–20:47.

## What happens

The in-office practice's interim FHIR server receives Dr. Webb's referral within a minute of it being sent — no fax, nothing sitting in an inbox until morning. Within about 40 minutes, their staff has reviewed it and calls Sarah to get her on the schedule for the next morning.

## What Sarah Sees (patient-facing)

📱 **Notification:** *"Appointment confirmed — tomorrow, 10:00 AM."*

## Key resources exchanged in this interaction

- `ServiceRequest` received and acknowledged at the in-office practice
- `Appointment` created, linked back to the referral
- `AppointmentResponse` returned to Dr. Webb's system

## Why this matters for testing

Same `Appointment`/`AppointmentResponse` pattern already proven in UC02 — the test here is whether it holds up cleanly when the *referring* side is a virtual-care platform rather than another in-office PMS, and whether same-evening turnaround (referral to confirmed appointment in under an hour, at 8:47 PM) is actually achievable end to end, not just theoretically fast.

## What's deliberately NOT part of this interaction

The actual evaluation — Sarah hasn't been seen in person yet. That's Interaction 3, the next morning.
