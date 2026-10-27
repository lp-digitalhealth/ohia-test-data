# UC07 Interaction-Level Materials

Clinician-readable writeups for UC07 (DentaQuest Texas Medicaid dental plan — pediatric-to-general-dentist referral for root canal therapy, build-up, and crown on tooth #4), following the same 5-interaction pattern established for UC01, UC02, and UC03. These files belong in an `interactions/` subfolder alongside the main use case document ([`../UC07-Texas-Medicaid-Pediatric-RootCanal`](../UC07-Texas-Medicaid-Pediatric-RootCanal)). Test data is organized around integration-worthy **interactions**, not a 1:1 map to clinical **encounters** (see `CLAUDE.md` §4).

- **UC07-I1: The Handoff** (`uc07-i1-the-handoff.md`) — evaluation, radiographs, and referral on 2026-07-08; CDex referral push to Dr. Garcia, structured notification to DentaQuest, and DICOMweb image viewing (360X reference + SMART Imaging Access retrieval)
- **UC07-I2: Three Procedures, One Authorization** (`uc07-i2-three-procedures-one-authorization.md`) — CRD → DTR → PAS with ARex attachments for the bundled D3320 + D2950 + D2740 plan (2026-07-09 – 07-15)
- **UC07-I3: Linda Says Yes** (`uc07-i3-linda-says-yes.md`) — consultation, eligibility re-check, guardian consent for a minor, and completed treatment (2026-07-22)
- **UC07-I4: Closing the Loop** (`uc07-i4-closing-the-loop.md`) — CDex post-treatment push to Dr. Parker: summary, post-op radiograph, clinical note, and a separate thank-you note (2026-07-22)
- **UC07-I5: Billing Two Practices** (`uc07-i5-billing-two-practices.md`) — both practices bill DentaQuest via 837D (2026-07-23); the PA number must appear on the restorative claim

## Scope notes

- **Dental-to-dental direction:** imaging uses **support-a-pull** (the referral carries the `ImagingStudy` pointer; the receiver retrieves via WADO-RS), per the standing rule in `CLAUDE.md` §8.
- **Prior authorization uses Da Vinci PAS only.** DentaQuest is the payer throughout (payer type, Payer ID `CX014`, no NPI).
- **No patient-facing notification sections.** Unlike UC01–UC03, the UC07 narrative defines no patient or guardian app, so none is invented here.
- **ARex is a draft/provisional IG** (Onyx Technology, v0.2.0). Attachment delivery in I2 should be read as a pilot of that draft, not settled practice.
- **Open question carried from the narrative:** whether I2's single PAS `Claim` should carry three line items (the narrative's intent) or whether DentaQuest requires per-procedure requests. The test is written to the narrative.

## Build status

Business-terms writeups only. FHIR fixtures for UC07 are not yet built; the resource-by-resource build spec is `UC-Pediatric-RootCanal-FHIR-Build-Data.md`.
