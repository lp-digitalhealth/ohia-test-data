# Durable resources (reusable across use cases)

Everything here is tied to a **real-world (or stably-synthetic) entity** - an institution, clinician, insurance plan, or a payer's rule set - not to any one patient's story. That is what makes it durable: the same file is loaded by every use case that involves that entity, and adding a new use case that reuses an existing organization or clinician means loading the file that is already here, not creating a new one.

A resource belongs in `durable/` if it answers "who/what is this entity in the real world?" rather than "what happened to this patient?". If it is specific to one patient's episode, it belongs in [`../purpose-built/`](../purpose-built/) instead.

## Subfolders

| Folder | Resource type(s) | Count |
|---|---|---|
| `organizations/` | Organization | 17 |
| `practitioners/` | Practitioner | 12 |
| `locations/` | Location | 8 |
| `endpoints/` | Endpoint (FHIR REST / WADO-RS addresses) | 14 |
| `healthcare-services/` | HealthcareService (Plan-Net directory entries) | 1 |
| `insurance-plans/` | InsurancePlan | 5 |
| `payer-rules/plan-definitions/` | PlanDefinition (CRD ECA rules) | 4 |
| `payer-rules/libraries/` | Library (CQL logic) | 4 |
| `payer-rules/questionnaires/` | Questionnaire (DTR templates) | 3 |
| `cds-hooks/` | CDS Hooks discovery configs (NOT FHIR resources) | 4 |

**UC03 (Connecticut pediatric referral) added a net-new block of Connecticut entities:** organizations `org-nemg`, `org-cornell-scott`, `org-connie` (statewide HIE), `org-ctdhp`, `org-benecare` (ASO), `org-gainwell` (fiscal agent/payer), `org-yale-diabetes`; practitioners `pract-smith`, `pract-watson`, `pract-endo`, `pract-dietitian`; locations `loc-nemg`, `loc-cornell-scott`; endpoints `endpoint-nemg`, `endpoint-cornell-scott`, `endpoint-connie`, `endpoint-benecare`; the new `healthcare-services/` subfolder with `hs-cornell-scott-pediatric-dental` (the Plan-Net entry BeneCare returns); and `insplan-ctdhp-huskyb`. Note the Connecticut payer split: **Gainwell** is the claims payer (fiscal agent), while **CTDHP/BeneCare** runs the directory/referral coordination — there is no dental MCO.

**UC03's D4341 prior-authorization (fires at the treatment visit, I3) added the CTDHP PA rule set:** `payer-rules/plan-definitions/plandef-ctdhp-d4341-pa-rule`, `payer-rules/libraries/lib-ctdhp-d4341-pa-logic`, `payer-rules/questionnaires/questionnaire-ctdhp-d4341-pa-dtr`, and `cds-hooks/cds-hooks-discovery-ctdhp` (the `order-sign` discovery config). Their notes capture the Connecticut routing/adjudication split — **Connie** routes, **BeneCare** takes PA intake, **Gainwell** runs DTR/PAS and adjudicates. Durable because they are the CTDHP/HUSKY B plan's rules, not Timothy's episode.

**UC04a (commercial teledentistry referral) added a net-new block:** organizations `org-meridian-teledental` (fictional teledentistry brand, POS 02), `org-barton-springs-dental` (fictional in-office practice, Austin, POS 11), `org-uc04-commercial-payer` (**Aetna Dental** — the real payer named in the source, synthetic EDI/endpoint); practitioners `pract-webb`, `pract-nair`; locations `loc-meridian-virtual` (telehealth, no physical site), `loc-barton-springs`; endpoints `endpoint-meridian-teledental`, `endpoint-barton-springs` (in-office **interim FHIR server**), `endpoint-uc04-commercial-payer`; and `insplan-uc04-commercial-ppo` (Aetna Dental PPO — teledentistry + endodontic benefit, **no PA**). No CRD payer-rule set was added: UC04a's commercial plan requires no prior authorization, so there is no PlanDefinition/Library/Questionnaire/CDS-Hooks entry for it. Meridian and Barton Springs are shared with (future) UC04b.

## What is shared across more than one use case (the reuse payoff)

These are the files that prove the durable tier is doing its job - loaded by two use cases each:

- `organizations/org-south-congress-dental.json`, `organizations/org-austin-oral-surgery.json`
- `practitioners/pract-parker.json`, `practitioners/pract-maxil.json`
- `locations/loc-south-congress-dental.json`, `locations/loc-austin-oral-surgery.json`
- `endpoints/endpoint-south-congress-dental.json`, `endpoints/endpoint-austin-oral-surgery.json`

Everything else here is currently loaded by a single use case, but lives in `durable/` because it is entity-scoped and would be reused as-is by any future use case involving that same institution, clinician, or plan.

The full file-by-file manifest (which real-world entity each file represents, and which use cases consume it) is in the library master index: [`../README.md`](../README.md).

## CDS Hooks placement note
All four payers' `order-sign` discovery configs now live together in `cds-hooks/` (IBX, DentaQuest, commercial, and CTDHP). Previously two sat loose at the registry root and IBX's was mis-filed inside a UC01 interaction folder; they were consolidated here during the library reorg. Each interaction bundle that exercises a payer's hook still embeds its own inline copy, so moving the standalone files did not affect any bundle.
