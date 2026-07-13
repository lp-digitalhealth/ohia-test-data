# UC01-I2: Dental Exam & Open Questions

**Corresponds to:** clinical Encounter #2 (dental exam & radiographs, 2026-07-23) — plus the acceptance step that precedes it, and one later moment that shares the same underlying mechanism.

## What happens

### Step 1: Penn Dental accepts the referral (2026-07-07)

Before anything clinical happens, Penn Dental's front office reviews the referral that arrived from FCCC and confirms they'll take it. This is the moment the relationship actually becomes real — not just "a referral was sent," but "a specific practice, and specifically Dr. Bellweather, has agreed to see John." An appointment gets scheduled for 2026-07-23.

## What John Sees (patient-facing) — Step 1

📱 **Notification:** *"Appointment scheduled with Dr. Bellweather at Penn Dental — July 23."*

This step matters more than it might seem: it's the first moment anyone other than Dr. Whitfield's office has formal ownership of getting John cleared for radiation. Everything downstream depends on this handoff actually happening and being visible to the systems tracking it — and to John.

### Step 2: The dental exam (2026-07-23)

Dr. Bellweather examines John and takes radiographs. He finds three teeth needing attention: #4 (needs extraction), #17 (impacted, needs extraction), and #30 (structurally fine, but sitting inside the planned radiation field).

## What John Sees (patient-facing) — Step 2

📱 **Notification:** *"Dr. Bellweather is reviewing your case."*

### Step 3: The DDC dose inquiry (same day, 2026-07-23)

For tooth #30, Dr. Bellweather can't decide whether to extract it or leave it in place without knowing exactly how much radiation dose it's going to receive. That number lives in FCCC's radiation planning system, not in anything Penn Dental has access to. So he asks Dr. Priya Nandakumar, FCCC's medical physicist, directly: *what's the dose at tooth #30?*

Two days later, the answer comes back: 52 Gy — well above the 45 Gy threshold considered safe for extraction healing. That tells Dr. Bellweather the tooth needs to come out, with an implant placed immediately, rather than waiting.

## What John Sees (patient-facing) — Step 3

**Nothing.** This is deliberate, not an oversight: Dr. Bellweather asking Dr. Nandakumar a clinical question, and Dr. Nandakumar's answer, are provider-to-provider communication that never surfaces to John directly — he isn't notified that a question was asked or answered, only the *consequence* of it (the extraction/implant decision) once it's actually acted on. A patient app that fires a notification for this step is doing the wrong thing; testing that it correctly stays silent here is as important as testing that it correctly fires for the real milestones.

### Step 4: The treatment extension request (early August)

After all three extractions and the implant placement are done, Dr. Bellweather documents John's clearance and sends it to FCCC. Prior authorization for the radiation is approved by IBX shortly after. But the radiation can't start on its originally planned date — the extraction and implant sites need real time to heal first.

So Dr. Bellweather (or the coordinating team) tells Dr. Whitfield, informally: *hold off — this needs more healing time than the original schedule allows.* The radiation start date moves out by two weeks.

## What John Sees (patient-facing) — Step 4

**Nothing directly from this exchange** — same reasoning as Step 3, this is provider-to-provider. What John *does* eventually see is the practical downstream effect: his radiation start date on the app updates to the revised date. That update is driven by the `ServiceRequest` occurrence date changing, not by this note itself — the note is the reason behind the change, not something the app surfaces on its own.

## Why steps 3 and 4 are modeled the same way

Neither the dose question nor the extension request is a formal order, a referral, or even a structured message type in the underlying standards. Both are exactly what the base FHIR Clinical Order Workflows (COW) standard calls **"Requesting additional information"** — a named, expected pattern where a clinician needs data they don't have, and COW explicitly allows it to travel as something as simple as a note rather than a formal resource. So both are captured as informal notes, while the actual resulting data (the dose value; the revised start date) is captured formally, since that data matters for downstream decisions.

## Why this matters for testing

This interaction tests three distinct things in sequence: **(1)** whether a system correctly reflects a referral moving from sent → accepted → actively being worked, not just "sent" and then silence; **(2)** whether informal, ad hoc provider-to-provider communication — common in real practice, but outside most standards' formal scope — can be represented without a dedicated resource type; and **(3)** whether a firm's patient-facing app distinguishes "the referral relationship is progressing" (patient-visible) from "the specific clinical back-and-forth producing that progress" (not patient-visible), since both are true at once but only one should ever reach John.

---

**A structural note on how this maps to the base resources:** Steps 1 and 2 are Task status/businessStatus transitions on the *existing* referral Task from Interaction 1 (not new resources) — `Task.owner` gets set here for the first time, at acceptance, per the crosswalk's rule that ownership belongs to PCC-56, not intake. Steps 3 and 4 are notes plus the formally-captured resulting data (the dose `Observation`; eventually, an updated occurrence date on the IMRT order). **Known gap:** the Task update reflecting Steps 1–2's status transitions has not yet been built as its own file — see `CLAUDE.md` and the companion guide's Resource Index for this interaction.
