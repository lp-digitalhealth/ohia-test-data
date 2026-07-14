# Purpose-built resources (one episode only)

Everything here is specific to a single patient's episode and is **not** reusable across use cases. Each use case is its own folder, and within a use case there are two sub-tiers with different reuse scopes:

| Sub-tier | Folder | Reuse scope | Contents |
|---|---|---|---|
| **Base** | `<uc>/base/` | Reusable *within* this one use case (loaded by every interaction) | `Patient`, `Coverage`, `Consent`, the episode's `PractitionerRole` pairings, patient-app `Subscription` |
| **Per-interaction** | `<uc>/interactions/interaction-0N/` | One integration point only | `Encounter`, `Condition`, `Observation`, `ServiceRequest`, `Task`, `Procedure`, `Device`, bundles, etc. |

Why base is separate from durable: a `Patient` or their `Coverage` is stable across every step of one episode, but it does not carry over to another use case - e.g. Frank Castle is modeled twice, `uc02a/base/patient-frank-castle.json` and `uc02b/base/patient-frank-castle.json`, because his coverage differs between the Medicaid and commercial scenarios. `PractitionerRole` lives in base (not durable) for the same reason: the role *pairing* of clinician + org + specialty + location can vary by use case even when the underlying `Practitioner` (in `durable/`) does not.

## Use cases

| Use case | Folder | Story | Built |
|---|---|---|---|
| **UC01** | `uc01-medical-to-dental/` | Medical-to-dental referral, head & neck cancer (John Smith), with prior auth | I1-I4 |
| **UC02a** | `uc02a-surgical-extraction/` | Texas Medicaid surgical extraction (Frank Castle), **with** prior auth | I1-I5 |
| **UC02b** | `uc02b-commercial-implant/` | Commercial surgical extraction + immediate implant (Frank Castle), **no** prior auth | I1-I5 |
| **UC03** | `uc03-pediatric-referral/` | Pediatric dental referral, Type 1 diabetes (Timothy Jones), CT HUSKY B routed via **Connie HIE**; covered referral (**no PA at referral**) but **D4341 PA fires at the treatment visit (I3)**, no imaging/HL7v2, minor/guardian proxy | I1-I5 |

Each use case's `interactions/README.md` lists its per-interaction resources in detail. Durable dependencies (organizations, clinicians, plans, payer rules) live in [`../durable/`](../durable/); see [`../README.md`](../README.md) for the full library map and load order.

## Loading a single interaction
Each `interaction-0N-bundle.json` is self-contained - it inlines the durable + base + prior-interaction resources it needs (via `urn:uuid` fullUrls and logical `Type/id` references), so one bundle load reproduces the complete state at that interaction without separately loading `durable/` or `base/` first.
