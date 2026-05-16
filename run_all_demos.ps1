# =============================================================================
# Nawaz1 Quantum VQE Engine - Run All Demos (PowerShell)
# =============================================================================
# Runs all quantum domain examples and data import demonstrations.
#
# Prerequisites:
#   - nawaz1-server running on localhost:8080 (or set NAWAZ1_HOST/NAWAZ1_PORT)
#   - Python 3.8+ with 'requests' library installed
#   - PowerShell 5.1+
#
# Usage:
#   .\run_all_demos.ps1
#
# Author: Shahnawaz Alam
# Copyright (c) 2026 Shahnawaz Alam. All rights reserved.
# =============================================================================

$ErrorActionPreference = "Continue"

# Configuration
$Host_ = if ($env:NAWAZ1_HOST) { $env:NAWAZ1_HOST } else { "localhost" }
$Port = if ($env:NAWAZ1_PORT) { $env:NAWAZ1_PORT } else { "8080" }
$BaseUrl = "http://${Host_}:${Port}/api/v1"
$ApiKey = $env:NAWAZ1_API_KEY

# Headers
$headers = @{ "Content-Type" = "application/json" }
if ($ApiKey) {
    $headers["X-API-Key"] = $ApiKey
}

function Invoke-Quantum($payload, $label) {
    Write-Host "`n  --- $label ---" -ForegroundColor Cyan
    try {
        $body = $payload | ConvertTo-Json -Depth 10 -Compress
        $resp = Invoke-RestMethod -Uri "$BaseUrl/quantum/execute" -Method Post -Body $body -Headers $headers -TimeoutSec 60
        Write-Host "  Result:" -ForegroundColor Green
        $resp | ConvertTo-Json -Depth 5 | Write-Host
        return $resp
    } catch {
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host "  NAWAZ1 QUANTUM VQE ENGINE - Demo Runner (PowerShell)"
Write-Host "  All 16 Domains + 4 Algorithms + Data Import + Pipeline"
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host ""

# =============================================================================
# Step 1: Health Check
# =============================================================================
Write-Host "[1/7] Checking server health..." -ForegroundColor Yellow

try {
    $health = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get -TimeoutSec 5
    Write-Host "  Server OK: $($health | ConvertTo-Json -Compress)" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Cannot reach server at $BaseUrl" -ForegroundColor Red
    Write-Host "  Please start: nawaz1-server" -ForegroundColor Red
    exit 1
}

try {
    $status = Invoke-RestMethod -Uri "$BaseUrl/quantum/status" -Method Get -Headers $headers -TimeoutSec 5
    Write-Host "  Quantum Status:" -ForegroundColor Cyan
    $status | ConvertTo-Json -Depth 3 | Write-Host
} catch {}

try {
    $domains = Invoke-RestMethod -Uri "$BaseUrl/quantum/domains" -Method Get -Headers $headers -TimeoutSec 5
    Write-Host "  Available Domains:" -ForegroundColor Cyan
    $domains | ConvertTo-Json -Depth 3 | Write-Host
} catch {}

# =============================================================================
# Step 2: All 16 Quantum Domains
# =============================================================================
Write-Host "`n[2/7] Running all 16 quantum domains..." -ForegroundColor Yellow

# 1. Chemistry
Invoke-Quantum @{ domain="chemistry"; num_qubits=65536; algorithm="vqe"; molecule="H2"; bond_length=0.74 } "Chemistry: H2 (VQE, 65536 qubits)"
Invoke-Quantum @{ domain="chemistry"; num_qubits=65536; algorithm="vqe"; molecule="H2O"; bond_length=0.96 } "Chemistry: H2O Water (65536 qubits)"

# 2. Physics
Invoke-Quantum @{ domain="physics"; num_qubits=65536; algorithm="vqe"; model="heisenberg"; lattice_size=8 } "Physics: Heisenberg Spin Chain (65536 qubits)"
Invoke-Quantum @{ domain="physics"; num_qubits=65536; algorithm="vqe"; model="ising"; transverse_field=0.5 } "Physics: Ising Model (65536 qubits)"

# 3. Finance
Invoke-Quantum @{ domain="finance"; num_qubits=65536; algorithm="qaoa"; problem_type="portfolio_optimization"; num_assets=8 } "Finance: Portfolio (QAOA, 65536 qubits)"

# 4. Materials Science
Invoke-Quantum @{ domain="materials_science"; num_qubits=65536; algorithm="vqe"; material="silicon"; crystal_structure="diamond_cubic" } "Materials: Silicon Band Gap (65536 qubits)"

# 5. Biomolecules
Invoke-Quantum @{ domain="biomolecules"; num_qubits=65536; algorithm="vqe"; problem_type="protein_folding"; num_residues=3 } "Biomolecules: Protein Folding (65536 qubits)"

# 6. Machine Learning
Invoke-Quantum @{ domain="machine_learning"; num_qubits=65536; algorithm="vqe"; problem_type="qnn_classification"; num_layers=4 } "ML: Quantum Neural Network (65536 qubits)"

# 7. Logistics
Invoke-Quantum @{ domain="logistics"; num_qubits=65536; algorithm="qaoa"; problem_type="routing"; num_cities=5 } "Logistics: TSP Routing (65536 qubits)"

# 8. Nuclear
Invoke-Quantum @{ domain="nuclear"; num_qubits=65536; algorithm="vqe"; nucleus="deuterium"; protons=1; neutrons=1 } "Nuclear: Deuterium (65536 qubits)"

# 9. Mathematics
Invoke-Quantum @{ domain="mathematics"; num_qubits=65536; algorithm="hhl"; problem_type="linear_system" } "Mathematics: HHL Linear System (65536 qubits)"

# 10. Error Mitigation
Invoke-Quantum @{ domain="error_mitigation"; num_qubits=65536; algorithm="vqe"; mitigation_method="zero_noise_extrapolation" } "Error Mitigation: ZNE (65536 qubits)"

# 11. Graphics
Invoke-Quantum @{ domain="graphics"; num_qubits=65536; algorithm="grover"; problem_type="ray_tracing"; scene_objects=64 } "Graphics: Quantum Ray Tracing (65536 qubits)"

# 12. Real-Time
Invoke-Quantum @{ domain="real_time"; num_qubits=65536; algorithm="vqe"; problem_type="state_monitoring" } "Real-Time: State Monitoring (65536 qubits)"

# 13. Fluid Mechanics
Invoke-Quantum @{ domain="fluid_mechanics"; num_qubits=65536; algorithm="vqe"; problem_type="navier_stokes"; reynolds_number=100 } "Fluid Mechanics: Navier-Stokes (65536 qubits)"

# 14. Turbulence CFD
Invoke-Quantum @{ domain="turbulence_cfd"; num_qubits=65536; algorithm="vqe"; problem_type="channel_flow"; reynolds_number=5000 } "Turbulence: Channel Flow (65536 qubits)"

# 15. Heat Transfer
Invoke-Quantum @{ domain="heat_transfer"; num_qubits=65536; algorithm="hhl"; problem_type="conduction"; thermal_conductivity=237 } "Heat Transfer: Conduction (65536 qubits)"

# 16. Core Gates
Invoke-Quantum @{ domain="core_gates"; num_qubits=65536; algorithm="grover"; search_space_size=64; target_states=@(42) } "Core Gates: Grover Search (65536 qubits)"

# =============================================================================
# Step 3: Algorithm Bridge Demos
# =============================================================================
Write-Host "`n[3/7] Algorithm Bridge - All 4 algorithms..." -ForegroundColor Yellow

Invoke-Quantum @{ domain="chemistry"; num_qubits=65536; algorithm="vqe"; molecule="H2"; bond_length=0.74 } "Algorithm: VQE (65536 qubits)"
Invoke-Quantum @{ domain="finance"; num_qubits=65536; algorithm="qaoa"; problem_type="portfolio_optimization" } "Algorithm: QAOA (65536 qubits)"
Invoke-Quantum @{ domain="mathematics"; num_qubits=65536; algorithm="hhl"; problem_type="linear_system" } "Algorithm: HHL (65536 qubits)"
Invoke-Quantum @{ domain="core_gates"; num_qubits=65536; algorithm="grover"; search_space_size=256 } "Algorithm: Grover (65536 qubits)"

# =============================================================================
# Step 4: VQS Time Evolution
# =============================================================================
Write-Host "`n[4/7] VQS Time Evolution..." -ForegroundColor Yellow

try {
    $vqsBody = @{ num_qubits=65536; time_steps=10; dt_seconds=0.1 } | ConvertTo-Json -Compress
    $vqsResp = Invoke-RestMethod -Uri "$BaseUrl/quantum/vqs/evolve" -Method Post -Body $vqsBody -Headers $headers -TimeoutSec 60
    Write-Host "  VQS Evolution:" -ForegroundColor Green
    $vqsResp | ConvertTo-Json -Depth 5 | Write-Host
} catch {
    Write-Host "  VQS Error: $($_.Exception.Message)" -ForegroundColor Red
}

# =============================================================================
# Step 5: Pipeline Execution
# =============================================================================
Write-Host "`n[5/7] Pipeline Execution (L1->L2->L3)..." -ForegroundColor Yellow

try {
    $pipeBody = @{ domain="chemistry"; num_qubits=65536; molecule="H2"; bond_length=0.74 } | ConvertTo-Json -Compress
    $pipeResp = Invoke-RestMethod -Uri "$BaseUrl/quantum/pipeline/execute" -Method Post -Body $pipeBody -Headers $headers -TimeoutSec 60
    Write-Host "  Pipeline Result:" -ForegroundColor Green
    $pipeResp | ConvertTo-Json -Depth 5 | Write-Host
} catch {
    Write-Host "  Pipeline Error: $($_.Exception.Message)" -ForegroundColor Red
}

# =============================================================================
# Step 6: Data Import Demo
# =============================================================================
Write-Host "`n[6/7] Data Import Demo..." -ForegroundColor Yellow

# Login first
try {
    $loginBody = '{"username":"admin","password":"admin123"}'
    $loginResp = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method Post -Body $loginBody -ContentType "application/json" -TimeoutSec 10
    $token = $loginResp.token
    if (-not $token) { $token = $loginResp.access_token }
    if ($token) {
        $authHeaders = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }
        Write-Host "  Auth: Token acquired" -ForegroundColor Green
        
        # Create table
        $sql = '{"query":"CREATE TABLE IF NOT EXISTS ps_demo (id INT PRIMARY KEY, name TEXT, value REAL)"}'
        Invoke-RestMethod -Uri "$BaseUrl/query" -Method Post -Body $sql -Headers $authHeaders -TimeoutSec 10 | Out-Null
        Write-Host "  Table created: ps_demo" -ForegroundColor Green
        
        # Insert data
        $sql = '{"query":"INSERT INTO ps_demo VALUES (1, ''hydrogen'', -1.137), (2, ''lithium'', -7.882), (3, ''water'', -75.456)"}'
        Invoke-RestMethod -Uri "$BaseUrl/query" -Method Post -Body $sql -Headers $authHeaders -TimeoutSec 10 | Out-Null
        Write-Host "  Inserted 3 rows" -ForegroundColor Green
        
        # Query
        $sql = '{"query":"SELECT * FROM ps_demo ORDER BY id"}'
        $qResp = Invoke-RestMethod -Uri "$BaseUrl/query" -Method Post -Body $sql -Headers $authHeaders -TimeoutSec 10
        Write-Host "  Query result:" -ForegroundColor Green
        $qResp | ConvertTo-Json -Depth 5 | Write-Host
        
        # Cleanup
        $sql = '{"query":"DROP TABLE ps_demo"}'
        Invoke-RestMethod -Uri "$BaseUrl/query" -Method Post -Body $sql -Headers $authHeaders -TimeoutSec 10 | Out-Null
        Write-Host "  Cleanup: table dropped" -ForegroundColor Green
    } else {
        Write-Host "  Auth: No token (open-access mode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  Data import error: $($_.Exception.Message)" -ForegroundColor Red
}

# =============================================================================
# Step 7: Run Python scripts (if available)
# =============================================================================
Write-Host "`n[7/7] Running Python scripts..." -ForegroundColor Yellow

$pythonCmd = if (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" } elseif (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { $null }

if ($pythonCmd) {
    Write-Host "  Running quantum_usage_examples.py..." -ForegroundColor Cyan
    & $pythonCmd quantum_usage_examples.py 2>&1 | Select-Object -First 50
    Write-Host "`n  Running data_import_examples.py..." -ForegroundColor Cyan
    & $pythonCmd data_import_examples.py 2>&1 | Select-Object -First 50
} else {
    Write-Host "  Python not found. Install Python 3.8+ to run full examples." -ForegroundColor Red
}

# =============================================================================
# Summary
# =============================================================================
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "  ALL DEMOS COMPLETE" -ForegroundColor Green
Write-Host ""
Write-Host "  Domains:    16 (chemistry, physics, finance, materials,"
Write-Host "              biomolecules, ML, logistics, nuclear, math,"
Write-Host "              error_mitigation, graphics, real_time,"
Write-Host "              fluid_mechanics, turbulence_cfd, heat_transfer,"
Write-Host "              core_gates)"
Write-Host ""
Write-Host "  Algorithms: VQE, QAOA, HHL, Grover"
Write-Host "  Features:   VQS evolution, Pipeline, Multidimensional"
Write-Host "  Data:       Import, Batch, Query, Auth"
Write-Host "================================================================" -ForegroundColor Green
