# UC04a Companion Guide — Commercial Teledentistry Referral, Acute Pulpitis, Austin TX

**Status:** covers **all five interactions as built FHIR resources** — I1 (Tuesday Night Pain — the after-hours virtual encounter, coverage verification, and structured referral), I2 (An Appointment by Morning — same-evening scheduling and confirmation), I3 (The Root Canal — in-office evaluation, the first radiograph, and endodontic treatment), I4 (Reporting Back — the closed-loop outcome summary), and I5 (Two Bills, One Visit — the two-organization claims-sharing). See the [UC04 interactions README](../use-cases/UC04-teledentistry-referral/interactions/README.md) for all business writeups.

**Patient:** Sarah Okonkwo, 34 (an adult — self-authorizes, no guardian proxy), Austin, TX — acute front-tooth pain on biting, provisionally (suspected) irreversible pulpitis, tooth #9, and no dental home. **Coverage:** Aetna Dental PPO (employer-sponsored commercial). **Referring provider:** Dr. Marcus Webb, DDS, **Meridian Teledental** (a virtual-care platform, Place of Service 02 — no physical office, no radiograph capability). **Receiving provider:** Dr. Priya Nair, DDS, **Barton Springs Dental Group** (in-office general dentistry, Austin, POS 11). Meridian Teledental and Barton Springs Dental Group are fictional; **Aetna Dental is the real payer named in the source** (its EDI/endpoint identifiers here are synthetic).

> **What makes UC04a different from UC01/UC02/UC03.** The originating provider is a **virtual-care platform**, not another in-office PMS. That changes three things: (1) there is **no diagnostic radiograph at referral** — Dr. Webb can't take one — so no `ImagingStudy`/DICOM/PACS/WADO-RS until the in-office visit (I3); (2) but the patient **does** contribute **intraoral photos** captured on her phone through the app, which travel with the referral **by ARex reference** — a manifest of US Core-style `DocumentReference` entries (see the standards note below); and (3) the referral is a **dental-to-dental CDex provider-to-provider push** (direct, not HIE-routed like UC03, not a 360X bridge like UC01/UC02), landing on the in-office practice's **interim FHIR server**.

> **The intraoral-photo standards decision (get this right).** The photos are modeled as a **US Core `DocumentReference`** (`image/jpeg`, `author` = Patient, delivered by ARex reference and not inline), **not** an R4 `Media`. Rationale across the project's real constraints: (1) ONC's mandated path is **R4 → R6, skipping R5** — `Media` is removed in R5 and stays removed in R6, while `DocumentReference` exists in both, so a `Media`-based artifact is a guaranteed future rewrite; (2) US Core profiles `DocumentReference` and CDex uses it — `Media` has no US Core profile; (3) through a 360X/C-CDA bridge the photo bytes survive as embedded multimedia either way, and the one thing `Media` does natively (tooth-on-image via `Media.bodySite`) is exactly the structured detail that flattens crossing into C-CDA. Because R4 `DocumentReference` has **no `bodySite`**, tooth #9 is correlated **indirectly**: the symptom `Observation` carries `bodySite` = tooth #9 and `derivedFrom` → the photo `DocumentReference`. This is **not** a DICOM radiograph — that is a separate artifact that first appears in-office at I3.

---

## 0. Business Overview

Late on a Tuesday (**2026-07-14, ~7:30 PM**), **Sarah Okonkwo**, who has no dental home, has escalating pain when she bites on her front teeth — she can no longer chew or bite with them. She opens her employer's dental benefit app and starts an on-demand **teledentistry** visit with **Dr. Marcus Webb** at Meridian Teledental.

**UC04a-I1** is the after-hours virtual encounter. At session start, the app **verifies her Aetna Dental PPO coverage in real time** — the virtual consult (D9995) is a covered benefit, so this is not an out-of-pocket expense. Dr. Webb runs a structured assessment (duration, thermal sensitivity, pain on biting, spontaneous aching), confirms she **has no dental home**, has Sarah **capture one or two intraoral photos** of the sore area on her phone, and documents findings consistent with **suspected irreversible pulpitis, tooth #9** (`ICD-10 K04.01`, recorded **provisional** — a virtual visit can't confirm without a radiograph). Because this needs in-person evaluation, a radiograph, and likely a root canal, he creates a **structured dental-to-dental referral** (priority `urgent`) to an in-network in-office practice — Barton Springs Dental Group — and **pushes it via CDex provider-to-provider**, with the intraoral photos traveling **by ARex reference** (a manifest of two image entries), not inline. **No prior authorization fires** — the commercial plan requires none for the virtual consult, the radiograph, the root canal, or the composite restoration.

**UC04a-I2** (**2026-07-14, 20:06–20:47**) is the same-evening turnaround. Barton Springs' **interim FHIR server** receives the referral within a minute — no fax, nothing waiting until morning. Within ~40 minutes their staff reviews it and books Sarah for **the next morning, 10:00 AM**, returning an `AppointmentResponse` to Meridian. The referral `Task` advances to *appointment-confirmed*, with Dr. Nair now its `owner`. Both milestones — referral sent and appointment confirmed — surface to Sarah's app.

**UC04a-I3** (**2026-07-15, 10:00–12:15**) is the in-office visit where the **first radiograph** is taken (`ImagingStudy` + `DiagnosticReport`, DICOM/WADO-RS pointer — generated **in-office**, not exchanged back to Meridian) and the root canal (D3310) performed, with the access restored in the same visit by a lingual direct composite (D2330). The provisional `Condition` flips to **confirmed**, and a new **K04.7** periapical-abscess `Condition` is added. **UC04a-I4** (**2026-07-15, 12:35**) reports the outcome back to Meridian as a structured `ClinicalImpression` + `CarePlan` pushed via CDex, closing the referral loop (the referral `Task` reaches `outcome-final`) — a **single recipient** (contrast UC03's dual fan-out). **UC04a-I5** (**2026-07-16**) is the **two-organization claims-sharing** proof point: Meridian bills the virtual consult (D9995), Barton Springs bills the in-office treatment (D0220 + D3310 + D2330) — two independent `ODEOralProfessionalEOB` packages to the same commercial payer, tied together only by the shared referral, both CDT-coded (837D-equivalent), no CPT crosswalk.

See the interaction writeups: [I1](../use-cases/UC04-teledentistry-referral/interactions/uc04a-i1-tuesday-night-pain.md), [I2](../use-cases/UC04-teledentistry-referral/interactions/uc04a-i2-appointment-by-morning.md), [I3](../use-cases/UC04-teledentistry-referral/interactions/uc04a-i3-the-root-canal.md), [I4](../use-cases/UC04-teledentistry-referral/interactions/uc04a-i4-reporting-back.md), [I5](../use-cases/UC04-teledentistry-referral/interactions/uc04a-i5-two-bills-one-visit.md).

> **Verification-discipline note (ICD-10).** The source use-case document labels the periapical finding "**K04.5** — Periapical abscess without sinus." K04.5 is actually *chronic apical periodontitis*; "periapical abscess without sinus" is **K04.7** (the code UC02a's claims-sharing EOB already uses). The built I3/I5 resources use **K04.7**, and the source doc has been corrected — flagged here so the difference from the original source isn't mistaken for an error.

---

## 1. Which IGs Apply

| Interaction | IGs in play |
|---|---|
| **I1 — Tuesday Night Pain** *(built)* | US Core (all clinical content, incl. the intraoral photos as US Core-style `DocumentReference` entries of an **ARex manifest**, and `us-core-smokingstatus`), Da Vinci **CDex** (the referral is a **provider-to-provider push**, virtual platform → in-office interim FHIR server — direct, not HIE-routed, not a 360X bridge), FHIR Subscriptions Backport IG (adult self-auth app: "referral sent"). Real-time **coverage verification** at session start (benefit active for D9995) — a plan lookup, **not** CRD/PA. **Not** CRD/DTR/PAS (commercial no-PA), **not** Plan-Net (that's UC04b) |
| **I2 — An Appointment by Morning** *(built)* | US Core, `Appointment` / `AppointmentResponse` (booked + confirmed), CDex (the confirmation is pushed back to Meridian), FHIR Subscriptions Backport IG (**this** milestone fires to the app: "appointment confirmed"), `Provenance` (in-office → teledentistry) |
| **I3 — The Root Canal** *(built)* | US Core, ODE oral profiles (`Procedure` D3310, D2330, D0220), **and the first imaging** — `DiagnosticReport` + `ImagingStudy` (periapical radiograph; DICOM/WADO-RS pointer, `endpoint` → the in-office interim server) generated **in-office** and **not** exchanged back to Meridian. Provisional `Condition` → confirmed; new K04.7 periapical-abscess `Condition` |
| **I4 — Reporting Back** *(built)* | US Core, CDex (structured `ClinicalImpression` + `CarePlan` outcome summary pushed back to Meridian — **single recipient**), referral `Task` closes to `outcome-final`, `AuditEvent` for the cross-org push, FHIR Subscriptions Backport IG ("visit summary available") |
| **I5 — Two Bills, One Visit** *(built)* | The `ODEOralProfessionalEOB` claims-sharing profile (`ode-dental-claim`) — **two separate claims-ready packages, one per submitting organization** (Meridian: D9995; Barton Springs: D0220 + D3310 + D2330), both to the same commercial payer, tied only by the shared referral, both CDT-coded (no CPT crosswalk). CARIN BB CodeSystem for careTeam roles |

**Notably NOT in scope for UC04a (unlike other use cases):**
- **No CRD / DTR / PAS.** The commercial plan requires no prior authorization for the virtual consult (D9995), radiograph (D0220), root canal (D3310), or composite restoration (D2330). Coverage is simply verified active in real time at I1 — a benefit lookup, not a PA cycle. (Contrast UC02a's Medicaid PA and UC03's HUSKY B D4341 PA.)
- **No diagnostic radiograph / DICOM until I3, and it is never *exchanged*.** The originating provider is virtual and cannot take a radiograph, so there is **no `ImagingStudy`, no WADO-RS, no PACS** at I1/I2. **Patient-submitted intraoral photos *are* exchanged at I1** — but by ARex reference (a manifest of non-radiographic `image/jpeg` `DocumentReference` entries), explicitly not DICOM. The radiograph (`ImagingStudy` + `DiagnosticReport`, DICOM/WADO-RS pointer) first appears **in-office at I3** and stays there — it is **not** pushed or pulled back to Meridian; I4's closed-loop summary is clinical (`ClinicalImpression`/`CarePlan`) and references the radiograph's conclusion, not the image. (Contrast UC02's dental-to-dental support-a-pull for DICOM.)
- **No Plan-Net directory query.** The commercial patient is referred to a known in-network practice; the provider-directory search is UC04b's (Medicaid) test, not UC04a's.
- **No HL7v2 and no IHE 360X bridge.** UC04 is entirely FHIR; routing is a direct CDex push, not a 360X transport (UC01/UC02) or an HIE hub (UC03).

---

## 2. Step-by-Step by Stakeholder

### 2a. Teledentistry Provider / Meridian Teledental (relevant to I1; reporting-back at I4)

1. Load the registry and base tiers first (see [Resource Index](#4-resource-index)).
2. **At I1:** at session start, verify Sarah's coverage in real time against the commercial payer — confirm the virtual consult (D9995) is an active benefit. This is a **benefit lookup, not a CRD/PA hook**; do **not** run an `order-sign` service.
3. Record the virtual `Encounter` (`class: VR`, POS 02), the symptom `Observation` (tooth #9 `bodySite`, discrete symptom components, and `derivedFrom` → the two ARex photo entries), the tobacco-status `Observation`, the dental-home `Observation` (no dental home), the patient-reported `MedicationStatement` and `AllergyIntolerance` (penicillin, rash, moderate), and the provisional `Condition` (K04.01, tooth #9 Universal — **no FDI**).
4. Publish the **patient-submitted intraoral photos** as an **ARex manifest** (`List`) of two content entries (`DocumentReference`, `author` = Patient, `context.encounter` → the virtual `Encounter`, absolute `url`, `size` and a SHA-256 digest; **nothing inline**) with a signed `Provenance`. This is **not** a radiograph — no DICOM, no `ImagingStudy`.
5. Create the referral (`ServiceRequest`, `ode-dental-to-dental-referral`, `priority: urgent`, referral-id `REF-2026-UC04A-001`), carrying `reasonCode` K04.01 + `reasonReference` → the Condition, `bodySite` tooth #9, `supportingInfo` → the three Observations (symptoms, tobacco, dental home) / MedicationStatement / the findings DocumentReference / the ARex manifest, and `insurance` → the Aetna Coverage. **Push it via CDex provider-to-provider** directly to Barton Springs' interim FHIR server — the photos travel **by ARex reference** (Barton Springs retrieves the two image entries and checks each digest; UC02's DICOM support-a-pull is not used).
6. Open the referral-tracking `Task` (`ode-referral-task`, `focus` → the referral, `businessStatus: referral-sent`, `requester` = Meridian); leave `owner` unset until the in-office practice accepts.
7. Write a `Provenance` recording Dr. Webb as author and Meridian as transmitter (CDex push).
8. **At I4:** *receive* the in-office outcome summary Barton Springs pushes back via CDex — a `ClinicalImpression` (+ `CarePlan`) referencing the confirmed diagnoses, the periapical `DiagnosticReport` conclusion, and the D3310 and D2330 procedures. This closes your original referral loop; you are the **single** recipient. The radiograph image itself is **not** re-transmitted — only its clinical conclusion travels in the summary.

### 2b. In-Office Practice / Barton Springs Dental Group PMS (relevant to I2; treatment/report-back/billing at I3–I5)

1. **At I2:** receive the referral `ServiceRequest` on your **interim FHIR server** and resolve its references. The intraoral photos arrive **by ARex reference**: the referral points at a manifest, and you retrieve each image entry and verify its digest (contrast UC02's DICOM support-a-pull). Re-associate the photos to tooth #9 via the symptom `Observation` (`bodySite` + `derivedFrom`).
2. Review, then book the next-morning appointment: create the `Appointment` (`basedOn` the referral, `start` 2026-07-15 10:00) and return an `AppointmentResponse` (accepted) to Meridian via CDex.
3. Advance the referral `Task` to `businessStatus: appointment-confirmed` and set `owner` = Dr. Nair — the **same `Task` `id`**, a new version (sequential `PUT`), not a second Task.
4. Write a `Provenance` for the appointment creation/confirmation (in-office system → teledentistry FHIR).
5. **At I3:** perform the in-office evaluation. Record the in-office `Encounter` (POS 11). Take the **first radiograph** — an `ImagingStudy` (modality IO, tooth #9, `endpoint` → your interim FHIR server as a DICOM/WADO-RS pointer) plus a `DiagnosticReport` (LOINC 62443-7 / CDT D0220) and a findings `Observation`. This image is generated **in-office only** — do **not** push or expose it back to Meridian. Advance the provisional pulpitis `Condition` to **confirmed** (same `id`, new version, encounter → I3), add a new **K04.7** periapical-abscess `Condition`, and record the root canal `Procedure` (D3310, tooth #9, `reasonReference` → both Conditions) and the lingual direct composite `Procedure` (D2330, tooth #9).
6. **At I4:** compose the closed-loop summary — a `ClinicalImpression` (problems, investigation → the D3310 and D2330 Procedures + periapical report, summary text) and a `CarePlan` (definitive crown by a dentist she establishes as her dental home, 6-month follow-up radiograph, ibuprofen PRN). **Push it via CDex** back to Meridian only (one `task-summary-delivery` Task, one `Provenance`, one `AuditEvent`). Advance the referral `Task` to `status: completed` / `businessStatus: outcome-final` and populate `Task.output` (summary, care plan, confirmed Condition, Procedure) — same `id`, a new version.
7. **At I5:** emit your own `ODEOralProfessionalEOB` (`ode-dental-claim`) for the **in-office** treatment — three lines, D0220 + D3310 + D2330 (tooth #9), rendered by Dr. Nair, referred by Dr. Webb, `item.location` → the office (POS 11), diagnoses K04.01 + K04.7, `supportingInfo` → the shared referral, **no PA ref**. This is a **separate** package from Meridian's — tied only by the referral, not a joint claim.

### 2c. Commercial Payer — Aetna Dental (coverage verification only at I1; claims at I5)

1. **At I1:** answer a **real-time benefit verification** — the virtual consult (D9995) is covered; return "benefit active." That is the extent of payer involvement at the referral. **No CRD, no DTR, no PAS, no PA number** — the plan requires none for D9995/D0220/D3310/D2330. Fixed plan benefits live on [`insplan-uc04-commercial-ppo.json`](../fhir-resources/durable/insurance-plans/insplan-uc04-commercial-ppo.json); point-in-time balances are returned by the benefit response, not stored on Coverage.
2. **At I5:** adjudicate the **two independent** claims-sharing packages — [`eob-teledentistry-claims-sharing.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/eob-teledentistry-claims-sharing.json) (Meridian, D9995, POS 02) and [`eob-inoffice-claims-sharing.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/eob-inoffice-claims-sharing.json) (Barton Springs, D0220 + D3310 + D2330, POS 11) — each from a different billing organization for the same episode, both CDT-coded, both to this commercial payer, tied only by the shared referral-id. No PA ref on either.

### 2d. Patient-Facing App Providers (adult self-auth — relevant to I1 and I2)

The app does the same thing throughout — subscribe once, display milestones — so its full guidance is consolidated in the [**Patient-Facing App Companion Guide**](#5-patient-facing-app-companion-guide-adult-self-auth) section below.

---

## 3. Stub Specifications

| Role | Minimum bar |
|---|---|
| **Teledentistry platform stub (Meridian)** | Verify coverage (return "D9995 benefit active"), emit the virtual `Encounter` + clinical resources + the findings `DocumentReference`, the dental-home `Observation` and the intraoral photos as an **ARex manifest** with two image entries, and a `ServiceRequest` referral (with `supportingInfo` and `insurance`) pushed via CDex to the in-office endpoint. No CRD hook. At I4, accept an inbound outcome summary |
| **In-office practice stub (Barton Springs interim FHIR server)** | Accept a pushed `ServiceRequest` (photos arrive by ARex reference — retrieve and verify the two entries), emit an `Appointment` + `AppointmentResponse` (accepted), and update the referral `Task` (`appointment-confirmed`, `owner` set). A fixed acknowledgment per step suffices. At I3–I5, emit the in-office encounter + radiograph (`ImagingStudy`/`DiagnosticReport`, not exchanged back), the D3310 and D2330 procedures, the closed-loop summary (`ClinicalImpression`/`CarePlan`) pushed back to Meridian, and its own in-office EOB |
| **Commercial payer stub (Aetna)** | Answer a real-time benefit check with "virtual consult covered / benefit active" — **no** CRD/PA. At I5, accept the two claims-sharing EOBs |
| **Patient app stub** | Display a status string for the two adult-visible milestones (referral sent @I1; appointment confirmed @I2) via a Backport-IG `Subscription`; confirm it fires nothing for the provider-to-provider mechanics themselves |

---

## 4. Resource Index

### Registry — [`../fhir-resources/durable/`](../fhir-resources/durable/) — load first; reusable across use cases

| File | Type | Purpose |
|---|---|---|
| [`org-meridian-teledental.json`](../fhir-resources/durable/organizations/org-meridian-teledental.json) | Organization | **Meridian Teledental** — fictional teledentistry brand (virtual, POS 02); referring provider org |
| [`org-barton-springs-dental.json`](../fhir-resources/durable/organizations/org-barton-springs-dental.json) | Organization | **Barton Springs Dental Group** — fictional in-office general practice, Austin (POS 11); receiving provider org |
| [`org-uc04-commercial-payer.json`](../fhir-resources/durable/organizations/org-uc04-commercial-payer.json) | Organization | **Aetna Dental** — the real commercial payer named in the source (synthetic EDI/endpoint) |
| [`pract-webb.json`](../fhir-resources/durable/practitioners/pract-webb.json) | Practitioner | Dr. Marcus Webb, DDS — teledentistry (referring) |
| [`pract-nair.json`](../fhir-resources/durable/practitioners/pract-nair.json) | Practitioner | Dr. Priya Nair, DDS — in-office (receiving) |
| [`loc-meridian-virtual.json`](../fhir-resources/durable/locations/loc-meridian-virtual.json) | Location | Meridian virtual-care location (POS 02, telehealth — no physical site) |
| [`loc-barton-springs.json`](../fhir-resources/durable/locations/loc-barton-springs.json) | Location | Barton Springs office (POS 11), Austin |
| [`endpoint-meridian-teledental.json`](../fhir-resources/durable/endpoints/endpoint-meridian-teledental.json) | Endpoint | Meridian Teledental FHIR API |
| [`endpoint-barton-springs.json`](../fhir-resources/durable/endpoints/endpoint-barton-springs.json) | Endpoint | Barton Springs **interim FHIR server** (CDex push target) |
| [`endpoint-uc04-commercial-payer.json`](../fhir-resources/durable/endpoints/endpoint-uc04-commercial-payer.json) | Endpoint | Aetna Dental FHIR API (benefit verification) |
| [`insplan-uc04-commercial-ppo.json`](../fhir-resources/durable/insurance-plans/insplan-uc04-commercial-ppo.json) | InsurancePlan | Aetna Dental PPO benefit (teledentistry + endodontic; $2,000 annual max, $50 deductible; **no PA**) |

### Base — [`../fhir-resources/purpose-built/uc04a-teledentistry-commercial/base/`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/base/) — load second; UC04a-specific

| File | Type | Purpose |
|---|---|---|
| [`patient-sarah-okonkwo.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/base/patients/patient-sarah-okonkwo.json) | Patient | Sarah Okonkwo — adult; teledentistry patient-id + Barton Springs MRN |
| [`coverage-sarah-okonkwo-ppo.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/base/coverage/coverage-sarah-okonkwo-ppo.json) | Coverage | Aetna Dental PPO; member AET-TX-00284711, group 847221; `payor` → the commercial payer org |
| [`role-webb.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/base/practitioner-roles/role-webb.json) | PractitionerRole | Dr. Webb @ Meridian (general dentistry 1223G0001X, POS 02) |
| [`role-nair.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/base/practitioner-roles/role-nair.json) | PractitionerRole | Dr. Nair @ Barton Springs (general dentistry 1223G0001X, POS 11) |
| [`subscription-sarah-referral-status.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/base/subscriptions/subscription-sarah-referral-status.json) | Subscription | **Adult self-auth** app subscription; milestones referral-sent (I1) + appointment-confirmed (I2) + referral-complete / visit summary available (I4). No PA milestone (commercial no-PA) |

### Interaction 1 — [`.../interactions/interaction-01/`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/) — 2026-07-14 virtual encounter

| File | Type | Purpose |
|---|---|---|
| [`encounter-01-virtual.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/encounter-01-virtual.json) | Encounter | The 2026-07-14 virtual consult (Dr. Webb, Meridian, `class: VR`, POS 02, 19:32–19:58) |
| [`condition-k04-01-pulpitis.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/condition-k04-01-pulpitis.json) | Condition | Irreversible pulpitis (ICD-10-CM **K04.01**), tooth #9 (Universal — **no FDI**), **provisional** — radiographic confirmation deferred to I3 |
| [`observation-symptoms.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/observation-symptoms.json) | Observation | Symptom findings as components (duration, pain on biting, thermal sensitivity, spontaneous aching); `bodySite` tooth #9; **`derivedFrom` → the two ARex photo entries** (the R4 tooth-correlation work-around) |
| [`observation-tobacco-status.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/observation-tobacco-status.json) | Observation | Tobacco smoking status (LOINC 72166-2; SNOMED "Never smoked tobacco") — `us-core-smokingstatus` |
| [`medicationstatement-ibuprofen.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/medicationstatement-ibuprofen.json) | MedicationStatement | Patient-reported OTC ibuprofen for the pain (RxNorm ingredient 5640) |
| [`allergyintolerance-penicillin.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/allergyintolerance-penicillin.json) | AllergyIntolerance | Patient-reported penicillin allergy (SNOMED 91936005), reaction rash, severity moderate, `unconfirmed`; in the referral's `supportingInfo` |
| [`documentreference-virtual-findings.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/documentreference-virtual-findings.json) | DocumentReference | Text clinical-note wrapper for the virtual assessment — **not an image** |
| [`arex-manifest-intraoral-photos.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/arex-manifest-intraoral-photos.json) | List (ARex manifest) | **Patient-submitted intraoral photos, by reference**: lists the two image entries; transaction-context business identifier = the referral id `REF-2026-UC04A-001`; expires 14 days after publication (assumed); the referral's `supportingInfo` points here |
| [`arex-entry-photo-1.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/arex-entry-photo-1.json), [`arex-entry-photo-2.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/arex-entry-photo-2.json) | DocumentReference (ARex content entries) | One per photo: `image/jpeg`, absolute `url`, `size`, SHA-256 `arex-digest` (real, over the files in [`arex-payloads/`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/arex-payloads/)), `author` = Patient; **not DICOM**; the files are 8×8 placeholder JPEGs |
| [`arex-provenance-intraoral-photos.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/arex-provenance-intraoral-photos.json) | Provenance | Signs the manifest; the detached JWS is a **placeholder** to be regenerated at test time |
| [`observation-dental-home.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/observation-dental-home.json) | Observation | Patient-reported dental history: no dental home, has not seen a dentist in some time (text only; no date asserted) |
| [`servicerequest-referral.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/servicerequest-referral.json) | ServiceRequest | The referral — `ode-dental-to-dental-referral`, `REF-2026-UC04A-001`, `priority: urgent`, `reasonCode` K04.01, `supportingInfo` → 3 Observations (symptoms, tobacco, dental home) / MedicationStatement / the findings DocumentReference / the ARex manifest, `insurance` → Coverage, `occurrenceDateTime` 2026-07-15; **no PA**, photos travel **by ARex reference** |
| [`task-referral-tracking.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/task-referral-tracking.json) | Task | `ode-referral-task`, `focus` → referral, `businessStatus: referral-sent`, no `owner` yet; **CDex push, not HIE/360X** |
| [`provenance-referral.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/provenance-referral.json) | Provenance | Author Dr. Webb (Meridian); transmitter Meridian (CDex provider-to-provider) |
| [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/interaction-01-bundle.json) | Bundle | Self-contained transaction: registry + base + I1 (**26 entries**) |

### Interaction 2 — [`.../interactions/interaction-02/`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-02/) — 2026-07-14 same-evening scheduling

| File | Type | Purpose |
|---|---|---|
| [`appointment-inoffice.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-02/appointment-inoffice.json) | Appointment | `status: booked`, `basedOn` the referral, `start` 2026-07-15 10:00; participants Sarah + Dr. Nair + location; created 20:47 |
| [`appointmentresponse-inoffice.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-02/appointmentresponse-inoffice.json) | AppointmentResponse | Accepted, returned to Meridian via CDex the same evening |
| [`task-referral-tracking-accepted.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-02/task-referral-tracking-accepted.json) | Task | **Snapshot** of the I1 referral Task → `businessStatus: appointment-confirmed`, `owner` = Dr. Nair (same `id` — version history) |
| [`provenance-appointment.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-02/provenance-appointment.json) | Provenance | Author Dr. Nair (Barton Springs); transmitter Barton Springs (CDex back to Meridian) |
| [`interaction-02-bundle.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-02/interaction-02-bundle.json) | Bundle | Self-contained transaction: registry + base + I1 + I2 (**29 entries**; the I2 Task snapshot overrides the I1 Task by shared `id`) |

### Interaction 3 — [`.../interactions/interaction-03/`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/) — 2026-07-15 in-office root canal (first radiograph)

| File | Type | Purpose |
|---|---|---|
| [`encounter-03-inoffice.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/encounter-03-inoffice.json) | Encounter | In-office visit (Dr. Nair, Barton Springs, `class: AMB`, POS 11, 10:00–12:15), `basedOn` the referral |
| [`imagingstudy-periapical.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/imagingstudy-periapical.json) | ImagingStudy | Periapical radiograph, modality IO, tooth #9; `endpoint` → the in-office interim server as a **DICOM/WADO-RS pointer** (metadata only, real bytes on PACS); **in-office-only, not exchanged back to Meridian** |
| [`diagnosticreport-periapical.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/diagnosticreport-periapical.json) | DiagnosticReport | LOINC 62443-7 / CDT D0220; `imagingStudy` → above; conclusion = periapical rarefaction consistent with abscess |
| [`observation-periapical-findings.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/observation-periapical-findings.json) | Observation | Radiographic findings (tooth #9), `derivedFrom` → the DiagnosticReport (text-only components) |
| [`condition-k04-01-pulpitis-confirmed.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/condition-k04-01-pulpitis-confirmed.json) | Condition | **Snapshot** of the I1 pulpitis Condition (same `id`) → `verificationStatus: confirmed`, encounter/asserter → in-office |
| [`condition-k04-7-periapical-abscess.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/condition-k04-7-periapical-abscess.json) | Condition | New in-office diagnosis — **K04.7** periapical abscess without sinus, tooth #9 (source's "K04.5" corrected) |
| [`procedure-d3310-rootcanal.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/procedure-d3310-rootcanal.json) | Procedure | CDT **D3310** root canal (anterior), tooth #9 (Universal — **no FDI**), completed 2026-07-15, `reasonReference` → both Conditions |
| [`procedure-d2330-composite.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/procedure-d2330-composite.json) | Procedure | CDT **D2330** single-surface direct composite (lingual), tooth #9, same visit; restores the access — a crown is still indicated |
| [`interaction-03-bundle.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/interaction-03-bundle.json) | Bundle | Self-contained transaction: registry + base + I1 + I2 + I3 (**35 entries**; confirmed Condition and appointment-confirmed Task override earlier versions by shared `id`) |

### Interaction 4 — [`.../interactions/interaction-04/`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/) — 2026-07-15 closed-loop summary

| File | Type | Purpose |
|---|---|---|
| [`clinicalimpression-summary.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/clinicalimpression-summary.json) | ClinicalImpression | Encounter summary (Dr. Nair → Dr. Webb); `problem` K04.01/K04.7, `investigation` → D3310 + D2330 + periapical report, full summary text |
| [`careplan-posttreatment.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/careplan-posttreatment.json) | CarePlan | Definitive crown by a dentist she establishes as her dental home (she has none yet), 6-month follow-up radiograph, ibuprofen PRN |
| [`servicerequest-referral-completed.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/servicerequest-referral-completed.json) | ServiceRequest | **Snapshot** of the referral (same `id`) → `status: completed` |
| [`task-referral-tracking-completed.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/task-referral-tracking-completed.json) | Task | **Snapshot** of the referral Task (same `id`) → `status: completed`, `businessStatus: outcome-final`, `output` → summary + care plan + confirmed Condition |
| [`task-summary-delivery.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/task-summary-delivery.json) | Task | Single CDex summary-delivery Task (Barton Springs → Meridian; `focus` → the ClinicalImpression) |
| [`provenance-summary.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/provenance-summary.json) | Provenance | Author Dr. Nair (Barton Springs); transmitter Barton Springs (CDex push to Meridian) |
| [`auditevent-summary.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/auditevent-summary.json) | AuditEvent | Cross-org access log for the summary push (Barton Springs → Meridian) |
| [`interaction-04-bundle.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/interaction-04-bundle.json) | Bundle | Self-contained transaction: registry + base + I1–I4 (**40 entries**; completed Task/ServiceRequest override earlier versions) |

### Interaction 5 — [`.../interactions/interaction-05/`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/) — 2026-07-16 two-organization claims-sharing

| File | Type | Purpose |
|---|---|---|
| [`procedure-d9995-teledentistry.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/procedure-d9995-teledentistry.json) | Procedure | CDT **D9995** synchronous teledentistry, POS 02, Dr. Webb, `encounter` → the I1 virtual Encounter — the billable virtual consult |
| [`eob-teledentistry-claims-sharing.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/eob-teledentistry-claims-sharing.json) | ExplanationOfBenefit | **EOB #1** (`ode-dental-claim`): insurer Aetna, provider Meridian, one line D9995 (POS 02), diagnosis K04.01, `supportingInfo` → referral; **no PA** |
| [`eob-inoffice-claims-sharing.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/eob-inoffice-claims-sharing.json) | ExplanationOfBenefit | **EOB #2** (`ode-dental-claim`): insurer Aetna, provider Barton Springs, referring Dr. Webb + rendering Dr. Nair, three lines D0220 + D3310 + D2330 (POS 11, tooth #9), diagnoses K04.01 + K04.7, `supportingInfo` → same referral; **no PA** |
| [`interaction-05-bundle.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/interaction-05-bundle.json) | Bundle | Self-contained transaction: registry + base + I1–I5 (**43 entries**) |

---

## 5. Patient-Facing App Companion Guide (adult self-auth)

Unlike the teledentistry platform, the in-office practice, and the payer — whose actions differ by interaction — Sarah's app does fundamentally the **same thing** throughout: subscribe once, then receive and display milestones as the referral progresses. **Sarah is an adult**, so this is a straightforward **self-authorized** SMART App Launch — no guardian/proxy flow (contrast UC03's minor patient).

### What to build

1. **A `Subscription`** to the referral's status changes — matching [`subscription-sarah-referral-status.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/base/subscriptions/subscription-sarah-referral-status.json). It is a Backport-IG `rest-hook` subscription whose `criteria` carries the `SubscriptionTopic` canonical (`.../SubscriptionTopic/ode-referral-status`) directly — same pattern as UC01/UC02/UC03. Built once, early.
2. **A notification handler** that translates the underlying `Task.status`/`businessStatus` into plain-language milestones — never raw FHIR codes.

### Milestone-by-milestone: what the app shows, and what's driving it

| When | What Sarah sees | What's actually happening (Task field) |
|---|---|---|
| I1 (2026-07-14 evening) | "Your referral has been sent to Barton Springs Dental Group" | [`task-referral-tracking.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/task-referral-tracking.json): `status: in-progress`, `businessStatus: referral-sent`; `owner` not set yet |
| I2 (2026-07-14, ~8:47 PM) | "Appointment confirmed — tomorrow, 10:00 AM" | [`task-referral-tracking-accepted.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-02/task-referral-tracking-accepted.json): `businessStatus: appointment-confirmed`; `owner` = Dr. Nair |
| I4 (2026-07-15 midday) | "Your dental visit summary is available" | [`task-referral-tracking-completed.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/task-referral-tracking-completed.json): `status: completed`, `businessStatus: outcome-final` |

**The one thing worth testing deliberately:** whether the app fires on the real referral milestones (referral sent @I1, appointment confirmed @I2) and correctly reflects the **under-an-hour, same-evening turnaround** — referral to confirmed appointment inside one evening, not "sometime tomorrow."

### Credentials and stubs

Full Patient Access API testing needs real SMART App Launch registration (client ID/secret, redirect URIs, scopes) against whichever FHIR server holds Sarah's data — treat client secrets as real secrets even in a sandbox. For the minimum bar, see the patient app row in [Section 3](#3-stub-specifications): a stub only needs to display a status string per milestone.

---

## 6. Tooling — what you need to actually run this

UC04a is **entirely FHIR** — unlike UC01, there is **no HL7v2/wire-level artifact** (no MLLP, no interface engine, no HL7v2 parser) anywhere. For I1/I2 there is **no DICOM imaging at all**, and even at I3 the radiograph is generated **in-office only** and **never exchanged** — so, unlike UC02, there is **no support-a-pull / WADO-RS / PACS *between organizations*** at any point. What you need is a FHIR server, a CDex provider-to-provider push, real-time coverage verification, retrieval of patient-submitted images by ARex reference (I1), a local DICOM/`ImagingStudy` pointer (I3), and the claims-sharing EOB profile (I5).

### 6a. FHIR services

- **A FHIR R4 server** to load resources onto: **HAPI FHIR** or **OnyxOS**. Any R4-conformant server works. Note the "in-office practice" here is explicitly modeled with an **interim FHIR server** — a practice without a native FHIR PMS stands one up to receive the CDex push.
- **Loading:** each file has a fixed `id` — `PUT [base]/{ResourceType}/{id}` per the load order (Registry → Base → Interaction), or `POST` an interaction bundle ([`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/interaction-01-bundle.json), [`interaction-02-bundle.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-02/interaction-02-bundle.json)) as a single transaction.
- **Profile validation:** the official **HL7 FHIR Validator CLI** checks a resource against its declared `meta.profile`; **Inferno** covers US Core and SMART App Launch (relevant to the adult self-auth flow). Our own checks were structural/cross-reference only — run the validator before the Connectathon if strict conformance will be checked.
- **CDex provider-to-provider push.** The referral (I1) and the appointment confirmation (I2) are direct pushes between the teledentistry platform and the in-office interim FHIR server — no HIE hub, no 360X bridge. A simple authenticated `POST` of a transaction bundle to the peer endpoint exercises this.
- **Real-time coverage verification** at I1 — a benefit lookup returning "D9995 covered / active," **not** a CRD `order-sign` hook. No Da Vinci PA stack is needed for UC04a.

### 6b. The intraoral-photo hop (the one novel piece)

The one thing UC04a exercises that the others don't is a **patient-submitted, non-radiographic image** riding along with the referral:

1. **Image transport by ARex reference.** The photos are not carried inline. Meridian publishes an ARex manifest (a `List`) with two content entries (`DocumentReference`, each with an absolute `url`, `size` and SHA-256 `arex-digest`) and a signed `Provenance`; the referral's `supportingInfo` points at the manifest, whose business identifier is the referral id. Barton Springs retrieves each entry and verifies its digest. In the test data the payload files are 8×8 placeholder JPEGs, the URLs are synthetic and the signature is a placeholder.
2. **Tooth correlation without `bodySite`.** R4 `DocumentReference` has no `bodySite`, so the affected tooth rides on the symptom `Observation` (`bodySite` tooth #9) which points at the photo via `derivedFrom`. Any consumer that wants "which tooth is this photo?" reads it off the Observation, not the DocumentReference.
3. **Not DICOM.** No DICOMweb server, no PACS, no WADO-RS, no viewer — those belong to the **radiograph** at I3, a different artifact entirely.

**Explicitly not needed for I1/I2:** DICOMweb server, PACS (Orthanc/dcm4chee), WADO-RS, DICOM viewer, MLLP/interface engine, HL7v2 validator, Plan-Net directory service, any CRD/DTR/PAS service.

### 6c. Imaging at I3 (in-office only, not exchanged)

The first — and only — radiograph in UC04a appears in-office at I3, and it never crosses an organizational boundary, so the imaging tooling here is **local to Barton Springs**, not an exchange stack:

1. **`ImagingStudy` is a pointer, not the image.** Per HL7's own spec, [`imagingstudy-periapical.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/imagingstudy-periapical.json) carries DICOM Study/Series UIDs and an `endpoint` (the interim server as a **WADO-RS** base URL); the real pixel data lives as DICOM on a PACS. The accurate stack when imaging is discussed is **`ImagingStudy` (FHIR pointer) → DICOM/WADO-RS (the image + retrieval)** — but here it is entirely **in-office**.
2. **Nothing to pull cross-org.** Because the image isn't exchanged, there is **no support-a-pull, no cross-org WADO-RS call, no PACS federation** to test. I4's summary carries the [`diagnosticreport-periapical.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/diagnosticreport-periapical.json) *conclusion* to Meridian, not the image. If you want to exercise a real DICOM/WADO-RS pull between organizations, that's UC02's dental-to-dental support-a-pull, not this one.

### 6d. Claims-sharing at I5

The two [`ExplanationOfBenefit`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/) packages are `ODEOralProfessionalEOB` (`ode-dental-claim`) — the CARIN Blue Button-derived, oral-optimized claims-sharing shape. No adjudication/financials are modeled (non-financial by design). The test is that the **same profile shape** holds when emitted **twice, independently**, by two different billing organizations for one episode — CDT only, no CPT crosswalk (dental payer), no PA ref (commercial no-PA). A stub only needs to accept both packages.

---

## 7. What to do if something doesn't match

Check this guide's [Resource Index](#4-resource-index) and the interaction writeups first. If a resource doesn't match what your system expects, it's either a documented design decision — **no CRD/PA** (commercial no-PA), **virtual origin so no radiograph until I3**, **patient photos by ARex reference** (US Core-style `DocumentReference` entries, not `Media`, not DICOM), a **direct CDex push** (not HIE/360X), or **no Plan-Net/HL7v2** — or genuinely new, in which case flag it rather than silently working around it. A few specific things to expect rather than treat as errors:

- **The intraoral photos are a `DocumentReference`, not a `Media`** — a deliberate standards decision (R4 → R6 forward compatibility, US Core conformance, 360X/C-CDA behavior; see the header note). If your model expected `Media.bodySite` for the tooth, that correlation lives on [`observation-symptoms.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/observation-symptoms.json) (`bodySite` + `derivedFrom`) instead, because R4 `DocumentReference` has no `bodySite`.
- **The photo payloads are 8×8 placeholder JPEGs behind synthetic `example.org` URLs, and the manifest signature is a placeholder.** That's intentional — the pattern is ARex retrieval with digest verification; a real submission serves the full photos and carries a valid detached JWS.
- **The `Condition` is `provisional`, not `confirmed`** — a virtual visit can't radiographically confirm irreversible pulpitis. Confirmation is I3 work.
- **Tooth #9 is Universal numbering; FDI is deliberately not asserted** anywhere (per ADA confirmation that FDI isn't used for US dental data). The source doc's "FDI 21" label is a separately-flagged error, not reproduced in the resources.
- **No CRD card / PA number anywhere** — commercial no-PA. Coverage is verified active in real time at I1; there is no `Claim`/`ClaimResponse` PA cycle (contrast UC02a/UC03).
- **Text-only codes by design (project verification discipline):** the symptom `Observation` code and the `MedicationStatement` (RxNorm ingredient only, since the OTC product was patient-reported). If your validator wants a more specific code there, that's the reason.
- **The referral `Task` is one Task across I1→I4** — [`task-referral-tracking.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/task-referral-tracking.json) (referral-sent), [`task-referral-tracking-accepted.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-02/task-referral-tracking-accepted.json) (appointment-confirmed), and [`task-referral-tracking-completed.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-04/task-referral-tracking-completed.json) (outcome-final) all share one `id` (sequential `PUT`s, version history), not three Tasks. Load them in interaction order; `owner` is set for the first time at I2. The separate `task-summary-delivery` at I4 is a *different* Task (CDex delivery), deliberately distinct from the referral Task.
- **The `K04.7` periapical-abscess code is intentional** — the source doc's "K04.5" is a mislabel (K04.5 is chronic apical periodontitis). The I3/I5 resources use **K04.7** ("periapical abscess without sinus"); the source doc has been corrected. Expect K04.7, not K04.5.
- **The I3 radiograph is in-office-only and is not exchanged** — [`imagingstudy-periapical.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/imagingstudy-periapical.json) / [`diagnosticreport-periapical.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-03/diagnosticreport-periapical.json) exist at Barton Springs but are not pushed/pulled to Meridian. If you expected the image to reach the teledentistry provider, it doesn't — only its clinical conclusion does, via the I4 summary.
- **The D9995 teledentistry `Procedure` lives in the I5 folder, not I1** — [`procedure-d9995-teledentistry.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/procedure-d9995-teledentistry.json) references the I1 virtual `Encounter` but is filed under I5 (the billing interaction that needs it), to avoid churning the already-committed I1/I2 bundles. Clinically it belongs to the I1 encounter it points at.
- **There are two independent EOBs at I5, not one joint claim** — [`eob-teledentistry-claims-sharing.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/eob-teledentistry-claims-sharing.json) and [`eob-inoffice-claims-sharing.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-05/eob-inoffice-claims-sharing.json) are separate packages from two billing organizations, tied only by the shared referral-id. No financial/adjudication fields (non-financial profile by design).

All persons are fictional and both provider organizations are fictional; **Aetna Dental** is the real payer named in the source, with synthetic EDI/endpoint identifiers. All MRNs, NPIs, member IDs, and licenses are synthetic placeholders.

---

## 8. Test Server Roles — November Connectathon (DRAFT for owner review)

> **Status (2026-11-04):** the OHIA test server is **not deployed yet**. Everything marked **Planned** is intended behavior, not tested behavior. Everything marked **TBD** is undecided and is not a default. This section does not change §1–§7; where it conflicts with them, the conflict is called out below.

### 8.0 Purpose and precedence

For the November connectathon, **the interaction in this section overrides the use-case narrative wherever they differ.** Its purpose is to **get initial connectivity working** between participants and the test server. The fuller capabilities described elsewhere in this guide (the appointment and outcome exchange in I2 and I4, the in-office radiograph in I3, claims sharing in I5, and the patient app) are **not tested in this iteration and will be added in later iterations.**

### 8.1 What the test server is

One FHIR R4 test server (HAPI FHIR on PostgreSQL), synthetic data only. For UC04a it plays **both the teledentistry platform (Meridian Teledental) and the in-office PMS (Barton Springs' interim FHIR server)**, so a participant can take either side. Public base URL(s): **TBD**. Authentication: **TBD**.

### 8.2 Scope

Only **Interaction 1 — Tuesday Night Pain** (teledentistry platform to PMS: the referral request and the images) is on the connectathon list given by the owner. I2–I5 are **not** on that list and are not covered by this section. The patient-facing app in §5 is **optional** for this event. Whether any of I2–I5 should be added is **TBD**.

### 8.3 Who plays what in I1

| You play | The test server plays | What is exchanged |
|---|---|---|
| **Teledentistry platform** (Meridian) | **In-office PMS** (Barton Springs) | You send the referral and images; the server receives them |
| **In-office PMS** (Barton Springs) | **Teledentistry platform** (Meridian) | The server sends the referral and images to your endpoint |

### 8.4 If you play the teledentistry platform

- *You do:* follow §2a steps 3–6 and push the referral by CDex provider-to-provider push — a `POST` of a transaction Bundle to the test server's PMS endpoint. The existing [`interaction-01-bundle.json`](../fhir-resources/purpose-built/uc04a-teledentistry-commercial/interactions/interaction-01/interaction-01-bundle.json) is a good reference payload. It is a `transaction` Bundle of 31 entries, all `PUT`, and it already contains the durable and base resources as well as the I1 resources. Its referral carries the `ode-dental-to-dental-referral` profile with `priority: urgent`. It also includes the patient-app `Subscription`; whether to send that to the server is **TBD**.
- *The test server does (Planned):* accepts and stores the entries, returns validation feedback (8.6), and lets you read the stored referral and its `Task` back.
- *Success looks like:* the transaction response reports each entry created, and a `GET` returns the referral, the ARex manifest with its two entries, and the tracking `Task`.

### 8.5 If you play the in-office PMS

- *You do:* publish an endpoint that accepts a pushed transaction Bundle (§2b step 1), and give the test server team its base URL and any credentials.
- *The test server does (Planned, **TBD**):* sends the I1 referral package to your endpoint. This needs an outbound client on the server side, which is **not built**. Which payload it sends is **TBD**.

### 8.6 Images and validation feedback

- **Images (owner's decision):** the intraoral photos travel **by ARex reference** (a manifest of two image entries), not inline, in keeping with the decision that **ARex carries all attachments and imaging at this event** (§6b). The test server retrieving the entries from a participant's ARex content endpoint and checking each digest is **Planned, TBD**; the payload files in the repository are placeholders behind synthetic URLs.
- **Validation feedback.** For ODE referral content the test server **validates against the draft ODE profiles but always accepts and stores the submission, and returns the validation results in the response.** A validation error is a finding about the draft, not a rejection. The response format is **TBD**.

### 8.7 What you must prepare

- Your payload (the reference bundle above, or your own).
- The test server's base URL(s) and credentials: **TBD**, to be published before the event.
- A policy on resets: logical IDs are reused across scenarios in this repository (see `CLAUDE.md` §6), and whether the server is reset between participants is **TBD**.

### 8.8 Open items on this section

| Item | Owner | Status |
|---|---|---|
| Base URLs and authentication | Test server team | TBD |
| Outbound sending by the test server (8.5) | Test server team | Not built |
| Photos inline vs ARex | Owner | Decided: ARex, two entries |
| The referral's allergy (owner, 2026-11-12: penicillin, rash, moderate) is authored as `AllergyIntolerance`; its verification status `unconfirmed` and the absence of a criticality are assumptions | Owner | Decided; assumptions to confirm |
| The three failing UC04a NPIs in the data (Meridian, Barton Springs, Dr. Webb) were fixed by changing only the check digit (owner, 2026-11-12). The narrative's Appendix A lists four DIFFERENT NPIs, all of which fail the Luhn check, so the data and the narrative disagree | Owner | Narrative NPIs open |
| Whether any of I2–I5 are in scope (the patient app is optional) | Owner | TBD |
| Reset policy between participants | Owner | TBD |
