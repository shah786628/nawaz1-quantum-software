# Quantum Multidimensional Package

## Overview

The Multidimensional Package provides quantum-accelerated multidimensional array tables and schema-driven data organization. It enables storing, querying, and processing N-dimensional data structures (tensors, time series, geospatial grids, multi-attribute datasets) with quantum-level performance.

**API Endpoint:** `POST http://localhost:8080/api/v1/multidimensional/create`

**Query Endpoint:** `POST http://localhost:8080/api/v1/multidimensional/query`

---

## Key Features

- **N-dimensional array tables** — Store data as multidim tensors (1D, 2D, 3D, ..., ND)
- **Schema-driven** — Define column types, dimensions, indexing strategies upfront
- **Range queries** — Query subregions of multidim arrays with O(log N) complexity
- **Quantum-accelerated indexing** — Mixed-radix indexing for fast lookups
- **Streaming pipeline** — Process large datasets in chunks
- **Type safety** — Strong typing for each dimension (INT, FLOAT, TEXT, BLOB, AMPLITUDE, COMPLEX)

---

## The 6 Sub-Modules

| # | Sub-Module | Source | Key Domain |
|---|-----------|--------|------------|
| 1 | Schema Designer | `schema_designer.rs` | Schema Definition |
| 2 | Array Storage | `array_storage.rs` | Storage Backend |
| 3 | Range Query | `range_query.rs` | Query Engine |
| 4 | Mixed Radix Index | `mixed_radix_index.rs` | Quantum Indexing |
| 5 | Streaming Pipeline | `streaming_pipeline.rs` | Stream Processing |
| 6 | Schema Registry | `schema_registry.rs` | Schema Management |

---

## 1. Schema Designer

**Source:** `schema_designer.rs`

Define table schemas with N-dimensional columns, type specifications, and indexing hints.

**Key Capabilities:**
- Declarative schema definition with dimension and measure separation
- Type inference and validation for all supported data types
- Indexing strategy selection (mixed_radix, btree, hash)
- Chunk size optimization hints for storage layout
- Resolution and range constraints per dimension
- Nested schema composition for complex data models

**When to Use:** Initial table creation, schema migration planning, data modeling for new domains.

---

## 2. Array Storage

**Source:** `array_storage.rs`

Multidimensional array storage backend with chunked compression for efficient disk/memory utilization.

**Key Capabilities:**
- Chunked N-dimensional array storage with configurable chunk sizes
- Zstd compression with 5-50x typical reduction ratios
- Copy-on-write semantics for concurrent reads
- Memory-mapped I/O for large arrays
- Automatic chunk boundary alignment
- Garbage collection for deleted/overwritten chunks

**When to Use:** Storing large multidimensional datasets, time series archival, scientific simulation output.

---

## 3. Range Query

**Source:** `range_query.rs`

Range query engine for slicing N-dimensional arrays with O(log N) complexity.

**Key Capabilities:**
- Hyper-rectangular range selection across any subset of dimensions
- Predicate pushdown into storage layer
- Lazy evaluation with streaming result sets
- Multi-range union and intersection queries
- Projection (select subset of measures)
- Aggregation over ranges (sum, mean, min, max, count)

**When to Use:** Subsetting geospatial data, time-window queries, extracting simulation subdomains.

---

## 4. Mixed Radix Index

**Source:** `mixed_radix_index.rs`

Quantum-optimized indexing using mixed-radix number systems for fast point and range lookups.

**Key Capabilities:**
- Mixed-radix encoding of N-dimensional coordinates into 1D keys
- O(log N) point lookups and range scans
- Space-filling curve ordering (Hilbert, Z-order) for locality
- Quantum amplitude-based search acceleration
- Adaptive radix selection based on dimension cardinality
- Zero external dependencies (pure CPU path)

**When to Use:** High-throughput point queries, spatial proximity searches, quantum-accelerated lookups.

---

## 5. Streaming Pipeline

**Source:** `streaming_pipeline.rs`

Stream processing for large multidimensional datasets that exceed available memory.

**Key Capabilities:**
- Chunk-at-a-time processing with configurable buffer sizes
- Backpressure-aware ingestion from external sources
- Transform pipelines (map, filter, aggregate) on streaming chunks
- Fault-tolerant checkpointing for long-running ingestion
- Parallel chunk processing across multiple cores
- Integration with quantum pipeline (L1→L2→L3) for amplitude encoding

**When to Use:** Bulk data ingestion, ETL pipelines, real-time sensor data, continuous data feeds.

---

## 6. Schema Registry

**Source:** `schema_registry.rs`

Reusable schema definitions with versioning, migration support, and cross-table consistency.

**Key Capabilities:**
- Named schema storage and retrieval
- Schema versioning with backward compatibility checks
- Migration generation (add/remove/rename dimensions and measures)
- Cross-table foreign key relationships
- Schema inheritance and composition
- Export/import schemas as JSON for sharing

**When to Use:** Multi-table data models, schema evolution over time, team collaboration on data formats.

---

## How to Create a Schema

### Step-by-Step Guide

```python
import requests

# Step 1: Define your schema
schema = {
    "table_name": "climate_grid_2026",
    "dimensions": [
        {"name": "latitude", "type": "FLOAT", "range": [-90, 90], "resolution": 0.1},
        {"name": "longitude", "type": "FLOAT", "range": [-180, 180], "resolution": 0.1},
        {"name": "altitude", "type": "FLOAT", "range": [0, 50000], "resolution": 100},
        {"name": "time", "type": "TIMESTAMP", "resolution": "1h"}
    ],
    "measures": [
        {"name": "temperature", "type": "FLOAT", "unit": "celsius"},
        {"name": "pressure", "type": "FLOAT", "unit": "hPa"},
        {"name": "humidity", "type": "FLOAT", "unit": "percent"},
        {"name": "amplitude", "type": "AMPLITUDE", "qubits": 65536}
    ],
    "indexing": "mixed_radix",
    "compression": "chunked_zstd",
    "chunk_size": [180, 360, 50, 24]
}

# Step 2: Create the table
resp = requests.post("http://localhost:8080/api/v1/multidimensional/create", 
                     json=schema)
table_id = resp.json()["table_id"]

# Step 3: Insert N-dimensional data
data = {
    "table_id": table_id,
    "rows": [
        {"latitude": 12.5, "longitude": 77.6, "altitude": 920, 
         "time": "2026-05-18T12:00:00Z", "temperature": 28.5, 
         "pressure": 912.3, "humidity": 65.2}
    ]
}
requests.post("http://localhost:8080/api/v1/multidimensional/insert", json=data)

# Step 4: Range query
query = {
    "table_id": table_id,
    "ranges": {
        "latitude": [10, 15],
        "longitude": [75, 80], 
        "time": ["2026-05-18T00:00:00Z", "2026-05-18T23:59:59Z"]
    },
    "select": ["temperature", "pressure"]
}
results = requests.post("http://localhost:8080/api/v1/multidimensional/query", 
                        json=query).json()
```

### Schema Definition Fields

| Field | Required | Description |
|-------|----------|-------------|
| `table_name` | Yes | Unique table identifier |
| `dimensions` | Yes | Array of coordinate axis definitions |
| `measures` | Yes | Array of value columns stored at each coordinate |
| `indexing` | No | Index type: `mixed_radix` (default), `btree`, `hash` |
| `compression` | No | Compression: `chunked_zstd` (default), `lz4`, `none` |
| `chunk_size` | No | Array of chunk sizes per dimension |

### Dimension Definition

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Dimension name |
| `type` | Yes | Data type (see Supported Data Types) |
| `range` | No | Valid value range `[min, max]` |
| `resolution` | No | Grid resolution for continuous dimensions |

### Measure Definition

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Measure name |
| `type` | Yes | Data type (see Supported Data Types) |
| `unit` | No | Physical unit label |
| `qubits` | No | Required for AMPLITUDE type |

---

## Supported Data Types

| Type | Size | Use Case | Example |
|------|------|----------|---------|
| `INT` | 8 bytes | Counts, IDs | 42, -1, 1000 |
| `FLOAT` | 8 bytes (f64) | Measurements | 3.14159, -273.15 |
| `TEXT` | Variable | Labels, names | "hemoglobin" |
| `TIMESTAMP` | 8 bytes | Time series | "2026-05-18T12:00:00Z" |
| `BLOB` | Variable | Binary data | Raw bytes |
| `AMPLITUDE` | 8 bytes per element | Quantum amplitudes | f64 array |
| `COMPLEX` | 16 bytes | Complex numbers | (real, imag) |
| `VECTOR` | N × 8 bytes | Multi-value | [x, y, z] |

---

## When to Use Multidimensional Package

| Use Case | Dimensions | Example Schema |
|----------|-----------|----------------|
| **Climate/weather data** | lat × lon × altitude × time | Temperature, pressure, humidity grids |
| **Medical imaging** | x × y × z × time × modality | CT/MRI/PET volumetric data |
| **Financial time series** | symbol × time × OHLCV × indicators | Global portfolio tracking |
| **Scientific simulations** | spatial grid × time × physical quantities | Navier-Stokes, heat transfer |
| **Quantum state tables** | qubit × amplitude × measurement basis | VQE state vectors |
| **Sensor networks** | sensor_id × time × measurements | IoT telemetry data |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/multidimensional/create` | Create table from schema |
| `POST` | `/api/v1/multidimensional/insert` | Insert rows |
| `POST` | `/api/v1/multidimensional/query` | Range query |
| `POST` | `/api/v1/multidimensional/quantum-query` | Quantum-accelerated query |
| `GET` | `/api/v1/multidimensional/schema/<table_id>` | Get schema |
| `DELETE` | `/api/v1/multidimensional/<table_id>` | Drop table |

---

## Performance

| Metric | Value |
|--------|-------|
| Range queries | O(log N) via mixed-radix index |
| Insert throughput | 1M+ rows/sec on standard hardware |
| Compression | 5-50x typical reduction with zstd chunked compression |
| Quantum acceleration | HHL/QFT on stored amplitude columns |
| Max dimensions | Unlimited (practical: 1-20 for interactive queries) |

---

## Python Example (Full Workflow)

```python
import requests
import numpy as np

BASE = "http://localhost:8080/api/v1/multidimensional"

# 1. Create a schema for seismic sensor data
schema = {
    "table_name": "seismic_network_2026",
    "dimensions": [
        {"name": "station_id", "type": "INT"},
        {"name": "time", "type": "TIMESTAMP", "resolution": "10ms"},
        {"name": "channel", "type": "TEXT"}
    ],
    "measures": [
        {"name": "acceleration", "type": "FLOAT", "unit": "m/s²"},
        {"name": "velocity", "type": "FLOAT", "unit": "m/s"},
        {"name": "displacement", "type": "FLOAT", "unit": "m"}
    ],
    "indexing": "mixed_radix",
    "compression": "chunked_zstd",
    "chunk_size": [100, 1000, 3]
}

resp = requests.post(f"{BASE}/create", json=schema)
table_id = resp.json()["table_id"]
print(f"Created table: {table_id}")

# 2. Insert sensor readings
rows = []
for station in range(10):
    for t in range(100):
        rows.append({
            "station_id": station,
            "time": f"2026-05-18T12:00:{t:02d}.000Z",
            "channel": "BHZ",
            "acceleration": float(np.random.normal(0, 0.01)),
            "velocity": float(np.random.normal(0, 0.001)),
            "displacement": float(np.random.normal(0, 0.0001))
        })

requests.post(f"{BASE}/insert", json={"table_id": table_id, "rows": rows})

# 3. Range query: get all data from stations 0-5 in first 10 seconds
query = {
    "table_id": table_id,
    "ranges": {
        "station_id": [0, 5],
        "time": ["2026-05-18T12:00:00.000Z", "2026-05-18T12:00:10.000Z"]
    },
    "select": ["acceleration", "velocity"]
}
results = requests.post(f"{BASE}/query", json=query).json()
print(f"Query returned {len(results['rows'])} rows")

# 4. Quantum-accelerated query (uses amplitude encoding internally)
quantum_query = {
    "table_id": table_id,
    "ranges": {
        "station_id": [0, 9],
        "time": ["2026-05-18T12:00:00.000Z", "2026-05-18T12:01:00.000Z"]
    },
    "select": ["acceleration"],
    "quantum_accelerated": True,
    "algorithm": "grover"
}
results = requests.post(f"{BASE}/quantum-query", json=quantum_query).json()
print(f"Quantum query found {len(results['matches'])} anomalies")
```

---

## Use Cases

| Research Area | Relevant Sub-Modules |
|---------------|---------------------|
| **Climate Science** | Schema Designer, Array Storage, Range Query |
| **Medical Imaging** | Array Storage, Range Query, Streaming Pipeline |
| **Quantitative Finance** | Schema Designer, Mixed Radix Index, Streaming Pipeline |
| **Scientific Computing** | Array Storage, Range Query, Schema Registry |
| **IoT/Sensor Networks** | Streaming Pipeline, Mixed Radix Index, Range Query |
| **Quantum State Management** | Schema Designer, Array Storage, Mixed Radix Index |

---

## Scale

- **Qubits:** 65536 (for quantum-accelerated queries)
- **Maximum dimensions:** Unlimited
- **Maximum table size:** Limited only by available storage
- **Chunk processing:** < 2 MB active memory per chunk
