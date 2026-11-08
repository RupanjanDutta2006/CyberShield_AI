# CyberShield AI --- Member 1 Core Backend Roadmap

**Role:** Member 1 --- Core Backend Lead\
**Project:** CyberShield AI --- AI-Powered Web Threat Detection &
Digital Trust Intelligence\
**Roadmap scope:** Phase 1 --- 20 implementation Parts\
**Primary stack:** Python, FastAPI, Pydantic\
**Schedule reference:** 48-hour hackathon plan (development through Hour
40; final 8 hours for testing and stabilization)

------------------------------------------------------------------------

## 1. Roadmap objective

Member 1 owns the central backend that receives user input, coordinates
technical inspection services, combines findings, calculates a
deterministic risk classification, and returns a consistent threat
report.

The backend must integrate with:

-   **Member 2:** AI scam-message analysis and evidence-grounded
    explanations.
-   **Member 3:** Blockchain report fingerprint registration and
    verification.
-   **Member 4:** Threat-intelligence lookup, database persistence, and
    later frontend integration.

This roadmap divides the Core Backend work into five stages and twenty
sequential Parts. Complete and test each Part before treating it as
finished.

## 2. Important project rules

1.  Keep the backend modular and maintain clear service boundaries.
2.  Agree on public API contracts and the common report schema with all
    team members.
3.  Do not treat a valid HTTPS certificate as proof that a website is
    legitimate.
4.  A threat-intelligence no-match is not proof that a URL is safe.
5.  Missing or unavailable checks must be reported as unavailable or
    inconclusive, not safe.
6.  Do not classify a URL as **Confirmed Malicious** solely because an
    LLM says so. This label requires authoritative threat intelligence
    or sufficient documented validation.
7.  Prevent SSRF: block localhost, private, link-local, reserved, and
    otherwise prohibited destinations.
8.  Revalidate every redirect destination before following it.
9.  Apply timeouts, response-size limits, redirect limits, and
    controlled error handling.
10. Do not exploit websites, execute downloaded content, or perform
    intrusive testing without authorization.
11. Keep deterministic technical evidence separate from AI
    interpretation.
12. Keep secrets in environment variables. Never commit API keys,
    private keys, or `.env` files.
13. Do not invent scan results, intelligence evidence, or confidence
    values.
14. Blockchain registration proves that a fingerprint was registered; it
    does not prove that the report itself is true.

## 3. Five-stage overview

  --------------------------------------------------------------------------------
  Stage                            Parts Focus            Main output
  ---------------- --------------------- ---------------- ------------------------
  Stage 1                           1--4 Backend          Running FastAPI
                                         foundation       skeleton, project
                                                          structure, agreed API
                                                          and report schemas

  Stage 2                           5--8 URL              Validated, normalized
                                         investigation    URL input and initial
                                         engine           URL indicators

  Stage 3                          9--12 Technical        DNS, redirect, TLS, and
                                         website          HTTP security-header
                                         investigation    findings

  Stage 4                         13--16 Risk assessment  Standardized evidence,
                                                          severity classification,
                                                          deterministic risk
                                                          result, unified report

  Stage 5                         17--20 API,             Core APIs, integrated
                                         integration, and modules,
                                         stabilization    persistence/blockchain
                                                          interfaces, tested
                                                          backend
  --------------------------------------------------------------------------------

------------------------------------------------------------------------

# Stage 1 --- Backend Foundation

## Part 1 --- Project Architecture & Requirement Understanding

**Objective:** Understand the project requirements and define the
backend architecture before implementation.

### Tasks

-   Read the CyberShield AI problem statement and team execution
    blueprint.
-   Identify the required user journeys:
    -   URL and website investigation.
    -   Scam-message analysis through the AI module.
    -   Threat-report integrity registration and verification.
-   Identify Member 1's responsibilities and boundaries.
-   Define backend service responsibilities and module boundaries.
-   Identify dependencies on Members 2, 3, and 4.
-   Draw the high-level backend architecture and data flow.
-   Record assumptions, unresolved decisions, and integration risks.

### Expected output

-   Backend architecture diagram.
-   Responsibility and service-boundary notes.
-   Initial dependency and integration list.

### Definition of done

-   The team understands which module owns each responsibility.
-   Member 1's scope is clear.
-   External module dependencies and handoff points are documented.

## Part 2 --- Development Environment Setup

**Objective:** Prepare a repeatable local development environment.

### Tasks

-   Check the installed Python version and existing project environment.
-   Create or activate a virtual environment if the project does not
    already have one.
-   Set up FastAPI and the project's ASGI server.
-   Add only the dependencies actually required by the implementation.
-   Configure environment-variable loading.
-   Create or update `.env.example` with placeholder values only.
-   Ensure `.env` and other secret files are ignored by Git.
-   Add a basic application startup command.
-   Confirm the backend can start locally.

### Expected output

-   Working local Python environment.
-   FastAPI application starts successfully.
-   Documented dependency and startup commands.
-   Safe environment-variable template.

### Definition of done

-   Another team member can follow the setup instructions and start the
    backend.
-   No secret is committed to the repository.

## Part 3 --- Backend Folder Structure

**Objective:** Organize the backend so each feature can be developed and
tested independently.

### Suggested structure

``` text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   ├── schemas/
│   ├── core/
│   ├── services/
│   │   ├── url_investigation/
│   │   ├── dns/
│   │   ├── redirects/
│   │   ├── tls_analysis/
│   │   ├── security_headers/
│   │   ├── risk_engine/
│   │   ├── ai_analysis/
│   │   ├── threat_intelligence/
│   │   └── blockchain/
│   ├── database/
│   └── utils/
├── tests/
├── requirements.txt
└── README.md
```

### Tasks

-   Create or adapt the application entry point.
-   Separate API routes from business logic.
-   Separate Pydantic schemas from service implementation.
-   Create service modules for URL, DNS, redirects, TLS, headers, and
    risk engine.
-   Create integration interfaces for AI, threat intelligence, database,
    and blockchain.
-   Create a tests directory.
-   Add a README with setup and run instructions.

### Expected output

-   Consistent backend directory structure.
-   Clear separation between API, schemas, services, configuration, and
    tests.

### Definition of done

-   The app starts from the agreed entry point.
-   Each major service has a clear location.
-   No unnecessary duplicate project structure is introduced.

## Part 4 --- API Contract & Common Threat Report Schema

**Objective:** Agree on stable request and response formats before
parallel module integration.

### Tasks

-   Define request models for URL scanning.
-   Define response models for scan results.
-   Define common finding and evidence structures.
-   Define risk classification values.
-   Define how unavailable checks and partial results are represented.
-   Define the common Threat Report schema with all four members.
-   Define the fields required by the AI, threat-intelligence, database,
    and blockchain interfaces.
-   Record schema versioning and change-control rules.
-   Publish example request and response JSON.

### Proposed initial API endpoints

  ---------------------------------------------------------------------------
  Method                  Endpoint                    Purpose
  ----------------------- --------------------------- -----------------------
  `POST`                  `/api/v1/scan-url`          Investigate a URL

  `POST`                  `/api/v1/analyze-message`   Expose the AI
                                                      message-analysis flow
                                                      through the backend

  `GET`                   `/api/v1/scans/{scan_id}`   Retrieve a scan report

  `GET`                   `/api/v1/history`           Retrieve scan/report
                                                      history

  `POST`                  `/api/v1/reports`           Save/register a threat
                                                      report

  `POST`                  `/api/v1/reports/verify`    Verify a report
                                                      fingerprint

  `GET`                   `/api/v1/health`            Backend health check
  ---------------------------------------------------------------------------

These are proposed project interfaces. Confirm exact request and
response details with the relevant module owners before implementation.

### Proposed common report shape

``` json
{
  "scan_id": "generated-id",
  "submitted_input": {
    "type": "url",
    "value": "https://example.test"
  },
  "timestamp": "ISO-8601 timestamp",
  "risk": {
    "classification": "inconclusive",
    "score": null,
    "confidence": null,
    "method": "documented deterministic rules"
  },
  "technical_findings": [],
  "threat_intelligence": [],
  "ai_analysis": null,
  "recommendations": [],
  "limitations": [],
  "report_integrity": {
    "report_hash": null,
    "blockchain_network": null,
    "contract_address": null,
    "transaction_hash": null,
    "verification_status": "not_registered"
  }
}
```

This is a starting proposal, not a substitute for the team's agreed
final schema.

### Expected output

-   Versioned Pydantic request and response models.
-   API contract document.
-   Example JSON fixtures.
-   Agreement from Members 2, 3, and 4 on their integration fields.

### Definition of done

-   All members know the expected input and output formats.
-   Schema changes have an agreed review process.
-   Unavailable values and partial results have defined representations.

------------------------------------------------------------------------

# Stage 2 --- URL Investigation Engine

## Part 5 --- URL Input Validation

**Objective:** Accept URL input safely and reject malformed or
prohibited input before network activity.

### Tasks

-   Accept a URL through the scan request model.
-   Reject empty input and malformed URL values.
-   Validate the URL scheme; allow only the schemes agreed by the
    project (normally HTTP and HTTPS).
-   Validate hostname presence and syntax.
-   Reject unsupported schemes and malformed ports.
-   Apply input length limits.
-   Return structured validation errors.
-   Add tests for valid, invalid, empty, malformed, and
    unsupported-scheme inputs.

### Expected output

-   URL validation service.
-   Pydantic request validation.
-   Controlled error responses and tests.

### Definition of done

-   Invalid input is rejected before any outbound request.
-   Valid test URLs pass validation.
-   Error responses follow the agreed API contract.

## Part 6 --- URL Normalization

**Objective:** Parse URLs into consistent components for downstream
investigation.

### Tasks

-   Normalize scheme and hostname according to a documented policy.
-   Parse hostname, port, path, query, and fragment.
-   Extract the registrable domain where a suitable library is
    available.
-   Handle internationalized domain names consistently.
-   Define treatment of default ports and trailing dots.
-   Avoid changing URL components in ways that alter their meaning.
-   Preserve the submitted input separately where required for
    reporting.
-   Add unit tests for equivalent and edge-case URL representations.

### Expected output

-   Reusable URL normalization function.
-   Structured parsed-URL object.
-   Test cases and documented normalization rules.

### Definition of done

-   Downstream services receive consistent parsed URL data.
-   Original user input is not silently lost.
-   Normalization does not accidentally transform an unsafe destination
    into an allowed one.

## Part 7 --- IP & Hostname Security Validation

**Objective:** Prevent the scanner from reaching internal or otherwise
prohibited network destinations.

### Tasks

-   Resolve hostnames using a controlled DNS resolution process.
-   Validate IPv4 and IPv6 addresses.
-   Detect loopback, private, link-local, reserved, multicast, and
    unspecified addresses.
-   Block localhost and prohibited internal destinations.
-   Validate all resolved addresses, not only one returned address.
-   Revalidate the destination at connection time to reduce
    DNS-rebinding risk.
-   Ensure the HTTP client connects only to an address that passed
    validation while preserving correct hostname/TLS verification.
-   Do not allow user-controlled proxy settings or alternate routing to
    bypass checks.
-   Add tests for public addresses, private addresses, localhost, IPv6
    local addresses, and mixed DNS answers.

### Expected output

-   Safe destination validation service.
-   Explicit allow/block decision and reason.
-   SSRF-focused tests.

### Definition of done

-   Requests to prohibited destinations are blocked.
-   DNS resolution failures are reported as unavailable or failed
    checks, not safe.
-   Destination validation is applied before every outbound connection.

## Part 8 --- Suspicious URL Pattern Detection

**Objective:** Identify URL characteristics that may warrant additional
investigation.

### Tasks

-   Detect IP-address-based URLs.
-   Identify unusually long or deeply nested subdomains.
-   Identify known URL-shortener patterns where a maintained list is
    available.
-   Detect suspicious encoding and unusual URL structures.
-   Identify possible lookalike or homograph indicators.
-   Detect suspicious use of user-info components and unusual ports.
-   Return indicators with evidence and severity rather than making
    unsupported final claims.
-   Add benign and suspicious fixture tests.

### Expected output

-   Initial URL-pattern analysis service.
-   Standardized findings with evidence and severity.

### Definition of done

-   Findings explain which observed URL characteristic triggered them.
-   Heuristics are not presented as proof of maliciousness.
-   Benign test URLs do not automatically receive high-risk
    classifications.

------------------------------------------------------------------------

# Stage 3 --- Technical Website Investigation

## Part 9 --- DNS & Domain Investigation

**Objective:** Collect relevant DNS and domain-resolution information.

### Tasks

-   Query A and AAAA records where available.
-   Query CNAME records where relevant.
-   Query MX and NS records where useful.
-   Record lookup status and timestamp.
-   Handle NXDOMAIN, timeout, SERVFAIL, and empty answers distinctly.
-   Apply DNS timeouts and response limits.
-   Revalidate resolved addresses under Part 7's destination-safety
    rules.
-   Return findings in the common evidence format.

### Expected output

-   DNS investigation service.
-   Structured DNS findings and failure states.

### Definition of done

-   DNS results are represented consistently.
-   DNS failure is not interpreted as proof of maliciousness or safety.
-   DNS-derived addresses cannot bypass destination controls.

## Part 10 --- Safe Redirect Analysis

**Objective:** Inspect redirect behavior without following a redirect to
an unsafe destination.

### Tasks

-   Make controlled HTTP requests with automatic redirect following
    disabled initially.
-   Detect redirect response codes and `Location` values.
-   Parse and resolve each next destination.
-   Apply Part 5 and Part 7 validation to every redirect target.
-   Enforce a maximum redirect count.
-   Detect loops and repeated destinations.
-   Apply connection and total-operation timeouts.
-   Record the redirect chain and the point where a redirect is blocked.
-   Do not download or execute page scripts or files.

### Expected output

-   Safe redirect-inspection service.
-   Redirect-chain evidence and blocked-destination reason.

### Definition of done

-   Every redirect destination is revalidated before it is contacted.
-   Redirect loops and excessive chains stop safely.
-   Redirect inspection cannot reach prohibited internal destinations.

## Part 11 --- TLS & SSL Certificate Analysis

**Objective:** Inspect certificate and TLS trust signals for HTTPS
endpoints.

### Tasks

-   Establish a TLS connection using safe connection handling.
-   Verify certificate validity.
-   Verify hostname/SAN matching.
-   Record certificate expiry and validity period.
-   Record issuer and subject information where available.
-   Collect certificate-chain information where available.
-   Record negotiated TLS information where practical.
-   Handle expired, self-signed, hostname-mismatched, and unavailable
    certificates distinctly.
-   Apply connection timeouts.
-   Keep certificate findings separate from overall website legitimacy.

### Expected output

-   TLS inspection service.
-   Structured certificate findings and limitations.

### Definition of done

-   Certificate and hostname validation results are explicit.
-   TLS failures do not crash the whole scan.
-   A valid certificate is never treated as proof that the website is
    legitimate.

## Part 12 --- HTTP Security Headers Analysis

**Objective:** Inspect selected HTTP response headers for basic
web-security configuration signals.

### Tasks

-   Collect response headers from the controlled HTTP request.
-   Inspect HSTS (`Strict-Transport-Security`).
-   Inspect Content-Security-Policy.
-   Inspect X-Content-Type-Options.
-   Inspect X-Frame-Options.
-   Inspect Referrer-Policy.
-   Add other selected headers only where the project has a clear
    reason.
-   Distinguish missing headers from malformed or weak values.
-   Record the response status and whether the check was possible.
-   Avoid making exploit attempts or intrusive vulnerability tests.

### Expected output

-   HTTP security-header analysis service.
-   Findings with observed values and limitations.

### Definition of done

-   Header findings are reproducible and evidence-based.
-   Missing headers are not automatically described as proof of
    compromise.
-   Unreachable endpoints are represented as unavailable.

------------------------------------------------------------------------

# Stage 4 --- Risk Assessment Engine

## Part 13 --- Evidence Collection & Standardization

**Objective:** Convert outputs from technical services into one
consistent evidence model.

### Tasks

-   Define the common finding structure.
-   Include finding type, severity, description, observed evidence,
    source, and timestamp where applicable.
-   Normalize URL-pattern, DNS, redirect, TLS, and header results.
-   Preserve the original observed value where useful and safe.
-   Mark checks as completed, unavailable, failed, or not applicable.
-   Keep technical observations distinct from AI explanations.
-   Deduplicate identical findings without losing source references.
-   Add tests for normalizing each service's output.

### Expected output

-   Common evidence/finding model.
-   Finding normalization service.
-   Unit tests for each technical finding category.

### Definition of done

-   The risk engine receives consistent finding objects.
-   Findings retain their evidence and source.
-   Unavailable checks remain distinguishable from negative findings.

## Part 14 --- Severity & Indicator Classification

**Objective:** Assign consistent severity and authority metadata to
individual indicators.

### Tasks

-   Define allowed severity levels, such as Informational, Low, Medium,
    and High.
-   Document severity rules for each technical indicator.
-   Identify authoritative versus heuristic indicators.
-   Record the evidence source and source status.
-   Handle duplicate or correlated indicators.
-   Prevent multiple representations of the same underlying issue from
    being counted repeatedly.
-   Define how unavailable checks affect coverage and confidence.
-   Add tests for severity mapping and duplicate handling.

### Expected output

-   Indicator classification rules.
-   Severity mapping module.
-   Documented evidence-authority policy.

### Definition of done

-   Each indicator has a documented severity basis.
-   Correlated indicators are not blindly double-counted.
-   Heuristic findings are not represented as authoritative
    confirmation.

## Part 15 --- Deterministic Risk Engine

**Objective:** Aggregate evidence into an explainable risk
classification using documented deterministic rules.

### Tasks

-   Define the risk aggregation rules.
-   Decide whether a numeric score is useful and document its meaning.
-   Map indicator combinations to Low Risk, Suspicious, High Risk,
    Confirmed Malicious, or Inconclusive.
-   Define authoritative evidence requirements for Confirmed Malicious.
-   Handle conflicting evidence.
-   Handle missing, failed, and unavailable checks.
-   Avoid treating a no-match intelligence result as proof of safety.
-   Avoid treating HTTPS as proof of legitimacy.
-   Avoid allowing an LLM's unsupported opinion to override technical
    evidence.
-   Add unit tests for benign, suspicious, high-risk, conflicting, and
    inconclusive cases.

### Risk classifications

  -----------------------------------------------------------------------
  Classification                      Meaning
  ----------------------------------- -----------------------------------
  Low Risk                            No significant malicious indicators
                                      were found within the checks
                                      performed; this does not prove the
                                      site is safe.

  Suspicious                          One or more indicators require
                                      further investigation.

  High Risk                           Multiple significant indicators
                                      suggest a substantial threat.

  Confirmed Malicious                 An authoritative
                                      threat-intelligence source or
                                      sufficient documented validation
                                      supports the finding.

  Inconclusive                        There is insufficient information
                                      or important checks were
                                      unavailable.
  -----------------------------------------------------------------------

### Expected output

-   Deterministic risk engine.
-   Documented rule set.
-   Test suite and sample explanations for classifications.

### Definition of done

-   The same evidence produces the same risk result.
-   Every classification can be explained through its supporting
    evidence.
-   Confirmed Malicious requires the documented authority/validation
    threshold.
-   Missing data does not become a clean result.

## Part 16 --- Final Risk Report Generator

**Objective:** Combine the scan input, technical findings, risk result,
external module outputs, recommendations, and limitations into the
common report structure.

### Tasks

-   Generate a unique scan ID.
-   Add submitted-input metadata and timestamp.
-   Include the risk classification and documented method.
-   Include technical findings.
-   Add the threat-intelligence module's normalized results when
    available.
-   Add AI analysis as a separate field when available.
-   Add recommendations grounded in the findings.
-   Add limitations and unavailable checks.
-   Add report-integrity placeholders or metadata when blockchain
    integration is not yet completed.
-   Validate the final object against the common Pydantic report schema.
-   Add fixture-based report tests.

### Expected output

-   Unified Threat Report builder.
-   Validated JSON report.
-   Example reports for different risk outcomes.

### Definition of done

-   Each completed scan returns a schema-valid report.
-   Partial failures appear in limitations or status fields.
-   AI inference is not mixed with deterministic technical findings.
-   No score or confidence is invented when it is not supported.

------------------------------------------------------------------------

# Stage 5 --- API Integration & Backend Stabilization

## Part 17 --- Core API Development

**Objective:** Expose the core backend functions through stable FastAPI
endpoints.

### Tasks

-   Implement `POST /api/v1/scan-url`.
-   Implement `GET /api/v1/scans/{scan_id}` where report retrieval is
    available.
-   Implement `GET /api/v1/health`.
-   Add request and response validation.
-   Use consistent HTTP status codes and error structures.
-   Add request-size and input limits.
-   Add API-level timeouts where appropriate.
-   Configure CORS for the agreed frontend origin(s), not unrestricted
    access by default.
-   Generate and review OpenAPI/Swagger documentation.
-   Add API tests.

### Expected output

-   Working core API endpoints.
-   Stable response formats.
-   OpenAPI documentation and API tests.

### Definition of done

-   A valid URL can be submitted through the API.
-   Invalid input receives a controlled response.
-   The health endpoint reports service status accurately.
-   The API response matches the agreed contract.

## Part 18 --- AI & Threat Intelligence Integration

**Objective:** Connect Member 2's AI module and Member 4's
threat-intelligence service to the core report pipeline.

### Tasks

-   Confirm the callable interface and schema from Member 2.
-   Confirm the callable interface and normalized response schema from
    Member 4.
-   Add adapters or service clients without coupling the core risk
    engine to provider-specific response formats.
-   Integrate scam-message analysis through the agreed API flow.
-   Integrate extracted URLs/domains into URL investigation where the
    team has agreed to support that flow.
-   Include threat-intelligence source, timestamp, match status,
    evidence, and source availability.
-   Keep AI analysis separate from technical findings.
-   Apply timeouts and controlled failure handling.
-   Ensure unavailable external services produce partial reports rather
    than crashing the whole scan.
-   Add integration tests with real or clearly labelled mock responses.

### Expected output

-   AI integration adapter.
-   Threat-intelligence integration adapter.
-   Integrated report output with source and limitation metadata.

### Definition of done

-   Both modules can be called through agreed interfaces.
-   Their outputs match the shared schema.
-   Provider failure is represented accurately.
-   No-match and AI-only results are not presented as confirmed safety
    or maliciousness.

## Part 19 --- Database & Blockchain Integration

**Objective:** Connect report persistence and blockchain integrity
services through the agreed module interfaces.

### Tasks

-   Confirm Member 4's database interface and data model.
-   Agree which report metadata should be stored.
-   Apply data minimization; avoid retaining full user messages or
    sensitive content without a justified need.
-   Connect report save and retrieval operations.
-   Confirm Member 3's blockchain registration and verification
    interface.
-   Define the exact report representation and fields used for
    fingerprinting with Member 3.
-   Ensure Python and TypeScript hashing behavior is compatible if both
    are used.
-   Send only the approved fingerprint and minimal non-sensitive
    metadata to the blockchain service.
-   Store transaction reference and verification metadata off-chain as
    agreed.
-   Handle unavailable chain, failed transactions, duplicate
    registrations, and verification failures.
-   Add integration tests.

### Expected output

-   Database integration.
-   Blockchain registration/verification adapter.
-   Report metadata retrieval and integrity information.

### Definition of done

-   Reports can be saved and retrieved through the agreed interface.
-   Blockchain registration and verification can be called through the
    backend.
-   Sensitive report contents are not written on-chain.
-   Chain failure does not corrupt the original scan result.

## Part 20 --- Backend Testing, Security & Final Integration

**Objective:** Verify that the complete backend is reliable, safe, and
ready for frontend integration and demonstration.

### Tasks

-   Run unit tests for each service.
-   Run API tests for all core endpoints.
-   Run integration tests across URL validation, technical checks, risk
    aggregation, and report generation.
-   Test invalid and malformed URLs.
-   Test localhost, private, link-local, reserved, and IPv6 prohibited
    destinations.
-   Test redirects to prohibited destinations.
-   Test redirect loops and excessive redirect chains.
-   Test DNS failures and timeouts.
-   Test TLS hostname mismatch and certificate failure handling where
    feasible.
-   Test unavailable threat-intelligence and AI providers.
-   Test incomplete or partial scan results.
-   Test report persistence and retrieval.
-   Test blockchain registration, verification, duplicate handling, and
    unavailable-chain behavior.
-   Review logs to ensure secrets and unnecessary sensitive input are
    not exposed.
-   Review timeout, response-size, and error-handling behavior.
-   Update README, setup instructions, API documentation, and test
    report.
-   Confirm frontend integration readiness with Member 4.

### Expected output

-   Backend test report.
-   Security test results.
-   Updated documentation.
-   Stable backend release for integration/demo.

### Definition of done

-   Critical backend test cases pass.
-   SSRF protections are tested.
-   Partial failures do not crash the entire scan.
-   API contracts are stable and documented.
-   Frontend can consume the agreed endpoints.
-   Known limitations and unresolved issues are documented.

------------------------------------------------------------------------

## 4. Suggested development schedule

This follows the team's 48-hour blueprint. The Parts are work packages;
some integration work continues across multiple time windows.

  -----------------------------------------------------------------------
  Time window                         Main work
  ----------------------------------- -----------------------------------
  H0--H3                              Parts 1--4: architecture, setup,
                                      structure, contracts

  H3--H8                              Parts 5--8: URL validation,
                                      normalization, destination safety,
                                      URL patterns

  H8--H14                             Parts 9--12: DNS, redirects, TLS,
                                      security headers

  H14--H19                            Parts 13--16: evidence, severity,
                                      risk engine, report generation

  H19--H24                            Prepare and begin Parts 17--19
                                      integration; stabilize interfaces

  H24--H30                            Continue API and module integration

  H30--H40                            Complete integration, reliability,
                                      documentation, and frontend support

  H40--H48                            Final testing, critical fixes, and
                                      demo stabilization
  -----------------------------------------------------------------------

## 5. Required backend deliverables

-   [ ] FastAPI application that starts reliably.
-   [ ] URL validation and normalization service.
-   [ ] Safe URL/domain investigation pipeline.
-   [ ] DNS/domain information collection.
-   [ ] Safe redirect inspection.
-   [ ] TLS certificate and hostname validation.
-   [ ] Selected HTTP security-header checks.
-   [ ] Deterministic, explainable risk engine.
-   [ ] Common Threat Report schema.
-   [ ] AI integration interface.
-   [ ] Threat-intelligence integration interface.
-   [ ] Database integration interface.
-   [ ] Blockchain registration/verification interface.
-   [ ] API documentation.
-   [ ] Unit and integration tests.
-   [ ] Security test results.
-   [ ] Setup instructions and backend README.

## 6. Team handoff checklist

### With Member 2 --- AI

-   [ ] Agree on the AI input and output schema.
-   [ ] Confirm how message analysis is called.
-   [ ] Keep AI inference separate from technical evidence.
-   [ ] Agree on timeout and provider-failure behavior.

### With Member 3 --- Blockchain

-   [ ] Agree on the exact report representation to fingerprint.
-   [ ] Agree on canonicalization and hash algorithm.
-   [ ] Confirm registration and verification request/response formats.
-   [ ] Keep report content and sensitive data off-chain.

### With Member 4 --- Threat Intelligence & Database

-   [ ] Agree on normalized intelligence result format.
-   [ ] Agree on database ownership and persistence interface.
-   [ ] Agree on scan/report retrieval interface.
-   [ ] Confirm how unavailable intelligence sources are represented.

## 7. Collaboration and Git rules

-   Use the team's agreed branch ownership and do not push unfinished
    work directly to `main`.
-   Make small, meaningful commits.
-   Keep `.env` files and secrets out of Git.
-   Maintain `.env.example` with placeholder variable names.
-   Document setup and run commands.
-   Communicate breaking API/schema changes before implementing them.
-   Use mocks only when clearly labelled and replace them before final
    testing.
-   Integrate continuously rather than waiting until the end.
-   Keep a shared list of blockers, decisions, and owners.

## 8. Final acceptance checklist

The Core Backend can be considered ready for the hackathon demonstration
when:

-   [ ] A valid URL can be submitted through the API.
-   [ ] Invalid input is rejected safely.
-   [ ] The backend performs the agreed technical checks.
-   [ ] Prohibited internal destinations and unsafe redirects are
    blocked.
-   [ ] Findings include evidence and source/status information where
    available.
-   [ ] A deterministic risk classification is generated.
-   [ ] Missing checks and service failures are represented as
    limitations.
-   [ ] AI and threat-intelligence results are integrated using agreed
    schemas.
-   [ ] A unified report is returned.
-   [ ] Report persistence and blockchain integration work through the
    agreed interfaces.
-   [ ] The backend does not claim that a site is safe solely because no
    threat was found.
-   [ ] The backend does not claim that a report is true merely because
    its hash is on-chain.
-   [ ] API documentation, setup instructions, and test results are
    available.

------------------------------------------------------------------------

## 9. How to use this roadmap

1.  Start with **Part 1** only.
2.  Break that Part into small implementation steps.
3.  For every step, record the files changed, commands run, and test
    results.
4.  Mark a Part complete only after its Definition of done is satisfied.
5.  If a dependency or schema is still changing, record it as a blocker
    instead of guessing.
6.  Do not skip ahead when a foundational Part is incomplete.
7.  Keep this Markdown file as the roadmap and maintain progress
    separately if needed.

**Important:** This roadmap defines the planned work and acceptance
criteria. It does not claim that any Part has already been implemented
or tested.
