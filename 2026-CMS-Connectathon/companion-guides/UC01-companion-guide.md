# UC01 Companion Guide — Medical-to-Dental Referral (Head & Neck Cancer)

**Status:** Interactions 1–4 are built (FHIR resources); Interaction 1 also has an HL7v2 wire-level message. Each interaction has its own section below — see [`../CLAUDE.md`](../CLAUDE.md) for what's still pending.

**How this guide relates to the other project documents:** [`../use-cases/UC01-medical-to-dental-tongue-cancer/`](../use-cases/UC01-medical-to-dental-tongue-cancer/) tells the clinical story. [`stakeholder-matrix.md`](stakeholder-matrix.md) tells you which IGs apply to which interaction. This guide tells you, step by step, how to actually prepare and load data to test each interaction. [`UC01-readiness-checklist.md`](UC01-readiness-checklist.md) is the conformance checklist to self-assess against once you've prepared.

This guide is intentionally **not prescriptive about internal implementation** — it tells you what your system needs to be capable of and what to load, not how to build it internally.

---

## 0. Business Overview (read this first — no technical background needed)

John Smith is a 63-year-old FCCC oncology patient about to start radiation therapy for tongue cancer. Before radiation can begin, he needs a dental clearance — radiation to the head and neck carries a real risk of bone damage if dental problems aren't addressed first.

**Interaction 1 is the moment his oncologist, Dr. Whitfield, places the radiation order.** The instant that happens, two things fire automatically:

1. **The system checks his insurance** and discovers his radiation treatment requires prior authorization — and that prior authorization requires a documented dental clearance first.
2. **A referral is sent** to Dr. Bellweather at Penn Dental Medicine, starting a clock: he has under three weeks to evaluate John and clear him before the treatment date already on the calendar.

Everything technical in the rest of this guide exists to make those two things happen correctly, automatically, and traceably — no faxes, no phone tag, no lost referrals.

---

## 1. Which IGs apply to Interaction 1

Per [`stakeholder-matrix.md`](stakeholder-matrix.md): **CRD, DTR, SMART App Launch, IHE 360X, and ODE are required. CARIN Blue Button and Provider Access API are not required at this interaction.**

Two pathways, no shared FHIR dependency between them:

- **Pathway A (Request for Treatment):** entirely FHIR-based. Payer exposes CRD/DTR; EHR fires CDS Hooks and launches DTR via SMART.
- **Pathway B (Referral):** EHR side is HL7v2/C-CDA only — **no FHIR**. The bridge is the only system that speaks both HL7v2 and FHIR. PMS side is FHIR only.

---

## 2. Step-by-step preparation, by stakeholder

### 2a. Payer Technology Providers

**Files for this role:**

| File | Why you need it |
|---|---|
| [`insplan-ibx-pc65ppo.json`](../fhir-resources/durable/insurance-plans/insplan-ibx-pc65ppo.json) | Load onto your FHIR server — the plan record CRD evaluates against |
| [`plandef-ibx-imrt-pa-rule.json`](../fhir-resources/durable/payer-rules/plan-definitions/plandef-ibx-imrt-pa-rule.json) | Load onto your FHIR server — CRD entry point |
| [`lib-ibx-imrt-pa-logic.json`](../fhir-resources/durable/payer-rules/libraries/lib-ibx-imrt-pa-logic.json) | Load onto your FHIR server — CQL logic referenced by the PlanDefinition |
| [`questionnaire-ibx-imrt-pa-dtr.json`](../fhir-resources/durable/payer-rules/questionnaires/questionnaire-ibx-imrt-pa-dtr.json) | Load onto your FHIR server — served to DTR on launch |
| [`cds-hooks-discovery-ibx.json`](../fhir-resources/durable/cds-hooks/cds-hooks-discovery-ibx.json) | Reference shape for your `/cds-services` discovery document |

1. Load registry resources onto your FHIR server: [`insplan-ibx-pc65ppo.json`](../fhir-resources/durable/insurance-plans/insplan-ibx-pc65ppo.json), [`plandef-ibx-imrt-pa-rule.json`](../fhir-resources/durable/payer-rules/plan-definitions/plandef-ibx-imrt-pa-rule.json), [`lib-ibx-imrt-pa-logic.json`](../fhir-resources/durable/payer-rules/libraries/lib-ibx-imrt-pa-logic.json), [`questionnaire-ibx-imrt-pa-dtr.json`](../fhir-resources/durable/payer-rules/questionnaires/questionnaire-ibx-imrt-pa-dtr.json).
2. Expose a CDS Hooks discovery document at `{your-base-url}/cds-services` matching the content of [`cds-hooks-discovery-ibx.json`](../fhir-resources/durable/cds-hooks/cds-hooks-discovery-ibx.json) — critically, the hook is **`order-sign`**, not `order-select`.
3. Confirm your CDS service evaluates an incoming `ServiceRequest` (IMRT, CPT 77301/77338) against the `Coverage` referenced and returns a card indicating prior authorization is required, directing the requester to launch DTR.
4. Confirm your DTR endpoint serves the `Questionnaire` correctly when launched.
5. You do not need 360X, HL7v2, or C-CDA capability for this interaction — that's the EHR/bridge's concern, not yours.

### 2b. Dental Technology Providers (bridge + PMS)

**Files for this role:**

| File | Why you need it |
|---|---|
| [`OMG_O19-dental-referral-request.hl7`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request.hl7) | Input: the HL7v2 message your bridge must ingest |
| [`OMG_O19-dental-referral-request-QA-notes.md`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request-QA-notes.md) | Read first — field-by-field notes on referral ID placement, no `IN1` segment, corrections applied |
| [`servicerequest-dental-referral.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/servicerequest-dental-referral.json) | Expected bridge output: `ODEMedicalToDentalReferral` ServiceRequest |
| [`task-360x-dental-referral.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/task-360x-dental-referral.json) | Expected bridge output: `ODEReferralTask` with `businessStatus: received` |
| [`provenance-dental-referral.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/provenance-dental-referral.json) | Expected bridge output: Provenance (required in bundle — easy to miss) |
| [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/interaction-01-bundle.json) | Full expected output bundle — validate your bridge's FHIR translation against this |

1. Stand up (or configure) the `ode-360x-adapter` bridge, or your own equivalent implementing the same `FhirBackend`/`IheCodec`/`IheOutboundTransport` port contracts.
2. Confirm your bridge can ingest an `OMG^O19` message matching [`OMG_O19-dental-referral-request.hl7`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request.hl7) — read [`OMG_O19-dental-referral-request-QA-notes.md`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request-QA-notes.md) first, since it documents exact field placement (referral ID in `ORC-2`/`OBR-2`, no `IN1` segment, etc.).
3. Confirm your bridge translates that message into a FHIR bundle matching the referral-related resources in [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/interaction-01-bundle.json) — directional `ServiceRequest` (profile `ode-medical-to-dental-referral`), `ODEReferralTask` (`businessStatus: received` on intake), `Condition`, medication `List`/`AllergyIntolerance`, `Provenance`.
4. Load the resulting bundle onto your PMS-side FHIR server (or the server your PMS reads from).
5. As you do this, note any real-world PMS constraints that don't fit the ODE IG's current shape — this feedback loop is part of your role per the stakeholder matrix, not just executing the spec as given.

### 2c. EHR Technology Providers (or EHR stub)

**Files for this role:**

| File | Why you need it |
|---|---|
| [`patient-john-smith.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/patients/patient-john-smith.json) | Load into your system — subject of the IMRT order |
| [`coverage-john-smith.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/coverage/coverage-john-smith.json) | Load into your system — evaluated by CRD when the order fires |
| [`servicerequest-imrt-order.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/servicerequest-imrt-order.json) | Reference shape for the IMRT order that triggers the `order-sign` CDS Hooks call |
| [`OMG_O19-dental-referral-request.hl7`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request.hl7) | The HL7v2 message your system sends to the bridge — no FHIR production needed for this pathway |

1. Load [`patient-john-smith.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/patients/patient-john-smith.json) and [`coverage-john-smith.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/coverage/coverage-john-smith.json) so the order has a subject and coverage to evaluate.
2. Place the IMRT order (shape: [`servicerequest-imrt-order.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/servicerequest-imrt-order.json)) in your system — this should fire the `order-sign` CDS Hooks call to the payer.
3. Confirm the returned card is handled and DTR is launched via SMART App Launch, in patient/encounter context.
4. Separately, send the referral as an `OMG^O19` HL7v2 message (see [`OMG_O19-dental-referral-request.hl7`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request.hl7)) to the bridge — **this is HL7v2/C-CDA only; you do not need to produce any FHIR resources for this pathway.**
5. If you're standing up a stub rather than a real EHR, see Section 3 below for the minimum bar.

### 2d. Patient-Facing App Providers

**See also:** the consolidated "Patient-Facing App Companion Guide" section below (after Interaction 1, before Interaction 2) — it covers the full milestone-by-milestone picture across all interactions, not just this one.

**Files for this role:**

| File | Why you need it |
|---|---|
| [`task-360x-dental-referral.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/task-360x-dental-referral.json) | The resource your app queries for referral status — `Task.businessStatus` = `received` after Interaction 1 |

1. You are last in the dependency chain — Payer, EHR, and Bridge/PMS all need to be functioning (or realistically stubbed, per Section 3) before you can meaningfully test.
2. For Interaction 1, you do not need CARIN Blue Button or Provider Access API — those aren't exercised until later interactions.
3. You do need standard Patient Access API support (SMART App Launch + US Core) against the EHR, to pull John's clinical context.
4. Referral/appointment status display: query the bridge/PMS for `Task.businessStatus` on the referral (expect `received` immediately after Interaction 1). **Note:** the exact patient-facing profile for this is an open question (see [`stakeholder-matrix.md`](stakeholder-matrix.md) open items) — build against `Task.businessStatus` directly for now, since no ODE-specific patient-facing profile has been confirmed to exist yet.

---

## 3. Stub Specifications

If you don't have a live partner system to test against, here's the minimum your stub needs to expose for each role. A stub only needs to satisfy the *other* stakeholders' dependencies on it (per the dependency chain in [`stakeholder-matrix.md`](stakeholder-matrix.md): Payer+EHR → Bridge → PMS → Patient App) — it doesn't need real clinical logic behind it.

**EHR stub** (if you're testing the bridge, payer, or PMS without a real EHR):
- Must be able to send an `OMG^O19` HL7v2 message matching the shape in [`OMG_O19-dental-referral-request.hl7`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request.hl7)
- Must be able to receive and display a CDS Hooks card (doesn't need real UI — logging the response is sufficient for Connectathon testing)
- Does NOT need to produce any FHIR resources itself

**Bridge/PMS stub** (if you're testing the EHR or Patient App without a real bridge/PMS):
- Must accept the `OMG^O19` message and respond with at least a positive ACK
- Must be able to serve back a FHIR bundle resembling [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/interaction-01-bundle.json)'s referral-related resources (`ServiceRequest`, `Task`, `Condition`, medication `List`, `AllergyIntolerance`, `Provenance`) so downstream systems have something real to query
- Task `businessStatus` should be settable to `received` at minimum, to test the Patient App's status display

**Payer stub** (if you're testing the EHR, bridge, or Patient App without a real payer):
- Must expose a `/cds-services` discovery document listing an `order-sign` service (see [`cds-hooks-discovery-ibx.json`](../fhir-resources/durable/cds-hooks/cds-hooks-discovery-ibx.json) for the shape)
- Must return a card indicating PA is required and DTR should launch, when queried with an IMRT-coded `ServiceRequest`
- Must be able to serve the DTR `Questionnaire` ([`questionnaire-ibx-imrt-pa-dtr.json`](../fhir-resources/durable/payer-rules/questionnaires/questionnaire-ibx-imrt-pa-dtr.json))
- Does NOT need real adjudication logic — a fixed "yes, PA required" response is sufficient for Interaction 1 testing

**Patient App stub** — not typically needed by other stakeholders (Patient App is last in the dependency chain and nothing depends on it), but if you want a placeholder to demo against: any UI that can display a referral status string is sufficient.

---

## 4. Resource Index — all test data files for Interaction 1

Every file needed for Interaction 1 is listed here. Load order: Registry → Base → Interaction 1, or use the [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/interaction-01-bundle.json) shortcut to load all three tiers at once.

### Registry — [`../fhir-resources/durable/`](../fhir-resources/durable/) — load first; shared across use cases

| File | Type | Purpose |
|---|---|---|
| [`org-fccc.json`](../fhir-resources/durable/organizations/org-fccc.json) | Organization | Fox Chase Cancer Center |
| [`org-ibx.json`](../fhir-resources/durable/organizations/org-ibx.json) | Organization | Independence Blue Cross (payer) |
| [`org-penndental.json`](../fhir-resources/durable/organizations/org-penndental.json) | Organization | Penn Dental Medicine (receiving dental practice) |
| [`pract-whitfield.json`](../fhir-resources/durable/practitioners/pract-whitfield.json) | Practitioner | Dr. Whitfield — referring oncologist at FCCC |
| [`pract-nandakumar.json`](../fhir-resources/durable/practitioners/pract-nandakumar.json) | Practitioner | Dr. Nandakumar — FCCC radiation oncology |
| [`pract-osei.json`](../fhir-resources/durable/practitioners/pract-osei.json) | Practitioner | Dr. Osei — FCCC |
| [`pract-bellweather.json`](../fhir-resources/durable/practitioners/pract-bellweather.json) | Practitioner | Dr. Bellweather — receiving dentist at Penn Dental |
| [`loc-fccc-radonc.json`](../fhir-resources/durable/locations/loc-fccc-radonc.json) | Location | FCCC Radiation Oncology |
| [`loc-penndental.json`](../fhir-resources/durable/locations/loc-penndental.json) | Location | Penn Dental Medicine |
| [`endpoint-fccc.json`](../fhir-resources/durable/endpoints/endpoint-fccc.json) | Endpoint | FCCC FHIR server endpoint |
| [`endpoint-ibx.json`](../fhir-resources/durable/endpoints/endpoint-ibx.json) | Endpoint | IBX payer FHIR endpoint |
| [`endpoint-penndental.json`](../fhir-resources/durable/endpoints/endpoint-penndental.json) | Endpoint | Penn Dental FHIR endpoint |
| [`insplan-ibx-pc65ppo.json`](../fhir-resources/durable/insurance-plans/insplan-ibx-pc65ppo.json) | InsurancePlan | IBX PC65 PPO — John's insurance plan |
| [`plandef-ibx-imrt-pa-rule.json`](../fhir-resources/durable/payer-rules/plan-definitions/plandef-ibx-imrt-pa-rule.json) | PlanDefinition | IBX IMRT prior auth rule — CRD entry point |
| [`lib-ibx-imrt-pa-logic.json`](../fhir-resources/durable/payer-rules/libraries/lib-ibx-imrt-pa-logic.json) | Library | CQL logic for IMRT prior auth evaluation |
| [`questionnaire-ibx-imrt-pa-dtr.json`](../fhir-resources/durable/payer-rules/questionnaires/questionnaire-ibx-imrt-pa-dtr.json) | Questionnaire | DTR questionnaire for IMRT prior auth |
| [`cds-hooks-discovery-ibx.json`](../fhir-resources/durable/cds-hooks/cds-hooks-discovery-ibx.json) | CDS Hooks config *(not a FHIR resource)* | IBX payer's `order-sign` CDS service discovery document |

### Base — [`../fhir-resources/purpose-built/uc01-medical-to-dental/base/`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/) — load second; UC01-specific

| File | Type | Purpose |
|---|---|---|
| [`patient-john-smith.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/patients/patient-john-smith.json) | Patient | John Smith — UC01 patient |
| [`coverage-john-smith.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/coverage/coverage-john-smith.json) | Coverage | John's IBX PC65 PPO coverage |
| [`consent-john-smith-hie.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/consent/consent-john-smith-hie.json) | Consent | John's HIE data-sharing consent |
| [`role-whitfield.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/practitioner-roles/role-whitfield.json) | PractitionerRole | Dr. Whitfield's role at FCCC Radiation Oncology |
| [`role-nandakumar.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/practitioner-roles/role-nandakumar.json) | PractitionerRole | Dr. Nandakumar's role at FCCC |
| [`role-osei.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/practitioner-roles/role-osei.json) | PractitionerRole | Dr. Osei's role at FCCC |
| [`role-bellweather.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/practitioner-roles/role-bellweather.json) | PractitionerRole | Dr. Bellweather's role at Penn Dental |
| [`subscription-john-smith-referral-status.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/subscriptions/subscription-john-smith-referral-status.json) | Subscription | John's patient app subscription to referral status changes (Backport IG) — spans the whole use case, not one interaction; retroactively added, see [`../CLAUDE.md`](../CLAUDE.md) |

### Interaction 1 — [`../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/) — load third

| File | Type | Purpose |
|---|---|---|
| [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/interaction-01-bundle.json) | Transaction bundle | **Shortcut: all 35 resources (all three tiers) in one `POST`** |
| [`encounter-01-imrt-order.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/encounter-01-imrt-order.json) | Encounter | The oncology visit on 2026-07-06 |
| [`condition-john-smith-tongue-cancer.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/condition-john-smith-tongue-cancer.json) | Condition | Tongue cancer diagnosis (ICD-10-CM C02.1) |
| [`servicerequest-imrt-order.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/servicerequest-imrt-order.json) | ServiceRequest | IMRT radiation therapy order — fires CRD at `order-sign` |
| [`servicerequest-dental-referral.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/servicerequest-dental-referral.json) | ServiceRequest (ODEMedicalToDentalReferral) | Dental clearance referral to Dr. Bellweather at Penn Dental |
| [`task-360x-dental-referral.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/task-360x-dental-referral.json) | Task (ODEReferralTask) | 360X referral tracking task; `businessStatus: received` on intake |
| [`provenance-dental-referral.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/provenance-dental-referral.json) | Provenance | Authorship/transmitter record for the referral bundle |
| [`allergyintolerance-john-smith-penicillin.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/allergyintolerance-john-smith-penicillin.json) | AllergyIntolerance | Penicillin allergy (RxNorm 7980) — in referral `supportingInfo` |
| [`list-john-smith-medications.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/list-john-smith-medications.json) | List (ODEMedicationList) | Active medication list — in referral `supportingInfo` |
| [`medrequest-john-smith-lisinopril.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/medrequest-john-smith-lisinopril.json) | MedicationRequest | Lisinopril |
| [`medrequest-john-smith-atorvastatin.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/medrequest-john-smith-atorvastatin.json) | MedicationRequest | Atorvastatin |
| [`medrequest-john-smith-oxycodone-apap.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/medrequest-john-smith-oxycodone-apap.json) | MedicationRequest | Oxycodone/acetaminophen |

### HL7v2 — [`../hl7v2/uc01-medical-to-dental/interaction-01/`](../hl7v2/uc01-medical-to-dental/interaction-01/)

| File | Type | Purpose |
|---|---|---|
| [`OMG_O19-dental-referral-request.hl7`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request.hl7) | HL7v2 PCC-55 | Wire-level referral request (`OMG^O19`) sent by EHR to bridge |
| [`OMG_O19-dental-referral-request-QA-notes.md`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request-QA-notes.md) | QA notes | Field-by-field verification notes — **read before modifying the `.hl7` file** |

---

## 5. Loading order

Registry → base → encounter-specific, since later tiers reference earlier ones:

| Step | Directory | Key files | Notes |
|---|---|---|---|
| 1 | [`../fhir-resources/durable/`](../fhir-resources/durable/) | Organizations, Practitioners, Locations, Endpoints, InsurancePlan, payer-rules (PlanDefinition, Library, Questionnaire), cds-hooks | Shared across use cases — load once |
| 2 | [`../fhir-resources/purpose-built/uc01-medical-to-dental/base/`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/) | Patient, Coverage, Consent, PractitionerRole ×4, Subscription | UC01-specific; referenced by all UC01 interactions |
| 3 | [`../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/) | Encounter, Condition, ServiceRequests, Task, Provenance, meds, allergy | Interaction-specific |

**Shortcut:** `POST` [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/interaction-01-bundle.json) to `[base]/` — it pre-bundles all 35 resources from all three tiers in the correct order.

---

## 6. HL7v2 — what you need to actually run it

The [`OMG_O19-dental-referral-request.hl7`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request.hl7) file is plain pipe-delimited text — readable in any text editor, no special software needed just to look at one. But to validate, transmit, or programmatically process it the way a real interface would, you need one of the following, depending on your role:

**To parse/validate structure only** (e.g., if you're the bridge or EHR checking field positions):
A library, not a full application — HAPI HL7v2 (Java), Python's `hl7` or `hl7apy`, or .NET's NHapi. This is sufficient for confirming the message matches the shape documented in [`OMG_O19-dental-referral-request-QA-notes.md`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request-QA-notes.md).

**To actually transmit/receive it like a real interface** (e.g., EHR sending to the bridge):
HL7v2 traditionally moves over **MLLP** (a simple TCP wrapper — start block `\x0b`, end block `\x1c\r`) around the raw message. An interface engine — **Mirth Connect / NextGen Connect** (free, open-source, common for Connectathon testing), Rhapsody, or Cloverleaf — is the standard tool for sending/receiving MLLP and inspecting messages visually. If you're standing up an EHR stub per Section 3, this is likely the easiest path to actually send our sample message somewhere.

**If you're testing against the real `ode-360x-adapter` bridge specifically:** Per its `ARCHITECTURE.md`, the bridge has its own internal HL7v2 parser (`hl7v2.py`) — you don't need separate HL7v2 software to *be* the bridge. You do need to feed it through whichever transport plugin it's configured with: `json-envelope` for the default test harness, or `direct`/`xdm-zip` if testing real Direct/XDM transport.

**If you just want to sanity-check the message quickly** without setting up an interface engine: a lightweight online validator (e.g., Caristix's HL7 validator, or "HL7 Inspector") will parse a pasted message into segments/fields visually — useful for a one-off check, not for actual transmission testing.

---

## 7. FHIR services — what you need to actually run them

Unlike the `.hl7` files, the `.json` FHIR resources in `fhir-resources/` aren't meant to be read standalone — they need to be **loaded onto a FHIR server** to be queried, referenced, or evaluated (e.g., for CRD to evaluate a `PlanDefinition` against a `ServiceRequest`, both need to actually be sitting on a server, not just sitting as files).

**To stand up a FHIR server to load these onto:**
- **HAPI FHIR** (Java, open-source) — the most common choice for Connectathon testing; runs standalone or via Docker, supports R4 out of the box, has a built-in web UI for browsing loaded resources.
- **OnyxOS** — referenced directly in `ode-360x-adapter`'s `ARCHITECTURE.md` as one of its built-in `FhirBackend` plugins; if you're testing against the real bridge, confirm which backend it's configured with.
- Any FHIR R4-conformant server works in principle — the resources here don't depend on server-specific features.

**To load the resources:**
- Each file is a standalone resource with a fixed `id` — load with `PUT [base]/{ResourceType}/{id}` per the load order in Section 5, or load [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/interaction-01-bundle.json) as a single `POST` transaction to `[base]/`.
- Any HTTP client works for this — `curl`, Postman, Insomnia. No FHIR-specific tool required just to load data.

**To validate conformance** (not just "does it load," but "does it actually match the declared profile"):
- The **official HL7 FHIR Validator CLI** (Java, `validator_cli.jar`) — checks a resource against its `meta.profile` declaration. This is the right tool to confirm, e.g., that our `ServiceRequest` genuinely conforms to `ode-medical-to-dental-referral`, not just that it's well-formed JSON.
- **Inferno** (ONC's official testing tool) — for validating conformance to certification-relevant IGs specifically (US Core, SMART App Launch, Patient Access API). More relevant to EHR/Payer Tech providers than to loading test data.
- What we did ourselves while building this library was structural/cross-reference validation only (JSON parses, identifiers match across resources) — not full profile validation against the actual StructureDefinitions. Worth running the resources through the official validator before the Connectathon if strict IG conformance will be checked there.

**To fire CDS Hooks / test the CRD-DTR pathway specifically:**
- No special software beyond an HTTP client — CDS Hooks is just HTTP POST requests with a defined JSON shape. Useful for manually testing a payer's `order-sign` service without needing a real EHR: `POST {payer-base}/cds-services/{service-id}` with a hook context payload.

---

## 8. Patient-facing apps — credentials and OAuth setup

Patient-facing apps are the one stakeholder type in this use case that requires **registering real credentials** before they can connect to anything — this isn't optional tooling, it's a required setup step.

**What's needed:**
- **SMART App Launch registration** with each FHIR server the app connects to (EHR for clinical data, Payer for CARIN Blue Button/claims data) — this means registering your app and receiving a **client ID** (and, for confidential clients, a **client secret**) from each server operator before the Connectathon, not something you can generate yourself.
- **Redirect URI(s)** registered in advance — the OAuth2 authorization server will reject a callback to an unregistered URI, so this needs to be settled before testing, not discovered mid-session.
- **Scopes** — request only what's needed for this use case: patient-level clinical read scopes (`patient/*.read` or more specific `patient/Observation.read` etc. per US Core) for the EHR side, and CARIN Blue Button-defined scopes for the payer side. Over-scoping can itself cause a conformance failure in some test harnesses.

**Where to get these for Connectathon testing specifically:**
- Check with FCCC's (or IBX's) Connectathon coordinator for sandbox client registration — production credentials should never be used for Connectathon testing, and most Da Vinci/US Core reference sandboxes (e.g., a HAPI FHIR test server with a SMART launcher in front of it) have a self-service registration flow for exactly this purpose.
- The **SMART Health IT sandbox launcher** (`launch.smarthealthit.org`) is a commonly used public reference implementation for testing a patient app's OAuth flow without needing a real EHR's credential system at all — useful if FCCC's actual sandbox isn't ready yet.

**Credential handling — a real caution, not boilerplate:** Even in a test/Connectathon context, treat client secrets like real secrets — don't commit them to this repo or any shared test-data repository. If a stub or sandbox needs a secret checked in for convenience, use an obviously fake placeholder value and note in-line that it's a placeholder, not a working credential.

**If you're testing without real registered credentials yet:** Per the Stub Specifications in Section 3, a Patient App stub only needs to display a referral status string — it doesn't need working OAuth at all for that minimal bar. Full Patient Access API testing does require real registration, though, so budget time for that setup ahead of the Connectathon rather than assuming it can happen same-day.

---

## 9. What to do if something doesn't match

If a resource in `../fhir-resources/` or the HL7v2 message doesn't match what your system expects, check [`../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/README.md`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/README.md) and [`OMG_O19-dental-referral-request-QA-notes.md`](../hl7v2/uc01-medical-to-dental/interaction-01/OMG_O19-dental-referral-request-QA-notes.md) first — several corrections were already made during this project (wrong SNOMED/NUCC/HL7 codes, a wrong message type, a wrong CDS Hooks trigger name) and are documented there. If it's a genuinely new discrepancy, that's useful Connectathon feedback — flag it rather than silently working around it.

---

## Patient-Facing App Companion Guide (spans all interactions)

Unlike the Payer, EHR, and Dental Tech tracks — whose actions genuinely differ interaction by interaction — the patient-facing app does fundamentally the **same thing** throughout: subscribe once, then receive and display milestone notifications as the referral progresses. This section is consolidated in one place for that reason, rather than repeated (and previously, only partially repeated) across each interaction's section.

### What to build

1. **A `Subscription`** to the referral's status changes — matching the shape of [`subscription-john-smith-referral-status.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/subscriptions/subscription-john-smith-referral-status.json) (in [`../fhir-resources/purpose-built/uc01-medical-to-dental/base/subscriptions/`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/subscriptions/)). This is built once, early (conceptually alongside Interaction 1, since the app should be subscribed before the referral even starts generating status changes), not re-created per interaction.
2. **A notification handler** that receives `SubscriptionStatus` payloads (per the HL7 FHIR Subscriptions R4 Backport IG this project follows) and translates the underlying `Task.status`/`businessStatus` values into plain-language milestones for John — he should never see raw FHIR codes.
3. **Standard Patient Access API support** (SMART App Launch + US Core) to pull John's actual clinical data from FCCC — this is a separate capability from the Subscription/notification piece, and is covered in Section 8 below (credentials/OAuth setup), not repeated here.

### Milestone-by-milestone: what the app should show, and what's actually driving it

| When | What John sees | What's actually happening (Task field) |
|---|---|---|
| Interaction 1 (2026-07-06) | "Referral sent to Penn Dental" | `Task.status: requested`, `businessStatus: received` |
| Between 1 and 2 (2026-07-07, not its own interaction) | "Appointment scheduled" | `Task.status: accepted`→`in-progress`, `owner` set (not yet built as its own artifact — see Interaction 2's gap note) |
| Interaction 2 (2026-07-23) | "Dr. Bellweather is reviewing your case" | `Task.status: in-progress` |
| Interaction 2, DDC inquiry / extension request | **Nothing new should display.** These are provider-to-provider notes, not patient-visible events — confirm your app correctly does *not* surface every backend note as a patient notification. | N/A — no Task status change from these specifically |
| Interaction 3 (2026-07-31) | "Clearance sent to your cancer care team" | `Task.status: completed`, `businessStatus: outcome-final` |
| Interaction 4 (2026-08-03) | "Prior authorization approved" | Confirmed: [`eob-imrt-priorauth-ppa.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-04/eob-imrt-priorauth-ppa.json) (Da Vinci PDex PPA profile, `use: preauthorization`), delivered via CARIN Blue Button — **not** the same referral `Task`/Subscription as every other row above. If your app only listens to the referral Subscription, it will miss this milestone; confirm you also query or subscribe to PA-status data separately. |

**The one thing worth testing deliberately:** whether your app can tell the difference between a Task change that should generate a patient-visible notification (every row above except the DDC/extension row) and backend activity that shouldn't (that row). Getting this wrong in either direction — missing a real milestone, or spamming John with internal provider chatter — is a real failure mode this use case is designed to surface.

### Credentials and stubs

See Section 8 (FHIR services / Patient-facing app credentials, below) for OAuth/SMART registration, and the Stub Specifications (Section 3) for the minimal bar if you're testing without a live upstream system — a Patient App stub only needs to display a referral status string; it doesn't need working OAuth for that minimal bar.

---

## Interaction 2: Dental Exam & Requests for Additional Information

**Status:** built (FHIR resources), including the Task update that was previously flagged as a gap. No HL7v2/wire-level artifact for this interaction by design — this interaction is pure FHIR-side Task/note activity, not a new 360X transaction.

This section comes in **two parts**, because a firm might approach Interaction 2 in either of two ways: continuing straight on from Interaction 1 (most firms), or picking up here directly without having executed Interaction 1 themselves (e.g., a firm testing only the dental-side exam/finding-request pathway).

### Part A — If you're continuing directly from Interaction 1

You already have everything loaded (registry, base, Interaction 1's 35 resources). What's new for Interaction 2:

1. **Accept the referral.** The existing `Task/task-360x-dental-referral` is updated (same `id`, new version — [`task-360x-dental-referral-interim.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-02/task-360x-dental-referral-interim.json)): `status` → `in-progress`, `businessStatus` → `in-progress`, and — for the first time — `Task.owner` is set to the accepting party (Dr. Bellweather's `PractitionerRole`). Per the crosswalk, this is the correct point for `owner` to first appear — not at intake (Interaction 1).
2. **The exam happens.** The same Task update reflects the exam occurring (2026-07-23) — `Task.output` references the exam `Encounter` and both `DiagnosticReport`s.
3. **Load the exam content.** [`encounter-02-dental-exam.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-02/encounter-02-dental-exam.json), the two `DiagnosticReport`s, and the dose `Observation`.
3. **Capture the two information requests as notes** — the DDC dose inquiry (reflected in the `Observation`'s `.note`) and the treatment-extension request (still not yet built as a discrete resource — see gap note below). Neither is a new order or referral resource; both are the COW "Requesting additional information" pattern.
4. **No new HL7v2 message.** Nothing here crosses the wire as a new 360X transaction — the Task update is a FHIR-side state change the bridge would reflect internally, not a fresh PCC-55-style message.

### Part B — If you're starting fresh at Interaction 2 (didn't execute Interaction 1 yourself)

You need Interaction 1's output loaded as **prerequisite state**, not as something you're testing — the exam only makes sense if a referral already exists and has been sent.

1. Load the full registry ([`../fhir-resources/durable/`](../fhir-resources/durable/)) and base tier ([`../fhir-resources/purpose-built/uc01-medical-to-dental/base/`](../fhir-resources/purpose-built/uc01-medical-to-dental/base/)), exactly as Interaction 1 requires.
2. Load Interaction 1's resources as-is ([`../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/), or the [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-01/interaction-01-bundle.json) shortcut) — treat this as a fixture, not a test target. You are not validating Interaction 1's referral-sending behavior; you're just establishing that a referral exists and was received.
3. From there, follow Part A above.
4. If you want to skip building/loading Interaction 1 entirely and just need *a* referral + Task to hang the exam content off of, the [`interaction-02-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-02/interaction-02-bundle.json) shortcut already includes everything from both Interaction 1 and Interaction 2 pre-bundled — load that single file instead of assembling it yourself.

### Patient-Facing App

See the consolidated "Patient-Facing App Companion Guide" section above (spans all interactions) — no interaction-specific patient-app work here beyond what's already covered there.

### Which IGs apply

Same core set as Interaction 1 (IHE 360X for the underlying referral state; ODE for the FHIR resources) — no CRD/DTR activity in this interaction (that was Interaction 1 only), and no CARIN Blue Button/Provider Access API yet.

### Resource Index

| File | Type | Purpose |
|---|---|---|
| [`encounter-02-dental-exam.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-02/encounter-02-dental-exam.json) | Encounter | The dental exam visit |
| [`diagnosticreport-periapical.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-02/diagnosticreport-periapical.json) | DiagnosticReport | CDT D0220 / LOINC 62443-7 |
| [`diagnosticreport-panoramic.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-02/diagnosticreport-panoramic.json) | DiagnosticReport | CDT D0330 / LOINC 24828-6 |
| [`observation-tooth30-radiation-dose.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-02/observation-tooth30-radiation-dose.json) | Observation | 52 Gy dose at tooth #30; carries the DDC-request note; LOINC-gap resource |
| [`task-360x-dental-referral-interim.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-02/task-360x-dental-referral-interim.json) | Task (updated version) | `businessStatus` → `in-progress`, `Task.owner` set, `Task.output` populated — fills a previously-flagged gap |
| [`interaction-02-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-02/interaction-02-bundle.json) | Transaction bundle | Shortcut: all 40 resources (Interaction 1 + Interaction 2) in one `POST` |
| [`interaction-02-delta-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-02/interaction-02-delta-bundle.json) | Transaction bundle | Lightweight alternative: just this interaction's own 5 new/updated resources |
| *(not yet built)* | — | Treatment-extension request note + updated `ServiceRequest.occurrenceDateTime` on the IMRT order — **gap, needs building** (this is the later, early-August moment described in the interaction writeup) |

### Stub Specifications

No new stub requirements beyond Interaction 1's — a Bridge/PMS stub for this interaction additionally needs to accept a Task status update (not just initial creation) and be able to attach `Observation`/`DiagnosticReport` content to an existing referral context.

### What to do if something doesn't match

Same as Interaction 1's guidance (Section 9 above) — check the interactions README and any QA notes first; if it's new, that's real feedback, not a mistake to quietly work around.

---

## Interaction 3: The Clearance

**Status:** built (FHIR resources), rigorous QA performed. Corresponds to clinical Encounter #6 (2026-07-31).

**Wire-level transaction:** IHE 360X **PCC-57 (Referral Outcome)** — `OMG^O19` + C-CDA Consultation Note.

### Part A — If you're continuing directly from Interaction 2

1. **Load the clinical outcome resources**: 3 `Procedure`s (extractions #4, #17; extraction+implant #30 — CDT-coded D7210/D6010, confirmed real codes), a coded disposition `Observation` (text-only — see terminology caution below), and the `ClinicalImpression` (the clearance attestation, also text-only for its assessment code).
2. **Load the `DocumentReference`** representing the C-CDA Consultation Note component of the PCC-57 transaction (LOINC `11488-4`, verified).
3. **Load the final Task snapshot** ([`task-360x-dental-referral-completed.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/task-360x-dental-referral-completed.json)) — same `id` as the Task from Interaction 1, but now `status: completed`, `businessStatus: outcome-final`, `owner` set (Dr. Bellweather's `PractitionerRole` — populated here for the first time in a built resource, since the PCC-56 accept step itself isn't separately modeled), and `output` populated with all of the above.
4. **Load the final ServiceRequest snapshot** ([`servicerequest-dental-referral-completed.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/servicerequest-dental-referral-completed.json)) — same `id`, `status: completed`.

### Part B — If you're starting fresh at Interaction 3

You need Interactions 1 and 2's output loaded as prerequisite state (the referral must exist and the exam/dose-finding must already have happened for the clearance to make sense). Either:
- Load registry + base + Interaction 1 + Interaction 2 first, then follow Part A, or
- Use the [`interaction-03-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/interaction-03-bundle.json) shortcut, which pre-bundles all 48 resources (registry + base + all three interactions) in correct temporal order — the two Task/ServiceRequest versions are both included, sequentially, so the final `PUT` correctly represents the completed state.

### Patient-Facing App

See the consolidated "Patient-Facing App Companion Guide" section (before Interaction 2, spans all interactions) — this interaction corresponds to the "Clearance sent to your cancer care team" milestone row in that section's table.

### ⚠️ Terminology caution — read before using this interaction's codes elsewhere

During QA, the use case's own "SNOMED CT Clinical Codes" reference table was found to contain at least one confirmed-invalid code (wrong format) and several more that couldn't be verified via general web search. **All SNOMED codes originally planned for this interaction's `Procedure`, `Observation`, and `ClinicalImpression` resources are represented as text-only (no `coding`) in the actual built files**, pending verification against a real SNOMED terminology browser. Do not assume these concepts have no valid code — only that we haven't confirmed one. See the use case doc's Section 6 for the full caution and which specific codes are affected.

### Resource Index

| File | Type | Purpose |
|---|---|---|
| [`procedure-extraction-tooth4.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/procedure-extraction-tooth4.json) | Procedure | CDT D7210 |
| [`procedure-extraction-tooth17.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/procedure-extraction-tooth17.json) | Procedure | CDT D7210 |
| [`procedure-extraction-implant-tooth30.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/procedure-extraction-implant-tooth30.json) | Procedure | CDT D7210 + D6010 |
| [`observation-dental-clearance-disposition.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/observation-dental-clearance-disposition.json) | Observation | Text-only disposition code |
| [`clinicalimpression-dental-clearance.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/clinicalimpression-dental-clearance.json) | ClinicalImpression | The clearance attestation |
| [`documentreference-dental-clearance-note.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/documentreference-dental-clearance-note.json) | DocumentReference | C-CDA Consultation Note wrapper, LOINC 11488-4 |
| [`servicerequest-dental-referral-completed.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/servicerequest-dental-referral-completed.json) | ServiceRequest (snapshot) | Same id as Interaction 1's, `status: completed` |
| [`task-360x-dental-referral-completed.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/task-360x-dental-referral-completed.json) | Task (snapshot) | Same id as Interaction 1's, final version |
| [`interaction-03-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-03/interaction-03-bundle.json) | Transaction bundle | Shortcut: all 48 resources, correct temporal order |

### What to do if something doesn't match

Same as Interaction 1 (Section 9) — plus, for terminology specifically, see the caution above rather than assuming the text-only codes are a mistake.

---

## Interaction 4: Ending the Prior Authorization

**Status:** built (FHIR resources). Corresponds to the PA submission/approval cycle, 2026-08-01 through 2026-08-03 — not tied to a single clinical encounter, since this is billing-office activity, not a patient visit.

**Standards used:** Da Vinci PAS (`Claim`/`ClaimResponse`, `use: preauthorization`) for the request/response cycle itself; Da Vinci CDex for the dental clearance attachment; Da Vinci PDex PPA profile + CARIN Blue Button for the patient-facing delivery. **PAS replaces X12 278 entirely** — 278 is not exercised anywhere in this use case.

### Part A — If you're continuing directly from Interaction 3

1. **Load the PA request.** [`claim-imrt-priorauth.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-04/claim-imrt-priorauth.json) — `use: preauthorization`, for the IMRT/radiation service specifically (CPT 77301/77338, the same planning codes as Interaction 1's original order — **not** a claim for Dr. Bellweather's dental procedures). `supportingInfo` references the dental clearance `ClinicalImpression` and the DTR `Questionnaire` as evidence the prerequisite is satisfied.
2. **Load the approval.** [`claimresponse-imrt-priorauth.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-04/claimresponse-imrt-priorauth.json) — `outcome: complete`, `disposition: Approved`, `preAuthRef`/`preAuthPeriod` populated. No line-item adjudication is included — the header-level fields alone convey the decision, since this is non-financial.
3. **Load the patient-facing record.** [`eob-imrt-priorauth-ppa.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-04/eob-imrt-priorauth-ppa.json) — PDex PPA profile, delivered to John's app via the same milestone-notification pattern as every prior interaction, but sourced from IBX's payer-side systems directly rather than the referral `Task`.

### Part B — If you're starting fresh at Interaction 4

You need the referral (Interaction 1) and the completed clearance (Interaction 3) loaded as prerequisite state — this PA request only makes sense if a dental clearance already exists to attach as evidence. Either load Interactions 1 and 3 individually first, or use the [`interaction-04-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-04/interaction-04-bundle.json) shortcut, which pre-bundles all 51 resources (registry + base + all four interactions) in correct temporal order.

### Patient-Facing App

See the consolidated "Patient-Facing App Companion Guide" section above — its milestone table has been updated to reflect this interaction as built, not speculative. This interaction is the one exception to that section's general pattern: every prior milestone came from the referral `Task`'s `Subscription`; this one — *"Prior authorization approved"* — comes from IBX's payer system directly via PDex PPA, not from the same Task-based Subscription. If your app only listens to the referral Subscription, it will miss this milestone entirely; confirm your app also queries or subscribes to PA-status data separately.

### ⚠️ Scope caution — what this interaction does NOT include

This is a **prior authorization** decision only. It is not a bill and does not authorize or reference Dr. Bellweather's dental procedures as a billable service — those are supporting evidence, not the subject of the request. The actual **reimbursement** billing (837P for FCCC's IMRT delivery, 837P for Dr. Bellweather's medically-billed dental procedures, 835 remittance for both) is explicitly out of scope for this use case as built — mentioned in the source use case document only as real-world context. That reimbursement step is where this project's separately-designed claims-sharing profile (`ODEOralProfessionalEOB`, drafted as a proposed ODE interface extension) would eventually apply — future work, not this interaction.

### Resource Index

| File | Type | Purpose |
|---|---|---|
| [`claim-imrt-priorauth.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-04/claim-imrt-priorauth.json) | Claim (PAS) | PA request for IMRT — CPT 77301/77338, dental clearance as supporting evidence |
| [`claimresponse-imrt-priorauth.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-04/claimresponse-imrt-priorauth.json) | ClaimResponse (PAS) | IBX's approval — `preAuthRef`, `preAuthPeriod` |
| [`eob-imrt-priorauth-ppa.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-04/eob-imrt-priorauth-ppa.json) | ExplanationOfBenefit (PDex PPA) | Patient-facing PA status, delivered via CARIN Blue Button |
| [`interaction-04-bundle.json`](../fhir-resources/purpose-built/uc01-medical-to-dental/interactions/interaction-04/interaction-04-bundle.json) | Transaction bundle | Shortcut: all 51 resources (registry + base + all four interactions), correct temporal order |

### What to do if something doesn't match

Same as Interaction 1 (Section 9). One thing specific to this interaction: if your system expects an X12 278 anywhere in this flow, that's a mismatch with this use case's design, not a bug in the resources — 278 is explicitly out of scope, replaced entirely by PAS's `Claim`/`ClaimResponse`.
