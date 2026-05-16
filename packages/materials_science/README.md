# Quantum Materials Science Package

## Overview

The Materials Science package provides quantum simulation of crystalline materials, superconductors, topological phases, and novel materials through the unified L3 VQE circuit at 65536-qubit scale. It enables band structure calculations, phonon spectra, superconducting gap equations, and defect modeling — all executed via the Algorithm Bridge on 7 tensor network experts in unconditional superposition.

## Key Features

- **Superconductor simulation** — YBCO, MgB2, and novel high-Tc materials
- **Topological materials** — topological insulators, Weyl semimetals, Majorana modes
- **Crystal structure** — unit cell optimization and phase stability prediction
- **Band theory** — electronic band structure and density of states
- **Phonon spectra** — lattice dynamics and electron-phonon coupling
- **Defect physics** — point defects, dislocations, and grain boundaries
- **Surface science** — catalytic surfaces, adsorption energies, reaction barriers
- **Alloy design** — multi-component phase diagrams and ordering transitions

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **VQE** | Ground state of crystal Hamiltonians |
| **DMFT** | Dynamical Mean-Field Theory for correlated electrons |
| **QPE** | Precise band gap and eigenvalue computation |
| **Quantum Monte Carlo** | Electron correlation in periodic systems |
| **ADAPT-VQE** | Adaptive ansatz for complex crystal structures |
| **QITE** | Thermal properties and phase transitions |

## Scale

- **Qubits:** 65536
- **Maximum unit cell:** 8192 atoms with periodic boundaries
- **k-point mesh:** Up to 256×256×1 Brillouin zone sampling
- **Bond dimension:** Adaptive χ = ln(Q) per geometry
- **Tensor experts:** MPS/PEPS/PEPS3D/MERA/TTN/LoopTTN/PepsND in superposition

## Input Data Format

The input data array encodes the material system as 65536 floating-point amplitudes representing the quantum state of the electronic structure.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [/* 65536 float values: amplitude-encoded crystal state */],
  "config": {
    "material": "YBCO",
    "task": "superconducting_gap",
    "lattice_type": "orthorhombic",
    "k_points": [16, 16, 4],
    "temperature": 0.0
  }
}
```

**Input encoding:**
- Amplitudes represent Bloch states in the crystal momentum basis
- Lattice vectors and atomic positions specified in config
- Spin-orbit coupling and relativistic effects included automatically

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "materials_science",
    "algorithm": "vqe",
    "input_data": [0.0045, -0.0012, 0.0078, ... /* 65536 amplitude values */],
    "config": {
      "material": "YBCO",
      "task": "band_structure",
      "lattice_vectors": [[3.82, 0, 0], [0, 3.89, 0], [0, 0, 11.68]],
      "k_path": "G-X-M-G-Z",
      "num_bands": 20,
      "include_soc": true
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Encode YBCO crystal electronic state
amplitudes = np.random.randn(65536).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "materials_science",
        "algorithm": "vqe",
        "input_data": amplitudes,
        "config": {
            "material": "YBCO",
            "task": "superconducting_gap",
            "temperature": 77.0,
            "doping": 0.15
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
    "band_gap": 0.0,
    "superconducting_gap": 0.025,
    "critical_temperature": 92.0,
    "unit": "eV",
    "convergence": true,
    "observables": {
      "density_of_states_at_fermi": 4.23,
      "electron_phonon_coupling": 1.87,
      "london_penetration_depth": 150.0,
      "coherence_length": 1.5
    },
    "tensor_expert_used": "PEPS3D",
    "qubit_count": 65536,
    "wall_time_ms": 4521
  }
}
```

## Use Cases

1. **High-Tc Superconductor Discovery** — Screen candidate materials for room-temperature superconductivity
2. **Battery Materials** — Design solid-state electrolytes and cathode materials for next-gen batteries
3. **Semiconductor Design** — Band engineering for photovoltaics, LEDs, and quantum dots
4. **Topological Quantum Computing** — Identify materials hosting Majorana zero modes
5. **Thermoelectric Materials** — Optimize ZT figure of merit for waste heat recovery
6. **Catalysis** — Design surfaces with optimal binding energies for industrial reactions
7. **Aerospace Materials** — Predict mechanical properties of novel alloys under extreme conditions
