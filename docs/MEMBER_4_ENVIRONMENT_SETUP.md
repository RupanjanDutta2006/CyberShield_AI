# CyberShield AI — Environment Configuration & Setup Guide

This document explains the runtime requirements, environment variables, startup scripts, and graceful fallback behaviors for CyberShield AI.

---

## 1. Quick-Start (PowerShell)

The master repository provides automated 1-click execution scripts in the root directory:

```powershell
# 1. Navigate to Master Project
cd "D:\My Created Projects\CyberShield-AI\CyberShield-AI"

# 2. Run All Automated Tests (25 Master Tests)
.\run-tests.ps1

# 3. Start the Full-Stack Application
.\run-server.ps1
```

Once running:
- **Full-Stack Application UI**: `http://localhost:8000`
- **Swagger Interactive API Documentation**: `http://localhost:8000/docs`
- **Alternative Redoc Documentation**: `http://localhost:8000/redoc`

---

## 2. Environment Variables Specification (`.env`)

Create `.env` in `D:\My Created Projects\CyberShield-AI\CyberShield-AI\.env`:

```ini
# Application Configuration
ENVIRONMENT=development
DEBUG=True
PORT=8000
HOST=0.0.0.0
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Relational Database
# In production: postgresql://username:password@localhost:5432/cybershield
# If unconfigured: automatically uses embedded SQLite (cybershield.db)
DATABASE_URL=sqlite:///./cybershield.db

# Member 2 AI Scam Analysis Engine (Multi-Tier Failover)
# Tier 1: Groq Cloud (Primary - Ultra-low latency)
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b

# Tier 2: Google Gemini (Backup 1)
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-flash

# Tier 3: OpenAI (Backup 2)
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# External Threat Intelligence (Optional)
URLHAUS_AUTH_KEY=
URLHAUS_API_URL=https://urlhaus-api.abuse.ch/v1
PHISHTANK_APP_KEY=
PHISHTANK_API_URL=https://checkurl.phishtank.com/checkurl/

# Blockchain Verification (Optional Web3)
BLOCKCHAIN_RPC_URL=
BLOCKCHAIN_PRIVATE_KEY=
BLOCKCHAIN_CONTRACT_ADDRESS=
```

---

## 3. Required vs Optional Credentials Matrix

| Provider / Dependency | Environment Variable | Necessity | Free Source | Fallback Mechanism |
| :--- | :--- | :---: | :--- | :--- |
| **Groq Cloud** | `GROQ_API_KEY` | **Recommended** | [console.groq.com](https://console.groq.com/keys) | Automatic failover to Tier 2 (Gemini). |
| **Google Gemini** | `GEMINI_API_KEY` | Optional | [aistudio.google.com](https://aistudio.google.com/) | Automatic failover to Tier 3 (OpenAI). |
| **OpenAI** | `OPENAI_API_KEY` | Optional | [platform.openai.com](https://platform.openai.com/api-keys) | Automatic failover to Tier 4 (Offline Heuristics). |
| **URLhaus Feed** | `URLHAUS_AUTH_KEY` | Optional | [urlhaus.abuse.ch](https://urlhaus.abuse.ch/api/) | Community rate-limited query + heuristic fallback. |
| **PhishTank Feed** | `PHISHTANK_APP_KEY` | Optional | [phishtank.org](https://phishtank.org/developer_info.php) | Marked as `not_configured`, non-blocking. |
| **PostgreSQL DB** | `DATABASE_URL` | Optional | Local / Neon / Supabase | Local SQLite (`cybershield.db`). |
| **Web3 Ethereum** | `BLOCKCHAIN_RPC_URL` | Optional | Alchemy Sepolia | Local RFC 8785 SHA-256 cryptographic verification. |

---

## 4. Frontend Production Build

The frontend is built using Vite and served directly by FastAPI:

```powershell
cd "D:\My Created Projects\CyberShield-AI\CyberShield-AI\frontend"
npm run build
```
Build output is generated into `frontend/dist/` and automatically mounted at `/` by `backend/main.py`.
