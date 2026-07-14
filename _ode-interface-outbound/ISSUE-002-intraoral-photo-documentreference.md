# ODE Interface Issue 002 — Patient-submitted intraoral photo: DocumentReference profile + R4 tooth-correlation pattern

> **Delivery note (read first):** This is a **standalone draft**, NOT part of the `ohia-test-data` repository. Per `CLAUDE.md` Section 5a, ODE interface gaps target the **`lp-digitalhealth/ohia-fhirr4-scratchpad`** repo (the ODE-native REST interface contract, `interfaces/openapi.yaml`) and its running **`ODE-INTERFACE-ISSUES-LOG.md`** — they are delivered separately to that repo's maintainers, not committed into `ohia-test-data`. This file lives at the repo root under `_ode-interface-outbound/` only so it isn't swept into a commit of the `2026-CMS-Connectathon/` test-data tree. Append this as **Issue 002** to that log (Issue 001 was the Encounter/DiagnosticReport/Observation gap). We have **no write access** to the target repo — this is a draft for its maintainers.

**Status:** Open — proposed
**Raised by:** UC04a (commercial teledentistry referral), Interaction 1 build
**Affected artifact:** ODE-native REST interface (`ohia-fhirr4-scratchpad/interfaces/openapi.yaml`), the ODE IG under development

---

## Summary

UC04a is the project's first **teledentistry** use case. Its originating provider is a virtual-care platform with **no radiograph capability**, but real teledentistry platforms (teledentistry.com/MESH, TheTeleDentists, Dentistry.One) center on **patient-submitted intraoral photographs** captured on a phone. So UC04a-I1 exchanges a **non-radiographic, patient-authored clinical image** with the dental-to-dental referral. Modeling this against the current ODE interface surfaced three gaps that are expected to recur in any teledentistry or patient-mediated-image scenario (UC04b, and likely UC05).

The photo is modeled — deliberately — as a **US Core `DocumentReference`** (inline `image/jpeg`, `author` = Patient), **not** an R4 `Media`. That choice is itself the crux of the issue: it's correct for ODE's constraints but leaves a structured-data gap (tooth correlation) that the interface should specify rather than leave to each implementer.

## Why `DocumentReference`, not `Media` (context for the recommendation)

- **ONC mandates FHIR R4 and is expected to skip R5, moving to R6.** `Media` is **removed** in R5 and stays removed in R6; `DocumentReference` exists in R4 **and** R6. A `Media`-based artifact is a guaranteed future rewrite; `DocumentReference` is stable across the path ODE must actually travel.
- **US Core profiles `DocumentReference` (and CDex uses it); there is no US Core `Media` profile.** A `Media`-based image is valid-but-non-conformant R4 in a US Core ecosystem.
- **Through a 360X/C-CDA bridge, the image bytes survive either way** as embedded multimedia. `Media`'s one native advantage — the affected tooth on the image via `Media.bodySite` — is exactly the structured detail that flattens crossing into C-CDA, so choosing `DocumentReference` loses nothing there.

## The gaps

### Gap A — No ODE profile for a patient-submitted intraoral photo `DocumentReference`

The interface has no profile describing a non-DICOM, patient-authored oral photograph: expected `category` (clinical photography), `type` (a photographic-image code — UC04a used LOINC `72170-4` "Photographic image"), `content.attachment.contentType` (`image/jpeg`), inline `data` vs. `url`/`Binary`, `author` = `Patient`, and `context.encounter` → the virtual encounter. Without a profile, every teledentistry implementer invents this shape differently.

**Proposed fix:** add an `ODEIntraoralPhotoDocumentReference` profile (or constrain `us-core-documentreference`) covering the above, explicitly distinguished from the DICOM radiograph path (`ImagingStudy` + WADO-RS), which is a different artifact that appears only at the in-office visit.

### Gap B — R4 tooth correlation: `DocumentReference` has no `bodySite`

R4 `DocumentReference` has **no `bodySite` element**, so "which tooth is this photo of?" cannot be carried on the resource itself. UC04a's work-around: a symptom **`Observation`** carries `bodySite` = tooth #19 (ADA Universal) and `derivedFrom` → the photo `DocumentReference`, so a receiver re-associates the image to the tooth off the Observation.

**Proposed fix:** the ODE IG should **specify this correlation pattern normatively** (`Observation.bodySite` + `Observation.derivedFrom` → the image) as the R4 way to bind an oral image to a tooth, so it isn't reinvented per implementer. (Note: this is also the pattern that survives the C-CDA bridge — the tooth persists as a coded `Observation` entry even though it can't live on the image.)

### Gap C — The patient-device → platform upload hop has no HL7 IG

Three transport hops exist for a teledentistry image: (1) **patient mobile/web app → teledentistry platform** (the upload), (2) **platform → dental PMS** (CDex provider-to-provider — governed), (3) **PMS chart correlation/reuse** (Gaps A/B). Hop (1) — the patient-write path — has **no governing HL7 IG**: who may write, provenance (`author` = Patient/Device), and consent are unspecified.

**Proposed fix:** ODE could specify the patient-write path — a `POST` for patient-authored clinical images with `Provenance` (`author` = Patient or the capturing `Device`) — as the ODE-native equivalent of the platform ingest step, independent of any bridge.

### Gap D (documentation) — 360X/C-CDA lossiness, expected and specific

When this crosses a 360X/C-CDA bridge: the **photo bytes survive** as embedded multimedia, but the **tooth correlation survives only as the coded `Observation`** (Gap B), not attached to the image. This is expected behavior worth documenting so implementers don't treat the loss of on-image body-site as a bug.

## Traceability

- **UC04a-I1 resources:** `documentreference-intraoral-photos.json` (the photo), `observation-symptoms.json` (`bodySite` tooth #19 + `derivedFrom` → the photo), `servicerequest-referral.json` (`supportingInfo` → the photo).
- **Companion guide:** `companion-guides/UC04a-companion-guide.md` (header standards note + Section 6b "the intraoral-photo hop").
- **Expected recurrence:** UC04b (Medicaid teledentistry, same photo pattern) and likely UC05.
