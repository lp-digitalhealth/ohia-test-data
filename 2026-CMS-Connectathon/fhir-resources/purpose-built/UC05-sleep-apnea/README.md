# UC05 Purpose-Built FHIR Resources

This package contains the patient-episode and interaction-specific FHIR R4 resources for **UC05 — Medical to Dental: Oral Appliance Therapy for Obstructive Sleep Apnea**.

## Interaction model

- **Interaction 1:** sleep medicine sends the complete medical-to-dental referral package. The preceding PCP referral and internal sleep testing are context, not separate tested interactions.
- **Interaction 2:** the dental practice sends the readiness assessment and E0486 prior-authorization package to the test payer; the payer approves it.
- **Interaction 3:** after fabrication and delivery, the dental practice creates the non-financial `ODEDentalClaim` claims-sharing package for E0486. Optional downstream Claim/ClaimResponse/EOB fixtures demonstrate medical-payer submission and adjudication, but the tested repository artifact remains the interoperable claims-ready package.
- **Interaction 4:** the dental practice returns treatment and titration status to sleep medicine; follow-up HSAT establishes effectiveness and the referral loop closes.

## Tiers

- `durable-addendum/` contains four PCP registry dependencies that were absent from the first durable package but are required to represent the payer's PCP-referral-chain rule without unresolved references.
- `base/` contains Maya, her coverage, consent, chronic conditions, care team, practitioner roles, patient subscription, and the antecedent PCP-to-sleep referral.
- `interactions/interaction-0N/` contains only resources created or materially updated for that tested exchange, plus a cumulative self-contained transaction Bundle.

## Important modeling rules

- Synthetic people and organization names are used. Real Jacksonville addresses may be geographic anchors.
- No real NPI is attached to any synthetic practitioner or organization.
- The sleep physician diagnoses OSA and orders oral appliance therapy. The dentist assesses dental candidacy and delivers/titrates the appliance; the dentist does not diagnose OSA.
- E0486 is the medical/DME claim line. D9947 and D9948 are retained as dental clinical documentation and are not duplicate paid medical lines.
- `ImagingStudy` and `DocumentReference` carry imaging metadata and synthetic retrieval URLs; pixel/scan payloads are not embedded.
- Local UC05 codes are used where a verified standard code was not established, rather than guessing.
- Florida Blue coverage rules, network status, authorization, prices, and adjudication are Connectathon assumptions.

## Counts

- Individual FHIR resource files: 84
- Transaction Bundles: 4
- Total JSON files in manifest: 88
