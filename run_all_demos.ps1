# =============================================================================
# Nawaz1 Quantum VQE Engine - Run All Demos (PowerShell)
# =============================================================================
# Runs all quantum domain examples at REAL 65536-qubit scale.
# Covers ALL 62 algorithms across 13 categories (A-M) via the Python script,
# with inline 1024-qubit PowerShell demos for quick API validation.
#
# The VQE engine uses amplitude encoding: num_qubits is determined by the
# input_data array length (data.len().next_power_of_two()). For 65536 qubits,
# each request must include 65536 amplitude values.
#
# Inline PowerShell demos use 1024 data points (= 1024 qubits) for speed.
# Full 65536-qubit examples run via quantum_usage_examples.py (Step 7).
#
# Prerequisites:
#   - nawaz1-server running on localhost:8080 (or set NAWAZ1_HOST/NAWAZ1_PORT)
#   - Python 3.8+ with 'numpy' and 'requests' libraries
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

function Generate-Data($seed, $size) {
    # Generate normalized random data array using Python/numpy
    $script = "import numpy as np, json; rng=np.random.RandomState($seed); d=rng.normal(0,1,$size); d=d/np.linalg.norm(d); print(json.dumps(d.tolist()))"
    $pythonCmd = if (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" } elseif (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { $null }
    if ($pythonCmd) {
        $result = & $pythonCmd -c $script 2>$null
        if ($result) { return ($result | ConvertFrom-Json) }
    }
    # Fallback: generate simple data in PowerShell (smaller for performance)
    $data = @()
    $rng = New-Object System.Random($seed)
    for ($i = 0; $i -lt $size; $i++) {
        $data += [math]::Round(($rng.NextDouble() * 2 - 1), 6)
    }
    $norm = [math]::Sqrt(($data | ForEach-Object { $_ * $_ } | Measure-Object -Sum).Sum)
    return $data | ForEach-Object { [math]::Round($_ / $norm, 8) }
}

function Invoke-Quantum($payload, $label) {
    Write-Host "`n  --- $label ---" -ForegroundColor Cyan
    try {
        $body = $payload | ConvertTo-Json -Depth 10 -Compress
        $resp = Invoke-RestMethod -Uri "$BaseUrl/quantum/execute" -Method Post -Body $body -Headers $headers -TimeoutSec 120
        Write-Host "  Result:" -ForegroundColor Green
        $resp | ConvertTo-Json -Depth 5 | Write-Host
        return $resp
    } catch {
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Yellow
Write-Host "  NAWAZ1 QUANTUM VQE ENGINE - Demo Runner (65536-Qubit Scale)"
Write-Host "  62 Algorithms | 13 Categories (A-M) | Unified L3 VQE Substrate"
Write-Host "  Data SIZE determines qubit count (amplitude encoding)"
Write-Host "========================================================================" -ForegroundColor Yellow
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
# Step 2: All 15 Quantum Domains (1024-point inline demo)
# Qubit count = input_data.length = 1024 for inline speed.
# Full 65536-qubit scale runs in Step 7 via Python.
# =============================================================================
Write-Host "`n[2/7] Running all 15 quantum domains (1024-qubit inline demo)..." -ForegroundColor Yellow
Write-Host "       (Full 65536-qubit scale runs in Step 7 via Python)" -ForegroundColor Gray

# Generate 1024-point data arrays for inline demos
Write-Host "  Generating 1024-point amplitude arrays..." -ForegroundColor Gray
$chemData = Generate-Data 42 1024
$physData = Generate-Data 43 1024
$finData = Generate-Data 44 1024
$matData = Generate-Data 45 1024
$bioData = Generate-Data 46 1024
$mlData = Generate-Data 47 1024
$logData = Generate-Data 48 1024
$mathData = Generate-Data 50 1024
$errData = Generate-Data 51 1024
$gfxData = Generate-Data 52 1024
$rtData = Generate-Data 53 1024
$fluidData = Generate-Data 54 1024
$turbData = Generate-Data 55 1024
$heatData = Generate-Data 56 1024
$gateData = Generate-Data 57 1024

# 1. Chemistry — Hemoglobin (scaled to 1024 for inline)
Invoke-Quantum @{ domain="chemistry"; algorithm="vqe"; molecule="hemoglobin"; atoms=8738; description="Hemoglobin 8738 atoms (1024 orbital amplitudes demo)"; input_data=$chemData } "Chemistry: Hemoglobin (1024 amplitudes → 1024 qubits)"

# 2. Physics — 32×32 Heisenberg lattice (1024 sites)
Invoke-Quantum @{ domain="physics"; algorithm="vqe"; model="heisenberg_xxz"; lattice_size=32; description="32x32 Heisenberg XXZ (1024 sites demo)"; input_data=$physData } "Physics: 32×32 Heisenberg (1024 sites → 1024 qubits)"

# 3. Finance — 1024-asset portfolio
Invoke-Quantum @{ domain="finance"; algorithm="qaoa"; problem_type="portfolio_optimization"; num_assets=1024; description="1024-asset portfolio (demo scale)"; input_data=$finData } "Finance: 1024-Asset Portfolio (1024 qubits)"

# 4. Materials Science — 1024-atom crystal
Invoke-Quantum @{ domain="materials_science"; algorithm="vqe"; material="YBCO"; lattice_atoms=1024; description="YBCO 1024-atom lattice (demo)"; input_data=$matData } "Materials: YBCO Crystal (1024 atoms → 1024 qubits)"

# 5. Biomolecules — Protein folding (1024 conformations)
Invoke-Quantum @{ domain="biomolecules"; algorithm="vqe"; problem_type="protein_folding"; protein="hemoglobin_tetramer"; atoms=4532; description="Hemoglobin folding (1024 conformations demo)"; input_data=$bioData } "Biomolecules: Hemoglobin Folding (1024 qubits)"

# 6. Machine Learning — 1024-feature kernel
Invoke-Quantum @{ domain="machine_learning"; algorithm="vqe"; problem_type="quantum_kernel_svm"; num_features=1024; description="Quantum kernel SVM (1024 features demo)"; input_data=$mlData } "ML: Quantum Kernel SVM (1024 features → 1024 qubits)"

# 7. Logistics — 1024-node routing
Invoke-Quantum @{ domain="logistics"; algorithm="qaoa"; problem_type="vehicle_routing"; num_nodes=1024; description="1024-node supply chain (demo)"; input_data=$logData } "Logistics: 1024-Node Routing (1024 qubits)"

# 8. Mathematics — 1024×1024 linear system
Invoke-Quantum @{ domain="mathematics"; algorithm="hhl"; problem_type="linear_system"; matrix_size=1024; description="1024x1024 sparse system (demo)"; input_data=$mathData } "Mathematics: HHL 1024×1024 (1024 qubits)"

# 9. Error Mitigation — 1024-qubit ZNE
Invoke-Quantum @{ domain="error_mitigation"; algorithm="vqe"; mitigation_method="zero_noise_extrapolation"; noise_factors=@(1.0, 1.5, 2.0, 2.5); description="1024-qubit ZNE (demo)"; input_data=$errData } "Error Mitigation: ZNE (1024 qubits)"

# 10. Graphics — 32×32 ray tracing
Invoke-Quantum @{ domain="graphics"; algorithm="grover"; problem_type="ray_tracing"; resolution=@(32, 32); scene_objects=4096; description="32x32 quantum ray tracing (demo)"; input_data=$gfxData } "Graphics: Ray Tracing (1024 pixels → 1024 qubits)"

# 11. Real-Time — 1024-site state evolution
Invoke-Quantum @{ domain="real_time"; algorithm="vqe"; problem_type="state_evolution"; num_sites=1024; description="1024-site real-time evolution (demo)"; input_data=$rtData } "Real-Time: State Evolution (1024 qubits)"

# 12. Fluid Mechanics — 32×32 Navier-Stokes
Invoke-Quantum @{ domain="fluid_mechanics"; algorithm="vqe"; problem_type="navier_stokes"; grid_size=@(32, 32); reynolds_number=1000; description="32x32 NS grid (demo)"; input_data=$fluidData } "Fluid Mechanics: 32×32 NS (1024 qubits)"

# 13. Turbulence CFD — 1024-point DNS
Invoke-Quantum @{ domain="turbulence_cfd"; algorithm="vqe"; problem_type="dns_turbulence"; grid_points=1024; reynolds_number=10000; description="1024-point DNS Re=10000 (demo)"; input_data=$turbData } "Turbulence: 1024-Point DNS (1024 qubits)"

# 14. Heat Transfer — 32×32 thermal grid
Invoke-Quantum @{ domain="heat_transfer"; algorithm="hhl"; problem_type="conduction"; grid_size=@(32, 32); thermal_conductivity=237; description="32x32 heat grid (demo)"; input_data=$heatData } "Heat Transfer: 32×32 Grid (1024 qubits)"

# 15. Core Gates — 1024-element Grover search
Invoke-Quantum @{ domain="core_gates"; algorithm="grover"; problem_type="quantum_fourier_transform"; register_size=1024; search_space_size=1024; target_states=@(42); input_data=$gateData } "Core Gates: QFT + Grover (1024 qubits)"

# =============================================================================
# Step 3: Algorithm Bridge Demos — Selected from 13 Categories (1024-qubit inline)
# Full 62-algorithm coverage runs via Python in Step 7.
# Categories: A(VQE×8), B(Optimizers×6), C(Ansatze×5), D(QAOA×5),
#             E(HHL×4), F(Grover×1), G(ErrMit×5), H(MeasRed×3),
#             I(Numerical×7), J(Specialized×5), K(CondMatter×4),
#             L(TimeEvol×3), M(Advanced×6)
# =============================================================================
Write-Host "`n[3/7] Algorithm Bridge - Sample from 13 categories (1024-qubit demo)..." -ForegroundColor Yellow
Write-Host "       (Full 62 algorithms at 65536-qubit scale run in Step 7 via Python)" -ForegroundColor Gray

# A: VQE Family
Invoke-Quantum @{ domain="chemistry"; algorithm="vqe"; molecule="hemoglobin"; atoms=8738; input_data=$chemData } "Cat A: VQE — Hemoglobin ground state (1024 amplitudes)"
Invoke-Quantum @{ domain="chemistry"; algorithm="adapt_vqe"; molecule="hemoglobin"; atoms=8738; operator_pool="fermionic"; input_data=$chemData } "Cat A: ADAPT-VQE — iterative ansatz growth"

# B: VQE Optimizers
Invoke-Quantum @{ domain="chemistry"; algorithm="vqe"; optimizer="spsa"; molecule="hemoglobin"; atoms=8738; max_iterations=500; input_data=$chemData } "Cat B: VQE+SPSA optimizer"

# C: VQE Ansatze
Invoke-Quantum @{ domain="chemistry"; algorithm="vqe"; ansatz="uccsd"; molecule="hemoglobin"; atoms=8738; input_data=$chemData } "Cat C: VQE+UCCSD ansatz"

# D: QAOA Variants
Invoke-Quantum @{ domain="finance"; algorithm="qaoa"; qaoa_variant="standard"; problem_type="portfolio_optimization"; num_assets=1024; p_layers=8; input_data=$finData } "Cat D: QAOA — 1024-asset portfolio"

# E: HHL Family
Invoke-Quantum @{ domain="mathematics"; algorithm="hhl"; problem_type="linear_system"; matrix_size=1024; input_data=$mathData } "Cat E: HHL — 1024×1024 linear system"

# F: Grover Search
Invoke-Quantum @{ domain="core_gates"; algorithm="grover"; search_space_size=1024; target_states=@(42); input_data=$gateData } "Cat F: Grover — 1024-element search"

# G: Error Mitigation
Invoke-Quantum @{ domain="error_mitigation"; algorithm="vqe"; mitigation_method="pec"; num_calibration_circuits=256; input_data=$errData } "Cat G: PEC — Probabilistic Error Cancellation"

# I: Numerical Solvers
Invoke-Quantum @{ domain="fluid_mechanics"; algorithm="vqe"; problem_type="pde_solver"; pde_method="fdm"; equation="navier_stokes_2d"; grid_size=@(32,32); input_data=$fluidData } "Cat I: FDM — Navier-Stokes (32×32)"

# K: Condensed Matter
Invoke-Quantum @{ domain="physics"; algorithm="vqe"; problem_type="condensed_matter"; model="hubbard"; lattice_size=32; hopping_t=1.0; interaction_u=4.0; input_data=$physData } "Cat K: Hubbard Model — 32×32 lattice"

# M: Advanced Quantum
Invoke-Quantum @{ domain="machine_learning"; algorithm="vqe"; problem_type="qnn"; num_features=1024; num_layers=12; input_data=$mlData } "Cat M: QNN — Quantum Neural Network"

# =============================================================================
# Step 4: VQS Time Evolution (1024-site demo)
# =============================================================================
Write-Host "`n[4/7] VQS Time Evolution (1024-site demo)..." -ForegroundColor Yellow

try {
    $vqsPayload = @{
        num_sites = 1024
        time_steps = 20
        dt_seconds = 0.05
        hamiltonian = "heisenberg_xxz"
        initial_state = "neel"
        description = "1024-site Heisenberg XXZ time evolution (demo scale)"
        input_data = $rtData
    }
    $vqsBody = $vqsPayload | ConvertTo-Json -Depth 10 -Compress
    $vqsResp = Invoke-RestMethod -Uri "$BaseUrl/quantum/vqs/evolve" -Method Post -Body $vqsBody -Headers $headers -TimeoutSec 120
    Write-Host "  VQS Evolution:" -ForegroundColor Green
    $vqsResp | ConvertTo-Json -Depth 5 | Write-Host
} catch {
    Write-Host "  VQS Error: $($_.Exception.Message)" -ForegroundColor Red
}

# =============================================================================
# Step 5: Pipeline Execution (1024-amplitude demo)
# =============================================================================
Write-Host "`n[5/7] Pipeline Execution (L1→L2→L3, 1024 amplitudes)..." -ForegroundColor Yellow

try {
    $pipePayload = @{
        domain = "chemistry"
        molecule = "hemoglobin"
        atoms = 8738
        description = "Hemoglobin pipeline: 1024 orbital amplitudes → L1 encode → L2 tensor → L3 VQE"
        input_data = $chemData
    }
    $pipeBody = $pipePayload | ConvertTo-Json -Depth 10 -Compress
    $pipeResp = Invoke-RestMethod -Uri "$BaseUrl/quantum/pipeline/execute" -Method Post -Body $pipeBody -Headers $headers -TimeoutSec 120
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
        $sql = '{"query":"INSERT INTO ps_demo VALUES (1, ''hemoglobin'', -4532.7), (2, ''uranium238'', -1783.2), (3, ''ybco_crystal'', -892.1)"}'
        Invoke-RestMethod -Uri "$BaseUrl/query" -Method Post -Body $sql -Headers $authHeaders -TimeoutSec 10 | Out-Null
        Write-Host "  Inserted 3 rows (large-scale quantum results)" -ForegroundColor Green
        
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
# Step 7: Run Python scripts — FULL 65536-QUBIT SCALE
# =============================================================================
Write-Host "`n[7/7] Running Python scripts (FULL 65536-qubit scale)..." -ForegroundColor Yellow
Write-Host "       Each domain sends 65536 amplitude values → engine allocates 65536 qubits" -ForegroundColor Gray

$pythonCmd = if (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" } elseif (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { $null }

if ($pythonCmd) {
    Write-Host "  Running quantum_usage_examples.py --list (category overview)..." -ForegroundColor Cyan
    & $pythonCmd quantum_usage_examples.py --list 2>&1
    Write-Host ""
    Write-Host "  Running quantum_usage_examples.py (ALL 62 algorithms, 65536-qubit scale)..." -ForegroundColor Cyan
    & $pythonCmd quantum_usage_examples.py 2>&1 | Select-Object -First 200
    Write-Host "`n  Running data_import_examples.py..." -ForegroundColor Cyan
    & $pythonCmd data_import_examples.py 2>&1 | Select-Object -First 50
} else {
    Write-Host "  Python not found. Install Python 3.8+ with numpy to run 65536-qubit examples." -ForegroundColor Red
    Write-Host "  The Python script demonstrates all 62 algorithms across 13 categories (A-M):" -ForegroundColor Red
    Write-Host "    A: VQE Family (8)        B: VQE Optimizers (6)   C: VQE Ansatze (5)" -ForegroundColor Gray
    Write-Host "    D: QAOA Variants (5)     E: HHL Family (4)       F: Grover (1)" -ForegroundColor Gray
    Write-Host "    G: Error Mitigation (5)  H: Meas. Reduction (3)  I: Numerical (7)" -ForegroundColor Gray
    Write-Host "    J: Specialized (5)       K: Condensed Matter (4)  L: Time Evol (3)" -ForegroundColor Gray
    Write-Host "    M: Advanced Quantum (6)" -ForegroundColor Gray
}

# =============================================================================
# Summary
# =============================================================================
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "  ALL DEMOS COMPLETE" -ForegroundColor Green
Write-Host ""
Write-Host "  QUBIT SCALING (amplitude encoding):"
Write-Host "    PowerShell inline: 1024 data points -> 1024 qubits (quick demo)"
Write-Host "    Python full scale: 65536 data points -> 65536 qubits"
Write-Host ""
Write-Host "  ALGORITHMS: 62 total across 13 categories (A-M):"
Write-Host "    A: VQE Family (8)        B: VQE Optimizers (6)   C: VQE Ansatze (5)"
Write-Host "    D: QAOA Variants (5)     E: HHL Family (4)       F: Grover (1)"
Write-Host "    G: Error Mitigation (5)  H: Meas. Reduction (3)  I: Numerical (7)"
Write-Host "    J: Specialized (5)       K: Condensed Matter (4)  L: Time Evol (3)"
Write-Host "    M: Advanced Quantum (6)"
Write-Host ""
Write-Host "  Domains:    15 (chemistry, physics, finance, materials,"
Write-Host "              biomolecules, ML, logistics, math,"
Write-Host "              error_mitigation, graphics, real_time,"
Write-Host "              fluid_mechanics, turbulence_cfd, heat_transfer,"
Write-Host "              core_gates)"
Write-Host ""
Write-Host "  Features:   VQS evolution, Pipeline, Multidimensional"
Write-Host "  Data:       Import, Batch, Query, Auth"
Write-Host ""
Write-Host "  Run individual categories:"
Write-Host "    python quantum_usage_examples.py --list        # List all categories"
Write-Host "    python quantum_usage_examples.py vqe_family    # Run single category"
Write-Host "    python quantum_usage_examples.py algorithms    # Run all 62 algorithms"
Write-Host "========================================================================" -ForegroundColor Green
