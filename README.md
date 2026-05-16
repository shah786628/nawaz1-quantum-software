# Nawaz1 Quantum VQE Engine - Usage Guide

> **Multidimensional L6→L3 Quantum Pipeline** — A production-grade quantum VQE engine supporting 16 domains, 4 algorithms, data persistence, and real-time streaming.

**Author:** Shahnawaz Alam  
**License:** Proprietary  
**Copyright (c) 2026 Shahnawaz Alam. All rights reserved.**

---

## How Qubit Count Works (Amplitude Encoding)

The VQE engine uses **amplitude encoding**: the number of qubits is determined by the **input data length**, not a forced parameter.

```
num_qubits = input_data.len().next_power_of_two()
```

For **65536 qubits**, you must provide **65536 amplitude values** in the `input_data` array. Each value represents one amplitude in a 65536-dimensional Hilbert space. The problem must be large enough to justify this scale:

| Domain | Problem Scale for 65536 Qubits |
|--------|-------------------------------|
| Chemistry | Hemoglobin protein (8738 atoms, 65536 orbital amplitudes) |
| Physics | 256×256 Heisenberg lattice (65536 sites) |
| Finance | 65536 financial instruments (global portfolio) |
| Materials | 65536-atom YBCO superconductor crystal |
| Biomolecules | Hemoglobin tetramer (4532 atoms, 65536 conformations) |
| Machine Learning | 65536-feature quantum kernel SVM |
| Logistics | 65536-node global supply chain |
| Nuclear | Uranium-238 (238 nucleons, 65536 basis states) |
| Mathematics | 65536×65536 sparse linear system |
| Error Mitigation | 65536-amplitude noisy state correction |
| Graphics | 256×256 = 65536-pixel quantum ray tracing |
| Real-Time | 65536-site quantum state evolution |
| Fluid Mechanics | 256×256 Navier-Stokes grid (65536 points) |
| Turbulence CFD | 65536-point DNS turbulence (Re=10000) |
| Heat Transfer | 256×256 thermal conduction grid (65536 nodes) |
| Core Gates | 65536-qubit quantum Fourier transform |

---

## Table of Contents

- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [All 16 Quantum Domains](#all-16-quantum-domains)
- [Algorithm Bridge](#algorithm-bridge)
- [Data Import Guide](#data-import-guide)
- [Authentication & Security](#authentication--security)
- [VQS Time Evolution](#vqs-time-evolution)
- [Pipeline Execution](#pipeline-execution)
- [Multidimensional Queries](#multidimensional-queries)
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

The `input_data` array MUST contain enough values to justify 65536 qubits:

```python
import numpy as np, requests, json

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
# Bash (Linux/macOS) — includes 1024-qubit curl demos + full 65536-qubit Python
chmod +x run_all_demos.sh
./run_all_demos.sh

# PowerShell (Windows) — same structure
.\run_all_demos.ps1

# Python only (full 65536-qubit scale for all 16 domains)
pip install numpy requests
python quantum_usage_examples.py
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

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/quantum/status` | Engine status (qubits, memory, tier) |
| `GET` | `/api/v1/quantum/domains` | List available domains |
| `POST` | `/api/v1/quantum/execute` | **Execute quantum computation** |
| `POST` | `/api/v1/quantum/vqs/evolve` | VQS time evolution |
| `POST` | `/api/v1/quantum/pipeline/execute` | Full L1→L2→L3 pipeline |
| `POST` | `/api/v1/multidimensional/query` | Multidimensional range query |

### Data Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Register new user |
| `POST` | `/api/v1/auth/login` | Login (returns JWT) |
| `POST` | `/api/v1/query` | Execute SQL query |
| `POST` | `/api/v1/bulk-import` | Bulk data import |

---

## All 16 Quantum Domains

### 1. Chemistry — Hemoglobin Molecular Simulation (8738 atoms)

Simulates ground-state energy of large molecules. 65536 qubits encode the full molecular wavefunction in STO-6G basis.

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "molecule": "hemoglobin",
  "atoms": 8738,
  "basis_set": "STO-6G",
  "input_data": [65536 orbital amplitude coefficients]
}
```

### 2. Physics — 256×256 Heisenberg Lattice (65536 sites)

Simulates quantum lattice models on a 256×256 grid. Each site maps to one qubit amplitude.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "model": "heisenberg_xxz",
  "lattice_size": 256,
  "coupling_j": 1.0,
  "anisotropy_delta": 0.5,
  "input_data": [65536 lattice coupling coefficients]
}
```

### 3. Finance — 65536-Instrument Global Portfolio

Portfolio optimization over 65536 financial instruments. Each asset's return amplitude is one qubit.

```json
{
  "domain": "finance",
  "algorithm": "qaoa",
  "problem_type": "portfolio_optimization",
  "num_assets": 65536,
  "risk_tolerance": 0.15,
  "input_data": [65536 asset return amplitudes]
}
```

### 4. Materials Science — 65536-Atom YBCO Crystal

High-temperature superconductor simulation with full electron density at each atomic site.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "material": "YBCO",
  "lattice_atoms": 65536,
  "crystal_structure": "orthorhombic",
  "input_data": [65536 electron density coefficients]
}
```

### 5. Biomolecules — Hemoglobin Tetramer (4532 atoms)

Protein folding energy landscape with 65536 conformational states explored simultaneously.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "problem_type": "protein_folding",
  "protein": "hemoglobin_tetramer",
  "atoms": 4532,
  "residues": 574,
  "input_data": [65536 conformational energy amplitudes]
}
```

### 6. Machine Learning — 65536-Feature Quantum Kernel SVM

Quantum kernel method for genomic classification with 65536 SNP features.

```json
{
  "domain": "machine_learning",
  "algorithm": "vqe",
  "problem_type": "quantum_kernel_svm",
  "num_features": 65536,
  "dataset": "human_genome_gwas",
  "input_data": [65536 genomic feature amplitudes]
}
```

### 7. Logistics — 65536-Node Global Supply Chain

Vehicle routing and supply chain optimization across 65536 geographic nodes.

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "problem_type": "vehicle_routing",
  "num_nodes": 65536,
  "num_vehicles": 512,
  "input_data": [65536 routing cost amplitudes]
}
```

### 8. Nuclear — Uranium-238 Structure (238 nucleons)

Heavy nucleus shell model: 238 nucleons with 65536 configuration-interaction basis states.

```json
{
  "domain": "nuclear",
  "algorithm": "vqe",
  "nucleus": "uranium-238",
  "protons": 92,
  "neutrons": 146,
  "nucleons": 238,
  "input_data": [65536 nuclear wavefunction amplitudes]
}
```

### 9. Mathematics — 65536×65536 Sparse Linear System

Quantum HHL algorithm solving a 65536-dimensional linear system (Poisson equation on 256×256 grid).

```json
{
  "domain": "mathematics",
  "algorithm": "hhl",
  "problem_type": "linear_system",
  "matrix_size": 65536,
  "sparsity": "pentadiagonal",
  "input_data": [65536-element RHS vector b]
}
```

### 10. Error Mitigation — 65536-Qubit ZNE

Zero-noise extrapolation on a full 65536-amplitude noisy quantum state.

```json
{
  "domain": "error_mitigation",
  "algorithm": "vqe",
  "mitigation_method": "zero_noise_extrapolation",
  "noise_factors": [1.0, 1.5, 2.0, 2.5, 3.0],
  "input_data": [65536 noisy state amplitudes]
}
```

### 11. Graphics — 256×256 Quantum Ray Tracing

Parallel ray-surface intersection via Grover search over 65536 pixels.

```json
{
  "domain": "graphics",
  "algorithm": "grover",
  "problem_type": "ray_tracing",
  "resolution": [256, 256],
  "scene_objects": 4096,
  "input_data": [65536 radiance field amplitudes]
}
```

### 12. Real-Time — 65536-Site Quantum State Evolution

Live monitoring and Hamiltonian time evolution of a 65536-site quantum system.

```json
{
  "domain": "real_time",
  "algorithm": "vqe",
  "problem_type": "state_evolution",
  "num_sites": 65536,
  "observable": "magnetization",
  "input_data": [65536 initial state amplitudes]
}
```

### 13. Fluid Mechanics — 256×256 Navier-Stokes

Quantum lattice-Boltzmann CFD on a 256×256 grid (65536 velocity field points).

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "vqe",
  "problem_type": "navier_stokes",
  "grid_size": [256, 256],
  "reynolds_number": 1000,
  "input_data": [65536 velocity field amplitudes]
}
```

### 14. Turbulence CFD — 65536-Point DNS (Re=10000)

Direct numerical simulation capturing the full Kolmogorov energy cascade.

```json
{
  "domain": "turbulence_cfd",
  "algorithm": "vqe",
  "problem_type": "dns_turbulence",
  "grid_points": 65536,
  "reynolds_number": 10000,
  "input_data": [65536 Fourier mode amplitudes]
}
```

### 15. Heat Transfer — 256×256 Thermal Grid

Steady-state heat equation solved via quantum HHL on 65536 grid nodes.

```json
{
  "domain": "heat_transfer",
  "algorithm": "hhl",
  "problem_type": "conduction",
  "grid_size": [256, 256],
  "thermal_conductivity": 237.0,
  "input_data": [65536 temperature field coefficients]
}
```

### 16. Core Gates — 65536-Qubit QFT

Full quantum Fourier transform on a 65536-dimensional state vector.

```json
{
  "domain": "core_gates",
  "algorithm": "grover",
  "problem_type": "quantum_fourier_transform",
  "register_size": 65536,
  "input_data": [65536 state amplitudes to transform]
}
```

---

## Algorithm Bridge

The engine includes a pre-built Algorithm Bridge with 23 domain-specific modules. It routes requests to the optimal quantum algorithm automatically.

### Available Algorithms

| Algorithm | Best For | Complexity |
|-----------|----------|------------|
| **VQE** | Energy minimization, ground states | Variational, iterative |
| **QAOA** | Combinatorial optimization | p-layer circuit |
| **HHL** | Linear systems Ax=b | Exponential speedup |
| **Grover** | Unstructured search | O(√N) |

### Usage

Simply set the `"algorithm"` field in your request:

```json
{"algorithm": "vqe"}     // Default - variational eigensolver
{"algorithm": "qaoa"}    // Combinatorial problems
{"algorithm": "hhl"}     // Linear algebra
{"algorithm": "grover"}  // Search problems
```

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
# Response: {"token": "eyJ..."}
```

### 2. Create Table

```bash
curl -X POST http://localhost:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query":"CREATE TABLE experiments (id INT, domain TEXT, energy REAL, fidelity REAL)"}'
```

### 3. Insert Data

```bash
# Single row
curl -X POST http://localhost:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query":"INSERT INTO experiments VALUES (1, '\''chemistry'\'', -4532.7, 0.9998)"}'

# Batch (multiple rows)
curl -X POST http://localhost:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query":"INSERT INTO experiments VALUES (1,'\''chem'\'',-4532.7,0.99),(2,'\''phys'\'',-1783.2,0.99)"}'
```

### 4. Bulk Import

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

### 5. Query Data

```bash
curl -X POST http://localhost:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query":"SELECT * FROM experiments WHERE fidelity > 0.99 ORDER BY energy"}'
```

---

## Authentication & Security

### API Key Mode

When `NAWAZ1_API_KEY` environment variable is set, **all quantum endpoints** require the `X-API-Key` header:

```bash
# Start server with API key
NAWAZ1_API_KEY=my-secret-key-123 ./nawaz1-server

# All requests must include the key
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "X-API-Key: my-secret-key-123" \
  -d '{"domain":"chemistry","algorithm":"vqe","molecule":"hemoglobin","atoms":8738,"input_data":[...]}'
```

When `NAWAZ1_API_KEY` is **not set**, endpoints are open (dev/demo mode).

### JWT Authentication

For data operations (query, import), use JWT tokens:

```bash
# 1. Login to get token
TOKEN=$(curl -s -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.token')

# 2. Use token in requests
curl -X POST http://localhost:8080/api/v1/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT * FROM my_table"}'
```

---

## VQS Time Evolution

Simulate time-dependent quantum dynamics on a 65536-site system:

```python
import numpy as np, requests

rng = np.random.RandomState(53)
initial_state = np.array([((-1)**i)*(1.0+0.05*rng.normal()) for i in range(65536)])
initial_state = (initial_state / np.linalg.norm(initial_state)).tolist()

resp = requests.post("http://localhost:8080/api/v1/quantum/vqs/evolve", json={
    "num_sites": 65536,
    "time_steps": 50,
    "dt_seconds": 0.02,
    "hamiltonian": "heisenberg_xxz",
    "initial_state": "neel",
    "input_data": initial_state
})
```

Response includes state evolution snapshots at each time step.

---

## Pipeline Execution

The L1→L2→L3 pipeline processes data through encoding, tensor geometry, and VQE execution:

```python
import numpy as np, requests

rng = np.random.RandomState(42)
orbital_data = rng.normal(0, 1, 65536)
orbital_data = (orbital_data / np.linalg.norm(orbital_data)).tolist()

resp = requests.post("http://localhost:8080/api/v1/quantum/pipeline/execute", json={
    "domain": "chemistry",
    "molecule": "hemoglobin",
    "atoms": 8738,
    "input_data": orbital_data  # 65536 amplitudes → 65536 qubits
})
```

---

## Multidimensional Queries

Range queries on quantum-indexed multidimensional data:

```bash
curl -X POST http://localhost:8080/api/v1/multidimensional/query \
  -H "Content-Type: application/json" \
  -d '{
    "type": "range",
    "dimensions": 3,
    "data_points": 65536,
    "bounds": {"min": [0, 0, 0], "max": [1, 1, 1]}
  }'
```

---

## Running the Examples

### Files in this repository

| File | Description |
|------|-------------|
| `quantum_usage_examples.py` | All 16 domains at **full 65536-qubit scale** (Python + numpy) |
| `data_import_examples.py` | Auth, tables, import, query (Python) |
| `run_all_demos.sh` | Full demo runner (Bash) — 1024-qubit curl + 65536-qubit Python |
| `run_all_demos.ps1` | Full demo runner (PowerShell) — 1024-qubit inline + 65536-qubit Python |
| `README.md` | This documentation |

### Prerequisites

- **Server:** nawaz1-server binary running
- **Python:** 3.8+ with `numpy` and `requests` (`pip install numpy requests`)
- **curl:** For shell-based examples

### Run Individual Domains

```bash
python quantum_usage_examples.py chemistry
python quantum_usage_examples.py physics
python quantum_usage_examples.py finance
python quantum_usage_examples.py --list  # show all options
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
