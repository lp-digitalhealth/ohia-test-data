# OHIA Connectathon Test Materials

**See `CLAUDE.md` at this folder's root for the authoritative, up-to-date project state, decisions, and session history.** This README gives a quick structural orientation only.

```
/
├── CLAUDE.md              Authoritative project state — read this first.
├── use-cases/             Narrative documents. Written to be understandable by
│                          clinicians and non-technical stakeholders. The clinical
│                          story is documented as numbered ENCOUNTERS (real visits),
│                          but test data is organized by INTERACTION — see CLAUDE.md
│                          for why these are two different axes.
├── fhir-resources/        The actual loadable FHIR content, organized by interaction.
├── hl7v2/                 Sample HL7 v2 messages, same interaction organization.
└── companion-guides/      Prep guidance + readiness checklists per use case.
```

**Cross-repo feedback** (proposed changes to repos this project doesn't own, e.g. `ode-360x-adapter`, `ohia-fhirr4-scratchpad`) is delivered separately, outside this repo — see `CLAUDE.md` Section 5a for pointers.
