# AI-Powered Web Threat Detection & Digital Trust Intelligence

**Domains:** Artificial Intelligence · Cybersecurity · Web3  
**Build duration:** 48 hours

## 1. Background

Growing reliance on online banking, education, recruitment, commerce, payments and communications exposes people and organisations to phishing, fraudulent links, impersonation, malicious redirects, deceptive ads and credential theft. Fraudulent sites may imitate banks, universities, government services or companies to steal passwords, financial/personal data and authentication credentials.

Trust infrastructure is also at risk: certificates and Certificate Authorities (CAs) underpin HTTPS identity checks, while weak cryptography, compromised CAs and mismanaged chains can undermine trust. The eMudhra TLS certificate incident illustrates why certificate transparency, cryptographic validation and continuous monitoring matter. Insecure configurations, exposed services and outdated software add application-level risk. Existing tools often work separately; the opportunity is an accessible platform combining threat detection, website security analysis, certificate validation and collaborative intelligence.

## 2. Challenge

Build an intelligent platform that helps people and organisations identify phishing, fraudulent links, scams, impersonation and suspicious digital activity before harm occurs. Combine AI, cybersecurity and Web3 to investigate URLs, domains, websites, emails and messages; assess website security; and provide understandable, evidence-based risk assessments. Explain indicators and limitations rather than simply labelling a site safe or malicious.

## 3. Real-world problem scenarios

### A. Phishing and suspicious links

Examples: fake banking/payment gateways; university admission/exam portals; government/tax services; parcel-delivery/payment links; job/internship portals; social-media login pages; fake support/account recovery; shortened URLs and redirect chains. Detect domain spoofing/typosquatting, homoglyphs, suspicious URL/redirect parameters, known campaign domains, claimed-identity mismatches, unexpected redirects and previously reported destinations. **Outcome:** help users assess danger before opening a link or sharing sensitive information.

### B. Certificates and digital trust

HTTPS encrypts connections and authenticates through certificates; it does **not** prove a site is legitimate or non-fraudulent. Inspect expired/invalid certificates, hostname/identity mismatches, untrusted or revoked CAs, unexpected issuance, weak algorithms/key sizes, broken chains, Certificate Transparency (CT) anomalies and known-compromised CAs/intermediates. Monitor CT where useful and distinguish ordinary misconfiguration from compromised trust. An eMudhra-like assessment may flag certificates linked by trusted intelligence/chain data to a compromised or distrusted CA; do **not** claim to detect a CA's internal key-generation weakness from a URL alone.

### C. Scams and social engineering

Examples: fake jobs/internships, investment/crypto scams, giveaways/prizes, refund/cashback fraud, bank/university/company impersonation, fake support, OTP/password/payment-credential requests, fraudulent KYC/account verification and remote-access scams. Accept message/email text; identify suspicious language, impersonation, unusual payment requests, misleading links and attempts to collect sensitive data.

### D. Website security

Safely inspect missing/misconfigured security headers, insecure HTTP, weak TLS, passively detectable exposed sensitive endpoints, suspicious redirects, mixed content and known software/dependency vulnerabilities when reliable version data is public. Explain impact and remediation. Do not exploit vulnerabilities or scan intrusively without explicit authorization.

## 4. Core functional requirements

1. **URL/site analysis:** accept URLs/domains; normalize URLs; inspect domain patterns, phishing/impersonation indicators, redirects/destinations, reputation, available DNS/domain characteristics and threat-report matches. Output domain/site details, indicators, intelligence matches, redirects, risk, evidence and precautions.
2. **TLS/trust analysis:** check certificate validity/expiry, hostname and SAN identity, issuer/chain, revocation/distrust, key strength/signature algorithms, CT records and known-compromised CA/intermediate indicators. Explain whether configuration appears valid, suspicious or potentially compromised based on evidence. A valid certificate is never proof a site is safe.
3. **AI scam/message analysis:** accept pasted messages, emails and notifications; identify social-engineering patterns, urgency/payment manipulation and impersonation; extract URLs, emails, phone numbers and other indicators; correlate with intelligence; explain risks and safety measures. Distinguish suspicion from verified fraud—urgent/persuasive language alone is not proof.
4. **Threat correlation:** connect reports through repeated domains/infrastructure, similar phishing messages, recurring impersonation, previously reported URLs and related indicators. AI may summarize relationships; deterministic matching and evidence must establish connections.
5. **Website assessment:** perform non-exploitative checks of public security information. Each finding includes issue, technical evidence, impact, severity, remediation and limitations. Active testing only on explicitly authorized targets.
6. **Decentralized intelligence:** accept threat reports with URL/domain indicators, campaign reports, incident summaries, report fingerprints and evidence references. Blockchain may record cryptographic commitments, verifiable history, integrity checks, revisions/disputes/validation status and provenance. Keep raw URLs, personal data, email contents, passwords and sensitive data off-chain. An on-chain record proves report integrity/history, not truth.

## 5. User workflow

1. **Submit:** link/domain or suspicious email/message. 2. **Investigate:** gather available domain, certificate, intelligence and technical data. 3. **Analyse:** security checks identify patterns; AI correlates and explains evidence. 4. **Assess:** provide threats, supporting evidence and precautions. 5. **Report/verify:** optionally submit an incident; record an on-chain cryptographic commitment for independent verification.

## 6. Risk classification and report

Use consistent labels:
- **Low risk:** no significant malicious indicators found within available checks.
- **Suspicious:** one or more indicators need further investigation.
- **High risk:** multiple significant indicators suggest substantial threat.
- **Confirmed malicious:** authoritative threat intelligence or sufficient validation supports the finding.
- **Inconclusive:** insufficient data or unavailable verification sources.

Every assessment includes classification, indicators, technical evidence, source for important findings, timestamp, confidence/evidence coverage, recommended actions, limitations and unavailable checks. Absence of known threats does not prove safety.

## 7. Mandatory 48-hour MVP

Deliver an end-to-end functional prototype with: URL/domain investigation; phishing indicators; TLS certificate/trust checks; evidence-grounded AI explanations; pasted-message scam analysis; structured/explainable risk classification; at least one external intelligence source or documented dataset; on-chain threat-report registry or equivalent; independent report-integrity verification; functional dashboard; and tests demonstrating at least **3 suspicious + 3 benign** cases. Prioritize a working URL pipeline with meaningful checks and reliable output; not every advanced feature is required.

## 8. Suggested technology

Any suitable stack is allowed. **AI:** LLMs, NLP, ML, anomaly detection, RAG. **URL intelligence:** Google Safe Browsing, URLhaus, PhishTank, OpenPhish, VirusTotal. **Web security:** Python SSL libraries, OpenSSL, DNS and HTTP-header inspection. **Certificates:** CT logs, crt.sh, public CA trust data. **Blockchain:** Solidity, EVM networks, smart contracts. **Backend:** Python/FastAPI or Node.js. **Frontend:** React, Next.js, TypeScript. **Data:** PostgreSQL, MongoDB, Redis. **Infrastructure:** Docker/cloud. External APIs, open-source tools, existing models and public datasets are allowed; teams need not train models from scratch.

## 9. Security and privacy

- **Safe URL inspection:** defend against SSRF/internal-network access; validate redirects and destination IPs; do not execute scripts or download suspicious files; isolate inspection; enforce limits/timeouts.
- **AI:** treat web content/messages as untrusted; prevent prompt injection from affecting security decisions; require evidence for important findings; avoid unnecessary sharing of sensitive data with external AI services.
- **Privacy:** never request passwords, OTPs, private keys or seed phrases; minimize personal-data collection; keep sensitive data off public blockchains; protect credentials and reports.
- **Operations:** never execute malware or exploit sites; no intrusive testing without authorization; passing automated checks does not mean a site is secure.

## 10. Expected deliverables

1. Working web prototype with URL/domain investigation. 2. Public GitHub repository with source and setup instructions. 3. AI scam-analysis demo with evidence-based explanations. 4. Cybersecurity demo of phishing/suspicious-site investigation, including TLS. 5. Web3 demo: testnet smart contract or reproducible local blockchain. 6. Verification evidence: contract address and transaction reference, or reproducible equivalent. 7. Technical documentation: architecture, pipeline, intelligence sources and methodology. 8. Test report with legitimate and suspicious cases/results. 9. Live end-to-end demo: submission → investigation → risk assessment → threat report.

## 11. Evaluation

| Category | Weight | Focus |
|---|---:|---|
| Cybersecurity & threat detection | 30% | Phishing, certificate analysis, evidence quality, false-positive handling |
| AI implementation | 20% | Intelligent/contextual analysis and explainability |
| Web3 integration | 20% | Meaningful reporting, integrity and independent verification |
| Technical implementation | 20% | Working architecture, reliability and integration |
| Innovation & user experience | 10% | Practical relevance, usability and originality |
| **Total** | **100%** | Demonstrated functionality matters more than number of technologies/APIs. |

## 12. Optional extensions

Browser extension/pre-navigation checks; real-time protection; QR scam detection; screenshot-based impersonation detection; email analysis; domain monitoring/alerts for suspicious issuance; lookalike/homoglyph detection; monitoring compromised CAs; automated header/TLS audits; intelligence-sharing APIs; community reporting/validation; organisation security-monitoring dashboard. These are optional and must not displace the MVP.

## 13. Scope boundaries

Within 48 hours, teams are not expected to build antivirus, train foundation models, detect every attack, reproduce/exploit real vulnerabilities, build a commercial-scale intelligence database, support every CA/blockchain, scan without authorization, or guarantee all sites are safe/malicious. Target outcome: a focused, reliable prototype identifying real phishing patterns, inspecting TLS trust, explaining evidence and verifying threat reports.

## 14. Final objective

Build an accessible intelligent security platform that helps people and organisations identify potentially malicious websites, avoid phishing, recognize scams and understand website risks. Demonstrate AI investigating/correlating activity, cybersecurity validating technical threats, and Web3 enabling transparent, verifiable intelligence sharing—helping people detect digital deception before becoming victims.
