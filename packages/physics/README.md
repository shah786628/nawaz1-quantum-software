# Quantum Physics Package

## Overview

The Physics package delivers quantum simulation of condensed matter systems, many-body physics, and quantum field theory through the unified L3 VQE circuit at 65536-qubit scale. It supports lattice models up to 256×256, spin chains, Hubbard models, and full quantum field theory calculations — all executed via the Algorithm Bridge on 7 tensor network experts in unconditional superposition.

## Key Features

- **Heisenberg model simulation** — arbitrary dimension spin chains and lattices up to 256×256
- **Ising model** — transverse field, longitudinal field, and frustrated systems
- **Hubbard model** — 2D Fermi-Hubbard at scale for high-Tc superconductivity
- **Quantum field theory** — scalar fields, gauge theories, lattice QCD
- **Condensed matter** — topological phases, quantum phase transitions, critical phenomena
- **Time evolution** — real-time and imaginary-time dynamics of quantum systems
- **Correlation functions** — N-point correlators computed on-demand from raw amplitudes
- **Spectral functions** — density of states, dynamic structure factor

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **VQE** | Ground state energy of many-body Hamiltonians |
| **VQS** | Variational Quantum Simulation for time dynamics |
| **Quantum Monte Carlo** | Sampling many-body wave functions |
| **TEBD** | Time-Evolving Block Decimation for 1D chains |
| **QPE** | Exact energy eigenvalues |
| **QITE** | Imaginary time evolution for thermal equilibrium |

## Scale

- **Qubits:** 65536
- **Maximum lattice:** 256×256 sites (65536 spins)
- **Dimensions:** 1D, 2D, 3D lattice geometries
- **Bond dimension:** Adaptive χ = ln(Q) per geometry
- **Tensor experts:** MPS/PEPS/PEPS3D/MERA/TTN/LoopTTN/PepsND in superposition

## Input Data Format

The input data array encodes the physical system as 65536 floating-point amplitudes representing the quantum state vector of the lattice or field configuration.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [/* 65536 float values: amplitude-encoded quantum state */],
  "config": {
    "model": "heisenberg",
    "lattice": "square",
    "dimensions": [256, 256],
    "coupling_J": 1.0,
    "external_field": 0.5
  }
}
```

**Input encoding:**
- Each amplitude corresponds to a basis state in the computational Hilbert space
- Lattice sites map directly to qubits (1 site = 1 qubit for spin-1/2)
- Coupling parameters specified in `config` define the Hamiltonian

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "physics",
    "algorithm": "vqe",
    "input_data": [0.001, -0.002, 0.003, ... /* 65536 amplitude values */],
    "config": {
      "model": "hubbard",
      "lattice": "square",
      "dimensions": [128, 128],
      "hopping_t": 1.0,
      "interaction_U": 4.0,
      "filling": 0.5,
      "temperature": 0.0
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Encode 256x256 Heisenberg lattice state
amplitudes = np.random.randn(65536).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "physics",
        "algorithm": "vqe",
        "input_data": amplitudes,
        "config": {
            "model": "heisenberg",
            "lattice": "square",
            "dimensions": [256, 256],
            "coupling_J": 1.0,
            "external_field": 0.0
        }
    }
)
print(response.json())
```

## Example Response

```json
{
  "status": "success",
  "result": {
    "ground_state_energy": -0.669437,
    "energy_per_site": -0.669437,
    "magnetization": 0.0,
    "staggered_magnetization": 0.307,
    "correlation_length": 12.4,
    "observables": {
      "spin_spin_correlation": [1.0, -0.334, 0.112, ...],
      "structure_factor_peak": [3.14159, 3.14159],
      "entanglement_entropy": 1.247
    },
    "tensor_expert_used": "PEPS",
    "qubit_count": 65536,
    "wall_time_ms": 2341
  }
}
```

## Use Cases

1. **High-Tc Superconductivity** — Solve the 2D Hubbard model to understand cuprate superconductors
2. **Quantum Phase Transitions** — Map phase diagrams of frustrated magnets and topological materials
3. **Quantum Spin Liquids** — Identify exotic phases with long-range entanglement
4. **Lattice Gauge Theory** — Non-perturbative QCD calculations for hadron physics
5. **Topological Quantum Matter** — Simulate Kitaev models, fractional quantum Hall states
6. **Quantum Thermalization** — Study equilibration and many-body localization
7. **Critical Phenomena** — Extract universal critical exponents at quantum phase transitions
