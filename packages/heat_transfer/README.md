# Quantum Heat Transfer Package

## Overview

The Heat Transfer package provides quantum-accelerated solutions for thermal conduction, convection, radiation, and conjugate heat transfer through the unified L3 VQE circuit at 65536-qubit scale. It solves the Fourier heat equation and coupled thermal-fluid systems on 256×256 grids.

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

- **Qubits:** 65536
- **Maximum grid:** 256×256 thermal nodes
- **3D thermal:** 64×64×16 volumetric grids
- **Temperature range:** 0 K to 10^6 K (plasma conditions)

## Input Data Format

The input data array encodes the thermal field as 65536 floating-point amplitudes representing temperature distribution or heat flux.

```json
{
  "domain": "heat_transfer",
  "algorithm": "hhl",
  "input_data": [/* 65536 float values: amplitude-encoded temperature field */],
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
    "algorithm": "hhl",
    "input_data": [293.15, 293.15, 293.15, ... /* 65536 temperature values */],
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
temp_field = np.full(65536, 293.15)
temp_field[32768] = 500.0  # Hot spot at center
amplitudes = (temp_field / np.linalg.norm(temp_field)).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "heat_transfer",
        "algorithm": "fem",
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
    "tensor_expert_used": "PEPS",
    "qubit_count": 65536,
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
