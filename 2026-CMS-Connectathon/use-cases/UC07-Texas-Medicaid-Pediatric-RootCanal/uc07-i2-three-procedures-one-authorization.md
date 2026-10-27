# UC07-I2: Three Procedures, One Authorization

**Corresponds to:** 2026-07-09, 08:00 (CRD) through 2026-07-15, 15:00 (approval received and appointment set).

## What happens

The next business morning, Dr. Garcia's staff enter the treatment plan: root canal therapy (D3320), a build-up (D2950), and a crown (D2740), all on tooth #4. The moment the order is entered, his EHR asks DentaQuest what it needs, and DentaQuest answers within minutes: **prior authorization is required**.

The EHR then retrieves DentaQuest's documentation requirements and pre-fills what it can from the chart: the diagnosis, the tooth, the radiographic findings. DentaQuest's answer is that **clinical notes documenting medical necessity and images are required**.

On July 10, Dr. Garcia's office submits the request electronically. Rather than stuffing notes and radiographs into the authorization transaction as inline base64, the practice publishes them as an **ARex manifest**: a signed list of individually retrievable objects with a digest for each. The authorization `Claim` points to that manifest. At 09:05, DentaQuest retrieves the objects and verifies each digest.

DentaQuest reviews and approves on **July 15**. That is three business days after submission, in line with DentaQuest's published standard turnaround for Texas. The response carries an authorization number and a validity window of 180 days. Dr. Garcia's office then books Joe for the following week.

## Why this matters for testing

This is the highest-novelty interaction in UC07. It exercises Da Vinci CRD, DTR, and PAS against a dental benefit and CDT codes, and then adds two things UC02a did not have:

- **A bundled, multi-procedure request.** Root canal, build-up, and crown are submitted and decided as one coordinated authorization with three service lines, not three independent requests. The test is whether the plan's rules engine and the PAS `Claim` / `ClaimResponse` handle that bundle with consistent per-line outcomes.
- **Out-of-band attachments via ARex.** Supporting evidence is delivered by reference, with signed-manifest and per-object digest verification. ARex is a draft, provisional IG, so this is a pilot of the pattern. Failure modes worth exercising include a digest mismatch, an expired grant, and a manifest the payer cannot retrieve.

The authorization number returned here has to survive intact to the restorative practice's claim in Interaction 5.

## What's deliberately NOT part of this interaction

The consultation and consent. Joe hasn't been seen by Dr. Garcia yet. That happens in Interaction 3.
