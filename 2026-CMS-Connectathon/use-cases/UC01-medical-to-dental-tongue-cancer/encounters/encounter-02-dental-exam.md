# Encounter #2: Dental Exam & Radiographs, Penn Dental Medicine

**Date:** July 23, 2026, 2:00–3:30 PM
**Setting:** Penn Dental Family Practice, Robert Schattner Center, 240 South 40th Street, Philadelphia, PA 19104
**Clinician:** Dr. Thomas Sollecito, DMD, MMSc (Oral Medicine, Penn Dental Medicine)

## What happens

Dr. Sollecito sees John Smith for the pre-radiation dental clearance evaluation referred by Dr. Galloway at Fox Chase Cancer Center (Encounter #1, July 6). He performs a comprehensive clinical examination and takes two sets of radiographs — a full-arch panoramic survey and targeted periapical views.

The findings fall into three categories:

**Straightforward extractions (finalized same day):**
- **Tooth #4** — periapical lesion is visible on the radiograph; standard extraction indicated before radiation.
- **Tooth #17** — impacted; extraction indicated.

**Decision pending — needs dose data (tooth #30):**
- **Tooth #30** — structurally sound, but Dr. Sollecito notes it sits within the planned high-dose radiation field based on the treatment site described in the referral. Before he can recommend extraction vs. preservation, he needs to know the exact planned dose at that tooth. A dose above 45 Gray (the established osteoradionecrosis risk threshold for this procedure) would require extracting the tooth *before* radiation starts; a lower dose would allow it to stay.

That same afternoon, Dr. Sollecito contacts Dr. Teh Lin (Medical Physicist, Fox Chase Cancer Center) and asks for site-specific dosimetric dental contouring (DDC) data for tooth #30 — the planned radiation dose at that exact anatomical location, extracted from the IMRT treatment plan Dr. Galloway ordered in Encounter #1.

Dr. Lin transmits the answer on July 25: **52 Gy planned at tooth #30**, which exceeds the 45 Gy threshold. Tooth #30 will also require extraction, with an immediate implant placed at the same appointment to preserve the jaw structure before radiation starts.

With all three decisions now finalized, the treatment plan is set:

| Tooth | Finding | Decision |
|---|---|---|
| #4 | Periapical lesion | Extract (July 27) |
| #17 | Impacted | Extract (July 28) |
| #30 | In high-dose field, 52 Gy | Extract + immediate implant (July 29) |

## Why this matters for testing

This encounter exercises three things that Interaction 1 did not:

**1. First reverse-direction bridge transaction (PMS → bridge → EHR)**
In Interaction 1, FCCC's system sent a referral outbound to Penn Dental via the bridge (EHR → bridge → PMS). This encounter is the first time the direction reverses: Penn Dental's PMS generates an interim consultation note and pushes it back through the bridge to FCCC's EHR as an IHE PCC-59 transaction. The FHIR representation of this is the Task update (`in-progress` / `interim-results`) in the Interaction 2 resources. Systems testing the bridge need to confirm they can generate and route an outbound PCC-59, not just receive an inbound PCC-55.

**2. Named LOINC gap for the ODE IG**
The DDC dose data (52 Gy at tooth #30) is a specific kind of clinical data — site-specific planned radiation dose transmitted from an oncology treatment planning system to a dental EHR — for which there is no established LOINC code as of this writing. The test data deliberately leaves this uncoded (text-only `Observation.code`) and documents the gap explicitly. This is a named ODE IG test objective: firms testing this interaction should expect to encounter it and are expected to handle an uncoded Observation gracefully.

**3. Task state machine exercised in both directions**
The referral Task (identifier `REF-2026-UC01-001`) was created in `requested` / `received` state in Interaction 1. After this encounter, it is at `in-progress` / `interim-results`. Systems need to process this state change — surfacing it in FCCC's referral tracking view and in John's patient app — before the extractions begin.

## What this interaction produces

**5 FHIR resources** (see `fhir-resources/uc01-medical-to-dental/interactions/interaction-02/`):

| Resource | File | Description |
|---|---|---|
| Encounter | `encounter-02-dental-exam.json` | The dental exam, July 23, 2:00–3:30 PM |
| DiagnosticReport | `diagnosticreport-periapical.json` | Periapical radiograph (CDT D0220 / LOINC 62443-7) |
| DiagnosticReport | `diagnosticreport-panoramic.json` | Panoramic radiograph (CDT D0330 / LOINC 24828-6) |
| Observation | `observation-tooth30-radiation-dose.json` | 52 Gy at tooth #30 — LOINC gap resource |
| Task (update) | `task-360x-dental-referral-interim.json` | Referral Task at `in-progress` / `interim-results` |

**1 HL7v2 transaction (gap — not yet built):**
The PCC-59 outbound message (Penn Dental's bridge → FCCC's EHR) is documented as a gap. It would live at `hl7v2/uc01-medical-to-dental/interaction-02/` when built.

**Note on the DDC inquiry:** the request from Dr. Sollecito to Dr. Lin is not a standalone FHIR resource. It is captured as a `.note` on the Observation — a legitimate application of the COW IG "Requesting additional information" pattern (see `interactions/README.md` for the full design reasoning). The two-day gap between the exam (July 23) and the dose response (July 25) is intentional; the dose data carries `effectiveDateTime: 2026-07-25` while remaining linked to the exam encounter.

## What's expected to happen next

With all three extractions confirmed, the treatment schedule is:

- **July 27** — Extract tooth #4 (Encounter #3)
- **July 28** — Extract tooth #17 (Encounter #4)
- **July 29** — Extract tooth #30 + immediate implant placement (Encounter #5)
- **July 31** — Dental clearance visit; Dr. Sollecito confirms healing is progressing and issues the formal clearance back to FCCC (Encounter #6, closes the referral loop via PCC-57)
- **August 24** — Revised IMRT start date (Encounter #7)
