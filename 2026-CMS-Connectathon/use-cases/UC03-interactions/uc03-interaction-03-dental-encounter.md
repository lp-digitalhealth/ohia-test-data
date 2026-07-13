# UC03 — Interaction 3: The Dental Encounter

**Corresponds to:** 2026-05-28.

## What happens

Timothy comes in with his grandparents, and Dr. Watson already knows what he's walking into — the diabetes, the medications, the CGM, the gingivitis finding from three months earlier. He does a comprehensive oral evaluation and a periodontal risk assessment. What he finds confirms the concern Dr. Smith had back in February: the gingivitis has progressed. This is no longer just gingivitis — it's early-stage chronic periodontitis, localized and slight, but real, and unusual to see in a six-year-old. It's consistent with exactly the accelerated trajectory poorly controlled Type 1 diabetes is known to cause.

Dr. Watson treats it: scaling and root planing across two quadrants, then a localized chlorhexidine chip placed at the affected sites to reduce the bacterial load. His hygienist spends time with both Timothy and his grandmother on oral hygiene — brushing technique, flossing, age-appropriate toothpaste — and sends them home with a toothbrush, toothpaste, and floss.

## What Timothy's Guardians See (patient-facing)

📱 **Notification:** *(none fires during the visit itself — the next notification comes once the encounter summaries go out, in Interaction 4)*

## Key resources exchanged in this interaction

- `Encounter` (the dental visit itself)
- `DiagnosticReport` — the periodontal risk assessment
- `Observation` — periodontal findings per site, and tooth development status (Timothy has a mix of primary and permanent teeth present at once, which the source doc calls out specifically as a modeling consideration for ODE)
- `Condition` — K05.21 (chronic periodontitis, localized, slight), newly confirmed and asserted here
- `Procedure` — D0150 (comprehensive oral evaluation), D4381 (chlorhexidine delivery), D1330 (oral hygiene instructions)
- `MedicationAdministration` — the chlorhexidine 2.5% chip itself, as an in-office administration record
- `Communication` — the oral hygiene education delivered to the guardian

**One thing genuinely unresolved, flagged rather than assumed:** the scaling and root planing (D4341) is billed "per quadrant," and two quadrants were treated — which by CDT billing convention usually means two separate service lines. But the source doc's own appendix describes this as a single `Procedure` entry with both quadrants listed under one `Body Site` field. Whether this should be **one `Procedure` resource covering both quadrants, or two separate `Procedure` resources** (matching the billing granularity) isn't settled by the source doc, and I haven't decided it here — worth resolving before building, not defaulting to either silently.

## Why this matters for testing

Beyond the clinical procedures themselves, this interaction tests whether ODE's oral health profiles can represent a genuinely pediatric clinical picture — mixed dentition, periodontal disease in a population it's not typically associated with, and a confirmed diagnosis that's directly connected to a systemic condition rather than a standalone dental finding. The periodontal risk assessment itself is also where this project's third named terminology gap lives: there's no established LOINC code for a structured PRA score, which the source doc calls out explicitly as its own ODE IG action item.

## What's deliberately NOT part of this interaction

Telling anyone else what happened — Dr. Smith and the endocrinologist don't get word of this yet. That's Interaction 4.
