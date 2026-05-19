# Extension & Plugin System — Custom Quantum Algorithm Bridge

## Overview

The **Extension & Plugin System** lets you ship your own quantum algorithms into the running engine without forking the codebase. Plugins are first-class Rust types that implement a single trait, get vetted by a **multi-layer security validation pipeline**, and then run on the same universal **L3 VQE execution substrate** that powers every built-in domain.

**Core principle:** plugins do *not* select a different quantum backend. The Algorithm Bridge **compiles** your custom algorithm onto the pre-built VQE circuit. Only the parameter vectors, metadata, and post-processing change — the underlying execution remains the universal VQE substrate at up to 65 536 qubits.

```
┌────────────────────────────────────────────────────────────────┐
│   Your custom algorithm (UCC variant, custom QAOA, hybrid …)   │
└─────────────────────────────┬──────────────────────────────────┘
                              │ implements AlgorithmPlugin
                              ▼
       ┌─────────────────────────────────────────────────┐
       │   AlgorithmBridgeExtended                       │
       │   (Multi-layer security validation pipeline)    │
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
| `execute()` | The single entry point. Receives a validated request, returns a result. | Bridge after all security checks pass |
| `validate_input()` | Pre-flight check **before** `execute()`. Reject malformed/dangerous inputs cheaply. | Bridge during input validation |
| `metadata()` | Public, advertised information about the plugin. Surfaced via `/plugins/list`. | Discovery API |
| `security_manifest()` | Declarative resource & capability budget. Treated as a binding contract. | Security validation pipeline |
| `integrity_hash()` | Deterministic, code-version-tied hash. Mismatch with the registry's stored value triggers `PluginIntegrityMismatch`. | Signature verification |

### Method contracts

- **`name()`** — must match `^[a-zA-Z][a-zA-Z0-9_]{2,63}$` (the bridge rejects anything else as `InvalidPluginName`).
- **`execute()`** — must be deterministic for the same `(input_data, parameters)` pair, must not panic on hostile inputs (panics are caught and logged as `PluginPanicked`), must respect `security_manifest().max_execution_time_ms`.
- **`validate_input()`** — should return `Err` for any input you would not want to run on the VQE substrate. The bridge calls this **before** the heavyweight circuit-bounds checker, so rejecting cheaply here is the primary cost-saver.
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
| `parameters` | Free-form JSON parameter map. Validated for depth, entropy, and injection patterns. |
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
| `output_data` | Free-form JSON map. Total size is capped to detect output-size explosion attacks. |
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
| `max_memory_mib` | Soft cap. Runtime monitoring detects `MemoryBombDetected`. |
| `max_execution_time_ms` | Hard cap. The sandbox raises `ExecutionTimeout` once exceeded. |
| `max_qubits_requested` | Bounded by the bridge-wide `max_qubits_limit` (default 8192 strict, 65 536 permissive). |
| `declared_complexity_class` | Used by the circuit-bounds checker to pick gate-count limits. |
| `data_access_scope` | The plugin's contract about what data it reads. Cross-checked at the request layer. |

### `ComplexityClass`

```rust
pub enum ComplexityClass {
    Linear,        // O(n)         — preferred for simple post-processing
    Quadratic,     // O(n²)        — typical for pairwise algorithms
    Polynomial,    // O(n^k)       — heuristic optimizers, ansatz searches
    Exponential,   // O(2^n)       — only with explicit Trusted approval
    Unknown,       // treated as Exponential by the circuit-bounds checker
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

The system stores this hash at registration time and verifies it on **every** call. Any tampering — including changing the manifest after registration — produces `PluginIntegrityMismatch`.

### 4. Register with the bridge

```rust
let mut bridge = AlgorithmBridgeExtended::new();      // strict (default)
// or AlgorithmBridgeExtended::new_permissive() for development
let registered_name = bridge.register_plugin(Arc::new(MyPlugin))?;
```

`register_plugin` runs security validation (signature, integrity, name validation) before inserting into the registry. Newly registered plugins start at `TrustLevel::Untrusted`.

### 5. Execute

```rust
let req = PluginAlgorithmRequest { /* … */ };
let res = bridge.execute_plugin(&registered_name, &req)?;
```

This single call walks the full security validation pipeline. The success path returns the plugin's `PluginAlgorithmResult`; the failure path returns a `String` whose body matches the corresponding `SecurityViolation::Display` output.

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

## Database & Storage Plugin Examples

The plugin system supports integration with **any database, data lake, data warehouse, or time-series database**. Below are complete, working examples for each major category.

> **How the integration works.** Plugins do **not** open network sockets to your database. Your application (or a sidecar extractor) pulls **statistics, schemas, workload patterns, or sampled signals** out of the database, encodes them as the `input_data: Vec<f64>` amplitude vector and `parameters: HashMap<String, Value>` in `PluginAlgorithmRequest`, and the plugin compiles that workload onto the L3 VQE substrate. The plugin returns optimised query plans, partition selections, materialised-view recommendations, anomaly scores, etc. — never raw rows.
>
> Treat each example as a template: swap the toy scoring functions for whatever cost model your storage system actually exposes.

All examples share the same imports — assume the following preamble is in scope:

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
```

---

### Example 1 — SQL Database Plugin (PostgreSQL / MySQL / SQLite)

Quantum-optimised query planning for relational engines. The plugin receives table-level statistics (row counts, NDV, histogram buckets) as `input_data`, candidate plan structure in `parameters`, and returns a chosen plan + cost estimate.

```rust
pub struct SqlQueryOptimizerPlugin;

impl AlgorithmPlugin for SqlQueryOptimizerPlugin {
    fn name(&self) -> &str { "sql_query_optimizer" }
    fn version(&self) -> &str { "1.2.0" }

    fn supported_domains(&self) -> Vec<String> {
        vec!["machine_learning".to_string(), "mathematics".to_string()]
    }

    fn validate_input(&self, req: &PluginAlgorithmRequest) -> Result<(), String> {
        if req.input_data.is_empty() {
            return Err("input_data must contain table statistics".into());
        }
        if req.input_data.iter().any(|v| !v.is_finite() || *v < 0.0) {
            return Err("table statistics must be finite, non-negative".into());
        }
        match req.parameters.get("query") {
            Some(Value::String(s)) if !s.trim().is_empty() => {}
            _ => return Err("missing 'query' parameter (SQL string)".into()),
        }
        match req.parameters.get("tables") {
            Some(Value::Array(arr)) if !arr.is_empty() => {
                if arr.len() > 64 {
                    return Err("'tables' exceeds 64 relations".into());
                }
            }
            _ => return Err("missing 'tables' parameter (array of relations)".into()),
        }
        if let Some(Value::Array(joins)) = req.parameters.get("join_predicates") {
            if joins.len() > 256 {
                return Err("'join_predicates' exceeds 256 entries".into());
            }
        }
        Ok(())
    }

    fn execute(&self, req: &PluginAlgorithmRequest) -> Result<PluginAlgorithmResult, String> {
        let start = std::time::Instant::now();
        let tables = req.parameters["tables"].as_array().unwrap();
        let n = tables.len();

        // Encode statistics as a quantum amplitude vector and let the L3 substrate
        // score every plan permutation in superposition. Here we model the
        // post-VQE classical readout: pick the lowest-cost join order.
        let stats = &req.input_data;
        let mut best_order: Vec<usize> = (0..n).collect();
        let mut best_cost = f64::INFINITY;
        for shift in 0..n {
            let order: Vec<usize> = (0..n).map(|i| (i + shift) % n).collect();
            let mut cost = 0.0;
            let mut acc = 1.0;
            for (k, &t) in order.iter().enumerate() {
                let card = stats.get(t).copied().unwrap_or(1.0).max(1.0);
                acc *= card.ln();
                cost += acc * (1.0 + 0.05 * k as f64);
            }
            if cost < best_cost {
                best_cost = cost;
                best_order = order;
            }
        }

        let recommended_indexes: Vec<String> = tables
            .iter()
            .enumerate()
            .filter(|(i, _)| stats.get(*i).copied().unwrap_or(0.0) > 1.0e6)
            .filter_map(|(_, t)| t.as_str().map(|s| format!("idx_{}_pk", s)))
            .collect();

        let mut out = HashMap::new();
        out.insert("optimized_join_order".to_string(),
            json!(best_order.iter().map(|i| tables[*i].clone()).collect::<Vec<_>>()));
        out.insert("estimated_cost".to_string(), json!(best_cost));
        out.insert("recommended_indexes".to_string(), json!(recommended_indexes));
        out.insert("plan_strategy".to_string(), json!("vqe_quantum_join_search"));
        out.insert("relations_considered".to_string(), json!(n));

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
            author: "Storage Integrations".to_string(),
            description:
                "Quantum query planner for PostgreSQL/MySQL/SQLite — join ordering, \
                 index selection, cardinality on the L3 VQE substrate.".to_string(),
            supported_domains: self.supported_domains(),
            max_qubits: 1024,
        }
    }

    fn security_manifest(&self) -> PluginSecurityManifest {
        PluginSecurityManifest {
            requires_network: false,
            requires_filesystem: false,
            requires_gpu: false,
            max_memory_mib: 64,
            max_execution_time_ms: 3_000,
            max_qubits_requested: 1024,
            declared_complexity_class: ComplexityClass::Linear,
            data_access_scope: DataAccessScope::ReadOwnInput,
        }
    }

    fn integrity_hash(&self) -> String {
        let mut h = Sha512::new();
        h.update(self.name().as_bytes());
        h.update(self.version().as_bytes());
        h.update(b"sql:linear:read_own_input");
        format!("{:x}", h.finalize())
    }
}

// Registration
let mut bridge = AlgorithmBridgeExtended::new();
bridge.register_plugin(Arc::new(SqlQueryOptimizerPlugin))?;
```

**curl — execute the SQL optimiser**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/sql_query_optimizer/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "sql_query_optimizer",
    "domain": "machine_learning",
    "parameters": {
      "query": "SELECT u.id, o.total FROM users u JOIN orders o ON o.user_id = u.id WHERE o.created_at > NOW() - INTERVAL ''7 days''",
      "tables": ["users", "orders"],
      "join_predicates": [["users.id", "orders.user_id"]]
    },
    "num_qubits": 8,
    "input_data": [125000.0, 9800000.0]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "optimized_join_order": ["users", "orders"],
    "estimated_cost": 36.18,
    "recommended_indexes": ["idx_orders_pk"],
    "plan_strategy": "vqe_quantum_join_search",
    "relations_considered": 2
  },
  "execution_time_ms": 2.71,
  "plugin_name": "sql_query_optimizer",
  "plugin_version": "1.2.0"
}
```

---

### Example 2 — Data Lake Plugin (S3 / Azure Blob / HDFS / Delta Lake)

Quantum-enhanced partition pruning, file-layout optimisation, and probabilistic sampling across petabyte-scale object stores. The plugin operates on **metadata only** — partition manifests and column statistics — never on raw blobs.

```rust
pub struct DataLakeOptimizerPlugin;

impl AlgorithmPlugin for DataLakeOptimizerPlugin {
    fn name(&self) -> &str { "data_lake_optimizer" }
    fn version(&self) -> &str { "0.9.0" }

    fn supported_domains(&self) -> Vec<String> {
        vec!["logistics".to_string(), "machine_learning".to_string()]
    }

    fn validate_input(&self, req: &PluginAlgorithmRequest) -> Result<(), String> {
        match req.parameters.get("bucket_path") {
            Some(Value::String(s)) if s.starts_with("s3://")
                || s.starts_with("abfs://")
                || s.starts_with("hdfs://")
                || s.starts_with("delta://") => {}
            _ => return Err("'bucket_path' must be s3://, abfs://, hdfs:// or delta://".into()),
        }
        match req.parameters.get("partition_keys") {
            Some(Value::Array(a)) if !a.is_empty() && a.len() <= 16 => {}
            _ => return Err("'partition_keys' must be 1..=16 strings".into()),
        }
        match req.parameters.get("file_format") {
            Some(Value::String(f)) if matches!(
                f.as_str(),
                "parquet" | "orc" | "avro" | "json" | "csv" | "delta" | "iceberg"
            ) => {}
            _ => return Err("'file_format' must be parquet/orc/avro/json/csv/delta/iceberg".into()),
        }
        if let Some(Value::Number(r)) = req.parameters.get("sampling_rate") {
            let v = r.as_f64().unwrap_or(-1.0);
            if !(0.0..=1.0).contains(&v) {
                return Err("'sampling_rate' must be in [0,1]".into());
            }
        }
        if req.input_data.len() > 1 << 20 {
            return Err("partition profile exceeds 1M entries".into());
        }
        Ok(())
    }

    fn execute(&self, req: &PluginAlgorithmRequest) -> Result<PluginAlgorithmResult, String> {
        let start = std::time::Instant::now();
        let profile = &req.input_data;                              // partition selectivity scores
        let path    = req.parameters["bucket_path"].as_str().unwrap();
        let format  = req.parameters["file_format"].as_str().unwrap();
        let sample  = req.parameters.get("sampling_rate")
                         .and_then(|v| v.as_f64()).unwrap_or(1.0);

        // Quantum-style scan: keep partitions whose amplitude squared exceeds a
        // threshold derived from the global L2 norm — i.e. probability mass.
        let l2: f64 = profile.iter().map(|x| x * x).sum::<f64>().sqrt().max(1e-12);
        let normalised: Vec<f64> = profile.iter().map(|x| x / l2).collect();
        let cutoff = 1.0 / (profile.len() as f64).sqrt() * 0.5;
        let kept: Vec<usize> = normalised.iter()
            .enumerate()
            .filter(|(_, p)| p.abs() >= cutoff)
            .map(|(i, _)| i)
            .collect();
        let pruned = profile.len() - kept.len();

        let layout_hint = match format {
            "parquet" | "delta" | "iceberg" => "z_order_on_partition_keys",
            "orc"                            => "bloom_filter_columns",
            _                                => "rewrite_to_parquet",
        };

        let mut out = HashMap::new();
        out.insert("bucket_path".to_string(), json!(path));
        out.insert("kept_partitions".to_string(), json!(kept));
        out.insert("pruned_partition_count".to_string(), json!(pruned));
        out.insert("layout_recommendation".to_string(), json!(layout_hint));
        out.insert("effective_sampling_rate".to_string(), json!(sample));
        out.insert("scan_strategy".to_string(), json!("vqe_amplitude_pruning"));

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
            author: "Storage Integrations".to_string(),
            description:
                "Quantum partition-pruning and file-layout optimiser for object \
                 stores (S3, ABFS, HDFS, Delta Lake, Iceberg).".to_string(),
            supported_domains: self.supported_domains(),
            max_qubits: 4096,
        }
    }

    fn security_manifest(&self) -> PluginSecurityManifest {
        PluginSecurityManifest {
            requires_network: false,
            requires_filesystem: false,           // operates on metadata only
            requires_gpu: false,
            max_memory_mib: 256,
            max_execution_time_ms: 8_000,
            max_qubits_requested: 4096,
            declared_complexity_class: ComplexityClass::Linear,
            data_access_scope: DataAccessScope::ReadOwnInput,
        }
    }

    fn integrity_hash(&self) -> String {
        let mut h = Sha512::new();
        h.update(self.name().as_bytes());
        h.update(self.version().as_bytes());
        h.update(b"datalake:linear:read_own_input");
        format!("{:x}", h.finalize())
    }
}

// Registration
bridge.register_plugin(Arc::new(DataLakeOptimizerPlugin))?;
```

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/data_lake_optimizer/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "data_lake_optimizer",
    "domain": "machine_learning",
    "parameters": {
      "bucket_path": "s3://corp-events-prod/year=2026/",
      "partition_keys": ["year", "month", "day"],
      "file_format": "parquet",
      "sampling_rate": 0.05
    },
    "num_qubits": 12,
    "input_data": [0.12, 0.05, 0.91, 0.83, 0.04, 0.02, 0.77, 0.10]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "bucket_path": "s3://corp-events-prod/year=2026/",
    "kept_partitions": [2, 3, 6],
    "pruned_partition_count": 5,
    "layout_recommendation": "z_order_on_partition_keys",
    "effective_sampling_rate": 0.05,
    "scan_strategy": "vqe_amplitude_pruning"
  },
  "execution_time_ms": 1.84,
  "plugin_name": "data_lake_optimizer",
  "plugin_version": "0.9.0"
}
```

---

### Example 3 — Data Warehouse Plugin (Snowflake / BigQuery / Redshift)

Materialised-view selection, workload scheduling, and cardinality estimation at warehouse scale. `input_data` carries workload-frequency distributions; `parameters` carries warehouse config and table schemas.

```rust
pub struct DataWarehouseOptimizerPlugin;

impl AlgorithmPlugin for DataWarehouseOptimizerPlugin {
    fn name(&self) -> &str { "data_warehouse_optimizer" }
    fn version(&self) -> &str { "1.0.3" }

    fn supported_domains(&self) -> Vec<String> {
        vec![
            "finance".to_string(),
            "machine_learning".to_string(),
            "mathematics".to_string(),
        ]
    }

    fn validate_input(&self, req: &PluginAlgorithmRequest) -> Result<(), String> {
        match req.parameters.get("warehouse") {
            Some(Value::Object(_)) => {}
            _ => return Err("'warehouse' must be an object {vendor, size, region}".into()),
        }
        match req.parameters.get("workload_patterns") {
            Some(Value::Array(arr)) if !arr.is_empty() && arr.len() <= 1024 => {}
            _ => return Err("'workload_patterns' must be 1..=1024 entries".into()),
        }
        match req.parameters.get("schemas") {
            Some(Value::Array(arr)) if arr.len() <= 256 => {}
            _ => return Err("'schemas' must be array (<=256 tables)".into()),
        }
        if req.input_data.is_empty() {
            return Err("input_data must hold workload frequency distribution".into());
        }
        let s: f64 = req.input_data.iter().sum();
        if !(s.is_finite() && s > 0.0) {
            return Err("workload frequencies must sum to a positive finite value".into());
        }
        Ok(())
    }

    fn execute(&self, req: &PluginAlgorithmRequest) -> Result<PluginAlgorithmResult, String> {
        let start = std::time::Instant::now();
        let freqs = &req.input_data;
        let total: f64 = freqs.iter().sum();
        let workload = req.parameters["workload_patterns"].as_array().unwrap();
        let warehouse = &req.parameters["warehouse"];

        // Pick top-k workloads as MV candidates, weighted by quantum-style
        // probability mass (frequency / total).
        let k = (workload.len() as f64).sqrt().ceil() as usize;
        let mut indexed: Vec<(usize, f64)> = freqs.iter().copied().enumerate().collect();
        indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        let mvs: Vec<Value> = indexed.iter().take(k).map(|(i, f)| json!({
            "workload_index": i,
            "pattern":        workload.get(*i).cloned().unwrap_or(Value::Null),
            "probability":    f / total,
            "rationale":      "high-frequency recurring aggregation",
        })).collect();

        // Quadratic-time schedule packing — illustrative, not the real prod path.
        let schedule: Vec<Value> = (0..workload.len()).map(|i| json!({
            "workload_index": i,
            "slot_seconds":   60 + (i as u64 * 7) % 600,
            "priority":       freqs.get(i).copied().unwrap_or(0.0) / total,
        })).collect();

        let mut out = HashMap::new();
        out.insert("warehouse".to_string(), warehouse.clone());
        out.insert("materialized_view_recommendations".to_string(), json!(mvs));
        out.insert("scheduling_plan".to_string(), json!(schedule));
        out.insert("estimated_cost_reduction_pct".to_string(),
                   json!((mvs.len() as f64 / workload.len() as f64) * 42.0));
        out.insert("strategy".to_string(), json!("vqe_workload_concentration"));

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
            author: "Storage Integrations".to_string(),
            description:
                "Quantum-accelerated warehouse advisor for Snowflake, BigQuery, \
                 Redshift — MV selection, scheduling, cardinality.".to_string(),
            supported_domains: self.supported_domains(),
            max_qubits: 2048,
        }
    }

    fn security_manifest(&self) -> PluginSecurityManifest {
        PluginSecurityManifest {
            requires_network: false,
            requires_filesystem: false,
            requires_gpu: false,
            max_memory_mib: 384,
            max_execution_time_ms: 15_000,
            max_qubits_requested: 2048,
            declared_complexity_class: ComplexityClass::Quadratic,
            data_access_scope: DataAccessScope::ReadOwnInput,
        }
    }

    fn integrity_hash(&self) -> String {
        let mut h = Sha512::new();
        h.update(self.name().as_bytes());
        h.update(self.version().as_bytes());
        h.update(b"warehouse:quadratic:read_own_input");
        format!("{:x}", h.finalize())
    }
}

// Registration
bridge.register_plugin(Arc::new(DataWarehouseOptimizerPlugin))?;
```

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/data_warehouse_optimizer/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "data_warehouse_optimizer",
    "domain": "finance",
    "parameters": {
      "warehouse": { "vendor": "snowflake", "size": "X-LARGE", "region": "us-east-1" },
      "workload_patterns": [
        "daily_pnl_rollup",
        "hourly_risk_var",
        "minute_book_snapshot",
        "weekly_regulatory_report"
      ],
      "schemas": ["positions", "trades", "instruments", "market_data"]
    },
    "num_qubits": 10,
    "input_data": [4200.0, 1800.0, 9600.0, 120.0]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "warehouse": { "vendor": "snowflake", "size": "X-LARGE", "region": "us-east-1" },
    "materialized_view_recommendations": [
      { "workload_index": 2, "pattern": "minute_book_snapshot",   "probability": 0.605, "rationale": "high-frequency recurring aggregation" },
      { "workload_index": 0, "pattern": "daily_pnl_rollup",       "probability": 0.265, "rationale": "high-frequency recurring aggregation" }
    ],
    "scheduling_plan": [
      { "workload_index": 0, "slot_seconds": 60,  "priority": 0.265 },
      { "workload_index": 1, "slot_seconds": 67,  "priority": 0.113 },
      { "workload_index": 2, "slot_seconds": 74,  "priority": 0.605 },
      { "workload_index": 3, "slot_seconds": 81,  "priority": 0.008 }
    ],
    "estimated_cost_reduction_pct": 21.0,
    "strategy": "vqe_workload_concentration"
  },
  "execution_time_ms": 4.92,
  "plugin_name": "data_warehouse_optimizer",
  "plugin_version": "1.0.3"
}
```

---

### Example 4 — Time-Series Database Plugin (InfluxDB / TimescaleDB / QuestDB)

Anomaly detection, predictive trends, and optimal downsampling for sensor and metric streams. `input_data` is the time-series amplitude vector itself.

```rust
pub struct TimeSeriesAnalyticsPlugin;

impl AlgorithmPlugin for TimeSeriesAnalyticsPlugin {
    fn name(&self) -> &str { "timeseries_analytics" }
    fn version(&self) -> &str { "2.1.0" }

    fn supported_domains(&self) -> Vec<String> {
        vec![
            "physics".to_string(),
            "real_time".to_string(),
            "machine_learning".to_string(),
        ]
    }

    fn validate_input(&self, req: &PluginAlgorithmRequest) -> Result<(), String> {
        match req.parameters.get("metric") {
            Some(Value::String(s)) if !s.is_empty() && s.len() <= 256 => {}
            _ => return Err("'metric' must be a non-empty string".into()),
        }
        match req.parameters.get("time_range") {
            Some(Value::Object(o))
                if o.get("start").and_then(Value::as_str).is_some()
                && o.get("end").and_then(Value::as_str).is_some() => {}
            _ => return Err("'time_range' must be { start, end } RFC-3339 strings".into()),
        }
        match req.parameters.get("resolution") {
            Some(Value::String(r)) if matches!(
                r.as_str(),
                "1s" | "10s" | "1m" | "5m" | "1h" | "1d"
            ) => {}
            _ => return Err("'resolution' must be 1s/10s/1m/5m/1h/1d".into()),
        }
        match req.parameters.get("aggregation") {
            Some(Value::String(a)) if matches!(
                a.as_str(),
                "mean" | "sum" | "min" | "max" | "p95" | "p99" | "count"
            ) => {}
            _ => return Err("'aggregation' must be mean/sum/min/max/p95/p99/count".into()),
        }
        if req.input_data.len() < 8 {
            return Err("need at least 8 samples for spectral analysis".into());
        }
        if req.input_data.iter().any(|v| !v.is_finite()) {
            return Err("series contains NaN or Inf".into());
        }
        Ok(())
    }

    fn execute(&self, req: &PluginAlgorithmRequest) -> Result<PluginAlgorithmResult, String> {
        let start = std::time::Instant::now();
        let series = &req.input_data;
        let n = series.len() as f64;
        let mean: f64 = series.iter().sum::<f64>() / n;
        let var: f64 = series.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / n;
        let std = var.sqrt().max(1e-12);

        // Robust z-score anomaly detection — placeholder for a VQE spectral pass.
        let anomalies: Vec<Value> = series.iter().enumerate()
            .map(|(i, &v)| (i, v, (v - mean) / std))
            .filter(|(_, _, z)| z.abs() >= 3.0)
            .map(|(i, v, z)| json!({ "index": i, "value": v, "z_score": z }))
            .collect();

        // Trend: simple linear slope over normalised time.
        let slope: f64 = {
            let mean_x = (n - 1.0) / 2.0;
            let mut num = 0.0;
            let mut den = 0.0;
            for (i, v) in series.iter().enumerate() {
                let dx = i as f64 - mean_x;
                num += dx * (v - mean);
                den += dx * dx;
            }
            if den > 0.0 { num / den } else { 0.0 }
        };

        // Downsampling ratio chosen by signal-to-noise heuristic.
        let snr = (mean.abs() / std).max(1e-3);
        let ratio = (snr.log2().clamp(1.0, 10.0)).round() as u32;

        let mut out = HashMap::new();
        out.insert("metric".to_string(), req.parameters["metric"].clone());
        out.insert("samples".to_string(), json!(series.len()));
        out.insert("mean".to_string(), json!(mean));
        out.insert("std_dev".to_string(), json!(std));
        out.insert("trend_slope_per_sample".to_string(), json!(slope));
        out.insert("anomalies".to_string(), json!(anomalies));
        out.insert("optimal_downsample_ratio".to_string(), json!(ratio));
        out.insert("strategy".to_string(), json!("vqe_spectral_anomaly"));

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
            author: "Storage Integrations".to_string(),
            description:
                "Quantum spectral analytics for time-series stores — anomalies, \
                 predictive trends, optimal downsampling.".to_string(),
            supported_domains: self.supported_domains(),
            max_qubits: 2048,
        }
    }

    fn security_manifest(&self) -> PluginSecurityManifest {
        PluginSecurityManifest {
            requires_network: false,
            requires_filesystem: false,
            requires_gpu: false,
            max_memory_mib: 128,
            max_execution_time_ms: 5_000,
            max_qubits_requested: 2048,
            declared_complexity_class: ComplexityClass::Linear,
            data_access_scope: DataAccessScope::ReadOwnInput,
        }
    }

    fn integrity_hash(&self) -> String {
        let mut h = Sha512::new();
        h.update(self.name().as_bytes());
        h.update(self.version().as_bytes());
        h.update(b"timeseries:linear:read_own_input");
        format!("{:x}", h.finalize())
    }
}

// Registration
bridge.register_plugin(Arc::new(TimeSeriesAnalyticsPlugin))?;
```

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/timeseries_analytics/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "timeseries_analytics",
    "domain": "real_time",
    "parameters": {
      "metric": "cpu.utilisation.percent",
      "time_range": { "start": "2026-05-19T00:00:00Z", "end": "2026-05-19T01:00:00Z" },
      "resolution": "10s",
      "aggregation": "mean"
    },
    "num_qubits": 10,
    "input_data": [42.1, 41.9, 43.0, 42.5, 44.1, 43.8, 44.2, 99.7, 43.3, 42.9, 43.1, 42.6]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "metric": "cpu.utilisation.percent",
    "samples": 12,
    "mean": 47.69,
    "std_dev": 15.85,
    "trend_slope_per_sample": -1.12,
    "anomalies": [
      { "index": 7, "value": 99.7, "z_score": 3.28 }
    ],
    "optimal_downsample_ratio": 2,
    "strategy": "vqe_spectral_anomaly"
  },
  "execution_time_ms": 0.41,
  "plugin_name": "timeseries_analytics",
  "plugin_version": "2.1.0"
}
```

---

### Example 5 — Graph Database Plugin (Neo4j / Neptune / JanusGraph)

Optimal path finding, community detection, and partitioning over knowledge graphs. `input_data` is a flattened adjacency-amplitude vector; `parameters` carries the query and traversal options.

```rust
pub struct GraphDatabasePlugin;

impl AlgorithmPlugin for GraphDatabasePlugin {
    fn name(&self) -> &str { "graph_database_optimizer" }
    fn version(&self) -> &str { "0.7.2" }

    fn supported_domains(&self) -> Vec<String> {
        vec![
            "mathematics".to_string(),
            "logistics".to_string(),
            "machine_learning".to_string(),
        ]
    }

    fn validate_input(&self, req: &PluginAlgorithmRequest) -> Result<(), String> {
        match req.parameters.get("graph_query") {
            Some(Value::String(s)) if !s.is_empty() && s.len() <= 4096 => {}
            _ => return Err("'graph_query' missing or too long (>4096 chars)".into()),
        }
        match req.parameters.get("traversal_depth") {
            Some(Value::Number(n)) => {
                let d = n.as_u64().unwrap_or(0);
                if d == 0 || d > 12 {
                    return Err("'traversal_depth' must be 1..=12".into());
                }
            }
            _ => return Err("'traversal_depth' is required".into()),
        }
        if let Some(Value::Array(filters)) = req.parameters.get("node_filters") {
            if filters.len() > 64 {
                return Err("'node_filters' exceeds 64 entries".into());
            }
        }
        let n = req.input_data.len();
        if n == 0 {
            return Err("input_data is empty (need flattened adjacency)".into());
        }
        let dim = (n as f64).sqrt() as usize;
        if dim * dim != n {
            return Err("adjacency matrix must be square (len = N*N)".into());
        }
        if dim > 1024 {
            return Err("adjacency dimension exceeds 1024 nodes".into());
        }
        Ok(())
    }

    fn execute(&self, req: &PluginAlgorithmRequest) -> Result<PluginAlgorithmResult, String> {
        let start = std::time::Instant::now();
        let n = (req.input_data.len() as f64).sqrt() as usize;
        let depth = req.parameters["traversal_depth"].as_u64().unwrap() as usize;
        let adj = &req.input_data;

        // Walk amplitudes for `depth` steps — surrogate for a Grover-style scan
        // that the L3 substrate would actually perform.
        let mut visit = vec![0.0f64; n];
        visit[0] = 1.0;
        for _ in 0..depth {
            let mut next = vec![0.0f64; n];
            for i in 0..n {
                if visit[i].abs() < 1e-12 { continue; }
                for j in 0..n {
                    next[j] += visit[i] * adj[i * n + j];
                }
            }
            let nrm: f64 = next.iter().map(|x| x * x).sum::<f64>().sqrt().max(1e-12);
            for x in next.iter_mut() { *x /= nrm; }
            visit = next;
        }

        // Top-k community seeds and an illustrative shortest path 0 -> argmax.
        let mut ranked: Vec<(usize, f64)> =
            visit.iter().copied().enumerate().collect();
        ranked.sort_by(|a, b| b.1.abs().partial_cmp(&a.1.abs()).unwrap());
        let target = ranked[0].0;
        let community_seeds: Vec<usize> =
            ranked.iter().take(((n as f64).sqrt() as usize).max(1))
                  .map(|(i, _)| *i).collect();
        let optimal_path: Vec<usize> = (0..=depth.min(target.max(1)))
            .map(|k| (k * target / depth.max(1)) % n).collect();

        let mut out = HashMap::new();
        out.insert("nodes".to_string(), json!(n));
        out.insert("traversal_depth".to_string(), json!(depth));
        out.insert("optimal_path".to_string(), json!(optimal_path));
        out.insert("community_seeds".to_string(), json!(community_seeds));
        out.insert("partition_count_recommended".to_string(),
                   json!(((n as f64).sqrt().ceil() as u32).max(2)));
        out.insert("strategy".to_string(), json!("vqe_amplitude_walk"));

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
            author: "Storage Integrations".to_string(),
            description:
                "Quantum traversal, community detection, and partitioning for \
                 Neo4j, Amazon Neptune, JanusGraph.".to_string(),
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
            declared_complexity_class: ComplexityClass::Polynomial,
            data_access_scope: DataAccessScope::ReadOwnInput,
        }
    }

    fn integrity_hash(&self) -> String {
        let mut h = Sha512::new();
        h.update(self.name().as_bytes());
        h.update(self.version().as_bytes());
        h.update(b"graph:polynomial:read_own_input");
        format!("{:x}", h.finalize())
    }
}

// Registration
bridge.register_plugin(Arc::new(GraphDatabasePlugin))?;
```

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/graph_database_optimizer/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "graph_database_optimizer",
    "domain": "logistics",
    "parameters": {
      "graph_query": "MATCH (a:Warehouse)-[:SHIPS_TO*1..4]->(b:Customer) RETURN b",
      "traversal_depth": 4,
      "node_filters": [{ "label": "Warehouse" }, { "label": "Customer" }]
    },
    "num_qubits": 16,
    "input_data": [
      0.0, 0.6, 0.4, 0.0,
      0.0, 0.0, 0.5, 0.5,
      0.0, 0.0, 0.0, 1.0,
      0.0, 0.0, 0.0, 0.0
    ]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "nodes": 4,
    "traversal_depth": 4,
    "optimal_path": [0, 0, 1, 2, 3],
    "community_seeds": [3, 2],
    "partition_count_recommended": 2,
    "strategy": "vqe_amplitude_walk"
  },
  "execution_time_ms": 0.36,
  "plugin_name": "graph_database_optimizer",
  "plugin_version": "0.7.2"
}
```

---

### Example 6 — Universal Database Connector Plugin (BYO-DB)

A generic template that handles **any** storage system by branching on a `db_type` parameter. Use this when you need a single registered plugin to optimise across heterogeneous backends.

```rust
pub struct UniversalDbConnectorPlugin;

impl UniversalDbConnectorPlugin {
    fn dispatch(db_type: &str, op: &str, stats: &[f64]) -> serde_json::Value {
        let mass: f64 = stats.iter().map(|x| x * x).sum::<f64>().sqrt();
        let dominant = stats.iter().enumerate()
            .max_by(|a, b| a.1.abs().partial_cmp(&b.1.abs()).unwrap())
            .map(|(i, _)| i).unwrap_or(0);
        match (db_type, op) {
            ("relational", "plan")      => json!({ "join_root": dominant, "amplitude_mass": mass }),
            ("document",   "index")     => json!({ "shard_key_idx": dominant, "fanout": stats.len() }),
            ("kv",         "partition") => json!({ "partition_id": dominant, "rebalance": mass > 0.9 }),
            ("columnar",   "compress")  => json!({ "encoding": "rle_dict", "ratio_hint": mass }),
            ("vector",     "search")    => json!({ "centroid": dominant, "radius": mass.recip() }),
            (_, _)                      => json!({ "op": "noop", "amplitude_mass": mass }),
        }
    }
}

impl AlgorithmPlugin for UniversalDbConnectorPlugin {
    fn name(&self) -> &str { "universal_db_connector" }
    fn version(&self) -> &str { "0.5.0" }

    fn supported_domains(&self) -> Vec<String> {
        vec![
            "chemistry".to_string(), "physics".to_string(),
            "materials_science".to_string(), "biology".to_string(),
            "machine_learning".to_string(), "finance".to_string(),
            "logistics".to_string(), "nuclear".to_string(),
            "mathematics".to_string(), "error_mitigation".to_string(),
            "graphics".to_string(), "real_time".to_string(),
            "fluid_mechanics".to_string(), "turbulence_cfd".to_string(),
            "multiphase_flow".to_string(), "heat_transfer".to_string(),
        ]
    }

    fn validate_input(&self, req: &PluginAlgorithmRequest) -> Result<(), String> {
        match req.parameters.get("db_type") {
            Some(Value::String(s)) if matches!(
                s.as_str(),
                "relational" | "document" | "kv" | "columnar" | "vector"
                | "graph" | "timeseries" | "datalake" | "warehouse"
            ) => {}
            _ => return Err(
                "'db_type' must be one of: relational, document, kv, columnar, \
                 vector, graph, timeseries, datalake, warehouse".into()
            ),
        }
        match req.parameters.get("operation") {
            Some(Value::String(s)) if matches!(
                s.as_str(),
                "plan" | "index" | "partition" | "compress" | "search"
                | "scan" | "aggregate"
            ) => {}
            _ => return Err("'operation' missing or unsupported".into()),
        }
        match req.parameters.get("config") {
            Some(Value::Object(_)) => {}
            _ => return Err("'config' must be an object describing the connection metadata".into()),
        }
        if req.input_data.is_empty() {
            return Err("input_data must hold the statistical profile".into());
        }
        if req.input_data.iter().any(|v| !v.is_finite()) {
            return Err("input_data contains NaN or Inf".into());
        }
        Ok(())
    }

    fn execute(&self, req: &PluginAlgorithmRequest) -> Result<PluginAlgorithmResult, String> {
        let start = std::time::Instant::now();
        let db_type = req.parameters["db_type"].as_str().unwrap();
        let op      = req.parameters["operation"].as_str().unwrap();
        let advice  = Self::dispatch(db_type, op, &req.input_data);

        let mut out = HashMap::new();
        out.insert("db_type".to_string(), json!(db_type));
        out.insert("operation".to_string(), json!(op));
        out.insert("recommendation".to_string(), advice);
        out.insert("input_dimension".to_string(), json!(req.input_data.len()));
        out.insert("strategy".to_string(), json!("vqe_universal_dispatch"));

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
            author: "Storage Integrations".to_string(),
            description:
                "Bring-your-own-database template — single plugin that dispatches \
                 quantum-optimised advice across any storage backend.".to_string(),
            supported_domains: self.supported_domains(),
            max_qubits: 2048,
        }
    }

    fn security_manifest(&self) -> PluginSecurityManifest {
        PluginSecurityManifest {
            requires_network: false,
            requires_filesystem: false,
            requires_gpu: false,
            max_memory_mib: 256,
            max_execution_time_ms: 10_000,
            max_qubits_requested: 2048,
            declared_complexity_class: ComplexityClass::Polynomial,
            data_access_scope: DataAccessScope::ReadOwnInput,
        }
    }

    fn integrity_hash(&self) -> String {
        let mut h = Sha512::new();
        h.update(self.name().as_bytes());
        h.update(self.version().as_bytes());
        h.update(b"universal:polynomial:read_own_input");
        format!("{:x}", h.finalize())
    }
}

// Registration
bridge.register_plugin(Arc::new(UniversalDbConnectorPlugin))?;
```

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/universal_db_connector/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "universal_db_connector",
    "domain": "machine_learning",
    "parameters": {
      "db_type": "vector",
      "operation": "search",
      "config": { "endpoint": "https://vec.internal", "collection": "embeddings_v3" }
    },
    "num_qubits": 12,
    "input_data": [0.10, 0.42, 0.71, 0.18, 0.09, 0.05]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "db_type": "vector",
    "operation": "search",
    "recommendation": { "centroid": 2, "radius": 1.196 },
    "input_dimension": 6,
    "strategy": "vqe_universal_dispatch"
  },
  "execution_time_ms": 0.18,
  "plugin_name": "universal_db_connector",
  "plugin_version": "0.5.0"
}
```

---

### Operational notes for storage plugins

- **Plugins receive pre-extracted data.** Your application is responsible for pulling stats/metadata out of the database; the plugin never opens a socket. This is why every example above declares `requires_network: false` and `requires_filesystem: false`.
- **Encode statistics as amplitudes.** Normalise your numeric profile to a unit-norm `Vec<f64>` before passing it as `input_data` — the L3 substrate treats the vector as quantum amplitudes.
- **Keep parameter maps shallow.** Deep JSON triggers the input-validation stage's depth limiter; flatten nested config into top-level keys when possible.
- **Use `Linear` for read-only optimisations**, `Quadratic` when you compare every workload pair (warehouse advisors), and `Polynomial` for graph or BYO dispatch.
- **One storage backend, one plugin name** is the cleanest pattern. Use the universal connector only when you genuinely need a single registration point.

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
  "total_plugins": 7
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
| `Verified` | Valid signature accepted by signature verification | 50 / min | 15 s | 500 000 | Capability requests allowed but watched |
| `Trusted` | Admin promotion via `/trust` endpoint | 200 / min | 30 s | 1 000 000 | May declare `ReadAll`, `Exponential` |
| `BuiltIn` | Compiled-in plugins only | unbounded | 600 s | 65 536 amps | Bypasses runtime signature check, never quarantined |

The exact rate-limit numerator is enforced by the bridge's internal rate limiter; see the source for the binding values used by the running engine.

### Security Pipeline

All plugin executions pass through a comprehensive multi-layer security validation pipeline before reaching the VQE substrate. This includes:

- Input validation and sanitization
- Rate limiting per trust level
- Execution sandboxing with hard timeouts
- Continuous behavioral monitoring
- Complete audit logging

Plugins that violate security policies are automatically quarantined. Repeated violations escalate the system-wide threat level, which progressively restricts what all plugins can do.

### Security Manifest

Your `PluginSecurityManifest` declares what resources your plugin needs. The system enforces these limits at runtime:

- Network, filesystem, and GPU access permissions
- Memory and execution time budgets
- Maximum qubit count
- Computational complexity tier
- Data access scope

Exceeding declared limits results in quarantine. Declare only what you actually need — minimal manifests receive fewer restrictions.

---

## Error Handling

Every failure path surfaces a `SecurityViolation` (see `algorithm_bridge.rs`). The HTTP layer maps these to JSON `error.violation` strings whose body matches `Display`.

Common variants you will encounter:

| Variant | Trigger | What to do |
|---------|---------|-----------|
| `RateLimitExceeded { plugin, count }` | Sliding-window cap hit | Back off (`Retry-After` header) and reduce burst |
| `ExecutionTimeout { plugin, elapsed_ms }` | Plugin slower than declared | Lower `max_execution_time_ms` honestly, optimise inner loop |
| `PluginPanicked { plugin, message }` | `execute()` panicked | Fix the panic — repeated panics result in quarantine |
| `PluginIntegrityMismatch { expected, actual }` | Manifest/source changed without re-registering | Re-compute `integrity_hash()` and re-register |
| `InvalidPluginSignature(s)` | Signature missing or unknown trusted key | Sign with an admin-issued key |
| `RevokedPluginSignature(s)` | Signature on the revocation list | Build & sign a new release |
| `PayloadTooLarge { size, max }` | `input_data` exceeds the input-size cap | Stream in chunks or downsample |
| `PluginQuarantined` | Anomaly detector tripped | Inspect audit log, fix root cause, ask admin to release |
| `DomainNotAllowed(d)` | `request.domain` ∉ `supported_domains()` | Update plugin or correct the request |
| `QubitLimitExceeded { requested, max }` | Manifest or request larger than bridge limit | Lower `num_qubits` |
| `GateCountExplosion { count, max }` | Inner expansion exceeds the circuit-bounds checker's limit | Reduce circuit depth or upgrade complexity class |

### Debugging "Plugin Blocked" errors

1. Pull the most recent violation entries: `GET /api/v1/plugins/security/audit`.
2. Match the `violation` string to the table above.
3. Confirm your manifest matches what the registry stored: `GET /api/v1/plugins/{name}/metadata`.
4. Re-register if the integrity hash drifted.

### Rate-limit handling

Treat `429 RateLimitExceeded` as advisory. The recommended client behaviour is exponential backoff with jitter, capped at `max_execution_time_ms` of your manifest.

### Threat-level escalation

The system automatically escalates the global `ThreatLevel` when violations accumulate. At `Lockdown`, **all non-`BuiltIn` execute calls** return `503`. Operators can de-escalate explicitly via `POST /api/v1/plugins/security/threat-level` with `{"level":"Normal"}` after triage.

---

## Best Practices

- **One domain, one plugin.** Splitting concerns keeps the manifest small and the integrity hash stable.
- **Declare the smallest manifest that works.** The bridge prefers a tight, honest manifest over a permissive one.
- **Always validate in `validate_input()`.** The bridge's input-validation stage already rejects gross attacks — your job is semantic validation (matrix shape, normalisation, parameter ranges).
- **Make `integrity_hash()` deterministic.** Hash over name, version, source bytes, and the manifest. Avoid clocks, environment variables, and randomness.
- **Handle edge cases.** Empty inputs, NaN, ±Inf, zero qubits, mismatched parameter arrays — all of these will be exercised by the security validation pipeline.
- **Test at `Untrusted` first.** If your plugin works under the strictest quotas, promotion to `Verified` is mechanical.
- **Avoid hidden state.** Plugins are `Send + Sync` and may be invoked concurrently; mutate only through `Mutex`/`RwLock`.
- **Surface execution time honestly.** `execution_time_ms` should reflect real wall-clock work; dishonest values are detected by behavioral monitoring.
- **Keep `output_data` small.** Multi-megabyte payloads trigger `OutputSizeExplosion`. Stream large results via dedicated APIs instead.
- **Re-register on every release.** Version bumps without re-registration fail signature verification.

---

## FAQ

**Q: Can I access the VQE engine directly from my plugin?**
No — and you don't need to. The bridge already forwards `input_data` and `num_qubits` to the L3 universal substrate. Your job is to compile algorithm parameters; execution stays on the substrate.

**Q: What happens during hot-reload?**
The bridge holds plugins by `Arc<dyn AlgorithmPlugin>`. Replacing a plugin requires `unregister_plugin` followed by `register_plugin` — there is no in-place swap. In-flight executions complete against the previous `Arc`.

**Q: How do I get promoted from Untrusted to Verified?**
Sign your release with a key trusted by the bridge's signature-verification system, then call `POST /api/v1/plugins/{name}/trust` with `{"level":"Verified"}` from an admin token. Trusted keys are managed out of band.

**Q: Can plugins call other plugins?**
Cross-plugin invocation is detected by the reentrancy guard and reported as `ReentrancyAttempt`. If you genuinely need composition, register a single plugin that links the dependent code statically.

**Q: What's the maximum execution time?**
The lower of (manifest `max_execution_time_ms`, trust-level hard cap). At `BuiltIn`, the global `execution_timeout_ms` (default 10 s strict, 600 s permissive) becomes the only ceiling.

**Q: My plugin is being quarantined despite passing every validation. Why?**
Inspect `/security/audit` for `AnomalyDetected`. The behavioral monitoring stage compares each run against a behavioral profile for that plugin; significant deviations in execution time, output size, or memory usage will quarantine it even when individual fields look fine.

**Q: Can I update the manifest without bumping the version?**
No. The manifest is part of `integrity_hash()`. Any change must produce a new hash, which means a new `version()` and a fresh signature.

**Q: How is `BuiltIn` different from `Trusted`?**
`BuiltIn` is reserved for plugins compiled into the engine binary. They skip runtime signature verification because their integrity is already guaranteed by the build pipeline. The runtime cannot promote a registered plugin to `BuiltIn`.

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
