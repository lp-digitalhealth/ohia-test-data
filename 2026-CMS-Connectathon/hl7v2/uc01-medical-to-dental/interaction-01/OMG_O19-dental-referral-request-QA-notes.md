# QA Notes — OMG^O19 Dental Referral Request Sample (PCC-55)

## Revision history

This file replaces an earlier version built against `REF^I12^REF_I12` — that message type was **wrong** for this specific implementation. It was sourced from generic IHE 360X documentation rather than the actual bridge contract. After reading `spec/mapping/360x-cow-crosswalk.md` from `lp-digitalhealth/ode-360x-adapter` directly, the correct mapping is:

> **PCC-55 Referral Request → `OMG^O19`** (a General Clinical Order Message), not REF/RRI.

This is the single most important correction from that review — everything below reflects the rebuilt, crosswalk-conformant version.

**Second correction (later same review cycle):** a rebuild of this file accidentally re-introduced an `IN1` (insurance) segment that had already been correctly removed. Caught during QA before finalizing — the message now correctly has no `IN1` segment, matching the crosswalk's confirmation that insurance data lives only in the FHIR `Coverage` resource.

## Verified against primary/authoritative sources

- **Message type**: `OMG^O19^OMG_O19` confirmed as the correct message per the crosswalk's transaction table (Table 1), and independently confirmed as a real, standard HL7 v2.5/2.5.1 "General Clinical Order" message type.
- **Message structure**: `MSH → PID → [PV1] → {AL1} → {ORC → [TQ1/TQ2] → OBR → {NTE} → [CTD] → {DG1} → {OBX...}}` confirmed against HL7 v2.5 chapter 4 abstract message definition. This sample's segment order (MSH, PID, AL1, ORC, OBR, DG1, NTE) is a valid subset.
- **Referral ID location**: crosswalk states explicitly — "On the v2 side it travels in `ORC-2` (placer order number)." This sample carries `REF-2026-UC01-001` in `ORC-2`, matching the same value used in `ServiceRequest.identifier` and `Task.identifier` (system `urn:ohia:referral-id`) on the FHIR side.
- **No `IN1` (insurance) segment**: confirmed correct by *absence* from the crosswalk's segment/element table — coverage/insurance data lives only in the FHIR `Coverage` resource, never in the v2 message. The earlier draft incorrectly included an `IN1` segment; removed.
- **No `RF1`/`PRD` segments**: these belonged to the wrong message type (`REF_I12`) and have been removed entirely.
- **`Task.businessStatus = received`**: crosswalk states "PCC-55 intake stamps `received`" — the FHIR `Task` was corrected from an incorrect `sent` to `received` to match.
- **Cross-reference consistency** (11/11 automated checks pass): referral ID, patient MRN/MBI/DOB, ICD-10 code, penicillin RxNorm code, and the ordering provider's NPI all match exactly between this HL7 message and the Encounter #1 FHIR resources.

## Illustrative / a genuine gap surfaced by this review

- **No discrete field for the receiving clinician (Dr. Sollecito) in `OMG^O19`.** The crosswalk's segment/element table documents `ORC-12` as carrying the *ordering* provider (and, on a later accept message, the *accepting* provider) — but doesn't specify a field for naming the intended receiving clinician on the initial PCC-55 request itself. In this sample, Dr. Sollecito's identity is placed in the free-text `NTE` segment as a workaround, with the receiving *organization* (Penn Dental) implied only by `MSH-5`/`MSH-6`. This is worth raising back to the OHIA/`ode-360x-adapter` maintainers as a possible real gap, rather than something to silently work around in test data going forward.
- **`ORC`/`OBR` field padding** — populated with the key identifying fields (order control, placer order number, provider, service code, dates) but not verified field-by-field against the full v2.5.1 `ORC`/`OBR` data type definitions (each segment has 30+ fields). A real interface should be checked against your trading partner's companion guide.
- **`AL1` severity code (`MO`)** and **`DG1` diagnosis type (`F`)** — plausible per common usage, not independently confirmed against the authoritative HL7 table definitions (same caveat as the prior version of this file).

## What this message intentionally does not carry

Per the crosswalk, the clinical "referral package" (medications, aggregated medication list, structured allergy) lives on the **FHIR side** — `Task.input` referencing `Condition`, `List` (ODEMedicationList), and `AllergyIntolerance` — not embedded as v2 segments beyond the single summary `DG1` and `AL1` included here for referral context. PCC-55 does not carry an attached C-CDA document (unlike PCC-57/59, which explicitly do, per the crosswalk's "+ doc" notation) — so no CDA attachment is modeled in this sample.
