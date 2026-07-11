# OHIA Connectathon Test Materials

This repository is organized into three top-level folders, each with a distinct audience and purpose:

```
/
├── use-cases/            ← Narrative documents. Written to be understandable by
│                            clinicians and non-technical stakeholders — describes
│                            WHAT happens in the clinical/business story, encounter
│                            by encounter, without FHIR implementation detail.
│
├── fhir-resources/       ← The actual loadable FHIR content. Every resource a firm
│                            needs to load onto their test server lives here, in full
│                            technical detail (identifiers, codings, references).
│
├── hl7v2/                ← Sample HL7 v2 messages representing the wire-level
│                            transactions (e.g. IHE 360X) that sit "underneath" the
│                            FHIR resources — what a 360X bridge/adapter ingests to
│                            produce the FHIR content in fhir-resources/.
│
└── companion-guides/     ← The bridge between the two above. Tells an implementer,
                             role by role (EHR / PMS / Payer / Patient App), which
                             fhir-resources/ content to load and what their system
                             needs to be capable of to execute a given use case's
                             encounters — without being overly prescriptive about
                             internal implementation.
```

## How the three folders relate

1. **Read the use case** (`use-cases/UC0X.../`) to understand the clinical story and what each encounter represents.
2. **Read the companion guide** (`companion-guides/UC0X-companion-guide.md`) for your role (EHR, PMS, Payer, or Patient App) to understand what your system needs to load and support for the encounter(s) you're testing.
3. **Load the resources** referenced by the companion guide from `fhir-resources/UC0X.../` — registry resources from `common/` first, then the use case's `base/` resources, then the specific `encounters/encounter-0N/` resources for whichever encounter(s) you're testing.

A firm can choose to test a single encounter or the full use case end-to-end; the companion guide and resource folders are structured so either is possible without loading more than what's needed.

## Current status

- **UC01 (Medical-to-Dental, Head & Neck Cancer)** is the model use case. Its base resources (registry + patient/coverage/consent) are complete and verified. Its 7-encounter breakdown is finalized (see `use-cases/UC01-medical-to-dental-tongue-cancer/`). Encounter #1's FHIR resources, HL7 v2 sample message, and clinician-readable writeup are complete and cross-verified against each other. Encounters #2–7, the companion guide, and encounter-level test scripts are still in progress.
- **UC02–UC05** have not yet been built to this structure.
