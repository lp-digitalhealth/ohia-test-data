# UC05 — Medical → Dental: Oral Appliance Therapy for Obstructive Sleep Apnea

Maya Torres is a 44-year-old woman in Jacksonville, Florida, enrolled in a 2026 Florida Blue myBlue HMO ACA individual plan through the Marketplace. Her selected PCP is in the Florida Blue HMO network. She has hypertension, obesity, morning headaches, and daytime sleepiness. Her PCP documents a STOP-Bang score of 5 and sends a referral to sleep medicine.

Maya is evaluated by Dr. Priya Nanduri, MD, a fictitious Jacksonville sleep medicine physician practicing at a real Jacksonville location at 4500 San Pablo Rd S. The clinician name and identifiers used in this test scenario are synthetic.

Dr. Nanduri orders an unattended home sleep apnea test. The sleep study is represented as a FHIR `ServiceRequest` and `DiagnosticReport`; AASM lists 95800 and 95806 among unattended sleep-study CPT codes, depending on the channels recorded. The test returns:

| Finding                  | Value                   |
| ------------------------ | ----------------------- |
| Diagnosis                | Obstructive sleep apnea |
| ICD-10-CM                | G47.33                  |
| REI/AHI                  | 22.6 events/hour        |
| Severity                 | Moderate OSA            |
| Oxygen nadir             | 83%                     |
| Epworth Sleepiness Scale | 15                      |
| Comorbidity              | Hypertension            |

The REI value is sent as a structured `Observation`; LOINC 97519-3 is “Respiratory event index [AASM],” and LOINC describes REI as apneas plus hypopneas per hour of monitoring time, with 15–30/hour typically categorized as moderate. The Epworth score is also structured; CDC’s archived Epworth Sleepiness Scale page describes the 0–3 scoring across eight situations and notes that a total score of 10 or greater raises concern.

Dr. Nanduri first recommends PAP therapy. Maya attempts APAP for three weeks but cannot tolerate it because of mask claustrophobia, air leak, and facial irritation. The PAP adherence download shows use on 9 of 21 nights, with only 3 nights over four hours. Dr. Nanduri documents PAP intolerance and discusses alternatives. Maya prefers oral appliance therapy.

At order-sign, the sleep EHR calls the Florida Blue test CRD service. The Connectathon test payer response says:

| Coverage rule          | Connectathon assumption                                                                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Benefit                | Medical DME, not dental benefit                                                                                                                                          |
| Device code            | E0486                                                                                                                                                                    |
| PA required            | Yes                                                                                                                                                                      |
| Required documentation | Sleep-study report, AHI/RDI, diagnosis G47.33, physician order, PAP intolerance/preference documentation, dental candidacy assessment, provider identity, treatment plan |
| Network rule           | PCP referral and in-network dental sleep provider required                                                                                                               |
| Patient visibility     | PA status and eventual EOB visible through payer Patient Access API                                                                                                      |

The QHP Patient Access API piece is realistic for an ACA FFE issuer: CMS states that impacted payers, including QHP issuers on Federally Facilitated Exchanges, must make claims, encounter, and maintained clinical data available through a FHIR-based Patient Access API.

Dr. Nanduri sends a medical-to-dental referral to First Coast Dental Sleep Center, a fictitious dental organization operating at a real Jacksonville dental location. The organization name and identifiers used in this test scenario are synthetic. The referral packet includes:

| Data sent                          | FHIR representation                              |
| ---------------------------------- | ------------------------------------------------ |
| OSA diagnosis                      | `Condition`                                      |
| HSAT report                        | `DiagnosticReport`, `DocumentReference`          |
| AHI, oxygen nadir, Epworth         | `Observation`                                    |
| PAP intolerance/adherence          | `Observation`, `DocumentReference`               |
| Oral appliance order               | `ServiceRequest`                                 |
| Florida Blue coverage              | `Coverage`, `InsurancePlan`                      |
| PCP/sleep physician referral chain | `PractitionerRole`, `Organization`, `Provenance` |

The dentist does not diagnose OSA. The dentist determines whether Maya is a safe oral-appliance candidate. At the dental visit, the practice reviews dentition, periodontal status, TMJ history, mandibular range of motion, missing teeth, and ability to retain a mandibular advancement device. The dentist takes a panoramic radiograph and digital intraoral scans. The dental system returns a structured OAT Readiness Assessment to Dr. Nanduri and the payer.

The dental assessment says:

> Patient is dentally appropriate for a custom titratable mandibular advancement device. No active periodontal infection. No unstable dentition. No TMJ contraindication. Adequate protrusive range for titration. Proceed with custom appliance pending medical/DME authorization.

That assessment becomes the missing dental-side documentation for PA. The dental practice, acting as the rendering/billing provider, submits the PAS prior authorization for E0486 with supporting data from the sleep physician and dentist. This aligns with the Medicare LCD logic often used as a documentation baseline: the device must be ordered by the treating practitioner after review of the sleep test and provided/billed by a licensed dentist.

Florida Blue’s test payer returns a `ClaimResponse` approving the PA. The patient app updates: “Oral appliance approved — ready for fabrication.”

Only after approval, the dentist sends the digital scan to a fabricated lab, SunCoast Oral Appliance Lab, and fabricates a custom titratable mandibular advancement device. Delivery is documented as:

| Code  | Use                                                                             |
| ----- | ------------------------------------------------------------------------------- |
| D9947 | Dental documentation for custom sleep apnea appliance fabrication and placement |
| D9948 | Dental documentation for appliance adjustment/titration, if separately tracked  |

However, the device is coded as:

| Code  | Use                                                    |
| ----- | ------------------------------------------------------ |
| E0486 | Medical/DME claim for custom-fabricated oral appliance |

Over six weeks, the dentist titrates the device and sends structured updates to the sleep physician. Once Maya reports improved sleep and reduced daytime sleepiness, Dr. Nanduri orders a follow-up HSAT. The follow-up report shows AHI improved from 22.6 to 7.8 events/hour and oxygen nadir improved from 83% to 90%. The sleep physician closes the loop and continues annual follow-up.
