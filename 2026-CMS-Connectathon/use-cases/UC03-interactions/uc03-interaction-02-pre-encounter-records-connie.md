# UC03 — Interaction 2: Pre-Encounter Medical Records Delivery via Connie

**Corresponds to:** 2026-05-21 — a full week before Timothy's appointment, and roughly three months after the referral was created.

## What happens

Timothy's appointment is a week away. He'll be accompanied by his grandparents, who know he has diabetes and who his pediatrician is — and not much else. Without something changing that, Dr. Watson would start the visit blind: no idea what medications Timothy is on, no idea about the insulin pump or the CGM, no record of the gingivitis Dr. Smith found three months earlier.

New Haven Pediatric Care Center's Epic system — with Care Everywhere enabled — makes Timothy's record available. Connie, Connecticut's state health information exchange, routes it: not a document, not a PDF summary, but discrete FHIR data pulled from Epic and pushed through to Dr. Watson's practice, a full week before Timothy ever walks in. Diagnoses, active medications, the devices he's wearing, his full care team, and the oral health findings from February — all of it arrives in time to actually inform how Dr. Watson prepares.

## What Timothy's Guardians See (patient-facing)

📱 **Notification:** *(none — this is a provider-to-provider clinical data exchange; nothing here is patient-facing)*

## Key resources exchanged in this interaction

A single `Bundle`, routed New Haven Pediatric Care Center → Connie → Dr. Watson's interim FHIR server, containing:

- `Patient` (Timothy's demographics)
- `Condition` ×3 — E10.9, K05.00, Z77.22, all now transmitted as existing findings (not newly asserted — these were created back in Interaction 1, or earlier for E10.9)
- `MedicationRequest` — insulin lispro
- `Device` ×2 — the CGM and the insulin pump
- `CareTeam` — Dr. Smith, the pediatric endocrinologist, and the registered dietitian
- `Observation` — the oral health assessment findings from the well-child visit
- `Flag` — the Type 1 diabetes/elevated periodontal risk flag created in Interaction 1
- `Encounter` — a summary of the well-child visit itself

Also: a `Task` (per this use case's own resource table) specifically tracking this delivery until Connie confirms it reached the dental practice, and `Provenance`/`AuditEvent` entries logging the routing itself — Connie's role here is meant to be auditable, not just a pass-through.

## Why this matters for testing

This is the primary test objective of the entire use case, not one interaction among several — the source doc says so directly. Two genuinely first-of-kind things are being tested at once: whether a **state HIE** (Connie) can serve as a practical routing intermediary for dental-relevant medical data, rather than requiring direct endpoint-to-endpoint configuration between every pair of organizations; and whether an **Epic Care Everywhere**-enabled endpoint can be queried for discrete, actionable FHIR resources instead of the CCDs/PDFs it's historically produced. The real clinical stakes are also worth naming: this is explicitly a *pre-encounter* delivery, arriving a week ahead — not concurrent with a referral send the way UC01 and UC02's imaging did.

## What's deliberately NOT part of this interaction

The actual dental evaluation — Dr. Watson has the records now, but hasn't seen Timothy yet. That's Interaction 3.
