# UC04b-I1: Midnight Pain, A Diabetes Flag

**Corresponds to:** 2026-07-21, 23:47 through 2026-07-22, 00:38.

## What happens

It's nearly midnight. Darius hasn't seen a dentist in three years — he doesn't know his benefit, doesn't have a regular provider, doesn't know who nearby takes Medicaid. The pain has gotten bad enough that he can't sleep, so he opens the app tied to his Texas Medicaid dental benefit. Coverage confirms active. Before anything else happens, the teledentistry platform itself queries the dental benefit manager's provider directory — a structured search, not a phone call or a static PDF — to find an in-office practice in San Antonio that's actually in-network and taking new patients. It finds one, before Dr. Angela Torres even starts the visit.

Dr. Torres assesses him virtually: throbbing pain, upper right, sensitive to sweets, keeping him up at night. He mentions he's on metformin for Type 2 diabetes. That matters clinically, not just as background — diabetes elevates infection and healing risk, and whoever treats Darius in person needs to know that going in. Dr. Torres documents a `Flag` specifically to carry that signal forward. Her assessment points to irreversible pulpitis in tooth #3, likely with secondary caries underneath. She sends the referral — findings, medication, and the diabetes flag together — to the practice the directory query already confirmed.

## What Darius Sees (patient-facing)

📱 **Notification:** *"Referral sent."*

## Key resources exchanged in this interaction

- `Coverage` (queried) and `InsurancePlan` (Texas Medicaid dental benefit via the DBM)
- `PractitionerRole` and `HealthcareService` (queried from the DBM's Plan-Net directory — read-only, confirming network participation and open-panel status *before* the referral is created, not after)
- `Encounter` (virtual, POS 02)
- `Condition` — K04.01 (irreversible pulpitis)
- `Observation` — symptom findings
- `MedicationStatement` — metformin
- `Flag` — Type 2 diabetes, elevated infection/healing risk, newly created and travels with the referral
- `ServiceRequest` (urgent) + `DocumentReference` — transmitted via CDex push

Same as UC04a: **no imaging exists yet to exchange.** The radiograph doesn't happen until Interaction 3.

## Why this matters for testing

This combines three things UC04a didn't have to: a Medicaid-context Plan-Net query completed *before* referral creation (not after, the way it sometimes works elsewhere), a `Flag` carrying a real clinically-actionable comorbidity signal (not just background history), and all of it happening close to midnight — testing whether urgent-access timelines hold up outside business hours, not just during them.

## What's deliberately NOT part of this interaction

The in-office practice hasn't seen this yet — that's Interaction 2.
