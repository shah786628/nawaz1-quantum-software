# Extension & Plugin System — Custom Quantum Algorithm Bridge

## Overview

The **Extension & Plugin System** lets you ship your own quantum algorithms into the running engine without forking the codebase. Plugins are first-class Rust types that implement a single trait, get vetted by an **8-layer security stack**, and then run on the same universal **L3 VQE execution substrate** that powers every built-in domain.

**Core principle:** plugins do *not* select a different quantum backend. The Algorithm Bridge **compiles** your custom algorithm onto the pre-built VQE circuit. Only the parameter vectors, metadata, and post-processing change — the underlying execution remains the universal VQE substrate at up to 65 536 qubits.

```
┌────────────────────────────────────────────────────────────────┐
│   Your custom algorithm (UCC variant, custom QAOA, hybrid …)   │
└─────────────────────────────┬──────────────────────────────────┘
                              │ implements AlgorithmPlugin
                              ▼
       ┌─────────────────────────────────────────────────┐
       │   AlgorithmBridgeExtended  (8 security layers)  │
       │   Layer 1  Cryptographic signing                │
       │   Layer 2  Input sanitization                   │
       │   Layer 3  Per-plugin rate limits               │
       │   Layer 4  Canary trap detection                │
       │   Layer 5  Behavioral anomaly detection         │
       │   Layer 6  Circuit complexity bounds            │
       │   Layer 7  Forensic audit log                   │
       │   Layer 8  Sandboxed execution + timeout        │
       └─────────────────────────────┬───────────────────┘
                                     │ parameter vector
                                     ▼
                ┌─────────────────────────────────┐
                │   L3 VQE Universal Substrate    │
                │   (65 536-qubit circuit)        │
                └─────────────────────────────────┘
```

**Source of truth:** [`nawaz1_dev/src/api/algorithm_bridge.rs`](../../../nawaz1_dev/src/api/algorithm_bridge.rs). All trait shapes, request/result types, and security primitives in this guide are taken directly from that file.

**Base URL:** `http://localhost:8080`

---

## Quick Start

A minimal, working `AlgorithmPlugin` looks like this:

```rust
use std::collections::HashMap;
use std::sync::Arc;
use serde_json::json;
use nawaz1_dev::api::algorithm_bridge::{
    AlgorithmBridgeExtended,
    AlgorithmPlugin,
    PluginAlgorithmRequest,
    PluginAlgorithmResult,
    PluginMetadata,
    PluginSecurityManifest,
    ComplexityClass,
    DataAccessScope,
};

pub struct HelloPlugin;

impl AlgorithmPlugin for HelloPlugin {
    fn name(&self) -> &str { "hello_plugin" }
    fn version(&self) -> &str { "0.1.0" }

    fn supported_domains(&self) -> Vec<String> {
        vec!["mathematics".to_string()]
    }

    fn execute(
        &self,
        request: &PluginAlgorithmRequest,
    ) -> Result<PluginAlgorithmResult, String> {
        let start = std::time::Instant::now();
        let sum: f64 = request.input_data.iter().sum();
        let mut out = HashMap::new();
        out.insert("sum".to_string(), json!(sum));
        out.insert("samples".to_string(), json!(request.input_data.len()));
        Ok(PluginAlgorithmResult {
            success: true,
            output_data: out,
            execution_time_ms: start.elapsed().as_secs_f64() * 1000.0,
            plugin_name: self.name().to_string(),
            plugin_version: self.version().to_string(),
        })
    }

    fn validate_input(
        &self,
        request: &PluginAlgorithmRequest,
    ) -> Result<(), String> {
        if request.input_data.is_empty() {
            return Err("input_data is empty".into());
        }
        if request.input_data.iter().any(|v| !v.is_finite()) {
            return Err("input_data contains NaN or Inf".into());
        }
        Ok(())
    }

    fn metadata(&self) -> PluginMetadata {
        PluginMetadata {
            name: self.name().to_string(),
            version: self.version().to_string(),
            author: "Your Name".to_string(),
            description: "Reference hello-world plugin.".to_string(),
            supported_domains: self.supported_domains(),
            max_qubits: 64,
        }
    }

    fn security_manifest(&self) -> PluginSecurityManifest {
        PluginSecurityManifest {
            requires_network: false,
            requires_filesystem: false,
            requires_gpu: false,
            max_memory_mib: 16,
            max_execution_time_ms: 1_000,
            max_qubits_requested: 64,
            declared_complexity_class: ComplexityClass::Linear,
            data_access_scope: DataAccessScope::ReadOwnInput,
        }
    }

    fn integrity_hash(&self) -> String {
        // Deterministic, code-version-tied hash. See "Computing the integrity hash".
        "hello_plugin@0.1.0:linear:read_own_input".to_string()
    }
}

fn main() -> Result<(), String> {
    let mut bridge = AlgorithmBridgeExtended::new();
    bridge.register_plugin(Arc::new(HelloPlugin))?;
    let req = PluginAlgorithmRequest {
        algorithm_name: "hello".to_string(),
        domain: "mathematics".to_string(),
        parameters: HashMap::new(),
        num_qubits: 8,
        input_data: vec![1.0, 2.0, 3.0, 4.0],
    };
    let result = bridge.execute_plugin("hello_plugin", &req)?;
    println!("{:#?}", result.output_data);
    Ok(())
}
```

That is the entire contract. Every method on `AlgorithmPlugin` is required.

---

## The `AlgorithmPlugin` Trait

The trait is defined in `algorithm_bridge.rs`:

```rust
pub trait AlgorithmPlugin: Send + Sync {
    fn name(&self) -> &str;
    fn version(&self) -> &str;
    fn supported_domains(&self) -> Vec<String>;
    fn execute(
        &self,
        request: &PluginAlgorithmRequest,
    ) -> Result<PluginAlgorithmResult, String>;
    fn validate_input(&self, request: &PluginAlgorithmRequest) -> Result<(), String>;
    fn metadata(&self) -> PluginMetadata;
    fn security_manifest(&self) -> PluginSecurityManifest;
    fn integrity_hash(&self) -> String;
}
```

| Method | Purpose | Called by |
|--------|---------|-----------|
| `name()` | Unique identifier across the registry. Must be stable across versions. | Bridge, registry, audit log |
| `version()` | Semver string (`"1.4.2"`). Changes require re-signing. | Registry, metadata API |
| `supported_domains()` | Quantum domains this plugin can handle (e.g. `["chemistry", "materials_science"]`). | Domain router |
| `execute()` | The single entry point. Receives a validated request, returns a result. | Bridge after all 8 security checks pass |
| `validate_input()` | Pre-flight check **before** `execute()`. Reject malformed/dangerous inputs cheaply. | Bridge inside Layer 2 |
| `metadata()` | Public, advertised information about the plugin. Surfaced via `/plugins/list`. | Discovery API |
| `security_manifest()` | Declarative resource & capability budget. Treated as a binding contract. | Layers 3, 6, 8 |
| `integrity_hash()` | Deterministic, code-version-tied hash. Mismatch with the registry's stored value triggers `PluginIntegrityMismatch`. | Layer 1 |

### Method contracts

- **`name()`** — must match `^[a-zA-Z][a-zA-Z0-9_]{2,63}$` (the bridge rejects anything else as `InvalidPluginName`).
- **`execute()`** — must be deterministic for the same `(input_data, parameters)` pair, must not panic on hostile inputs (panics are caught and logged as `PluginPanicked`), must respect `security_manifest().max_execution_time_ms`.
- **`validate_input()`** — should return `Err` for any input you would not want to run on the VQE substrate. The bridge calls this **before** the heavyweight Layer 6 circuit-complexity analyzer, so rejecting cheaply here is the primary cost-saver.
- **`integrity_hash()`** — must change whenever the implementation, parameters, or security manifest change. SHA-512 over `(name, version, source_hash, manifest_bytes)` is the recommended pattern; see "Computing the integrity hash" below.

---

## Types Reference

### `PluginAlgorithmRequest`

```rust
pub struct PluginAlgorithmRequest {
    pub algorithm_name: String,
    pub domain: String,
    pub parameters: HashMap<String, serde_json::Value>,
    pub num_qubits: usize,
    pub input_data: Vec<f64>,
}
```

| Field | Meaning |
|-------|---------|
| `algorithm_name` | Logical name selected by the caller (the plugin can ignore or branch on it). |
| `domain` | One of the 16 supported quantum domains. Must intersect `supported_domains()`. |
| `parameters` | Free-form JSON parameter map. Validated by Layer 2 (depth, entropy, injection). |
| `num_qubits` | Logical qubit width requested for this run. Bounded by the manifest's `max_qubits_requested`. |
| `input_data` | Raw amplitude vector. Treated as quantum amplitudes by the L3 substrate. |

### `PluginAlgorithmResult`

```rust
pub struct PluginAlgorithmResult {
    pub success: bool,
    pub output_data: HashMap<String, serde_json::Value>,
    pub execution_time_ms: f64,
    pub plugin_name: String,
    pub plugin_version: String,
}
```

| Field | Meaning |
|-------|---------|
| `success` | `true` only when the plugin completed normally. Error paths must return `Err(String)` from `execute()` rather than `Ok` with `success = false`. |
| `output_data` | Free-form JSON map. Layer 8 caps total size to detect output-size explosion attacks. |
| `execution_time_ms` | Wall-clock milliseconds inside `execute()`. The bridge cross-checks against `security_manifest().max_execution_time_ms` and against historical baselines. |
| `plugin_name` / `plugin_version` | Should match `name()` / `version()`. Mismatch is logged. |

### `PluginMetadata`

```rust
pub struct PluginMetadata {
    pub name: String,
    pub version: String,
    pub author: String,
    pub description: String,
    pub supported_domains: Vec<String>,
    pub max_qubits: usize,
}
```

Returned by `metadata()` and surfaced verbatim through `GET /api/v1/plugins/list` and `GET /api/v1/plugins/{name}/metadata`.

### `PluginSecurityManifest`

```rust
pub struct PluginSecurityManifest {
    pub requires_network: bool,
    pub requires_filesystem: bool,
    pub requires_gpu: bool,
    pub max_memory_mib: usize,
    pub max_execution_time_ms: u64,
    pub max_qubits_requested: usize,
    pub declared_complexity_class: ComplexityClass,
    pub data_access_scope: DataAccessScope,
}
```

| Field | Notes |
|-------|-------|
| `requires_network` / `requires_filesystem` / `requires_gpu` | Capabilities you are requesting. Untrusted plugins that declare `true` are auto-quarantined on first execution. |
| `max_memory_mib` | Soft cap. Layer 5 watches for `MemoryBombDetected`. |
| `max_execution_time_ms` | Hard cap. Layer 8 raises `ExecutionTimeout` once exceeded. |
| `max_qubits_requested` | Bounded by the bridge-wide `max_qubits_limit` (default 8192 strict, 65 536 permissive). |
| `declared_complexity_class` | Used by Layer 6 to pick the gate-count bound. |
| `data_access_scope` | The plugin's contract about what data it reads. Cross-checked at the request layer. |

### `ComplexityClass`

```rust
pub enum ComplexityClass {
    Linear,        // O(n)         — preferred for simple post-processing
    Quadratic,     // O(n²)        — typical for pairwise algorithms
    Polynomial,    // O(n^k)       — heuristic optimizers, ansatz searches
    Exponential,   // O(2^n)       — only with explicit Trusted approval
    Unknown,       // treated as Exponential by Layer 6
}
```

### `DataAccessScope`

```rust
pub enum DataAccessScope {
    None,           // pure compute over request only
    ReadOwnInput,   // recommended default
    ReadDomainData, // can read shared state for its declared domain
    ReadAll,        // requires Trusted level
}
```

---

## Creating a Custom Algorithm Plugin — Step by Step

### 1. Implement the trait

Start from the Quick Start template above. Keep `execute()` short and pure — push validation to `validate_input()`.

### 2. Define your security manifest

Declare **only what you need.** The bridge enforces every field:

```rust
fn security_manifest(&self) -> PluginSecurityManifest {
    PluginSecurityManifest {
        requires_network: false,           // never set true unless absolutely required
        requires_filesystem: false,
        requires_gpu: false,
        max_memory_mib: 256,               // honest upper bound
        max_execution_time_ms: 5_000,
        max_qubits_requested: 4096,
        declared_complexity_class: ComplexityClass::Polynomial,
        data_access_scope: DataAccessScope::ReadOwnInput,
    }
}
```

Over-declaring is treated as a security smell; under-declaring causes runtime kills.

### 3. Compute the integrity hash

`integrity_hash()` must be deterministic and tied to *both* the source and the manifest. The reference pattern uses SHA-512:

```rust
use sha2::{Digest, Sha512};

fn integrity_hash(&self) -> String {
    let mut h = Sha512::new();
    h.update(self.name().as_bytes());
    h.update(self.version().as_bytes());
    h.update(env!("CARGO_PKG_VERSION").as_bytes());
    h.update(include_bytes!("../src/lib.rs"));        // source binding
    let m = self.security_manifest();
    h.update(format!(
        "{}|{}|{}|{}|{}|{}|{:?}|{:?}",
        m.requires_network, m.requires_filesystem, m.requires_gpu,
        m.max_memory_mib, m.max_execution_time_ms, m.max_qubits_requested,
        m.declared_complexity_class, m.data_access_scope,
    ).as_bytes());
    format!("{:x}", h.finalize())
}
```

Layer 1 stores this hash at registration time and verifies it on **every** call. Any tampering — including changing the manifest after registration — produces `PluginIntegrityMismatch`.

### 4. Register with the bridge

```rust
let mut bridge = AlgorithmBridgeExtended::new();      // strict (default)
// or AlgorithmBridgeExtended::new_permissive() for development
let registered_name = bridge.register_plugin(Arc::new(MyPlugin))?;
```

`register_plugin` runs Layer 2 (signature, integrity, name validation) before inserting into the registry. Newly registered plugins start at `TrustLevel::Untrusted`.

### 5. Execute

```rust
let req = PluginAlgorithmRequest { /* … */ };
let res = bridge.execute_plugin(&registered_name, &req)?;
```

This single call walks every active layer. The success path returns the plugin's `PluginAlgorithmResult`; the failure path returns a `String` whose body matches the corresponding `SecurityViolation::Display` output.

---

## Complete Example — Custom Variational Eigensolver Plugin

A custom UCCSD-flavoured eigensolver that maps `parameters["theta"]` and `input_data` onto VQE circuit angles, runs an inner classical optimizer, and reports the converged ground-state energy.

```rust
use std::collections::HashMap;
use std::sync::Arc;
use serde_json::{json, Value};
use sha2::{Digest, Sha512};

use nawaz1_dev::api::algorithm_bridge::{
    AlgorithmBridgeExtended, AlgorithmPlugin,
    ComplexityClass, DataAccessScope,
    PluginAlgorithmRequest, PluginAlgorithmResult,
    PluginMetadata, PluginSecurityManifest,
};

pub struct CustomVqePlugin {
    pub max_iters: usize,
    pub learning_rate: f64,
}

impl CustomVqePlugin {
    pub fn new() -> Self { Self { max_iters: 200, learning_rate: 0.01 } }

    /// Map raw amplitudes to VQE rotation angles on the universal substrate.
    fn amplitudes_to_angles(input: &[f64]) -> Vec<f64> {
        input.iter().map(|a| 2.0 * a.abs().sqrt().atan2(1.0)).collect()
    }

    /// Toy energy expectation. Real plugins delegate to the VQE substrate
    /// via the same input_data the bridge already forwards.
    fn energy(angles: &[f64]) -> f64 {
        angles.iter().map(|t| 0.5 * (1.0 - t.cos())).sum::<f64>()
            - 0.05 * angles.len() as f64
    }
}

impl AlgorithmPlugin for CustomVqePlugin {
    fn name(&self) -> &str { "custom_vqe" }
    fn version(&self) -> &str { "1.0.0" }
    fn supported_domains(&self) -> Vec<String> {
        vec!["chemistry".to_string(), "materials_science".to_string()]
    }

    fn validate_input(&self, req: &PluginAlgorithmRequest) -> Result<(), String> {
        if req.input_data.is_empty() {
            return Err("input_data is empty".into());
        }
        if req.input_data.len() > 1 << 16 {
            return Err("input_data exceeds 65536 amplitudes".into());
        }
        let norm_sq: f64 = req.input_data.iter().map(|a| a * a).sum();
        if !(0.5..=1.5).contains(&norm_sq) {
            return Err(format!("amplitudes not normalised: |ψ|² = {:.4}", norm_sq));
        }
        if req.input_data.iter().any(|a| !a.is_finite()) {
            return Err("input_data contains NaN or Inf".into());
        }
        if req.num_qubits == 0 || req.num_qubits > 16 {
            return Err(format!("num_qubits {} outside [1,16]", req.num_qubits));
        }
        Ok(())
    }

    fn execute(&self, req: &PluginAlgorithmRequest) -> Result<PluginAlgorithmResult, String> {
        let start = std::time::Instant::now();
        let mut angles = Self::amplitudes_to_angles(&req.input_data);

        // Optional caller-provided initial theta override.
        if let Some(Value::Array(arr)) = req.parameters.get("theta") {
            for (i, v) in arr.iter().enumerate() {
                if i >= angles.len() { break; }
                if let Some(f) = v.as_f64() { angles[i] = f; }
            }
        }

        let mut history = Vec::with_capacity(self.max_iters);
        let mut best = Self::energy(&angles);
        history.push(best);
        for _ in 0..self.max_iters {
            for j in 0..angles.len() {
                let eps = 1e-3;
                let original = angles[j];
                angles[j] = original + eps;
                let plus = Self::energy(&angles);
                angles[j] = original - eps;
                let minus = Self::energy(&angles);
                angles[j] = original - self.learning_rate * (plus - minus) / (2.0 * eps);
            }
            let e = Self::energy(&angles);
            history.push(e);
            if (best - e).abs() < 1e-9 { break; }
            best = e;
        }

        let mut out = HashMap::new();
        out.insert("ground_state_energy".to_string(), json!(best));
        out.insert("iterations".to_string(), json!(history.len()));
        out.insert("energy_history".to_string(), json!(history));
        out.insert("converged_angles".to_string(), json!(angles));

        Ok(PluginAlgorithmResult {
            success: true,
            output_data: out,
            execution_time_ms: start.elapsed().as_secs_f64() * 1000.0,
            plugin_name: self.name().to_string(),
            plugin_version: self.version().to_string(),
        })
    }

    fn metadata(&self) -> PluginMetadata {
        PluginMetadata {
            name: self.name().to_string(),
            version: self.version().to_string(),
            author: "Quantum Plugin Authors".to_string(),
            description:
                "Custom VQE variant compiling onto the L3 universal substrate.".to_string(),
            supported_domains: self.supported_domains(),
            max_qubits: 16,
        }
    }

    fn security_manifest(&self) -> PluginSecurityManifest {
        PluginSecurityManifest {
            requires_network: false,
            requires_filesystem: false,
            requires_gpu: false,
            max_memory_mib: 128,
            max_execution_time_ms: 10_000,
            max_qubits_requested: 16,
            declared_complexity_class: ComplexityClass::Polynomial,
            data_access_scope: DataAccessScope::ReadOwnInput,
        }
    }

    fn integrity_hash(&self) -> String {
        let mut h = Sha512::new();
        h.update(self.name().as_bytes());
        h.update(self.version().as_bytes());
        h.update(self.max_iters.to_le_bytes());
        h.update(self.learning_rate.to_le_bytes());
        format!("{:x}", h.finalize())
    }
}

fn main() -> Result<(), String> {
    let mut bridge = AlgorithmBridgeExtended::new();
    bridge.register_plugin(Arc::new(CustomVqePlugin::new()))?;

    let mut amps = vec![0.0; 16];
    amps[0] = 1.0;                       // |0…0⟩ initial state
    let req = PluginAlgorithmRequest {
        algorithm_name: "custom_vqe".to_string(),
        domain: "chemistry".to_string(),
        parameters: HashMap::new(),
        num_qubits: 4,
        input_data: amps,
    };
    let res = bridge.execute_plugin("custom_vqe", &req)?;
    println!("E0 = {}", res.output_data["ground_state_energy"]);
    Ok(())
}
```

---

## Complete Example — Custom Optimization Algorithm Plugin (Finance + Logistics)

A QAOA-style portfolio/route optimizer that supports two domains. Demonstrates multi-domain registration, parameter validation, and a richer security manifest.

```rust
use std::collections::HashMap;
use std::sync::Arc;
use serde_json::{json, Value};
use sha2::{Digest, Sha512};

use nawaz1_dev::api::algorithm_bridge::{
    AlgorithmPlugin, ComplexityClass, DataAccessScope,
    PluginAlgorithmRequest, PluginAlgorithmResult,
    PluginMetadata, PluginSecurityManifest,
};

pub struct CustomQaoaOptimizer {
    pub layers: usize,
}

impl AlgorithmPlugin for CustomQaoaOptimizer {
    fn name(&self) -> &str { "qaoa_dual_domain" }
    fn version(&self) -> &str { "0.4.1" }

    fn supported_domains(&self) -> Vec<String> {
        vec!["finance".to_string(), "logistics".to_string()]
    }

    fn validate_input(&self, req: &PluginAlgorithmRequest) -> Result<(), String> {
        match req.parameters.get("cost_matrix") {
            Some(Value::Array(rows)) if !rows.is_empty() => {
                let n = rows.len();
                for r in rows {
                    let row = r.as_array().ok_or("cost_matrix row not array")?;
                    if row.len() != n {
                        return Err("cost_matrix not square".into());
                    }
                    if row.iter().any(|v| !v.as_f64().map_or(false, f64::is_finite)) {
                        return Err("cost_matrix has non-finite entries".into());
                    }
                }
            }
            _ => return Err("missing or invalid 'cost_matrix' parameter".into()),
        }
        if req.input_data.len() > 1 << 14 {
            return Err("input_data > 16384 amplitudes".into());
        }
        Ok(())
    }

    fn execute(&self, req: &PluginAlgorithmRequest) -> Result<PluginAlgorithmResult, String> {
        let start = std::time::Instant::now();
        let cost = req.parameters["cost_matrix"].as_array().unwrap();
        let n = cost.len();

        // Greedy + QAOA-style refinement skeleton (real plugin compiles
        // the cost Hamiltonian onto the L3 substrate via input_data).
        let mut assignment: Vec<usize> = (0..n).collect();
        let mut best_cost = f64::INFINITY;
        for _ in 0..self.layers {
            let mut total = 0.0;
            for i in 0..n {
                let row = cost[i].as_array().unwrap();
                total += row[assignment[i]].as_f64().unwrap_or(0.0);
            }
            if total < best_cost {
                best_cost = total;
            }
            assignment.rotate_left(1);
        }

        let mut out = HashMap::new();
        out.insert("best_cost".to_string(), json!(best_cost));
        out.insert("assignment".to_string(), json!(assignment));
        out.insert("layers".to_string(), json!(self.layers));
        out.insert("domain".to_string(), json!(req.domain));

        Ok(PluginAlgorithmResult {
            success: true,
            output_data: out,
            execution_time_ms: start.elapsed().as_secs_f64() * 1000.0,
            plugin_name: self.name().to_string(),
            plugin_version: self.version().to_string(),
        })
    }

    fn metadata(&self) -> PluginMetadata {
        PluginMetadata {
            name: self.name().to_string(),
            version: self.version().to_string(),
            author: "Optimisation Lab".to_string(),
            description:
                "QAOA-style optimiser for finance portfolios and logistics routes.".to_string(),
            supported_domains: self.supported_domains(),
            max_qubits: 4096,
        }
    }

    fn security_manifest(&self) -> PluginSecurityManifest {
        PluginSecurityManifest {
            requires_network: false,
            requires_filesystem: false,
            requires_gpu: false,
            max_memory_mib: 512,
            max_execution_time_ms: 20_000,
            max_qubits_requested: 4096,
            declared_complexity_class: ComplexityClass::Quadratic,
            data_access_scope: DataAccessScope::ReadDomainData,
        }
    }

    fn integrity_hash(&self) -> String {
        let mut h = Sha512::new();
        h.update(self.name().as_bytes());
        h.update(self.version().as_bytes());
        h.update(self.layers.to_le_bytes());
        format!("{:x}", h.finalize())
    }
}

let plugin = Arc::new(CustomQaoaOptimizer { layers: 8 });
```

---

## API Endpoints Reference

All endpoints are mounted under `http://localhost:8080`.

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/v1/plugins/register` | Admin | Register a new plugin |
| `GET` | `/api/v1/plugins/list` | Public | List all plugins with trust levels |
| `DELETE` | `/api/v1/plugins/{name}` | Admin | Unregister a plugin |
| `POST` | `/api/v1/plugins/{name}/execute` | Public (rate-limited) | Execute a plugin |
| `GET` | `/api/v1/plugins/{name}/metadata` | Public | Get plugin metadata |
| `GET` | `/api/v1/plugins/security/audit` | Admin | View forensic audit log |
| `GET` | `/api/v1/plugins/security/stats` | Admin | Security statistics |
| `POST` | `/api/v1/plugins/security/threat-level` | Admin | Override threat level |
| `POST` | `/api/v1/plugins/{name}/quarantine` | Admin | Quarantine a plugin |
| `POST` | `/api/v1/plugins/{name}/trust` | Admin | Set trust level |

### `POST /api/v1/plugins/register`

Registers a plugin already loaded inside the server process (for example, via a signed extension).

**Request**
```json
{
  "name": "custom_vqe",
  "version": "1.0.0",
  "signature_hex": "9f37c0…ab12",
  "integrity_hash": "ec1d8b9b…3f0a"
}
```

**Response — 201 Created**
```json
{
  "registered": true,
  "name": "custom_vqe",
  "trust_level": "Untrusted"
}
```

**curl**
```powershell
curl -X POST http://localhost:8080/api/v1/plugins/register `
  -H "Authorization: Bearer $ADMIN_TOKEN" `
  -H "Content-Type: application/json" `
  -d '{ "name":"custom_vqe","version":"1.0.0","signature_hex":"9f37c0ab12","integrity_hash":"ec1d8b9b3f0a" }'
```

Status codes: `201` registered · `400` invalid manifest · `401` unauthenticated · `403` not admin · `409` already registered.

### `GET /api/v1/plugins/list`

**Response — 200**
```json
{
  "plugins": [
    {
      "name": "custom_vqe",
      "version": "1.0.0",
      "author": "Quantum Plugin Authors",
      "description": "Custom VQE variant compiling onto the L3 universal substrate.",
      "supported_domains": ["chemistry", "materials_science"],
      "max_qubits": 16,
      "trust_level": "Verified"
    }
  ],
  "total": 1
}
```

**curl**
```powershell
curl http://localhost:8080/api/v1/plugins/list
```

### `DELETE /api/v1/plugins/{name}`

**Response — 200**
```json
{ "unregistered": true, "name": "custom_vqe" }
```

Status codes: `200` removed · `404` unknown plugin · `403` not admin.

```powershell
curl -X DELETE http://localhost:8080/api/v1/plugins/custom_vqe `
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### `POST /api/v1/plugins/{name}/execute`

**Request**
```json
{
  "algorithm_name": "custom_vqe",
  "domain": "chemistry",
  "parameters": { "theta": [0.1, 0.2, 0.3] },
  "num_qubits": 4,
  "input_data": [1.0, 0.0, 0.0, 0.0]
}
```

**Response — 200**
```json
{
  "success": true,
  "output_data": {
    "ground_state_energy": -1.137,
    "iterations": 42,
    "energy_history": [-0.5, -0.9, -1.1, -1.137]
  },
  "execution_time_ms": 124.7,
  "plugin_name": "custom_vqe",
  "plugin_version": "1.0.0"
}
```

**Response — 429 Rate Limited**
```json
{
  "error": "PluginBlocked",
  "violation": "rate limit exceeded for 'custom_vqe': 11 requests in window"
}
```

**curl**
```powershell
curl -X POST http://localhost:8080/api/v1/plugins/custom_vqe/execute `
  -H "Content-Type: application/json" `
  -d '{ "algorithm_name":"custom_vqe","domain":"chemistry","parameters":{},"num_qubits":4,"input_data":[1.0,0.0,0.0,0.0] }'
```

Status codes: `200` ok · `400` validation failed · `403` plugin quarantined · `408` timeout · `429` rate limited · `503` global threat-level lockdown.

### `GET /api/v1/plugins/{name}/metadata`

**Response — 200**
```json
{
  "name": "custom_vqe",
  "version": "1.0.0",
  "author": "Quantum Plugin Authors",
  "description": "Custom VQE variant compiling onto the L3 universal substrate.",
  "supported_domains": ["chemistry", "materials_science"],
  "max_qubits": 16,
  "trust_level": "Verified",
  "integrity_hash": "ec1d8b9b…3f0a",
  "security_manifest": {
    "requires_network": false,
    "requires_filesystem": false,
    "requires_gpu": false,
    "max_memory_mib": 128,
    "max_execution_time_ms": 10000,
    "max_qubits_requested": 16,
    "declared_complexity_class": "Polynomial",
    "data_access_scope": "ReadOwnInput"
  }
}
```

### `GET /api/v1/plugins/security/audit`

**Response — 200**
```json
{
  "entries": [
    {
      "id": 482,
      "timestamp_ns": 1716120004123456000,
      "event_type": "PluginExecuted",
      "plugin_name": "custom_vqe",
      "action": "execute",
      "violation": null,
      "threat_level_at_time": "Normal",
      "execution_time_ms": 124,
      "success": true
    },
    {
      "id": 483,
      "event_type": "PluginBlocked",
      "plugin_name": "shady_plugin",
      "violation": "rate limit exceeded for 'shady_plugin': 23 requests in window",
      "threat_level_at_time": "Elevated",
      "success": false
    }
  ],
  "total": 2,
  "violations": 1
}
```

```powershell
curl http://localhost:8080/api/v1/plugins/security/audit `
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### `GET /api/v1/plugins/security/stats`

**Response — 200**
```json
{
  "total_violations": 14,
  "threat_level": "Elevated",
  "quarantined_count": 1,
  "total_plugins": 7,
  "canary_triggers": 0
}
```

### `POST /api/v1/plugins/security/threat-level`

**Request**
```json
{ "level": "High" }
```
Allowed values: `Normal`, `Elevated`, `High`, `Critical`, `Lockdown`.

**Response — 200**
```json
{ "previous": "Elevated", "current": "High" }
```

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/security/threat-level `
  -H "Authorization: Bearer $ADMIN_TOKEN" `
  -H "Content-Type: application/json" `
  -d '{ "level":"High" }'
```

### `POST /api/v1/plugins/{name}/quarantine`

**Response — 200**
```json
{ "quarantined": true, "name": "shady_plugin" }
```

Quarantined plugins remain registered but every `execute_plugin` call returns immediately with `PluginBlocked`. Use the same endpoint with `{"release": true}` to lift quarantine.

### `POST /api/v1/plugins/{name}/trust`

**Request**
```json
{ "level": "Verified" }
```

Allowed values: `Untrusted`, `Verified`, `Trusted`. Promotion to `BuiltIn` is rejected at runtime — built-in is reserved for compile-time plugins.

**Response — 200**
```json
{ "previous": "Untrusted", "current": "Verified", "name": "custom_vqe" }
```

---

## Security Model

### Trust Levels

`TrustLevel` (defined in `algorithm_bridge.rs`) controls every quota a plugin sees.

| Level | How obtained | Rate limit | Hard timeout | Max input amplitudes | Notes |
|-------|--------------|------------|--------------|----------------------|-------|
| `Untrusted` | Default after registration | 10 / min | 5 s | 100 000 | Full sandbox; capability requests cause auto-quarantine |
| `Verified` | Valid signature accepted by `CryptoVerifier` | 50 / min | 15 s | 500 000 | Capability requests allowed but watched |
| `Trusted` | Admin promotion via `/trust` endpoint | 200 / min | 30 s | 1 000 000 | May declare `ReadAll`, `Exponential` |
| `BuiltIn` | Compiled-in plugins only | unbounded | 600 s | 65 536 amps | Bypasses runtime signature check, never quarantined |

The exact rate-limit numerator is taken from `PluginSecurityGuard::check_rate_limit` in `algorithm_bridge.rs`; see the source for the binding values used by the running engine.

### 8-Layer Protection

| # | Layer | Class | Protects against |
|---|-------|-------|------------------|
| 1 | Cryptographic signing + HMAC integrity | `CryptoVerifier` | Forged plugins, swapped binaries, replay of revoked builds |
| 2 | Input sanitization (14 distinct checks) | `PluginSecurityGuard` | Null-byte, path traversal, shell/SQL/code/script injection, serialization attacks, unicode homoglyphs, high-entropy payloads, parameter-depth bombs |
| 3 | Per-plugin sliding-window rate limiting | `RateLimitState` | Brute-force, denial-of-wallet, oracle scraping |
| 4 | Canary trap detection | `CanaryRegistry` | Plugin enumeration, registry probes |
| 5 | Behavioral anomaly detection & quarantine | `ThreatDetector` | Drift from historical baselines, memory bombs, output-size explosion |
| 6 | Quantum circuit complexity bounds | `CircuitComplexityAnalyzer` | Gate-count explosion, circuit-depth bombs, entanglement-density attacks |
| 7 | Forensic audit trail | `ForensicAuditLogger` | Repudiation, missing evidence — every event is logged, violation entries are never evicted |
| 8 | Sandboxed execution + hard timeout | `AlgorithmBridgeExtended::execute_plugin` | Panics, infinite loops, runaway compute |

Layers run in this order, and the first failure short-circuits the call with a `SecurityViolation` value.

### Security Manifest Requirements

Every field in `PluginSecurityManifest` is enforced:

- `requires_network` / `requires_filesystem` / `requires_gpu` — declaring `true` while at `Untrusted` triggers automatic quarantine on first execute.
- `max_memory_mib` — Layer 5 monitors RSS delta; exceeding by ≥1.5× yields `MemoryBombDetected`.
- `max_execution_time_ms` — both your declared cap **and** the trust-level hard cap apply; the smaller wins.
- `max_qubits_requested` — bounded by the bridge-wide `max_qubits_limit` and by `request.num_qubits`.
- `declared_complexity_class` — Layer 6 picks gate-count bounds: `Linear` ≤ 10⁵, `Quadratic` ≤ 10⁷, `Polynomial` ≤ 10⁹, `Exponential` requires `Trusted`.
- `data_access_scope` — declaring `ReadAll` or `ReadDomainData` while `Untrusted` is rejected.

If the running plugin exceeds any declared limit, Layer 5 raises a behavioral anomaly and Layer 7 records it; repeated breaches escalate the global `ThreatLevel`.

---

## Error Handling

Every failure path surfaces a `SecurityViolation` (see `algorithm_bridge.rs`). The HTTP layer maps these to JSON `error.violation` strings whose body matches `Display`.

Common variants you will encounter:

| Variant | Trigger | What to do |
|---------|---------|-----------|
| `RateLimitExceeded { plugin, count }` | Sliding-window cap hit | Back off (`Retry-After` header) and reduce burst |
| `ExecutionTimeout { plugin, elapsed_ms }` | Plugin slower than declared | Lower `max_execution_time_ms` honestly, optimise inner loop |
| `PluginPanicked { plugin, message }` | `execute()` panicked | Fix the panic — guards turn this into a hard ban after 3 occurrences |
| `PluginIntegrityMismatch { expected, actual }` | Manifest/source changed without re-registering | Re-compute `integrity_hash()` and re-register |
| `InvalidPluginSignature(s)` | Signature missing or unknown trusted key | Sign with an admin-issued key |
| `RevokedPluginSignature(s)` | Signature on the revocation list | Build & sign a new release |
| `PayloadTooLarge { size, max }` | `input_data` exceeds Layer 2 cap | Stream in chunks or downsample |
| `PluginQuarantined` | Anomaly detector tripped | Inspect audit log, fix root cause, ask admin to release |
| `DomainNotAllowed(d)` | `request.domain` ∉ `supported_domains()` | Update plugin or correct the request |
| `QubitLimitExceeded { requested, max }` | Manifest or request larger than bridge limit | Lower `num_qubits` |
| `GateCountExplosion { count, max }` | Inner expansion exceeds Layer 6 bound | Reduce circuit depth or upgrade complexity class |
| `CanaryTriggered { trap_type, trap_name }` | Plugin probed a honeypot identifier | Stop scanning the registry |

### Debugging "Plugin Blocked" errors

1. Pull the most recent violation entries: `GET /api/v1/plugins/security/audit`.
2. Match the `violation` string to the table above.
3. Confirm your manifest matches what the registry stored: `GET /api/v1/plugins/{name}/metadata`.
4. Re-register if the integrity hash drifted.

### Rate-limit handling

Treat `429 RateLimitExceeded` as advisory. The recommended client behaviour is exponential backoff with jitter, capped at `max_execution_time_ms` of your manifest.

### Threat-level escalation

`ThreatDetector` escalates the global `ThreatLevel` automatically when violations accumulate. At `Lockdown`, **all non-`BuiltIn` execute calls** return `503`. Operators can de-escalate explicitly via `POST /api/v1/plugins/security/threat-level` with `{"level":"Normal"}` after triage.

---

## Best Practices

- **One domain, one plugin.** Splitting concerns keeps the manifest small and the integrity hash stable.
- **Declare the smallest manifest that works.** The bridge prefers a tight, honest manifest over a permissive one.
- **Always validate in `validate_input()`.** Layer 2 already rejects gross attacks — your job is semantic validation (matrix shape, normalisation, parameter ranges).
- **Make `integrity_hash()` deterministic.** Hash over name, version, source bytes, and the manifest. Avoid clocks, environment variables, and randomness.
- **Handle edge cases.** Empty inputs, NaN, ±Inf, zero qubits, mismatched parameter arrays — all of these will be thrown at you by the canary registry.
- **Test at `Untrusted` first.** If your plugin works under the strictest quotas, promotion to `Verified` is mechanical.
- **Avoid hidden state.** Plugins are `Send + Sync` and may be invoked concurrently; mutate only through `Mutex`/`RwLock`.
- **Surface execution time honestly.** `execution_time_ms` should reflect real wall-clock work; dishonest values trigger Layer 5 timing anomalies.
- **Keep `output_data` small.** Multi-megabyte payloads trigger `OutputSizeExplosion`. Stream large results via dedicated APIs instead.
- **Re-register on every release.** Version bumps without re-registration fail Layer 1.

---

## FAQ

**Q: Can I access the VQE engine directly from my plugin?**
No — and you don't need to. The bridge already forwards `input_data` and `num_qubits` to the L3 universal substrate. Your job is to compile algorithm parameters; execution stays on the substrate.

**Q: What happens during hot-reload?**
The bridge holds plugins by `Arc<dyn AlgorithmPlugin>`. Replacing a plugin requires `unregister_plugin` followed by `register_plugin` — there is no in-place swap. In-flight executions complete against the previous `Arc`.

**Q: How do I get promoted from Untrusted to Verified?**
Sign your release with a key trusted by `CryptoVerifier::add_trusted_key`, then call `POST /api/v1/plugins/{name}/trust` with `{"level":"Verified"}` from an admin token. Trusted keys are managed out of band.

**Q: Can plugins call other plugins?**
Cross-plugin invocation is detected by the reentrancy guard and reported as `ReentrancyAttempt`. If you genuinely need composition, register a single plugin that links the dependent code statically.

**Q: What's the maximum execution time?**
The lower of (manifest `max_execution_time_ms`, trust-level hard cap). At `BuiltIn`, the global `execution_timeout_ms` (default 10 s strict, 600 s permissive) becomes the only ceiling.

**Q: My plugin is being quarantined despite passing every validation. Why?**
Inspect `/security/audit` for `AnomalyDetected`. Layer 5 compares each run against a `BehaviorBaseline` for that plugin; a sudden ×3-σ jump in execution time, output size, or memory delta will quarantine it even when individual fields look fine.

**Q: Can I update the manifest without bumping the version?**
No. The manifest is part of `integrity_hash()`. Any change must produce a new hash, which means a new `version()` and a fresh signature.

**Q: How is `BuiltIn` different from `Trusted`?**
`BuiltIn` is reserved for plugins compiled into the engine binary. They skip `CryptoVerifier::verify_plugin_hash` because their integrity is already guaranteed by the build pipeline. The runtime cannot promote a registered plugin to `BuiltIn`.

---

## Supported Quantum Domains

Plugins may declare any subset of the 16 domains served by the engine:

| # | Domain | `supported_domains` value |
|---|--------|---------------------------|
| 1 | Chemistry | `"chemistry"` |
| 2 | Physics | `"physics"` |
| 3 | Materials Science | `"materials_science"` |
| 4 | Biomolecules | `"biology"` |
| 5 | Machine Learning | `"machine_learning"` |
| 6 | Finance | `"finance"` |
| 7 | Logistics | `"logistics"` |
| 8 | Nuclear | `"nuclear"` |
| 9 | Mathematics | `"mathematics"` |
| 10 | Error Mitigation | `"error_mitigation"` |
| 11 | Graphics | `"graphics"` |
| 12 | Real-Time | `"real_time"` |
| 13 | Fluid Mechanics | `"fluid_mechanics"` |
| 14 | Turbulence CFD | `"turbulence_cfd"` |
| 15 | Multiphase Flow | `"multiphase_flow"` |
| 16 | Heat Transfer | `"heat_transfer"` |

Declaring a domain outside this set produces `DomainNotAllowed` at registration. Cross-domain plugins are encouraged — `cross_domain` is a reserved bucket that combines several of the above.

---

**Source files referenced:** [`nawaz1_dev/src/api/algorithm_bridge.rs`](../../../nawaz1_dev/src/api/algorithm_bridge.rs) — the canonical definitions for every type, trait, and security primitive in this guide.
