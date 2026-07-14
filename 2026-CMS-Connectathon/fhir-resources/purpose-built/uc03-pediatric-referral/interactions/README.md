# UC03 Per-Interaction FHIR Resources

Pediatric dental referral for **Timothy Jones** (age 6, Type 1 diabetes), covered by **Connecticut HUSKY B** dental (CTDHP), with the referral and clinical records routed through **Connie**, Connecticut's statewide HIE. **All five interactions (I1–I5) are built as FHIR resources** (see [`../../../../use-cases/UC03-pediatric-referral/interactions/README.md`](../../../../use-cases/UC03-pediatric-referral/interactions/README.md) for the business writeups).

Transactional resources specific to each interaction live here; base/registry resources live in [`../base/`](../base/) and the durable registry [`../../../durable/`](../../../durable/).

## What makes UC03 structurally different (don't pattern-match from UC01/UC02)

- **No imaging / DICOM.** There are no radiographs at referral; the only `DocumentReference` wraps a text clinical note. No `ImagingStudy`, no WADO-RS.
- **No HL7v2.** UC03 is entirely FHIR — no PCC-55/`OMG^O19` wire message, no MLLP.
- **No IHE 360X bridge.** Routing is via **Connie (HIE)**, which replaces the 360X transport. The referral `Task` is `ode-referral-task` but its `note` reflects HIE routing, not a bridge.
- **No CRD/DTR/PAS at the *referral* (I1/I2), but the full cycle fires at the treatment visit (I3).** The referral is a *covered evaluation* — coverage is confirmed active, no PA. At I3, the planned D4341 scaling & root planing **does** require prior authorization: CRD `order-sign` → DTR `Questionnaire` → PAS `Claim`/`ClaimResponse`, all **routed through Connie**, PA intake at **BeneCare**, DTR/PAS + adjudication by **Gainwell**. The durable CTDHP PA trio (PlanDefinition/Library/Questionnaire) + CDS-Hooks discovery live in [`../../../durable/payer-rules/`](../../../durable/payer-rules/) and [`../../../durable/cds-hooks/`](../../../durable/cds-hooks/).
- **Pre-existing clinical baseline lives in `base/`.** Timothy's diabetes `Condition` (E10.9), insulin `MedicationRequest`, the CGM + insulin-pump `Device`s, and his `CareTeam` predate the well-child visit — they are referenced (I1) and transmitted (I2), never re-asserted per interaction.
- **The Connecticut payer split:** `Coverage.payor` is **Gainwell** (fiscal agent that pays claims); the **Plan-Net directory** query targets **CTDHP/BeneCare** (ASO). No dental MCO.

## Interaction 1 — A Routine Checkup Finds Something Else (built) — 2026-02-28 → appointment 2026-05-28

Well-child visit where Dr. Smith (pediatrician) does an oral-health assessment, raises a diabetes→periodontal risk `Flag`, and creates a dental referral routed via Connie to BeneCare (Plan-Net → Dr. Watson).

- `encounter-01-well-child.json` — Encounter (well-child visit, Dr. Smith, NEMG, POS 11)
- `observation-oral-health-assessment.json` — Observation (gingivitis / tooth loss / pain / no dental home, as components; **text-only code**)
- `observation-tobacco-smoke.json` — Observation (household tobacco smoke exposure, LOINC 72166-2 per source mapping)
- `condition-k05-00-gingivitis.json`, `condition-z77-22-tobacco.json` — Condition x2 (ICD-10-CM K05.00, Z77.22; new this visit). Diabetes E10.9 lives in `base/`, referenced not re-asserted
- `flag-diabetes-perio-risk.json` — Flag (active systemic-disease risk; diabetes → periodontal; references the E10.9 Condition)
- `servicerequest-referral.json` — ServiceRequest, `ode-medical-to-dental-referral`: `urn:ohia:referral-id` `REF-2026-UC03-001`, `reasonCode` K05.00 + E10.9, `supportingInfo` → Flag/insulin/2 Devices/DocumentReference, `insurance` → Coverage, `occurrenceDateTime` 2026-05-28. **No PA, no imaging.**
- `documentreference-oral-health-assessment.json` — DocumentReference (text clinical-note wrapper for the oral-health findings — **not an image**)
- `task-referral-tracking.json` — Task, `ode-referral-task`: task-code `fulfill`, `businessStatus: referral-sent`, `focus` → referral, no `owner` yet. Note reflects **Connie HIE routing, no 360X bridge**
- `provenance-referral.json` — Provenance (author Dr. Smith/NEMG; **transmitter Connie**)
- `appointment-dental.json` — Appointment (created ~2026-03-05, `start` 2026-05-28; Timothy + Dr. Watson + location; `basedOn` the referral)
- `interaction-01-bundle.json` — self-contained transaction bundle: registry + base + I1 (**44 entries**)

## Interaction 2 — Records Before the Visit (built) — 2026-05-21

A week before the appointment, Dr. Smith's practice pushes Timothy's pre-encounter medical records (discrete FHIR, via Care Everywhere) through Connie to the dental practice — driven by the accompanying caregiver being a grandparent with limited medical history.

- `bundle-preencounter-records.json` — Bundle (**type `collection`**): the CDex payload pushed Epic → Connie → dental — Patient, 3 Conditions (E10.9/K05.00/Z77.22), insulin Med, 2 Devices, CareTeam, oral-health Observation, Flag, well-child Encounter (**11 members**). Distinct from the transaction load bundle below
- `task-records-delivery.json` — Task, CDex records delivery — **separate from the referral Task**; `owner` = receiving dental org; `status: completed` on Connie-confirmed receipt; `focus`/`output` → the collection bundle
- `provenance-records-delivery.json` — Provenance (author Dr. Smith/NEMG; transmitter Connie; source = Care Everywhere discrete FHIR)
- `auditevent-records-routing.json` — AuditEvent (Connie routing hop, source→destination, outcome success — chain of custody)
- `interaction-02-bundle.json` — self-contained transaction bundle: registry + base + I1 + I2 (**48 entries**; includes the collection bundle as a stored resource so the delivery Task/Provenance/AuditEvent references resolve)

**No patient-facing notification at I2** — provider-to-provider. The guardian-proxy `Subscription` (in `base/`) must fire nothing here.

## Interaction 3 — Three Months Later (built) — 2026-05-28 (the treatment visit; PA cycle fires here)

Dr. Watson does a comprehensive oral eval + periodontal risk assessment, confirms **aggressive periodontitis, localized, slight (K05.211)**, and plans **scaling & root planing (D4341) across two quadrants** — which requires prior authorization under HUSKY B. Signing the SRP order fires the full CRD → DTR → PAS cycle (routed via Connie; PA intake at BeneCare; DTR/PAS + adjudication by Gainwell), then he performs the work.

- `encounter-03-dental-eval.json` — Encounter (dental evaluation & treatment, Dr. Watson, Cornell Scott, POS 11)
- `condition-k05-211-periodontitis.json` — Condition (confirmed diagnosis, ICD-10-CM **K05.211** aggressive periodontitis, localized, slight)
- `observation-periodontal-findings.json`, `observation-tooth-development.json` — Observation x2 (periodontal findings by site; mixed-dentition status)
- `diagnosticreport-perio-risk-assessment.json` — DiagnosticReport (Periodontal Risk Assessment — medical-necessity backing for the PA)
- `servicerequest-srp-order.json` — ServiceRequest, D4341 SRP order (`SRP-2026-UC03-001`) — **triggers CRD**; `reasonCode` K05.211, `supportingInfo` → PRA
- `questionnaireresponse-srp-pa-dtr.json` — QuestionnaireResponse (completed **DTR**, answers the durable CTDHP D4341 Questionnaire)
- `claim-d4341-priorauth.json` — Claim (**PAS** PA request, `use: preauthorization`, two D4341 quadrants)
- `claimresponse-d4341-priorauth.json` — ClaimResponse (**approved**; `preAuthRef` **CT-HUSKYB-PA-2026-00318**, carried to I5; Gainwell insurer)
- `task-srp-pa-tracking.json` — Task (dedicated PA-tracking Task for the SRP authorization)
- `task-referral-tracking-inprogress.json` — Task (**snapshot** of the I1 referral Task → `in-progress`, `owner` = Dr. Watson; same `id`)
- `procedure-d0150-comprehensive-eval.json` — Procedure (D0150 comprehensive oral evaluation)
- `procedure-d4341-srp-lr.json`, `procedure-d4341-srp-ll.json` — Procedure x2 (D4341 SRP, **one per quadrant** — lower right, lower left; mirrors the two I5 EOB lines)
- `procedure-d4381-chlorhexidine.json` — Procedure (D4381 localized chlorhexidine delivery — **coverage flagged open**)
- `procedure-d1330-oral-hygiene.json` — Procedure (D1330 oral hygiene instructions)
- `medicationadministration-chlorhexidine.json` — MedicationAdministration (in-office chlorhexidine chip; pairs with the D4381 Procedure)
- `communication-oral-hygiene-education.json` — Communication (oral-hygiene education to guardian)
- `interaction-03-bundle.json` — self-contained transaction bundle: registry + base + I1–I3 incl. the durable CTDHP PA trio (**68 entries**)

**PA cycle is back-office — no patient-facing notification at I3.**

## Interaction 4 — Telling Both Doctors (built) — 2026-05-28 (same day; dual summaries, referral closes)

Dr. Watson transmits two simultaneous structured summaries through Connie — one to the pediatrician, one to the endocrinologist — and the referral `Task` closes to `outcome-final`.

- `clinicalimpression-summary-pediatrician.json`, `clinicalimpression-summary-endocrinologist.json` — ClinicalImpression x2 (dental encounter summaries; the endocrinologist's carries the new perio→glycemic Flag)
- `flag-perio-glycemic-risk.json` — Flag (**new** periodontal→glycemic risk — points the **opposite direction** from I1's diabetes→periodontal Flag; the two must not be conflated)
- `careplan-perio.json` — CarePlan (post-treatment periodontal care plan: recall, hygiene, diabetes-team coordination; surfaces to the guardian app)
- `servicerequest-referral-completed.json` — ServiceRequest (**snapshot** of the I1 referral → `status: completed`; same `id`)
- `task-referral-tracking-completed.json` — Task (**snapshot** of the referral Task → `completed`, `businessStatus: outcome-final`; same `id`)
- `task-summary-delivery-pediatrician.json`, `task-summary-delivery-endocrinologist.json` — Task x2 (CDex summary-delivery, one per recipient)
- `provenance-summary-pediatrician.json`, `provenance-summary-endocrinologist.json` — Provenance x2 (authorship + Connie transmission)
- `auditevent-summary-pediatrician.json`, `auditevent-summary-endocrinologist.json` — AuditEvent x2 (Connie routing per recipient — the **dual-routing** chain of custody)
- `interaction-04-bundle.json` — self-contained transaction bundle: registry + base + I1–I4 (**78 entries**)

**This** milestone (visit-complete / care-plan) is the one that fires to the guardian-proxy app — the provider-to-provider summary routing itself fires nothing.

## Interaction 5 — Billing Timothy's Visit (built) — 2026-05-29 (claims-sharing)

- `eob-timothy-dental-claims-sharing.json` — ExplanationOfBenefit, `ode-dental-claim` (`ODEOralProfessionalEOB`): **five** line items (D0150, D4341 ×2 one per quadrant, D4381, D1330), diagnosis K05.211 + E10.9, `preAuthRef` **CT-HUSKYB-PA-2026-00318** on the D4341 lines, D4381 flagged coverage-uncertain; Gainwell insurer, Cornell Scott provider. Third claims-sharing payer context (after Medicaid/UC02a, commercial/UC02b) — a CHIP fiscal-agent model
- `interaction-05-bundle.json` — self-contained transaction bundle: registry + base + I1–I5 (**79 entries**)

## Verification

All resources were verified programmatically: JSON validity, cross-reference id resolution (every `reference` resolves), and date/code consistency; all five transaction bundles plus the I2 collection bundle were assembled and validated (**44 / 48 / 68 / 78 / 79** transaction entries + 11-member collection confirmed). The I3+ bundles include the durable CTDHP D4341 PA trio (`PlanDefinition` / `Library` / `Questionnaire`), matching UC02a's PA-bundle pattern. Cumulative snapshots override earlier versions of the same `id` (referral `Task`: sent → in-progress → completed; referral `ServiceRequest`: active → completed). Per project discipline, codes not confidently verified are **text-only** (no `coding`): the oral-health assessment code, the insulin medication (no RxNorm in the source), and both `Device` `type`s. Standard codes used: ICD-10-CM K05.00 / Z77.22 / E10.9 / **K05.211**, LOINC 72166-2, CDT D0150 / D1330 / D4341 / D4381, and NUCC taxonomies 208000000X / 1223P0221X / 2080P0202X.
