# UC02b — Interaction 2: Referral Receipt & Scheduling

**Corresponds to:** 2026-07-08, 11:00–11:35.

## What happens

Austin Oral Surgery's system receives Dr. Parker's referral — carrying both treatment options and confirmation that no PA is needed. As with UC02a, the imaging isn't bundled into the referral itself: this is a dental-to-dental exchange, so it uses **support-a-pull** — the referral carries a FHIR `ImagingStudy` resource pointing at the actual radiograph (DICOM Study Instance UID and a WADO-RS endpoint), and Austin Oral Surgery's system makes a real DICOMweb **WADO-RS** call against Dr. Parker's PACS to retrieve the periapical radiograph and periodontal charting. FHIR/CDex govern the referral and the pointer; DICOM/WADO-RS is what actually moves the image data.

Once the imaging is retrieved, their scheduling team books Frank for a consultation. Confirmation goes back to Dr. Parker's office within minutes.

## What Frank Sees (patient-facing)

📱 **Notification:** *"Appointment confirmed with Dr. Maxil — July 15."*

## Why this matters for testing

Structurally identical to UC02a's Interaction 2 — same `Appointment`/`AppointmentResponse` pattern, same organizations, same CDex → `ImagingStudy` → DICOM/WADO-RS imaging stack. Worth keeping as its own interaction here too rather than merging into Interaction 1, for consistency with UC02a and because the referral in this case genuinely does carry more complexity (two treatment options, not one) — worth confirming both the DICOMweb retrieval and the scheduling step handle that correctly.

## What's deliberately NOT part of this interaction

The treatment decision itself and the procedure — Interaction 3.
