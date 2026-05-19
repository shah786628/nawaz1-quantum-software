# Quantum Fluid Mechanics Package

## Overview

The Fluid Mechanics package provides quantum-accelerated computational fluid dynamics through the unified L3 VQE circuit at 65536-qubit scale. It encompasses **6 specialized sub-modules** covering the full spectrum of CFD — from incompressible Navier-Stokes to quantum-native linear solvers for fluid systems.

**API Endpoint:** `POST http://localhost:8080/api/v1/quantum/execute`

**Demo Endpoint:** `POST http://localhost:8080/api/v1/quantum/fluid_mechanics/demo`

---

## The 6 Quantum CFD Sub-Modules

| # | Sub-Module | Source | Key Domain |
|---|-----------|--------|------------|
| 1 | Navier-Stokes | `navier_stokes.rs` | Core Flow Solver |
| 2 | Turbulence | `turbulence.rs` | Turbulence Modeling |
| 3 | Compressible | `compressible.rs` | Compressible Flow |
| 4 | Multiphase | `multiphase.rs` | Interface Tracking |
| 5 | Heat Transfer | `heat_transfer.rs` | Thermal Simulation |
| 6 | Quantum CFD | `quantum_cfd.rs` | Quantum Linear Solvers |

---

## 1. Navier-Stokes

**Source:** `navier_stokes.rs`

Core incompressible and compressible Navier-Stokes solver supporting multiple flow regimes with spatial discretization schemes and finite volume method integration at 65536-qubit scale via the L3 VQE engine.

**Key Capabilities:**
- Incompressible flow solver (pressure-velocity coupling, SIMPLE/PISO algorithms)
- Compressible flow solver (density-based formulation)
- Multi-regime support: incompressible, subsonic, transonic, supersonic, hypersonic
- Spatial discretization schemes (upwind, central, QUICK, MUSCL, WENO)
- Finite Volume Method (FVM) integration with cell-centered and vertex-centered variants
- Time-stepping methods: explicit (RK4), implicit (backward Euler, BDF2), dual time-stepping
- Boundary conditions: no-slip, slip, inlet/outlet, periodic, pressure far-field

**When to Use:** General-purpose flow simulation, aerodynamic analysis, internal flow design, pipe networks, and any problem governed by the Navier-Stokes equations.

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "qft",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "navier_stokes",
    "task": "steady_state_solve",
    "regime": "incompressible",
    "grid": [256, 256],
    "reynolds_number": 100000,
    "discretization": "fvm",
    "boundary_conditions": "no_slip"
  }
}
```

---

## 2. Turbulence

**Source:** `turbulence.rs`

Comprehensive turbulence modeling framework providing DNS, RANS, LES, and hybrid methods for resolving or modeling turbulent flow structures at all relevant scales via the L3 VQE engine at 65536-qubit scale.

**Key Capabilities:**
- Direct Numerical Simulation (DNS) — full resolution of all turbulent scales
- RANS models: k-epsilon (standard, RNG, realizable), k-omega, k-omega SST
- LES models: Smagorinsky, WALE (Wall-Adapting Local Eddy-viscosity), dynamic Smagorinsky
- Hybrid methods: DES (Detached Eddy Simulation), DDES, IDDES
- Wall functions: standard, scalable, enhanced wall treatment
- Turbulence intensity and length scale initialization
- Reynolds stress transport modeling (RSM)

**When to Use:** High-Reynolds-number flows, aeroacoustics, mixing problems, separated flows, and any scenario requiring accurate turbulence resolution or modeling.

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "qft",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "turbulence",
    "task": "les_simulation",
    "model": "k_omega_sst",
    "les_model": "wale",
    "grid": [256, 256],
    "reynolds_number": 500000,
    "wall_treatment": "enhanced"
  }
}
```

---

## 3. Compressible

**Source:** `compressible.rs`

Compressible flow solvers for Euler equations and compressible Navier-Stokes with advanced flux schemes for shock-capturing and high-speed flow simulation at 65536-qubit scale via the L3 VQE engine.

**Key Capabilities:**
- Euler equation solver (inviscid compressible flow)
- Compressible Navier-Stokes solver (viscous high-speed flow)
- Compressible LES for turbulent high-speed flows
- Flux schemes: Roe (approximate Riemann), HLLC, AUSM+, AUSM+up, Lax-Friedrichs
- Shock-capturing with slope limiters (minmod, van Leer, superbee, MC)
- Mach number regime handling: subsonic, transonic, supersonic, hypersonic
- Real gas effects and equation of state models

**When to Use:** Supersonic/hypersonic vehicle design, shock-boundary layer interaction, nozzle flows, re-entry aerothermodynamics, and detonation modeling.

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "qft",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "compressible",
    "task": "shock_tube",
    "solver": "euler",
    "flux_scheme": "hllc",
    "mach_number": 2.5,
    "grid": [256, 256],
    "limiter": "van_leer"
  }
}
```

---

## 4. Multiphase

**Source:** `multiphase.rs`

Multiphase flow simulation with interface tracking and surface tension modeling for immiscible fluid systems at 65536-qubit scale via the L3 VQE engine.

**Key Capabilities:**
- Volume of Fluid (VOF) method for interface capturing
- Level set method for smooth interface representation
- Coupled Level Set and VOF (CLSVOF) for mass-conservative sharp interfaces
- Phase field method for diffuse interface modeling
- Front tracking with Lagrangian marker particles
- Surface tension models: CSF (Continuum Surface Force), CSS (Continuum Surface Stress), height function
- Droplet dynamics, bubble rise, and film rupture

**When to Use:** Liquid-gas interfaces, spray atomization, bubble columns, wave breaking, droplet impact, oil-water separation, and microfluidic device design.

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "qft",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "multiphase",
    "task": "interface_tracking",
    "method": "clsvof",
    "surface_tension_model": "csf",
    "grid": [256, 256],
    "density_ratio": 1000.0,
    "viscosity_ratio": 100.0,
    "weber_number": 12.0
  }
}
```

---

## 5. Heat Transfer

**Source:** `heat_transfer.rs`

Heat transfer simulation with multiple modes including conduction, convection, conjugate heat transfer, and radiation at 65536-qubit scale via the L3 VQE engine.

**Key Capabilities:**
- Pure conduction solver (steady-state and transient)
- Forced and natural convection with buoyancy coupling (Boussinesq approximation)
- Conjugate heat transfer (coupled solid-fluid thermal analysis)
- Full thermal modeling with combined convection and radiation
- Radiation models: surface-to-surface (S2S), discrete ordinates (DO), P1 approximation
- Temperature-dependent material properties
- Phase change and solidification/melting (enthalpy-porosity method)

**When to Use:** Electronics cooling, heat exchanger design, building thermal analysis, casting solidification, furnace modeling, and thermal management systems.

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "qft",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "heat_transfer",
    "task": "conjugate_thermal",
    "mode": "convection",
    "radiation_model": "discrete_ordinates",
    "grid": [256, 256],
    "inlet_temperature": 300.0,
    "wall_heat_flux": 5000.0,
    "emissivity": 0.85
  }
}
```

---

## 6. Quantum CFD

**Source:** `quantum_cfd.rs`

Quantum CFD integration providing quantum linear solvers for fluid mechanics systems, quantum error mitigation, and quantum circuit configuration for CFD workloads at 65536-qubit scale via the L3 VQE engine.

**Key Capabilities:**
- HHL (Harrow-Hassidim-Lloyd) algorithm for sparse linear systems from flow discretization
- VQLS (Variational Quantum Linear Solver) for near-term quantum CFD
- QSVT (Quantum Singular Value Transformation) for general matrix operations
- VQE-based flow optimization and variational flow solving
- Quantum error mitigation (ZNE, PEC, readout correction) for CFD results
- Quantum circuit configuration: depth control, ancilla management, precision tuning
- Hybrid quantum-classical iteration for nonlinear Navier-Stokes coupling

**When to Use:** Leveraging quantum advantage for large sparse linear systems in CFD, quantum-accelerated pressure Poisson solvers, and next-generation quantum-classical hybrid CFD workflows.

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "qft",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_cfd",
    "task": "quantum_pressure_solve",
    "quantum_solver": "vqls",
    "error_mitigation": "zne",
    "grid": [256, 256],
    "precision_qubits": 16,
    "max_iterations": 500,
    "convergence_threshold": 1e-8
  }
}
```

---

## General Request Format

All sub-modules are accessed through the unified quantum execution endpoint:

```
POST http://localhost:8080/api/v1/quantum/execute
```

**Request body:**

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "qft",
  "input_data": [/* 65536 float amplitude values */],
  "config": {
    "sub_module": "<feature_name>"
  }
}
```

**Demo endpoint (no input_data required):**

```
POST http://localhost:8080/api/v1/quantum/fluid_mechanics/demo
```

---

## Scale

- **Qubits:** 65536
- **Maximum grid:** 256×256 (65536 cells per 2D slice)
- **3D extension:** 64×64×16 volumetric grids
- **Reynolds number:** Up to Re = 10⁶ with quantum turbulence models

---

## Python Example (Full Workflow)

```python
import requests
import numpy as np

API = "http://localhost:8080/api/v1/quantum/execute"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}

# Generate 65536 amplitude-encoded flow field state
rng = np.random.RandomState(42)
amplitudes = rng.normal(0, 1, 65536)
amplitudes = (amplitudes / np.linalg.norm(amplitudes)).tolist()

# Example: Turbulent flow with k-omega SST
response = requests.post(API, headers=HEADERS, json={
    "domain": "fluid_mechanics",
    "algorithm": "qft",
    "input_data": amplitudes,
    "config": {
        "sub_module": "turbulence",
        "task": "rans_simulation",
        "model": "k_omega_sst",
        "reynolds_number": 500000
    }
})
print(response.json())

# Example: Multiphase VOF simulation
response = requests.post(API, headers=HEADERS, json={
    "domain": "fluid_mechanics",
    "algorithm": "qft",
    "input_data": amplitudes,
    "config": {
        "sub_module": "multiphase",
        "task": "interface_tracking",
        "method": "vof",
        "surface_tension_model": "csf"
    }
})
print(response.json())
```

---

## Use Cases

| Research Area | Relevant Sub-Modules |
|---------------|---------------------|
| **Aerospace Design** | Navier-Stokes, Compressible, Turbulence |
| **Automotive Aerodynamics** | Navier-Stokes, Turbulence, Heat Transfer |
| **Chemical Engineering** | Multiphase, Heat Transfer, Navier-Stokes |
| **Electronics Cooling** | Heat Transfer, Navier-Stokes, Quantum CFD |
| **Marine Engineering** | Multiphase, Navier-Stokes, Turbulence |
| **Hypersonic Vehicles** | Compressible, Heat Transfer, Turbulence |
| **Power-Plant Coolant Thermal-Hydraulics** | Multiphase, Heat Transfer, Navier-Stokes |
| **Microfluidics** | Multiphase, Navier-Stokes, Quantum CFD |
| **Wind Energy** | Turbulence, Navier-Stokes, Quantum CFD |
| **Climate & Ocean Modeling** | Navier-Stokes, Turbulence, Heat Transfer |
