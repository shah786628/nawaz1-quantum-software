# Quantum Chemistry Package

## Overview

The Chemistry package provides quantum-native molecular simulation capabilities through the unified VQE engine at 2^53-qubit scale. It encompasses **5 specialized sub-modules** covering electronic structure calculations, molecular Hamiltonian construction, orbital optimization, and variational quantum chemistry.

**API Endpoint:** `POST http://localhost:8080/api/v1/quantum/execute`

**Demo Endpoint:** `POST http://localhost:8080/api/v1/quantum/chemistry/demo`

---

## The 5 Quantum Chemistry Sub-Modules

| # | Sub-Module | Key Domain |
|---|-----------|------------|
| 1 | Algorithms  | Algorithm Types |
| 2 | Geometry  | Molecular Geometry |
| 3 | Molecular  | Hamiltonian Construction |
| 4 | Orbital Optimization  | Active Space Selection |
| 5 | VQE Chemistry  | Variational Eigensolver |

---

## 1. Algorithms


Defines chemistry algorithm types and molecular system representations for quantum simulation, providing the foundational data structures for all chemistry computations.

**Key Capabilities:**
- VQE (Variational Quantum Eigensolver) algorithm configuration
- QPE (Quantum Phase Estimation) for exact eigenvalue extraction
- ADAPT-VQE with iterative operator pool growth
- QITE (Quantum Imaginary Time Evolution) for thermal state preparation
- Quantum dynamics simulation protocols
- Excited state VQE and subspace VQE variants
- Molecular system representation with atom types, coordinates, and properties

**When to Use:** Selecting and configuring the quantum chemistry algorithm for a given molecular problem, defining molecular systems with atomic coordinates and properties.

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "algorithms",
    "algorithm_type": "adapt_vqe",
    "molecule": "H2O",
    "atoms": [
      {"element": "O", "x": 0.0, "y": 0.0, "z": 0.0},
      {"element": "H", "x": 0.757, "y": 0.586, "z": 0.0},
      {"element": "H", "x": -0.757, "y": 0.586, "z": 0.0}
    ]
  }
}
```

---

## 2. Geometry


Implements molecular geometry calculations including 3D vector operations, bond length and angle computations, and geometry analysis for quantum chemistry simulations.

**Key Capabilities:**
- 3D vector operations (dot product, cross product, normalization)
- Bond length computation between atom pairs
- Bond angle calculation (three-atom angle)
- Dihedral angle measurement (four-atom torsion)
- Molecular geometry analysis and symmetry detection
- Center of mass and moment of inertia computation
- Geometry optimization coordinate transformations

**When to Use:** Preparing molecular geometries for Hamiltonian construction, computing structural properties, geometry optimization, and validating molecular configurations.

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "geometry",
    "task": "bond_analysis",
    "atoms": [
      {"element": "C", "x": 0.0, "y": 0.0, "z": 0.0},
      {"element": "C", "x": 1.54, "y": 0.0, "z": 0.0},
      {"element": "H", "x": -0.63, "y": 0.89, "z": 0.0}
    ],
    "compute": ["bond_lengths", "bond_angles", "dihedrals"]
  }
}
```

---

## 3. Molecular


Provides molecular Hamiltonian construction with Jordan-Wigner fermion-to-qubit mapping, one-electron and two-electron integral energy calculations, and statevector-based expectation value computation.

**Key Capabilities:**
- Molecular Hamiltonian construction from atomic coordinates
- Jordan-Wigner transformation (fermion-to-qubit mapping)
- One-electron integrals (kinetic energy + electron–core attraction)
- Two-electron integrals (electron-electron repulsion)
- Statevector-based expectation value computation
- Core–core electrostatic repulsion energy calculation
- Spin-orbital indexing and mapping

**When to Use:** Building and evaluating molecular Hamiltonians for VQE ground state calculations, computing electronic structure properties, and evaluating molecular energies.

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "molecular",
    "task": "hamiltonian_construction",
    "molecule": "LiH",
    "basis": "sto-3g",
    "charge": 0,
    "multiplicity": 1,
    "mapping": "jordan_wigner"
  }
}
```

---

## 4. Orbital Optimization


Handles active space selection and orbital optimization for molecular orbital space reduction, supporting multiple selection strategies and embedding engines.

**Key Capabilities:**
- Manual active space selection (user-specified orbitals)
- Automatic active space selection (energy-based criteria)
- Natural orbital-based selection (occupation number thresholds)
- Entanglement-based selection (mutual information ranking)
- Complete Active Space (CAS) configuration
- Selected Configuration Interaction (SCI) methods
- Orbital optimization configuration and convergence control
- Embedding engines for large-molecule orbital reduction

**When to Use:** Reducing the orbital space for large molecular systems, selecting chemically relevant orbitals for VQE, and configuring active space for strongly correlated systems.

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "orbital_optimization",
    "task": "active_space_selection",
    "molecule": "Fe2S2",
    "method": "entanglement_based",
    "num_active_electrons": 12,
    "num_active_orbitals": 12,
    "embedding": "dmet"
  }
}
```

---

## 5. VQE Chemistry


Core variational quantum eigensolver for chemistry with configuration management, ansatz types, optimization protocols, and integration with molecular Hamiltonian for ground and excited state energy computations.

**Key Capabilities:**
- UCCSD (Unitary Coupled Cluster Singles and Doubles) ansatz
- HEA (Hardware-Efficient Ansatz) for near-term devices
- k-UpCCGSD (k-fold Unitary pair Coupled Cluster GSD) for strong correlation
- Ground state energy minimization with convergence control
- Excited state calculations via folded spectrum and subspace methods
- Optimization protocol configuration (SPSA, L-BFGS-B, CMA-ES, QNG)
- Integration with molecular Hamiltonian construction
- Chemical accuracy targeting (< 1 kcal/mol)

**When to Use:** Computing ground state and excited state energies of molecular systems, benchmarking quantum chemistry methods, and production molecular energy calculations.

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "vqe_chemistry",
    "task": "ground_state_energy",
    "molecule": "C6H6",
    "basis": "cc-pvdz",
    "ansatz": "uccsd",
    "active_space": [6, 6],
    "optimizer": "l_bfgs_b",
    "convergence_threshold": 1e-9,
    "max_iterations": 1000
  }
}
```

---

## General Request Format

> **Algorithm:** The user specifies `"algorithm"` per request. For molecular energy / eigenvalue problems (electronic structure, ground-state energy, excited states) the correct choice is `"algorithm": "vqe"` — VQE is the proper algorithm for chemistry and is what every example in this package uses. The engine then compiles the requested algorithm onto the VQE execution substrate. Circuit depth is **automatically determined** by the engine based on input complexity; do not include `"depth"` in requests.

All sub-modules are accessed through the unified quantum execution endpoint:

```
POST http://localhost:8080/api/v1/quantum/execute
```

**Request body:**

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "input_data": [/* N float amplitudes (up to 2^53 supported) */],
  "config": {
    "sub_module": "<feature_name>"
  }
}
```

**Demo endpoint (no input_data required):**

```
POST http://localhost:8080/api/v1/quantum/chemistry/demo
```

---

## Scale

- **Qubits:** Up to 2^53 (9,007,199,254,740,992)
- **Maximum atoms:** 8738 (hemoglobin-scale)
- **Basis functions:** Up to 32768 spin-orbitals

---

## Python Example (Full Workflow)

```python
import requests
import numpy as np

API = "http://localhost:8080/api/v1/quantum/execute"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}

# Generate amplitude-encoded molecular state
rng = np.random.RandomState(42)
amplitudes = rng.normal(0, 1, 1024)  # Example uses 1024; engine supports up to 2^53
amplitudes = (amplitudes / np.linalg.norm(amplitudes)).tolist()

# Example: VQE ground state energy for benzene
response = requests.post(API, headers=HEADERS, json={
    "domain": "chemistry",
    "algorithm": "vqe",
    "input_data": amplitudes,
    "config": {
        "sub_module": "vqe_chemistry",
        "task": "ground_state_energy",
        "molecule": "C6H6",
        "ansatz": "uccsd"
    }
})
print(response.json())

# Example: Orbital optimization for iron-sulfur cluster
response = requests.post(API, headers=HEADERS, json={
    "domain": "chemistry",
    "algorithm": "vqe",
    "input_data": amplitudes,
    "config": {
        "sub_module": "orbital_optimization",
        "task": "active_space_selection",
        "molecule": "Fe2S2",
        "method": "entanglement_based"
    }
})
print(response.json())
```

---

## Use Cases

| Research Area | Relevant Sub-Modules |
|---------------|---------------------|
| **Drug Discovery & Binding Affinity** | VQE Chemistry, Molecular, Algorithms |
| **Catalyst Design** | VQE Chemistry, Orbital Optimization, Geometry |
| **Electronic Structure** | Molecular, VQE Chemistry, Algorithms |
| **Strongly Correlated Systems** | Orbital Optimization, VQE Chemistry |
| **Molecular Geometry Analysis** | Geometry, Molecular |
| **Battery Materials** | VQE Chemistry, Molecular, Orbital Optimization |
| **Photochemistry & Excited States** | VQE Chemistry, Algorithms |
| **Protein-Ligand Interactions** | Molecular, VQE Chemistry, Geometry |

---

### Continuum QFT for Solvation Chemistry

- Quantum Field Theory approach to solvation: treats solvent as a continuum quantum field rather than discrete molecules
- Enables accurate solvation free energy calculations at quantum level
- Applications: drug-solvent interactions, reaction kinetics in solution, electrochemistry
- Combines with VQE chemistry for full solvated molecular simulation

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "input_data": [/* N amplitude floats (up to 2^53 supported) */],
  "config": {
    "sub_module": "vqe_chemistry",
    "task": "solvation_free_energy",
    "solute": "acetaminophen",
    "solvent_model": "continuum_qft",
    "dielectric": 78.4
  }
}
```

---

## Input Method

### API Endpoint
```
POST http://localhost:8080/api/v1/quantum/execute
```

### Request Format
```json
{
  "problem": "molecular_energy",
  "config": {
    "num_qubits": 1024,
    "optimizer": "SPSA",
    "max_iterations": 100
  },
  "input_data": [0.001, -0.003, 0.002, "...Born-normalized floats..."]
}
```

### Supported Problem Types
- `"molecular_energy"` — Ground state energy of molecular systems
- `"reaction_pathway"` — Reaction coordinate energy profiles and transition states

### Data Input Options
- **Direct API**: Send JSON payload with amplitudes (Born-normalized floats)
- **File Import**: Upload binary/CSV data files via the import endpoint
- **Streaming**: For large datasets, use chunked streaming mode

---

## Hamiltonian Selection

### Available Hamiltonians
| Hamiltonian Type | Description | Use Case |
|---|---|---|
| Molecular (H2, LiH, H2O, C6H6) | Pre-defined molecular Hamiltonians | Benchmarking, quick validation |
| UCCSD Ansatz | Unitary Coupled Cluster Singles and Doubles | Production molecular energy calculations |
| Custom Hamiltonian Matrix | User-supplied qubit Hamiltonian | Advanced research, non-standard molecules |
| Orbital Energies | One-electron and two-electron integrals | Electronic structure from external codes |

### Configuration
```json
{
  "hamiltonian": {
    "type": "molecular",
    "parameters": {
      "molecule": "H2O",
      "basis": "sto-3g",
      "charge": 0,
      "multiplicity": 1
    }
  }
}
```

### Encoding Options
- **Jordan-Wigner**: Fermion-to-qubit mapping (default for chemistry)
- **Bravyi-Kitaev**: Reduced gate depth for large molecular systems
- **Direct Encoding**: For pre-computed qubit Hamiltonians

---

## Supported Scale

| Parameter | Maximum Value |
|---|---|
| **Qubits** | 2^53 (9,007,199,254,740,992) |
| **Bond Dimension** | 2^53 |
| **Precision** | IEEE 754 double (64-bit float) |

The quantum engine supports computations from small-scale (8 qubits) up to the theoretical maximum of 2^53 qubits with matching bond dimension, enabling simulation of molecular systems from simple hydrogen molecules to complex biological macromolecules and beyond.

