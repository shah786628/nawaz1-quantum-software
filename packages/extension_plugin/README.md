# Extension & Plugin System — Custom Quantum Algorithm Interface

## Overview

The **Extension & Plugin System** lets you ship your own quantum algorithms into the running engine without forking the codebase. Plugins are first-class components that implement a single trait, get vetted by a **multi-layer security validation pipeline**, and then run on the same universal **VQE execution substrate** that powers every built-in domain.

**Core principle:** plugins do *not* select a different quantum backend, **and they do not choose qubit counts either**. The Algorithm Interface **compiles** your custom algorithm onto the VQE execution substrate; only the parameter vectors, metadata, and post-processing change — the underlying execution remains the universal VQE substrate. The number of qubits used per call is **auto-selected by the engine's qubit allocation logic** from your `input_data` — via Born normalization, Shannon-entropy complexity analysis, element count, and quantum state complexity — up to the engine's ceiling of 65 536 qubits. Plugins just hand over meaningful amplitude data; the engine handles qubit allocation, normalization, and quantum state preparation automatically.

```
┌────────────────────────────────────────────────────────────────┐
│   Your custom algorithm (UCC variant, custom QAOA, hybrid …)   │
└─────────────────────────────────┬──────────────────────────────┘
                                  │ implements AlgorithmPlugin
                                  ▼
       ┌─────────────────────────────────────────────────────┐
       │   Extension Plugin Security                         │
       │   (Multi-layer security validation pipeline)        │
       └─────────────────────────────────┬───────────────────┘
                                         │ validated
                                         ▼
       ┌─────────────────────────────────────────────────────┐
       │   Algorithm Interface                               │
       │   (Universal algorithm → VQE compiler)              │
       │   (Auto-compiles any algorithm, including           │
       │    unknown algorithms via adaptive fallback)        │
       └─────────────────────────────────┬───────────────────┘
                                         │ parameter vector
                                         ▼
                ┌─────────────────────────────────────┐
                │   VQE Execution Substrate           │
                │   (engine auto-selects qubit        │
                │    width per call; ≤ 65 536)        │
                └─────────────────────────────────────┘
```

**Base URL:** `http://localhost:8080`

---

## Qubit Allocation

**You do not select qubits.** The quantum engine automatically determines the optimal qubit count for your problem.

When your plugin provides `input_data`, the engine:

1. **Normalizes** the data to a valid quantum state (Born normalization, ‖ψ‖₂ = 1).
2. **Analyzes complexity** via Shannon entropy measurement on the normalized amplitudes.
3. **Evaluates** element count, quantum state complexity, and entanglement structure.
4. **Auto-selects** the optimal qubit width from these factors (the engine's qubit allocation logic takes the maximum of the three lower bounds, capped at the engine's ceiling of 65 536 qubits).

The `num_qubits` field in `PluginAlgorithmRequest` is **advisory only** — the engine's qubit allocation logic makes the final decision and will override it whenever its analysis demands a different width. Setting it to `0` (or any reasonable default) is fine; the engine will pick the right number regardless.

The `max_qubits_requested` field in `PluginSecurityManifest` is a **security cap**, not an allocation. It declares the upper bound your plugin is allowed to consume so the bridge can refuse runs that would exceed your declared budget — set it honestly to the largest width your most complex use case could legitimately need.

**Your job as a plugin author:** provide meaningful amplitude data in `input_data`. The engine handles qubit allocation, normalization, and quantum state preparation automatically.

---

## Quick Start

A minimal, working `AlgorithmPlugin` implementation:

```typescript
// AlgorithmPlugin implementation: HelloPlugin
// ─────────────────────────────────────────────

// Plugin identity
name(): "hello-plugin"
version(): "0.1.0"
supported_domains(): ["mathematics"]

// Input validation
validate_input(request):
    if request.input_data is empty → error("input_data is empty")
    if request.input_data contains NaN or Inf → error("invalid values")
    return ok

// Core execution
execute(request):
    start_timer()
    sum = sum_of(request.input_data)
    return {
        success: true,
        output_data: { "sum": sum, "samples": request.input_data.length },
        execution_time_ms: elapsed_ms(),
        plugin_name: "hello-plugin",
        plugin_version: "0.1.0"
    }

// Metadata
metadata():
    name: "hello-plugin"
    version: "0.1.0"
    author: "Your Name"
    description: "Reference hello-world plugin."
    supported_domains: ["mathematics"]
    max_qubits: 64

// Security manifest
security_manifest():
    requires_network: false
    requires_filesystem: false
    requires_gpu: false
    max_memory_mib: 16
    max_execution_time_ms: 1000
    max_qubits_requested: 64
    declared_complexity_class: Linear
    data_access_scope: ReadOwnInput

// Integrity hash
integrity_hash(): "hello-plugin@0.1.0:linear:read_own_input"

// Registration and execution
bridge = new ExtensionPluginSecurity()
bridge.register_plugin(HelloPlugin)
request = {
    algorithm_name: "hello",
    domain: "mathematics",
    parameters: {},
    num_qubits: 0,    // Engine auto-selects optimal qubits from input_data
    input_data: [1.0, 2.0, 3.0, 4.0]
}
result = bridge.execute_plugin("hello-plugin", request)
print(result.output_data)
```

That is the entire contract. Every method on `AlgorithmPlugin` is required.

---

## The `AlgorithmPlugin` Trait

The trait defines the complete plugin interface:

```typescript
// AlgorithmPlugin trait — all methods required
interface AlgorithmPlugin {
    name(): string;
    version(): string;
    supported_domains(): string[];
    execute(request: PluginAlgorithmRequest): Result<PluginAlgorithmResult, string>;
    validate_input(request: PluginAlgorithmRequest): Result<void, string>;
    metadata(): PluginMetadata;
    security_manifest(): PluginSecurityManifest;
    integrity_hash(): string;
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

```typescript
interface PluginAlgorithmRequest {
    algorithm_name: string;        // Logical name selected by the caller
    domain: string;                // One of the 16 supported quantum domains
    parameters: Record<string, any>;  // Free-form JSON parameter map
    num_qubits: number;            // Advisory hint only — engine auto-selects
    input_data: number[];          // Raw amplitude vector (quantum amplitudes)
}
```

| Field | Meaning |
|-------|---------|
| `algorithm_name` | Logical name selected by the caller (the plugin can ignore or branch on it). |
| `domain` | One of the 16 supported quantum domains. Must intersect `supported_domains()`. |
| `parameters` | Free-form JSON parameter map. Validated for depth, entropy, and injection patterns. |
| `num_qubits` | **Advisory hint only — the engine's qubit allocation logic auto-selects the optimal qubit width** from `input_data` (Born normalization → Shannon entropy → element count → quantum state complexity) and will override this value whenever its analysis demands a different width. Setting it to `0` is fine. The actual width is still bounded by the manifest's `max_qubits_requested` security cap. |
| `input_data` | Raw amplitude vector. Treated as quantum amplitudes by the VQE substrate. |

### `PluginAlgorithmResult`

```typescript
interface PluginAlgorithmResult {
    success: boolean;
    output_data: Record<string, any>;
    execution_time_ms: number;
    plugin_name: string;
    plugin_version: string;
}
```

| Field | Meaning |
|-------|---------|
| `success` | `true` only when the plugin completed normally. Error paths must return `Err(String)` from `execute()` rather than `Ok` with `success = false`. |
| `output_data` | Free-form JSON map. Total size is capped to detect output-size explosion attacks. |
| `execution_time_ms` | Wall-clock milliseconds inside `execute()`. The bridge cross-checks against `security_manifest().max_execution_time_ms` and against historical baselines. |
| `plugin_name` / `plugin_version` | Should match `name()` / `version()`. Mismatch is logged. |

### `PluginMetadata`

```typescript
interface PluginMetadata {
    name: string;
    version: string;
    author: string;
    description: string;
    supported_domains: string[];
    max_qubits: number;
}
```

Returned by `metadata()` and surfaced verbatim through `GET /api/v1/plugins/list` and `GET /api/v1/plugins/{name}/metadata`.

> **Note:** `max_qubits` in `PluginMetadata` is informational only. Actual qubit limits are enforced via `PluginSecurityManifest.max_qubits_requested`.

> **Serialization:** All three types (`PluginAlgorithmRequest`, `PluginAlgorithmResult`, `PluginMetadata`) support full JSON serialization and deserialization for seamless integration.

### `PluginSecurityManifest`

```typescript
interface PluginSecurityManifest {
    requires_network: boolean;
    requires_filesystem: boolean;
    requires_gpu: boolean;
    max_memory_mib: number;
    max_execution_time_ms: number;
    max_qubits_requested: number;
    declared_complexity_class: ComplexityClass;
    data_access_scope: DataAccessScope;
}
```

| Field | Notes |
|-------|-------|
| `requires_network` / `requires_filesystem` / `requires_gpu` | Capabilities you are requesting. Untrusted plugins that declare `true` are auto-quarantined on first execution. |
| `max_memory_mib` | Soft cap. Runtime monitoring detects `MemoryBombDetected`. |
| `max_execution_time_ms` | Hard cap. The sandbox raises `ExecutionTimeout` once exceeded. |
| `max_qubits_requested` | **Security cap, not an allocation.** Upper bound the plugin is permitted to consume; the bridge refuses runs that would exceed it. The engine still auto-selects the actual width internally — this field only sets the ceiling. Bounded by the bridge-wide `max_qubits_limit` (default 8192 strict, 65 536 permissive). |
| `declared_complexity_class` | Used by the circuit-bounds checker to pick limits. |
| `data_access_scope` | The plugin's contract about what data it reads. Cross-checked at the request layer. |

### `ComplexityClass`

```typescript
enum ComplexityClass {
    Linear,        // O(n)         — preferred for simple post-processing
    Quadratic,     // O(n²)        — typical for pairwise algorithms
    Polynomial,    // O(n^k)       — heuristic optimizers, ansatz searches
    Exponential,   // O(2^n)       — only with explicit Trusted approval
    Unknown,       // treated as Exponential by the circuit-bounds checker
}
```

### `DataAccessScope`

```typescript
enum DataAccessScope {
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

```typescript
// Security manifest example
security_manifest(): {
    requires_network: false,           // never set true unless absolutely required
    requires_filesystem: false,
    requires_gpu: false,
    max_memory_mib: 256,               // honest upper bound
    max_execution_time_ms: 5000,
    max_qubits_requested: 4096,
    declared_complexity_class: Polynomial,
    data_access_scope: ReadOwnInput,
}
```

Over-declaring is treated as a security smell; under-declaring causes runtime kills.

### 3. Compute the integrity hash

`integrity_hash()` must be deterministic and tied to *both* the source and the manifest. The reference pattern uses SHA-512:

```typescript
// Integrity hash computation (pseudocode)
integrity_hash():
    hasher = SHA512.new()
    hasher.update(self.name())
    hasher.update(self.version())
    hasher.update(CARGO_PKG_VERSION)
    hasher.update(source_file_bytes)        // source binding
    manifest = self.security_manifest()
    hasher.update(format(
        "{}|{}|{}|{}|{}|{}|{:?}|{:?}",
        manifest.requires_network, manifest.requires_filesystem, manifest.requires_gpu,
        manifest.max_memory_mib, manifest.max_execution_time_ms, manifest.max_qubits_requested,
        manifest.declared_complexity_class, manifest.data_access_scope,
    ))
    return hex(hasher.finalize())
```

The system stores this hash at registration time and verifies it on **every** call. Any tampering — including changing the manifest after registration — produces `PluginIntegrityMismatch`.

### 4. Register with the bridge

```typescript
// Registration
bridge = ExtensionPluginSecurity.new()      // strict (default)
// or ExtensionPluginSecurity.new_permissive() for development
registered_name = bridge.register_plugin(MyPlugin)
```

`register_plugin` runs security validation (signature, integrity, name validation) before inserting into the registry. Newly registered plugins start at `TrustLevel::Untrusted`.

### 5. Execute

```typescript
// Execution
request = PluginAlgorithmRequest { /* … */ }
result = bridge.execute_plugin(registered_name, request)
```

This single call walks the full security validation pipeline. The success path returns the plugin's `PluginAlgorithmResult`; the failure path returns a string whose body matches the corresponding `SecurityViolation::Display` output.

---

## Complete Example — Custom Variational Eigensolver Plugin

A custom UCCSD-flavoured eigensolver that maps `parameters["theta"]` and `input_data` onto VQE circuit angles, runs an inner classical optimizer, and reports the converged ground-state energy.

**Algorithm description:**

1. Convert raw amplitudes to VQE rotation angles: `angle = 2 * atan2(sqrt(|amplitude|), 1.0)` for each amplitude
2. Optionally override angles from caller-provided `parameters["theta"]` array
3. Run gradient-descent optimization loop (up to `max_iters` iterations):
   - For each angle, compute numerical gradient via central-difference with epsilon = 1e-3
   - Update angle via learning rate (default 0.01)
   - Track energy history; stop when convergence < 1e-9
4. Return ground-state energy, iteration count, energy history, and converged angles

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `custom-vqe` |
| version | `1.0.0` |
| supported_domains | `["chemistry", "materials_science"]` |
| max_memory_mib | 128 |
| max_execution_time_ms | 10,000 |
| max_qubits_requested | 16 |
| complexity_class | Polynomial |
| data_access_scope | ReadOwnInput |

**Input validation rules:**
- `input_data` must not be empty
- `input_data` must not exceed 65,536 amplitudes
- Amplitudes must be approximately normalized: 0.5 ≤ |ψ|² ≤ 1.5
- No NaN or Inf values allowed
- `num_qubits` is NOT validated (it's advisory; engine auto-selects from input_data)

**curl — execute the custom VQE plugin**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/custom-vqe/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "custom-vqe",
    "domain": "chemistry",
    "parameters": { "theta": [0.1, 0.2, 0.3] },
    "num_qubits": 0,
    "input_data": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "ground_state_energy": -0.8,
    "iterations": 42,
    "energy_history": [-0.5, -0.6, -0.7, -0.75, -0.8],
    "converged_angles": [0.05, 0.12, 0.08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  },
  "execution_time_ms": 124.7,
  "plugin_name": "custom-vqe",
  "plugin_version": "1.0.0"
}
```

---

## Complete Example — Custom Optimization Algorithm Plugin (Finance + Logistics)

A QAOA-style portfolio/route optimizer that supports two domains. Demonstrates multi-domain registration, parameter validation, and a richer security manifest.

**Algorithm description:**

1. Validate a square `cost_matrix` parameter (must be NxN with finite entries)
2. Limit input amplitudes to 16,384 entries
3. Execute a greedy + QAOA-style refinement: cycle through assignment rotations for `layers` iterations
4. Track best total cost across all assignment permutations
5. Return best cost, assignment, layer count, and domain

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `qaoa-dual-domain` |
| version | `0.4.1` |
| supported_domains | `["finance", "logistics"]` |
| max_memory_mib | 512 |
| max_execution_time_ms | 20,000 |
| max_qubits_requested | 4,096 |
| complexity_class | Quadratic |
| data_access_scope | ReadDomainData |

---

## Database & Storage Plugin Examples

The plugin system supports integration with **any database, data lake, data warehouse, or time-series database**. Below are complete, working examples for each major category.

> **How the integration works.** Plugins do **not** open network sockets to your database. Your application (or a sidecar extractor) pulls **statistics, schemas, workload patterns, or sampled signals** out of the database, encodes them as the `input_data` amplitude vector and `parameters` map in `PluginAlgorithmRequest`, and the plugin compiles that workload onto the VQE substrate. The plugin returns optimised query plans, partition selections, materialised-view recommendations, anomaly scores, etc. — never raw rows.
>
> Treat each example as a template: swap the toy scoring functions for whatever cost model your storage system actually exposes.

---

### Example 1 — SQL Database Plugin (PostgreSQL / MySQL / SQLite)

Quantum-optimised query planning for relational engines. The plugin receives table-level statistics (row counts, NDV, histogram buckets) as `input_data`, candidate plan structure in `parameters`, and returns a chosen plan + cost estimate.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `sql-query-optimizer` |
| version | `1.2.0` |
| supported_domains | `["machine_learning", "mathematics"]` |
| max_memory_mib | 64 |
| max_execution_time_ms | 3,000 |
| max_qubits_requested | 1,024 |
| complexity_class | Linear |
| data_access_scope | ReadOwnInput |

**Input validation rules:**
- `input_data` must contain table statistics (finite, non-negative values)
- `query` parameter required (SQL string, non-empty)
- `tables` parameter required (array of relations, 1–64 entries)
- `join_predicates` optional (array, max 256 entries)

**Algorithm:**
- Encodes table cardinality statistics as quantum amplitude vector
- Scores join order permutations using logarithmic cost accumulation
- Recommends indexes for tables exceeding 1M rows
- Returns optimized join order, estimated cost, recommended indexes, and plan strategy

**curl — execute the SQL optimiser**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/sql-query-optimizer/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "sql-query-optimizer",
    "domain": "machine_learning",
    "parameters": {
      "query": "SELECT u.id, o.total FROM users u JOIN orders o ON o.user_id = u.id WHERE o.created_at > NOW() - INTERVAL ''7 days''",
      "tables": ["users", "orders"],
      "join_predicates": [["users.id", "orders.user_id"]]
    },
    "num_qubits": 0,
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
  "plugin_name": "sql-query-optimizer",
  "plugin_version": "1.2.0"
}
```

---

### Example 2 — Data Lake Plugin (S3 / Azure Blob / HDFS / Delta Lake)

Quantum-enhanced partition pruning, file-layout optimisation, and probabilistic sampling across petabyte-scale object stores. The plugin operates on **metadata only** — partition manifests and column statistics — never on raw blobs.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `data-lake-optimizer` |
| version | `0.9.0` |
| supported_domains | `["logistics", "machine_learning"]` |
| max_memory_mib | 256 |
| max_execution_time_ms | 8,000 |
| max_qubits_requested | 4,096 |
| complexity_class | Linear |
| data_access_scope | ReadOwnInput |

**Input validation rules:**
- `bucket_path` must start with `s3://`, `abfs://`, `hdfs://`, or `delta://`
- `partition_keys` must be 1–16 strings
- `file_format` must be one of: parquet, orc, avro, json, csv, delta, iceberg
- Optional `sampling_rate` must be in [0, 1]
- Partition profile (`input_data`) must not exceed 1M entries

**Algorithm:**
- Normalizes partition selectivity scores to unit Euclidean norm
- Applies quantum-style amplitude pruning: keeps partitions whose |amplitude|² exceeds a threshold derived from `1/√(N) × 0.5`
- Recommends file layout based on format (z-order for parquet/delta/iceberg, bloom filters for ORC, rewrite for others)

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/data-lake-optimizer/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "data-lake-optimizer",
    "domain": "machine_learning",
    "parameters": {
      "bucket_path": "s3://corp-events-prod/year=2026/",
      "partition_keys": ["year", "month", "day"],
      "file_format": "parquet",
      "sampling_rate": 0.05
    },
    "num_qubits": 0,
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
  "plugin_name": "data-lake-optimizer",
  "plugin_version": "0.9.0"
}
```

---

### Example 3 — Data Warehouse Plugin (Snowflake / BigQuery / Redshift)

Materialised-view selection, workload scheduling, and cardinality estimation at warehouse scale. `input_data` carries workload-frequency distributions; `parameters` carries warehouse config and table schemas.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `data-warehouse-optimizer` |
| version | `1.0.3` |
| supported_domains | `["finance", "machine_learning", "mathematics"]` |
| max_memory_mib | 384 |
| max_execution_time_ms | 15,000 |
| max_qubits_requested | 2,048 |
| complexity_class | Quadratic |
| data_access_scope | ReadOwnInput |

**Input validation rules:**
- `warehouse` parameter must be an object with `{vendor, size, region}`
- `workload_patterns` must be 1–1024 entries
- `schemas` must be array (≤256 tables)
- `input_data` must hold workload frequency distribution (positive finite sum)

**Algorithm:**
- Picks top-k workloads as materialised-view candidates using quantum-style probability mass (frequency/total), where k = √(workload_count)
- Generates a schedule packing plan assigning time slots proportional to frequency
- Estimates cost reduction percentage based on MV coverage ratio

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/data-warehouse-optimizer/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "data-warehouse-optimizer",
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
    "num_qubits": 0,
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
  "plugin_name": "data-warehouse-optimizer",
  "plugin_version": "1.0.3"
}
```

---

### Example 4 — Time-Series Database Plugin (InfluxDB / TimescaleDB / QuestDB)

Anomaly detection, predictive trends, and optimal downsampling for sensor and metric streams. `input_data` is the time-series amplitude vector itself.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `timeseries-analytics` |
| version | `2.1.0` |
| supported_domains | `["physics", "real_time", "machine_learning"]` |
| max_memory_mib | 128 |
| max_execution_time_ms | 5,000 |
| max_qubits_requested | 2,048 |
| complexity_class | Linear |
| data_access_scope | ReadOwnInput |

**Input validation rules:**
- `metric` parameter required (non-empty string, ≤256 chars)
- `time_range` must be `{ start, end }` with RFC-3339 strings
- `resolution` must be one of: 1s, 10s, 1m, 5m, 1h, 1d
- `aggregation` must be one of: mean, sum, min, max, p95, p99, count
- Need at least 8 samples for spectral analysis
- No NaN or Inf values

**Algorithm:**
- Computes mean and standard deviation of the time series
- Detects anomalies via robust z-score (threshold: |z| ≥ 3.0)
- Calculates trend via simple linear regression slope
- Determines optimal downsampling ratio from signal-to-noise heuristic: `ratio = round(clamp(log₂(SNR), 1, 10))`

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/timeseries-analytics/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "timeseries-analytics",
    "domain": "real_time",
    "parameters": {
      "metric": "cpu.utilisation.percent",
      "time_range": { "start": "2026-05-19T00:00:00Z", "end": "2026-05-19T01:00:00Z" },
      "resolution": "10s",
      "aggregation": "mean"
    },
    "num_qubits": 0,
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
  "plugin_name": "timeseries-analytics",
  "plugin_version": "2.1.0"
}
```

---

### Example 5 — Graph Database Plugin (Neo4j / Neptune / JanusGraph)

Optimal path finding, community detection, and partitioning over knowledge graphs. `input_data` is a flattened adjacency-amplitude vector; `parameters` carries the query and traversal options.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `graph-database-optimizer` |
| version | `0.7.2` |
| supported_domains | `["mathematics", "logistics", "machine_learning"]` |
| max_memory_mib | 512 |
| max_execution_time_ms | 20,000 |
| max_qubits_requested | 4,096 |
| complexity_class | Polynomial |
| data_access_scope | ReadOwnInput |

**Input validation rules:**
- `graph_query` parameter required (non-empty, max 4096 chars)
- `traversal_depth` required (1–12)
- Optional `node_filters` array (max 64 entries)
- `input_data` must be a flattened square adjacency matrix (length = N×N, N ≤ 1024)

**Algorithm:**
- Performs amplitude walk over the adjacency matrix for `depth` steps (surrogate for Grover-style scan on VQE substrate)
- At each step: multiply visit vector by adjacency, normalize to unit norm
- Ranks nodes by final amplitude magnitude
- Identifies top-k community seeds (k = √N)
- Constructs illustrative shortest path from node 0 to highest-amplitude node

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/graph-database-optimizer/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "graph-database-optimizer",
    "domain": "logistics",
    "parameters": {
      "graph_query": "MATCH (a:Warehouse)-[:SHIPS_TO*1..4]->(b:Customer) RETURN b",
      "traversal_depth": 4,
      "node_filters": [{ "label": "Warehouse" }, { "label": "Customer" }]
    },
    "num_qubits": 0,
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
  "plugin_name": "graph-database-optimizer",
  "plugin_version": "0.7.2"
}
```

---

### Example 6 — Universal Database Connector Plugin (BYO-DB)

A generic template that handles **any** storage system by branching on a `db_type` parameter. Use this when you need a single registered plugin to optimise across heterogeneous backends.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `universal-db-connector` |
| version | `0.5.0` |
| supported_domains | All 16 domains |
| max_memory_mib | 256 |
| max_execution_time_ms | 10,000 |
| max_qubits_requested | 2,048 |
| complexity_class | Polynomial |
| data_access_scope | ReadOwnInput |

**Input validation rules:**
- `db_type` must be one of: relational, document, kv, columnar, vector, graph, timeseries, datalake, warehouse
- `operation` must be one of: plan, index, partition, compress, search, scan, aggregate
- `config` must be an object describing connection metadata
- `input_data` must hold the statistical profile (finite values, non-empty)

**Algorithm — dispatch logic by (db_type, operation):**

| db_type | operation | Recommendation |
|---------|-----------|----------------|
| relational | plan | `{ join_root: dominant_index, amplitude_mass }` |
| document | index | `{ shard_key_idx: dominant_index, fanout: N }` |
| kv | partition | `{ partition_id: dominant_index, rebalance: mass > 0.9 }` |
| columnar | compress | `{ encoding: "rle_dict", ratio_hint: mass }` |
| vector | search | `{ centroid: dominant_index, radius: 1/mass }` |
| (other) | (other) | `{ op: "noop", amplitude_mass: mass }` |

Where `dominant_index` = index of maximum-amplitude entry, `mass` = Euclidean norm of `input_data`.

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/universal-db-connector/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "universal-db-connector",
    "domain": "machine_learning",
    "parameters": {
      "db_type": "vector",
      "operation": "search",
      "config": { "endpoint": "https://vec.internal", "collection": "embeddings_v3" }
    },
    "num_qubits": 0,
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
  "plugin_name": "universal-db-connector",
  "plugin_version": "0.5.0"
}
```

---

### Example 7 — Kafka Streaming Pipeline Plugin

Optimises Kafka topic partition layout, consumer-group rebalancing, and end-to-end throughput by encoding broker-side statistics as a quantum amplitude vector.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `kafka-streaming-optimizer` |
| version | `1.0.0` |
| supported_domains | `["real_time", "logistics", "machine_learning"]` |
| max_memory_mib | 512 |
| max_execution_time_ms | 30,000 |
| max_qubits_requested | 4,096 |
| complexity_class | Linear |
| data_access_scope | ReadOwnInput |
| requires_network | true |

**Required parameters:** `topic_count`, `partition_count`, `consumer_count`, `message_rate_per_sec`, `retention_hours`

**Input validation rules:**
- All required parameters must be present
- `input_data` must contain broker telemetry samples (1–65,536 entries)

**Algorithm:**
- Born-normalizes broker telemetry and computes Shannon entropy
- Calculates load balance score: `entropy / ln(partition_count)` clamped to [0, 1]
- Determines optimal partitions: `max(consumer_count, ceil(message_rate / 50,000))` capped at 4× current
- Assigns partitions to consumers round-robin
- Estimates throughput and rebalance latency

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/kafka-streaming-optimizer/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "kafka-streaming-optimizer",
    "domain": "real_time",
    "parameters": {
      "brokers": ["broker-1:9092", "broker-2:9092", "broker-3:9092"],
      "topic": "events.orders",
      "topic_count": 24,
      "partition_count": 48,
      "replication_factor": 3,
      "min_isr": 2,
      "consumer_group": "orders-processor",
      "consumer_count": 12,
      "message_rate_per_sec": 1200000,
      "retention_hours": 168,
      "compression": "zstd"
    },
    "num_qubits": 0,
    "input_data": [0.42, 0.31, 0.55, 0.19, 0.27, 0.38, 0.61, 0.22, 0.17, 0.44, 0.29, 0.36]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "optimal_partitions": 48,
    "consumer_assignment": [
      [0, 12, 24, 36],
      [1, 13, 25, 37],
      [2, 14, 26, 38],
      [3, 15, 27, 39],
      [4, 16, 28, 40],
      [5, 17, 29, 41],
      [6, 18, 30, 42],
      [7, 19, 31, 43],
      [8, 20, 32, 44],
      [9, 21, 33, 45],
      [10, 22, 34, 46],
      [11, 23, 35, 47]
    ],
    "predicted_throughput_mb_s": 1146.3,
    "rebalance_latency_ms": 140,
    "topic_count": 24,
    "retention_hours": 168,
    "load_balance_score": 0.97
  },
  "execution_time_ms": 4.21,
  "plugin_name": "kafka-streaming-optimizer",
  "plugin_version": "1.0.0"
}
```

---

### Example 8 — Apache Pulsar Streaming Plugin

Optimises Pulsar topic-subscription layout, tiered storage offload, and geo-replication routing across regions.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `pulsar-streaming-plugin` |
| version | `1.0.0` |
| supported_domains | `["real_time", "finance", "logistics"]` |
| max_memory_mib | 512 |
| max_execution_time_ms | 30,000 |
| max_qubits_requested | 2,048 |
| complexity_class | Linear |
| data_access_scope | ReadOwnInput |
| requires_network | true |

**Required parameters:** `namespace`, `tenant`, `subscription_count`, `geo_regions`, `tiered_storage_threshold_gb`

**Algorithm:**
- Computes average signal strength from `input_data`
- Determines optimal subscription count: `subscription_count × min(1 + avg_signal, 2)`
- Builds geo-routing plan with per-region weights from input amplitudes
- Generates tiered storage recommendations (hot/warm/cold with configurable offload thresholds)

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/pulsar-streaming-plugin/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "pulsar-streaming-plugin",
    "domain": "finance",
    "parameters": {
      "tenant": "trading",
      "namespace": "trading/equities",
      "topic": "persistent://trading/equities/orderbook",
      "subscription_count": 16,
      "subscription_type": "Shared",
      "geo_regions": ["us-east", "eu-west", "ap-southeast"],
      "tiered_storage_threshold_gb": 200.0,
      "backlog_quota_gb": 1000.0
    },
    "num_qubits": 0,
    "input_data": [0.71, 0.42, 0.18, 0.55, 0.27, 0.36]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "optimal_subscriptions": 22,
    "geo_routing_plan": {
      "us-east": { "weight": 0.71, "primary": true, "replication_lag_ms_target": 250 },
      "eu-west": { "weight": 0.42, "primary": false, "replication_lag_ms_target": 250 },
      "ap-southeast": { "weight": 0.18, "primary": false, "replication_lag_ms_target": 250 }
    },
    "storage_tier_recommendations": {
      "hot_tier_gb": 200.0,
      "warm_tier_offload_after_hours": 6,
      "cold_tier_backend": "s3",
      "cold_tier_offload_after_hours": 72
    }
  },
  "execution_time_ms": 2.84,
  "plugin_name": "pulsar-streaming-plugin",
  "plugin_version": "1.0.0"
}
```

---

### Example 9 — Vector Database Plugin (Milvus / Pinecone / Weaviate / Qdrant / ChromaDB)

Optimises HNSW graph construction, IVF centroid placement, DiskANN partitioning, and similarity-search recall across the major vector backends.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `vector-db-optimizer` |
| version | `1.0.0` |
| supported_domains | `["machine_learning", "mathematics", "biology"]` |
| max_memory_mib | 1,024 |
| max_execution_time_ms | 60,000 |
| max_qubits_requested | 16,384 |
| complexity_class | Polynomial |
| data_access_scope | ReadOwnInput |

**Required parameters:** `vector_dimension` (1–65,536), `collection_size`, `index_type` (HNSW/IVF_FLAT/IVF_SQ8/DiskANN), `metric_type` (L2/IP/COSINE)

**Algorithm:**
- HNSW tuning: `ef_construction = clamp(round(log₂(N) × 16), 64, 512)`, `M = clamp(round(log₂(N) / 2), 8, 64)`
- IVF tuning: `nlist ≈ √N × (1 + entropy)`, `nprobe = √nlist`
- Recall@k estimates by index type: HNSW=0.985, IVF_FLAT=0.97, IVF_SQ8=0.94, DiskANN=0.96
- QPS estimates scaled by `dimension/768` ratio
- Memory footprint: `bytes_per_vec × collection_size` (IVF_SQ8=1B/dim, DiskANN=2B/dim, others=4B/dim)
- Partition strategy: `shards = max(1, ceil(N/5M))`, replicas=2

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/vector-db-optimizer/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "vector-db-optimizer",
    "domain": "machine_learning",
    "parameters": {
      "backend": "milvus",
      "collection": "doc_embeddings_v4",
      "vector_dimension": 1536,
      "collection_size": 50000000,
      "index_type": "HNSW",
      "metric_type": "COSINE",
      "top_k": 20,
      "ef_search": 128
    },
    "num_qubits": 0,
    "input_data": [0.18, 0.42, 0.71, 0.09, 0.05, 0.33, 0.27, 0.61]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "backend": "milvus",
    "index_type": "HNSW",
    "metric_type": "COSINE",
    "optimal_ef_construction": 412,
    "optimal_m": 13,
    "optimal_nlist": 9341,
    "optimal_nprobe": 97,
    "recall_at_k": 0.985,
    "top_k": 20,
    "qps_estimate": 17677,
    "memory_usage_gb": 286.1,
    "partition_strategy": {
      "shards": 10,
      "replicas": 2,
      "partition_key": "tenant_id"
    }
  },
  "execution_time_ms": 6.74,
  "plugin_name": "vector-db-optimizer",
  "plugin_version": "1.0.0"
}
```

---

### Example 10 — Redis Streams + Pub/Sub Plugin

Optimises Redis Streams consumer-group assignment, pub/sub channel partitioning, and memory layout under a configurable eviction policy.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `redis-streams-plugin` |
| version | `1.0.0` |
| supported_domains | `["real_time", "finance"]` |
| max_memory_mib | 256 |
| max_execution_time_ms | 15,000 |
| max_qubits_requested | 1,024 |
| complexity_class | Linear |
| data_access_scope | ReadOwnInput |
| requires_network | true |

**Required parameters:** `stream_count`, `consumer_groups`, `max_memory_gb`, `eviction_policy`
- `eviction_policy` must be one of: noeviction, allkeys-lru, allkeys-lfu, volatile-lru, volatile-lfu, volatile-ttl

**Algorithm:**
- Computes signal strength from absolute values of input amplitudes
- Assigns streams to consumer groups round-robin
- Generates memory recommendations (maxmemory, policy, trim strategy, lazyfree, io_threads)
- Estimates throughput: `10M × (1 + signal_strength) × √(consumer_groups)` ops/sec

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/redis-streams-plugin/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "redis-streams-plugin",
    "domain": "real_time",
    "parameters": {
      "stream_count": 16,
      "consumer_groups": 6,
      "max_memory_gb": 64.0,
      "eviction_policy": "allkeys-lfu",
      "pubsub_channels": 32
    },
    "num_qubits": 0,
    "input_data": [0.55, 0.27, 0.31, 0.42, 0.18, 0.36]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "optimal_consumer_assignment": {
      "group-0": [0, 6, 12],
      "group-1": [1, 7, 13],
      "group-2": [2, 8, 14],
      "group-3": [3, 9, 15],
      "group-4": [4, 10],
      "group-5": [5, 11]
    },
    "memory_recommendations": {
      "maxmemory_gb": 64.0,
      "maxmemory_policy": "allkeys-lfu",
      "stream_trim_strategy": "MAXLEN ~ 1000000",
      "lazyfree_lazy_eviction": true,
      "io_threads": 8
    },
    "throughput_estimate_ops_s": 33665282
  },
  "execution_time_ms": 1.92,
  "plugin_name": "redis-streams-plugin",
  "plugin_version": "1.0.0"
}
```

---

### Example 11 — Apache Flink Streaming Analytics Plugin

Optimises Flink job DAGs, checkpoint cadence, watermark strategy, and state-backend layout for sub-second p99 latencies.

**Plugin configuration:**

| Property | Value |
|----------|-------|
| name | `flink-streaming-plugin` |
| version | `1.0.0` |
| supported_domains | `["real_time", "machine_learning", "finance"]` |
| max_memory_mib | 768 |
| max_execution_time_ms | 30,000 |
| max_qubits_requested | 4,096 |
| complexity_class | Linear |
| data_access_scope | ReadOwnInput |
| requires_network | true |

**Required parameters:** `job_parallelism`, `checkpoint_interval_ms`, `state_backend` (rocksdb/heap), `watermark_strategy`

**Algorithm:**
- Computes signal variance from `input_data`
- Optimal parallelism: `parallelism × min(1 + √(variance), 2)`
- Checkpoint interval recommendation: if variance > 0.25, cap at 15s; otherwise floor at 30s
- Checkpoint mode: EXACTLY_ONCE with incremental for rocksdb, unaligned if variance > 0.4
- State size estimate: `parallelism × (1 + variance) × 0.75` GB
- Latency p99: heap = `15 + variance × 30` ms, rocksdb = `45 + variance × 80` ms

**curl**

```powershell
curl -X POST http://localhost:8080/api/v1/plugins/flink-streaming-plugin/execute `
  -H "Content-Type: application/json" `
  -d '{
    "algorithm_name": "flink-streaming-plugin",
    "domain": "real_time",
    "parameters": {
      "job_name": "fraud-scoring",
      "job_parallelism": 32,
      "checkpoint_interval_ms": 60000,
      "state_backend": "rocksdb",
      "watermark_strategy": "bounded_out_of_orderness",
      "max_out_of_orderness_ms": 2000,
      "savepoint_dir": "s3://flink/savepoints"
    },
    "num_qubits": 0,
    "input_data": [0.31, 0.55, 0.18, 0.42, 0.27, 0.61, 0.09, 0.36]
  }'
```

**Expected response**

```json
{
  "success": true,
  "output_data": {
    "optimal_parallelism": 38,
    "checkpoint_recommendations": {
      "interval_ms": 60000,
      "mode": "EXACTLY_ONCE",
      "min_pause_between_checkpoints_ms": 5000,
      "incremental": true,
      "unaligned": false
    },
    "state_size_estimate_gb": 31,
    "latency_p99_ms": 50,
    "state_backend": "rocksdb",
    "watermark_strategy": "bounded_out_of_orderness"
  },
  "execution_time_ms": 3.12,
  "plugin_name": "flink-streaming-plugin",
  "plugin_version": "1.0.0"
}
```

---

## Streaming Architecture Integration

The plugins above expose a unified surface for the major streaming systems. Each one ingests pre-extracted broker / job telemetry, compiles it onto the VQE substrate, and returns deployment-ready tuning recommendations.

| Plugin | Streaming System | Key Use Case | Throughput |
|--------|------------------|--------------|------------|
| `kafka-streaming-optimizer` | Apache Kafka | Partition optimization | 1M+ msg/sec |
| `pulsar-streaming-plugin` | Apache Pulsar | Geo-replication routing | 500K+ msg/sec |
| `redis-streams-plugin` | Redis Streams | Real-time pub/sub | 10M+ ops/sec |
| `flink-streaming-plugin` | Apache Flink | DAG optimization | Continuous |

**Integration pattern.** Run each plugin as part of a control-plane sidecar that periodically samples broker / job metrics, invokes the plugin via `/api/v1/plugins/<name>/execute`, and feeds the returned recommendations back into the cluster (Kafka admin API, Pulsar admin REST, Redis `CONFIG SET`, Flink REST). All four plugins are stateless from the engine's perspective — re-runs are safe and deterministic for the same `(input_data, parameters)`.

---

## Vector Database Integration

A single plugin covers the dominant vector backends, exposing a uniform tuning surface for HNSW, IVF, and DiskANN families.

| Plugin | Supported Backends | Index Types | Max Dimensions |
|--------|--------------------|-------------|----------------|
| `vector-db-optimizer` | Milvus, Pinecone, Weaviate, Qdrant, ChromaDB | HNSW, IVF_FLAT, IVF_SQ8, DiskANN | 65536 |

**Integration pattern.** Pass the collection's vector dimension, size, target index, metric, and a small sample of representative embedding statistics as `input_data`. The plugin returns `optimal_ef_construction`, `optimal_m`, `optimal_nlist`, `optimal_nprobe`, `recall_at_k`, `qps_estimate`, `memory_usage_gb`, and a `partition_strategy` block that maps directly onto each backend's create-index / create-collection APIs.

---

### Operational notes for storage plugins

- **Plugins receive pre-extracted data.** Your application is responsible for pulling stats/metadata out of the database; the plugin never opens a socket. This is why every example above declares `requires_network: false` and `requires_filesystem: false`.
- **Encode statistics as amplitudes.** Normalise your numeric profile to a unit-norm vector before passing it as `input_data` — the VQE substrate treats the vector as quantum amplitudes.
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
  "name": "custom-vqe",
  "version": "1.0.0",
  "signature_hex": "9f37c0…ab12",
  "integrity_hash": "ec1d8b9b…3f0a"
}
```

**Response — 201 Created**
```json
{
  "registered": true,
  "name": "custom-vqe",
  "trust_level": "Untrusted"
}
```

**curl**
```powershell
curl -X POST http://localhost:8080/api/v1/plugins/register `
  -H "Authorization: Bearer $ADMIN_TOKEN" `
  -H "Content-Type: application/json" `
  -d '{ "name":"custom-vqe","version":"1.0.0","signature_hex":"9f37c0ab12","integrity_hash":"ec1d8b9b3f0a" }'
```

Status codes: `201` registered · `400` invalid manifest · `401` unauthenticated · `403` not admin · `409` already registered.

### `GET /api/v1/plugins/list`

**Response — 200**
```json
{
  "plugins": [
    {
      "name": "custom-vqe",
      "version": "1.0.0",
      "author": "Quantum Plugin Authors",
      "description": "Custom VQE variant compiling onto the universal VQE substrate.",
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
{ "unregistered": true, "name": "custom-vqe" }
```

Status codes: `200` removed · `404` unknown plugin · `403` not admin.

```powershell
curl -X DELETE http://localhost:8080/api/v1/plugins/custom-vqe `
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### `POST /api/v1/plugins/{name}/execute`

**Request**
```json
{
  "algorithm_name": "custom-vqe",
  "domain": "chemistry",
  "parameters": { "theta": [0.1, 0.2, 0.3] },
  "num_qubits": 0,
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
  "plugin_name": "custom-vqe",
  "plugin_version": "1.0.0"
}
```

**Response — 429 Rate Limited**
```json
{
  "error": "PluginBlocked",
  "violation": "rate limit exceeded for 'custom-vqe': 11 requests in window"
}
```

**curl**
```powershell
curl -X POST http://localhost:8080/api/v1/plugins/custom-vqe/execute `
  -H "Content-Type: application/json" `
  -d '{ "algorithm_name":"custom-vqe","domain":"chemistry","parameters":{},"num_qubits":0,"input_data":[1.0,0.0,0.0,0.0] }'
```

Status codes: `200` ok · `400` validation failed · `403` plugin quarantined · `408` timeout · `429` rate limited · `503` global threat-level lockdown.

### `GET /api/v1/plugins/{name}/metadata`

**Response — 200**
```json
{
  "name": "custom-vqe",
  "version": "1.0.0",
  "author": "Quantum Plugin Authors",
  "description": "Custom VQE variant compiling onto the universal VQE substrate.",
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
      "plugin_name": "custom-vqe",
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
{ "previous": "Untrusted", "current": "Verified", "name": "custom-vqe" }
```

---

## Security Model

### Trust Levels

`TrustLevel` controls every quota a plugin sees.

| Level | How obtained | Rate limit | Hard timeout | Max input amplitudes | Notes |
|-------|--------------|------------|--------------|----------------------|-------|
| `Untrusted` | Default after registration | 10 / min | 5 s | 100 000 | Full sandbox; capability requests cause auto-quarantine |
| `Verified` | Valid signature accepted by signature verification | 50 / min | 15 s | 500 000 | Capability requests allowed but watched |
| `Trusted` | Admin promotion via `/trust` endpoint | 200 / min | 30 s | 1 000 000 | May declare `ReadAll`, `Exponential` |
| `BuiltIn` | Compiled-in plugins only | unbounded | 600 s | 65 536 amps | Bypasses runtime signature check, never quarantined |

The exact rate-limit numerator is enforced by the bridge's internal rate limiter.

### Security Pipeline

All plugin executions pass through a comprehensive multi-layer security validation pipeline before reaching the VQE substrate. This includes:

- Input validation and sanitization
- Rate limiting per trust level
- Execution sandboxing with hard timeouts
- Continuous behavioral monitoring (execution profiles are recorded *before* anomaly checking to ensure the baseline is always current when detection runs)
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

Every failure path surfaces a `SecurityViolation`. The HTTP layer maps these to JSON `error.violation` strings.

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
| `CircuitExpansionExplosion { count, max }` | Inner expansion exceeds the circuit-bounds checker's limit | Reduce circuit depth or upgrade complexity class |

### Debugging "Plugin Blocked" errors

1. Pull the most recent violation entries: `GET /api/v1/plugins/security/audit`.
2. Match the `violation` string to the table above.
3. Confirm your manifest matches what the registry stored: `GET /api/v1/plugins/{name}/metadata`.
4. Re-register if the integrity hash drifted.

### Rate-limit handling

Treat `429 RateLimitExceeded` as advisory. The recommended client behaviour is exponential backoff with jitter, capped at `max_execution_time_ms` of your manifest.

### Threat-level escalation

The system automatically escalates the global `ThreatLevel` when violations accumulate. At `Lockdown`, **all non-`BuiltIn` execute calls** return `503`. Operators can de-escalate explicitly via `POST /api/v1/plugins/security/threat-level` with `{"level":"Normal"}` after triage.

**Threat Level Escalation Rules:**

| Transition | Trigger |
|------------|---------|
| Normal → Elevated | 5+ violations in 1 hour |
| Elevated → High | 15+ violations in 1 hour |
| High → Critical | 30+ violations in 1 hour |
| Critical → Lockdown | Manual trigger or 60+ violations in 1 hour |

Violations expire after 1 hour of inactivity. All escalations are logged in the forensic audit trail.

> **Buffer limits:** Both the main audit entries buffer and the violation entries buffer are capped at 100,000 entries with FIFO eviction — oldest entries are discarded first when the cap is reached.

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
No — and you don't need to. The bridge already forwards `input_data` and `num_qubits` to the VQE universal substrate. Your job is to compile algorithm parameters; execution stays on the substrate.

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

## Input Method

### API Endpoint
```
POST http://localhost:8080/api/v1/quantum/execute
```

### Request Format
```json
{
  "problem": "custom_algorithm",
  "config": {
    "num_qubits": 65536,
    "optimizer": "SPSA",
    "max_iterations": 100
  },
  "input_data": [0.001, -0.003, 0.002, "...Born-normalized floats..."]
}
```

### Supported Problem Types
- `"custom_algorithm"` — User-defined quantum algorithm via the plugin interface

### Data Input Options
- **Direct API**: Send JSON payload with amplitudes (Born-normalized floats)
- **File Import**: Upload binary/CSV data files via the import endpoint
- **Streaming**: For large datasets, use chunked streaming mode

---

## Hamiltonian Selection

### Available Hamiltonians
| Hamiltonian Type | Description | Use Case |
|---|---|---|
| User-Defined Custom | Plugin-provided Hamiltonian specification | Novel algorithms, research |
| Domain-Inherited | Hamiltonian from any supported domain | Cross-domain plugins |
| Parameterized | Custom parameterized operator | Variational algorithms |

### Configuration
```json
{
  "hamiltonian": {
    "type": "custom",
    "parameters": {
      "plugin_name": "my_algorithm",
      "version": "1.0.0",
      "custom_params": {}
    }
  }
}
```

### Encoding Options
- **Jordan-Wigner**: Fermion-to-qubit mapping (available to plugins)
- **Bravyi-Kitaev**: Reduced gate depth for large systems
- **Direct Encoding**: For custom operator specifications

---

## Supported Scale

| Parameter | Maximum Value |
|---|---|
| **Qubits** | 2^53 (9,007,199,254,740,992) |
| **Tensor Dimension** | 2^53 |
| **Precision** | IEEE 754 double (64-bit float) |

The quantum engine supports computations from small-scale (8 qubits) up to the theoretical maximum of 2^53 qubits with matching tensor dimension, enabling simulation of molecular systems from simple hydrogen molecules to complex biological macromolecules and beyond.
