# UC07-I4: Closing the Loop

**Corresponds to:** 2026-07-22, 13:30 (post-treatment push) through 13:35 (referral closed).

## What happens

That afternoon, Dr. Garcia's system pushes a structured package back to Dr. Parker's practice, the same kind of CDex push that brought the referral to him, now running in reverse. The package contains four things:

1. A **treatment summary** with the status of the tooth and healing.
2. The **post-operative radiograph**, again as a pointer to a DICOM object that Dr. Parker's system can retrieve.
3. A **clinical note** describing what was done.
4. A **separate note thanking Dr. Parker for the referral.**

Five minutes after the package arrives, Dr. Parker's system marks the referral complete.

## Why this matters for testing

This is the closed-loop pattern already proven in UC01 and UC02, applied to a bundled endodontic and restorative course of treatment. The distinctive test here is the **thank-you note**. It is a courtesy communication, not clinical content, and it travels in the same push as the clinical material. The receiving system must tell the two apart: the clinical note files into the chart, and the thank-you note must not be mistaken for clinical documentation.

The test also confirms that the post-op radiograph comes back as an imaging reference. Dr. Parker retrieves it through the same pull pattern used in Interaction 1.

## What's deliberately NOT part of this interaction

Billing. Both practices submit claims the next morning, in Interaction 5.
