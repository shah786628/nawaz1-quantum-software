# Quantum Heat Transfer Package

## Overview

The Heat Transfer package provides quantum-accelerated solutions for thermal conduction, convection, radiation, and conjugate heat transfer through the unified VQE engine at 2^53-qubit scale. It solves the Fourier heat equation and coupled thermal-fluid systems on 256×256 grids.

## Key Features

- **Thermal conduction** — steady-state and transient heat diffusion in complex geometries
- **Convective heat transfer** — forced, natural, and mixed convection
- **Thermal radiation** — view factors, radiative transfer equation, participating media
- **Conjugate heat transfer** — coupled solid-fluid thermal interaction
- **Phase change** — melting, solidification, and boiling simulation
- **Thermal management** — electronic cooling, heat sink optimization
- **Multi-scale thermal** — from nanoscale phonon transport to system-level thermal design
- **Inverse heat transfer** — parameter estimation and thermal property identification

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **HHL** | Solving large thermal systems exponentially fast |
| **PDE Solvers (FDM)** | Finite Difference for heat equation discretization |
| **PDE Solvers (FEM)** | Finite Element for complex geometry thermal analysis |
| **VQE** | Variational optimization of thermal configurations |
| **Quantum Monte Carlo** | Radiative transfer Monte Carlo acceleration |
| **QITE** | Thermal equilibrium state computation |

## Scale

- **Qubits:** Up to 2^53 (9,007,199,254,740,992)
- **Maximum grid:** 256×256 thermal nodes
- **3D thermal:** 64×64×16 volumetric grids
- **Temperature range:** 0 K to 10^6 K (plasma conditions)

## Input Data Format

The input data array encodes the thermal field as N floating-point amplitudes (up to 2^53) representing temperature distribution or heat flux.

```json
{
  "domain": "heat_transfer",
  "algorithm": "qft",
  "input_data": [/* N float values: amplitude-encoded temperature field (up to 2^53) */],
  "config": {
    "equation": "fourier",
    "grid": [256, 256],
    "thermal_conductivity": 401.0,
    "density": 8960.0,
    "specific_heat": 385.0,
    "boundary_conditions": {
      "left": {"type": "dirichlet", "value": 373.15},
      "right": {"type": "dirichlet", "value": 293.15}
    }
  }
}
```

**Input encoding:**
- Amplitudes represent the discretized temperature or heat source distribution
- Material properties specified in config (can be temperature-dependent)
- Boundary conditions define thermal environment

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "heat_transfer",
    "algorithm": "qft",
    "input_data": [293.15, 293.15, 293.15, ... /* N temperature values (up to 2^53) */],
    "config": {
      "equation": "fourier_transient",
      "grid": [256, 256],
      "material": "copper",
      "thermal_conductivity": 401.0,
      "density": 8960.0,
      "specific_heat": 385.0,
      "time_total": 60.0,
      "heat_source": {"type": "point", "power": 1000.0, "location": [128, 128]}
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Initial temperature field (room temperature with hot spot)
temp_field = np.full(1024, 293.15)
temp_field[32768] = 500.0  # Hot spot at center
amplitudes = (temp_field / np.linalg.norm(temp_field)).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "heat_transfer",
        "algorithm": "qft",
        "input_data": amplitudes,
        "config": {
            "equation": "fourier_transient",
            "grid": [256, 256],
            "material": "aluminum",
            "thermal_conductivity": 237.0,
            "time_total": 30.0
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
    "converged": true,
    "max_temperature": 412.7,
    "min_temperature": 293.15,
    "mean_temperature": 301.4,
    "steady_state_reached": true,
    "observables": {
      "heat_flux_max": 15234.5,
      "thermal_resistance": 0.0023,
      "nusselt_number": 45.7,
      "thermal_diffusion_time": 12.3,
      "temperature_gradient_max": 1247.8
    },
    "grid_resolution": [256, 256],
    "qubit_count": 1024,
    "wall_time_ms": 3456
  }
}
```

## Use Cases

1. **Electronics Cooling** — Thermal management of data centers, GPUs, and high-power electronics
2. **Additive Manufacturing** — Thermal simulation of laser powder bed fusion (3D printing)
3. **Building Energy** — HVAC system design and building envelope thermal performance
4. **Power-Plant Coolant Thermal** — Fuel-element temperature distribution and coolant thermal-hydraulics
5. **Spacecraft Thermal Control** — Orbital thermal cycling and radiator design for satellites
6. **Industrial Furnaces** — Temperature uniformity optimization in heat treatment processes
7. **Geothermal Energy** — Subsurface heat transport modeling for geothermal reservoir engineering

---

## Input Method

### API Endpoint
```
POST http://localhost:8080/api/v1/quantum/execute
```

### Request Format
```json
{
  "problem": "thermal_diffusion",
  "config": {
    "num_qubits": 1024,
    "optimizer": "SPSA",
    "max_iterations": 100
  },
  "input_data": [293.15, 293.15, 300.0, "...Born-normalized floats..."]
}
```

### Supported Problem Types
- `"thermal_diffusion"` — Transient and steady-state heat conduction
- `"steady_state_heat"` — Equilibrium temperature distribution

### Data Input Options
- **Direct API**: Send JSON payload with amplitudes (Born-normalized floats)
- **File Import**: Upload binary/CSV data files via the import endpoint
- **Streaming**: For large datasets, use chunked streaming mode

---

## Hamiltonian Selection

### Available Hamiltonians
| Hamiltonian Type | Description | Use Case |
|---|---|---|
| Diffusion Operator | Fourier heat equation discretization | Thermal conduction problems |
| Boundary-Valued | Dirichlet/Neumann/Robin boundary conditions | Industrial thermal analysis |
| Conjugate Thermal | Coupled solid-fluid thermal interaction | Heat exchangers, electronics |
| Radiation Operator | Surface-to-surface and participating media | High-temperature systems |

### Configuration
```json
{
  "hamiltonian": {
    "type": "diffusion_operator",
    "parameters": {
      "thermal_conductivity": 401.0,
      "density": 8960.0,
      "specific_heat": 385.0,
      "grid": [256, 256]
    }
  }
}
```

### Encoding Options
- **Jordan-Wigner**: For quantum thermal state preparation
- **Bravyi-Kitaev**: Reduced gate depth for large thermal systems
- **Direct Encoding**: For discretized heat equation linear systems (HHL-based)

---

## Supported Scale

| Parameter | Maximum Value |
|---|---|
| **Qubits** | 2^53 (9,007,199,254,740,992) |
| **Bond Dimension** | 2^53 |
| **Precision** | IEEE 754 double (64-bit float) |

The quantum engine supports computations from small-scale (8 qubits) up to the theoretical maximum of 2^53 qubits with matching bond dimension, enabling simulation of molecular systems from simple hydrogen molecules to complex biological macromolecules and beyond.

