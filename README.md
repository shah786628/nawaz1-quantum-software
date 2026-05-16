# Nawaz1 Quantum VQE Engine - Usage Guide

> **Multidimensional L6→L3 Quantum Pipeline** — A production-grade quantum VQE engine supporting 16 domains, **51+ algorithms**, data persistence, and real-time streaming.

**Author:** Shahnawaz Alam  
**License:** Proprietary  
**Copyright (c) 2026 Shahnawaz Alam. All rights reserved.**

---

## Key Architecture: Unified L3 Substrate

All 51+ algorithms route through the **Algorithm Bridge → execute_l3()** on the pre-built VQE circuit substrate. The `algorithm` field is metadata for orchestration — all execution goes through the **same unified L3 quantum substrate**. The engine automatically selects the optimal algorithm based on domain and problem type when not explicitly specified.

---

## How Qubit Count Works (Amplitude Encoding)

The VQE engine uses **amplitude encoding**: the number of qubits is determined by the **input data length**, not a forced parameter.

```
num_qubits = input_data.len().next_power_of_two()
```

For **65536 qubits**, provide **65536 amplitude values** in the `input_data` array.

| Domain | Problem Scale for 65536 Qubits |
|--------|-------------------------------|
| Chemistry | Hemoglobin protein (8738 atoms, 65536 orbital amplitudes) |
| Physics | 256×256 Heisenberg lattice (65536 sites) |
| Finance | 65536 financial instruments (global portfolio) |
| Materials | 65536-atom YBCO superconductor crystal |
| Biomolecules | Hemoglobin tetramer (4532 atoms, 65536 conformations) |
| Machine Learning | 65536-feature quantum kernel SVM |
| Logistics | 65536-node global supply chain |
| Nuclear | Uranium-238 (238 nucleons, 65536 basis states) |
| Mathematics | 65536×65536 sparse linear system |
| Error Mitigation | 65536-amplitude noisy state correction |
| Graphics | 256×256 = 65536-pixel quantum ray tracing |
| Real-Time | 65536-site quantum state evolution |
| Fluid Mechanics | 256×256 Navier-Stokes grid (65536 points) |
| Turbulence CFD | 65536-point DNS turbulence (Re=10000) |
| Heat Transfer | 256×256 thermal conduction grid (65536 nodes) |
| Core Gates | 65536-qubit quantum Fourier transform |

---

## Table of Contents

- [Quick Start](#quick-start)
- [All 51+ Algorithms](#all-51-algorithms)
- [API Endpoints](#api-endpoints)
- [All 16 Quantum Domains](#all-16-quantum-domains)
- [Algorithm Categories (A–J)](#algorithm-categories-aj)
- [Data Import Guide](#data-import-guide)
- [Authentication & Security](#authentication--security)
- [Running the Examples](#running-the-examples)

---

## Quick Start

### 1. Start the Server

```bash
# Linux/macOS
./nawaz1-server

# Windows
nawaz1-server.exe

# With custom port
NAWAZ1_PORT=9090 ./nawaz1-server
```

### 2. Verify Health

```bash
curl http://localhost:8080/api/v1/health
# Expected: {"status":"healthy","version":"..."}
```

### 3. Run First Query (65536-qubit scale)

```python
import numpy as np, requests

data = np.random.RandomState(42).normal(0, 1, 65536)
data = (data / np.linalg.norm(data)).tolist()

resp = requests.post("http://localhost:8080/api/v1/quantum/execute", json={
    "domain": "chemistry",
    "algorithm": "vqe",
    "molecule": "hemoglobin",
    "atoms": 8738,
    "input_data": data  # 65536 values → engine allocates 65536 qubits
})
print(resp.json())
```

### 4. Run All Examples

```bash
pip install numpy requests
python quantum_usage_examples.py              # All demos
python quantum_usage_examples.py algorithms   # All 51+ algorithm demos
python quantum_usage_examples.py --list       # Show all options
```

---

## All 51+ Algorithms

### A. Core API-Routable Algorithms (`POST /api/v1/quantum/execute`)

| # | Algorithm | Description | Best For |
|---|-----------|-------------|----------|
| 1 | **VQE** | Variational Quantum Eigensolver | Energy minimization, ground states |
| 2 | **QAOA** | Quantum Approximate Optimization | Combinatorial optimization |
| 3 | **HHL** | Harrow-Hassidim-Lloyd | Linear systems Ax=b |
| 4 | **Grover** | Grover Search | Unstructured search O(√N) |

### B. QAOA Variants (via `qaoa_variant` field)

| # | Variant | Description |
|---|---------|-------------|
| 5 | Standard QAOA | Fixed p-layer schedule |
| 6 | Adaptive QAOA | Dynamically adds layers until convergence |
| 7 | Continuous QAOA | Continuous-time quantum walk formulation |
| 8 | Multi-Angle QAOA | Independent angle per constraint |
| 9 | Warm-Start QAOA | Initialized from classical relaxation |

### C. VQE Advanced Optimizers (`POST /api/v1/quantum/optimizer/run`)

| # | Optimizer | Description |
|---|-----------|-------------|
| 10 | SPSA | Simultaneous Perturbation Stochastic Approximation |
| 11 | CMAES | Covariance Matrix Adaptation Evolution Strategy |
| 12 | L-BFGS-B | Limited-memory Broyden-Fletcher-Goldfarb-Shanno |
| 13 | ADAM | Adaptive Moment Estimation |
| 14 | COBYLA | Constrained Optimization by Linear Approximation |
| 15 | QNG | Quantum Natural Gradient |
| 16 | Rotosolve | Analytical parameter rotation |
| 17 | Nelder-Mead | Simplex direct search |

### D. VQE Ansatz Types (via `ansatz` field)

| # | Ansatz | Description |
|---|--------|-------------|
| 18 | UCCSD | Unitary Coupled Cluster Singles & Doubles |
| 19 | Qubit-Adapt VQE | Iteratively grows operator pool |
| 20 | Symmetry-Preserving | Respects system symmetries |
| 21 | Hardware-Efficient | Shallow circuit, native gates |
| 22 | LDCA | Low-Depth Circuit Ansatz |

### E. Error Mitigation Algorithms (via `mitigation_method` field)

| # | Method | Description |
|---|--------|-------------|
| 23 | ZNE | Zero Noise Extrapolation (Richardson) |
| 24 | PEC | Probabilistic Error Cancellation |
| 25 | Virtual Distillation | Multi-copy purification |
| 26 | CDR | Clifford Data Regression |
| 27 | Readout Mitigation | Measurement error correction |

### F. Quantum Simulation

| # | Algorithm | Endpoint | Description |
|---|-----------|----------|-------------|
| 28 | VQS Time Evolution | `POST /api/v1/quantum/vqs/evolve` | Variational quantum simulation |
| 29 | Lindblad Solver | `POST /api/v1/quantum/execute` | Open quantum system dynamics |
| 30 | Quantum Monte Carlo | `POST /api/v1/quantum/execute` | Projector/diffusion MC |

### G. Auto-Selected by Orchestration (`algorithm: "auto"` or omitted)

| # | Algorithm | Auto-Selected When |
|---|-----------|-------------------|
| 31 | QPE | Phase estimation / eigenvalue problems |
| 32 | QFT | Frequency analysis / Fourier transforms |
| 33 | Shor | Integer factoring |
| 34 | Boson Sampling | Photonic quantum advantage |
| 35 | Gaussian Boson Sampling | Molecular vibronic spectra |
| 36 | Conformal Field Theory | Critical systems |
| 37 | Renormalization Group | Scale-dependent physics |
| 38 | Quantum Thermodynamics | Partition functions, free energy |
| 39 | Quantum Metrology | Heisenberg-limited sensing |
| 40 | Measurement-Based QC | Cluster-state computation |

### H. Numerical/Scientific Algorithms

| # | Algorithm | Description |
|---|-----------|-------------|
| 41 | PDE Solvers | FDM, FEM, FVM for fluid/heat/structural |
| 42 | SINDy | Sparse Identification of Nonlinear Dynamics |
| 43 | Uncertainty Quantification | Bayesian, Monte Carlo, Polynomial Chaos |

### I. Machine Learning Algorithms

| # | Algorithm | Description |
|---|-----------|-------------|
| 44 | QNN | Quantum Neural Networks (variational classifier) |
| 45 | QPINN | Quantum Physics-Informed Neural Networks |
| 46 | Quantum Kernel Methods | Projected quantum kernel SVM |

### J. Advanced Quantum Algorithms

| # | Algorithm | Description |
|---|-----------|-------------|
| 47 | Belief Propagation | Quantum message passing on factor graphs |
| 48 | Knowledge Compilation | Boolean to quantum circuit compilation |
| 49 | Circuit Optimization | Gate synthesis and simplification |
| 50 | Quantum Error Correction | Surface code decoding |
| 51 | Quantum Teleportation | Multi-qubit state transfer protocol |

---

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/quantum/status` | Engine status |
| `GET` | `/api/v1/quantum/domains` | List available domains |
| `POST` | `/api/v1/quantum/execute` | **Execute quantum computation** (all algorithms) |
| `POST` | `/api/v1/quantum/optimizer/run` | VQE optimizer loop (Section C) |
| `POST` | `/api/v1/quantum/vqs/evolve` | VQS time evolution (Section F) |
| `POST` | `/api/v1/quantum/pipeline/execute` | Full L1→L2→L3 pipeline |
| `POST` | `/api/v1/multidimensional/query` | Multidimensional range query |

### Data Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Register new user |
| `POST` | `/api/v1/auth/login` | Login (returns JWT) |
| `POST` | `/api/v1/query` | Execute SQL query |
| `POST` | `/api/v1/bulk-import` | Bulk data import |

---

## Algorithm Categories (A–J)

### A. Core Algorithms — Request Examples

```json
// VQE (default)
{"domain": "chemistry", "algorithm": "vqe", "molecule": "hemoglobin", "atoms": 8738, "input_data": [...]}

// QAOA
{"domain": "finance", "algorithm": "qaoa", "problem_type": "portfolio_optimization", "num_assets": 65536, "input_data": [...]}

// HHL
{"domain": "mathematics", "algorithm": "hhl", "problem_type": "linear_system", "matrix_size": 65536, "input_data": [...]}

// Grover
{"domain": "core_gates", "algorithm": "grover", "search_space_size": 65536, "target_states": [42, 1337], "input_data": [...]}
```

### B. QAOA Variants

```json
{"domain": "finance", "algorithm": "qaoa", "qaoa_variant": "standard", "p_layers": 8, "input_data": [...]}
{"domain": "logistics", "algorithm": "qaoa", "qaoa_variant": "adaptive", "max_layers": 20, "input_data": [...]}
{"domain": "finance", "algorithm": "qaoa", "qaoa_variant": "continuous", "time_limit": 5.0, "input_data": [...]}
{"domain": "logistics", "algorithm": "qaoa", "qaoa_variant": "multi_angle", "angles_per_layer": 4, "input_data": [...]}
{"domain": "finance", "algorithm": "qaoa", "qaoa_variant": "warm_start", "classical_solution": "greedy_relaxation", "input_data": [...]}
```

### C. VQE Optimizers (`POST /api/v1/quantum/optimizer/run`)

```json
{"domain": "chemistry", "algorithm": "vqe", "optimizer": "spsa", "max_iterations": 500, "input_data": [...]}
{"domain": "chemistry", "algorithm": "vqe", "optimizer": "cmaes", "max_iterations": 500, "input_data": [...]}
{"domain": "chemistry", "algorithm": "vqe", "optimizer": "l_bfgs_b", "max_iterations": 500, "input_data": [...]}
{"domain": "chemistry", "algorithm": "vqe", "optimizer": "adam", "max_iterations": 500, "input_data": [...]}
{"domain": "chemistry", "algorithm": "vqe", "optimizer": "cobyla", "max_iterations": 500, "input_data": [...]}
{"domain": "chemistry", "algorithm": "vqe", "optimizer": "qng", "max_iterations": 500, "input_data": [...]}
{"domain": "chemistry", "algorithm": "vqe", "optimizer": "rotosolve", "max_iterations": 500, "input_data": [...]}
{"domain": "chemistry", "algorithm": "vqe", "optimizer": "nelder_mead", "max_iterations": 500, "input_data": [...]}
```

### D. VQE Ansatz Types

```json
{"algorithm": "vqe", "ansatz": "uccsd", "excitation_order": "singles_doubles", "input_data": [...]}
{"algorithm": "vqe", "ansatz": "qubit_adapt", "operator_pool": "full_pauli", "input_data": [...]}
{"algorithm": "vqe", "ansatz": "symmetry_preserving", "symmetry_sector": "zero_magnetization", "input_data": [...]}
{"algorithm": "vqe", "ansatz": "hardware_efficient", "circuit_depth": 6, "input_data": [...]}
{"algorithm": "vqe", "ansatz": "ldca", "input_data": [...]}
```

### E. Error Mitigation

```json
{"mitigation_method": "zne", "noise_factors": [1.0, 1.5, 2.0, 2.5, 3.0], "extrapolation": "richardson", "input_data": [...]}
{"mitigation_method": "pec", "num_calibration_circuits": 256, "input_data": [...]}
{"mitigation_method": "virtual_distillation", "num_copies": 3, "input_data": [...]}
{"mitigation_method": "cdr", "num_training_circuits": 100, "input_data": [...]}
{"mitigation_method": "readout_mitigation", "calibration_shots": 8192, "input_data": [...]}
```

### F. Quantum Simulation

```json
// VQS Time Evolution (POST /api/v1/quantum/vqs/evolve)
{"num_sites": 65536, "time_steps": 50, "dt_seconds": 0.02, "hamiltonian": "heisenberg_xxz", "input_data": [...]}

// Lindblad Solver
{"simulation_type": "lindblad", "dissipation_rate": 0.01, "lindblad_operators": ["sigma_minus"], "input_data": [...]}

// Quantum Monte Carlo
{"simulation_type": "quantum_monte_carlo", "num_walkers": 10000, "projection_time": 20.0, "input_data": [...]}
```

### G. Auto-Selected Algorithms

```json
// Engine picks the best algorithm automatically
{"domain": "chemistry", "algorithm": "auto", "problem_type": "phase_estimation", "input_data": [...]}
{"domain": "mathematics", "algorithm": "auto", "problem_type": "integer_factoring", "number_to_factor": 18446744073709551557, "input_data": [...]}
{"domain": "physics", "algorithm": "auto", "problem_type": "boson_sampling", "num_modes": 65536, "input_data": [...]}
```

### H. Numerical/Scientific

```json
// PDE Solvers
{"problem_type": "pde_solver", "pde_method": "fdm", "equation": "navier_stokes_2d", "grid_size": [256, 256], "input_data": [...]}
{"problem_type": "pde_solver", "pde_method": "fem", "equation": "heat_equation_3d", "num_elements": 65536, "input_data": [...]}
{"problem_type": "pde_solver", "pde_method": "fvm", "equation": "euler_equations", "num_cells": 65536, "input_data": [...]}

// SINDy
{"problem_type": "sindy", "time_series_length": 65536, "sparsity_threshold": 0.01, "input_data": [...]}

// Uncertainty Quantification
{"problem_type": "uncertainty_quantification", "uq_method": "polynomial_chaos", "samples": 65536, "input_data": [...]}
```

### I. Machine Learning

```json
{"problem_type": "qnn", "num_features": 65536, "num_layers": 12, "input_data": [...]}
{"problem_type": "qpinn", "physics_equation": "schrodinger", "num_collocation_points": 65536, "input_data": [...]}
{"problem_type": "quantum_kernel", "kernel_type": "projected_quantum", "num_features": 65536, "input_data": [...]}
```

### J. Advanced Quantum

```json
{"problem_type": "belief_propagation", "num_variables": 65536, "factor_graph_type": "ising", "input_data": [...]}
{"problem_type": "knowledge_compilation", "num_variables": 65536, "target_representation": "obdd", "input_data": [...]}
{"problem_type": "circuit_optimization", "circuit_gates": 65536, "optimization_level": 3, "input_data": [...]}
{"problem_type": "quantum_error_correction", "code_type": "surface_code", "code_distance": 7, "input_data": [...]}
{"problem_type": "quantum_teleportation", "num_qubits_to_teleport": 65536, "input_data": [...]}
```

---

## All 16 Quantum Domains

### 1. Chemistry
```json
{"domain": "chemistry", "algorithm": "vqe", "molecule": "hemoglobin", "atoms": 8738, "basis_set": "STO-6G", "input_data": [...]}
```

### 2. Physics
```json
{"domain": "physics", "algorithm": "vqe", "model": "heisenberg_xxz", "lattice_size": 256, "input_data": [...]}
```

### 3. Finance
```json
{"domain": "finance", "algorithm": "qaoa", "problem_type": "portfolio_optimization", "num_assets": 65536, "input_data": [...]}
```

### 4. Materials Science
```json
{"domain": "materials_science", "algorithm": "vqe", "material": "YBCO", "lattice_atoms": 65536, "input_data": [...]}
```

### 5. Biomolecules
```json
{"domain": "biomolecules", "algorithm": "vqe", "problem_type": "protein_folding", "protein": "hemoglobin_tetramer", "input_data": [...]}
```

### 6. Machine Learning
```json
{"domain": "machine_learning", "algorithm": "vqe", "problem_type": "quantum_kernel_svm", "num_features": 65536, "input_data": [...]}
```

### 7. Logistics
```json
{"domain": "logistics", "algorithm": "qaoa", "problem_type": "vehicle_routing", "num_nodes": 65536, "input_data": [...]}
```

### 8. Nuclear
```json
{"domain": "nuclear", "algorithm": "vqe", "nucleus": "uranium-238", "protons": 92, "neutrons": 146, "input_data": [...]}
```

### 9. Mathematics
```json
{"domain": "mathematics", "algorithm": "hhl", "problem_type": "linear_system", "matrix_size": 65536, "input_data": [...]}
```

### 10. Error Mitigation
```json
{"domain": "error_mitigation", "mitigation_method": "zne", "noise_factors": [1.0, 1.5, 2.0, 2.5, 3.0], "input_data": [...]}
```

### 11. Graphics
```json
{"domain": "graphics", "algorithm": "grover", "problem_type": "ray_tracing", "resolution": [256, 256], "input_data": [...]}
```

### 12. Real-Time
```json
{"domain": "real_time", "problem_type": "state_evolution", "num_sites": 65536, "input_data": [...]}
```

### 13. Fluid Mechanics
```json
{"domain": "fluid_mechanics", "problem_type": "navier_stokes", "grid_size": [256, 256], "reynolds_number": 1000, "input_data": [...]}
```

### 14. Turbulence CFD
```json
{"domain": "turbulence_cfd", "problem_type": "dns_turbulence", "grid_points": 65536, "reynolds_number": 10000, "input_data": [...]}
```

### 15. Heat Transfer
```json
{"domain": "heat_transfer", "algorithm": "hhl", "problem_type": "conduction", "grid_size": [256, 256], "input_data": [...]}
```

### 16. Core Gates
```json
{"domain": "core_gates", "algorithm": "grover", "problem_type": "quantum_search", "search_space_size": 65536, "input_data": [...]}
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NAWAZ1_HOST` | `0.0.0.0` | Server bind address |
| `NAWAZ1_PORT` | `8080` | Server port |
| `NAWAZ1_TIER` | `free` | Tier: `free`, `pro`, `enterprise` |
| `NAWAZ1_API_KEY` | *(unset)* | When set, requires `X-API-Key` header |
| `RUST_LOG` | `info` | Log verbosity |
| `JWT_SECRET` | *(auto)* | Secret for JWT token signing |

---

## Data Import Guide

### Register & Login

```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"myuser","password":"MyPass123!","email":"me@example.com"}'

curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"myuser","password":"MyPass123!"}'
```

### Bulk Import

```bash
curl -X POST http://localhost:8080/api/v1/bulk-import \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "table": "experiments",
    "columns": ["id", "domain", "energy", "fidelity"],
    "rows": [[1,"chemistry",-4532.7,0.999],[2,"physics",-1783.2,0.999]]
  }'
```

---

## Authentication & Security

### API Key Mode

```bash
NAWAZ1_API_KEY=my-secret-key-123 ./nawaz1-server

curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "X-API-Key: my-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"domain":"chemistry","algorithm":"vqe","input_data":[...]}'
```

### JWT Authentication (for data operations)

```bash
TOKEN=$(curl -s -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.token')

curl -X POST http://localhost:8080/api/v1/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT * FROM experiments"}'
```

---

## Running the Examples

### Files in this repository

| File | Description |
|------|-------------|
| `quantum_usage_examples.py` | **All 51+ algorithms** at 65536-qubit scale (Python + numpy) |
| `data_import_examples.py` | Auth, tables, import, query (Python) |
| `run_all_demos.sh` | Demo runner (Bash) |
| `run_all_demos.ps1` | Demo runner (PowerShell) |
| `README.md` | This documentation |

### Run Individual Sections

```bash
python quantum_usage_examples.py --list              # Show all options
python quantum_usage_examples.py algorithms          # All 51+ algorithms
python quantum_usage_examples.py algorithms_core     # Section A only
python quantum_usage_examples.py algorithms_qaoa     # Section B only
python quantum_usage_examples.py algorithms_optimizers  # Section C only
python quantum_usage_examples.py chemistry           # Single domain
```

### Expected Response Format

```json
{
  "success": true,
  "domain": "chemistry",
  "algorithm": "vqe",
  "result": {
    "energy": -4532.7183,
    "converged": true,
    "iterations": 120,
    "fidelity": 0.9998,
    "num_qubits": 65536,
    "gate_count": 524288
  },
  "metadata": {
    "execution_time_ms": 45.2,
    "tier": "free",
    "input_amplitudes": 65536
  }
}
```

---

## Support

- **Issues:** https://github.com/shah786628/nawaz1-quantum-software/issues
- **Author:** Shahnawaz Alam
