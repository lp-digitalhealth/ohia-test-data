# HL7 v2 Sample Messages

This folder holds sample HL7 v2 messages representing the wire-level transactions that sit "underneath" the FHIR resources in `fhir-resources/` — specifically, the messages IHE 360X actually moves between EHR/PMS systems, which the ODE 360X bridge (see `lp-digitalhealth/ode-360x-adapter`) translates into the FHIR content already built for each use case.

This is a parent-level folder (sibling to `use-cases/`, `fhir-resources/`, and `companion-guides/`) because HL7 v2 transaction samples apply across use cases the same way `fhir-resources/durable/` does.

**All message-type and mapping decisions here are governed by `spec/mapping/360x-cow-crosswalk.md`** in the `ode-360x-adapter` repo — the project's own stated "single source of truth" for how 360X (v2) and COW (FHIR) relate. A local reference summary is kept at `_reference/360x-cow-crosswalk-summary.md`.

## Structure

```
hl7v2/
├── _reference/
│   └── 360x-cow-crosswalk-summary.md      ← local summary of the crosswalk; check the live repo for updates
└── uc01-medical-to-dental/
    └── interaction-01/
        ├── OMG_O19-dental-referral-request.hl7          ← the raw ER7 message (PCC-55)
        └── OMG_O19-dental-referral-request-QA-notes.md  ← verified vs. illustrative, revision history
```

## What's built so far

**UC01 Interaction 1** — the PCC-55 "Referral Request" transaction (FCCC → Penn Dental), as an `OMG^O19^OMG_O19` HL7 v2.5.1 message — corrected from an earlier, incorrect `REF^I12` draft after reading the crosswalk directly (see the QA notes' revision history for what changed and why). Every identifier in the HL7 message (referral ID via `ORC-2`, patient MRN/MBI, ICD-10 code, allergy code, ordering provider NPI) was cross-checked against the Interaction 1 FHIR resources and matches exactly (11/11 automated checks).

**Always read the QA notes alongside the message** — they document what's verified vs. illustrative, and flag one genuine gap surfaced during this build: the crosswalk doesn't specify a discrete v2 field for the *receiving clinician's* identity on the initial referral request (only the receiving organization and, later, the accepting provider on a PCC-56 accept).

## Not yet built

Sample messages for the remaining UC01 interactions, and the corresponding 360X response transactions (PCC-56 accept/decline, PCC-57 outcome, PCC-59 interim note, PCC-60/61 appointment/no-show).
