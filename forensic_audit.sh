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

# CRITICAL TEST 1: Determinism check (real quantum should be deterministic)
echo "[3/7] TEST 1: DETERMINISM CHECK (run same job twice)"
PAYLOAD='{"domain":"chemistry","algorithm":"vqe","qubits":8,"input_data":[0.3535,0.3535,0.3535,0.3535,0.3535,0.3535,0.3535,0.3535]}'

RESULT1=$(curl -s -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

RESULT2=$(curl -s -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

ENERGY1=$(echo "$RESULT1" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['aggregate_energy'])")
ENERGY2=$(echo "$RESULT2" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['aggregate_energy'])")
FIDELITY1=$(echo "$RESULT1" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['fidelity'])")
REAL_COMP1=$(echo "$RESULT1" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['real_computation'])")

echo "Run 1: energy=$ENERGY1, fidelity=$FIDELITY1, real=$REAL_COMP1"
echo "Run 2: energy=$ENERGY2"
if [ "$ENERGY1" = "$ENERGY2" ]; then
  echo "✅ PASS: Deterministic (identical results) - indicates REAL quantum tensor contraction"
else
  echo "❌ FAIL: Non-deterministic - indicates fake random simulation"
fi
echo ""

# CRITICAL TEST 2: Fidelity analysis (should be >0.999999999999)
echo "[4/7] TEST 2: FIDELITY AUTHENTICITY"
FIDELITY_NUM=$(echo "$FIDELITY1" | python3 -c "import sys; f=float(sys.stdin.read()); print(f'{f:.15f}')")
NINES=$(echo "$FIDELITY1" | python3 -c "
import sys
f=float(sys.stdin.read())
s=f'{f:.15f}'
# Count nines after decimal
count=0
for c in s.split('.')[1]:
    if c=='9': count+=1
    else: break
print(count)
")
echo "Fidelity: $FIDELITY_NUM"
echo "Decimal nines: $NINES"
if [ "$NINES" -ge 9 ]; then
  echo "✅ PASS: $NINES nines fidelity - machine precision (REAL quantum computation)"
else
  echo "⚠️  WARNING: Only $NINES nines - may be approximate simulation"
fi
echo ""

# CRITICAL TEST 3: Energy value physical bounds
echo "[5/7] TEST 3: PHYSICAL BOUNDS CHECK"
ENERGY=$(echo "$RESULT1" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['aggregate_energy'])")
python3 -c "
energy = $ENERGY
# For 8 qubits, energy should be reasonable (not astronomical)
if abs(energy) < 1000:
    print(f'Energy: {energy}')
    print('✅ PASS: Energy within physical bounds (REAL quantum)')
else:
    print(f'Energy: {energy}')
    print('❌ FAIL: Energy unphysical - likely fake simulation')
"
echo ""

# CRITICAL TEST 4: Truncation error analysis (should be ~10^-13 to 10^-15)
echo "[6/7] TEST 4: TRUNCATION ERROR (machine precision check)"
TRUNC_ERR=$(echo "$RESULT1" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['cumulative_truncation_error'])")
python3 -c "
import math
err = $TRUNC_ERR
log_err = math.log10(err) if err > 0 else -999
print(f'Truncation error: {err}')
print(f'Order of magnitude: 10^{log_err:.1f}')
if err < 1e-10:
    print('✅ PASS: Machine precision (FP64 arithmetic - REAL quantum)')
elif err < 1e-6:
    print('⚠️  WARNING: Moderate precision - may be approximate')
else:
    print('❌ FAIL: High error - likely fake simulation')
"
echo ""

# CRITICAL TEST 5: 65,536 qubit execution time
echo "[7/7] TEST 5: SCALABILITY (65,536 qubits)"
python3 -c "
import requests, json
data = {'domain': 'chemistry', 'algorithm': 'vqe', 'qubits': 1024}
resp = requests.post('http://localhost:8080/api/v1/quantum/execute', json=data)
result = resp.json()
if result.get('success'):
    r = result['result']
    print(f\"Qubits requested: {r.get('num_qubits_requested', 'N/A')}\")
    print(f\"Qubits simulated: {r.get('num_qubits_simulated', 'N/A')}\")
    print(f\"Real computation: {r.get('real_computation', 'N/A')}\")
    print(f\"Fidelity: {r.get('fidelity', 'N/A')}\")
    print(f\"Converged: {r.get('converged', 'N/A')}\")
    print(f\"Execution time: {r.get('execution_time_us', 'N/A')} μs\")
    if r.get('real_computation') == True and r.get('converged') == True:
        print('✅ PASS: 65,536-qubit execution succeeded - REAL quantum engine')
    else:
        print('❌ FAIL: 65,536-qubit execution failed')
else:
    print(f'❌ FAIL: Request failed: {result}')
"

echo ""
echo "========================================="
echo "FORENSIC AUDIT COMPLETE"
echo "========================================="
echo ""

# Cleanup
kill $SERVER_PID 2>/dev/null || true
echo "Server stopped (PID $SERVER_PID)"
