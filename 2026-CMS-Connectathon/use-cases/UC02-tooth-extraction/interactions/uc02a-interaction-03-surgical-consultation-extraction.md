# UC02a — Interaction 3: Surgical Consultation & Extraction

**Corresponds to:** 2026-07-21, 09:00.

## What happens

Frank arrives at Austin Oral Surgery. Dr. Maxil already has everything Dr. Parker sent — he doesn't start from a blank chart. He reviews the radiographs and diagnosis, confirms it independently, reviews Frank's medications for surgical risk, and has his staff double-check that Frank's Medicaid coverage is still active and that nothing has changed since the PA was approved a week earlier.

## What Frank Sees (patient-facing)

📱 **Notification:** *(none new — Frank was already told his appointment is confirmed; nothing further fires until the visit concludes)*

Dr. Maxil performs the surgical extraction of tooth #30 — elevating and sectioning the tooth, curetting and irrigating the socket, achieving closure. He documents the anesthesia used, the procedure itself, and gives Frank discharge instructions with a follow-up scheduled for one week out.

## Why this matters for testing

This is the core clinical event UC02a exists to test: whether a receiving specialist can act on a referral's clinical package without repeating diagnostic work, and whether the procedure itself — CDT-coded, tooth-specific, tied back to the original PA number — is captured in a form that closes the loop cleanly in the next interaction. It's also a re-verification test: does the system correctly re-check coverage at time of service, not just assume the PA from a week ago still holds?

## What's deliberately NOT part of this interaction

Sending word back to Dr. Parker that this happened — that's Interaction 4.
