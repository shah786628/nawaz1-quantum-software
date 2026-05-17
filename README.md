# Nawaz1 Quantum VQE Engine - Usage Guide

> **Multidimensional L6→L3 Quantum Pipeline** — A production-grade quantum VQE engine supporting 16 domains, **62 algorithms across 13 categories**, data persistence, and real-time streaming.

**Author:** Shahnawaz Alam  
**License:** Proprietary  
**Copyright (c) 2026 Shahnawaz Alam. All rights reserved.**

---

## How Qubit Count Works (Amplitude Encoding)

The VQE engine uses **amplitude encoding**: the number of qubits is determined by the **input data length**, not a forced parameter.

```
num_qubits = input_data.len().next_power_of_two()
```

For **65536 qubits**, you must provide **65536 amplitude values** in the `input_data` array. Each value represents one amplitude in a 65536-dimensional Hilbert space.

| Domain | Problem Scale for 65536 Qubits |
|--------|-------------------------------|
| Chemistry | Hemoglobin protein (8738 atoms, 65536 orbital amplitudes) |
| Physics | 256×256 Heisenberg lattice (65536 sites) |
| Finance | 65536 financial instruments (global portfolio) |
| Materials | 65536-atom YBCO superconductor crystal |
| Biomolecules | Hemoglobin tetramer (4532 atoms, 65536 conformations) — **14 sub-modules** |
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

## Biomolecules Domain — 14 Quantum Biology Sub-Modules

The **biomolecules** domain contains 14 specialized sub-modules (~460 KB total) providing comprehensive quantum biology coverage:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **DNA/RNA** | Nucleotide base encoding, Watson-Crick pairing, hybridization thermodynamics |
| 2 | **Drug Discovery** | Lipinski's Rule of Five, Veber rules, Ghose filter, QED scoring |
| 3 | **Enzyme Catalysis** | Michaelis-Menten kinetics, inhibition types, diffusion-limited catalysis |
| 4 | **Glycobiology** | Monosaccharide classification, glycosidic bonds, lectin binding |
| 5 | **Membrane Biophysics** | Ion channels, Nernst/Goldman equations, membrane potential |
| 6 | **Metabolic Networks** | Flux balance analysis, Gibbs free energy, compartment modeling |
| 7 | **Molecular Dynamics** | Force fields (AMBER/CHARMM), Lennard-Jones, Coulomb, trajectory integration |
| 8 | **Neurochemistry** | 10 neurotransmitter types, receptor binding, synaptic dynamics |
| 9 | **Photosynthesis** | Chromophore types, quantum yield, exciton energy transfer |
| 10 | **Protein Folding** | 20 amino acids, Ramachandran analysis, energy landscapes |
| 11 | **Protein-Protein Interactions** | Interface properties, SASA, binding free energy |
| 12 | **Quantum Virology** | Capsid geometry, icosahedral symmetry, T-number classification |
| 13 | **Structural Biology** | X-ray scattering factors, structure factor calculations |
| 14 | **Systems Biology** | Hill functions, gene regulatory networks, cooperativity |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/biology/README.md`](packages/biology/README.md) for full API documentation per sub-module.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "drug_discovery", "task": "drug_likeness" }
}
```

**Demo endpoint:** `POST /api/v1/quantum/biomolecules/demo`

---

## Table of Contents

- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Complete Algorithm Reference (62 Algorithms)](#complete-algorithm-reference-62-algorithms)
- [Algorithm Summary Table](#algorithm-summary-table)
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

# Generate 65536 molecular orbital amplitudes for hemoglobin
rng = np.random.RandomState(42)
data = rng.normal(0, 1, 65536)
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
python quantum_usage_examples.py              # Run all 62 algorithms
python quantum_usage_examples.py --list       # List all categories
python quantum_usage_examples.py vqe_family   # Run single category
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NAWAZ1_HOST` | `0.0.0.0` | Server bind address |
| `NAWAZ1_PORT` | `8080` | Server port |
| `NAWAZ1_TIER` | `free` | Tier: `free`, `pro`, `enterprise` |
| `NAWAZ1_API_KEY` | *(unset)* | When set, requires `X-API-Key` header on all quantum endpoints |
| `RUST_LOG` | `info` | Log verbosity: `error`, `warn`, `info`, `debug`, `trace` |
| `JWT_SECRET` | *(auto)* | Secret for JWT token signing |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/quantum/status` | Engine status (qubits, memory, tier) |
| `GET` | `/api/v1/quantum/domains` | List available domains |
| `POST` | `/api/v1/quantum/execute` | **Execute quantum computation** |
| `POST` | `/api/v1/quantum/optimizer/run` | Run VQE with specific optimizer |
| `POST` | `/api/v1/quantum/vqs/evolve` | VQS time evolution |
| `POST` | `/api/v1/quantum/pipeline/execute` | Full L1→L2→L3 pipeline |
| `POST` | `/api/v1/multidimensional/query` | Multidimensional range query |

---

## Complete Algorithm Reference (62 Algorithms)

**ARCHITECTURAL KEY POINT:** All algorithms route through the **Algorithm Bridge → execute_l3()** on the pre-built VQE circuit substrate. The `algorithm` field is metadata for orchestration — execution always goes through the same unified L3 parametric circuit. Only the parameter vector changes.

---

### Category A: VQE Family (8 variants)

The core variational quantum eigensolver and its specialized variants.

| # | Algorithm | Description | When to Use | Key Fields |
|---|-----------|-------------|-------------|------------|
| A1 | Standard VQE | Variational ground-state energy solver | Default for energy minimization | `"algorithm": "vqe"` |
| A2 | ADAPT-VQE | Iteratively grows ansatz from operator pool | When circuit depth must be minimized | `"algorithm": "adapt_vqe"` |
| A3 | Subspace VQE | Solves multiple eigenstates simultaneously | Excited states, spectroscopy | `"algorithm": "subspace_vqe", "num_eigenstates": 6` |
| A4 | Hardware-Aware VQE | Circuit adapted to device connectivity | Noisy hardware deployment | `"algorithm": "hardware_aware_vqe", "topology": "heavy_hex"` |
| A5 | VQE + Measurement Reduction | Fewer shots via Pauli grouping | Large Hamiltonians (many terms) | `"algorithm": "vqe_measurement_reduction"` |
| A6 | VQE + Quantum Fisher | Natural gradient using Fisher information | Barren plateau avoidance | `"algorithm": "vqe_quantum_fisher"` |
| A7 | VQE + Error Mitigation | Built-in noise correction | Noisy intermediate-scale | `"algorithm": "vqe_error_mitigated", "mitigation": "zne"` |
| A8 | VQE + Advanced Optimizer | Meta-learned optimization | Fast convergence on new molecules | `"algorithm": "vqe_advanced_optimizer"` |

---

### Category B: VQE Advanced Optimizers (6)

Classical optimizers that drive the VQE variational loop. Use endpoint `/api/v1/quantum/optimizer/run`.

| # | Optimizer | Description | When to Use |
|---|-----------|-------------|-------------|
| B1 | SPSA | Simultaneous Perturbation Stochastic Approximation | Noisy cost functions, hardware |
| B2 | CMA-ES | Covariance Matrix Adaptation Evolution Strategy | Global optimization, few parameters |
| B3 | L-BFGS-B | Limited-memory BFGS with box constraints | Smooth landscapes, many parameters |
| B4 | QNG | Quantum Natural Gradient (Fisher metric) | Avoiding barren plateaus |
| B5 | Rotosolve | Analytical single-parameter rotation | Rz/Ry gates, exact 1D minima |
| B6 | Nelder-Mead | Simplex direct search (derivative-free) | Non-differentiable landscapes |

```json
{"algorithm": "vqe", "optimizer": "qng", "max_iterations": 500}
```

---

### Category C: VQE Advanced Ansätze (5)

Parametric circuit structures for the VQE substrate.

| # | Ansatz | Description | When to Use |
|---|--------|-------------|-------------|
| C1 | UCCSD | Unitary Coupled Cluster Singles & Doubles | Chemistry (gold standard) |
| C2 | QubitAdapt-VQE | Iteratively grows qubit operator pool | Minimal circuit depth |
| C3 | Symmetry-Preserving | Respects molecular/system symmetries | Symmetry-constrained problems |
| C4 | k-UpCCGSD | k-fold Unitary pair Coupled Cluster GSD | Strongly correlated systems |
| C5 | LDCA | Low-Depth Circuit Ansatz (log-depth) | Hardware with limited coherence |

```json
{"algorithm": "vqe", "ansatz": "uccsd", "excitation_order": "singles_doubles"}
```

---

### Category D: QAOA Variants (5)

Quantum Approximate Optimization Algorithm variants for combinatorial problems.

| # | Variant | Description | When to Use |
|---|---------|-------------|-------------|
| D1 | Standard QAOA | Fixed p-layer mixer/cost schedule | General combinatorial optimization |
| D2 | Adaptive QAOA | Dynamically adds layers until convergence | Unknown optimal depth |
| D3 | Continuous QAOA | Continuous-time quantum walk formulation | Time-continuous cost functions |
| D4 | Multi-Angle QAOA | Independent angle per constraint | Problems with many constraints |
| D5 | Warm-Start QAOA | Initialized from classical relaxation | When classical approximation exists |

```json
{"algorithm": "qaoa", "qaoa_variant": "adaptive", "max_layers": 20}
```

---

### Category E: HHL Family (4)

Quantum linear algebra algorithms with exponential speedup for sparse systems.

| # | Algorithm | Description | When to Use |
|---|-----------|-------------|-------------|
| E1 | Standard HHL | Harrow-Hassidim-Lloyd for Ax=b | Sparse well-conditioned systems |
| E2 | Preconditioned HHL | Better conditioned linear solve | Ill-conditioned matrices |
| E3 | QSVT | Quantum Singular Value Transformation | General matrix functions |
| E4 | Quantum Regression | Quantum-enhanced least squares | Regression/fitting |

```json
{"algorithm": "qsvt", "problem_type": "matrix_function", "function": "matrix_inversion"}
```

---

### Category F: Grover Search (1)

| # | Algorithm | Description | When to Use |
|---|-----------|-------------|-------------|
| F1 | Grover Search | O(√N) unstructured quantum search | Unstructured search, database queries |

```json
{"algorithm": "grover", "search_space_size": 65536, "target_states": [42, 1337]}
```

---

### Category G: Error Mitigation (5)

Post-processing techniques to reduce noise in quantum results.

| # | Method | Description | When to Use |
|---|--------|-------------|-------------|
| G1 | ZNE | Zero-Noise Extrapolation (Richardson) | General noise reduction |
| G2 | PEC | Probabilistic Error Cancellation | Known noise model |
| G3 | Virtual Distillation | Multi-copy state purification | High-fidelity required |
| G4 | CDR | Clifford Data Regression | Near-Clifford circuits |
| G5 | Readout Mitigation | Measurement error correction | Readout-dominated noise |

```json
{"mitigation_method": "zne", "noise_factors": [1.0, 1.5, 2.0, 2.5, 3.0]}
```

---

### Category H: Measurement Reduction (3)

Reduce measurement overhead for expectation value estimation.

| # | Method | Description | When to Use |
|---|--------|-------------|-------------|
| H1 | Term Grouper | Groups commuting Pauli terms | Large Hamiltonians |
| H2 | Classical Shadow | Randomized measurements for many observables | Many observables simultaneously |
| H3 | Adaptive Shot Allocator | Variance-aware shot budget distribution | Fixed shot budget optimization |

```json
{"measurement_strategy": "classical_shadow", "num_shadows": 10000}
```

---

### Category I: Numerical/Scientific Solvers (7)

PDE solvers and scientific computing on the L3 quantum substrate.

| # | Method | Description | When to Use |
|---|--------|-------------|-------------|
| I1 | FDM | Finite Difference Method | Structured grids, simple domains |
| I2 | FEM | Finite Element Method | Complex geometries, unstructured mesh |
| I3 | FVM | Finite Volume Method | Conservation laws, compressible flow |
| I4 | IMEX | Implicit-Explicit time stepping | Stiff reaction-diffusion systems |
| I5 | Multigrid | Hierarchical elliptic PDE solver | Elliptic equations, fast convergence |
| I6 | PDE General | General quantum-accelerated PDE framework | Heat/wave/diffusion equations |
| I7 | SINDy | Sparse Identification of Nonlinear Dynamics | Data-driven model discovery |

```json
{"problem_type": "pde_solver", "pde_method": "fem", "equation": "heat_equation_3d"}
```

---

### Category J: Specialized Quantum (5)

Domain-specific quantum primitives and algorithms.

| # | Algorithm | Description | When to Use |
|---|-----------|-------------|-------------|
| J1 | QFT | Quantum Fourier Transform | Frequency analysis, phase kickback |
| J2 | QPE | Quantum Phase Estimation | Eigenvalue extraction |
| J3 | Quantum Monte Carlo | Projector/diffusion Monte Carlo | Ground states of lattice models |
| J4 | Belief Propagation | Quantum message passing on factor graphs | Graphical model inference |
| J5 | Knowledge Compilation | Boolean function to quantum circuit | Circuit synthesis |

```json
{"algorithm": "qpe", "problem_type": "phase_estimation", "precision_bits": 16}
```

---

### Category K: Condensed Matter (4)

Lattice quantum many-body models at scale.

| # | Model | Description | When to Use |
|---|-------|-------------|-------------|
| K1 | Heisenberg | XXZ antiferromagnet on square lattice | Magnetic materials |
| K2 | Hubbard | Strongly correlated electron model | High-Tc superconductors |
| K3 | Ising | Transverse-field quantum spin chain | Phase transitions |
| K4 | Lattice Gauge Theory | SU(3) gauge field on lattice | QCD, nuclear physics |

```json
{"problem_type": "condensed_matter", "model": "hubbard", "hopping_t": 1.0, "interaction_u": 4.0}
```

---

### Category L: Time Evolution (3)

Quantum dynamics simulation algorithms.

| # | Algorithm | Description | When to Use |
|---|-----------|-------------|-------------|
| L1 | VQS | Variational Quantum Simulation (McLachlan) | Real-time dynamics |
| L2 | TEBD | Time-Evolving Block Decimation (MPS) | 1D systems, long times |
| L3 | QITE | Quantum Imaginary Time Evolution | Ground state preparation, thermal states |

```json
// VQS endpoint:
POST /api/v1/quantum/vqs/evolve
{"num_sites": 65536, "time_steps": 50, "dt_seconds": 0.02, "hamiltonian": "heisenberg_xxz"}
```

---

### Category M: Advanced Quantum (6)

Cutting-edge quantum algorithms for specialized applications.

| # | Algorithm | Description | When to Use |
|---|-----------|-------------|-------------|
| M1 | Shor's Algorithm | Integer factorization (exponential speedup) | Cryptanalysis, number theory |
| M2 | Quantum Lindblad Solver | Open quantum system dynamics | Decoherence, dissipation |
| M3 | Quantum Thermodynamics | Partition function & free energy | Thermal equilibrium properties |
| M4 | Quantum Metrology | Heisenberg-limited parameter estimation | Precision sensing |
| M5 | QNN | Quantum Neural Network (variational classifier) | Classification, generative models |
| M6 | QPINN | Quantum Physics-Informed Neural Network | PDE solving with physics constraints |

```json
{"algorithm": "shor", "problem_type": "integer_factoring", "number_to_factor": 18446744073709551557}
```

---

## Algorithm Summary Table

| Category | Count | Algorithms |
|----------|-------|------------|
| A. VQE Family | 8 | Standard, ADAPT, Subspace, Hardware-Aware, Measurement Reduction, Quantum Fisher, Error Mitigated, Advanced Optimizer |
| B. VQE Optimizers | 6 | SPSA, CMA-ES, L-BFGS-B, QNG, Rotosolve, Nelder-Mead |
| C. VQE Ansätze | 5 | UCCSD, QubitAdapt, Symmetry-Preserving, k-UpCCGSD, LDCA |
| D. QAOA Variants | 5 | Standard, Adaptive, Continuous, Multi-Angle, Warm-Start |
| E. HHL Family | 4 | Standard HHL, Preconditioned HHL, QSVT, Quantum Regression |
| F. Grover | 1 | Grover Search |
| G. Error Mitigation | 5 | ZNE, PEC, Virtual Distillation, CDR, Readout Mitigation |
| H. Measurement Reduction | 3 | Term Grouper, Classical Shadow, Adaptive Shot Allocator |
| I. Numerical/Scientific | 7 | FDM, FEM, FVM, IMEX, Multigrid, PDE General, SINDy |
| J. Specialized Quantum | 5 | QFT, QPE, Quantum Monte Carlo, Belief Propagation, Knowledge Compilation |
| K. Condensed Matter | 4 | Heisenberg, Hubbard, Ising, Lattice Gauge Theory |
| L. Time Evolution | 3 | VQS, TEBD, QITE |
| M. Advanced Quantum | 6 | Shor, Lindblad Solver, Thermodynamics, Metrology, QNN, QPINN |
| **TOTAL** | **62** | |

---

## Data Import Guide

### 1. Register & Login

```bash
# Register
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"myuser","password":"MyPass123!","email":"me@example.com"}'

# Login (get JWT token)
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"myuser","password":"MyPass123!"}'
```

### 2. Create Table & Insert

```bash
curl -X POST http://localhost:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query":"CREATE TABLE experiments (id INT, domain TEXT, energy REAL, fidelity REAL)"}'
```

### 3. Bulk Import

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

When `NAWAZ1_API_KEY` is set, all quantum endpoints require `X-API-Key` header:

```bash
NAWAZ1_API_KEY=my-secret-key-123 ./nawaz1-server

curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "X-API-Key: my-secret-key-123" \
  -d '{"domain":"chemistry","algorithm":"vqe","input_data":[...]}'
```

### JWT Authentication

For data operations (query, import), use JWT tokens obtained from `/api/v1/auth/login`.

---

## Running the Examples

### Files in this repository

| File | Description |
|------|-------------|
| `quantum_usage_examples.py` | All **62 algorithms** at 65536-qubit scale (Python + numpy) |
| `data_import_examples.py` | Auth, tables, import, query (Python) |
| `run_all_demos.sh` | Full demo runner (Bash) |
| `run_all_demos.ps1` | Full demo runner (PowerShell) |
| `README.md` | This documentation |

### Prerequisites

- **Server:** nawaz1-server binary running
- **Python:** 3.8+ with `numpy` and `requests` (`pip install numpy requests`)

### Run Individual Categories

```bash
python quantum_usage_examples.py vqe_family          # Category A
python quantum_usage_examples.py vqe_optimizers      # Category B
python quantum_usage_examples.py vqe_ansatz          # Category C
python quantum_usage_examples.py qaoa_variants       # Category D
python quantum_usage_examples.py hhl_family          # Category E
python quantum_usage_examples.py grover              # Category F
python quantum_usage_examples.py error_mitigation    # Category G
python quantum_usage_examples.py measurement_reduction  # Category H
python quantum_usage_examples.py numerical_solvers   # Category I
python quantum_usage_examples.py specialized_quantum # Category J
python quantum_usage_examples.py condensed_matter    # Category K
python quantum_usage_examples.py time_evolution      # Category L
python quantum_usage_examples.py advanced_quantum    # Category M
python quantum_usage_examples.py algorithms          # ALL categories
python quantum_usage_examples.py --list              # Show all options
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
