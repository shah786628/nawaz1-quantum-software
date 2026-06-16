# SDK Package — Multi-Language Client Libraries

## Overview

The Nawaz1 Quantum VQE Engine ships with native client libraries for **four** programming languages, all targeting the unified HTTP execution endpoint:

```
POST http://localhost:8080/api/v1/quantum/execute
```

Every SDK exposes the same request/response model — the only difference is the host language idiom. All examples below execute a chemistry VQE problem with **amplitude values (up to 2^53)** (full hemoglobin-scale simulation).

| Language | Status | Strengths | Use When |
|---|-----------|------------|
| **Python** | Primary | Full API coverage, NumPy integration | Notebooks, data science, prototyping |
| **C++** | Native | Zero-overhead, header-only | High-performance native integration |
| **Rust** | Native | Memory-safe, zero-copy data transfer | Systems programming, embedded clients |
| **Julia** | Native | First-class arrays, scientific computing | Numerical research, simulation pipelines |

---

## 1. Python — Primary SDK

**Installation**

```bash
pip install numpy requests
# (or pin from the SDK directory)
pip install -e ./packages/sdk/python
```

**Connect & Execute**

```python
import numpy as np
import requests

ENDPOINT = "http://localhost:8080/api/v1/quantum/execute"
API_KEY  = ""   # set if NAWAZ1_API_KEY enabled on the server

def headers():
    h = {"Content-Type": "application/json"}
    if API_KEY:
        h["X-API-Key"] = API_KEY
    return h

# Build amplitude values (engine supports up to 2^53) for a hemoglobin VQE run
rng = np.random.default_rng(42)
amps = rng.normal(0.0, 1.0, 1024)  # Example uses 1024; engine supports up to 2^53
amps = (amps / np.linalg.norm(amps)).tolist()

resp = requests.post(ENDPOINT, headers=headers(), json={
    "domain": "chemistry",
    "algorithm": "vqe",
    "molecule": "hemoglobin",
    "atoms": 8738,
    "input_data": amps,                # amplitude encoding determines qubit count (up to 2^53)
    "config": {
        "sub_module": "vqe_chemistry",
        "task": "ground_state_energy",
        "ansatz": "uccsd"
    }
}, timeout=300)

result = resp.json()
print("energy   :", result["result"]["energy"])
print("converged:", result["result"]["converged"])
print("qubits   :", result["result"]["num_qubits"])
```

**Response Handling**

```python
if not resp.ok:
    raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")

r = result["result"]
energy   = r["energy"]
fidelity = r["fidelity"]
qubits   = r["num_qubits"]
exec_ms  = result["metadata"]["execution_time_ms"]
```

---

## 2. C++ — High-Performance Native Integration

A header-only client (single `nawaz1_client.hpp`) wrapping `libcurl` and a JSON dependency of your choice (e.g., `nlohmann/json`).

**Installation**

```bash
# Header-only — drop into your include path
cp packages/sdk/cpp/nawaz1_client.hpp /usr/local/include/

# Link against libcurl
g++ -std=c++17 main.cpp -lcurl -o my_app
```

**Connect & Execute**

```cpp
#include "nawaz1_client.hpp"
#include <vector>
#include <random>
#include <iostream>

int main() {
    nawaz1::Client client("http://localhost:8080/api/v1");
    // client.set_api_key("...");  // optional

    // Generate amplitudes (engine supports up to 2^53)
    std::vector<double> amps(1024)  // Example; engine supports up to 2^53;
    std::mt19937_64 rng(42);
    std::normal_distribution<double> nd(0.0, 1.0);
    double sumsq = 0.0;
    for (auto& x : amps) { x = nd(rng); sumsq += x * x; }
    double norm = std::sqrt(sumsq);
    for (auto& x : amps) x /= norm;

    nawaz1::ExecuteRequest req;
    req.domain    = "chemistry";
    req.algorithm = "vqe";
    req.input_data = std::move(amps);
    req.config["sub_module"]  = "vqe_chemistry";
    req.config["task"]        = "ground_state_energy";
    req.config["molecule"]    = "hemoglobin";

    auto resp = client.execute(req);   // POST /quantum/execute
    if (!resp.success) {
        std::cerr << "error: " << resp.error_message << "\n";
        return 1;
    }
    std::cout << "energy = " << resp.result["energy"].get<double>() << "\n";
    std::cout << "qubits = " << resp.result["num_qubits"].get<int>() << "\n";
}
```

**Response Handling**

```cpp
if (!resp.success) { /* HTTP failure or non-2xx */ }
double energy   = resp.result.value("energy",   0.0);
double fidelity = resp.result.value("fidelity", 0.0);
bool   conv     = resp.result.value("converged", false);
```

---

## 3. Rust — Native Crate, Zero-Copy

**Installation**

Add to your `Cargo.toml`:

```toml
[dependencies]
nawaz1-client = { path = "../packages/sdk/rust" }
tokio  = { version = "1", features = ["full"] }
serde_json = "1"
```

**Connect & Execute**

```rust
use nawaz1_client::{Client, ExecuteRequest};
use serde_json::json;

// Requires tokio async runtime (#[tokio::main] entry point)
let client = Client::new("http://localhost:8080/api/v1");

// Amplitudes (zero-copy — passed by reference into the request body)
let mut amps: Vec<f64> = (0..1024)  // Example; engine supports up to 2^53
    .map(|i| (i as f64 * 0.001).sin())
    .collect();
let norm: f64 = amps.iter().map(|x| x * x).sum::<f64>().sqrt();
amps.iter_mut().for_each(|x| *x /= norm);

let req = ExecuteRequest {
    domain:    "chemistry".into(),
    algorithm: "vqe".into(),
    input_data: amps,
    config: json!({
        "sub_module": "vqe_chemistry",
        "task":       "ground_state_energy",
        "molecule":   "hemoglobin",
        "ansatz":     "uccsd"
    }),
};

let resp = client.execute(&req).await?;
println!("energy   = {}", resp.result["energy"]);
println!("qubits   = {}", resp.result["num_qubits"]);
```

**Response Handling**

```rust
match client.execute(&req).await {
    Ok(r) if r.success => {
        let energy   = r.result["energy"].as_f64().unwrap_or(0.0);
        let fidelity = r.result["fidelity"].as_f64().unwrap_or(0.0);
    }
    Ok(r)  => eprintln!("server error: {:?}", r.error),
    Err(e) => eprintln!("transport error: {e}"),
}
```

---

## 4. Julia — Scientific Computing

**Installation**

```julia
using Pkg
Pkg.add("HTTP")
Pkg.add("JSON3")
Pkg.develop(path="packages/sdk/julia/Nawaz1.jl")
```

**Connect & Execute**

```julia
using Nawaz1
using LinearAlgebra
using Random

client = Nawaz1.Client("http://localhost:8080/api/v1")
# Nawaz1.set_api_key!(client, "...")  # optional

# Amplitudes — native Julia Vector{Float64}, no copy (engine supports up to 2^53)
Random.seed!(42)
amps = randn(1024)  # Example; engine supports up to 2^53
amps ./= norm(amps)

resp = Nawaz1.execute(client; 
    domain    = "chemistry",
    algorithm = "vqe",
    input_data = amps,
    config = Dict(
        "sub_module" => "vqe_chemistry",
        "task"       => "ground_state_energy",
        "molecule"   => "hemoglobin",
        "ansatz"     => "uccsd"
    )
)

println("energy    = ", resp.result["energy"])
println("converged = ", resp.result["converged"])
println("qubits    = ", resp.result["num_qubits"])
```

**Response Handling**

```julia
if !resp.success
    error("Quantum engine error: $(resp.error)")
end

energy   = resp.result["energy"]
fidelity = resp.result["fidelity"]
exec_ms  = resp.metadata["execution_time_ms"]
```

---

## Common Request Schema

Every SDK serializes the same JSON body posted to `/api/v1/quantum/execute`:

```json
{
  "domain":    "chemistry",
  "algorithm": "vqe",
  "input_data": [/* N floats — determines qubit count (up to 2^53) */],
  "config": {
    "sub_module": "vqe_chemistry",
    "task":       "ground_state_energy",
    "molecule":   "hemoglobin"
  }
}
```

## Common Response Schema

```json
{
  "success": true,
  "domain":  "chemistry",
  "algorithm": "vqe",
  "result": {
    "energy":      -4532.7183,
    "converged":   true,
    "iterations":  120,
    "fidelity":    0.9998,
    "num_qubits":  1024,
    "gate_count":  524288
  },
  "metadata": {
    "execution_time_ms": 45.2,
    "tier":              "free",
    "input_amplitudes":  1024
  }
}
```

---

## Engine Behavior

> **These behaviors apply to every SDK language and every domain:**

- **Algorithm:** User-specified per request (required field). You must include `"algorithm"` in the payload — the engine does **not** auto-select. Pick the algorithm appropriate to your problem: `"vqe"` for chemistry / biology / materials energy minimization, `"qaoa"` for finance/logistics/optimization, `"qpe"` for physics ground states, `"dmrg"` for physics dynamics, `"hhl"` for linear systems, `"qft"` for fluid mechanics / graphics / heat transfer / Fourier methods, `"qnn"` for machine learning, `"monte_carlo"` for risk / sampling, `"trotter"` for real-time evolution, `"zne"` for error mitigation.
- **Quantum Dispatcher:** Compiles the selected algorithm onto the pre-built VQE execution substrate. The VQE circuit is a *universal execution substrate* — every algorithm above is compiled into parameter vectors that the substrate runs natively.
- **Depth:** Automatically optimized — do **NOT** specify `"depth"` or `"circuit_depth"`. The engine selects the optimal depth from input entropy and domain characteristics; any value you supply will be ignored.
- **Qubits:** Calculated from `input_data.len().next_power_of_two()`. The number of amplitudes determines qubit count (up to 2^53 qubits maximum).
- **Routing:** The router only routes the request to the correct **domain handler**. It does **not** select the algorithm — that choice remains yours.

| Setting | Behavior | Notes |
|---------|----------|-------|
| **Algorithm** | User-specified | Required field; bridge compiles your choice onto VQE substrate |
| **Depth** | Auto-optimized | Engine picks; do NOT include `"depth"` |
| **Qubits** | `input_data.len().next_power_of_two()` | Derived from input length |
| **Routing** | Domain router | Routes to domain handler only — never overrides your algorithm |

---

## Tips

- **Qubit count is data-driven.** The number of qubits equals `next_power_of_two(len(input_data))`. For N qubits, send exactly N normalized amplitudes (engine supports up to 2^53).
- **Normalize before sending.** All SDKs accept raw amplitudes, but the engine assumes Born-normalized vectors. Pre-normalize for predictable energies.
- **Reuse the client.** All four SDKs maintain connection pools — instantiate the client once, reuse for many `execute` calls.
- **Set `NAWAZ1_API_KEY` server-side** to require `X-API-Key` on every request; each SDK exposes a `set_api_key`-style helper.

---

## Input Method

### API Endpoint
```
POST http://localhost:8080/api/v1/quantum/execute
```

### Request Format (All Language Bindings)

Every SDK serializes the same JSON structure:

```json
{
  "domain": "<target_domain>",
  "algorithm": "<algorithm>",
  "input_data": [0.001, -0.003, 0.002, "...Born-normalized floats..."],
  "config": {
    "sub_module": "<module_name>",
    "task": "<task_name>"
  }
}
```

### Language-Specific Input Methods
| Language | Input Method | Notes |
|---|---|---|
| **Python** | `requests.post(url, json={...})` | NumPy array → `.tolist()` |
| **C++** | `nawaz1::Client::execute(req)` | `std::vector<double>` zero-copy |
| **Rust** | `client.execute(&req).await` | `Vec<f64>` by reference |
| **Julia** | `Nawaz1.execute(client; ...)` | Native `Vector{Float64}` |

### Data Input Options
- **Direct API**: Send JSON payload with amplitudes (Born-normalized floats)
- **File Import**: Upload binary/CSV data files via the import endpoint
- **Streaming**: For large datasets, use chunked streaming mode

---

## Hamiltonian Selection

The SDK provides access to all domain-specific Hamiltonians through the unified API. Select the appropriate Hamiltonian by specifying the `domain` and `config` parameters:

### Available Domains and Hamiltonians
| Domain | Hamiltonian Types | Reference |
|---|---|---|
| Chemistry | Molecular, UCCSD, Custom Matrix | See chemistry package |
| Physics | Heisenberg, Hubbard, Ising, Custom | See physics package |
| Materials Science | Tight-binding, DFT-derived, Phonon | See materials_science package |
| Finance | Ising (Portfolio), QUBO | See finance package |
| Logistics | QUBO, TSP, MaxCut | See logistics package |
| Machine Learning | Quantum Kernel, Variational Classifier | See machine_learning package |

### Configuration
```json
{
  "hamiltonian": {
    "type": "<domain_specific_type>",
    "parameters": { "...domain_specific_params..." }
  }
}
```

### Encoding Options
- **Jordan-Wigner**: Fermion-to-qubit mapping (default for chemistry/physics)
- **Bravyi-Kitaev**: Reduced gate depth for large systems
- **Direct Encoding**: For combinatorial optimization problems

---

## Supported Scale

| Parameter | Maximum Value |
|---|---|
| **Qubits** | 2^53 (9,007,199,254,740,992) |
| **Bond Dimension** | 2^53 |
| **Precision** | IEEE 754 double (64-bit float) |

The quantum engine supports computations from small-scale (8 qubits) up to the theoretical maximum of 2^53 qubits with matching bond dimension, enabling simulation of molecular systems from simple hydrogen molecules to complex biological macromolecules and beyond.

