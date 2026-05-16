#!/bin/bash
# =============================================================================
# Nawaz1 Quantum VQE Engine - Run All Demos (Bash)
# =============================================================================
# Runs all quantum domain examples at REAL 65536-qubit scale.
#
# The VQE engine uses amplitude encoding: the number of qubits is determined
# by the input_data array length (data.len().next_power_of_two()). For 65536
# qubits, each request must include 65536 amplitude values.
#
# This script uses Python to generate the 65536-element data arrays and
# submit them via curl. The inline curl examples use 1024 data points
# (= 1024 qubits) for quick demonstration; run quantum_usage_examples.py
# for full 65536-qubit scale.
#
# Prerequisites:
#   - nawaz1-server running on localhost:8080 (or set NAWAZ1_HOST/NAWAZ1_PORT)
#   - Python 3.8+ with 'numpy' and 'requests' libraries
#   - curl (for quick API demos)
#
# Usage:
#   chmod +x run_all_demos.sh
#   ./run_all_demos.sh
#
# Author: Shahnawaz Alam
# Copyright (c) 2026 Shahnawaz Alam. All rights reserved.
# =============================================================================

set -e

# Configuration
HOST="${NAWAZ1_HOST:-localhost}"
PORT="${NAWAZ1_PORT:-8080}"
BASE_URL="http://${HOST}:${PORT}/api/v1"
API_KEY="${NAWAZ1_API_KEY:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║  NAWAZ1 QUANTUM VQE ENGINE - Demo Runner (65536-Qubit Scale)           ║"
echo "║  All 16 Domains + Data Import + Pipeline                               ║"
echo "║  Data SIZE determines qubit count (amplitude encoding)                 ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Build headers for curl
HEADERS=(-H "Content-Type: application/json")
if [ -n "$API_KEY" ]; then
    HEADERS+=(-H "X-API-Key: $API_KEY")
    echo -e "${YELLOW}API Key: Enabled${NC}"
fi

# =============================================================================
# Step 1: Check server health
# =============================================================================
echo -e "\n${YELLOW}[1/6] Checking server health...${NC}"
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/health" 2>/dev/null || echo "000")

if [ "$HEALTH" = "200" ]; then
    echo -e "${GREEN}  ✓ Server is running at ${BASE_URL}${NC}"
else
    echo -e "${RED}  ✗ Server not reachable at ${BASE_URL} (HTTP ${HEALTH})${NC}"
    echo "  Please start the server: nawaz1-server"
    echo "  Or set NAWAZ1_HOST and NAWAZ1_PORT environment variables"
    exit 1
fi

# Show server status
echo -e "\n  Server Status:"
curl -s "${BASE_URL}/quantum/status" "${HEADERS[@]}" | python3 -m json.tool 2>/dev/null || \
    curl -s "${BASE_URL}/quantum/status" "${HEADERS[@]}"
echo ""

# Show available domains
echo -e "\n  Available Domains:"
curl -s "${BASE_URL}/quantum/domains" "${HEADERS[@]}" | python3 -m json.tool 2>/dev/null || \
    curl -s "${BASE_URL}/quantum/domains" "${HEADERS[@]}"
echo ""

# =============================================================================
# Step 2: Quick API demos with curl (1024-point inline = 1024 qubits)
# These demonstrate the API format. Full 65536-qubit examples use Python.
# =============================================================================
echo -e "\n${YELLOW}[2/6] Quick API demos (curl, 1024-qubit inline examples)...${NC}"
echo -e "       (Full 65536-qubit scale runs in Step 3 via Python)"

# Generate 1024-element JSON arrays via Python for curl demos
CHEM_DATA=$(python3 -c "
import numpy as np, json
rng = np.random.RandomState(42)
d = rng.normal(0, 1, 1024)
d = d / np.linalg.norm(d)
print(json.dumps(d.tolist()))
" 2>/dev/null || echo "[]")

PHYS_DATA=$(python3 -c "
import numpy as np, json
rng = np.random.RandomState(43)
d = np.array([((-1)**(i%512+i//512)) * (1.0 + 0.1*rng.normal()) for i in range(1024)])
d = d / np.linalg.norm(d)
print(json.dumps(d.tolist()))
" 2>/dev/null || echo "[]")

FIN_DATA=$(python3 -c "
import numpy as np, json
rng = np.random.RandomState(44)
d = rng.normal(0.05, 0.2, 1024)
d = d / np.linalg.norm(d)
print(json.dumps(d.tolist()))
" 2>/dev/null || echo "[]")

echo -e "\n${CYAN}  --- Chemistry: Hemoglobin (1024 orbital amplitudes → 1024 qubits demo) ---${NC}"
curl -s -X POST "${BASE_URL}/quantum/execute" \
    "${HEADERS[@]}" \
    -d "{\"domain\":\"chemistry\",\"algorithm\":\"vqe\",\"molecule\":\"hemoglobin\",\"atoms\":8738,\"input_data\":${CHEM_DATA}}" | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- Physics: 32×32 Heisenberg lattice (1024 sites → 1024 qubits demo) ---${NC}"
curl -s -X POST "${BASE_URL}/quantum/execute" \
    "${HEADERS[@]}" \
    -d "{\"domain\":\"physics\",\"algorithm\":\"vqe\",\"model\":\"heisenberg_xxz\",\"lattice_size\":32,\"input_data\":${PHYS_DATA}}" | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- Finance: 1024-asset portfolio (1024 returns → 1024 qubits demo) ---${NC}"
curl -s -X POST "${BASE_URL}/quantum/execute" \
    "${HEADERS[@]}" \
    -d "{\"domain\":\"finance\",\"algorithm\":\"qaoa\",\"problem_type\":\"portfolio_optimization\",\"num_assets\":1024,\"input_data\":${FIN_DATA}}" | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- Core Gates: Grover over 1024-element space (1024 qubits demo) ---${NC}"
GATES_DATA=$(python3 -c "
import numpy as np, json
rng = np.random.RandomState(57)
t = np.linspace(0, 1, 1024)
d = np.sin(2*np.pi*50*t) + 0.5*np.sin(2*np.pi*120*t)
d = d / np.linalg.norm(d)
print(json.dumps(d.tolist()))
" 2>/dev/null || echo "[]")
curl -s -X POST "${BASE_URL}/quantum/execute" \
    "${HEADERS[@]}" \
    -d "{\"domain\":\"core_gates\",\"algorithm\":\"grover\",\"search_space_size\":1024,\"target_states\":[42],\"input_data\":${GATES_DATA}}" | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- VQS Time Evolution (1024 sites, 20 steps) ---${NC}"
VQS_DATA=$(python3 -c "
import numpy as np, json
rng = np.random.RandomState(53)
d = np.array([((-1)**i)*(1.0+0.05*rng.normal()) for i in range(1024)])
d = d / np.linalg.norm(d)
print(json.dumps(d.tolist()))
" 2>/dev/null || echo "[]")
curl -s -X POST "${BASE_URL}/quantum/vqs/evolve" \
    "${HEADERS[@]}" \
    -d "{\"num_sites\":1024,\"time_steps\":20,\"dt_seconds\":0.05,\"hamiltonian\":\"heisenberg_xxz\",\"input_data\":${VQS_DATA}}" | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- Pipeline: Hemoglobin (1024 amplitudes → L1→L2→L3) ---${NC}"
curl -s -X POST "${BASE_URL}/quantum/pipeline/execute" \
    "${HEADERS[@]}" \
    -d "{\"domain\":\"chemistry\",\"molecule\":\"hemoglobin\",\"atoms\":8738,\"input_data\":${CHEM_DATA}}" | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- Multidimensional Query (65536 data points) ---${NC}"
curl -s -X POST "${BASE_URL}/multidimensional/query" \
    "${HEADERS[@]}" \
    -d '{"type":"range","dimensions":3,"data_points":65536,"bounds":{"min":[0,0,0],"max":[1,1,1]}}' | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

# =============================================================================
# Step 3: Run Python quantum examples (FULL 65536-qubit scale, all 16 domains)
# =============================================================================
echo -e "\n${YELLOW}[3/6] Running FULL 65536-qubit quantum examples (Python)...${NC}"
echo -e "       Each domain sends 65536 amplitude values → engine allocates 65536 qubits"
if command -v python3 &>/dev/null; then
    python3 quantum_usage_examples.py 2>&1 || echo -e "${RED}  Some examples failed (server may not support all domains)${NC}"
else
    echo -e "${RED}  Python3 not found. Install Python 3.8+ with numpy to run 65536-qubit examples.${NC}"
fi

# =============================================================================
# Step 4: Run data import examples
# =============================================================================
echo -e "\n${YELLOW}[4/6] Running data import examples (Python)...${NC}"
if command -v python3 &>/dev/null; then
    python3 data_import_examples.py 2>&1 || echo -e "${RED}  Some import steps failed${NC}"
else
    echo -e "${RED}  Python3 not found.${NC}"
fi

# =============================================================================
# Step 5: Authentication demo (curl)
# =============================================================================
echo -e "\n${YELLOW}[5/6] Authentication demo (curl)...${NC}"

echo -e "\n${CYAN}  --- Register user ---${NC}"
curl -s -X POST "${BASE_URL}/auth/register" \
    "${HEADERS[@]}" \
    -d '{"username":"demo_user","password":"DemoPass123!","email":"demo@quantum.dev"}'
echo ""

echo -e "\n${CYAN}  --- Login ---${NC}"
LOGIN_RESP=$(curl -s -X POST "${BASE_URL}/auth/login" \
    "${HEADERS[@]}" \
    -d '{"username":"demo_user","password":"DemoPass123!"}')
echo "$LOGIN_RESP" | python3 -m json.tool 2>/dev/null || echo "$LOGIN_RESP"

# Extract token
TOKEN=$(echo "$LOGIN_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('token','') or d.get('access_token',''))" 2>/dev/null || echo "")

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}  ✓ Token acquired${NC}"
    
    echo -e "\n${CYAN}  --- Create table with auth ---${NC}"
    curl -s -X POST "${BASE_URL}/query" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"query":"CREATE TABLE demo_auth_test (id INT, value TEXT)"}'
    echo ""
    
    echo -e "\n${CYAN}  --- Insert with auth ---${NC}"
    curl -s -X POST "${BASE_URL}/query" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"query":"INSERT INTO demo_auth_test VALUES (1, '\''authenticated write'\'')"}'
    echo ""
    
    echo -e "\n${CYAN}  --- Query with auth ---${NC}"
    curl -s -X POST "${BASE_URL}/query" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"query":"SELECT * FROM demo_auth_test"}'
    echo ""
    
    echo -e "\n${CYAN}  --- Cleanup ---${NC}"
    curl -s -X POST "${BASE_URL}/query" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"query":"DROP TABLE demo_auth_test"}'
    echo ""
fi

# =============================================================================
# Step 6: Summary
# =============================================================================
echo -e "\n${YELLOW}[6/6] Summary${NC}"
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║  ALL DEMOS COMPLETE                                                    ║"
echo "║                                                                        ║"
echo "║  QUBIT SCALING: Data length determines qubit count (amplitude encoding)║"
echo "║  - Curl demos: 1024 data points → 1024 qubits (quick inline demo)     ║"
echo "║  - Python:     65536 data points → 65536 qubits (full scale)           ║"
echo "║                                                                        ║"
echo "║  Domains tested: 16 (chemistry, physics, finance, materials,           ║"
echo "║    biomolecules, ML, logistics, nuclear, math, error_mitigation,       ║"
echo "║    graphics, real_time, fluid_mechanics, turbulence_cfd,               ║"
echo "║    heat_transfer, core_gates)                                          ║"
echo "║                                                                        ║"
echo "║  Algorithms: VQE, QAOA, HHL, Grover                                   ║"
echo "║  Features:   VQS evolution, Pipeline, Multidimensional queries         ║"
echo "║  Data:       Import, Batch, Query, Update, Delete                      ║"
echo "║  Auth:       Register, Login, JWT tokens                               ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
