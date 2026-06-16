# VQE Engine: Algorithm Input Methods Guide

## Overview

The nawaz1 Unified Quantum VQE Engine supports **108 algorithms** across 19 categories. All algorithms use the **SAME input method** via the `problem` field. The `algorithm` field selects how the engine interprets the parameter vector — execution always routes through the unified VQE substrate.

> **CRITICAL — Read before sending any request:**
> 1. **Correct Hamiltonian** — Input data must be physically valid (Hermitian, real coefficients). Random values give wrong results.
> 2. **Correct Algorithm** — Select the algorithm matching your problem type. Wrong algorithm = wrong answer.
> 3. **Qubits = Power of 2** — The `qubits` field MUST be a power of 2: `4`, `8`, `16`, `32`, `64`, `128`, `256`, `512`, `1024`, `2048`, `4096`, `8192`, `16384`, `32768`, `65536`, etc.
> 4. **Read the Input Data Guide** — See [VQE_INPUT_DATA_GUIDE.md](VQE_INPUT_DATA_GUIDE.md) for full `problem` field specification.

---

## Supported Algorithm Categories

The engine provides 108 algorithms in 19 categories. See the [main README](README.md#supported-algorithms-108) for the complete table.

| Category | Algorithm Count | Examples |
|----------|----------------|----------|
| Variational | 8 | `vqe`, `qaoa`, `vqs`, `qng`, `adapt_vqe` |
| Phase & Eigenvalue | 5 | `qpe`, `iqpe`, `qpm`, `qsvd`, `qpca` |
| Fourier & Transform | 4 | `qft`, `iqft`, `qwt`, `qht` |
| Search & Sampling | 6 | `grover`, `quantum_binary_search`, `qae`, `monte_carlo` |
| Linear Algebra | 8 | `hhl`, `preconditioned_hhl`, `qsvt`, `qls`, `qmi` |
| Simulation & Dynamics | 6 | `trotter`, `dmrg`, `tebd`, `qite`, `lanczos` |
| Machine Learning | 8 | `qnn`, `qsvm`, `kmeans`, `kernel_estimation` |
| Error Mitigation | 7 | `zne`, `pec`, `virtual_distillation`, `readout_correction` |
| Cryptography | 4 | `qkd`, `qrng`, `shor`, `qds` |
| Tensor Networks | 5 | `mps`, `mera`, `peps`, `ttn`, `tensor_train` |
| Classical-Quantum Hybrid | 6 | `ccsd`, `qnode`, `qbp`, `qsdp` |
| Specialized | 12 | `bernstein_vazirani`, `simon`, `qtda`, `metropolis` |
| VQE Execution Modes | 4 | VQE variants and execution configurations |
| Classical Optimizers | 7 | SPSA, L-BFGS-B, ADAM, CMA-ES, QNG, Rotosolve |
| Ansatz Design | 5 | UCCSD, QubitAdapt, Symmetry-Preserving, k-UpCCGSD |
| QAOA Variants | 4 | QAOA mixer and cost function variants |
| Measurement Reduction | 3 | Term Grouper, Classical Shadow, Adaptive Shot |
| Numerical/Scientific | 7 | FDM, FEM, FVM, IMEX, Multigrid, PDE General, SINDy |
| Condensed Matter | 4 | Heisenberg, Hubbard, Ising, Lattice Gauge Theory |

---

## Input Methods by Algorithm

All algorithms use the same three input channels:

| Input Channel | Field | Use Case |
|--------------|-------|----------|
| **Custom Hamiltonian** | `problem.orbital_energies` | Chemistry, finance, ML, optimization |
| **Interaction Model** | `problem.interaction_energies` | Physics (Ising, Heisenberg, Hubbard) |
| **Pre-computed Molecule** | `molecule` + `bond_length` | Chemistry (H2, LiH, H2O, etc.) |

---

### Method 1: VQE (Default — Ground State Energy)

**Best for:** Molecular Hamiltonians, quantum chemistry, energy minimization

**API Endpoint:** `POST /api/v1/quantum/execute`

#### Input Format A: Custom Hamiltonian (from quantum chemistry calculation)

```python
import requests

# H2 Hamiltonian at 0.74 Angstrom (STO-3G basis)
# Terms: I, Z0, Z1, Z0 tensor Z1, Y0X1X0Y1
hamiltonian = [
    -1.0523732457727362,   # Identity term
     0.39793742484318045,  # Z0
    -0.39793742484318045,  # Z1
    -0.01128010425623538,  # Z0 tensor Z1
     0.18093119978423148   # Y0 tensor X1 tensor X0 tensor Y1
]

payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
        "orbital_energies": hamiltonian
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
print(f"Energy: {result['result']['aggregate_energy']:.6f} Hartree")
```

#### Input Format B: Pre-computed Molecules

```python
payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 4,
    "molecule": "H2",
    "bond_length": 0.74
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
print(f"Energy: {result['result']['aggregate_energy']:.6f} Hartree")
```

**Supported Molecules:** `H2`, `LiH`, `H2O`, `hemoglobin`, and others. See [VQE Input Data Guide](VQE_INPUT_DATA_GUIDE.md) for full list.

---

### Method 2: QAOA (Combinatorial Optimization)

**Best for:** Portfolio optimization, MaxCut, TSP, vehicle routing, scheduling

```python
import requests

# Portfolio optimization: encode risk-adjusted asset scores
# Negative = high return / low risk (preferred)
# Positive = low return / high risk (avoid)
asset_scores = [
    -0.68,   # AAPL: high Sharpe ratio
    -0.60,   # MSFT: good Sharpe
     0.32,   # GOOGL: low Sharpe
    -0.60,   # AMZN: good Sharpe
     0.45    # TSLA: high volatility
]

payload = {
    "domain": "finance",
    "algorithm": "qaoa",
    "qubits": 8,
    "problem": {
        "orbital_energies": asset_scores
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
print(f"Optimal energy: {result['result']['aggregate_energy']:.6f}")
```

**Note:** QAOA uses the same `problem.orbital_energies` input. The algorithm name tells the engine to interpret data as cost function coefficients.

---

### Method 3: HHL (Linear Systems Ax = b)

**Best for:** Sparse linear systems, matrix inversion, regression

```python
import requests

# Encode 2x2 symmetric matrix A and vector b into Hamiltonian form
# A = [[4, 1], [1, 3]], b = [2, 1]
# Flattened: [A00, A01, A10, A11, b0, b1]
matrix_elements = [
    4.0,   # A[0,0]
    1.0,   # A[0,1]
    1.0,   # A[1,0]
    3.0,   # A[1,1]
    2.0,   # b[0]
    1.0    # b[1]
]

payload = {
    "domain": "mathematics",
    "algorithm": "hhl",
    "qubits": 4,
    "problem": {
        "orbital_energies": matrix_elements
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
print(f"Energy: {result['result']['aggregate_energy']:.6f}")
```

---

### Method 4: Grover (Unstructured Search)

**Best for:** Database search, SAT problems, unstructured lookup

```python
import requests

# Oracle encoding: mark solution states with amplitude 1.0
# 16-item database (4 qubits), searching for item #10
oracle_encoding = [
    0.0, 0.0, 0.0, 0.0,  # Items 0-3
    0.0, 0.0, 0.0, 0.0,  # Items 4-7
    0.0, 0.0,              # Items 8-9
    1.0,                   # Item 10 = SOLUTION (marked)
    0.0, 0.0, 0.0, 0.0, 0.0  # Items 11-15
]

payload = {
    "domain": "mathematics",
    "algorithm": "grover",
    "qubits": 4,
    "problem": {
        "orbital_energies": oracle_encoding
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
```

---

### Method 5: Quantum Binary Search

**Best for:** Ordered/sorted data search, O(log N) quantum search

```python
import requests

# Sorted array encoded as orbital energies
sorted_array = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

payload = {
    "domain": "mathematics",
    "algorithm": "quantum_binary_search",
    "qubits": 4,
    "problem": {
        "orbital_energies": sorted_array
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
```

---

### Method 6: Physics Interaction Models

**Best for:** Ising, Heisenberg, Hubbard spin chains, condensed matter

#### Ising Model (interaction_energies)

```python
import requests

# H = -J * sum(sigma_i^z * sigma_{i+1}^z)  — 4-spin chain
ising_interaction = [
    -1.0,   # Spin 1-2 coupling
    -1.0,   # Spin 2-3 coupling
    -1.0,   # Spin 3-4 coupling
     0.0    # Boundary term
]

payload = {
    "domain": "physics",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
        "interaction_energies": ising_interaction
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
```

#### Heisenberg Model (interaction_energies)

```python
# H = J * sum(X_i X_{i+1} + Y_i Y_{i+1} + Z_i Z_{i+1})
heisenberg_interaction = [
    1.0,   # J (exchange coupling)
    1.0,   # XX term
    1.0,   # YY term
    1.0    # ZZ term
]

payload = {
    "domain": "physics",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
        "interaction_energies": heisenberg_interaction
    }
}
```

---

### Method 7: Chemistry Bond Length Scan

**Best for:** Potential energy surface mapping

```python
import requests

bond_lengths = [0.5, 0.6, 0.7, 0.74, 0.8, 0.9, 1.0, 1.2]

for bl in bond_lengths:
    payload = {
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4,
        "molecule": "H2",
        "bond_length": bl
    }
    response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
    result = response.json()
    energy = result['result']['aggregate_energy']
    print(f"Bond: {bl:.2f} Angstrom -> Energy: {energy:.6f} Hartree")
```

---

## All Supported Domains (17)

All algorithms work with **17 domain packages**:

| Domain | Use Case | Example Algorithms |
|--------|----------|-------------------|
| **chemistry** | Molecular simulation, Hamiltonian construction | `vqe`, `qpe`, `adapt_vqe` |
| **biology** | Protein folding, biomolecular interactions | `vqe`, `qaoa` |
| **physics** | Quantum dynamics, many-body, condensed matter | `vqe`, `trotter`, `dmrg` |
| **mathematics** | Linear algebra, eigenvalue problems, optimization | `hhl`, `qaoa`, `qsvt` |
| **finance** | Portfolio optimization, derivatives, risk analysis | `qaoa`, `monte_carlo`, `qae` |
| **materials_science** | Crystal structure, band structure, phonons | `vqe`, `peps` |
| **machine_learning** | Quantum classification, kernels, QNN | `qnn`, `qsvm`, `vqe` |
| **fluid_mechanics** | Navier-Stokes, CFD solvers | `vqe`, `hhl`, `fvm` |
| **logistics** | Vehicle routing, scheduling, bin packing | `qaoa`, `grover` |
| **heat_transfer** | Thermal diffusion, phase change | `vqe`, `fem` |
| **graphics** | Quantum rendering, ray tracing | `vqe` |
| **turbulence_cfd** | LES, DNS, Reynolds-averaged methods | `vqe`, `hhl` |
| **time_evolution** | Hamiltonian evolution, adiabatic computation | `trotter`, `tebd`, `qite` |
| **error_mitigation** | ZNE, PEC, readout correction | `zne`, `pec` |
| **cross_domain** | Multi-physics pipelines | any combination |
| **extension_plugin** | Custom algorithm development | user-defined |
| **core_gates** | Quantum gate operations | `vqe`, `grover`, `qft` |

---

## Complete API Reference

### Request Structure

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "qubits": 4,

  "problem": {
    "orbital_energies": [-1.052, 0.398, -0.398, -0.011, 0.181],
    "interaction_energies": [-1.0, -1.0, -1.0, 0.0],
    "pi_energies_beta": [0.1, 0.2, 0.3]
  },

  "molecule": "H2",
  "bond_length": 0.74,
  "basis_set": "sto-3g"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `domain` | string | Yes | One of 17 domains (see table above) |
| `algorithm` | string | No (default: `vqe`) | Algorithm name — see README for all 108 |
| `qubits` | integer | Yes | **Must be a power of 2**: 4, 8, 16, 32, ..., 65536 |
| `problem.orbital_energies` | number[] | One of three | Custom Hamiltonian coefficients |
| `problem.interaction_energies` | number[] | One of three | Physics interaction model |
| `molecule` + `bond_length` | string + number | One of three | Pre-computed molecule (chemistry only) |

> **IMPORTANT:** Top-level `input_data` is IGNORED by all algorithms. Always use the `problem` field or `molecule` field.

### Response Structure

```json
{
  "execution_id": "qexec_abc123",
  "status": "completed",
  "algorithm": "vqe",
  "domain": "chemistry",
  "num_qubits_requested": 4,
  "num_qubits_simulated": 4,
  "real_computation": true,
  "result": {
    "aggregate_energy": -1.137270,
    "fidelity": 0.999999999999998,
    "converged": true,
    "iteration_count": 1
  }
}
```

| Response Field | Meaning |
|---------------|---------|
| `status` | `completed`, `error`, or `timeout` |
| `real_computation` | `true` = real quantum simulation, not synthetic |
| `aggregate_energy` | Computed energy in Hartree (lower = more stable) |
| `fidelity` | Overlap with exact answer (1.0 = perfect) |
| `converged` | Whether the optimizer found a stable solution |
| `iteration_count` | Number of variational optimization steps |

---

## Key Principles

### 1. Unified Engine — All 108 Algorithms Share One Execution Path

All algorithms route through the same VQE parametric circuit. The `algorithm` field selects how input data is mapped to the parameter vector. Only the parameter vector changes.

### 2. Single Input Method

All algorithms accept data through exactly three channels:
- `problem.orbital_energies` — Custom Hamiltonian coefficients
- `problem.interaction_energies` — Physics interaction models
- `molecule` + `bond_length` — Pre-computed molecular integrals

Top-level `input_data` is IGNORED — this is by design.

### 3. Domain Routing

The `domain` field selects domain-specific Hamiltonian construction and post-processing. Using the wrong domain may apply incorrect Hamiltonians to your data.

### 4. Algorithm Selection Guide

| Problem Type | Use Algorithm |
|-------------|--------------|
| Molecular ground state energy | `vqe` |
| Portfolio / combinatorial optimization | `qaoa` |
| Linear system Ax = b | `hhl` |
| Unstructured search | `grover` |
| Sorted / ordered search | `quantum_binary_search` |
| Frequency / spectral analysis | `qft` |
| Physics time evolution | `trotter` |
| 1D strongly correlated systems | `dmrg` |
| Neural network / classification | `qnn` |
| Noise reduction | `zne` |
| High-accuracy chemistry | `ccsd` |

See the [main README](README.md#supported-algorithms-108) for the complete algorithm table.

---

## Common Mistakes

### WRONG: Using `input_data`

```python
# THIS WON'T WORK!
payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 4,
    "input_data": [0.5, 0.5, 0.5, 0.5]  # IGNORED!
}
```

### CORRECT: Use `problem` field

```python
# THIS WORKS!
payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
        "orbital_energies": [0.5, 0.5, 0.5, 0.5]  # USED!
    }
}
```

### WRONG: Non-power-of-2 qubits

```python
# WRONG! qubits must be power of 2
"qubits": 5     # Invalid
"qubits": 100   # Invalid
"qubits": 7     # Invalid
```

### CORRECT: Power-of-2 qubits

```python
# CORRECT!
"qubits": 4      # 2^2
"qubits": 8      # 2^3
"qubits": 16     # 2^4
"qubits": 1024   # 2^10
"qubits": 65536  # 2^16
```

---

## Summary

| Algorithm | Input Method | Domain Examples | Use Case |
|-----------|-------------|-----------------|----------|
| **VQE** | `problem.orbital_energies` or `molecule` | chemistry, physics, biology | Ground state energy |
| **QAOA** | `problem.orbital_energies` | finance, logistics, mathematics | Combinatorial optimization |
| **HHL** | `problem.orbital_energies` | mathematics, physics | Linear systems Ax=b |
| **Grover** | `problem.orbital_energies` | mathematics, core_gates | Unstructured search |
| **Quantum Binary Search** | `problem.orbital_energies` | mathematics, core_gates | Sorted data search |
| **Physics Models** | `problem.interaction_energies` | physics | Ising, Heisenberg, Hubbard |

**All 108 algorithms:**
- Use the SAME input method (`problem` field)
- Execute on the unified VQE quantum engine
- Require qubits to be a power of 2
- Require physically valid Hamiltonians
- Support all 17 domain packages
