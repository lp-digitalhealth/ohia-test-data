# UC02a-I2: The Handoff to Oral Surgery

**Corresponds to:** 2026-07-14, 14:30–15:05.

## What happens

With the PA number in hand, Dr. Parker's staff sends the referral to Dr. Alex Maxil at Austin Oral Surgery — not a fax, not a phone call, a structured package sent directly into their system: the referral itself, the confirmed diagnosis, and the PA number proving this is already cleared.

**The imaging and charting data doesn't travel the same way UC01's did, and that distinction matters.** UC01 was medical-to-dental, where the medical side has no inbound pull capability — so imaging had to be pushed separately after the fact. This is dental-to-dental. Per the ODE/360X-adapter spec, dental-to-dental referrals use **support-a-pull**: the referral points at where the periapical radiograph and periodontal charting live, and Austin Oral Surgery's system retrieves them via CDex.

**What "retrieves via CDex" actually means, precisely:** the referral carries a FHIR `ImagingStudy` resource — but that resource doesn't contain the image itself, only metadata and a pointer (the DICOM Study Instance UID, and a WADO-RS endpoint address). Austin Oral Surgery's system makes an actual DICOMweb **WADO-RS** call against Dr. Parker's PACS to retrieve the real image data, using that UID. The radiograph itself is, and remains, a DICOM object — FHIR and CDex govern the referral and the pointer; DICOM/WADO-RS is what actually moves the pixels.

Austin Oral Surgery's system receives the referral and the pointers to the imaging, pulls the actual radiograph and charting data, and their scheduling team books Frank for a consultation. Confirmation goes back to Dr. Parker's office within minutes.

## What Frank Sees (patient-facing)

📱 **Notification:** *"Referral sent to Austin Oral Surgery."* — followed shortly after by *"Appointment confirmed with Dr. Maxil — July 21."*

Both notifications fire from this one interaction: the referral send itself, and the appointment confirmation that comes back once Austin Oral Surgery's system has pulled the imaging and scheduled Frank.

## Why this matters for testing

Two things are genuinely being tested here, not one. First, `Appointment`/`AppointmentResponse` as its own resource-bearing pattern — UC01 never formalized scheduling this way. Second, and more centrally to this project's actual purpose: whether the full **CDex → `ImagingStudy` → DICOM/WADO-RS** stack works end to end — can a receiving dental system resolve a FHIR pointer into an actual DICOMweb retrieval against a real PACS, not just receive a pre-bundled file. This is the dental-to-dental imaging pattern this whole project exists to prove out, not incidental detail riding along in "the referral package."

## What's deliberately NOT part of this interaction

The clinical encounter itself — Dr. Maxil hasn't seen Frank yet. That's Interaction 3.
