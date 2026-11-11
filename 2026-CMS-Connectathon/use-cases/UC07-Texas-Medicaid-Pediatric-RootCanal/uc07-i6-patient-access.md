# UC07-I6: Patient Access

**Corresponds to:** 2026-07-28, evening. DentaQuest posted both adjudicated claims that morning (06:00).

## What happens

Linda Castle, Joe's mother and guardian, opens a patient app on her phone to see what DentaQuest paid for Joe's care. The app finds Joe at DentaQuest by the **online member ID** DentaQuest issued for him, then reads his record through DentaQuest's **Patient Access API**. It shows three things:

1. **Joe's coverage**: Texas Medicaid dental through DentaQuest, active through 2026-12-31.
2. **Dr. Parker's claim** for the evaluation and radiographs on 2026-07-08 (D0140, D0220 on tooth #4, D0270): billed, the amount DentaQuest allowed, and what Joe owes.
3. **Dr. Garcia's claim** for the root canal, build-up and crown on tooth #4 on 2026-07-22 (D3320, D2950, D2740), with the **prior authorization number from Interaction 2** on it.

Both claims are Medicaid, so Joe owes nothing. Each is an `ExplanationOfBenefit` on the CARIN Blue Button **Oral** profile, version 2.2.0, the financial profile: the amounts submitted, the benefit amount, the discount and the amount paid to the provider are all there.

## Why this matters for testing

- **Patient apps test against payer-side data.** This is the first UC07 interaction where the consumer of the data is the patient's app, not a practice. The payer's record of Joe is held in its own resources (ids end in `-payer`), not the practices' copies.
- **The app starts from the payer's ID, not the practice's.** The online member ID exists only at the payer. An app that searches by a practice's medical record number will not find Joe.
- **The two sides must be matchable.** A patient app, or a test client, has to connect what the payer shows to what the practices recorded: the same member, the same practices and clinicians, the same services, and the same prior authorization. They are matched on business identifiers (Medicaid beneficiary ID, payer ID, NPIs, CDT code and date and tooth, the authorization number), never on FHIR ids. `crosswalk.json` lists every match and the key it uses.
- **Money.** This is where a patient first sees submitted amount against benefit amount against member liability. The amounts are **synthetic**: invented for this test, flagged in each EOB, and not DentaQuest rates.
- **The PA number carries through.** The number DentaQuest issued at approval in Interaction 2 appears on the restorative claim's EOB.
- **A minor and his guardian.** Joe is 16 and Linda is acting for him. How the payer's online account represents that, and how an app is authorized to act for him, is **not modeled here** (see the guide's open items).

## What's deliberately NOT part of this interaction

- **Authorization.** There is no SMART standalone launch yet. The first version of the test server uses the shared token it uses everywhere else. Patient scoping is described, not enforced.
- **The Provider Access API**, and payer-to-payer exchange.
- **The prior-authorization view** (the PDex `use: preauthorization` EOB). It stays optional, as section 8.5 of the companion guide describes.
- **Pending, partially paid and denied claims.** Both claims are adjudicated and paid.
- **The claims-sharing EOBs.** The non-financial claims-sharing packages the providers send are a different resource with a different purpose; nothing in this interaction replaces them.
- **X12.** The 837D and 835 for these claims belong to Interaction 5.
