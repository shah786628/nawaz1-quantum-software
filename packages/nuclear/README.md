# Quantum Nuclear Physics Package

## Overview

The Nuclear package provides quantum simulation of nuclear structure, fission/fusion processes, and nuclear forces through the unified L3 VQE circuit at 65536-qubit scale. It enables ab initio nuclear structure calculations, isotope analysis, nuclear reaction dynamics, and nuclear force modeling — all executed via the Algorithm Bridge on 7 tensor network experts in unconditional superposition.

## Key Features

- **Nuclear structure** — ab initio calculations of nuclear binding energies and spectra
- **Fission simulation** — potential energy surfaces and fission barrier heights
- **Fusion dynamics** — tunneling rates and cross-sections for fusion reactions
- **Nuclear forces** — chiral effective field theory interactions at N3LO
- **Isotope analysis** — nuclear chart predictions and drip line locations
- **Shell model** — large-scale configuration interaction for nuclei
- **Neutron stars** — equation of state from nuclear many-body theory
- **Radioactive decay** — alpha, beta, and gamma transition rates

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **VQE** | Nuclear ground state energies and binding curves |
| **QPE** | Precise nuclear eigenvalue computation |
| **Quantum Monte Carlo** | Nuclear many-body wave functions |
| **ADAPT-VQE** | Adaptive ansatz for nuclear shell model |
| **QITE** | Thermal nuclear properties |
| **UCCSD** | Coupled cluster for light nuclei |

## Scale

- **Qubits:** 65536
- **Maximum nucleons:** 65536 single-particle states
- **Model spaces:** Full sd, pf, sdpf, and no-core shell model
- **Bond dimension:** Adaptive χ = ln(Q) per geometry
- **Tensor experts:** MPS/PEPS/PEPS3D/MERA/TTN/LoopTTN/PepsND in superposition

## Input Data Format

The input data array encodes the nuclear system as 65536 floating-point amplitudes representing the quantum state of nucleons.

```json
{
  "domain": "nuclear",
  "algorithm": "vqe",
  "input_data": [/* 65536 float values: amplitude-encoded nuclear state */],
  "config": {
    "nucleus": "U-235",
    "task": "fission_barrier",
    "interaction": "chiral_n3lo",
    "model_space": "full",
    "protons": 92,
    "neutrons": 143
  }
}
```

**Input encoding:**
- Amplitudes represent nuclear wave function in occupation number basis
- Single-particle states mapped to qubits via Jordan-Wigner transformation
- Nuclear interaction matrix elements encoded in the Hamiltonian

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "nuclear",
    "algorithm": "vqe",
    "input_data": [0.0008, -0.0015, 0.0023, ... /* 65536 amplitude values */],
    "config": {
      "nucleus": "Fe-56",
      "task": "binding_energy",
      "interaction": "chiral_n3lo",
      "three_body_force": true,
      "model_space": "pf_shell"
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Encode nuclear state for iron-56
amplitudes = np.random.randn(65536).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "nuclear",
        "algorithm": "vqe",
        "input_data": amplitudes,
        "config": {
            "nucleus": "Fe-56",
            "task": "binding_energy",
            "interaction": "chiral_n3lo",
            "three_body_force": True
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
    "binding_energy": -492.26,
    "unit": "MeV",
    "binding_energy_per_nucleon": -8.79,
    "convergence": true,
    "observables": {
      "charge_radius": 3.737,
      "quadrupole_moment": 0.0,
      "magnetic_moment": 0.0,
      "excitation_spectrum": [0.847, 2.085, 2.657],
      "separation_energy_proton": 10.18,
      "separation_energy_neutron": 11.20
    },
    "tensor_expert_used": "MPS",
    "qubit_count": 65536,
    "wall_time_ms": 5234
  }
}
```

## Use Cases

1. **Nuclear Energy** — Optimize fuel cycles and predict fission product yields for next-gen reactors
2. **Fusion Reactor Design** — Calculate D-T and p-B11 fusion cross-sections at relevant energies
3. **Nuclear Astrophysics** — Neutron star equation of state and r-process nucleosynthesis
4. **Medical Isotopes** — Predict production pathways for Tc-99m, F-18, and other diagnostic isotopes
5. **Nuclear Security** — Model proliferation-relevant reactions and detection signatures
6. **Superheavy Elements** — Predict stability islands and synthesis routes for Z > 118
7. **Nuclear Waste** — Transmutation pathway optimization for long-lived actinide reduction
