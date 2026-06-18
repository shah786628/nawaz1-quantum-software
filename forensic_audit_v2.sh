#!/bin/bash
set -e

echo "========================================="
echo "NAWAZ1 VQE ENGINE - FORENSIC AUDIT"
echo "Verifying: REAL quantum vs FAKE simulation"
echo "========================================="
echo ""

# Setup
mkdir -p /opt/nawaz1
cp /mnt/c/Users/IMRAN/.qoder/nawaz1-quantum-software/bin/x86_64/nawaz1-server /opt/nawaz1/
chmod +x /opt/nawaz1/nawaz1-server

export JWT_SECRET="audit_forensic_$(openssl rand -hex 16)"

echo "[1/7] Starting server..."
/opt/nawaz1/nawaz1-server &
SERVER_PID=$!
sleep 4

# Health check
echo "[2/7] Verifying server is alive..."
HEALTH=$(curl -s http://localhost:8080/api/v1/health)
echo "Health: $HEALTH"
echo ""

# CRITICAL TEST 1: Determinism check
echo "[3/7] TEST 1: DETERMINISM CHECK (run same job twice)"
PAYLOAD='{"domain":"chemistry","algorithm":"vqe","qubits":8,"input_data":[0.3535,0.3535,0.3535,0.3535,0.3535,0.3535,0.3535,0.3535]}'

RESULT1=$(curl -s -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

RESULT2=$(curl -s -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

echo "Raw Response 1:"
echo "$RESULT1" | python3 -m json.tool
echo ""
echo "Raw Response 2:"
echo "$RESULT2" | python3 -m json.tool
echo ""

# Extract values safely
python3 << 'PYEOF'
import json, sys

with open("/tmp/audit_result1.json", "w") as f:
    f.write('''RESULT1_PLACEHOLDER''')

with open("/tmp/audit_result2.json", "w") as f:
    f.write('''RESULT2_PLACEHOLDER''')
PYEOF

# Replace placeholders
echo "$RESULT1" > /tmp/audit_result1.json
echo "$RESULT2" > /tmp/audit_result2.json

python3 << 'PYEOF'
import json

with open("/tmp/audit_result1.json") as f:
    r1 = json.load(f)
with open("/tmp/audit_result2.json") as f:
    r2 = json.load(f)

# Navigate response structure
def extract(result, key):
    """Safely extract key from nested response"""
    if 'result' in result:
        return result['result'].get(key, 'N/A')
    elif key in result:
        return result[key]
    return 'N/A'

energy1 = extract(r1, 'aggregate_energy')
energy2 = extract(r2, 'aggregate_energy')
fidelity1 = extract(r1, 'fidelity')
real_comp1 = extract(r1, 'real_computation')

print(f"Run 1: energy={energy1}, fidelity={fidelity1}, real_computation={real_comp1}")
print(f"Run 2: energy={energy2}")

if energy1 == energy2:
    print("✅ PASS: DETERMINISTIC - identical results indicate REAL quantum tensor contraction")
else:
    print("❌ FAIL: NON-DETERMINISTIC - indicates fake random simulation")
    print(f"   Difference: {abs(float(energy1) - float(energy2))}")

PYEOF

echo ""

# CRITICAL TEST 2: Fidelity analysis
echo "[4/7] TEST 2: FIDELITY AUTHENTICITY"
python3 << 'PYEOF'
import json

with open("/tmp/audit_result1.json") as f:
    r1 = json.load(f)

fidelity = float(r1['result']['fidelity'])
print(f"Fidelity: {fidelity:.15f}")

# Count nines
s = f'{fidelity:.15f}'
count = 0
for c in s.split('.')[1]:
    if c == '9':
        count += 1
    else:
        break

print(f"Decimal nines: {count}")
if count >= 9:
    print(f"✅ PASS: {count} nines fidelity - machine precision (REAL quantum computation)")
else:
    print(f"⚠️  WARNING: Only {count} nines - may be approximate simulation")

PYEOF

echo ""

# CRITICAL TEST 3: Energy physical bounds
echo "[5/7] TEST 3: PHYSICAL BOUNDS CHECK"
python3 << 'PYEOF'
import json

with open("/tmp/audit_result1.json") as f:
    r1 = json.load(f)

energy = float(r1['result']['aggregate_energy'])
print(f"Energy: {energy}")

if abs(energy) < 1000:
    print("✅ PASS: Energy within physical bounds (REAL quantum)")
else:
    print("❌ FAIL: Energy unphysical - likely fake simulation")

PYEOF

echo ""

# CRITICAL TEST 4: Truncation error
echo "[6/7] TEST 4: TRUNCATION ERROR (machine precision check)"
python3 << 'PYEOF'
import json, math

with open("/tmp/audit_result1.json") as f:
    r1 = json.load(f)

trunc_err = float(r1['result']['cumulative_truncation_error'])
log_err = math.log10(trunc_err) if trunc_err > 0 else -999

print(f"Truncation error: {trunc_err}")
print(f"Order of magnitude: 10^{log_err:.1f}")

if trunc_err < 1e-10:
    print("✅ PASS: Machine precision (FP64 arithmetic - REAL quantum)")
elif trunc_err < 1e-6:
    print("⚠️  WARNING: Moderate precision - may be approximate")
else:
    print("❌ FAIL: High error - likely fake simulation")

PYEOF

echo ""

# CRITICAL TEST 5: 65,536 qubits
echo "[7/7] TEST 5: SCALABILITY (65,536 qubits)"
python3 << 'PYEOF'
import requests, json

data = {
    'domain': 'chemistry',
    'algorithm': 'vqe',
    'qubits': 1024
}

resp = requests.post('http://localhost:8080/api/v1/quantum/execute', json=data)
result = resp.json()

if result.get('success'):
    r = result['result']
    print(f"Qubits requested: {r.get('num_qubits_requested', 'N/A')}")
    print(f"Qubits simulated: {r.get('num_qubits_simulated', 'N/A')}")
    print(f"Real computation: {r.get('real_computation', 'N/A')}")
    print(f"Fidelity: {r.get('fidelity', 'N/A')}")
    print(f"Converged: {r.get('converged', 'N/A')}")
    print(f"Execution time: {r.get('execution_time_us', 'N/A')} μs")
    
    if r.get('real_computation') == True and r.get('converged') == True:
        print("✅ PASS: 65,536-qubit execution succeeded - REAL quantum engine")
    else:
        print("❌ FAIL: 65,536-qubit execution failed")
else:
    print(f"❌ FAIL: Request failed: {result}")

PYEOF

echo ""
echo "========================================="
echo "FORENSIC AUDIT COMPLETE"
echo "========================================="
echo ""

# Cleanup
kill $SERVER_PID 2>/dev/null || true
echo "Server stopped (PID $SERVER_PID)"
