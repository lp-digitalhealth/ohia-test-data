# UC01 Interaction 2 Companion Guide — Dental Exam & DDC Inquiry

**Interaction:** 2 of 4 (UC01)
**Clinical encounter:** Encounter #2 — Dental Exam & Radiographs, July 23, 2026
**Status:** Complete

**How this guide fits with the other documents:**
- Clinical story: [`use-cases/UC01-medical-to-dental-tongue-cancer/encounters/encounter-02-dental-exam.md`](../use-cases/UC01-medical-to-dental-tongue-cancer/encounters/encounter-02-dental-exam.md)
- IG conformance matrix: [`companion-guides/stakeholder-matrix.md`](stakeholder-matrix.md)
- Interaction 1 guide (background + payer setup): [`companion-guides/UC01-companion-guide.md`](UC01-companion-guide.md)
- FHIR resources: [`fhir-resources/uc01-medical-to-dental/interactions/interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/)
- FHIR resources README: [`fhir-resources/uc01-medical-to-dental/interactions/README.md`](../fhir-resources/uc01-medical-to-dental/interactions/README.md)

This guide is **self-contained** — a firm testing only this interaction does not need to have read the Interaction 1 guide first. If you haven't loaded Interaction 1 data, use Path B below.

This guide is **not prescriptive about internal implementation** — it describes what your system needs to be capable of and what to load, not how to build it internally.

---

## 0. Business Overview (read this first — no technical background needed)

Following the referral sent at Encounter #1, John Smith sees Dr. Thomas Sollecito at Penn Dental Medicine on July 23 for the pre-radiation dental evaluation.

**Three teeth need attention before radiation can start:**

- **Tooth #4** — a lesion on the root visible on X-ray. Standard extraction, straightforward decision.
- **Tooth #17** — impacted (buried in the jaw). Extraction required.
- **Tooth #30** — structurally sound, but located in the path of the planned radiation beam. Too much radiation to a tooth before it's been extracted — specifically, more than 45 Gray — dramatically increases the risk of the jaw bone dying later (osteoradionecrosis, ORN). Dr. Sollecito can't make the call without knowing the exact planned dose at that tooth.

Dr. Sollecito contacts FCCC's Medical Physicist, Dr. Teh Lin, and asks for the site-specific dose data. Two days later (July 25), Dr. Lin transmits the answer: **52 Gray at tooth #30** — above the threshold. Tooth #30 gets extracted too, with an immediate implant placed at the same surgery to preserve jaw structure before radiation starts.

**What this interaction tests technically:**
1. **The referral loop now runs in reverse** — Penn Dental's system (PMS) generates an update and the bridge pushes it back to FCCC's EHR. This is called an interim consultation note, or PCC-59 in IHE 360X terminology. Interaction 1 was all inbound (EHR → bridge → PMS); this is the first outbound transaction (PMS → bridge → EHR).
2. **A named data gap surfaces** — there is no established LOINC code for site-specific planned radiation dose at a tooth site. The test data models this intentionally and explicitly. Systems need to handle an uncoded Observation gracefully.
3. **The referral Task advances through its state machine** — from `requested`/`received` (Interaction 1) to `in-progress`/`interim-results` (this interaction). Both FCCC's referral tracking view and John's patient app should reflect this change.

---

## 1. Loading paths

Interaction 2 supports two entry points — choose based on what you've already loaded:

| | Path A — Continue from Interaction 1 | Path B — Start here |
|---|---|---|
| **Prerequisite** | Interaction 1 fully loaded | Nothing — start clean |
| **Bundle to load** | [`interaction-02-delta-bundle.json`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/interaction-02-delta-bundle.json) | [`interaction-02-bundle.json`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/interaction-02-bundle.json) |
| **Resource count** | 5 new resources | 39 total (34 from Interaction 1 + 5 new) |
| **How to load** | POST to `{base}/Bundle` as a transaction | POST to `{base}/Bundle` as a transaction |
| **Verify after loading** | `GET Task/task-360x-dental-referral` → `status: in-progress`, `businessStatus.coding[0].code: interim-results` | Same |

Both paths produce identical server state. The delta bundle uses `PUT` semantics for all 5 entries, so it is safe to load even if you happen to have some of these resources already present (idempotent).

---

## 2. Step-by-step preparation, by stakeholder

### 2a. Dental Technology Providers (bridge + PMS)

This is the primary active role at this interaction. The bridge is the outbound transmitter for the first time.

**Files for this role:**

| File | Path | Why you need it |
|---|---|---|
| `encounter-02-dental-exam.json` | [`fhir-resources/.../interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/encounter-02-dental-exam.json) | The dental exam encounter your PMS generates |
| `diagnosticreport-periapical.json` | [`fhir-resources/.../interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/diagnosticreport-periapical.json) | Periapical radiograph findings |
| `diagnosticreport-panoramic.json` | [`fhir-resources/.../interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/diagnosticreport-panoramic.json) | Panoramic radiograph findings |
| `observation-tooth30-radiation-dose.json` | [`fhir-resources/.../interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/observation-tooth30-radiation-dose.json) | 52 Gy DDC data — note the LOINC gap (text-only code) |
| `task-360x-dental-referral-interim.json` | [`fhir-resources/.../interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/task-360x-dental-referral-interim.json) | Updated Task (`in-progress` / `interim-results`) |
| `interaction-02-delta-bundle.json` or `interaction-02-bundle.json` | [`fhir-resources/.../interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/) | Full transaction bundle for loading |

**Steps:**

1. **Load the bundle** — use Path A or Path B per Section 1. Confirm the transaction response shows 5 successful PUTs (for the delta bundle) or 39 (for the full bundle).

2. **Verify Task state** — `GET Task/task-360x-dental-referral`. Confirm:
   - `status: "in-progress"`
   - `businessStatus.coding[0].code: "interim-results"`
   - `lastModified: "2026-07-23T15:30:00-04:00"`
   - `output` array contains 3 references: `Encounter/encounter-02-dental-exam`, `DiagnosticReport/diagnosticreport-periapical`, `DiagnosticReport/diagnosticreport-panoramic`

3. **PCC-59 outbound capability** — confirm your bridge implementation can:
   - Receive the Task update from the PMS (status change + `Task.output` population)
   - Generate and transmit an outbound PCC-59 (Interim Consultation Note) to FCCC's EHR endpoint
   - **Note:** the PCC-59 HL7v2 wire-level message is not yet built in this test dataset. See `interactions/README.md` for the gap note. Your bridge's PCC-59 generation logic should be testable against the FHIR `Task.output` content regardless.

4. **Handle the uncoded Observation** — `GET Observation/observation-tooth30-radiation-dose`. Confirm your system surfaces the `valueQuantity` (52 Gy) and `interpretation` text without requiring a coded `Observation.code`. This is an intentional ODE IG gap — the test succeeds if the value is surfaced, not if the code is present.

5. **Verify DiagnosticReports are linked to the exam** — both DiagnosticReports should reference `Encounter/encounter-02-dental-exam` in their `encounter` field and `ServiceRequest/servicerequest-dental-referral` is reachable via the Encounter's `basedOn`.

---

### 2b. EHR (Fox Chase Cancer Center)

The EHR receives the PCC-59 state change from the bridge and surfaces it to Dr. Galloway's team.

**Files for this role:**

| File | Path | Why you need it |
|---|---|---|
| `task-360x-dental-referral-interim.json` | [`fhir-resources/.../interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/task-360x-dental-referral-interim.json) | Confirms what the Task looks like after bridge update |
| `diagnosticreport-periapical.json` | [`fhir-resources/.../interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/diagnosticreport-periapical.json) | Interim result visible to FCCC via Task.output |
| `diagnosticreport-panoramic.json` | [`fhir-resources/.../interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/diagnosticreport-panoramic.json) | Interim result visible to FCCC via Task.output |

**Steps:**

1. **Load the bundle** (if not already loaded) — see Section 1, Path A or Path B.

2. **Confirm the bridge update arrives** — after the bridge processes the PCC-59 outbound (Step 3 in 2a above), the EHR should receive and persist the Task state change. `GET Task/task-360x-dental-referral` from the EHR side and verify `status: in-progress` / `businessStatus: interim-results`.

3. **Confirm interim results are surfaced** — the EHR's referral tracking view should surface the two DiagnosticReport references from `Task.output`. Dr. Galloway's team should be able to see that Penn Dental's exam is complete and findings are available, even though formal clearance hasn't been issued yet.

4. **FCCC's FHIR involvement here is limited** — FCCC's EHR does not generate any new FHIR resources at this interaction. Its role is to receive and display the updated Task + DiagnosticReports. The DDC inquiry (Dr. Lin → Dr. Sollecito) is also handled at FCCC, but the dose data flows outbound from FCCC Medical Physics as the Observation resource — if your system hosts the FHIR server, confirm the Observation is queryable at `Observation/observation-tooth30-radiation-dose`.

---

### 2c. Patient-Facing Application

John Smith's app needs to reflect that his dental exam happened and that results are pending (treatment plan not yet finalized as of July 23 — full plan confirmed July 25 when DDC data arrives).

**Files for this role:**

| File | Path | Why you need it |
|---|---|---|
| `task-360x-dental-referral-interim.json` | [`fhir-resources/.../interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/task-360x-dental-referral-interim.json) | The status the patient app reads to show referral progress |

**Steps:**

1. **Load the bundle** — see Section 1.

2. **Confirm `interim-results` status surfaces** — after loading, the patient app should show that the dental referral is `in-progress` and that interim results have been received. The exact label or phrasing is implementation-specific; what matters is that the state change from Interaction 1 (`received`) to Interaction 2 (`interim-results`) is visible to the patient.

3. **Do not surface the DDC dose value to the patient** — the 52 Gy measurement is clinical data for providers. The patient app at this interaction should show "exam complete, treatment plan being finalized" — not raw dosimetric data.

4. **SMART App Launch scopes required** — the patient app reads `Task?patient=Patient/patient-john-smith` (or equivalent). Confirm the launch context and scopes established in your Interaction 1 setup still cover this read.

---

### 2d. Payer Technology Providers

**No action required at this interaction.** The payer (IBX) is not involved in the dental exam, the DDC inquiry, or the PCC-59 bridge transaction. Prior authorization tracking continues from Interaction 1 — the dental clearance status (still pending at this interaction) is relevant to the PA process, but it is not transmitted to the payer at this step.

If you are testing only the payer pathway and want to verify the full end-to-end prior authorization story, you will need Interaction 1 loaded and the final clearance (Interaction 3 or later, not yet built).

---

## 3. Resource index — Interaction 2

All files are in [`fhir-resources/uc01-medical-to-dental/interactions/interaction-02/`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/).

| File | FHIR type | Description |
|---|---|---|
| [`encounter-02-dental-exam.json`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/encounter-02-dental-exam.json) | Encounter | Dental exam, July 23, 2:00–3:30 PM at Penn Dental |
| [`diagnosticreport-periapical.json`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/diagnosticreport-periapical.json) | DiagnosticReport | Periapical radiograph — CDT D0220 / LOINC 62443-7 |
| [`diagnosticreport-panoramic.json`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/diagnosticreport-panoramic.json) | DiagnosticReport | Panoramic radiograph — CDT D0330 / LOINC 24828-6 |
| [`observation-tooth30-radiation-dose.json`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/observation-tooth30-radiation-dose.json) | Observation | 52 Gy at tooth #30 — LOINC gap resource (text-only code) |
| [`task-360x-dental-referral-interim.json`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/task-360x-dental-referral-interim.json) | Task | Referral Task at `in-progress` / `interim-results` — same `id` as Interaction 1, PUT semantics |
| [`interaction-02-delta-bundle.json`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/interaction-02-delta-bundle.json) | Bundle (transaction) | Path A — 5 new resources only |
| [`interaction-02-bundle.json`](../fhir-resources/uc01-medical-to-dental/interactions/interaction-02/interaction-02-bundle.json) | Bundle (transaction) | Path B — 39 total resources (self-contained) |

**Base/registry resources** referenced by the above but not included in the delta bundle — these are present in the full bundle (Path B) and in Interaction 1 (Path A prerequisite):

| Resource | ID | Type |
|---|---|---|
| Patient | `patient-john-smith` | Patient |
| Condition (cancer) | `condition-john-smith-tongue-cancer` | Condition |
| ServiceRequest (referral) | `servicerequest-dental-referral` | ServiceRequest |
| Task (Interaction 1 state) | `task-360x-dental-referral` | Task |
| Practitioner (Dr. Sollecito) | `pract-sollecito` | Practitioner |
| Practitioner (Dr. Lin) | `pract-lin` | Practitioner |
| Organization (Penn Dental) | `org-penndental` | Organization |
| Organization (FCCC) | `org-fccc` | Organization |
| Location (Penn Dental) | `loc-penndental` | Location |

---

## 4. Cross-references and known gaps

**For Interaction 1 background (payer setup, CRD/DTR, initial referral):** see [`companion-guides/UC01-companion-guide.md`](UC01-companion-guide.md).

**For the full list of Interaction 2 FHIR files and design decisions:** see [`fhir-resources/uc01-medical-to-dental/interactions/README.md`](../fhir-resources/uc01-medical-to-dental/interactions/README.md).

**For the clinical narrative:** see [`use-cases/UC01-medical-to-dental-tongue-cancer/encounters/encounter-02-dental-exam.md`](../use-cases/UC01-medical-to-dental-tongue-cancer/encounters/encounter-02-dental-exam.md).

**Known gaps at this interaction:**

| Gap | Location | Impact |
|---|---|---|
| PCC-59 HL7v2 wire-level message not yet built | `hl7v2/uc01-medical-to-dental/interaction-02/` (missing) | Bridge teams cannot validate outbound PCC-59 format against a sample message; test against FHIR Task.output instead |
| LOINC code for site-specific radiation dose at tooth site does not exist | `observation-tooth30-radiation-dose.json`, `Observation.code` (text-only) | Systems must handle an uncoded Observation; this is a named ODE IG test objective, not an error |
| Interaction 3 (formal clearance / PCC-57 close-loop) not yet designed | — | Firms cannot test the complete end-to-end referral loop closure from this data set alone |
