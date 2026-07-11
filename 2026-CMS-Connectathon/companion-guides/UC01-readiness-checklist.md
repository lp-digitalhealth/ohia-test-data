# UC01 Readiness Checklist

Organized encounter by encounter, since different systems carry different responsibilities at different points in the workflow — a single role-based list (e.g. "everything the EHR needs to support") blurs together things that only apply at specific moments. Encounter #1 is fully broken out below; Encounters #2–7 will follow the same pattern once built.

This is a **separate, standalone checklist** from the companion guide (which will cover the clinical workflow narrative). This checklist is about technical conformance readiness — what each system needs to support to actually execute the encounter.

---

## Encounter #1: IMRT Order & Referral

This encounter has **two distinct technical pathways that must not be conflated** — they use different protocols, run through different systems, and have no shared FHIR dependency between them at this encounter.

### Pathway A — Request for Treatment (Coverage Check)

**Payer (IBX) must support:**
- [ ] **CRD** (Da Vinci Coverage Requirements Discovery) — a CDS Hooks service responding to the `order-sign` hook (not `order-select`), evaluating `PlanDefinition/plandef-ibx-imrt-pa-rule` against the incoming order + `Coverage`
- [ ] **DTR** (Da Vinci Documentation Templates and Rules) — hosting/serving `Questionnaire/questionnaire-ibx-imrt-pa-dtr` for the ordering system to launch and complete

**EHR (FCCC) must support:**
- [ ] **CDS Hooks client** — firing the `order-sign` hook at the moment Dr. Galloway signs the IMRT order, and rendering the returned card
- [ ] **SMART App Launch** — launching the DTR SMART app in-context (patient, encounter, order) so the questionnaire can be completed/pre-populated without re-entering data

This pathway is **entirely FHIR-based** on both ends. No 360X, no HL7v2, no C-CDA involved here.

### Pathway B — Referral (FCCC → Penn Dental)

**EHR (FCCC) must support:**
- [ ] **IHE 360X only** — HL7 v2 (`OMG^O19` for the referral request, per the ODE crosswalk) and/or C-CDA (Referral Note), transported via Direct/XDM
- [ ] **Explicitly does NOT need any FHIR capability for this pathway** — the directional `ServiceRequest`, `ODEReferralTask`, `ODEMedicationList`, etc. are outputs the *bridge* produces, not artifacts FCCC's system generates or consumes natively. This corrects our earlier draft of this checklist, which listed FHIR resource production as if it were FCCC's responsibility.

**Dental interoperability bridge (the `ode-360x-adapter` or equivalent) must support:**
- [ ] Ingesting the inbound 360X transaction (HL7v2/C-CDA) and translating it into an ODE-conformant FHIR transaction Bundle, per the COW (Clinical Order Workflows) pattern: directional `ServiceRequest` (profile `ode-medical-to-dental-referral`), `ODEReferralTask` (`businessStatus` from the ODE referral sub-status code system), `Condition`, `MedicationRequest`/`ODEMedicationList`, `AllergyIntolerance`, `Coverage`, `Provenance`
- [ ] Correlating both the `ServiceRequest` and `Task` via a shared `urn:ohia:referral-id` identifier
- [ ] Delivering the resulting Bundle to the PMS's FHIR endpoint

**PMS (Penn Dental, via its interim FHIR server) must support:**
- [ ] Receiving and storing the ODE-conformant FHIR Bundle delivered by the bridge
- [ ] Reading `Task.input` for the referral package and `Task.businessStatus` to drive Dr. Sollecito's worklist
- [ ] **Does NOT need to speak 360X/HL7v2/C-CDA directly** — that's the bridge's job; the PMS only ever sees FHIR

This pathway has **no FHIR dependency on FCCC's side** and **no HL7v2/C-CDA dependency on Penn Dental's side** — the bridge is the only system that has to speak both.

### Consumer/Patient App

The patient app needs three distinct capabilities, each satisfying a different mandate/standard:

- [ ] **CARIN Blue Button** (Consumer-Directed Payer Data Exchange) — for claims/EOB data from IBX, satisfying IBX's obligation under CMS-9115-F
- [ ] **Patient Access API** (ONC/ASTP §170.315(g)(10): SMART App Launch + US Core) — for John's clinical data held at FCCC, satisfying FCCC's certified-EHR obligation
- [ ] **An ODE-specific profile for referral/appointment status** — surfacing the referral's `Task.businessStatus` and any `Appointment` in patient-readable form. **Open question, not yet confirmed**: it's unclear whether ODE defines its own patient-facing profile for this, or whether this is expected to ride on top of the same Patient Access API surface as regular clinical data. Needs verification against the ODE IG before this line item can be checked off with confidence.

---

## Encounters #2–7

Not yet built.

## Verification status

Pathway A and B breakdowns for Encounter #1 are built from `spec/mapping/360x-cow-crosswalk.md`, `ARCHITECTURE.md`, and `spec/api/ode-openapi.yaml` in `lp-digitalhealth/ode-360x-adapter`, plus this use case's own narrative (confirming `order-sign`, not `order-select`). The Patient Access API standards mapping (ONC g(10) vs. CMS-9115-F/CARIN) is general regulatory knowledge, not specific to the `ode-360x-adapter` repo. The ODE-specific patient-facing referral/appointment profile is flagged above as unconfirmed and should be checked against the ODE IG directly before relying on it.
