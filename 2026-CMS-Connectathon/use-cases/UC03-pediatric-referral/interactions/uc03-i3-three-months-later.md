# UC03-I3: Three Months Later

**Corresponds to:** 2026-05-28.

## What happens

Timothy comes in with his grandparents, and Dr. Watson already knows what he's walking into — the diabetes, the medications, the CGM, the gingivitis finding from three months earlier. He does a comprehensive oral evaluation and a periodontal risk assessment. What he finds confirms the concern Dr. Smith had back in February: the gingivitis has progressed. This is no longer just gingivitis — it's early-stage aggressive periodontitis, localized and slight, but real, and unusual to see in a six-year-old (aggressive, not chronic: chronic periodontitis is a slow adult disease, whereas the rapid breakdown seen here in a child with poorly controlled Type 1 diabetes is the aggressive pattern — ICD-10-CM K05.211). It's consistent with exactly the accelerated trajectory poorly controlled Type 1 diabetes is known to cause.

Dr. Watson's treatment plan is scaling and root planing (SRP) across two quadrants, plus a localized chlorhexidine chip at the affected sites to reduce the bacterial load. **This is where the coverage-requirements machinery finally fires** — unlike the covered evaluation that drove the I1 referral, **SRP (D4341) requires prior authorization** under HUSKY B. When Dr. Watson signs the SRP order, a **CRD** check surfaces that PA requirement; **Gainwell**'s **DTR** questionnaire is completed from the record already on hand (diabetes, the progressed periodontal findings, the PRA), and a **PAS** request goes in and comes back approved. With PA in hand, Dr. Watson performs the SRP on both quadrants and places the chlorhexidine chip. His hygienist spends time with both Timothy and his grandmother on oral hygiene — brushing technique, flossing, age-appropriate toothpaste — and sends them home with a toothbrush, toothpaste, and floss.

The routing/adjudication split is the same as everywhere else in UC03: the CRD/DTR/PAS traffic is **routed through Connie** and the requirements are held on the Connie/**BeneCare** (CTDHP ASO) side, but **Gainwell** — the DSS fiscal agent — is what actually runs DTR/PAS and adjudicates. There is no MCO in the chain.

## What Timothy's Guardians See (patient-facing)

📱 **Notification:** *(none fires during the visit itself — the next notification comes once the encounter summaries go out, in Interaction 4)*

## Key resources exchanged in this interaction

- `Encounter` (the dental visit itself)
- `DiagnosticReport` — the periodontal risk assessment
- `Observation` — periodontal findings per site, and tooth development status (Timothy has a mix of primary and permanent teeth present at once, which the source doc calls out specifically as a modeling consideration for ODE)
- `Condition` — K05.211 (aggressive periodontitis, localized, slight), newly confirmed and asserted here
- **Prior-authorization cycle for the SRP** — `ServiceRequest` (D4341 SRP order that triggers CRD), `QuestionnaireResponse` (the completed DTR), `Claim` + `ClaimResponse` (the PAS request/approval, carrying the `preAuthRef`), and a PA-tracking `Task`. The I1 referral `Task` also advances here (owner set, `in-progress`).
- `Procedure` — D0150 (comprehensive oral evaluation), **D4341 scaling & root planing modeled as two separate `Procedure` resources, one per quadrant** (see decision note below), D4381 (chlorhexidine delivery), D1330 (oral hygiene instructions)
- `MedicationAdministration` — the chlorhexidine 2.5% chip itself, as an in-office administration record
- `Communication` — the oral hygiene education delivered to the guardian

**Resolved decision — D4341 is two `Procedure` resources, two billed lines.** SRP (D4341) is billed "per quadrant," and two quadrants were treated. The source doc's appendix listed it as a single entry with both quadrants under one `Body Site` field, but we model it to match CDT billing granularity: **two separate `Procedure` resources**, which flow through as **two EOB line items** in I5. (This supersedes the earlier "one-vs-two, undecided" flag.)

**Still genuinely open — D4381 coverage.** Whether the localized chlorhexidine delivery (D4381) is covered at all under the HUSKY B pediatric dental benefit is not resolved by the source doc and is not asserted here; it is carried forward and flagged as coverage-uncertain in the I5 claims-sharing package rather than assumed either way.

## Why this matters for testing

Beyond the clinical procedures themselves, this interaction tests whether ODE's oral health profiles can represent a genuinely pediatric clinical picture — mixed dentition, periodontal disease in a population it's not typically associated with, and a confirmed diagnosis that's directly connected to a systemic condition rather than a standalone dental finding. It is also **UC03's prior-authorization proof point**: the full CRD → DTR → PAS cycle exercised against the HUSKY B fiscal-agent model (Connie-routed, Gainwell-adjudicated) for a procedure (D4341) that genuinely requires PA — the counterpart to UC01/UC02a's PA cycles, in a pediatric Medicaid dental context. The periodontal risk assessment itself is also where this project's third named terminology gap lives: there's no established LOINC code for a structured PRA score, which the source doc calls out explicitly as its own ODE IG action item.

## What's deliberately NOT part of this interaction

Telling anyone else what happened — Dr. Smith and the endocrinologist don't get word of this yet. That's Interaction 4.
