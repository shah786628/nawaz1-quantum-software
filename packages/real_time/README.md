# Quantum Real-Time Dynamics Package

## Overview

The Real-Time package provides quantum time evolution, dynamics simulation, and Lindblad open quantum system solvers through the unified L3 VQE circuit at 65536-qubit scale. It enables real-time and imaginary-time evolution, non-equilibrium dynamics, and dissipative quantum systems.

## Key Features

- **Real-time evolution** — Hamiltonian dynamics with high-order Trotterization
- **Variational quantum simulation (VQS)** — time-dependent variational principle
- **TEBD** — Time-Evolving Block Decimation for 1D and quasi-1D systems
- **Lindblad solver** — open quantum system dynamics with dissipation
- **Quantum quench** — non-equilibrium dynamics after sudden parameter change
- **Floquet engineering** — periodically driven quantum systems
- **Quantum transport** — non-equilibrium Green's function dynamics
- **Adiabatic evolution** — quantum annealing and adiabatic state preparation

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **VQS** | Variational Quantum Simulation for time evolution |
| **TEBD** | Time-Evolving Block Decimation for 1D dynamics |
| **QITE** | Quantum Imaginary Time Evolution for cooling |
| **Lindblad** | Open quantum system dissipative dynamics |
| **Trotter** | Product formula time evolution |
| **VQE** | Steady-state solutions of driven-dissipative systems |

## Scale

- **Qubits:** 65536
- **Maximum time steps:** Unlimited streaming evolution
- **System size:** 65536 sites for 1D, 256×256 for 2D

## Input Data Format

The input data array encodes the initial quantum state as 65536 floating-point amplitudes, with time evolution parameters in config.

```json
{
  "domain": "real_time",
  "algorithm": "vqs",
  "input_data": [/* 65536 float values: initial state amplitudes */],
  "config": {
    "hamiltonian": "heisenberg",
    "time_total": 10.0,
    "time_step": 0.01,
    "trotter_order": 4,
    "observables": ["magnetization", "entanglement_entropy"]
  }
}
```

**Input encoding:**
- Amplitudes represent the initial quantum state |ψ(0)⟩
- Time evolution operator U(t) = exp(-iHt) applied iteratively
- Observables computed at each time step or at specified intervals

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "real_time",
    "algorithm": "vqs",
    "input_data": [1.0, 0.0, 0.0, ... /* 65536 initial state amplitudes */],
    "config": {
      "hamiltonian": "transverse_ising",
      "coupling_J": 1.0,
      "field_h": 0.5,
      "time_total": 20.0,
      "time_step": 0.05,
      "output_interval": 1.0,
      "observables": ["magnetization_z", "correlation_function", "entanglement_entropy"]
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Initial Neel state |0101...01⟩
initial_state = np.zeros(65536)
initial_state[0] = 1.0  # Start in computational basis state
amplitudes = initial_state.tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "real_time",
        "algorithm": "tebd",
        "input_data": amplitudes,
        "config": {
            "hamiltonian": "heisenberg",
            "time_total": 10.0,
            "time_step": 0.01,
            "bond_dimension_max": 256
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
    "final_time": 20.0,
    "num_time_steps": 400,
    "convergence": true,
    "time_series": {
      "magnetization_z": [1.0, 0.98, 0.92, 0.83, ...],
      "entanglement_entropy": [0.0, 0.12, 0.34, 0.67, ...],
      "energy": [-0.5, -0.5, -0.5, -0.5, ...]
    },
    "final_state_fidelity": 0.99987,
    "observables": {
      "thermalization_time": 8.4,
      "max_entanglement": 3.21,
      "light_cone_velocity": 2.34
    },
    "tensor_expert_used": "MPS",
    "qubit_count": 65536,
    "wall_time_ms": 8934
  }
}
```

## Use Cases

1. **Quantum Computing Validation** — Simulate and benchmark quantum processor behavior in real time
2. **Quantum Thermalization** — Study how isolated quantum systems reach thermal equilibrium
3. **Many-Body Localization** — Identify disorder-driven localization transitions in interacting systems
4. **Quantum Control** — Design optimal control pulses for quantum gates and state preparation
5. **Photosynthesis** — Model exciton transport in biological light-harvesting complexes
6. **Ultrafast Spectroscopy** — Simulate pump-probe experiments and attosecond dynamics
7. **Quantum Networks** — Model entanglement distribution dynamics in quantum communication links
