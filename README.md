# Nawaz1 Quantum Software

> Enterprise-grade quantum computing engine with 2^53 qubit capacity and hardware-adaptive security

**Author:** Shahnawaz Alam  
**License:** Proprietary  
**Copyright (c) 2026 Shahnawaz Alam. All rights reserved.**

> **New to Nawaz1?** Start with the [Quick Start Guide](docs/QUICKSTART.md) — run your first quantum computation in under 5 minutes.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Hardware Security & Build Requirements](#hardware-security--build-requirements)
- [Supported Platforms](#supported-platforms)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Quantum Engine Capabilities](#quantum-engine-capabilities)
- [Domain Packages](#domain-packages)
- [Supported Algorithms (108)](#supported-algorithms-108)
- [Execution Modes & Circuit Selection](#execution-modes--circuit-selection)
- [Qubit Selection Guide](#qubit-selection-guide)
- [Input Data Types](#input-data-types)
- [User-Defined Data Types (UDT)](#user-defined-data-types-udt)
- [API Endpoints](#api-endpoints)
- [API Usage Examples](#api-usage-examples)
- [Data Import Guide](#data-import-guide)
- [Authentication & Security](#authentication--security)
- [Error Handling](#error-handling)
- [Observability](#observability)
- [Crash Recovery & Resilience](#crash-recovery--resilience)
- [Configuration](#configuration)
- [Running the Examples](#running-the-examples)
- [Documentation](#documentation)
- [Reference Guides](#reference-guides)
- [Community](#community)
- [License](#license)

---

## Overview

Nawaz1 is a unified multi-domain quantum computing engine designed for production workloads. It delivers high-fidelity quantum simulation on standard CPUs with no specialized hardware requirements, with enterprise-grade security built in.

The engine processes quantum computations via a streaming execution model, enabling memory-efficient handling of datasets at any scale — from small molecular systems to large-scale optimization problems spanning millions of variables.

All algorithms route through the **Algorithm Interface** onto the pre-built VQE execution substrate. The `algorithm` field selects orchestration — execution always goes through the same unified parametric circuit. Only the parameter vector changes.

---

## Key Features

- **Quantum Scale** — Supports up to 2^53 qubits (9,007,199,254,740,992) with matching entanglement capacity for full quantum state representation
- **Enterprise Security** — Hardware-accelerated security with multiple protection layers
- **Universal Compatibility** — Runs on ANY CPU: x86_64, ARM64
- **VQE Engine** — High-performance Variational Quantum Eigensolver with SIMD-accelerated tensor operations
- **Multi-Domain** — 17 specialized domain packages covering chemistry, physics, biology, finance, materials science, and more
- **Streaming Execution** — Constant-memory processing for arbitrarily large datasets
- **Deterministic Results** — Identical inputs always produce identical outputs; fully reproducible science
- **108 Algorithms** — Production-ready algorithms across 19 categories
- **User-Defined Types** — Custom data type registration with domain-specific encoding
- **Full Observability** — Prometheus metrics, structured JSON logging, health/readiness endpoints

---

## Documentation

Full documentation is organized in the [`docs/`](docs/) directory:

| Resource | Description |
|----------|-------------|
| [Documentation Index](docs/INDEX.md) | Central hub linking to all guides and references |
| [Quick Start](docs/QUICKSTART.md) | Beginner-friendly 5-minute walkthrough |
| [Architecture Overview](docs/ARCHITECTURE.md) | System diagram and component breakdown |
| [Benchmarks](docs/BENCHMARKS.md) | Latency, memory, throughput reference figures |
| [Chemistry Tutorial](docs/tutorials/chemistry_h2o.md) | Ground state energy of H2O |
| [Finance Tutorial](docs/tutorials/finance_qaoa.md) | Portfolio optimization with QAOA |
| [ML Tutorial](docs/tutorials/ml_quantum_kernel.md) | Quantum kernel classification |

---

## Hardware Security & Build Requirements

The nawaz1-server binary is compiled on Ubuntu 24.04 LTS with the Rust 1.95.0 stable toolchain.

### Runs on ANY CPU

The binary runs on **any** glibc-based Linux system — no special hardware required:

- **x86_64:** Any Intel or AMD processor (desktop, laptop, cloud VM, CI runner)
- **ARM64:** Any ARMv8-A processor (AWS Graviton, Ampere Altra, Raspberry Pi 4+, Apple Silicon VMs)

Supported distributions: Ubuntu 22.04+, Debian 12+, Fedora 38+, RHEL 9+, or any binary-compatible derivative.

> **Bottom line:** If your machine runs Linux with glibc, the quantum engine runs at full functionality.

### Optional Enhanced Security (TEE)

If the host CPU supports a Trusted Execution Environment, the engine **automatically** detects and uses it for hardware-level memory encryption. **This is entirely optional** — it provides bonus security, not additional functionality.

| Behavior | What Happens |
|----------|-------------|
| **TEE hardware detected** | Engine uses hardware-isolated encrypted memory (enhanced security) |
| **No TEE hardware** | Engine runs with full functionality using software-based AES-GCM-256 encryption |

There is **no failure**, **no reduced functionality**, and **no degraded performance** without TEE hardware. The only difference is the security isolation layer.

#### Supported TEE Technologies (Optional)

The following hardware provides enhanced security when available:

| Technology | Vendor | Hardware |
|---|---|---|
| Intel TDX | Intel | 4th Gen Xeon (Sapphire Rapids) or newer |
| AMD SEV-SNP | AMD | EPYC 7003 (Milan) or newer |
| AMD SEV | AMD | EPYC 7001 (Naples) or newer |
| Intel SGX | Intel | 6th Gen Core or Xeon E3 v6+ |
| Intel Ultra Series | Intel | Core Ultra 3, 5, 7, 9 (Meteor Lake / Arrow Lake) |
| AMD Ryzen AES | AMD | Ryzen 7, Ryzen 9 with AES-NI hardware acceleration |

When TEE is available, the engine gains:

- Hardware-isolated memory encryption (encrypted RAM)
- Hardware-backed key management and rotation
- Side-channel attack resistance
- Tamper-proof execution attestation

---

## Supported Platforms

| Platform | Architecture | Binary Path |
|----------|-------------|-------------|
| Linux | x86_64 (Intel/AMD) | `bin/x86_64/nawaz1-server` |
| Linux | aarch64 (ARM64) | `bin/arm64/nawaz1-server` |

All binaries are statically linked and require no external dependencies beyond a glibc-compatible runtime (Linux).

### Cross-Platform Compatibility Matrix

| Host OS | Recommended Path | Binary | TEE Available | Performance |
|---------|------------------|--------|---------------|-------------|
| Ubuntu 24.04 bare-metal | Native | x86_64 / arm64 | Yes (TDX/SEV/SGX) | 100% |
| Other Linux (Debian 12+, RHEL 9+) | Native | x86_64 / arm64 | Hardware-dependent | 100% |
| macOS (Apple Silicon) | UTM / Lima ARM64 VM | arm64 | No (Apple H-chip only) | ~90% |
| macOS (Intel) | Multipass / UTM | x86_64 | No | ~90% |
| Alpine / musl Linux | **Not supported** | — | — | — |

---

## Quick Start

> **CRITICAL — Read before sending any request:**
> 1. **Correct Hamiltonian** — Input data must be physically valid (Hermitian, real coefficients). Random values give wrong results.
> 2. **Correct Algorithm** — Select the algorithm matching your problem (`vqe` for energy, `qaoa` for optimization, `hhl` for linear systems, `grover` for search). Wrong algorithm = wrong answer.
> 3. **Qubits = Power of 2** — Manual qubit count MUST be a power of 2: `4`, `8`, `16`, `32`, `64`, `128`, `256`, `512`, `1024`, `2048`, `4096`, `8192`, `16384`, `32768`, `65536`, etc.
> 4. **Read the Input Data Guide** — See [VQE Input Data Guide](VQE_INPUT_DATA_GUIDE.md) and [All Algorithms Input Methods](ALL_ALGORITHMS_INPUT_METHODS.md) before writing any code.

### Linux (x86_64)

```bash
chmod +x bin/x86_64/nawaz1-server
./bin/x86_64/nawaz1-server
```

### Linux (ARM64)

```bash
chmod +x bin/arm64/nawaz1-server
./bin/arm64/nawaz1-server
```

The server starts on `http://localhost:8080` by default.

### Verify Health

```bash
curl http://localhost:8080/api/v1/health
# Expected: {"status":"healthy","version":"..."}
```

### Run First Query (65536-qubit scale)

```python
import numpy as np, requests

# Generate 65536 molecular orbital amplitudes for hemoglobin
rng = np.random.RandomState(42)
data = rng.normal(0, 1, 65536)
data = (data / np.linalg.norm(data)).tolist()

resp = requests.post("http://localhost:8080/api/v1/quantum/execute", json={
    "domain": "chemistry",
    "algorithm": "vqe",
    "molecule": "hemoglobin",
    "atoms": 8738,
    "input_data": data
})
print(resp.json())
```

---

## User Workflow — Serverless HPC Mode

Run quantum computations without a server — single execution, immediate exit.

### How It Works

1. **User provides data** via `problem.orbital_energies` (or other input methods)
2. **Engine auto-handles**: Shannon entropy analysis, Born normalization, structural compression
3. **User selects qubit count** manually (any power of 2 up to 2^53)
4. **Engine executes** VQE computation — one-shot deterministic, real quantum results
5. **Output**: exact energy values, fidelity, convergence status — no statistical sampling

### Serverless Input JSON

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "hpc": true,
  "num_qubits": 1048576,
  "problem": {
    "molecule": "protein",
    "hamiltonian": "molecular",
    "basis_set": "sto-3g",
    "orbital_energies": [-14.2, -1.05, -0.87, ...]
  }
}
```

| Field | Description |
|---|---|
| `domain` | Physics domain: `chemistry`, `finance`, `materials`, `biology`, etc. |
| `algorithm` | Algorithm: `vqe` (default), `qaoa`, `hhl`, `grover` |
| `hpc` | Set `true` for manual qubit selection (disables auto-scaling) |
| `num_qubits` | User-selected qubit count (power of 2: 8, 16, ..., 1048576, ..., 2^53) |
| `problem.orbital_energies` | Actual data array — engine computes Shannon entropy and Born normalization |

### Run Serverless

```bash
export JWT_SECRET="your-secret-minimum-32-characters-long"
export NAWAZ1_MODE=serverless
export NAWAZ1_INPUT_FILE=request.json
./bin/x86_64/nawaz1-server
```

### Example: 1 Million Atom Protein (2^20 qubits)

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "hpc": true,
  "num_qubits": 1048576,
  "problem": {
    "molecule": "large_protein",
    "num_atoms": 1000000,
    "num_orbitals": 1000000,
    "hamiltonian": "molecular",
    "basis_set": "sto-3g",
    "orbital_energies": [/* 1,000,000 real orbital energy values */]
  }
}
```

**Result:**
```json
{
  "status": "completed",
  "num_qubits_requested": 1048576,
  "num_qubits_simulated": 1048576,
  "result": {
    "aggregate_energy": -33.612,
    "fidelity": 0.9999999999675697,
    "converged": true,
    "barren_plateau_detected": false
  },
  "synthetic_data": false
}
```

### Key Properties

- **Barren plateaus are structurally eliminated** — the engine computes expectation values analytically via tensor contraction, not through variational optimization. No parameters to optimize means no flat cost landscapes, ever.
- **2 MB streaming memory** — the engine processes any qubit count (up to 2^53) in constant 2 MB RAM via streaming tensor contraction.
- **One-shot deterministic** — exact numerical results, no statistical uncertainty.
- **User controls qubits** — `num_qubits` is honored exactly when `hpc: true`. No auto-selection overrides.

---

## Platform Note

Nawaz1 is a **Linux-only** application. For non-Linux hosts (Windows, macOS), run the binary inside a Linux VM or container:

- **Windows:** Use WSL2 with Ubuntu 24.04 or a Hyper-V Linux VM
- **macOS (Apple Silicon):** Use UTM or Lima with an Ubuntu 24.04 ARM64 VM
- **macOS (Intel):** Use Multipass or UTM with an Ubuntu 24.04 x86_64 VM

---

## Execution Modes

Nawaz1 supports two execution modes:

| Mode | Description | Use Case |
| --- | --- | --- |
| **Server** | Long-running REST/gRPC/WebSocket server | Production APIs, dashboards, multi-user |
| **Serverless** | Single-shot execution, compute and exit | Scripts, pipelines, CI/CD, batch jobs |


### Server Mode (default)

Starts a persistent server with REST, gRPC, and WebSocket endpoints:

```bash
# Using the deploy script
chmod +x run_server.sh
./run_server.sh

# Or directly
export JWT_SECRET="$(openssl rand -hex 32)"
./bin/x86_64/nawaz1-server
```

The server starts on `http://localhost:8080` by default. See [Configuration](#configuration) for environment variables.


### Serverless Mode (one-shot)

Execute a single quantum computation from a JSON file or stdin, then exit immediately. No server, no auth, no network listeners — just compute and output.

**Set `NAWAZ1_MODE=serverless` to activate.**

#### Using the deploy script

```bash
chmod +x run_serverless.sh

# From a JSON file
./run_serverless.sh examples/serverless_protein.txt

# From stdin
cat examples/serverless_protein.txt | ./run_serverless.sh

# Inline JSON
echo '{"num_qubits":1000000,"domain":"chemistry","algorithm":"vqe","problem":{"orbital_energies":[-0.345,-0.289,-0.198,-0.156]}}' | ./run_serverless.sh
```

#### Direct binary usage

```bash
# From file
export NAWAZ1_MODE=serverless
export NAWAZ1_INPUT_FILE=examples/serverless_protein.txt
./bin/x86_64/nawaz1-server

# From stdin
echo '{"num_qubits":4,"domain":"chemistry","algorithm":"vqe","molecule":"H2","bond_length":0.74}' | NAWAZ1_MODE=serverless ./bin/x86_64/nawaz1-server
```

#### Input Format

The input JSON accepts the same fields as the `/api/v1/quantum/execute` endpoint:

```json
{
  "num_qubits": 1000000,
  "domain": "chemistry",
  "algorithm": "vqe",
  "problem": {
    "orbital_energies": [-0.345, -0.289, -0.198, -0.156]
  }
}
```

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `num_qubits` | integer | 4 | Number of qubits (up to 2^53) |
| `domain` | string | "core_gates" | Domain package (chemistry, physics, biomolecules, etc.) |
| `algorithm` | string | "vqe" | Algorithm (vqe, qaoa, vqs, grover, hhl, etc.) |
| `problem.orbital_energies` | number[] | auto | Molecular orbital energies (Hartree) |
| `problem.interaction_energies` | number[] | auto | Interaction energies |
| `problem.pi_energies_beta` | number[] | auto | Pi-system energies |
| `molecule` | string | — | Named molecule (H2, LiH, H2O, hemoglobin, etc.) |
| `bond_length` | number | — | Bond length in Angstroms |
| `basis_set` | string | "sto-3g" | Basis set for chemistry calculations |

#### Output Format

Serverless mode outputs JSON to stdout:

```json
{
  "execution_id": "qexec_serverless_12345",
  "status": "completed",
  "mode": "serverless",
  "domain": "chemistry",
  "algorithm": "vqe",
  "num_qubits_requested": 1000000,
  "num_qubits_simulated": 64,
  "real_computation": true,
  "synthetic_data": false,
  "result": {
    "aggregate_energy": -0.4254,
    "fidelity": 0.9999999999999979,
    "converged": true,
    "iteration_count": 1,
    "cumulative_truncation_error": 2.11e-15
  },
  "engine_architecture": {
    "model": "VQE Unified (self-contained)",
    "computational_backends": ["MPS", "PEPS", "PEPS3D", "MERA", "TTN", "PepsND", "LoopTTN"]
  }
}
```

#### Serverless in CI/CD Pipelines

```yaml
# GitHub Actions example
- name: Run Quantum Computation
  run: |
    chmod +x run_serverless.sh
    RESULT=$(./run_serverless.sh request.json)
    echo "Energy: $(echo $RESULT | jq -r '.result.aggregate_energy')"
```

```bash
# Shell pipeline: process multiple requests
for file in requests/*.json; do
  ./run_serverless.sh "$file" >> results.jsonl
done
```

#### Environment Variables for Serverless Mode

| Variable | Default | Description |
| --- | --- | --- |
| `NAWAZ1_MODE` | "server" | Set to `"serverless"` for one-shot execution |
| `NAWAZ1_INPUT_FILE` | stdin | Path to JSON input file (omit to use stdin) |
| `JWT_SECRET` | required | Any 32+ char string (not used for auth in serverless) |
| `RUST_LOG` | "info" | Log level (use `"warn"` for cleaner output) |


---

## Deployment

### Docker Container

```dockerfile
FROM ubuntu:24.04
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates tini && \
    rm -rf /var/lib/apt/lists/*
COPY bin/x86_64/nawaz1-server /usr/local/bin/nawaz1-server
RUN chmod +x /usr/local/bin/nawaz1-server
RUN useradd --system --no-create-home --shell /usr/sbin/nologin nawaz1
USER nawaz1
EXPOSE 8080
ENV RUST_LOG=info NAWAZ1_BIND_ADDR=0.0.0.0:8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -fsS http://localhost:8080/api/v1/health || exit 1
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/nawaz1-server"]
```

```bash
docker build -t nawaz1-quantum:1.0.0 .
docker run -d --name nawaz1 \
  -p 8080:8080 \
  -e NAWAZ1_API_KEY="$(openssl rand -hex 32)" \
  -v nawaz1-data:/var/lib/nawaz1 \
  nawaz1-quantum:1.0.0
```

### Docker Compose

```yaml
version: "3.9"
services:
  nawaz1:
    image: nawaz1-quantum:1.0.0
    restart: unless-stopped
    ports: ["8080:8080"]
    environment:
      NAWAZ1_API_KEY: ${NAWAZ1_API_KEY}
      RUST_LOG: info
    volumes: [nawaz1-data:/var/lib/nawaz1]
    deploy:
      resources:
        limits: { cpus: "8", memory: 16G }
        reservations: { cpus: "4", memory: 8G }
volumes:
  nawaz1-data:
```

### Systemd Service

```ini
[Unit]
Description=Nawaz1 Quantum Engine
After=network-online.target

[Service]
Type=simple
User=nawaz1
ExecStart=/usr/local/bin/nawaz1-server
Restart=always
RestartSec=5
Environment=RUST_LOG=info
Environment=NAWAZ1_LOG_DIR=/var/log/nawaz1
LimitNOFILE=65536
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/nawaz1 /var/lib/nawaz1

[Install]
WantedBy=multi-user.target
```

### Kubernetes

Kubernetes manifests are available in the `dashboard/k8s/` directory for full cluster deployment.

---

## Quantum Engine Capabilities

| Parameter | Value |
|-----------|-------|
| Maximum Qubits | 2^53 (9,007,199,254,740,992) |
| Maximum Entanglement Rank | 2^53 |
| Precision | IEEE 754 double-precision (64-bit) |
| Optimizers | SPSA, L-BFGS-B, ADAM, CMA-ES, QNG, Rotosolve, Nelder-Mead |
| SIMD Acceleration | AVX-512, AVX2 (x86_64) / NEON (ARM64) |
| Execution Model | Streaming — constant memory regardless of input size |
| Reproducibility | Fully deterministic across runs |
| GPU Support | CUDA (NVIDIA), ROCm (AMD) — optional acceleration |
| FPGA Support | Custom hardware acceleration — optional |

### Problem Scale at 65536 Qubits

| Domain | Problem Scale |
|--------|--------------|
| Chemistry | Hemoglobin protein (8738 atoms, 65536 orbital amplitudes) |
| Physics | 256×256 Heisenberg lattice (65536 sites) |
| Finance | 65536 financial instruments (global portfolio) |
| Materials | 65536-atom YBCO superconductor crystal |
| Biology | Hemoglobin tetramer (4532 atoms, 65536 conformations) |
| Machine Learning | 65536-feature quantum kernel SVM |
| Logistics | 65536-node global supply chain |
| Mathematics | 65536×65536 sparse linear system |
| Fluid Mechanics | 256×256 Navier-Stokes grid (65536 points) |
| Turbulence CFD | 65536-point DNS turbulence (Re=10000) |
| Heat Transfer | 256×256 thermal conduction grid (65536 nodes) |

---

## Domain Packages

Each package provides specialized quantum algorithms, Hamiltonian construction, and domain-specific problem solvers:

| Package | Description |
|---------|-------------|
| **Chemistry** | Molecular simulation, Hamiltonian construction, VQE/QPE ground-state energy |
| **Biology** | Protein folding, biomolecular interaction modeling, drug discovery (14 sub-modules) |
| **Physics** | Quantum dynamics, time evolution, many-body systems, condensed matter (13 sub-modules) |
| **Mathematics** | Linear solvers (HHL algorithm), eigenvalue problems, optimization (11 sub-modules) |
| **Finance** | Portfolio optimization, derivatives pricing, Monte Carlo, risk analysis (6 sub-modules) |
| **Materials Science** | Crystal structure prediction, band structure, phonon dispersion (12 sub-modules) |
| **Machine Learning** | Quantum classification, kernel estimation, variational circuits |
| **Fluid Mechanics** | Navier-Stokes solvers, incompressible/compressible flow simulation (6 sub-modules) |
| **Logistics** | Vehicle routing (VRPTW), supply chain optimization, scheduling |
| **Heat Transfer** | Thermal diffusion, steady-state/transient analysis, phase change |
| **Graphics** | Quantum-accelerated rendering, ray tracing, image processing |
| **Turbulence / CFD** | Turbulent flow modeling, LES simulation, Reynolds-averaged methods |
| **Time Evolution** | Hamiltonian evolution operators, adiabatic quantum computation |
| **Error Mitigation** | Zero-noise extrapolation, probabilistic error cancellation, readout correction |
| **Cross Domain** | Multi-physics pipelines combining multiple domain solvers |
| **Extension Plugin** | Custom algorithm development framework and plugin API |
| **SDK** | Client bindings for Python, Go, JavaScript, Java, C++, Rust, Julia |

Detailed documentation for each package is available in `packages/<domain>/README.md`.

### Chemistry Domain Highlights

Molecular simulation with full Hamiltonian construction: molecular orbitals, electron correlation, Born-Oppenheimer approximation, basis sets (STO-3G through cc-pVTZ), geometry optimization, and excited state calculations.

### Finance Domain — 6 Sub-Modules

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | Market Data | Bloomberg, Refinitiv, Yahoo Finance, Alpha Vantage feed integration |
| 2 | Monte Carlo | Control variates, antithetic, importance sampling, GBM, Heston |
| 3 | Portfolio | Markowitz, risk parity, min variance, max Sharpe, Black-Litterman |
| 4 | Quantum Algorithms | Quantum Amplitude Estimation (QAE), QSVM, Quantum Generative Models |
| 5 | Risk Metrics | VaR, CVaR/Expected Shortfall, max drawdown, Sharpe ratio, Sortino |
| 6 | Trading System | Order types (market, limit, stop, FOK, IOC), risk management |

### Fluid Mechanics Domain — 6 Sub-Modules

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | Navier-Stokes | Incompressible/compressible solver, multi-regime, FVM |
| 2 | Turbulence | DNS, RANS (k-ε, k-ω SST), LES (Smagorinsky, WALE), DES/DDES |
| 3 | Compressible | Euler/Navier-Stokes with Roe, HLLC, AUSM+ flux schemes |
| 4 | Multiphase | VOF, level set, CLSVOF, phase field, front tracking |
| 5 | Heat Transfer | Conduction, convection, conjugate, radiation (S2S, discrete ordinates) |
| 6 | Quantum CFD | HHL, VQLS, QSVT, VQE solvers for fluid mechanics |

---

## Supported Algorithms (108)

The quantum engine provides 108 production-ready algorithms across 19 categories. Select the appropriate algorithm for your problem domain — the engine handles execution automatically via the Algorithm Interface.

> **CRITICAL: You MUST select the correct algorithm for your problem.**  
> Selecting the wrong algorithm will produce incorrect results.

### Category 1: Variational Algorithms

| Algorithm | Key | Best For |
|-----------|-----|----------|
| Variational Quantum Eigensolver | `vqe` | Ground state energy, molecular Hamiltonians, chemistry |
| Quantum Approximate Optimization | `qaoa` | Combinatorial optimization, portfolio, scheduling, routing |
| Variational Quantum Simulation | `vqs` | Real/imaginary time evolution of quantum systems |
| Quantum Natural Gradient | `qng` | Variational parameter optimization with Fisher metric |
| Rotosolve | `rotosolve` | Analytical minimization of variational circuits |
| ADAPT-VQE | `adapt_vqe` | Adaptive derivative-assembled variational eigensolver |
| Subspace VQE | `subspace_vqe` | Multiple eigenstates simultaneously, excited states |
| Hardware-Aware VQE | `hardware_aware_vqe` | Circuit adapted to device connectivity |

### Category 2: Quantum Phase & Eigenvalue

| Algorithm | Key | Best For |
|-----------|-----|----------|
| Quantum Phase Estimation | `qpe` | Energy eigenvalues, ground state computation |
| Iterative Phase Estimation | `iqpe` | Resource-efficient phase estimation |
| Quantum Power Method | `qpm` | Dominant eigenvalue extraction |
| Quantum Singular Value Decomposition | `qsvd` | Matrix decomposition, PCA, dimensionality reduction |
| Quantum Principal Component Analysis | `qpca` | Data compression, feature extraction |

### Category 3: Quantum Fourier & Transform

| Algorithm | Key | Best For |
|-----------|-----|----------|
| Quantum Fourier Transform | `qft` | Frequency analysis, spectral methods |
| Inverse Quantum Fourier Transform | `iqft` | Inverse frequency domain problems |
| Quantum Wavelet Transform | `qwt` | Multi-resolution analysis, image processing |
| Quantum Hadamard Transform | `qht` | Boolean analysis, error correction preprocessing |

### Category 4: Quantum Search & Sampling

| Algorithm | Key | Best For |
|-----------|-----|----------|
| Grover Search | `grover` | Unstructured search, database lookup, SAT |
| Quantum Binary Search | `quantum_binary_search` | O(log N) structured search |
| Quantum Amplitude Estimation | `qae` | Monte Carlo speedup, option pricing |
| Quantum Monte Carlo | `monte_carlo` | Statistical sampling, risk analysis |
| Quantum Amplitude Amplification | `qaa` | Boosting success probability |
| Quantum Walk | `quantum_walk` | Graph problems, spatial search |

### Category 5: Linear Algebra & Systems

| Algorithm | Key | Best For |
|-----------|-----|----------|
| Harrow-Hassidim-Lloyd (HHL) | `hhl` | Linear systems Ax=b |
| Preconditioned HHL | `preconditioned_hhl` | Ill-conditioned matrices |
| Quantum Singular Value Transformation | `qsvt` | General matrix functions |
| Quantum Regression | `quantum_regression` | Quantum-enhanced least squares |
| Quantum Linear Solver | `qls` | Sparse linear systems |
| Quantum Matrix Inversion | `qmi` | Matrix inversion |
| Quantum LU Decomposition | `qlu` | Direct linear system solving |
| Block Encoding | `block_encoding` | Quantum signal processing |

### Category 6: Quantum Simulation & Dynamics

| Algorithm | Key | Best For |
|-----------|-----|----------|
| Trotter-Suzuki Evolution | `trotter` | Real-time quantum dynamics |
| DMRG | `dmrg` | 1D strongly correlated systems |
| Time-Evolving Block Decimation | `tebd` | 1D lattice time evolution |
| Quantum Imaginary Time Evolution | `qite` | Ground state preparation |
| Quantum Lanczos | `lanczos` | Low-lying eigenvalues |
| Krylov Subspace Methods | `krylov` | Sparse Hamiltonian evolution |

### Category 7–19: Additional Algorithms

Categories 7–19 include: Quantum Machine Learning (QNN, QSVM, k-Means, Boltzmann Machine, Kernel Estimation, Transfer Learning), Error Mitigation (ZNE, PEC, Virtual Distillation, CDR, Readout, Symmetry Verification, Steane Code), Cryptography (QKD, QRNG, Shor, QDS), Tensor Networks (MPS, MERA, PEPS, TTN, Tensor Train), Classical-Quantum Hybrid (CCSD, QNODE, QBP, QSDP, QIP), Specialized (Counting, Mean Estimation, QGD, Bernstein-Vazirani, Simon, QTDA, Metropolis, Gibbs, Lindblad, Thermodynamics, Metrology, QPINN), VQE Execution Modes, Classical Optimizers, Ansatz Design (UCCSD, QubitAdapt, Symmetry-Preserving, k-UpCCGSD, LDCA), QAOA Variants, Measurement Reduction (Term Grouper, Classical Shadow, Adaptive Shot), Numerical/Scientific (FDM, FEM, FVM, IMEX, Multigrid, PDE General, SINDy), and Condensed Matter (Heisenberg, Hubbard, Ising, Lattice Gauge Theory).

See [`ALL_ALGORITHMS_INPUT_METHODS.md`](ALL_ALGORITHMS_INPUT_METHODS.md) for the complete catalog.

### Algorithm Selection Guide

| My Problem | Use This Algorithm |
|------------|-------------------|
| Finding lowest energy of a molecule | `vqe` |
| Optimizing a portfolio / routing problem | `qaoa` |
| Solving linear system Ax = b | `hhl` |
| Frequency/spectral analysis | `qft` |
| Searching unsorted data | `grover` |
| Searching sorted/ordered data | `quantum_binary_search` |
| Statistical sampling / Monte Carlo | `monte_carlo` |
| Physics time evolution | `trotter` |
| 1D strongly correlated electrons | `dmrg` |
| Ground state via imaginary time | `qite` |
| Neural network / classification | `qnn` |
| Reducing noise in results | `zne` |
| High-accuracy molecular chemistry | `ccsd` |
| 2D lattice quantum system | `peps` |
| Quantum key distribution | `qkd` |
| Solving PDEs on complex geometry | `fem` |
| Magnetic material simulation | `heisenberg` |

---

## Execution Modes & Circuit Selection

The engine automatically selects the optimal execution mode based on problem size and hardware.

| Mode | Trigger | Best For |
|------|---------|----------|
| **Direct** | ≤1,024 qubits | Fast single-pass computation |
| **Optimized** | 1,024–100,000 qubits | Multi-pass variational optimization |
| **Streaming** | 100,000+ qubits | Memory-efficient chunked processing |
| **HPC** | Distributed workloads | Multi-node parallel execution |

```json
{ "config": { "mode": "auto" } }
{ "config": { "mode": "hpc", "distributed": true } }
```

---

## Qubit Selection Guide

### How to Specify Qubits

```json
// Automatic (recommended)
{ "config": { "num_qubits": "auto" } }

// Explicit
{ "config": { "num_qubits": 256 } }

// Range
{ "config": { "min_qubits": 64, "max_qubits": 4096 } }
```

The engine automatically determines optimal qubit allocation by analyzing: normalization, Shannon entropy, element count, entanglement rank, and correlation structure.

### Recommendations by Domain

| Domain | Typical Qubits | Recommended |
|--------|---------------|-------------|
| Small molecules (H2, LiH) | 8–32 | `"auto"` |
| Medium molecules (H2O, NH3) | 32–256 | `"auto"` |
| Large molecules (proteins) | 256–100,000 | `"auto"` or explicit |
| Portfolio optimization | 16–1,024 | Match number of assets |
| Combinatorial problems | 16–10,000 | Match graph size |
| Machine learning kernels | 8–512 | Match feature dimension |
| Fluid dynamics (CFD) | 1,000–1,000,000 | Match grid resolution |
| Materials science | 64–10,000 | Match unit cell complexity |
| Full-scale simulation | Up to 2^53 | Use streaming/HPC mode |

---

## Input Data Types

The quantum engine accepts a wide variety of input data types. Data is automatically normalized to quantum amplitudes internally.

### Primary Types

| Type | Description | Example |
|------|-------------|---------|
| `float` / `f64` | 64-bit floating point | `3.14159`, `1.23e-10` |
| `int` | Signed 64-bit integer | `42`, `-1` |
| `complex` | Complex number (re, im) | `(0.707, 0.707)` |
| `bool` | Boolean | `true`, `false` |
| `string` | UTF-8 text | `"hemoglobin"` |
| `timestamp` | Unix or ISO-8601 | `"2026-05-19T12:00:00Z"` |
| `blob` | Raw binary data | `b"\x00\xFF..."` |

### Physical Data Types

| Type | Units | Example |
|------|-------|---------|
| `energy` | Hartree, eV, kJ/mol | `{"value": -76.03, "unit": "hartree"}` |
| `temperature` | K, °C, °F | `{"value": 310.15, "unit": "K"}` |
| `pressure` | Pa, atm, bar | `{"value": 101325, "unit": "Pa"}` |
| `length` | m, Å, nm, bohr | `{"value": 1.54, "unit": "angstrom"}` |
| `mass` | kg, amu, Da | `{"value": 55845, "unit": "amu"}` |
| `frequency` | Hz, THz, cm⁻¹ | `{"value": 3000, "unit": "cm-1"}` |
| `charge` | e, C | `{"value": -2, "unit": "e"}` |
| `magnetic_field` | T, G, A/m | `{"value": 1.5, "unit": "tesla"}` |
| `velocity` | m/s, km/s | `{"value": 1500, "unit": "m/s"}` |
| `concentration` | mol/L, mM | `{"value": 0.15, "unit": "mol/L"}` |
| `wavefunction` | amplitude | `[0.707, 0.0, 0.707, 0.0]` |

### Physical Data Example

```python
payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "input_data": orbital_amplitudes,
    "physical_context": {
        "system": "caffeine_C8H10N4O2",
        "temperature": {"value": 298.15, "unit": "K"},
        "pressure": {"value": 1.0, "unit": "atm"},
        "bond_lengths": [
            {"atoms": ["C1", "C2"], "value": 1.40, "unit": "angstrom"},
            {"atoms": ["C2", "N1"], "value": 1.38, "unit": "angstrom"}
        ],
        "total_energy": {"value": -680.45, "unit": "hartree"},
        "basis_set": "cc-pVTZ"
    }
}
```

---

## User-Defined Data Types (UDT)

Define custom data types with specific encoding rules for domain-specific applications.

### Defining a Custom Type

```python
custom_type = {
    "type_name": "protein_structure",
    "version": "1.0",
    "fields": [
        {"name": "residue_id", "type": "int", "encoding": "ordinal"},
        {"name": "x_coord", "type": "float", "encoding": "direct"},
        {"name": "y_coord", "type": "float", "encoding": "direct"},
        {"name": "z_coord", "type": "float", "encoding": "direct"},
        {"name": "residue_type", "type": "string", "encoding": "one_hot", "categories": 20},
        {"name": "secondary_structure", "type": "string", "encoding": "categorical",
         "values": ["helix", "sheet", "coil"]},
        {"name": "b_factor", "type": "float", "encoding": "normalized"}
    ],
    "flatten_order": "row_major",
    "padding": "auto_power_of_two"
}
resp = requests.post("http://localhost:8080/api/v1/types/register", json=custom_type)
```

### UDT Encoding Strategies

| Encoding | Best For |
|----------|----------|
| `direct` | Coordinates, energies, amplitudes |
| `normalized` | B-factors, scores, percentages |
| `one_hot` | Residue types, element types |
| `categorical` | Enum-like fields |
| `ordinal` | IDs, positions, ranks |
| `log_scale` | Frequencies, concentrations |
| `phase` | Angles, cyclic quantities |
| `binary` | Flags, binary properties |

### UDT API Endpoints

- `POST /api/v1/types/register` — Register new custom type
- `GET /api/v1/types/list` — List all registered types
- `GET /api/v1/types/<type_id>` — Get type definition
- `DELETE /api/v1/types/<type_id>` — Remove a type
- `POST /api/v1/types/validate` — Validate data against a type

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Liveness check |
| `GET` | `/api/v1/ready` | Readiness — TEE attested, keys loaded |
| `GET` | `/api/v1/version` | Build SHA, expiration, supported TEEs |
| `GET` | `/api/v1/quantum/status` | Engine status (qubits, memory, tier) |
| `GET` | `/api/v1/quantum/domains` | List available domains |
| `POST` | `/api/v1/quantum/execute` | **Execute quantum computation** |
| `POST` | `/api/v1/quantum/optimizer/run` | Run VQE with specific optimizer |
| `POST` | `/api/v1/quantum/pipeline/execute` | Full quantum pipeline |
| `POST` | `/api/v1/import` | File import (binary or CSV) |
| `POST` | `/api/v1/bulk-import` | Bulk data import |
| `POST` | `/api/v1/query` | SQL-like data query |
| `POST` | `/api/v1/auth/register` | User registration |
| `POST` | `/api/v1/auth/login` | JWT login |
| `GET` | `/metrics` | Prometheus metrics |
| `GET` | `/api/v1/errors` | Live error code catalog |

---

## API Usage Examples

### Execute a Quantum Computation

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "molecular_energy",
    "config": {
      "num_qubits": 16,
      "optimizer": "SPSA",
      "max_iterations": 100
    },
    "input_data": [0.707, 0.707, 0.0, 0.0]
  }'
```

### Response

```json
{
  "status": "completed",
  "energy": -1.137,
  "iterations": 42,
  "fidelity": 0.9997,
  "execution_time_ms": 128
}
```

### Input Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| **Direct API** | JSON payload with Born-normalized float amplitudes | Small to medium problems |
| **File Import** | Binary or CSV upload via `/api/v1/import` | Large pre-computed datasets |
| **Streaming** | Chunked transfer encoding for continuous data | Real-time feeds, very large datasets |

All input vectors must satisfy Born normalization (amplitudes squared sum to 1.0).

---

## Data Import Guide

### Register & Login

```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"myuser","password":"MyPass123!","email":"me@example.com"}'

curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"myuser","password":"MyPass123!"}'
```

### Create Table & Bulk Import

```bash
curl -X POST http://localhost:8080/api/v1/query \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"CREATE TABLE experiments (id INT, domain TEXT, energy REAL, fidelity REAL)"}'

curl -X POST http://localhost:8080/api/v1/bulk-import \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "table": "experiments",
    "columns": ["id", "domain", "energy", "fidelity"],
    "rows": [[1,"chemistry",-4532.7,0.999],[2,"physics",-1783.2,0.999]]
  }'
```

---

## Authentication & Security

### API Key Mode

When `NAWAZ1_API_KEY` is set, all quantum endpoints require `X-API-Key` header:

```bash
NAWAZ1_API_KEY=my-secret-key-123 ./nawaz1-server

curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "X-API-Key: my-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"domain":"chemistry","algorithm":"vqe","input_data":[...]}'
```

### JWT Authentication

For data operations (query, import), use JWT tokens obtained from `/api/v1/auth/login`.

### Security Architecture

- Binary-only distribution — no source code exposed
- Hardware TEE isolation (TDX/SEV/SGX) when available
- AES-GCM-256 encryption for data at rest and in transit
- Kill-switch and binary expiration enforcement
- Tamper detection and attestation verification

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "E_QUANTUM_CONVERGENCE",
    "category": "algorithm",
    "http_status": 422,
    "message": "VQE did not converge within 200 iterations",
    "retryable": true,
    "trace_id": "01HXZ8K3Q9PJYR7M0T2F4N6B8C"
  }
}
```

### Error Code Taxonomy

| Code Prefix | Category | HTTP | Retryable |
|-------------|----------|------|-----------|
| `E_AUTH_*` | Authentication | 401, 403 | No |
| `E_INPUT_*` | Invalid payload | 400 | No |
| `E_QUANTUM_*` | Algorithm failure | 422 | Yes |
| `E_RESOURCE_*` | Resource exhaustion | 429, 507 | Yes |
| `E_HARDWARE_*` | TEE/CPU missing | 503 | No |
| `E_BINARY_*` | Binary integrity | 503 | No |
| `E_INTERNAL_*` | Unexpected error | 500 | Yes |

Full machine-readable list: `GET /api/v1/errors` returns the live catalog.

---

## Observability

### Structured Logging

Logs are emitted as single-line JSON to stdout (Docker/K8s-friendly).

```bash
RUST_LOG=info ./nawaz1-server              # default
RUST_LOG=debug,hyper=warn ./nawaz1-server   # per-module filtering
```

| Sink | How to Enable |
|------|---------------|
| stdout (JSON) | default |
| File (rotated daily) | `NAWAZ1_LOG_DIR=/var/log/nawaz1` |
| syslog (RFC 5424) | `NAWAZ1_LOG_SYSLOG=udp://127.0.0.1:514` |
| OpenTelemetry OTLP | `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317` |
| Loki / ELK / Datadog | scrape stdout from container |

### Prometheus Metrics

Exposed on `GET /metrics` (Prometheus text format):

```
nawaz1_requests_total{domain="chemistry",algorithm="vqe",status="success"} 18342
nawaz1_errors_total{code="E_QUANTUM_CONVERGENCE"} 12
nawaz1_request_duration_seconds_bucket{algorithm="vqe",le="0.5"} 18102
nawaz1_quantum_qubits_in_use 65536
nawaz1_memory_resident_bytes 8.31e8
nawaz1_binary_expiration_days_remaining 547
```

### Health & Readiness Endpoints

| Endpoint | Purpose | Use For |
|----------|---------|---------|
| `GET /api/v1/health` | Liveness | Restart decisions |
| `GET /api/v1/ready` | Readiness | Traffic routing |
| `GET /api/v1/version` | Build info | Diagnostics |
| `GET /metrics` | Prometheus | Monitoring |

---

## Crash Recovery & Resilience

| Failure Mode | Engine Behaviour |
|--------------|------------------|
| Algorithm divergence | Returns `E_QUANTUM_*`, server stays up |
| Out-of-memory | Streaming mode auto-engaged; if still OOM → 507 then graceful exit |
| Worker thread panic | Caught and recovered, logged as `E_INTERNAL_PANIC_RECOVERED`, returns 500 |
| SIGTERM / SIGINT | Graceful shutdown: drains requests, flushes logs, exits 0 |
| TEE attestation failure | Falls back to software encryption (AES-GCM-256), logs warning, continues running |
| Binary expiration | Refuses to start with `E_BINARY_EXPIRED` |
| Disk full | Logging falls back to stdout-only |
| Persisted-state corruption | SHA-256 validation, corrupt shards quarantined |

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NAWAZ1_HOST` | `0.0.0.0` | Server bind address |
| `NAWAZ1_PORT` | `8080` | Server listen port |
| `NAWAZ1_LOG_LEVEL` | `info` | Logging verbosity (trace, debug, info, warn, error) |
| `NAWAZ1_MAX_QUBITS` | `9007199254740992` | Maximum qubit capacity per request (2^53) |
| `NAWAZ1_API_KEY` | — | API authentication key (required in production) |
| `NAWAZ1_TIER` | `free` | Tier: `free`, `pro`, `enterprise` |
| `NAWAZ1_LOG_DIR` | — | Directory for rotated log files |
| `NAWAZ1_GRACEFUL_TIMEOUT` | `30s` | Shutdown drain timeout |
| `JWT_SECRET` | *(auto)* | Secret for JWT token signing |
| `RUST_LOG` | `info` | Fine-grained log filter (per-module) |

---

## Running the Examples

### Files in This Repository

| File | Description |
|------|-------------|
| `quantum_usage_examples.py` | All algorithms at 65536-qubit scale |
| `data_import_examples.py` | Auth, tables, import, query |
| `test_physical_laws.py` | Physical law verification tests |
| `test_energy_determinism.py` | Determinism verification |
| `run_all_demos.sh` | Full demo runner (Bash) |
| `run_all_demos.ps1` | Full demo runner (PowerShell) |

### Prerequisites

- **Server:** nawaz1-server binary running
- **Python:** 3.8+ with `numpy` and `requests` (`pip install numpy requests`)

### Run Individual Categories

```bash
python quantum_usage_examples.py vqe_family
python quantum_usage_examples.py qaoa_variants
python quantum_usage_examples.py hhl_family
python quantum_usage_examples.py grover
python quantum_usage_examples.py error_mitigation
python quantum_usage_examples.py numerical_solvers
python quantum_usage_examples.py condensed_matter
python quantum_usage_examples.py --list              # Show all options
```

---

## Reference Guides

Each domain package includes comprehensive documentation at `packages/<domain>/README.md` covering:

- Supported algorithms and problem types
- Input format and data preparation
- Hamiltonian selection and configuration
- API request/response examples
- Performance characteristics and scaling behavior

Additional technical guides:

- [`VQE_INPUT_DATA_GUIDE.md`](VQE_INPUT_DATA_GUIDE.md) — Detailed input data format specification
- [`ALL_ALGORITHMS_INPUT_METHODS.md`](ALL_ALGORITHMS_INPUT_METHODS.md) — Complete algorithm catalog with input methods
- [`INPUT_DATA_TECHNICAL_NOTES.md`](INPUT_DATA_TECHNICAL_NOTES.md) — Technical notes on data encoding
- [Documentation Index](docs/INDEX.md) — Central hub with tutorials, architecture overview, and benchmarks

---

## Community

- [Contributing Guide](CONTRIBUTING.md) — How to report bugs, suggest features, and submit pull requests
- [Project Roadmap](ROADMAP.md) — Public roadmap showing what's shipped, in progress, and planned
- [Issue Tracker](https://github.com/shah786628/nawaz1-quantum-software/issues) — Report bugs and request features

---

## License

**Proprietary. Binary distribution only.**

Copyright (c) 2026 Shahnawaz Alam. All rights reserved.

Unauthorized copying, modification, distribution, or reverse engineering of this software is strictly prohibited. See LICENSE file for full terms.

---

## Support

- **Issues:** https://github.com/shah786628/nawaz1-quantum-software/issues
- **Author:** Shahnawaz Alam
