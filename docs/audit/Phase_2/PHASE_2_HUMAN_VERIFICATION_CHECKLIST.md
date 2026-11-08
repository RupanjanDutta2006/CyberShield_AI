# PHASE 2 AUDIT: HUMAN VERIFICATION & ACCEPTANCE CHECKLIST
**Project:** CyberShield AI  
**Scope:** Explicit Step-by-Step Manual Verification Procedures for the Project Owner  
**Auditor Role:** Senior QA Auditor & Verification Validator  
**Audit Target:** `D:\Adamas Hackathon\Integration_Member_1_3`  
**Date:** November 2026  
**Status:** READY FOR OWNER EXECUTION  

> [!IMPORTANT]
> In accordance with strict audit rules, **all checklist items below remain unchecked [ ]**.
> The project owner must execute each verification step personally and verify the expected console/UI outputs.

---

## 1. Quick Verification Matrix

| # | Check Item | Target URL / Command | Success Indicator |
| :-: | :--- | :--- | :--- |
| **1** | System Health | `GET /api/v1/health` | `status: "healthy"` |
| **2** | Swagger UI | `http://127.0.0.1:8000/docs` | Interactive API documentation renders |
| **3** | URL Investigation | `POST /api/v1/reports/investigate` | Returns `scan_id`, risk score, severity |
| **4** | Real EVM Node | `npx hardhat node` | 20 accounts initialized on `8545` |
| **5** | Contract Deploy | `npx hardhat run scripts/deploy.js` | Deployed at `0x5FbDB...` |
| **6** | Blockchain Register| `POST /api/v1/reports/register` | Returns `status: "confirmed"` & `tx_hash` |
| **7** | Duplicate Reject | `POST /api/v1/reports/register` (repeat) | HTTP 400 or Revert (`Report already registered`) |
| **8** | Report Verify | `POST /api/v1/reports/verify` | `is_valid: true`, `verified_valid` |
| **9** | Tamper Detection | `POST /api/v1/reports/verify` (altered hash)| `is_valid: false`, `verified_tampered` |

---

## 2. Detailed Step-by-Step Manual Procedures

### Step 1: Start the Backend Server
- **Exact Step:**
  1. Open a terminal in `D:\Adamas Hackathon\Integration_Member_1_3`.
  2. Double-click `CyberShield.bat` (or execute `start_server.cmd`).
- **Expected Output:**
  ```
  INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
  INFO:     Application startup complete.
  ```
- **Failure Indicator:** Terminal window closes immediately; `Address already in use` error.
- **Required Evidence:** Console log showing `Application startup complete`.
- [ ] **Owner Verification Check 1**

---

### Step 2: Verify API Health & Swagger Documentation
- **Exact Step:**
  1. Open web browser to `http://127.0.0.1:8000/api/v1/health`.
  2. Open web browser to `http://127.0.0.1:8000/docs`.
- **Expected Output:**
  - Health endpoint returns JSON:
    ```json
    {
      "status": "healthy",
      "service": "CyberShield AI API",
      "version": "1.0.0"
    }
    ```
  - Swagger UI renders interactive documentation with endpoints: `/health`, `/reports/investigate`, `/reports/register`, `/reports/verify`, `/reports/{report_id}`.
- **Failure Indicator:** HTTP 404 Not Found, 500 Internal Server Error, or blank white page.
- **Required Evidence:** Browser view of Swagger UI.
- [ ] **Owner Verification Check 2**

---

### Step 3: Perform URL Investigation (Member 1 Core Scan)
- **Exact Step:**
  Using Swagger UI (or curl / Postman):
  - Click on `POST /api/v1/reports/investigate` -> `Try it out`.
  - Enter Header: `X-API-Key: cybershield-auth-key-2026`
  - Enter Request Body:
    ```json
    {
      "url": "https://adamas-university.ac.in"
    }
    ```
  - Click `Execute`.
- **Expected Output:**
  - HTTP Status: `200 OK`
  - Response Body contains:
    - `"scan_id"`: (UUID format, e.g. `68008ef6-6cbe-4e86-8233-703c3920e978`)
    - `"status"`: `"completed"`
    - `"risk_score"`: Numerical score between 0 and 100
    - `"severity"`: One of `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `SAFE`
    - `"evidence"`: Technical findings for DNS, TLS, redirects, and heuristics.
- **Failure Indicator:** HTTP 401 Unauthorized (invalid key) or 500 error.
- **Required Evidence:** Save the generated `"scan_id"` for subsequent steps.
- [ ] **Owner Verification Check 3**

---

### Step 4: Start Local EVM Node & Deploy Contract (Member 3 Blockchain)
- **Exact Step:**
  1. Open a second terminal:
     ```cmd
     cd "D:\Adamas Hackathon\Integration_Member_1_3\blockchain"
     npx hardhat node
     ```
  2. In a third terminal:
     ```cmd
     cd "D:\Adamas Hackathon\Integration_Member_1_3\blockchain"
     npx hardhat run scripts/deploy.js --network localhost
     ```
- **Expected Output:**
  ```
  ═══════════════════════════════════════════
    ThreatReportRegistry deployed!
    Address: 0x5FbDB2315678afecb367f032d93F642f64180aa3
    Network: localhost
  ═══════════════════════════════════════════
  ```
- **Failure Indicator:** `ECONNREFUSED 127.0.0.1:8545`.
- **Required Evidence:** Console confirmation showing deployment address `0x5FbDB...`.
- [ ] **Owner Verification Check 4**

---

### Step 5: Register Threat Report on Blockchain
- **Exact Step:**
  In Swagger UI:
  - Click `POST /api/v1/reports/register` -> `Try it out`.
  - Header: `X-API-Key: cybershield-auth-key-2026`
  - Request Body:
    ```json
    {
      "report_id": "<PASTE_SCAN_ID_FROM_STEP_3>"
    }
    ```
  - Click `Execute`.
- **Expected Output:**
  - HTTP Status: `200 OK`
  - Response Body:
    ```json
    {
      "report_id": "<YOUR_SCAN_ID>",
      "report_hash": "0x...",
      "transaction_hash": "0x...",
      "blockchain_network": "Hardhat Local (EVM 31337)",
      "contract_address": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
      "status": "confirmed"
    }
    ```
- **Failure Indicator:** `"status": "simulated"` when live node is active, or HTTP 500.
- **Required Evidence:** JSON response showing `status: "confirmed"` with non-empty transaction hash.
- [ ] **Owner Verification Check 5**

---

### Step 6: Verify Duplicate Registration Protection
- **Exact Step:**
  Immediately click `Execute` again with the exact same request body from Step 5.
- **Expected Output:**
  - HTTP Status: `400 Bad Request` or `500` with detail containing:
    `Smart contract transaction reverted: ... 'Report already registered'`
- **Failure Indicator:** Transaction succeeds a second time with status 200, creating duplicate report.
- **Required Evidence:** Error message confirming rejection due to duplicate hash.
- [ ] **Owner Verification Check 6**

---

### Step 7: Verify Authentic Threat Report
- **Exact Step:**
  In Swagger UI:
  - Click `POST /api/v1/reports/verify` -> `Try it out`.
  - Request Body:
    ```json
    {
      "report_id": "<PASTE_SCAN_ID_FROM_STEP_3>"
    }
    ```
  - Click `Execute`.
- **Expected Output:**
  - HTTP Status: `200 OK`
  - Response Body:
    ```json
    {
      "report_id": "<YOUR_SCAN_ID>",
      "is_valid": true,
      "verification_status": "verified_valid",
      "tampered_fields": []
    }
    ```
- **Failure Indicator:** `"is_valid": false`.
- **Required Evidence:** Response showing `is_valid: true`.
- [ ] **Owner Verification Check 7**

---

### Step 8: Verify Tamper Detection
- **Exact Step:**
  In Swagger UI:
  - On `POST /api/v1/reports/verify`:
  - Request Body with a forged client hash:
    ```json
    {
      "report_id": "<PASTE_SCAN_ID_FROM_STEP_3>",
      "provided_hash": "0xdeadbeef111122223333444455556666777788889999aaaabbbbccccddddeeee"
    }
    ```
  - Click `Execute`.
- **Expected Output:**
  - HTTP Status: `200 OK`
  - Response Body:
    ```json
    {
      "report_id": "<YOUR_SCAN_ID>",
      "is_valid": false,
      "verification_status": "verified_tampered",
      "tampered_fields": ["report_hash"]
    }
    ```
- **Failure Indicator:** `"is_valid": true`.
- **Required Evidence:** Response confirming `is_valid: false` and status `verified_tampered`.
- [ ] **Owner Verification Check 8**

---

## 3. Human Verification Sign-Off

Upon completing the 8 checks above:
- **Verified By (Project Owner):** ___________________________
- **Date Verified:** ___________________________
- **Final Acceptance Decision:** `[ ] ACCEPTED / READY FOR MERGE`  `[ ] REJECTED`

