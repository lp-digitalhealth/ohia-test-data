# IG Conformance Matrix — All Use Cases, By Encounter

This is the master cross-reference: for every encounter, in every use case, which Implementation Guides are **required (R)**, **not required (NR)**, or **unknown/not yet determined (U)** — and who's responsible for each.

**Why by encounter, not just by use case:** a use case can span multiple IGs, but not every encounter within it exercises all of them. Encounter #1 fires CRD/DTR and the 360X referral; a later encounter might exercise Provider Access API instead. Testing at the Connectathon happens encounter-by-encounter, so conformance requirements need to be scoped that granularly to be actionable.

**How to read a column:** the first header row is the IG. The second header row is the stakeholder type primarily responsible for implementing/exposing that IG's conformance (some IGs have a shared responsibility — noted in the Description column when relevant).

---

## Encounter-level matrix

| Use Case | Encounter | CRD<br>*(Payer)* | DTR<br>*(Payer + EHR)* | SMART App Launch<br>*(EHR)* | IHE 360X<br>*(EHR + Bridge)* | ODE<br>*(Dental Tech / Bridge)* | CARIN Blue Button<br>*(Payer)* | Provider Access API<br>*(Payer)* | Description |
|---|---|---|---|---|---|---|---|---|---|
| UC01 | 1 — IMRT order & referral | R | R | R | R | R | NR | NR | Order-sign fires CRD; DTR launched via SMART; referral sent via 360X (`OMG^O19`); bridge produces ODE-conformant FHIR bundle. CARIN BB / Provider Access API not exercised yet. |
| UC01 | 2 — Dental exam & radiographs | U | U | U | U | U | U | U | Not yet designed. Likely involves a 360X interim-note transaction (PCC-59) and imaging push — not confirmed. |
| UC01 | 3 — Extraction #4 | U | U | U | U | U | U | U | Not yet designed. |
| UC01 | 4 — Extraction #17 | U | U | U | U | U | U | U | Not yet designed. |
| UC01 | 5 — Extraction #30 + implant | U | U | U | U | U | U | U | Not yet designed. |
| UC01 | 6 — Dental clearance visit | U | U | U | U | U | U | U | Not yet designed. Likely closes the 360X loop (PCC-57 outcome). Provider Access API may be exercised here (per user: "needed later in the use case, not Encounter #1") — not yet confirmed which encounter. |
| UC01 | 7 — Revised IMRT start | U | U | U | U | U | U | U | Not yet designed. |
| UC02 | *(not yet designed)* | — | — | — | — | — | — | — | UC02 (tooth extraction) not yet reviewed for IG scope. Do not assume it mirrors UC01. |
| UC03 | I1 — Exam, assessment & referral | NR | NR | R | NR | R | NR | NR | Referral created in Epic and routed via **Connie (statewide HIE hub)** to **BeneCare** (CTDHP ASO), whose **Plan-Net** directory query identifies Dr. Watson — **CDex push, HIE-mediated (not 360X, not point-to-point)**. Guardian-proxy **SMART App Launch** (minor patient) + **FHIR Subscriptions** for the "referral created" milestone. **No CRD/PA at referral** — covered evaluation; CRD/DTR/PAS (via Gainwell) apply at the treatment visit (I3), not here. No imaging/HL7v2. *(CDex / Connie routing / Plan-Net / Subscriptions are captured here in Description, not as separate columns.)* |
| UC03 | I2 — Pre-encounter records via Connie | NR | NR | NR | NR | R | NR | NR | Pre-encounter medical records pushed **Epic → Connie → dental** via **CDex** as a discrete-FHIR `collection` bundle (**Epic Care Everywhere**); `Provenance`/`AuditEvent` chain-of-custody for the Connie routing hop. **Provider-to-provider — no patient-facing event.** No CRD/PA, no imaging/HL7v2. |
| UC03 | I3 — Treatment visit & PA cycle | R | R | R | NR | R | NR | NR | **The PA proof point.** Dr. Watson signs the D4341 (SRP) order → **CRD** `order-sign` card surfaces the PA requirement → **DTR** `Questionnaire` (launched via SMART, pre-populated from the I2 record) → **PAS** `Claim`/`ClaimResponse` approved (`preAuthRef`). **Routed through Connie**; PA intake at **BeneCare**; DTR/PAS run + adjudicated by **Gainwell** (DSS fiscal agent). ODE oral profiles carry the encounter, five procedures (D0150, D4341 ×2, D4381, D1330), `MedicationAdministration`, `Communication`; referral `Task` → in-progress. **PA is back-office — no patient-facing event.** Not 360X (Connie HIE). |
| UC03 | I4 — Dual summaries, referral closes | NR | NR | R | NR | R | NR | NR | Two simultaneous structured summaries pushed **Cornell Scott → Connie → pediatrician *and* → endocrinologist** via **CDex** (dual `Provenance`/`AuditEvent` routing); new periodontal→glycemic `Flag` (opposite direction from I1's) + `CarePlan`; referral `Task` closes to `outcome-final`. **This** milestone fires to the guardian-proxy **SMART** app via **FHIR Subscriptions** ("visit summary / care plan available") — the provider-to-provider routing itself fires nothing. Not 360X (Connie HIE). |
| UC03 | I5 — Claims-sharing | NR | NR | NR | NR | R | R | NR | The `ODEOralProfessionalEOB` claims-sharing bundle (`ode-dental-claim`, **derived from CARIN Blue Button**): five CDT line items (D0150, D4341 ×2, D4381, D1330), diagnosis K05.211 + E10.9, I3 `preAuthRef` carried on the D4341 lines, D4381 flagged coverage-uncertain. **Gainwell** insurer, **Cornell Scott** billing provider. UC03's payer context = CHIP fiscal-agent model (third after UC02a Medicaid, UC02b commercial). Back-office billing — no patient-facing event. |
| UC04a | I1 — Tuesday Night Pain (virtual referral) | NR | NR | R | NR | R | NR | NR | After-hours **teledentistry** virtual encounter (POS 02). Coverage checked by **real-time benefit verification** (Aetna Dental PPO — virtual consult D9995 covered) — a benefit lookup, **not CRD/PA**. Structured **dental-to-dental** referral pushed via **CDex provider-to-provider** (direct, **not HIE like UC03, not 360X like UC01/UC02**) to the in-office practice's **interim FHIR server**. **Patient-submitted intraoral photos** travel **inline** as a US Core `DocumentReference` (`image/jpeg`, `author` = Patient) — **not DICOM**; tooth #19 correlated via the symptom `Observation` (`bodySite` + `derivedFrom`), since R4 `DocumentReference` has no `bodySite`. Adult self-auth **SMART** + **FHIR Subscriptions** for the "referral sent" milestone. **No Plan-Net** (commercial, known in-network practice), no imaging radiograph (virtual origin), no HL7v2. *(CDex / benefit verification / intraoral-photo DocumentReference / Subscriptions captured here in Description, not as separate columns.)* |
| UC04a | I2 — An Appointment by Morning | NR | NR | R | NR | R | NR | NR | Same-evening scheduling: in-office practice receives the referral on its interim FHIR server, books the next-morning appointment, and returns an `AppointmentResponse` (accepted) via **CDex**. Referral `Task` advances to `appointment-confirmed` with the in-office dentist as `owner` (same `id`, version history). **This** milestone fires to the patient app via **FHIR Subscriptions** ("appointment confirmed — tomorrow 10 AM"). No CRD/PA, no imaging, no HL7v2. |
| UC04a | I3 — The Root Canal (in-office) | NR | NR | NR | NR | R | NR | NR | In-office visit (POS 11): the **first — and only — radiograph** appears here as an `ImagingStudy` + `DiagnosticReport` (DICOM/WADO-RS pointer, `endpoint` → interim server), generated **in-office and NOT exchanged** back to the teledentistry provider (no cross-org support-a-pull; contrast UC02). Provisional pulpitis `Condition` → **confirmed**; new **K04.7** periapical-abscess `Condition` (source's "K04.5" corrected); root canal `Procedure` (CDT D3330, tooth #19). ODE oral profiles carry the encounter/procedure. No patient-facing event at treatment. No CRD/PA (commercial no-PA), no HL7v2. |
| UC04a | I4 — Reporting Back (closed loop) | NR | NR | R | NR | R | NR | NR | Structured `ClinicalImpression` + `CarePlan` outcome summary pushed **Barton Springs → Meridian** via **CDex** — a **single recipient** (contrast UC03's dual fan-out); `Provenance` + `AuditEvent` for the cross-org push. Referral `Task` closes to `status: completed` / `businessStatus: outcome-final` (same `id`, version history) with `Task.output` populated. **This** milestone fires to the adult self-auth **SMART** app via **FHIR Subscriptions** ("visit summary available"). The radiograph is **not** re-transmitted — only its conclusion. Not HIE/360X. |
| UC04a | I5 — Two Bills, One Visit | NR | NR | NR | NR | R | R | NR | Two **independent** `ODEOralProfessionalEOB` bundles (`ode-dental-claim`, **derived from CARIN Blue Button**) — Meridian bills D9995 (POS 02), Barton Springs bills D0220 + D3330 (POS 11, tooth #19) — same commercial payer (Aetna), tied only by the shared referral-id, **not** a joint claim. First time this profile represents **two billing organizations for one episode**. CDT only, **no CPT crosswalk** (dental payer), no PA ref. Non-financial (no adjudication). Back-office billing — no patient-facing event. |
| UC04b | *(not yet built)* | U | U | U | U | U | U | U | UC04b (Medicaid teledentistry, Darius Reyes / diabetes `Flag`) is narrative-only — no FHIR resources built. Mirrors UC04a's virtual-referral shape plus a diabetes-risk `Flag` and (unlike UC04a) a **Plan-Net** directory search. |
| UC05 | *(not yet designed)* | — | — | — | — | — | — | — | UC05 (sleep apnea referral) not yet reviewed. |

**Legend:** R = required for this encounter · NR = confirmed not required for this encounter · U = unknown/not yet determined (encounter not yet designed) · — = use case not yet reviewed at all

---

## Stakeholder-to-IG responsibility (reference)

Which stakeholder type is primarily responsible for each IG's conformance, independent of any specific encounter:

| IG | Primary responsible party | Notes |
|---|---|---|
| **CRD** | Payer Tech | Exposes the CDS Hooks `order-sign` service and `PlanDefinition`; EHR Tech is the *caller*, not the implementer, of this IG |
| **DTR** | Payer Tech + EHR Tech | Payer hosts the `Questionnaire`; EHR launches it via SMART App Launch — genuinely shared |
| **SMART App Launch** | EHR Tech | The launching context; Payer's DTR app is what gets launched into it |
| **IHE 360X** | EHR Tech (sends) + Dental Tech/Bridge (receives, translates) | EHR only needs HL7v2/C-CDA conformance here — no FHIR requirement on the EHR side (see CLAUDE.md Section 5) |
| **ODE** | Dental Tech / Bridge | The FHIR output profile the bridge must produce; PMS consumes it |
| **CARIN Blue Button** | Payer Tech | Feeds both Patient Access API (patient-facing) and Provider Access API (provider-facing) — same underlying data model, two different consumers |
| **Provider Access API** | Payer Tech | Out-of-band provider→payer query capability, independent of the 360X referral workflow |

---

## Open items this matrix surfaces

- Which encounter(s) in UC01 exercise Provider Access API — user has confirmed "not Encounter #1, needed later" but the specific encounter isn't pinned down yet. Likely candidate: Encounter #6 (clearance visit), where Dr. Bellweather might query IBX's claims history — **not confirmed, don't assume.**
- Whether CARIN Blue Button is exercised anywhere in UC01 at all, or only relevant as an always-on payer capability that this specific use case's narrative never actually calls on.
- Encounters #2–7 need actual design sessions before their rows can move from U to R/NR — see CLAUDE.md Section 3.
