# UC03 Companion Guide — Pediatric Dental Referral, Type 1 Diabetes, Connecticut HUSKY B via Connie HIE

**Status:** covers **all five interactions** — I1 (A Routine Checkup Finds Something Else), I2 (Records Before the Visit), I3 (Three Months Later — the dental encounter + prior-authorization cycle), I4 (Telling Both Doctors), and I5 (Billing Timothy's Visit). FHIR resources and companion-guide sections are built for all five. See the [UC03 interactions README](../use-cases/UC03-pediatric-referral/interactions/README.md) for the business writeups.

**Patient:** Timothy Jones, 6 (a minor), New Haven, CT — Type 1 diabetes (E10.9), managed with an insulin pump + CGM. **Coverage:** HUSKY B (Connecticut CHIP) dental benefit. **Referring provider:** Dr. Laura Smith, MD, Northeast Medical Group / Yale New Haven Health pediatrics (runs Epic, Care Everywhere enabled). **Receiving provider:** Dr. David Watson, DDS, Cornell Scott-Hill Health Center (pediatric dental, FQHC). Practitioners are fictional; the institutions (NEMG/YNHH, Cornell Scott-Hill, Connie, CTDHP/BeneCare, Gainwell, Yale diabetes program) are real.

> **What makes UC03 different from UC01/UC02.** There is **no imaging/DICOM** and **no HL7v2** anywhere in this use case. The novel things being tested are: (1) a referral and clinical records that travel **through the state HIE, Connie**, as the central routing hub rather than point-to-point; (2) **Epic Care Everywhere** supplying discrete FHIR records; (3) a **minor patient with a guardian proxy** for the patient-facing app; and (4) a **pediatric-CHIP prior-authorization cycle** — the referral itself (I1) is a *covered evaluation* that triggers **no** PA, but the treatment visit (I3) plans scaling & root planing (D4341), which **does** require PA, so a full **CRD → DTR → PAS** cycle fires there. Don't conflate the two: no PA at the referral, PA at the treatment visit.

> **The Connecticut administration model (get this right).** Connecticut DSS sponsors HUSKY. **Gainwell Technologies** is the DSS fiscal agent (CMAP/MMIS) that verifies eligibility, performs DTR/PAS where PA applies, and **adjudicates and pays** dental claims — it is the payer. **CTDHP** is the HUSKY dental plan brand, **administered/facilitated by the BeneCare ASO** (network, Plan-Net directory, referral coordination, PA intake — *not* the claims payer). **There is no dental MCO.** **Connie** is the statewide HIE and the routing hub for the referral and the records exchange.

---

## 0. Business Overview

At a **well-child visit (2026-02-28)**, Timothy's pediatrician **Dr. Smith** does an oral health assessment and finds plaque-induced gingivitis, two lost lower baby incisors (one site still edentulous), and reported pain — and Timothy has never seen a dentist. Layered on top is his **Type 1 diabetes**, which materially raises periodontal/infection/healing risk. **UC03-I1** is the assessment-and-referral moment: Dr. Smith records the findings, raises an active systemic-disease risk **`Flag`** (diabetes → periodontal risk), and creates a **structured dental referral in Epic**. That referral is **routed through Connie** (the statewide HIE) to **BeneCare** (the CTDHP ASO), whose **Plan-Net** directory returns **Dr. Watson** at Cornell Scott-Hill Health Center (HUSKY B, accepting new patients, within 20 miles). Because this is a referral for a **covered evaluation, not a treatment order, no CRD/prior-authorization fires** — the benefit is simply confirmed active. The earliest appointment is **three months out (2026-05-28)** — which is the clinical setup for what I3 later finds.

**UC03-I2 (2026-05-21)** is the primary interoperability objective: a week before the appointment, Dr. Smith's practice **pushes Timothy's pre-encounter medical records through Connie** to Cornell Scott-Hill's dental system — his diabetes problem, insulin medication, insulin pump + CGM devices, care team, and the oral-health findings — as **discrete FHIR** (Epic Care Everywhere), not a PDF. The clinical driver: the caregiver bringing Timothy to the dental visit is a **grandparent with limited knowledge of his medical history**, so the dental team needs the record ahead of time. This is a **provider-to-provider** exchange — it fires **no** patient-facing notification.

**UC03-I3 (2026-05-28)** is the treatment visit and UC03's **prior-authorization proof point**. Dr. Watson does a comprehensive oral evaluation and a periodontal risk assessment and confirms the gingivitis has progressed to **early-stage aggressive periodontitis, localized, slight (K05.211)** — the aggressive (not chronic) pattern is clinically apt for a six-year-old with poorly controlled Type 1 diabetes. His treatment plan — **scaling & root planing (D4341) across two quadrants** — requires prior authorization under HUSKY B, so signing the SRP order fires a **CRD** check, a **DTR** questionnaire (pre-populated from the record Connie delivered at I2), and a **PAS** request that comes back approved. He then performs the SRP (two quadrants → **two `Procedure` resources, two billed lines**), places a localized chlorhexidine chip (**D4381 — coverage-uncertain, flagged**), delivers oral-hygiene education (D1330), and the referral `Task` advances to *in-progress* with Dr. Watson as owner. The PA cycle is **back-office — no patient-facing notification.**

**UC03-I4 (2026-05-28, same day)** closes the loop by **telling both doctors at once**. Dr. Watson transmits **two simultaneous structured summaries through Connie** — one to the referring pediatrician (Dr. Smith) and one to the pediatric endocrinologist — and the referral `Task` closes to *outcome-final*. The endocrinologist's summary carries a **new `Flag` pointing the opposite direction from I1's**: periodontal disease → glycemic risk (I1's Flag was diabetes → periodontal risk). A `CarePlan` (recall + oral-hygiene) is produced. This is the milestone that **does** surface to the guardian app ("visit summary / care plan available").

**UC03-I5 (2026-05-29)** is the **claims-sharing** proof point: the interoperable `ODEOralProfessionalEOB` bundle for the five services (D0150, D4341 ×2, D4381, D1330), carrying the I3 **`preAuthRef`** on the SRP lines and flagging D4381 as coverage-uncertain. Insurer is **Gainwell** (the fiscal agent that adjudicates/pays); billing provider is **Cornell Scott-Hill**. This is UC03's third payer context for the claims-sharing profile after UC02a (Medicaid) and UC02b (commercial) — now a CHIP fiscal-agent model.

See the interaction writeups for the full narratives: [I1](../use-cases/UC03-pediatric-referral/interactions/uc03-i1-checkup-finds-something-else.md), [I2](../use-cases/UC03-pediatric-referral/interactions/uc03-i2-records-before-visit.md), [I3](../use-cases/UC03-pediatric-referral/interactions/uc03-i3-three-months-later.md), [I4](../use-cases/UC03-pediatric-referral/interactions/uc03-i4-telling-both-doctors.md), [I5](../use-cases/UC03-pediatric-referral/interactions/uc03-i5-billing-timothys-visit.md).

---

## 1. Which IGs Apply

| Interaction | IGs in play |
|---|---|
| **I1 — A Routine Checkup Finds Something Else** | US Core (all clinical content), Da Vinci CDex (the referral is pushed from Epic and routed **through Connie** to the dental practice — HIE-mediated, not point-to-point, and not a 360X bridge), Da Vinci PDex/**Plan-Net** (BeneCare provider-directory query identifies Dr. Watson — HUSKY B, accepting new patients, in range), FHIR Subscriptions Backport IG (guardian-proxy notification: "referral created" and "appointment confirmed"). **Not** CRD/DTR/PAS — covered-evaluation referral, no PA at referral |
| **I2 — Records Before the Visit** | US Core, Da Vinci CDex (pre-encounter clinical records **pushed Epic → Connie → dental** as a `collection` bundle), **Epic Care Everywhere** (discrete FHIR record retrieval, not document dump), `Provenance` + `AuditEvent` (chain-of-custody / Connie routing event). **No** patient-facing event |
| **I3 — Three Months Later** | US Core (encounter, condition, PRA, procedures), **Da Vinci CRD** (order-sign check on the SRP order surfaces the PA requirement), **Da Vinci DTR** (`Questionnaire`/`QuestionnaireResponse`, pre-populated from the I2 record), **Da Vinci PAS** (`Claim`/`ClaimResponse`, approved, `preAuthRef`) — all **routed through Connie**, PA intake at **BeneCare**, DTR/PAS + adjudication by **Gainwell**; ODE oral profiles (procedures, `MedicationAdministration`, `Communication`); the referral `Task` advances to in-progress. **No** patient-facing event (PA is back-office) |
| **I4 — Telling Both Doctors** | US Core, **Da Vinci CDex** (two simultaneous structured summaries pushed Cornell Scott → Connie → pediatrician *and* → endocrinologist), `Provenance` + `AuditEvent` ×2 (dual Connie routing), `Flag` (new periodontal→glycemic direction), `CarePlan`, referral `Task` closes to outcome-final. FHIR Subscriptions Backport IG (**this** milestone fires to the guardian app: visit summary / care plan available) |
| **I5 — Billing Timothy's Visit** | The `ODEOralProfessionalEOB` claims-sharing profile (`ode-dental-claim`); CDT-coded line items (D0150, D4341 ×2, D4381, D1330), diagnosis K05.211 + E10.9, `preAuthRef` carried from I3, D4381 flagged coverage-uncertain; **Gainwell** insurer, **Cornell Scott** billing provider. No patient-facing event (back-office billing) |

**Notably NOT in scope for UC03 (unlike UC01/UC02):**
- **No CRD / DTR / PAS at the *referral* (I1/I2).** The referral is a covered evaluation; coverage is simply confirmed active. **CRD/DTR/PAS *do* fire — but at the treatment visit (I3)**, for the D4341 scaling & root planing, which requires PA. DTR/PAS run downstream through **Gainwell** (the DSS fiscal agent), routed through **Connie**, with PA intake at **BeneCare** — not adjudicated by Connie or BeneCare.
- **No imaging / DICOM.** There are no radiographs anywhere in UC03. The only `DocumentReference` (I1) wraps a text clinical note (the oral health assessment), not an image; there is no `ImagingStudy`, no WADO-RS, no PACS.
- **No HL7v2.** UC03 is entirely FHIR — no PCC-55/OMG^O19 wire message, no MLLP, no interface engine (unlike UC01).
- **No IHE 360X bridge.** Routing is via **Connie (HIE)**, which replaces the 360X transport used in UC01/UC02.

---

## 2. Step-by-Step by Stakeholder

### 2a. Referring Pediatric Practice / Epic (relevant to I1, I2, and I4)

1. Load the registry and base tiers first (see [Resource Index](#4-resource-index)).
2. **At I1:** record the well-child `Encounter`, the oral-health assessment `Observation` and the household-tobacco `Observation`, and the two new `Condition`s (K05.00 gingivitis, Z77.22 tobacco exposure). Timothy's **diabetes `Condition` (E10.9) already exists** in the base tier — reference it, don't re-assert it.
3. Raise the systemic-risk **`Flag`** (diabetes → elevated periodontal/infection/healing risk), authored by Dr. Smith, referencing the pre-existing E10.9 Condition. This is the diabetes→dental direction; the reverse (periodontal→glycemic) `Flag` to the endocrinologist is [I4 work](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/flag-perio-glycemic-risk.json), not part of this I1 step — the two Flags point in opposite directions and must not be conflated.
4. Create the referral (`ServiceRequest`, `status: active`, `ode-medical-to-dental-referral` profile, referral-id `REF-2026-UC03-001`) and **push it via CDex, routed through Connie**, not directly to the dental practice. Carry `reasonCode` K05.00 + E10.9, `supportingInfo` → the risk Flag, insulin `MedicationRequest`, both `Device`s, and the oral-health `DocumentReference`; set `insurance` → the HUSKY B Coverage. **Do not** attach imaging (there is none). **Do not** run a CRD hook — this is a covered evaluation referral, no PA at referral.
5. Open the referral-tracking `Task` (`ode-referral-task`), `focus` on the referral `ServiceRequest`, `businessStatus: referral-sent`, `requester` your organization; leave `owner` unset until the dental practice accepts.
6. Write a `Provenance` recording that Dr. Smith authored the referral and **Connie transmitted/routed** it — the HIE routing is auditable.
7. **At I2 (2026-05-21):** assemble the pre-encounter records as a **`collection` `Bundle`** (Patient, the three Conditions, insulin `MedicationRequest`, both `Device`s, `CareTeam`, oral-health `Observation`, the risk `Flag`, and the well-child `Encounter`) extracted as **discrete FHIR via Care Everywhere**, and **push it through Connie** to Cornell Scott-Hill. Track the delivery with a **separate** `Task` (not the referral Task), and write a `Provenance` + `AuditEvent` for the routing. Fire **no** patient notification.
8. **At I4 (2026-05-28):** *receive* the dental encounter summary Dr. Watson routes back through Connie ([`clinicalimpression-summary-pediatrician.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/clinicalimpression-summary-pediatrician.json)) — the closed loop from your original referral. Ingest the confirmed diagnosis (K05.211), the procedures performed, and the `CarePlan` as discrete FHIR into Epic.

### 2b. Connie — Statewide HIE Routing Hub (relevant to I1, I2, I3, I4)

1. Connie is the **central router** across the whole use case — nothing goes point-to-point. Confirm your system can act as an intermediary that receives from one endpoint (Epic at NEMG/YNHH, [`endpoint-nemg.json`](../fhir-resources/durable/endpoints/endpoint-nemg.json)) and delivers to another ([`endpoint-benecare.json`](../fhir-resources/durable/endpoints/endpoint-benecare.json), [`endpoint-cornell-scott.json`](../fhir-resources/durable/endpoints/endpoint-cornell-scott.json)), recording each hop in `Provenance`/`AuditEvent` ([`endpoint-connie.json`](../fhir-resources/durable/endpoints/endpoint-connie.json)).
2. **At I1** — for the referral, route to **BeneCare** (the CTDHP ASO), whose Plan-Net directory resolves the dental provider; deliver the resulting referral to the dental practice.
3. **At I2** — route the records `collection` bundle to the dental practice's interim FHIR server and confirm receipt.
4. **At I3** — route the **CRD/DTR/PAS** traffic between the dental practice and **Gainwell** (with PA intake coordinated by BeneCare). Connie is the routing mechanism and holder of many of the coverage requirements; Gainwell runs the actual DTR/PAS and adjudicates.
5. **At I4** — perform the **dual routing**: two simultaneous summaries from Cornell Scott, one to the pediatrician (NEMG/Epic) and one to the endocrinologist (Yale diabetes program), each with its own `Provenance`/`AuditEvent`.

### 2c. Payer Side — BeneCare (directory + PA intake) + Gainwell (eligibility, CRD/DTR/PAS, adjudication)

1. **BeneCare / CTDHP (I1):** answer a **Plan-Net** provider-directory query for a HUSKY B–participating pediatric dental provider within 20 miles accepting new patients — returning [`hs-cornell-scott-pediatric-dental.json`](../fhir-resources/durable/healthcare-services/hs-cornell-scott-pediatric-dental.json) (paired with [`role-watson.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/practitioner-roles/role-watson.json)). BeneCare also receives the routed referral for coordination.
2. **Gainwell (I1):** confirm the dental benefit is **active** (eligibility). At the *referral*, that is the extent of the payer's involvement — **no CRD, no DTR, no PAS, no PA number**. Those fire at the treatment visit.
3. **At I3 — the PA cycle fires.** When Dr. Watson signs the SRP (D4341) order, stand up the **CDS Hooks `order-sign`** service ([`cds-hooks-discovery-ctdhp.json`](../fhir-resources/durable/cds-hooks/cds-hooks-discovery-ctdhp.json), backed by [`plandef-ctdhp-d4341-pa-rule.json`](../fhir-resources/durable/payer-rules/plan-definitions/plandef-ctdhp-d4341-pa-rule.json) + [`lib-ctdhp-d4341-pa-logic.json`](../fhir-resources/durable/payer-rules/libraries/lib-ctdhp-d4341-pa-logic.json)) that returns a "PA required" card for D4341. Serve the **DTR `Questionnaire`** ([`questionnaire-ctdhp-d4341-pa-dtr.json`](../fhir-resources/durable/payer-rules/questionnaires/questionnaire-ctdhp-d4341-pa-dtr.json)); accept the completed `QuestionnaireResponse` and the PAS `Claim`; return an approved `ClaimResponse` with a `preAuthRef`. **Gainwell** runs DTR/PAS and adjudicates; **BeneCare** handles PA intake; **Connie** routes. There is no dental MCO.
4. **At I5 — adjudicate/pay.** Gainwell (CMAP) is the insurer on the claims-sharing EOB; it is the entity that adjudicates and pays the dental claim, carrying the I3 `preAuthRef`.

### 2d. Receiving Dental Practice / PMS (relevant to I2, I3, I4, I5)

1. Receive the routed referral `ServiceRequest` (via Connie) and resolve its references. There is **no imaging to pull** — the only attachment is a text oral-health `DocumentReference`.
2. **At I2:** receive the pre-encounter records `collection` bundle routed by Connie, and ingest the discrete FHIR (diabetes Condition, insulin med, pump + CGM Devices, care team, oral-health findings) so Dr. Watson has Timothy's full picture before the visit — this is the point of the exercise, given the accompanying caregiver's limited history.
3. **At I3:** record the dental `Encounter`, PRA (`DiagnosticReport` + two `Observation`s), and the confirmed diagnosis (`Condition` K05.211). Sign the SRP order (`ServiceRequest` D4341) — which triggers the **CRD/DTR/PAS** cycle (complete the DTR `QuestionnaireResponse`, submit the PAS `Claim`, receive the approved `ClaimResponse`). Perform the work as **five `Procedure`s** (D0150, D4341 ×2 one per quadrant, D4381, D1330) plus a `MedicationAdministration` (chlorhexidine chip) and a `Communication` (hygiene education). Advance the referral `Task` to `in-progress` and set `owner` to Dr. Watson. **Fire no patient notification for the PA.**
4. **At I4:** compose two structured summaries (`ClinicalImpression` ×2) and route them through Connie — one to the pediatrician, one to the endocrinologist (the latter carrying the new periodontal→glycemic `Flag`). Produce the `CarePlan`. Close the referral `Task` to `outcome-final`. This is the milestone that surfaces to the guardian app.
5. **At I5:** emit the `ODEOralProfessionalEOB` claims-sharing bundle (`ode-dental-claim`) with the five line items, the I3 `preAuthRef` on the D4341 lines, and D4381 flagged coverage-uncertain.

### 2e. Patient-Facing App Providers (guardian proxy — relevant to I1 and I4; explicitly NOT I2 or I3)

The guardian-facing app does the same thing throughout — subscribe once, display milestones — so its full guidance is consolidated in the [**Patient-Facing App Companion Guide**](#5-patient-facing-app-companion-guide-guardian-proxy) section below (milestone table, guardian-proxy specifics, and the explicit I2 non-event), rather than repeated here.

---

## 3. Stub Specifications

| Role | Minimum bar |
|---|---|
| **Referring practice / Epic stub** | Emit a `ServiceRequest` referral (with `supportingInfo` and `insurance`) and, at I2, a `collection` records bundle — both addressed to Connie, not directly to the dental practice. No CRD hook at the referral. At I4, accept an inbound encounter summary routed back through Connie |
| **Connie HIE routing stub** | Accept an inbound bundle from one endpoint and forward it to another, stamping a `Provenance`/`AuditEvent` for the hop. Must handle: the referral (I1), the records bundle (I2), the CRD/DTR/PAS traffic (I3), and the **dual** summary routing (I4). A fixed "received/forwarded" acknowledgment is sufficient |
| **Payer directory + PA stub (BeneCare + Gainwell)** | **I1:** answer a Plan-Net query with the fixed pediatric-dental `HealthcareService`/`PractitionerRole` pair (HUSKY B, accepting new patients) and an eligibility check with "benefit active" — **no** CRD/PA at the referral. **I3:** return a fixed "PA required" `order-sign` CDS card for D4341, serve the DTR `Questionnaire`, accept the `QuestionnaireResponse` + PAS `Claim`, and return an approved `ClaimResponse` with a fixed `preAuthRef`. **I5:** accept the claims-sharing EOB |
| **Receiving dental practice stub** | Accept a routed `ServiceRequest`; at I2 ingest a `collection` records bundle; at I3 emit the encounter/procedures + drive the PA cycle (DTR response, PAS claim) and produce the confirmed `Condition`; at I4 emit two summaries + `CarePlan`; at I5 emit the EOB. A placeholder acknowledgment per step is sufficient |
| **Guardian app stub** | Display a status string for the guardian-visible milestones (referral created @I1; appointment confirmed; **visit summary / care plan available @I4**) and confirm it fires **nothing** for the I2 records exchange, the I3 PA cycle, or the I4 provider-to-provider routing itself |

---

## 4. Resource Index

### Registry — [`../fhir-resources/durable/`](../fhir-resources/durable/) — load first; reusable across use cases (all UC03 entities are net-new Connecticut)

| File | Type | Purpose |
|---|---|---|
| [`org-nemg.json`](../fhir-resources/durable/organizations/org-nemg.json) | Organization | Northeast Medical Group / Yale New Haven Health pediatrics — referring practice (Epic, Care Everywhere) |
| [`org-cornell-scott.json`](../fhir-resources/durable/organizations/org-cornell-scott.json) | Organization | Cornell Scott-Hill Health Center — receiving pediatric dental FQHC |
| [`org-connie.json`](../fhir-resources/durable/organizations/org-connie.json) | Organization | **Connie** — Connecticut statewide HIE; the routing hub for both interactions |
| [`org-ctdhp.json`](../fhir-resources/durable/organizations/org-ctdhp.json) | Organization | Connecticut Dental Health Partnership — HUSKY dental plan brand |
| [`org-benecare.json`](../fhir-resources/durable/organizations/org-benecare.json) | Organization | BeneCare ASO — administers CTDHP (directory, referral coordination, PA intake); **not** the payer |
| [`org-gainwell.json`](../fhir-resources/durable/organizations/org-gainwell.json) | Organization | Gainwell Technologies — DSS fiscal agent (CMAP); **the payer** (eligibility, DTR/PAS, claims adjudication) |
| [`org-yale-diabetes.json`](../fhir-resources/durable/organizations/org-yale-diabetes.json) | Organization | Yale Children's Diabetes Program — endocrinology/dietitian care-team home |
| [`pract-smith.json`](../fhir-resources/durable/practitioners/pract-smith.json) | Practitioner | Dr. Laura Smith, MD — pediatrician (referring) |
| [`pract-watson.json`](../fhir-resources/durable/practitioners/pract-watson.json) | Practitioner | Dr. David Watson, DDS — pediatric dentist (receiving) |
| [`pract-endo.json`](../fhir-resources/durable/practitioners/pract-endo.json), [`pract-dietitian.json`](../fhir-resources/durable/practitioners/pract-dietitian.json) | Practitioner | Endocrinologist + dietitian (care-team members; names withheld) |
| [`loc-nemg.json`](../fhir-resources/durable/locations/loc-nemg.json), [`loc-cornell-scott.json`](../fhir-resources/durable/locations/loc-cornell-scott.json) | Location | The two New Haven offices (POS 11) |
| [`endpoint-nemg.json`](../fhir-resources/durable/endpoints/endpoint-nemg.json) | Endpoint | NEMG/YNHH Epic FHIR (Care Everywhere) |
| [`endpoint-cornell-scott.json`](../fhir-resources/durable/endpoints/endpoint-cornell-scott.json) | Endpoint | Cornell Scott-Hill interim FHIR server |
| [`endpoint-connie.json`](../fhir-resources/durable/endpoints/endpoint-connie.json) | Endpoint | Connie routing endpoint |
| [`endpoint-benecare.json`](../fhir-resources/durable/endpoints/endpoint-benecare.json) | Endpoint | CTDHP/BeneCare API (Plan-Net, referral coordination) |
| [`hs-cornell-scott-pediatric-dental.json`](../fhir-resources/durable/healthcare-services/hs-cornell-scott-pediatric-dental.json) | HealthcareService | **The Plan-Net directory entry** BeneCare returns in I1 (HUSKY B, accepting new patients, in range) |
| [`insplan-ctdhp-huskyb.json`](../fhir-resources/durable/insurance-plans/insplan-ctdhp-huskyb.json) | InsurancePlan | HUSKY B dental benefit (CTDHP, administered by BeneCare ASO; Gainwell payer) |
| [`plandef-ctdhp-d4341-pa-rule.json`](../fhir-resources/durable/payer-rules/plan-definitions/plandef-ctdhp-d4341-pa-rule.json) | PlanDefinition | **CRD rule (fires at I3):** D4341 requires prior authorization under CTDHP/HUSKY B; notes capture the Connie-routing / BeneCare-intake / Gainwell-adjudication split |
| [`lib-ctdhp-d4341-pa-logic.json`](../fhir-resources/durable/payer-rules/libraries/lib-ctdhp-d4341-pa-logic.json) | Library | CQL logic backing the D4341 PA determination |
| [`questionnaire-ctdhp-d4341-pa-dtr.json`](../fhir-resources/durable/payer-rules/questionnaires/questionnaire-ctdhp-d4341-pa-dtr.json) | Questionnaire | **DTR** form for the D4341 PA — medical-necessity justification (pediatric periodontitis + diabetes) |
| [`cds-hooks-discovery-ctdhp.json`](../fhir-resources/durable/cds-hooks/cds-hooks-discovery-ctdhp.json) | CDS Hooks config | `order-sign` discovery entry that surfaces the D4341 PA-required card (not a FHIR resource — flagged in-file) |

### Base — [`../fhir-resources/purpose-built/uc03-pediatric-referral/base/`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/) — load second; UC03-specific

| File | Type | Purpose |
|---|---|---|
| [`patient-timothy-jones.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/patients/patient-timothy-jones.json) | Patient | Timothy Jones — minor; Epic MRN + dental MRN + HUSKY B Medicaid ID |
| [`coverage-timothy-jones-huskyb.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/coverage/coverage-timothy-jones-huskyb.json) | Coverage | HUSKY B dental; `payor` → Gainwell; plan class CTDHP; BeneCare ASO noted; child relationship |
| [`relatedperson-timothy-guardian.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/related-persons/relatedperson-timothy-guardian.json) | RelatedPerson | Parent / legal guardian — SMART proxy; receives notifications |
| [`relatedperson-timothy-grandparent.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/related-persons/relatedperson-timothy-grandparent.json) | RelatedPerson | Accompanying grandparent, limited history — **the driver for the I2 pre-encounter records exchange** |
| [`role-smith.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/practitioner-roles/role-smith.json), [`role-watson.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/practitioner-roles/role-watson.json), [`role-endo.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/practitioner-roles/role-endo.json) | PractitionerRole | Pediatrics (208000000X), Pediatric Dentistry (1223P0221X, HUSKY B participation), Pediatric Endocrinology (2080P0202X) |
| [`subscription-timothy-referral-status.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/subscriptions/subscription-timothy-referral-status.json) | Subscription | **Guardian-proxy** app subscription; milestones referral-created (I1) + appointment-confirmed + **visit-complete/care-plan (I4)**; **I2 records exchange, I3 PA cycle, and I4 summary routing all fire nothing** |
| [`consent-timothy-connie-hie.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/consent/consent-timothy-connie-hie.json) | Consent | Guardian-authorized (minor) HIE data-sharing consent via Connie |
| [`condition-e10-9-diabetes.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/conditions/condition-e10-9-diabetes.json) | Condition | **Pre-existing** Type 1 diabetes (E10.9, onset 2025) — referenced by the Flag and referral, transmitted in I2; not re-asserted at I1 |
| [`medicationrequest-insulin-lispro.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/medications/medicationrequest-insulin-lispro.json) | MedicationRequest | Insulin lispro via pump — **text-only medication** (no RxNorm asserted; source gives none) |
| [`device-cgm.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/devices/device-cgm.json), [`device-insulin-pump.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/devices/device-insulin-pump.json) | Device | CGM + insulin pump — **text-only `type`** (no verified SNOMED); R4 Device has no `bodySite` |
| [`careteam-timothy.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/care-team/careteam-timothy.json) | CareTeam | Pediatrician + endocrinologist + dietitian — transmitted in the I2 records bundle |

### Interaction 1 — [`.../interactions/interaction-01/`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/) — 2026-02-28 → appointment 2026-05-28

| File | Type | Purpose |
|---|---|---|
| [`encounter-01-well-child.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/encounter-01-well-child.json) | Encounter | The 2026-02-28 well-child visit (Dr. Smith, NEMG, POS 11) |
| [`observation-oral-health-assessment.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/observation-oral-health-assessment.json) | Observation | Oral-health findings (gingivitis, tooth loss, pain, no dental home) as components — **text-only code** |
| [`observation-tobacco-smoke.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/observation-tobacco-smoke.json) | Observation | Household tobacco smoke exposure (LOINC 72166-2, per source mapping) |
| [`condition-k05-00-gingivitis.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/condition-k05-00-gingivitis.json), [`condition-z77-22-tobacco.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/condition-z77-22-tobacco.json) | Condition | New this visit (ICD-10-CM K05.00, Z77.22). Diabetes E10.9 lives in base, referenced not re-asserted |
| [`flag-diabetes-perio-risk.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/flag-diabetes-perio-risk.json) | Flag | Active systemic-disease risk (diabetes → periodontal); references the E10.9 Condition; travels with the referral |
| [`servicerequest-referral.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/servicerequest-referral.json) | ServiceRequest | The referral — `ode-medical-to-dental-referral`, `REF-2026-UC03-001`, `reasonCode` K05.00 + E10.9, `supportingInfo` → Flag/insulin/2 Devices/DocumentReference, `insurance` → Coverage, `occurrenceDateTime` 2026-05-28; **no PA**, **no imaging** |
| [`documentreference-oral-health-assessment.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/documentreference-oral-health-assessment.json) | DocumentReference | Text clinical-note wrapper for the oral-health findings — **not an image** |
| [`task-referral-tracking.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/task-referral-tracking.json) | Task | `ode-referral-task`, `focus` → referral, `businessStatus: referral-sent`, no `owner` yet; **no 360X bridge — routed via Connie** |
| [`provenance-referral.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/provenance-referral.json) | Provenance | Author Dr. Smith (NEMG); **transmitter Connie** — HIE routing is auditable |
| [`appointment-dental.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/appointment-dental.json) | Appointment | Created ~2026-03-05, `start` 2026-05-28; participants Timothy + Dr. Watson + location; `basedOn` the referral |
| [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/interaction-01-bundle.json) | Bundle | Self-contained transaction: registry + base + I1 (**44 entries**) |

### Interaction 2 — [`.../interactions/interaction-02/`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-02/) — 2026-05-21

| File | Type | Purpose |
|---|---|---|
| [`bundle-preencounter-records.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-02/bundle-preencounter-records.json) | Bundle (**collection**) | The CDex payload pushed Epic → Connie → dental: Patient, 3 Conditions (E10.9/K05.00/Z77.22), insulin Med, 2 Devices, CareTeam, oral-health Observation, Flag, well-child Encounter (**11 members**). Distinct from the transaction load bundle |
| [`task-records-delivery.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-02/task-records-delivery.json) | Task | CDex records-delivery task — **separate from the referral Task**; `owner` = the receiving dental org; `status: completed` on Connie-confirmed receipt |
| [`provenance-records-delivery.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-02/provenance-records-delivery.json) | Provenance | Author Dr. Smith / NEMG; transmitter Connie; source = Care Everywhere discrete FHIR |
| [`auditevent-records-routing.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-02/auditevent-records-routing.json) | AuditEvent | Connie routing event (source/destination), outcome success — chain of custody |
| [`interaction-02-bundle.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-02/interaction-02-bundle.json) | Bundle | Self-contained transaction: registry + base + I1 + I2 (**48 entries**; includes the collection bundle as a stored resource so the delivery Task/Provenance/AuditEvent references resolve) |

### Interaction 3 — [`.../interactions/interaction-03/`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/) — 2026-05-28 (the treatment visit; PA cycle fires here)

| File | Type | Purpose |
|---|---|---|
| [`encounter-03-dental-eval.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/encounter-03-dental-eval.json) | Encounter | The 2026-05-28 dental evaluation & treatment visit (Dr. Watson, Cornell Scott, POS 11) |
| [`condition-k05-211-periodontitis.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/condition-k05-211-periodontitis.json) | Condition | **Confirmed diagnosis** — aggressive periodontitis, localized, slight (ICD-10-CM **K05.211**) |
| [`observation-periodontal-findings.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/observation-periodontal-findings.json) | Observation | Periodontal findings by site (pocket depths, bleeding) |
| [`observation-tooth-development.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/observation-tooth-development.json) | Observation | Mixed-dentition status (partially erupted lower central incisor) |
| [`diagnosticreport-perio-risk-assessment.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/diagnosticreport-perio-risk-assessment.json) | DiagnosticReport | Periodontal Risk Assessment — the medical-necessity backing for the PA |
| [`servicerequest-srp-order.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/servicerequest-srp-order.json) | ServiceRequest | The signed **D4341** SRP order (`SRP-2026-UC03-001`) — **triggers CRD**; `reasonCode` K05.211, `insurance` → Coverage, `supportingInfo` → PRA |
| [`questionnaireresponse-srp-pa-dtr.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/questionnaireresponse-srp-pa-dtr.json) | QuestionnaireResponse | Completed **DTR** form (answers [`questionnaire-ctdhp-d4341-pa-dtr.json`](../fhir-resources/durable/payer-rules/questionnaires/questionnaire-ctdhp-d4341-pa-dtr.json)) |
| [`claim-d4341-priorauth.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/claim-d4341-priorauth.json) | Claim | **PAS** PA request (`use: preauthorization`, two D4341 quadrants) |
| [`claimresponse-d4341-priorauth.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/claimresponse-d4341-priorauth.json) | ClaimResponse | **Approved** PA; `preAuthRef` **CT-HUSKYB-PA-2026-00318** (carried to I5); Gainwell insurer |
| [`task-srp-pa-tracking.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/task-srp-pa-tracking.json) | Task | Dedicated PA-tracking Task for the SRP authorization |
| [`task-referral-tracking-inprogress.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/task-referral-tracking-inprogress.json) | Task | **Snapshot** of the I1 referral Task → `in-progress`, `owner` = Dr. Watson (same `id` — version history) |
| [`procedure-d0150-comprehensive-eval.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/procedure-d0150-comprehensive-eval.json) | Procedure | Comprehensive oral evaluation (CDT **D0150**) |
| [`procedure-d4341-srp-lr.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/procedure-d4341-srp-lr.json), [`procedure-d4341-srp-ll.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/procedure-d4341-srp-ll.json) | Procedure | SRP (CDT **D4341**) — **two resources, one per quadrant** (lower right, lower left); mirrors the two EOB lines at I5 |
| [`procedure-d4381-chlorhexidine.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/procedure-d4381-chlorhexidine.json) | Procedure | Localized chlorhexidine delivery (CDT **D4381**) — **coverage flagged open** |
| [`procedure-d1330-oral-hygiene.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/procedure-d1330-oral-hygiene.json) | Procedure | Oral hygiene instructions (CDT **D1330**) |
| [`medicationadministration-chlorhexidine.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/medicationadministration-chlorhexidine.json) | MedicationAdministration | In-office chlorhexidine chip placement (pairs with the D4381 Procedure) |
| [`communication-oral-hygiene-education.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/communication-oral-hygiene-education.json) | Communication | Oral-hygiene education delivered to guardian |
| [`interaction-03-bundle.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/interaction-03-bundle.json) | Bundle | Self-contained transaction: registry + base + I1–I3 incl. the CTDHP PA trio (**68 entries**) |

### Interaction 4 — [`.../interactions/interaction-04/`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/) — 2026-05-28 (dual summaries, referral closes)

| File | Type | Purpose |
|---|---|---|
| [`clinicalimpression-summary-pediatrician.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/clinicalimpression-summary-pediatrician.json) | ClinicalImpression | Structured dental summary → the pediatrician (NEMG), routed via Connie |
| [`clinicalimpression-summary-endocrinologist.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/clinicalimpression-summary-endocrinologist.json) | ClinicalImpression | Structured dental summary → the endocrinologist (Yale); carries the new periodontal→glycemic `Flag` |
| [`flag-perio-glycemic-risk.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/flag-perio-glycemic-risk.json) | Flag | **New** periodontal→glycemic risk — points the **opposite direction** from the I1 diabetes→periodontal Flag; the two must not be conflated |
| [`careplan-perio.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/careplan-perio.json) | CarePlan | Post-treatment periodontal care plan (recall, hygiene, diabetes-team coordination); surfaces to the guardian app |
| [`servicerequest-referral-completed.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/servicerequest-referral-completed.json) | ServiceRequest | **Snapshot** of the I1 referral → `status: completed` (same `id`) |
| [`task-referral-tracking-completed.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/task-referral-tracking-completed.json) | Task | **Snapshot** of the referral Task → `completed`, `businessStatus: outcome-final` (same `id`) |
| [`task-summary-delivery-pediatrician.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/task-summary-delivery-pediatrician.json), [`task-summary-delivery-endocrinologist.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/task-summary-delivery-endocrinologist.json) | Task | Two CDex summary-delivery Tasks — one per recipient |
| [`provenance-summary-pediatrician.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/provenance-summary-pediatrician.json), [`provenance-summary-endocrinologist.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/provenance-summary-endocrinologist.json) | Provenance | Authorship + Connie transmission for each summary |
| [`auditevent-summary-pediatrician.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/auditevent-summary-pediatrician.json), [`auditevent-summary-endocrinologist.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/auditevent-summary-endocrinologist.json) | AuditEvent | Connie routing event per recipient — the **dual-routing** chain of custody |
| [`interaction-04-bundle.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/interaction-04-bundle.json) | Bundle | Self-contained transaction: registry + base + I1–I4 (**78 entries**) |

### Interaction 5 — [`.../interactions/interaction-05/`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-05/) — 2026-05-29 (claims-sharing)

| File | Type | Purpose |
|---|---|---|
| [`eob-timothy-dental-claims-sharing.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-05/eob-timothy-dental-claims-sharing.json) | ExplanationOfBenefit | `ODEOralProfessionalEOB` (`ode-dental-claim`) — **five** line items (D0150, D4341 ×2 one per quadrant, D4381, D1330), diagnosis K05.211 + E10.9, `preAuthRef` **CT-HUSKYB-PA-2026-00318** on the D4341 lines, D4381 flagged coverage-uncertain; Gainwell insurer, Cornell Scott provider. Third claims-sharing payer context (after Medicaid/UC02a, commercial/UC02b) — a CHIP fiscal-agent model |
| [`interaction-05-bundle.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-05/interaction-05-bundle.json) | Bundle | Self-contained transaction: registry + base + I1–I5 (**79 entries**) |

---

## 5. Patient-Facing App Companion Guide (guardian proxy)

Unlike the referring practice, Connie, and the payer — whose actions differ by interaction — Timothy's guardian-facing app does fundamentally the **same thing** throughout: subscribe once, then receive and display milestones as the referral progresses. It is consolidated here for that reason. **The defining wrinkle: Timothy is a minor.** Notifications go to the **guardian proxy**, not to Timothy, and authorization is a guardian-mediated SMART App Launch.

### What to build

1. **A `Subscription`** to the referral's status changes — matching [`subscription-timothy-referral-status.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/subscriptions/subscription-timothy-referral-status.json). It is a Backport-IG `rest-hook` subscription whose `criteria` carries the `SubscriptionTopic` canonical (`.../SubscriptionTopic/ode-referral-status`) directly — same pattern as UC01/UC02. Built once, early.
2. **A guardian-proxy notification handler** that translates the underlying `Task.status`/`businessStatus` into plain-language milestones for the guardian — never raw FHIR codes — and enforces that the authorized recipient is the guardian ([`relatedperson-timothy-guardian.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/related-persons/relatedperson-timothy-guardian.json)), not the child.

### Milestone-by-milestone: what the app shows, and what's driving it

| When | What the guardian sees | What's actually happening (Task field) |
|---|---|---|
| I1 (2026-02-28) | "Dental referral created for Timothy" | [`task-referral-tracking.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/task-referral-tracking.json): `status: requested`, `businessStatus: referral-sent`; `owner` not set yet |
| ~I1/I2 boundary (~2026-03-05) | "Dental appointment confirmed — May 28 with Dr. Watson" | Appointment confirmed / referral Task advances (the acceptance step is I3 work; the appointment is [`appointment-dental.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/appointment-dental.json)) |
| **I2 (2026-05-21)** | **Nothing.** The pre-encounter medical-records exchange (Epic → Connie → dental) is **provider-to-provider** — no guardian notification fires. | N/A — [`task-records-delivery.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-02/task-records-delivery.json) is a records-delivery Task, not the referral Task the app subscribes to |
| **I3 (2026-05-28)** | **Nothing.** The CRD/DTR/PAS prior-authorization cycle for D4341 is entirely **back-office** — the family sees no PA chatter. | N/A — [`task-srp-pa-tracking.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-03/task-srp-pa-tracking.json) is a PA-tracking Task, not the subscribed referral Task |
| **I4 (2026-05-28)** | "Timothy's dental visit summary and care plan are available" | Referral Task closes: [`task-referral-tracking-completed.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/task-referral-tracking-completed.json) → `completed` / `businessStatus: outcome-final`; the [`careplan-perio.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-04/careplan-perio.json) is surfaced. **The provider-to-provider summary routing itself fires nothing** — only the visit-complete/care-plan milestone does |

**The one thing worth testing deliberately:** whether the guardian app fires on the real referral milestones (created @I1, appointment confirmed, visit-complete/care-plan @I4) and **stays silent for the I2 records exchange, the I3 PA cycle, and the I4 provider-to-provider summary routing** — an app that notifies the family every time providers swap records or run a prior auth behind the scenes is doing the wrong thing. That silence is a genuine, testable requirement, not an omission.

### Credentials and stubs

Full Patient Access API testing needs real SMART App Launch registration (client ID/secret, redirect URIs, scopes) **with a guardian/proxy authorization flow**, against whichever FHIR server holds Timothy's data — treat client secrets as real secrets even in a sandbox. For the minimum bar, see the guardian app row in [Section 3](#3-stub-specifications): a stub only needs to display a status string per milestone and must NOT fire for the I2 records exchange.

---

## 6. Tooling — what you need to actually run this

UC03 is **entirely FHIR** and has **no imaging** — so, unlike UC01, there is **no HL7v2/wire-level artifact** (no MLLP, no interface engine, no HL7v2 parser) and, unlike UC01/UC02, **no DICOM/PACS/WADO-RS stack** at all. What you need is a FHIR server plus the ability to model an **HIE routing intermediary** and **Care Everywhere discrete-FHIR** retrieval.

### 6a. FHIR services

- **A FHIR R4 server** to load resources onto: **HAPI FHIR** (Java, open-source, Docker-friendly) or **OnyxOS**. Any R4-conformant server works.
- **Loading:** each file has a fixed `id` — `PUT [base]/{ResourceType}/{id}` per the load order (Registry → Base → Interaction), or `POST` an interaction bundle ([`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-01/interaction-01-bundle.json), [`interaction-02-bundle.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/interactions/interaction-02/interaction-02-bundle.json)) as a single transaction. Any HTTP client (`curl`, Postman) suffices.
- **Profile validation:** the official **HL7 FHIR Validator CLI** (`validator_cli.jar`) checks a resource against its declared `meta.profile`; **Inferno** covers US Core and SMART App Launch (relevant to the guardian-proxy flow). Our own checks were structural/cross-reference only — run the validator before the Connectathon if strict conformance will be checked.
- **CRD/DTR/PAS services are needed at I3 (not I1/I2).** For the treatment visit you'll want a **CDS Hooks `order-sign`** endpoint returning the D4341 "PA required" card ([`cds-hooks-discovery-ctdhp.json`](../fhir-resources/durable/cds-hooks/cds-hooks-discovery-ctdhp.json) + [`plandef-ctdhp-d4341-pa-rule.json`](../fhir-resources/durable/payer-rules/plan-definitions/plandef-ctdhp-d4341-pa-rule.json)), a **DTR** `Questionnaire` renderer ([`questionnaire-ctdhp-d4341-pa-dtr.json`](../fhir-resources/durable/payer-rules/questionnaires/questionnaire-ctdhp-d4341-pa-dtr.json)), and a **PAS** `Claim`/`ClaimResponse` exchange — the same Da Vinci stack UC02a exercises, here on a HUSKY B fiscal-agent model. At the *referral* (I1/I2) none of this fires. **Reuse the CTDHP payer-rule trio** ([durable/payer-rules/](../fhir-resources/durable/payer-rules/)) rather than rebuilding it.

### 6b. HIE routing + Care Everywhere (the actual novel stack)

The thing UC03 exercises that UC01/UC02 don't is **HIE-mediated routing through Connie** plus **Epic Care Everywhere discrete FHIR**:

1. **Connie as an intermediary.** Both the I1 referral and the I2 records bundle transit Connie ([`endpoint-connie.json`](../fhir-resources/durable/endpoints/endpoint-connie.json)) rather than going point-to-point. To exercise this, stand up (or stub) a routing node that receives a bundle from a source endpoint and forwards it to a destination endpoint, recording a `Provenance` and `AuditEvent` for the hop. The `AuditEvent`/`Provenance` pair in I2 shows the expected chain-of-custody shape.
2. **Care Everywhere discrete FHIR.** The I2 payload is a **`collection` `Bundle`** of discrete FHIR resources (not a C-CDA document or PDF) — the point is that the receiver ingests structured data, not a document blob. Any R4 server can hold and serve the collection bundle; the test is that your dental-side system can consume discrete resources.
3. **Guardian-proxy SMART App Launch** (see [Section 5](#5-patient-facing-app-companion-guide-guardian-proxy)) — a minor-patient authorization flow, distinct from the adult self-authorization in UC01/UC02.

**Explicitly not needed:** DICOMweb server, PACS (Orthanc/dcm4chee), WADO-RS, DICOM viewer, MLLP/interface engine, HL7v2 validator. None of these apply to UC03.

---

## 7. What to do if something doesn't match

Check this guide's [Resource Index](#4-resource-index) and the interaction writeups first. If a resource doesn't match what your system expects, it's either a documented design decision — **no CRD/PA at referral** (covered evaluation), **HIE routing via Connie** (not 360X, not point-to-point), the pre-existing diabetes resources living in the **base tier**, the I2 payload being a **`collection`** bundle distinct from the transaction load bundle, or **no imaging/HL7v2 anywhere** — or genuinely new, in which case flag it rather than silently working around it. A few specific things to expect rather than treat as errors:

- **Text-only codes by design (project verification discipline):** the oral-health assessment `Observation` code, the insulin `MedicationRequest` (no RxNorm — the source gives none), and both `Device` `type`s (no verified SNOMED). These are deliberate, not oversights. If your validator wants a code there, that's the reason.
- **Diabetes (E10.9), insulin, the two Devices, and the CareTeam live in the base tier**, not in Interaction 1 — they pre-exist Timothy's well-child visit. Interaction 1 *references* them (Flag, referral `supportingInfo`); Interaction 2 *transmits* them (records bundle). They are not re-asserted at I1.
- **Two separate `Task`s.** The referral-tracking `Task` (I1) and the records-delivery `Task` (I2) are distinct — referral state and records-delivery state are tracked independently. Don't expect one Task to carry both.
- **No CRD card or PA number at the *referral* (I1/I2)** — but the **PA cycle *does* fire at I3** (D4341 requires prior authorization: CRD card → DTR `Questionnaire` → PAS `Claim`/`ClaimResponse`, `preAuthRef` **CT-HUSKYB-PA-2026-00318** carried to the I5 EOB). **No `ImagingStudy` and no HL7v2 message anywhere** in UC03 — those are by design across all five interactions.
- **D4341 is two `Procedure`s (one per quadrant) and two EOB line items** — not one combined line. **D4381 (chlorhexidine) is flagged coverage-uncertain**, carried honestly as an open question rather than asserted covered.
- **Three snapshots share IDs with earlier versions:** the referral `Task` (I1 → in-progress @I3 → completed @I4) and the referral `ServiceRequest` (I1 → completed @I4) are sequential `PUT`s to the same `id` (FHIR version history), not new resources. Load them in interaction order.
- **The payer split:** `Coverage.payor` is **Gainwell** (the fiscal agent that actually pays), while the **directory** query targets **BeneCare/CTDHP** (the ASO). If your model expects a single payer entity that both runs the directory and pays claims, that's the Connecticut-specific split to account for — [`coverage-timothy-jones-huskyb.json`](../fhir-resources/purpose-built/uc03-pediatric-referral/base/coverage/coverage-timothy-jones-huskyb.json) and [`insplan-ctdhp-huskyb.json`](../fhir-resources/durable/insurance-plans/insplan-ctdhp-huskyb.json) document it.

All persons except the institutions are fictional; identifiers (MRNs, NPIs, member IDs, licenses) are synthetic placeholders.
