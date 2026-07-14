# Durable resources (reusable across use cases)

Everything here is tied to a **real-world (or stably-synthetic) entity** - an institution, clinician, insurance plan, or a payer's rule set - not to any one patient's story. That is what makes it durable: the same file is loaded by every use case that involves that entity, and adding a new use case that reuses an existing organization or clinician means loading the file that is already here, not creating a new one.

A resource belongs in `durable/` if it answers "who/what is this entity in the real world?" rather than "what happened to this patient?". If it is specific to one patient's episode, it belongs in [`../purpose-built/`](../purpose-built/) instead.

## Subfolders

| Folder | Resource type(s) | Count |
|---|---|---|
| `organizations/` | Organization | 7 |
| `practitioners/` | Practitioner | 6 |
| `locations/` | Location | 4 |
| `endpoints/` | Endpoint (FHIR REST / WADO-RS addresses) | 7 |
| `insurance-plans/` | InsurancePlan | 3 |
| `payer-rules/plan-definitions/` | PlanDefinition (CRD ECA rules) | 3 |
| `payer-rules/libraries/` | Library (CQL logic) | 3 |
| `payer-rules/questionnaires/` | Questionnaire (DTR templates) | 2 |
| `cds-hooks/` | CDS Hooks discovery configs (NOT FHIR resources) | 3 |

## What is shared across more than one use case (the reuse payoff)

These are the files that prove the durable tier is doing its job - loaded by two use cases each:

- `organizations/org-south-congress-dental.json`, `organizations/org-austin-oral-surgery.json`
- `practitioners/pract-parker.json`, `practitioners/pract-maxil.json`
- `locations/loc-south-congress-dental.json`, `locations/loc-austin-oral-surgery.json`
- `endpoints/endpoint-south-congress-dental.json`, `endpoints/endpoint-austin-oral-surgery.json`

Everything else here is currently loaded by a single use case, but lives in `durable/` because it is entity-scoped and would be reused as-is by any future use case involving that same institution, clinician, or plan.

The full file-by-file manifest (which real-world entity each file represents, and which use cases consume it) is in the library master index: [`../README.md`](../README.md).

## CDS Hooks placement note
All three payers' `order-sign` discovery configs now live together in `cds-hooks/`. Previously two sat loose at the registry root and IBX's was mis-filed inside a UC01 interaction folder; they were consolidated here during the library reorg. Each interaction bundle that exercises a payer's hook still embeds its own inline copy, so moving the standalone files did not affect any bundle.
