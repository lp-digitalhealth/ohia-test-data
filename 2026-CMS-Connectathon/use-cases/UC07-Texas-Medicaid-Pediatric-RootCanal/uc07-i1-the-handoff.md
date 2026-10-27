# UC07-I1: The Handoff

**Corresponds to:** 2026-07-08, 09:30 (evaluation) through 10:30 (Dr. Garcia reviews the referral and images).

## What happens

Joe Castle, 16, comes to Dr. Mary Parker's pediatric dental practice in Texas with pain when chewing on the upper right and sensitivity to cold. Dr. Parker performs a limited evaluation and takes a periapical and a bitewing radiograph. They show decay that has reached the pulp and a periapical infection on tooth #4, the maxillary right second premolar. The tooth is restorable, so she plans root canal therapy, a build-up, and a crown rather than extraction. That work is outside her practice, so she refers Joe to Dr. Max Garcia, a general dentist.

At 10:15 the referral goes out as a structured package pushed directly into Dr. Garcia's practice: the referral, the diagnosis, clinical notes, the proposed treatment plan, and pointers to the radiographs. One minute later, at 10:16, Dr. Parker's system sends a **structured referral notification to DentaQuest**, Joe's dental plan. It is not a prior authorization and it asks nothing of the plan. It tells DentaQuest that a referral for this treatment is in motion, so the plan has context before the authorization and claims arrive.

**The images do not travel inside the referral.** This is dental-to-dental, so imaging uses **support-a-pull**. The referral carries a FHIR `ImagingStudy` that holds only metadata and a pointer: the DICOM Study Instance UID and a WADO-RS endpoint on Dr. Parker's imaging service. By 10:30, Dr. Garcia opens the referral and his viewer retrieves the actual radiographs from that endpoint, using the access already granted for this referral. He does not log into a separate imaging portal, and he is not looking at compressed copies pasted into a clinical note.

## Why this matters for testing

Three things are tested together:

1. The **360X-style delivery of an imaging reference** inside a CDex provider-to-provider referral.
2. The **SMART Imaging Access retrieval pattern**: can the receiving system resolve `ImagingStudy.endpoint` into a working WADO-RS call, including the `requires-access-token` handshake, and render diagnostic-quality images?
3. The **provider-to-payer notification**: does DentaQuest's endpoint receive it, and can the notification later be associated with the PA request and the claims?

The notification is the least proven of the three. Nothing downstream depends on it for correctness, which is the point. The test is whether payer awareness at referral time is cheap to deliver and useful to have.

## What's deliberately NOT part of this interaction

Coverage requirements, documentation, and prior authorization. Dr. Garcia's office has not yet entered a treatment-plan order, so CRD has not fired. That begins the next business day, in Interaction 2.
