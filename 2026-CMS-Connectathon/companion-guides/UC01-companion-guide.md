# UC01 Companion Guide — Medical-to-Dental Referral (Head & Neck Cancer)

**Status:** Encounter #1 only. Encounters #2–7 will be added to this same file as they're designed — see `CLAUDE.md` for what's still pending.

**How this guide relates to the other project documents:** `use-cases/UC01-medical-to-dental-tongue-cancer/` tells the clinical story. `companion-guides/stakeholder-matrix.md` tells you which IGs apply to which encounter. This guide tells you, step by step, how to actually prepare and load data to test Encounter #1. `companion-guides/UC01-readiness-checklist.md` is the conformance checklist to self-assess against once you've prepared.

This guide is intentionally **not prescriptive about internal implementation** — it tells you what your system needs to be capable of and what to load, not how to build it internally.

---

## 0. Business Overview (read this first — no technical background needed)

John Smith is a 63-year-old FCCC oncology patient about to start radiation therapy for tongue cancer. Before radiation can begin, he needs a dental clearance — radiation to the head and neck carries a real risk of bone damage if dental problems aren't addressed first.

**Encounter #1 is the moment his oncologist, Dr. Galloway, places the radiation order.** The instant that happens, two things fire automatically:

1. **The system checks his insurance** and discovers his radiation treatment requires prior authorization — and that prior authorization requires a documented dental clearance first.
2. **A referral is sent** to Dr. Sollecito at Penn Dental Medicine, starting a clock: he has under three weeks to evaluate John and clear him before the treatment date already on the calendar.

Everything technical in the rest of this guide exists to make those two things happen correctly, automatically, and traceably — no faxes, no phone tag, no lost referrals.

---

## 1. Which IGs apply to Encounter #1

Per `stakeholder-matrix.md`: **CRD, DTR, SMART App Launch, IHE 360X, and ODE are required. CARIN Blue Button and Provider Access API are not required at this encounter.**

Two pathways, no shared FHIR dependency between them:

- **Pathway A (Request for Treatment):** entirely FHIR-based. Payer exposes CRD/DTR; EHR fires CDS Hooks and launches DTR via SMART.
- **Pathway B (Referral):** EHR side is HL7v2/C-CDA only — **no FHIR**. The bridge is the only system that speaks both HL7v2 and FHIR. PMS side is FHIR only.

---

## 2. Stub Specifications

If you don't have a live partner system to test against, here's the minimum your stub needs to expose for each role. A stub only needs to satisfy the *other* stakeholders' dependencies on it (per the dependency chain in `stakeholder-matrix.md`: Payer+EHR → Bridge → PMS → Patient App) — it doesn't need real clinical logic behind it.

**EHR stub** (if you're testing the bridge, payer, or PMS without a real EHR):
- Must be able to send a `OMG^O19` HL7v2 message matching the shape in `hl7v2/uc01-medical-to-dental/encounter-01/OMG_O19-dental-referral-request.hl7`
- Must be able to receive and display a CDS Hooks card (doesn't need real UI — logging the response is sufficient for Connectathon testing)
- Does NOT need to produce any FHIR resources itself

**Bridge/PMS stub** (if you're testing the EHR or Patient App without a real bridge/PMS):
- Must accept the `OMG^O19` message and respond with at least a positive ACK
- Must be able to serve back a FHIR bundle resembling `fhir-resources/uc01-medical-to-dental/encounters/encounter-01/encounter-01-bundle.json`'s referral-related resources (`ServiceRequest`, `Task`, `Condition`, medication `List`, `AllergyIntolerance`, `Provenance`) so downstream systems have something real to query
- Task `businessStatus` should be settable to `received` at minimum, to test the Patient App's status display

**Payer stub** (if you're testing the EHR, bridge, or Patient App without a real payer):
- Must expose a `/cds-services` discovery document listing an `order-sign` service (see `fhir-resources/uc01-medical-to-dental/encounters/encounter-01/cds-hooks-discovery-ibx.json` for the shape)
- Must return a card indicating PA is required and DTR should launch, when queried with an IMRT-coded `ServiceRequest`
- Must be able to serve the DTR `Questionnaire` (`fhir-resources/common/payer-rules/questionnaires/questionnaire-ibx-imrt-pa-dtr.json`)
- Does NOT need real adjudication logic — a fixed "yes, PA required" response is sufficient for Encounter #1 testing

**Patient App stub** — not typically needed by other stakeholders (Patient App is last in the dependency chain and nothing depends on it), but if you want a placeholder to demo against: any UI that can display a referral status string is sufficient.

---

## 3. Step-by-step preparation, by stakeholder

### 3a. Payer Technology Providers

1. Load registry resources onto your FHIR server: `fhir-resources/common/insurance-plans/insplan-ibx-pc65ppo.json`, `common/payer-rules/plan-definitions/plandef-ibx-imrt-pa-rule.json`, `common/payer-rules/libraries/lib-ibx-imrt-pa-logic.json`, `common/payer-rules/questionnaires/questionnaire-ibx-imrt-pa-dtr.json`.
2. Expose a CDS Hooks discovery document at `{your-base-url}/cds-services` matching the content of `cds-hooks-discovery-ibx.json` — critically, the hook is **`order-sign`**, not `order-select`.
3. Confirm your CDS service evaluates an incoming `ServiceRequest` (IMRT, CPT 77301/77338) against the `Coverage` referenced and returns a card indicating prior authorization is required, directing the requester to launch DTR.
4. Confirm your DTR endpoint serves the `Questionnaire` correctly when launched.
5. You do not need 360X, HL7v2, or C-CDA capability for this encounter — that's the EHR/bridge's concern, not yours.

### 3b. Dental Technology Providers (bridge + PMS)

1. Stand up (or configure) the `ode-360x-adapter` bridge, or your own equivalent implementing the same `FhirBackend`/`IheCodec`/`IheOutboundTransport` port contracts.
2. Confirm your bridge can ingest an `OMG^O19` message matching `hl7v2/uc01-medical-to-dental/encounter-01/OMG_O19-dental-referral-request.hl7` — read the accompanying QA notes file first, since it documents exact field placement (referral ID in `ORC-2`/`OBR-2`, no `IN1` segment, etc.).
3. Confirm your bridge translates that message into a FHIR bundle matching the referral-related resources in `encounter-01-bundle.json` — directional `ServiceRequest` (profile `ode-medical-to-dental-referral`), `ODEReferralTask` (`businessStatus: received` on intake), `Condition`, medication `List`/`AllergyIntolerance`, `Provenance`.
4. Load the resulting bundle onto your PMS-side FHIR server (or the server your PMS reads from).
5. As you do this, note any real-world PMS constraints that don't fit the ODE IG's current shape — this feedback loop is part of your role per the stakeholder matrix, not just executing the spec as given.

### 3c. EHR Technology Providers (or EHR stub)

1. Load `fhir-resources/uc01-medical-to-dental/base/patients/patient-john-smith.json` and `base/coverage/coverage-john-smith.json` so the order has a subject and coverage to evaluate.
2. Place the IMRT order (shape: `servicerequest-imrt-order.json`) in your system — this should fire the `order-sign` CDS Hooks call to the payer.
3. Confirm the returned card is handled and DTR is launched via SMART App Launch, in patient/encounter context.
4. Separately, send the referral as an `OMG^O19` HL7v2 message (see `hl7v2/.../OMG_O19-dental-referral-request.hl7`) to the bridge — **this is HL7v2/C-CDA only; you do not need to produce any FHIR resources for this pathway.**
5. If you're standing up a stub rather than a real EHR, see Section 2 above for the minimum bar.

### 3d. Patient-Facing App Providers

1. You are last in the dependency chain — Payer, EHR, and Bridge/PMS all need to be functioning (or realistically stubbed, per Section 2) before you can meaningfully test.
2. For Encounter #1, you do not need CARIN Blue Button or Provider Access API — those aren't exercised until later encounters.
3. You do need standard Patient Access API support (SMART App Launch + US Core) against the EHR, to pull John's clinical context.
4. Referral/appointment status display: query the bridge/PMS for `Task.businessStatus` on the referral (expect `received` immediately after Encounter #1). **Note:** the exact patient-facing profile for this is an open question (see `stakeholder-matrix.md` open items) — build against `Task.businessStatus` directly for now, since no ODE-specific patient-facing profile has been confirmed to exist yet.

---

## 4. Loading order

Registry → base → encounter-specific, since later tiers reference earlier ones:

```
1. fhir-resources/common/                                    (Organizations, Practitioners, Locations, InsurancePlan, Endpoints, payer-rules)
2. fhir-resources/uc01-medical-to-dental/base/                (Patient, Coverage, Consent, PractitionerRole)
3. fhir-resources/uc01-medical-to-dental/encounters/encounter-01/   (Encounter, Condition, ServiceRequests, Task, Provenance, meds, allergy)
```

Or load `encounter-01-bundle.json` in one transaction call — it's pre-ordered.

---

## 5. HL7v2 — what you need to actually run it

The `.hl7` files in this repo (e.g., `hl7v2/uc01-medical-to-dental/encounter-01/OMG_O19-dental-referral-request.hl7`) are plain pipe-delimited text — readable in any text editor, no special software needed just to look at one. But to validate, transmit, or programmatically process it the way a real interface would, you need one of the following, depending on your role:

**To parse/validate structure only** (e.g., if you're the bridge or EHR checking field positions):
A library, not a full application — HAPI HL7v2 (Java), Python's `hl7` or `hl7apy`, or .NET's NHapi. This is sufficient for confirming the message matches the shape documented in the accompanying QA notes file.

**To actually transmit/receive it like a real interface** (e.g., EHR sending to the bridge):
HL7v2 traditionally moves over **MLLP** (a simple TCP wrapper — start block `\x0b`, end block `\x1c\r`) around the raw message. An interface engine — **Mirth Connect / NextGen Connect** (free, open-source, common for Connectathon testing), Rhapsody, or Cloverleaf — is the standard tool for sending/receiving MLLP and inspecting messages visually. If you're standing up an EHR stub per Section 2, this is likely the easiest path to actually send our sample message somewhere.

**If you're testing against the real `ode-360x-adapter` bridge specifically:**
Per its `ARCHITECTURE.md`, the bridge has its own internal HL7v2 parser (`hl7v2.py`) — you don't need separate HL7v2 software to *be* the bridge. You do need to feed it through whichever transport plugin it's configured with: `json-envelope` for the default test harness, or `direct`/`xdm-zip` if testing real Direct/XDM transport.

**If you just want to sanity-check the message quickly** without setting up an interface engine: a lightweight online validator (e.g., Caristix's HL7 validator, or "HL7 Inspector") will parse a pasted message into segments/fields visually — useful for a one-off check, not for actual transmission testing.

---

## 6. FHIR services — what you need to actually run them

Unlike the `.hl7` files, the `.json` FHIR resources in `fhir-resources/` aren't meant to be read standalone — they need to be **loaded onto a FHIR server** to be queried, referenced, or evaluated (e.g., for CRD to evaluate a `PlanDefinition` against a `ServiceRequest`, both need to actually be sitting on a server, not just sitting as files).

**To stand up a FHIR server to load these onto:**
- **HAPI FHIR** (Java, open-source) — the most common choice for Connectathon testing; runs standalone or via Docker, supports R4 out of the box, has a built-in web UI for browsing loaded resources.
- **OnyxOS** — referenced directly in `ode-360x-adapter`'s `ARCHITECTURE.md` as one of its built-in `FhirBackend` plugins; if you're testing against the real bridge, confirm which backend it's configured with.
- Any FHIR R4-conformant server works in principle — the resources here don't depend on server-specific features.

**To load the resources:**
- Each file is a standalone resource with a fixed `id` — load with `PUT [base]/{ResourceType}/{id}` per the load order in Section 4, or load `encounter-01-bundle.json` as a single `POST` transaction to `[base]/`.
- Any HTTP client works for this — `curl`, Postman, Insomnia. No FHIR-specific tool required just to load data.

**To validate conformance** (not just "does it load," but "does it actually match the declared profile"):
- The **official HL7 FHIR Validator CLI** (Java, `validator_cli.jar`) — checks a resource against its `meta.profile` declaration. This is the right tool to confirm, e.g., that our `ServiceRequest` genuinely conforms to `ode-medical-to-dental-referral`, not just that it's well-formed JSON.
- **Inferno** (ONC's official testing tool) — for validating conformance to certification-relevant IGs specifically (US Core, SMART App Launch, Patient Access API). More relevant to EHR/Payer Tech providers than to loading test data.
- What we did ourselves while building this library was structural/cross-reference validation only (JSON parses, identifiers match across resources) — not full profile validation against the actual StructureDefinitions. Worth running the resources through the official validator before the Connectathon if strict IG conformance will be checked there.

**To fire CDS Hooks / test the CRD-DTR pathway specifically:**
- No special software beyond an HTTP client — CDS Hooks is just HTTP POST requests with a defined JSON shape. Useful for manually testing a payer's `order-sign` service without needing a real EHR: `POST {payer-base}/cds-services/{service-id}` with a hook context payload.

---

## 7. Patient-facing apps — credentials and OAuth setup

Patient-facing apps are the one stakeholder type in this use case that requires **registering real credentials** before they can connect to anything — this isn't optional tooling, it's a required setup step.

**What's needed:**
- **SMART App Launch registration** with each FHIR server the app connects to (EHR for clinical data, Payer for CARIN Blue Button/claims data) — this means registering your app and receiving a **client ID** (and, for confidential clients, a **client secret**) from each server operator before the Connectathon, not something you can generate yourself.
- **Redirect URI(s)** registered in advance — the OAuth2 authorization server will reject a callback to an unregistered URI, so this needs to be settled before testing, not discovered mid-session.
- **Scopes** — request only what's needed for this use case: patient-level clinical read scopes (`patient/*.read` or more specific `patient/Observation.read` etc. per US Core) for the EHR side, and CARIN Blue Button-defined scopes for the payer side. Over-scoping can itself cause a conformance failure in some test harnesses.

**Where to get these for Connectathon testing specifically:**
- Check with FCCC's (or IBX's) Connectathon coordinator for sandbox client registration — production credentials should never be used for Connectathon testing, and most Da Vinci/US Core reference sandboxes (e.g., a HAPI FHIR test server with a SMART launcher in front of it) have a self-service registration flow for exactly this purpose.
- The **SMART Health IT sandbox launcher** (`launch.smarthealthit.org`) is a commonly used public reference implementation for testing a patient app's OAuth flow without needing a real EHR's credential system at all — useful if FCCC's actual sandbox isn't ready yet.

**Credential handling — a real caution, not boilerplate:**
Even in a test/Connectathon context, treat client secrets like real secrets — don't commit them to this repo or any shared test-data repository. If a stub or sandbox needs a secret checked in for convenience, use an obviously fake placeholder value and note in-line that it's a placeholder, not a working credential.

**If you're testing without real registered credentials yet:**
Per the Stub Specifications in Section 2, a Patient App stub only needs to display a referral status string — it doesn't need working OAuth at all for that minimal bar. Full Patient Access API testing does require real registration, though, so budget time for that setup ahead of the Connectathon rather than assuming it can happen same-day.

---

## 8. What to do if something doesn't match

If a resource in `fhir-resources/` or the HL7v2 message doesn't match what your system expects, check `fhir-resources/uc01-medical-to-dental/encounters/README.md` and the HL7v2 QA notes file first — several corrections were already made during this project (wrong SNOMED/NUCC/HL7 codes, a wrong message type, a wrong CDS Hooks trigger name) and are documented there. If it's a genuinely new discrepancy, that's useful Connectathon feedback — flag it rather than silently working around it.
