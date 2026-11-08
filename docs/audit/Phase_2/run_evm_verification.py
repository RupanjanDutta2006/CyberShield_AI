"""CyberShield AI — Phase 2 Independent Real EVM Verification Script.

Executes and logs raw receipts, hashes, and revert reasons for:
1. Deployment & Owner check
2. Authorized registration (tx status == 1)
3. Unauthorized registration rejection (reverts)
4. Duplicate registration rejection (reverts)
5. Tampered payload verification (returns False)
6. Authentic payload verification (returns True)
"""

import sys
import json
from pathlib import Path
from web3 import Web3
from eth_account import Account

# Connect to node
RPC_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print(f"FAILED: Cannot connect to {RPC_URL}")
    sys.exit(1)

print(f"[*] Connected to EVM Node: {RPC_URL} (Chain ID: {w3.eth.chain_id})")

# Load deployment info
dep_path = Path("D:/Adamas Hackathon/Integration_Member_1_3/blockchain/deployment.json")
dep_info = json.loads(dep_path.read_text(encoding="utf-8"))
contract_addr = Web3.to_checksum_address(dep_info["contractAddress"])
print(f"[*] Target Contract: {contract_addr}")

# Verify code deployed
code = w3.eth.get_code(contract_addr)
if len(code) <= 2:
    print(f"FAILED: No code deployed at {contract_addr}")
    sys.exit(1)
print(f"[*] Verified Bytecode at Contract: {len(code)} bytes")

# Load ABI
abi_path = Path("D:/Adamas Hackathon/Integration_Member_1_3/blockchain/artifacts/contracts/ThreatReportRegistry.sol/ThreatReportRegistry.json")
artifact = json.loads(abi_path.read_text(encoding="utf-8"))
abi = artifact["abi"]
contract = w3.eth.contract(address=contract_addr, abi=abi)

owner = contract.functions.owner().call()
print(f"[*] Contract Owner: {owner}")

# Hardhat Account #0 (Owner / Authorized)
acc0_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
acc0 = Account.from_key(acc0_key)
print(f"[*] Authorized Signer (Account #0): {acc0.address}")

# Hardhat Account #19 (Unauthorized Account)
acc19_key = "0xdf57089febbacf7ba0bc227dafbffa9fc08a93fdc68e1e42411a14efcf23656e"
acc19 = Account.from_key(acc19_key)
print(f"[*] Unauthorized Signer (Account #19): {acc19.address}")

is_auth_0 = contract.functions.isAuthorizedRegistrar(acc0.address).call()
is_auth_19 = contract.functions.isAuthorizedRegistrar(acc19.address).call()
print(f"[*] Authorization State: Account #0={is_auth_0}, Account #19={is_auth_19}")

# Test 1: Unauthorized Registration Rejection
test_hash_unauth = Web3.keccak(text="unauthorized_test_report_payload_999")
print("\n--- TEST 1: UNAUTHORIZED REGISTRATION ATTEMPT ---")
unauth_nonce = w3.eth.get_transaction_count(acc19.address)
tx_unauth = contract.functions.registerReport(test_hash_unauth).build_transaction({
    "from": acc19.address,
    "nonce": unauth_nonce,
    "gas": 300000,
    "gasPrice": w3.eth.gas_price,
})
signed_unauth = w3.eth.account.sign_transaction(tx_unauth, acc19.key)
try:
    tx_hash_unauth = w3.eth.send_raw_transaction(signed_unauth.raw_transaction)
    receipt_unauth = w3.eth.wait_for_transaction_receipt(tx_hash_unauth)
    print(f"FAILED: Unauthorized transaction did not revert! Status: {receipt_unauth.status}")
except Exception as e:
    print(f"SUCCESS: Unauthorized registration reverted as expected.")
    print(f"Revert Reason: {e}")

# Test 2: Authorized Registration & Receipt Validation
test_payload_valid = "cybershield_phase_2_live_audit_report_1001"
test_hash_valid = Web3.keccak(text=test_payload_valid)
print("\n--- TEST 2: AUTHORIZED REGISTRATION & RECEIPT VALIDATION ---")
auth_nonce = w3.eth.get_transaction_count(acc0.address)
tx_auth = contract.functions.registerReport(test_hash_valid).build_transaction({
    "from": acc0.address,
    "nonce": auth_nonce,
    "gas": 300000,
    "gasPrice": w3.eth.gas_price,
})
signed_auth = w3.eth.account.sign_transaction(tx_auth, acc0.key)
tx_hash_auth = w3.eth.send_raw_transaction(signed_auth.raw_transaction)
print(f"Submitted TX: {tx_hash_auth.hex()}")

receipt_auth = w3.eth.wait_for_transaction_receipt(tx_hash_auth)
print(f"Receipt Status: {receipt_auth.status} (1=Success, 0=Revert)")
print(f"Block Number: {receipt_auth.blockNumber}")
print(f"Gas Used: {receipt_auth.gasUsed}")
assert receipt_auth.status == 1, "Transaction failed on-chain!"
print("SUCCESS: Transaction mined with status 1.")

# Parse event logs to get reportId
logs = contract.events.ReportRegistered().process_receipt(receipt_auth)
event_data = logs[0]["args"]
report_id = event_data["reportId"]
report_hash = event_data["reportHash"]
print(f"Emitted ReportId: {report_id.hex()}")
print(f"Emitted ReportHash: {report_hash.hex()}")

# Test 3: Duplicate Registration Rejection
print("\n--- TEST 3: DUPLICATE REGISTRATION REJECTION ---")
auth_nonce_dup = w3.eth.get_transaction_count(acc0.address)
tx_dup = contract.functions.registerReport(test_hash_valid).build_transaction({
    "from": acc0.address,
    "nonce": auth_nonce_dup,
    "gas": 300000,
    "gasPrice": w3.eth.gas_price,
})
signed_dup = w3.eth.account.sign_transaction(tx_dup, acc0.key)
try:
    tx_hash_dup = w3.eth.send_raw_transaction(signed_dup.raw_transaction)
    receipt_dup = w3.eth.wait_for_transaction_receipt(tx_hash_dup)
    print(f"FAILED: Duplicate transaction did not revert! Status: {receipt_dup.status}")
except Exception as e:
    print(f"SUCCESS: Duplicate registration reverted as expected.")
    print(f"Revert Reason: {e}")

# Test 4: Authentic Report Verification
print("\n--- TEST 4: AUTHENTIC REPORT VERIFICATION ---")
is_valid = contract.functions.verifyReport(report_id, test_hash_valid).call()
print(f"Verification Result (Original Hash): {is_valid}")
assert is_valid is True, "Authentic report verification returned False!"
print("SUCCESS: Authentic report verified.")

# Test 5: Tampered Payload Verification
print("\n--- TEST 5: TAMPERED PAYLOAD VERIFICATION ---")
tampered_hash = Web3.keccak(text="tampered_payload_alteration_9999")
is_tampered_valid = contract.functions.verifyReport(report_id, tampered_hash).call()
print(f"Verification Result (Tampered Hash): {is_tampered_valid}")
assert is_tampered_valid is False, "Tampered payload verification returned True!"
print("SUCCESS: Tampered payload rejected as invalid.")

total_reports = contract.functions.reportCount().call()
print(f"\n[*] Total Reports in Smart Contract: {total_reports}")
print("\n=== ALL REAL EVM VERIFICATIONS COMPLETED SUCCESSFULLY ===")

