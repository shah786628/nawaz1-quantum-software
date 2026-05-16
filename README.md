# Nawaz1 Quantum VQE Engine - Usage Guide

> **Multidimensional L6→L3 Quantum Pipeline** — A production-grade quantum VQE engine supporting 16 domains, 4 algorithms, data persistence, and real-time streaming.

**Author:** Shahnawaz Alam  
**License:** Proprietary  
**Copyright (c) 2026 Shahnawaz Alam. All rights reserved.**

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

### 3. Run First Query

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -d '{"domain":"chemistry","num_qubits":65536,"algorithm":"vqe","molecule":"H2","bond_length":0.74}'
```

### 4. Run All Examples

```bash
# Bash (Linux/macOS)
chmod +x run_all_demos.sh
./run_all_demos.sh

# PowerShell (Windows)
.\run_all_demos.ps1

# Python (cross-platform)
pip install requests
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

### 1. Chemistry — Molecular Simulation

Simulates molecular ground-state energies using VQE. Applications: drug discovery, catalyst design.

```json
{
  "domain": "chemistry",
  "num_qubits": 65536,
  "algorithm": "vqe",
  "molecule": "H2",
  "bond_length": 0.74
}
```

Supported molecules: H2, LiH, H2O, BeH2, CH4, NH3, HF, and arbitrary molecular formulas.

### 2. Physics — Lattice Models

Simulates quantum lattice models (Heisenberg, Ising, Hubbard). Applications: magnetism, superconductivity.

```json
{
  "domain": "physics",
  "num_qubits": 65536,
  "algorithm": "vqe",
  "model": "heisenberg",
  "lattice_size": 8,
  "coupling_j": 1.0
}
```

### 3. Finance — Portfolio & Risk

Portfolio optimization and risk analysis using quantum annealing. Applications: asset allocation, VaR.

```json
{
  "domain": "finance",
  "num_qubits": 65536,
  "algorithm": "qaoa",
  "problem_type": "portfolio_optimization",
  "num_assets": 8,
  "risk_tolerance": 0.3
}
```

### 4. Materials Science — Crystal & Band Structure

Predicts electronic band gaps and crystal properties. Applications: solar cells, semiconductors.

```json
{
  "domain": "materials_science",
  "num_qubits": 65536,
  "algorithm": "vqe",
  "material": "silicon",
  "crystal_structure": "diamond_cubic",
  "lattice_constant": 5.43
}
```

### 5. Biomolecules — Protein & Drug Discovery

Protein folding and drug-target interactions. Applications: drug design, enzyme catalysis.

```json
{
  "domain": "biomolecules",
  "num_qubits": 65536,
  "algorithm": "vqe",
  "problem_type": "protein_folding",
  "sequence": "ALANINE-GLYCINE-VALINE",
  "num_residues": 3
}
```

### 6. Machine Learning — Quantum Neural Networks

Quantum-enhanced ML with variational circuits. Applications: classification, kernel methods.

```json
{
  "domain": "machine_learning",
  "num_qubits": 65536,
  "algorithm": "vqe",
  "problem_type": "qnn_classification",
  "num_layers": 4,
  "data": [0.1, 0.5, 0.3, 0.8, 0.2, 0.9, 0.4, 0.7]
}
```

### 7. Logistics — Routing & Supply Chain

Vehicle routing and supply chain optimization. Applications: TSP, delivery routing.

```json
{
  "domain": "logistics",
  "num_qubits": 65536,
  "algorithm": "qaoa",
  "problem_type": "routing",
  "num_cities": 5,
  "distances": [[0,10,15,20,25],[10,0,35,25,30],[15,35,0,30,20],[20,25,30,0,15],[25,30,20,15,0]]
}
```

### 8. Nuclear — Nuclear Structure

Nuclear shell model and reaction simulations. Applications: nuclear energy, fusion research.

```json
{
  "domain": "nuclear",
  "num_qubits": 65536,
  "algorithm": "vqe",
  "nucleus": "deuterium",
  "protons": 1,
  "neutrons": 1
}
```

### 9. Mathematics — Linear Algebra

Quantum linear algebra and optimization. Applications: linear systems, eigenvalue problems.

```json
{
  "domain": "mathematics",
  "num_qubits": 65536,
  "algorithm": "hhl",
  "problem_type": "linear_system",
  "matrix": [[2, -1], [-1, 2]],
  "vector": [1, 0]
}
```

### 10. Error Mitigation — Noise Reduction

Quantum error correction and noise suppression. Applications: improving noisy computations.

```json
{
  "domain": "error_mitigation",
  "num_qubits": 65536,
  "algorithm": "vqe",
  "mitigation_method": "zero_noise_extrapolation",
  "noise_factors": [1.0, 1.5, 2.0, 2.5]
}
```

### 11. Graphics — Quantum Rendering

Quantum-accelerated rendering and ray tracing. Applications: path tracing, global illumination.

```json
{
  "domain": "graphics",
  "num_qubits": 65536,
  "algorithm": "grover",
  "problem_type": "ray_tracing",
  "scene_objects": 64,
  "resolution": [128, 128]
}
```

### 12. Real-Time — Streaming Quantum State

Real-time quantum state monitoring and evolution. Applications: live monitoring, adaptive control.

```json
{
  "domain": "real_time",
  "num_qubits": 65536,
  "algorithm": "vqe",
  "problem_type": "state_monitoring",
  "update_interval_ms": 100
}
```

### 13. Fluid Mechanics — Navier-Stokes & CFD

Quantum CFD via lattice Boltzmann methods. Applications: aerodynamics, pipe flow.

```json
{
  "domain": "fluid_mechanics",
  "num_qubits": 65536,
  "algorithm": "vqe",
  "problem_type": "navier_stokes",
  "reynolds_number": 100,
  "geometry": "pipe"
}
```

### 14. Turbulence CFD — Turbulent Flow

Large eddy and direct numerical simulation. Applications: jet engines, combustion.

```json
{
  "domain": "turbulence_cfd",
  "num_qubits": 65536,
  "algorithm": "vqe",
  "problem_type": "channel_flow",
  "reynolds_number": 5000,
  "turbulence_model": "les"
}
```

### 15. Heat Transfer — Thermal Transport

Conduction, convection, and radiation simulation. Applications: electronics cooling, engines.

```json
{
  "domain": "heat_transfer",
  "num_qubits": 65536,
  "algorithm": "hhl",
  "problem_type": "conduction",
  "thermal_conductivity": 237.0,
  "boundary_temperatures": [100, 25, 25, 25]
}
```

### 16. Core Gates — Fundamental Operations

Low-level quantum gate operations. Applications: custom circuits, benchmarking.

```json
{
  "domain": "core_gates",
  "num_qubits": 65536,
  "algorithm": "grover",
  "search_space_size": 64,
  "target_states": [42]
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
  -d '{"query":"INSERT INTO experiments VALUES (1, '\''chemistry'\'', -1.137, 0.9998)"}'

# Batch (multiple rows)
curl -X POST http://localhost:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query":"INSERT INTO experiments VALUES (1,'\''chem'\'',-1.1,0.99),(2,'\''phys'\'',-3.6,0.99)"}'
```

### 4. Bulk Import

```bash
curl -X POST http://localhost:8080/api/v1/bulk-import \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "table": "experiments",
    "columns": ["id", "domain", "energy", "fidelity"],
    "rows": [[1,"chemistry",-1.137,0.999],[2,"physics",-3.651,0.999]]
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
  -d '{"domain":"chemistry","num_qubits":65536,"molecule":"H2","bond_length":0.74}'
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

Simulate time-dependent quantum dynamics (Variational Quantum Simulation):

```bash
curl -X POST http://localhost:8080/api/v1/quantum/vqs/evolve \
  -H "Content-Type: application/json" \
  -d '{
    "num_qubits": 65536,
    "time_steps": 20,
    "dt_seconds": 0.05
  }'
```

Response includes state evolution snapshots at each time step.

---

## Pipeline Execution

The L1→L2→L3 pipeline processes data through encoding, tensor geometry, and VQE execution:

```bash
curl -X POST http://localhost:8080/api/v1/quantum/pipeline/execute \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "chemistry",
    "num_qubits": 65536,
    "molecule": "H2",
    "bond_length": 0.74
  }'
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
    "data_points": 64
  }'
```

---

## Running the Examples

### Files in this repository

| File | Description |
|------|-------------|
| `quantum_usage_examples.py` | All 16 domains + algorithms (Python) |
| `data_import_examples.py` | Auth, tables, import, query (Python) |
| `run_all_demos.sh` | Full demo runner (Bash) |
| `run_all_demos.ps1` | Full demo runner (PowerShell) |
| `README.md` | This documentation |

### Prerequisites

- **Server:** nawaz1-server binary running
- **Python:** 3.8+ with `requests` (`pip install requests`)
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
    "energy": -1.1372838,
    "converged": true,
    "iterations": 45,
    "fidelity": 0.9998,
    "num_qubits": 65536,
    "gate_count": 128
  },
  "metadata": {
    "execution_time_ms": 12.5,
    "tier": "free"
  }
}
```

---

## Support

- **Issues:** https://github.com/shah786628/nawaz1-quantum-software/issues
- **Author:** Shahnawaz Alam
