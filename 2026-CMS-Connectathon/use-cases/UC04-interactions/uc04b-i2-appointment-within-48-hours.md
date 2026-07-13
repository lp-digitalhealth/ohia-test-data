# UC04b-I2: An Appointment Within 48 Hours

**Corresponds to:** 2026-07-22, 00:39–08:18.

## What happens

The in-office practice's system receives the referral overnight, one minute after it's sent. Nobody's there at 12:39 AM to act on it — staff reviews it first thing when the office opens and calls Darius at 8:15 to get him in. Texas Medicaid's urgent-access standard requires an appointment within 48 hours; they book him for the next day, well inside that window.

## What Darius Sees (patient-facing)

📱 **Notification:** *"Appointment confirmed."*

## Key resources exchanged in this interaction

- `ServiceRequest` received overnight, acted on the next morning
- `Appointment` created, `AppointmentResponse` returned

## Why this matters for testing

The test here isn't the resource pattern itself — that's proven already — it's timing: can a referral received overnight, outside business hours, still result in an appointment confirmed within the required access window, without anything getting lost in the gap between when it arrives and when someone's actually there to act on it.

## What's deliberately NOT part of this interaction

The evaluation itself — that's the next day, Interaction 3.
