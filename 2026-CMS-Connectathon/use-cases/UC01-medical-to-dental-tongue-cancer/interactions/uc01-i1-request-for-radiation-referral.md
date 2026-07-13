# UC01-I1: Request for Radiation & Referral

**Date:** July 6, 2026, 9:00–10:30 AM
**Setting:** Fox Chase Cancer Center, Head & Neck Radiation Oncology
**Clinician:** Dr. Marcus Whitfield (Radiation Oncology)

## What happens

Dr. Whitfield sees John Smith to place the order for his intensity-modulated radiation therapy (IMRT) — the treatment plan developed by the multidisciplinary team for John's Stage IV squamous cell carcinoma of the tongue.

The moment the order is entered into Dr. Whitfield's EHR, two things happen automatically, without anyone picking up a phone or logging into a payer portal:

1. **The system checks John's insurance in real time.** It confirms that IBX requires prior authorization for IMRT, and — critically — that IBX's coverage policy for this treatment also requires a documented **dental clearance** before authorization will be granted. This isn't a generic rule; it exists because high-dose radiation to the jaw carries a real risk of osteoradionecrosis (bone death from radiation damage), and any dental problems have to be resolved *before* treatment starts, not during.

2. **A referral is generated and sent** to Dr. Andrew Bellweather at Penn Dental Medicine, along with the relevant portions of John's oncology record. The clock starts here: Dr. Bellweather has fewer than 21 days to evaluate John and return a clearance, because the radiation start date is already on the calendar.

## What John Sees (patient-facing)

📱 **Notification:** *"Referral sent to Penn Dental Medicine."*

This is the first of several real-time updates John gets throughout this process without needing to call anyone. Behind the scenes, this fires the moment the referral's tracking record is created — John's app doesn't show him anything about the insurance check or the coverage-requirement logic, just this one plain-language milestone.

## Why this matters for testing

This encounter is the trigger for the entire rest of the use case. Nothing downstream — the dental exam, the extractions, the clearance, the prior authorization approval — can happen unless this encounter correctly:
- Fires the payer's real-time coverage check at the moment of order entry
- Surfaces the dental clearance requirement as an actionable, trackable item (not just a note in a chart)
- Sends a referral that the receiving system (Penn Dental's) can actually act on, and that both organizations can track through to completion — this is the "closed-loop" referral piece, meaning the loop isn't considered closed until Penn Dental has formally accepted and, later, completed it back to FCCC

## What this encounter produces

- The IMRT treatment order itself
- John's cancer diagnosis, formally recorded in context of this visit
- The referral to Penn Dental
- An open, trackable referral-loop record between the two organizations, which won't close until Dr. Bellweather's clearance comes back (see Encounter #6)

## What's expected to happen next

Penn Dental receives and schedules the referral (July 7) — this is the acceptance step in the closed referral loop, which happens outside a formal "encounter" in this use case but is a required system-to-system step before Encounter #2 (the dental exam) can occur on July 23.
