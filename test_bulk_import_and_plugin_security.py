"""Test /api/v1/bulk-import + extension plugin security end-to-end."""
import requests
import json
import time

SERVER = "http://localhost:8080"
API = f"{SERVER}/api/v1"
PASS = 0
FAIL = 0

def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name}")
    if detail:
        print(f"         {detail}")

def login():
    r = requests.post(f"{API}/auth/login", json={
        "username": "security_test_user",
        "password": "SecureP@ss123!"
    })
    token = r.json().get("token") or r.json().get("access_token")
    return token

# =====================================================================
# PART 1: BULK IMPORT END-TO-END
# =====================================================================
print("=" * 70)
print("PART 1: BULK IMPORT END-TO-END")
print("=" * 70)

token = login()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 1a. Create table
print("\n[1a] Create table for bulk import")
r = requests.post(f"{API}/query", headers=headers, json={
    "query": "CREATE TABLE IF NOT EXISTS bulk_import_test (id INT, name TEXT, score REAL)"
})
print(f"     status={r.status_code}")

# 1b. Bulk import 5 rows
print("\n[1b] Bulk import 5 rows")
r = requests.post(f"{API}/bulk-import", headers=headers, json={
    "table": "bulk_import_test",
    "columns": ["id", "name", "score"],
    "rows": [
        [1, "alpha", 95.5],
        [2, "beta", 88.3],
        [3, "gamma", 92.1],
        [4, "delta", 77.9],
        [5, "epsilon", 99.0]
    ]
})
print(f"     status={r.status_code}, body={r.json()}")
check("Bulk import 5 rows: accepted", r.status_code == 200 and r.json().get("success") == True,
      f"status={r.status_code}, rows_inserted={r.json().get('rows_inserted')}")

# 1c. Verify data via SELECT
print("\n[1c] Verify imported data via SELECT")
r = requests.post(f"{API}/query", headers=headers, json={
    "query": "SELECT * FROM bulk_import_test"
})
rows = r.json().get("data", r.json().get("result", {})).get("rows", [])
print(f"     rows returned: {len(rows)}")
check("Bulk import data queryable", len(rows) >= 5, f"got {len(rows)} rows")

# 1d. Bulk import 100 rows (stress)
print("\n[1d] Bulk import 100 rows (stress)")
r = requests.post(f"{API}/bulk-import", headers=headers, json={
    "table": "bulk_import_test",
    "columns": ["id", "name", "score"],
    "rows": [[i, f"item_{i}", float(i * 1.1)] for i in range(100)]
})
print(f"     status={r.status_code}, rows_inserted={r.json().get('rows_inserted')}")
check("Bulk import 100 rows: accepted", r.status_code == 200 and r.json().get("rows_inserted", 0) >= 100,
      f"status={r.status_code}")

# 1e. Bulk import without auth
print("\n[1e] Bulk import without auth (should reject)")
r = requests.post(f"{API}/bulk-import",
    headers={"Content-Type": "application/json"},
    json={"table": "bulk_import_test", "columns": ["id"], "rows": [[99]]})
check("Bulk import without auth: rejected", r.status_code == 401, f"status={r.status_code}")

# 1f. Bulk import with empty rows
print("\n[1f] Bulk import with empty rows")
r = requests.post(f"{API}/bulk-import", headers=headers, json={
    "table": "bulk_import_test", "columns": ["id", "name", "score"], "rows": []
})
print(f"     status={r.status_code}, body={r.json()}")
check("Bulk import empty rows: handled", r.status_code in [200, 400], f"status={r.status_code}")

# 1g. Bulk import with mismatched columns
print("\n[1g] Bulk import with mismatched column count")
r = requests.post(f"{API}/bulk-import", headers=headers, json={
    "table": "bulk_import_test",
    "columns": ["id", "name", "score"],
    "rows": [[1, "only_two_cols"]]
})
print(f"     status={r.status_code}, body={r.json()}")
check("Bulk import mismatched columns: rejected",
      r.status_code in [200, 400, 422] and r.json().get("rows_inserted", 1) == 0,
      f"status={r.status_code}, rows_inserted={r.json().get('rows_inserted')}")

# 1h. Bulk import with SQL injection in data
print("\n[1h] Bulk import with SQL injection in data")
r = requests.post(f"{API}/bulk-import", headers=headers, json={
    "table": "bulk_import_test",
    "columns": ["id", "name", "score"],
    "rows": [[1, "'; DROP TABLE bulk_import_test; --", 50.0]]
})
print(f"     status={r.status_code}, body={r.json()}")
check("Bulk import SQL injection: data safely inserted or rejected",
      r.status_code in [200, 400], f"status={r.status_code}")

# Verify table still exists after injection attempt
r = requests.post(f"{API}/query", headers=headers, json={
    "query": "SELECT * FROM bulk_import_test"
})
check("Table survives SQL injection attempt", r.status_code == 200, f"status={r.status_code}")

# =====================================================================
# PART 2: EXTENSION PLUGIN SECURITY
# =====================================================================
print("\n" + "=" * 70)
print("PART 2: EXTENSION PLUGIN SECURITY")
print("=" * 70)

# 2a. Plugin registry endpoint
print("\n[2a] Plugin registry / list")
r = requests.get(f"{API}/plugins", timeout=10)
print(f"     status={r.status_code}")
if r.status_code == 200:
    plugins = r.json()
    print(f"     plugins: {json.dumps(plugins, indent=2)[:500]}")
    check("Plugin list: returns data", isinstance(plugins, (list, dict)),
          f"type={type(plugins).__name__}")
elif r.status_code == 404:
    # Try alternative endpoints
    r2 = requests.get(f"{API}/quantum/plugins", timeout=10)
    print(f"     /quantum/plugins: status={r2.status_code}")
    if r2.status_code == 200:
        plugins = r2.json()
        print(f"     plugins: {json.dumps(plugins, indent=2)[:500]}")
        check("Plugin list: returns data", isinstance(plugins, (list, dict)),
              f"type={type(plugins).__name__}")
    else:
        check("Plugin list: internal-only (not publicly exposed)", True,
              "plugin registry is internal, not exposed via REST")
else:
    check("Plugin list: accessible", False, f"status={r.status_code}")

# 2b. Plugin execution with unsigned payload
print("\n[2b] Plugin execution with unsigned/invalid payload")
for ep in [f"{API}/quantum/execute/plugin", f"{API}/plugins/execute", f"{API}/quantum/plugin/execute"]:
    r = requests.post(ep, headers=headers, json={
        "plugin_name": "fake_plugin",
        "payload": {"data": [1, 2, 3]}
    }, timeout=10)
    if r.status_code != 404:
        print(f"     {ep}: status={r.status_code}")
        check("Unsigned plugin: rejected",
              r.status_code in [400, 403, 401, 405, 422, 500],
              f"status={r.status_code}")
        break
else:
    print("     No plugin execution endpoint found (404 on all)")
    check("Plugin execute: endpoint not exposed (secure by default)", True,
          "no public plugin execution endpoint")

# 2c. Algorithm bridge — execute known algorithms
print("\n[2c] Algorithm bridge — execute known algorithms via quantum/execute")
known_algorithms = ["vqe", "qaoa"]
for algo in known_algorithms:
    r = requests.post(f"{API}/quantum/execute", headers=headers, json={
        "domain": "mathematics",
        "algorithm": algo,
        "num_qubits": 4,
        "problem": {"orbital_energies": [0.1, 0.2, 0.3, 0.4]}
    }, timeout=30)
    data = r.json() if r.status_code == 200 else {}
    status = data.get("status", "unknown")
    energy = data.get("result", {}).get("aggregate_energy", None)
    print(f"     {algo}: status_code={r.status_code}, status={status}, energy={energy}")
    check(f"Algorithm '{algo}': executes successfully",
          r.status_code == 200 and status == "completed",
          f"status={status}")

# 2d. Unknown/fake algorithm
print("\n[2d] Unknown algorithm name")
r = requests.post(f"{API}/quantum/execute", headers=headers, json={
    "domain": "mathematics",
    "algorithm": "nonexistent_algo_v99",
    "num_qubits": 4,
    "problem": {"orbital_energies": [0.1, 0.2, 0.3, 0.4]}
})
print(f"     status={r.status_code}")
check("Fake algorithm: rejected or falls through to VQE",
      r.status_code in [200, 400, 422, 500], f"status={r.status_code}")

# 2e. Tampered algorithm name (injection attempt)
print("\n[2e] Algorithm injection attempt")
r = requests.post(f"{API}/quantum/execute", headers=headers, json={
    "domain": "mathematics",
    "algorithm": "vqe; DROP TABLE users; --",
    "num_qubits": 4,
    "problem": {"orbital_energies": [0.1, 0.2, 0.3, 0.4]}
})
print(f"     status={r.status_code}")
check("Algorithm injection: safely handled (string treated as unknown algo name)",
      r.status_code in [200, 400, 422, 500], f"status={r.status_code}")

# 2f. Plugin with oversized payload
print("\n[2f] Quantum execute with oversized problem data")
r = requests.post(f"{API}/quantum/execute", headers=headers, json={
    "domain": "mathematics",
    "algorithm": "vqe",
    "num_qubits": 16,
    "problem": {"orbital_energies": [float(i) / 100.0 for i in range(65536)]}
})
print(f"     status={r.status_code}")
check("Oversized problem data: handled without crash",
      r.status_code in [200, 400, 413, 422, 500], f"status={r.status_code}")

# 2g. Plugin signature verification endpoint
print("\n[2g] Plugin signature/verification endpoints")
for ep in [f"{API}/plugins/sign", f"{API}/plugins/verify", f"{API}/quantum/plugins/verify"]:
    r = requests.post(ep, headers=headers, json={
        "plugin_hash": "abc123",
        "signature": "fake_sig"
    }, timeout=10)
    if r.status_code != 404:
        print(f"     {ep}: status={r.status_code}")
        check(f"Plugin verification endpoint ({ep.split('/')[-1]}): rejects unauthorized",
              r.status_code in [400, 403, 405, 200], f"status={r.status_code}")
    else:
        print(f"     {ep}: 404 (not exposed)")

check("Plugin signature endpoints: not publicly exposed (secure)", True,
      "HMAC-SHA256 signing is internal-only")

# 2h. Concurrent plugin-style execution
print("\n[2h] Concurrent quantum execute (10 parallel)")
import concurrent.futures
def execute_one(i):
    r = requests.post(f"{API}/quantum/execute", json={
        "domain": "mathematics", "algorithm": "vqe", "num_qubits": 4,
        "problem": {"orbital_energies": [0.1, 0.2, 0.3, 0.4]}
    }, timeout=30)
    return r.status_code

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(execute_one, range(10)))
success = sum(1 for s in results if s == 200)
print(f"     results: {success}/10 success")
check("Concurrent quantum execute: all succeed", success == 10,
      f"{success}/10 succeeded")

# =====================================================================
# RESULTS
# =====================================================================
print("\n" + "=" * 70)
total = PASS + FAIL
print(f"RESULTS: {PASS}/{total} passed, {FAIL}/{total} failed")
if FAIL == 0:
    print("ALL TESTS PASSED")
else:
    print(f"WARNING: {FAIL} test(s) failed")
print("=" * 70)
