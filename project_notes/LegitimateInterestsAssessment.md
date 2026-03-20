# 📄 Legitimate Interests Assessment (LIA)

## Project Title:
**Court Summons Transparency and Alert System**

## Purpose of Processing:
To collect and pseudonymise publicly listed court case data, allowing individuals to:
- Check whether they have been named in a court summons (especially if they have not been properly served)
- Explore patterns in access to justice, such as attendance outcomes or anomalies in serving behavior

This is intended to support fairness, accountability, and transparency in civil litigation.

---

## 1. Purpose Test

**What are you trying to achieve?**  
I aim to create a searchable database of **pseudonymised** court listings that allows:
- Individuals to check if they have been named in a case
- Researchers to explore patterns in service and case outcomes

This is intended as a public-interest tool to protect people from being unknowingly defaulted in court cases they were not properly served notice for.

---

## 2. Necessity Test

**Is processing necessary?**  
Yes. This project relies on:
- Publicly available court listing data (e.g., names, dates, case numbers)
- Minimal identifying information to allow **data subjects (defendants)** to query the system

Without collecting names (and hashing them), the core functionality (letting people check for themselves) would not be possible.

---

## 3. Balancing Test

**Does this processing impact individuals' rights?**  
Minimal. Data is handled as follows:
- Personal names are **hashed with a secret salt**, not stored or displayed publicly 
- Original names are **encrypted** and stored separately under strict access controls
- Data is **never used to profile**, commercialize, or rank individuals
- Users may only search their own name, and results are masked unless identity is verified

**Risk Mitigations:**
- All personal data is **pseudonymised or encrypted**
- **No raw names or personal info are exposed publicly**
- An access control model ensures only authorized users (i.e. the individual being searched) can view matches
- The system logs access and enforces basic rate limits

---

**Conclusion:**  
The processing of personal data under this project is **lawful, fair, and necessary** under the **Legitimate Interests** basis of Article 6(1)(f) of the UK GDPR.

---

# 📄 GDPR Data Handling Statement

## Data Types Collected:
- Names (individual and company, from public court listings)
- Case metadata: case number, court, date, role (defendant/claimant)

## Personal Data?
Yes — **names of individuals** are considered personal data.

## Sensitive Data?
No sensitive data (e.g. health, race, religion) is collected.

---

## How Is Personal Data Protected?

| Protection Method     | Description                                                  |
|------------------------|--------------------------------------------------------------|
| Pseudonymisation       | All names are hashed and never exposed raw        |
| Encryption             | Original names stored encrypted  |
| Storage separation     | Personal and case data stored in separate database tables    |
| Access control         | Only hashed lookups will be allowed; full results to require ID verification |
| Logging                | All data access and searches will be logged and rate-limited     |

---

## Lawful Basis for Processing:
**Legitimate Interests** (UK GDPR Article 6(1)(f))  
Purpose: empowering individuals to check their own legal exposure, improving access to justice.

---

## Retention Policy:
- Encrypted name data is retained only as long as the associated case data remains useful
- Anonymous statistical data may be retained indefinitely

---

## Your Rights (as a data subject):
If you believe you have been listed in this system, you may:
- Request a copy of any data about you (Subject Access Request)
- Request correction or deletion
- Lodge a complaint with the Information Commissioner’s Office (ICO)


---

## Hosting & Security:
- Data is stored securely on PostgresQL
- Encryption keys are to be stored in environment variables, not in code

---

## Public Commitment:
This is a transparency tool, not a surveillance tool. The creator of this project is committed to:
- Respecting data subjects’ rights
- Protecting privacy
- Responding swiftly to concerns or takedown requests

---

## ✍️ Final Note:
This project operates in good faith to protect individuals' access to justice. If you have concerns or suggestions about its data handling, please get in touch.
