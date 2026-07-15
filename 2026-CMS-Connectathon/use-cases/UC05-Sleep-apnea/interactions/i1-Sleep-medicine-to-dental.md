
# UC05 Key Interactions

### I1 — PCP-to-Sleep Medicine Referral

**Organizations:**
Primary care practice → Sleep medicine practice

**Exchange:**
The PCP sends Maya’s referral and supporting clinical information for evaluation of suspected obstructive sleep apnea.

**Key data:**

* patient demographics;
* coverage information;
* hypertension and obesity;
* morning headaches and daytime sleepiness;
* STOP-Bang score of 5;
* referral order; and
* referring PCP identity.

**Primary FHIR resources:**

* `Patient`
* `Coverage`
* `Condition`
* `Observation`
* `ServiceRequest`
* `PractitionerRole`
* `Organization`
* `Provenance`### I2 — Sleep Medicine-to-Dental Referral

**Organizations:**
Sleep medicine practice → Dental sleep medicine practice

**Exchange:**
After diagnosing moderate OSA and documenting PAP intolerance, the sleep physician sends the medical referral and oral-appliance order to the dental practice.

**Key data:**

* OSA diagnosis, G47.33;
* HSAT report;
* REI/AHI of 22.6 events/hour;
* oxygen nadir of 83%;
* Epworth score of 15;
* PAP adherence and intolerance documentation;
* patient preference for oral appliance therapy;
* physician order for a custom oral appliance;
* coverage information; and
* referring and ordering provider identities.

**Primary FHIR resources:**

* `Condition`
* `DiagnosticReport`
* `Observation`
* `DocumentReference`
* `ServiceRequest`
* `Coverage`
* `PractitionerRole`
* `Organization`
* `Provenance`

---

