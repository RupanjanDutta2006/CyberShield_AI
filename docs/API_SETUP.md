# CyberShield AI — External API & Credential Configuration Guide

This guide provides step-by-step instructions for configuring all external APIs, databases, AI services, and blockchain verification networks supported by **CyberShield AI**.

---

## 1. Quick Summary Table

| Service / Provider | Purpose | Environment Variable | Cost / Tier | Registration URL |
| :--- | :--- | :--- | :--- | :--- |
| **URLhaus (abuse.ch)** | Malicious URL and payload intelligence | `URLHAUS_AUTH_KEY` | 100% Free (Community) | [URLhaus API Portal](https://urlhaus.abuse.ch/api/) |
| **PhishTank (Cisco Talos)** | Phishing URL database and verification | `PHISHTANK_APP_KEY` | Free registration | [PhishTank Developer Info](https://phishtank.org/developer_info.php) |
| **Google Gemini API** | Deep semantic phishing message analysis | `AI_API_KEY` | Free tier available | [Google AI Studio](https://aistudio.google.com/) |
| **PostgreSQL Database** | Persistent relational storage for scans & reports | `DATABASE_URL` | Free (Self-hosted or Neon/Supabase) | [PostgreSQL Official](https://www.postgresql.org/) |
| **Web3 / Blockchain RPC** | On-chain report integrity anchor (Optional) | `BLOCKCHAIN_RPC_URL` | Free public testnet RPC (Sepolia) | [Infura](https://www.infura.io/) / [Alchemy](https://www.alchemy.com/) |

---

## 2. Graceful Fallback Architecture

CyberShield AI is built with a **resilient zero-crash design**:
- **Missing API Keys**: If any external API key is missing or invalid, CyberShield AI does **not** crash or fail.
- **Provider Status**: The provider is flagged as `not_configured` in the UI and in backend response schemas.
- **Local Fallback**: 
  - For messages, a high-precision **Local Deterministic Heuristic Engine** executes immediately, analyzing urgency, financial pressure, sensitive keyword harvesting, and suspicious link syntax.
  - For URLs, built-in heuristic pattern checkers (e.g. suspicious TLDs, IP literal targets, punycode/IDN attacks, homoglyphs) operate locally.
  - For database storage, if PostgreSQL is unreachable or unconfigured, CyberShield automatically falls back to an embedded SQLite database (`cybershield.db`).
  - For report integrity, a cryptographic SHA-256 canonical hashing engine guarantees verifiable tamper-evidence locally without requiring blockchain fees.

---

## 3. Step-by-Step Provider Setup

### A. URLhaus API (abuse.ch)
- **Feature**: URL reputation and malware distribution tracking.
- **Cost**: Free.
- **Steps to obtain**:
  1. Visit [abuse.ch Authentication Portal](https://auth.abuse.ch/).
  2. Create an account or sign in via GitHub/GitLab/Twitter.
  3. Navigate to **My Account** -> **API Key**.
  4. Copy your API auth key.
  5. Add to your `.env` file:
     ```env
     URLHAUS_AUTH_KEY=your_urlhaus_api_key_here
     ```

### B. PhishTank API (Cisco Talos)
- **Feature**: Real-time phishing URL verification and community vote checks.
- **Cost**: Free.
- **Steps to obtain**:
  1. Go to [PhishTank Register](https://phishtank.org/register.php) and create an account.
  2. Once signed in, go to [PhishTank Developer Info](https://phishtank.org/developer_info.php).
  3. Click **Register an Application**.
  4. Copy your Application Key.
  5. Add to your `.env` file:
     ```env
     PHISHTANK_APP_KEY=your_phishtank_app_key_here
     ```

### C. Google Gemini AI API
- **Feature**: In-depth linguistic and intent analysis for phishing emails, SMS, and executive impersonation.
- **Cost**: Generous free tier (up to 15 requests/min with no billing required).
- **Steps to obtain**:
  1. Visit [Google AI Studio](https://aistudio.google.com/).
  2. Sign in with your Google account.
  3. Click **Get API key** and create a key in a new or existing Google Cloud project.
  4. Copy the key.
  5. Add to your `.env` file:
     ```env
     AI_API_KEY=your_gemini_api_key_here
     AI_PROVIDER=gemini
     ```

### D. PostgreSQL Database
- **Feature**: High-concurrency relational data storage for scans, threat intelligence events, and cryptographic risk reports.
- **Cost**: Free open-source or free cloud tiers (e.g., Neon.tech, Supabase).
- **Format**:
  ```env
  DATABASE_URL=postgresql://postgres:password@localhost:5432/cybershield
  ```
- *Note: If this variable is omitted or left as `sqlite:///./cybershield.db`, SQLite is automatically used.*

### E. Optional Blockchain Verification (Ethereum / Polygon / Sepolia)
- **Feature**: Immutably committing SHA-256 canonical report hashes onto an EVM blockchain for multi-party decentralized verification.
- **Cost**: Free on Sepolia Testnet (via Sepolia test faucets).
- **Setup**:
  1. Get a free RPC URL from [Alchemy](https://www.alchemy.com/) or public Sepolia RPC (`https://rpc.sepolia.org`).
  2. Add your wallet private key (with testnet ETH) and target contract:
     ```env
     BLOCKCHAIN_RPC_URL=https://rpc.sepolia.org
     BLOCKCHAIN_PRIVATE_KEY=your_testnet_private_key
     BLOCKCHAIN_CONTRACT_ADDRESS=0xYourContractAddress
     ```
  3. When credentials are not provided, the system operates in **Local SHA-256 Verification Mode** with instant tamper-detection.

---

## 4. Where to Place Credentials
Create a `.env` file in the root of the project:
```bash
cp .env.example .env
```
Open `.env` and fill in the values. **Never commit `.env` to version control.**
