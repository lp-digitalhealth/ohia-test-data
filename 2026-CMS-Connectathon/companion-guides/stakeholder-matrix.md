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
| UC03 | *(not yet designed)* | — | — | — | — | — | — | — | UC03 (pediatric referral) not yet reviewed. |
| UC04 | *(not yet designed)* | — | — | — | — | — | — | — | UC04 (teledentistry referral) not yet reviewed. |
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
