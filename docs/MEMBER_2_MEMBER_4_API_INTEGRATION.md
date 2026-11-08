# Member 2 & Member 4 API Integration Contract

**Specification:** CyberShield AI Inter-Module Communication  
**Integrated By:** Member 4  
**Authoritative AI Engine:** Member 2  
**Status:** Integrated, Tested & Verified  

---

## 1. Background & Integration Architecture

Member 2 authored the standalone AI Scam Message Analyzer engine (`ai-module`), which operates on:
- Endpoint: `POST /api/v1/analyze-message`
- Request Schema: `AnalyzeMessageRequest` (`message: str`, `message_type: str`)
- Response Schema: `AnalyzeMessageResponse` (`category`, `risk_level`, `confidence`, `observed_indicators`, `extracted_indicators`, `explanation`, `recommendations`, `limitations`)

Member 4 maintains the full-stack master project (`CyberShield-AI`), whose frontend expects:
- Endpoint: `POST /api/v1/scans/message`
- Request Schema: `MessageScanRequest` (`content: str`)
- Response Schema: `ScanDetailResponse` (`scan_id`, `scan_type`, `risk_level`, `risk_score`, `report`, `providers_checked`, `message_indicators`, `events`)

---

## 2. Orchestration & Schema Mapping

The Master Backend serves as the secure orchestrator:
```
[ Browser / Frontend UI ]
           │
           │  POST /api/v1/scans/message {"content": "..."}
           ▼
[ Master Backend Gateway ]
           │
           ├──► [ Member 2 AI Engine ] (backend/services/ai_engine/)
           │       ├── Groq / Gemini / OpenAI Failover
           │       ├── EvidenceValidator
           │       └── IndicatorExtractor
           │
           ├──► [ Schema Adapter ] (backend/services/message_analyzer.py)
           │       ├── Risk Level: high_risk -> Critical (score >= 85) / High (score >= 75)
           │       ├── Risk Level: suspicious -> Medium (score 45-74)
           │       ├── Risk Level: low_risk / benign -> Low (score 5-35)
           │       └── Indicators: ObservedIndicator -> MessageIndicator
           │
           ├──► [ URL Threat Intel Cross-Correlation ] (threat_intel/ providers)
           │       └── Embedded URLs queried against URLhaus & PhishTank
           │
           ├──► [ Cryptographic Report Hashing ] (ReportVerifier SHA-256)
           │
           ▼
[ Returns ScanDetailResponse ]
```

---

## 3. Schema Contract Field Comparison

| Member 2 Field | Member 4 Field | Transformation Logic |
| :--- | :--- | :--- |
| `message: str` | `content: str` | Direct mapping to `AnalyzeMessageRequest(message=content)`. |
| `risk_level: "high_risk"` | `risk_level: "Critical" \| "High"` | If confidence $\ge$ 0.85 or severe indicators $\rightarrow$ `Critical`; else `High`. |
| `risk_level: "suspicious"`| `risk_level: "Medium"` | Score mapped to 45–69 range based on confidence. |
| `risk_level: "low_risk"` | `risk_level: "Low"` | Score mapped to 5–25 range based on confidence. |
| `confidence: float` | `risk_score: int` (0–100) | Formulated quantitative score calibrated with risk level. |
| `observed_indicators` | `message_indicators` | Mapped to `MessageIndicator(category, severity, description)`. |
| `extracted_indicators.urls` | `extracted_urls` & DB `IntelligenceResult` | URLs extracted, stored, and sent to URL reputation feeds. |
| `extracted_indicators.phone_numbers` | DB `IntelligenceResult` | Saved as `indicator_type="phone_number"`. |
| `extracted_indicators.emails` | DB `IntelligenceResult` | Saved as `indicator_type="email"`. |
| `explanation` | `report.summary` | Direct mapping into forensic report summary. |
| `recommendations` | `report.recommendations` | Preserved verbatim in report. |

---

## 4. Dual Endpoint Compatibility

To guarantee complete cross-team compatibility:

### 1. Master UI Route: `POST /api/v1/scans/message`
- Consumed by `frontend/src/pages/MessageAnalyzer.tsx`.
- Returns full `ScanDetailResponse` with report hash, audit timeline, and risk gauge score.

### 2. Member 2 Direct Route: `POST /api/v1/analyze-message`
- Available at `http://localhost:8000/api/v1/analyze-message`.
- Directly returns `AnalyzeMessageResponse` matching Member 2's microservice contract.
- Allows Member 1, Member 3, or automated test runners to query Member 2's service directly.
