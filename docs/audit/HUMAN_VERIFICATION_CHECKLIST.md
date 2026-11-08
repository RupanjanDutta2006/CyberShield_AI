# HUMAN VERIFICATION AND ACCEPTANCE CHECKLIST
**Project:** CyberShield AI  
**Scope:** Manual Verification Procedures for Project Owner & Lead Evaluator  
**Auditor Role:** Independent Senior QA Auditor  
**Date:** November 2026  
**Status:** READY FOR OWNER EXECUTION  

> [!IMPORTANT]
> In accordance with independent audit guidelines, **all checklist items below remain unchecked [ ]**.
> The project owner must execute each verification step personally on their local workstation.

---

## 1. Pre-Execution Environment Verification

- [ ] **Step 1.1: Verify Python Environment**
  - Open terminal and run: `python --version`
  - Expected: Python 3.10+ (Verified on Python 3.11.9).
- [ ] **Step 1.2: Verify Node.js Environment**
  - Run: `node --version`
  - Expected: Node.js v18+ (Verified on Node.js v24.16.0).
- [ ] **Step 1.3: Verify Original Code Repositories Untouched**
  - Verify that `D:\Adamas Hackathon\Project` and `D:\Adamas Hackathon\CyberShield-Blockchain` remain clean and unmodified.

---

## 2. One-Click Interactive Launcher Verification

- [ ] **Step 2.1: Launch via `CyberShield.bat`**
  - Navigate to `D:\Adamas Hackathon\Integration_Member_1_3`.
  - Double-click `CyberShield.bat`.
  - Verify that the launcher window opens with ASCII banner, environment validation, and interactive mode selector.
- [ ] **Step 2.2: Verify Browser Auto-Launch**
  - Confirm that the default web browser automatically opens to `http://127.0.0.1:8000/docs`.

---

## 3. Smart Contract & Hardhat EVM Verification

- [ ] **Step 3.1: Run Smart Contract Unit Tests**
  - In a terminal, run:
    ```cmd
    cd "D:\Adamas Hackathon\Integration_Member_1_3\blockchain"
    npx hardhat test
    ```
  - Verify: **29 passing (672ms)** with 0 failures.
- [ ] **Step 3.2: Verify Cross-Language Hash Consistency**
  - Confirm that the first 7 tests in `hashConsistency.test.js` pass, proving bit-level hash parity between TypeScript and Python.

---

## 4. Live Blockchain EVM Integration Verification

- [ ] **Step 4.1: Start Local Hardhat EVM Node**
  - In a separate terminal or via `start_blockchain.cmd`, run:
    ```cmd
    cd "D:\Adamas Hackathon\Integration_Member_1_3\blockchain"
    npx hardhat node
    ```
  - Verify node is listening on `http://127.0.0.1:8545` with 20 pre-funded test accounts.
- [ ] **Step 4.2: Deploy Smart Contract to Local Node**
  - In another terminal:
    ```cmd
    cd "D:\Adamas Hackathon\Integration_Member_1_3\blockchain"
    npx hardhat run scripts/deploy.js --network localhost
    ```
  - Verify deployment output:
    `ThreatReportRegistry deployed! Address: 0x5FbDB2315678afecb367f032d93F642f64180aa3`
- [ ] **Step 4.3: Execute Live EVM Check**
  - Run:
    ```cmd
    cd "D:\Adamas Hackathon\Integration_Member_1_3\backend"
    python -m tests.verify_live_evm
    ```
  - Verify that all 4 checks pass:
    - [ ] 1. Registration: SUCCESS (returns real tx hash, block number, gas used)
    - [ ] 2. Verification: True
    - [ ] 3. Duplicate rejection: SUCCESS (reverts with 'Report already registered')
    - [ ] 4. Tamper detection: verified=False

---

## 5. REST API Workflow Verification (via Swagger UI / Postman)

- [ ] **Step 5.1: Health Endpoint Check**
  - Open `http://127.0.0.1:8000/api/v1/health` in browser.
  - Verify response: `{"status": "healthy", "service": "CyberShield AI API", ...}`.
- [ ] **Step 5.2: URL Investigation (`POST /api/v1/reports/investigate`)**
  - Set Header: `X-API-Key: cybershield-auth-key-2026`
  - Send Payload:
    ```json
    { "url": "https://example.com" }
    ```
  - Verify response contains: `scan_id`, `risk_score`, `severity`, `status: "completed"`.
- [ ] **Step 5.3: Blockchain Registration (`POST /api/v1/reports/register`)**
  - Send Payload with `scan_id` from step 5.2.
  - Verify response contains: `report_id`, `status: "confirmed"` (or `"simulated"`), `tx_hash`.
- [ ] **Step 5.4: Integrity Verification (`POST /api/v1/reports/verify`)**
  - Send Payload:
    ```json
    { "report_id": "<scan_id_from_above>" }
    ```
  - Verify response: `{"is_valid": true, "verification_status": "verified_valid"}`.
- [ ] **Step 5.5: Tamper Verification Test**
  - Send Payload with altered `provided_hash`:
    ```json
    {
      "report_id": "<scan_id_from_above>",
      "provided_hash": "0x0000000000000000000000000000000000000000000000000000000000000000"
    }
    ```
  - Verify response: `{"is_valid": false, "verification_status": "verified_tampered"}`.

---

## 6. Audit Findings & Hardening Review

- [ ] **Step 6.1: Review Finding AUDIT-FINDING-01**
  - Review proposed fix in `POST_MERGE_FINDINGS.md` for adding RPC connectivity check and unit test isolation fixture.
  - Decide whether to authorize applying this hardening change.
- [ ] **Step 6.2: Final Owner Sign-off**
  - Sign off on production readiness for Member 2 & Member 4 integration.

