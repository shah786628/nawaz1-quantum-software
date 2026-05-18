# Nawaz1 Quantum VQE Engine - Usage Guide

> **Multidimensional L6→L3 Quantum Pipeline** — A production-grade quantum VQE engine supporting 15 domains, **62 algorithms across 13 categories**, data persistence, and real-time streaming.

**Author:** Shahnawaz Alam  
**License:** Proprietary  
**Copyright (c) 2026 Shahnawaz Alam. All rights reserved.**

---

> **⚠️ IMPORTANT — Hardware Security Requirements for Launch**
>
> This software **MUST** be launched on a **Linux VM** with a CPU that supports at least one of the following hardware security extensions:
>
> | Technology | Vendor | Minimum Requirement |
> |-----------|--------|-------------------|
> | **Intel TDX** | Intel | Trust Domain Extensions — 4th Gen Xeon (Sapphire Rapids) or newer |
> | **AMD SEV-SNP** | AMD | Secure Encrypted Virtualization — EPYC 7003 (Milan) or newer |
> | **Intel SGX** | Intel | Software Guard Extensions — 6th Gen Core or Xeon E3 v6+ |
>
> **Why?** The quantum engine uses hardware-isolated trusted execution environments (TEEs) for:
> - Protecting quantum state data in memory (encrypted RAM)
> - Secure key management and rotation
> - Side-channel attack resistance
> - Tamper-proof execution of quantum algorithms
>
> **Verification:** Run `dmesg | grep -i "tdx\|sev\|sgx"` to check hardware support.
>
> Launching on unsupported hardware will result in degraded security posture.

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
| Physics | 256×256 Heisenberg lattice (65536 sites) — **13 sub-modules** |
| Finance | 65536 financial instruments (global portfolio) |
| Materials | 65536-atom YBCO superconductor crystal |
| Biomolecules | Hemoglobin tetramer (4532 atoms, 65536 conformations) — **14 sub-modules** |
| Machine Learning | 65536-feature quantum kernel SVM |
| Logistics | 65536-node global supply chain |
| Mathematics | 65536×65536 sparse linear system — **11 sub-modules** |
| Error Mitigation | 65536-amplitude noisy state correction |
| Graphics | 256×256 = 65536-pixel quantum ray tracing |
| Real-Time | 65536-site quantum state evolution |
| Fluid Mechanics | 256×256 Navier-Stokes grid (65536 points) |
| Turbulence CFD | 65536-point DNS turbulence (Re=10000) |
| Heat Transfer | 256×256 thermal conduction grid (65536 nodes) |
| Core Gates | 65536-qubit quantum Fourier transform |
| SDK | Python, C++, Rust, Julia client libraries |
| Cross-Domain | Multi-physics pipeline for complex problems |

---

## Biomolecules Domain — 14 Quantum Biology Sub-Modules

The **biomolecules** domain contains 14 specialized sub-modules providing comprehensive quantum biology coverage:

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

## Physics Domain — 13 Quantum Physics Sub-Modules

The **physics** domain contains 13 specialized sub-modules providing comprehensive quantum physics coverage from field theory to cosmology:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **Quantum Field Theory** | Lorentz 4-vectors, Dirac spinors, Feynman diagrams, renormalization, scattering amplitudes |
| 2 | **Quantum Electrodynamics** | Vacuum polarization, anomalous magnetic moment (5-loop), Lamb shift, Schwinger effect |
| 3 | **Quantum Chromodynamics** | SU(3) color algebra, running α_s (4-loop), confinement, DGLAP splitting, jet physics |
| 4 | **Relativistic Quantum Mechanics** | Klein-Gordon, Dirac hydrogen, Zitterbewegung, Klein paradox, Mott scattering |
| 5 | **Quantum Gravity** | Hawking radiation, black hole entropy, Unruh effect, Loop Quantum Gravity, GUP |
| 6 | **Quantum Entanglement Theory** | CHSH/Mermin/Svetlichny Bell tests, concurrence, negativity, teleportation, distillation |
| 7 | **Quantum Optics** | Fock/coherent/squeezed states, Jaynes-Cummings, g⁽²⁾ correlations, HOM effect |
| 8 | **Quantum Thermodynamics** | Quantum Otto/Carnot cycles, Jarzynski equality, Landauer's principle, quantum batteries |
| 9 | **Quantum Chaos** | RMT ensembles (GOE/GUE/GSE), OTOC, ETH, spectral form factor, SYK model |
| 10 | **Open Quantum Systems** | Lindblad master equation, T₁/T₂ decoherence, quantum channels, Zeno effect |
| 11 | **Quantum Phase Transitions** | Transverse-field Ising, critical exponents, BKT transition, Kibble-Zurek mechanism |
| 12 | **Quantum Metrology** | Quantum Fisher information, SQL vs Heisenberg limit, Ramsey interferometry |
| 13 | **Quantum Cosmology** | Wheeler-DeWitt equation, inflation observables, primordial power spectrum, quantum bounce |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/physics/README.md`](packages/physics/README.md) for full API documentation per sub-module.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "quantum_field_theory", "task": "scattering_amplitude" }
}
```

**Demo endpoint:** `POST /api/v1/quantum/physics/demo`

---

## Mathematics Domain — 11 Quantum Mathematics Sub-Modules

The **mathematics** domain contains 11 specialized sub-modules providing comprehensive quantum mathematical foundations:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **Quantum Algebra** | Lie algebras (SU, SO, Sp, E₆-E₈), Clifford algebras, Pauli/Weyl algebras |
| 2 | **Quantum Information Theory** | Von Neumann/Rényi entropy, quantum channels, Fisher information, Holevo bound |
| 3 | **Quantum Topology** | Jones polynomial, braid groups, Chern-Simons theory, TQFT partition functions |
| 4 | **Quantum Differential Geometry** | Fiber bundles, gauge fields, Berry connection, Fubini-Study metric, Chern numbers |
| 5 | **Quantum Functional Analysis** | Hilbert space, spectral decomposition, trace class operators, POVM |
| 6 | **Quantum Probability** | Quantum random walks, quantum Markov chains, non-commutative probability |
| 7 | **Quantum Harmonic Analysis** | Wigner function, Husimi Q, Glauber P, Moyal star product |
| 8 | **Quantum Category Theory** | Monoidal/dagger categories, quantum logic lattice, Frobenius algebras |
| 9 | **Quantum Optimization Theory** | SDP relaxations, quantum game theory, Nash equilibrium, QAOA mapping |
| 10 | **Quantum Number Theory** | Shor's factoring, discrete logarithm, Stabilizer/CSS/Toric/Surface codes |
| 11 | **Advanced Quantum Probability** | Free probability, Wigner semicircle, Marchenko-Pastur, Tracy-Widom |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/mathematics/README.md`](packages/mathematics/README.md) for full API documentation per sub-module.

```json
{
  "domain": "mathematics",
  "algorithm": "vqe",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "quantum_topology", "task": "jones_polynomial" }
}
```

**Demo endpoint:** `POST /api/v1/quantum/mathematics/demo`

---

## Chemistry Domain — 5 Quantum Chemistry Sub-Modules

The **chemistry** domain contains 5 specialized sub-modules providing comprehensive quantum chemistry coverage from electronic structure to variational eigensolvers:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **Algorithms** | VQE, QPE, ADAPT-VQE, QITE, quantum dynamics, excited state VQE, subspace VQE |
| 2 | **Geometry** | 3D vector operations, bond length/angle computations, molecular geometry analysis |
| 3 | **Molecular** | Hamiltonian construction, Jordan-Wigner mapping, 1e/2e integrals, expectation values |
| 4 | **Orbital Optimization** | Active space selection (CAS, SCI, natural orbital, entanglement-based), embedding engines |
| 5 | **VQE Chemistry** | UCCSD/HEA/k-UpCCGSD ansatz, ground & excited state energy computation |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/chemistry/README.md`](packages/chemistry/README.md) for full API documentation per sub-module.

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "vqe_chemistry", "task": "ground_state_energy", "molecule": "C6H6" }
}
```

**Demo endpoint:** `POST /api/v1/quantum/chemistry/demo`

---

## Finance Domain — 6 Quantum Finance Sub-Modules

The **finance** domain contains 6 specialized sub-modules providing comprehensive quantum-accelerated financial modeling, from market data ingestion to portfolio optimization and trading execution:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **Market Data** | Bloomberg, Refinitiv, Yahoo Finance, Alpha Vantage feed integration, real-time ingestion |
| 2 | **Monte Carlo** | Control variates, antithetic, importance sampling, GBM, Ornstein-Uhlenbeck, Heston |
| 3 | **Portfolio** | Markowitz, risk parity, min variance, max Sharpe, Black-Litterman, hierarchical risk parity |
| 4 | **Quantum Algorithms** | Quantum Amplitude Estimation (QAE), QSVM, Quantum Generative Models |
| 5 | **Risk Metrics** | VaR, CVaR/Expected Shortfall, max drawdown, Sharpe ratio, Sortino ratio |
| 6 | **Trading System** | Order types (market, limit, stop, FOK, IOC), risk management, trade execution |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/finance/README.md`](packages/finance/README.md) for full API documentation per sub-module.

```json
{
  "domain": "finance",
  "algorithm": "vqe",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "portfolio", "task": "markowitz_optimization", "num_assets": 65536 }
}
```

**Demo endpoint:** `POST /api/v1/quantum/finance/demo`

---

## Fluid Mechanics Domain — 6 Quantum CFD Sub-Modules

The **fluid_mechanics** domain contains 6 specialized sub-modules providing comprehensive quantum-accelerated computational fluid dynamics from incompressible Navier-Stokes to quantum-native linear solvers:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **Navier-Stokes** | Incompressible/compressible solver, multi-regime (subsonic to hypersonic), FVM |
| 2 | **Turbulence** | DNS, RANS (k-ε, k-ω, k-ω SST), LES (Smagorinsky, WALE, dynamic), DES/DDES/IDDES |
| 3 | **Compressible** | Euler/Navier-Stokes/LES with Roe, HLLC, AUSM+ flux schemes for shock-capturing |
| 4 | **Multiphase** | VOF, level set, CLSVOF, phase field, front tracking, CSF/CSS surface tension |
| 5 | **Heat Transfer** | Conduction, convection, conjugate, radiation (S2S, discrete ordinates, P1) |
| 6 | **Quantum CFD** | HHL, VQLS, QSVT, VQE solvers for fluid mechanics, error mitigation |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/fluid_mechanics/README.md`](packages/fluid_mechanics/README.md) for full API documentation per sub-module.

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "vqe",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "turbulence", "task": "les_simulation", "model": "k_omega_sst" }
}
```

**Demo endpoint:** `POST /api/v1/quantum/fluid_mechanics/demo`

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
