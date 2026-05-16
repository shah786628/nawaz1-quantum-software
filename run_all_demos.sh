#!/bin/bash
# =============================================================================
# Nawaz1 Quantum VQE Engine - Run All Demos (Bash)
# =============================================================================
# Runs all quantum domain examples and data import demonstrations.
#
# Prerequisites:
#   - nawaz1-server running on localhost:8080 (or set NAWAZ1_HOST/NAWAZ1_PORT)
#   - Python 3.8+ with 'requests' library installed
#   - curl (for direct API calls)
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
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          NAWAZ1 QUANTUM VQE ENGINE - Demo Runner                   ║"
echo "║          All 16 Domains + Data Import + Pipeline                   ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
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
# Step 2: Quick API demos with curl
# =============================================================================
echo -e "\n${YELLOW}[2/6] Quick API demos (curl)...${NC}"

echo -e "\n${CYAN}  --- Chemistry: H2 molecule (VQE, 65536 qubits) ---${NC}"
curl -s -X POST "${BASE_URL}/quantum/execute" \
    "${HEADERS[@]}" \
    -d '{"domain":"chemistry","num_qubits":65536,"algorithm":"vqe","molecule":"H2","bond_length":0.74}' | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- Physics: Heisenberg model (65536 qubits) ---${NC}"
curl -s -X POST "${BASE_URL}/quantum/execute" \
    "${HEADERS[@]}" \
    -d '{"domain":"physics","num_qubits":65536,"algorithm":"vqe","model":"heisenberg","lattice_size":8}' | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- Finance: Portfolio (QAOA, 65536 qubits) ---${NC}"
curl -s -X POST "${BASE_URL}/quantum/execute" \
    "${HEADERS[@]}" \
    -d '{"domain":"finance","num_qubits":65536,"algorithm":"qaoa","problem_type":"portfolio_optimization","num_assets":8}' | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- Core Gates: Grover search (65536 qubits) ---${NC}"
curl -s -X POST "${BASE_URL}/quantum/execute" \
    "${HEADERS[@]}" \
    -d '{"domain":"core_gates","num_qubits":65536,"algorithm":"grover","search_space_size":64,"target_states":[42]}' | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- VQS Time Evolution (65536 qubits) ---${NC}"
curl -s -X POST "${BASE_URL}/quantum/vqs/evolve" \
    "${HEADERS[@]}" \
    -d '{"num_qubits":65536,"time_steps":10,"dt_seconds":0.1}' | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- Pipeline Execution (65536 qubits) ---${NC}"
curl -s -X POST "${BASE_URL}/quantum/pipeline/execute" \
    "${HEADERS[@]}" \
    -d '{"domain":"chemistry","num_qubits":65536,"molecule":"H2","bond_length":0.74}' | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

echo -e "\n${CYAN}  --- Multidimensional Query ---${NC}"
curl -s -X POST "${BASE_URL}/multidimensional/query" \
    "${HEADERS[@]}" \
    -d '{"type":"range","dimensions":3,"data_points":64}' | \
    python3 -m json.tool 2>/dev/null || echo "(raw output above)"

# =============================================================================
# Step 3: Run Python quantum examples (all 16 domains)
# =============================================================================
echo -e "\n${YELLOW}[3/6] Running quantum domain examples (Python)...${NC}"
if command -v python3 &>/dev/null; then
    python3 quantum_usage_examples.py 2>&1 || echo -e "${RED}  Some examples failed (server may not support all domains)${NC}"
else
    echo -e "${RED}  Python3 not found. Install Python 3.8+ to run examples.${NC}"
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
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  ALL DEMOS COMPLETE                                                ║"
echo "║                                                                    ║"
echo "║  Domains tested: 16 (chemistry, physics, finance, materials,       ║"
echo "║    biomolecules, ML, logistics, nuclear, math, error_mitigation,   ║"
echo "║    graphics, real_time, fluid_mechanics, turbulence_cfd,           ║"
echo "║    heat_transfer, core_gates)                                      ║"
echo "║                                                                    ║"
echo "║  Algorithms: VQE, QAOA, HHL, Grover                               ║"
echo "║  Features:   VQS evolution, Pipeline, Multidimensional queries     ║"
echo "║  Data:       Import, Batch, Query, Update, Delete                  ║"
echo "║  Auth:       Register, Login, JWT tokens                           ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
