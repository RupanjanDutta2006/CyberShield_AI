# CyberShield AI — REST API Specification & Contract

This document outlines the REST API endpoints provided by the CyberShield AI backend (`FastAPI`).
Interactive Swagger UI documentation is available at `http://localhost:8000/docs` and ReDoc at `http://localhost:8000/redoc`.

Base URL: `/api/v1`

---

## 1. URL & Domain Scanner

### `POST /api/v1/scans/url`
Submits a URL or domain target for normalization, multi-provider threat intelligence querying, heuristic evaluation, and risk report generation.

**Request Body:**
```json
{
  "url": "https://example-phishing-login.com/auth"
}
```

**Response (`200 OK`):**
```json
{
  "scan_id": "8f489cf3-fbd9-4e67-89a1-2d7f8d689255",
  "target": "https://example-phishing-login.com/auth",
  "normalized_target": "https://example-phishing-login.com/auth",
  "domain": "example-phishing-login.com",
  "hostname": "example-phishing-login.com",
  "scan_type": "url",
  "status": "completed",
  "risk_level": "Critical",
  "risk_score": 92,
  "created_at": "2026-11-07T07:45:00Z",
  "providers_checked": [
    {
      "provider": "URLhaus",
      "status": "match_found",
      "matched": true,
      "verified": true,
      "reference": "https://urlhaus.abuse.ch/url/123456/",
      "details": {
        "threat": "malware_download",
        "url_status": "online"
      }
    },
    {
      "provider": "PhishTank",
      "status": "not_configured",
      "matched": false,
      "verified": false,
      "reference": null,
      "details": {
        "message": "PhishTank API key not configured"
      }
    }
  ],
  "report": {
    "report_id": "9bc303b7-789a-41df-a5c3-339247d8b5c9",
    "summary": "Confirmed malicious destination associated with malware distribution.",
    "evidence": [
      "Matched active malware payload URL on URLhaus blacklist (verified: true).",
      "Heuristic flag: Suspicious sub-structure in domain."
    ],
    "recommendations": [
      "Do not visit or browse this destination.",
      "Block traffic to domain 'example-phishing-login.com' on perimeter firewalls.",
      "Reset credentials if this link was opened previously by staff."
    ],
    "report_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "verification_status": "locally_hashed"
  }
}
```

---

## 2. Suspicious Message & Phishing Analyzer

### `POST /api/v1/scans/message`
Submits an email body, SMS text, or chat snippet for threat indicator analysis (urgency, credential theft, impersonation, sensitive requests).

**Request Body:**
```json
{
  "content": "URGENT: Your bank account will be suspended in 24 hours. Click here to verify your credentials: https://verify-bank.cc/login"
}
```

**Response (`200 OK`):**
```json
{
  "scan_id": "7a3560ec-6f9a-4ba4-9721-678096b86d11",
  "scan_type": "message",
  "status": "completed",
  "risk_level": "High",
  "risk_score": 85,
  "created_at": "2026-11-07T07:46:00Z",
  "analysis_engine": "heuristic_fallback",
  "extracted_urls": [
    "https://verify-bank.cc/login"
  ],
  "indicators": [
    {
      "category": "Urgency & Pressure",
      "severity": "High",
      "description": "Detected psychological urgency tactics ('URGENT', 'suspended in 24 hours')"
    },
    {
      "category": "Credential Harvesting",
      "severity": "Critical",
      "description": "Requests verification of sensitive banking credentials"
    }
  ],
  "report": {
    "report_id": "5fa23d1e-1289-4fa2-bc89-d9012356789a",
    "summary": "High-confidence phishing communication using urgency and credential harvesting patterns.",
    "evidence": [
      "Detected high-pressure deadline phrase: 'suspended in 24 hours'.",
      "Extracted unverified login portal URL: 'https://verify-bank.cc/login'."
    ],
    "recommendations": [
      "Do not click links or reply to the sender.",
      "Report message as phishing to IT Security.",
      "Verify directly with your bank through verified official channels."
    ],
    "report_hash": "a1b2c3d4e5f678901234567890abcdef1234567890abcdef1234567890abcdef",
    "verification_status": "locally_hashed"
  }
}
```

---

## 3. Scan History & Telemetry

### `GET /api/v1/scans`
Query scan records with pagination and filters.

**Query Parameters:**
- `query` (string, optional): search string matched against target/target domain.
- `risk_level` (string, optional): filter by `Critical`, `High`, `Medium`, `Low`, `Unknown`.
- `scan_type` (string, optional): `url`, `domain`, `message`.
- `limit` (integer, default: 20): number of items.
- `offset` (integer, default: 0): pagination offset.

### `GET /api/v1/scans/{scan_id}`
Returns complete scan details including all provider responses, audit events, and generated risk report.

### `GET /api/v1/stats`
Telemetry statistics for dashboard overview:
- `total_scans`: count
- `malicious_count`: count
- `suspicious_count`: count
- `benign_count`: count
- `risk_breakdown`: distribution by level
- `recent_scans`: latest 5 scans

---

## 4. Report Integrity & Verification

### `GET /api/v1/reports/{report_id}`
Retrieves a specific risk report and its SHA-256 cryptographic proof.

### `POST /api/v1/reports/{report_id}/verify`
Recomputes the canonical SHA-256 hash of the report data and compares it against the stored immutable hash.
Returns verification status (`verified` or `failed`), calculation audit, and on-chain blockchain anchoring state if enabled.

---

## 5. System Health & Threat Intel Providers

### `GET /api/v1/system/status`
Returns live subsystem status:
- Database connection (PostgreSQL / SQLite fallback).
- API provider status (URLhaus, PhishTank, Gemini AI, Blockchain).
- Environment flags.

### `GET /api/v1/threat-intel/providers`
Returns configured threat intelligence providers, their authentication status, and capabilities.
