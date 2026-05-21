# Nawaz1 Quantum VQE Engine - Usage Guide

> **Multidimensional Quantum Pipeline** — A production-grade quantum VQE engine supporting 15 domains, **63 algorithms across 13 categories**, data persistence, and real-time streaming.

**Author:** Shahnawaz Alam  
**License:** Proprietary  
**Copyright (c) 2026 Shahnawaz Alam. All rights reserved.**

---

> **⚠️ IMPORTANT — Hardware Security & Build Requirements for Launch**
>
> The `nawaz1-server` binary in this repository was compiled on **Ubuntu 22.04 LTS (`x86_64-unknown-linux-gnu`)** with the **Rust 1.70 stable toolchain**.
>
> You **MUST** run it on a **compatible Ubuntu Linux VM** (Ubuntu 22.04 LTS or a binary-compatible derivative on `x86_64`). Running on Windows, macOS, Alpine (musl), or other non-glibc / non-x86_64 systems is **not supported**.
>
> The host VM CPU **MUST** support at least one of the following hardware security extensions:
>
> | Technology | Vendor | Minimum Requirement |
> |-----------|--------|-------------------|
> | **Intel TDX** | Intel | Trust Domain Extensions — 4th Gen Xeon (Sapphire Rapids) or newer |
> | **AMD SEV-SNP** | AMD | Secure Encrypted Virtualization — EPYC 7003 (Milan) or newer |
> | **AMD SEV** | AMD | Secure Encrypted Virtualization — EPYC 7001 (Naples) or newer |
> | **Intel SGX** | Intel | Software Guard Extensions — 6th Gen Core or Xeon E3 v6+ |
> | **Intel Ultra Series** | Intel | Core Ultra 3, 5, 7, 9 (Meteor Lake / Arrow Lake) |
> | **AMD Ryzen AES** | AMD | Ryzen 7, Ryzen 9 with AES-NI hardware acceleration |
>
> **Why?** The quantum engine uses hardware-isolated trusted execution environments (TEEs) for:
> - Protecting quantum state data in memory (encrypted RAM)
> - Secure key management and rotation
> - Side-channel attack resistance
> - Tamper-proof execution of quantum algorithms
>
> **Verification:**
> ```bash
> # Confirm OS
> lsb_release -a    # Expect: Ubuntu 22.04 LTS (or compatible)
> uname -m          # Expect: x86_64
>
> # Confirm hardware security support
> dmesg | grep -i "tdx\|sev\|sgx"
> ```
>
> Launching on unsupported hardware or a non-Ubuntu / non-x86_64 system will result in immediate failure or degraded security posture.

---

## Binary Downloads

Pre-compiled server binaries are included in the `bin/` directory:

| Architecture | Path | Target | Supported CPUs |
|-------------|------|--------|----------------|
| **x86_64** | `bin/x86_64/nawaz1-server` | Intel/AMD 64-bit Linux | Intel TDX/SGX/Ultra 3,5,7,9 — AMD SEV/SEV-SNP/Ryzen 7,9 |
| **ARM64** | `bin/arm64/nawaz1-server` | Apple Silicon Linux VM | Apple M1, M2, M3, M4, M5 series |

### Quick Start

```bash
# For x86_64 (Intel/AMD):
chmod +x bin/x86_64/nawaz1-server
./bin/x86_64/nawaz1-server

# For ARM64 (Apple M1–M5 Linux VM):
chmod +x bin/arm64/nawaz1-server
./bin/arm64/nawaz1-server
```

### Binary Details

- **Build Date:** 2026-05-19
- **Expiration:** 18 months (November 2027)
- **Runtime:** 24/7 — No time restrictions
- **Built with:** Rust 1.95.0, Ubuntu 24.04

---

## How Qubit Count Works (Amplitude Encoding)

The engine automatically determines the optimal qubit allocation for your data through internal analysis (normalization, entropy measurement, and complexity evaluation). You do not need to calculate or specify qubit counts — provide your amplitude data and the engine handles qubit selection.

The engine internally:
1. Normalizes your data (Born normalization)
2. Analyzes Shannon entropy
3. Evaluates element count, bond dimension, and entanglement structure
4. Auto-selects the optimal qubit width

For maximum-scale problems, providing **65536 amplitude values** in the `input_data` array enables the engine to allocate up to 65536 qubits, where each value represents one amplitude in a 65536-dimensional Hilbert space.

| Domain | Problem Scale for 65536 Qubits |
|--------|-------------------------------|
| Chemistry | Hemoglobin protein (8738 atoms, 65536 orbital amplitudes) |
| Physics | 256×256 Heisenberg lattice (65536 sites) — **13 sub-modules** |
| Finance | 65536 financial instruments (global portfolio) |
| Materials | 65536-atom YBCO superconductor crystal — **12 sub-modules** |
| Biomolecules | Hemoglobin tetramer (4532 atoms, 65536 conformations) — **14 sub-modules** |
| Machine Learning | 65536-feature quantum kernel SVM |
| Logistics | 65536-node global supply chain |
| Mathematics | 65536×65536 sparse linear system — **11 sub-modules** |
| Error Mitigation | 65536-amplitude noisy state correction |
| Graphics | 256×256 = 65536-pixel quantum ray tracing |
| Real-Time | 65536-site quantum state evolution |
| Fluid Mechanics | 256×256 Navier-Stokes grid (65536 points) |
| Turbulence CFD | 65536-point DNS turbulence (Re=10000) |
| Heat Transfer | 256×256 thermal conduction grid (65536 nodes) |
| Core Gates | 65536-qubit quantum Fourier transform |
| SDK | Python, C++, Rust, Julia client libraries |
| Cross-Domain | Multi-physics pipeline for complex problems |

---

## Input Data Types & How to Define Them

The quantum engine accepts a wide variety of input data types. Data is automatically normalized to quantum amplitudes internally.

### Primary Data Types

| Type | Description | Size | Example |
|------|-------------|------|---------|
| `int` | Signed 64-bit integer | 8 bytes | `42`, `-1`, `1000000` |
| `float` / `f64` | 64-bit floating point | 8 bytes | `3.14159`, `-273.15`, `1.23e-10` |
| `bool` | Boolean | 1 byte | `true`, `false` |
| `string` | UTF-8 text | Variable | `"hemoglobin"`, `"H2O"` |
| `complex` | Complex number (re, im) | 16 bytes | `(0.707, 0.707)`, `(1.0, 0.0)` |
| `timestamp` | Unix timestamp or ISO-8601 | 8 bytes | `"2026-05-19T12:00:00Z"` |
| `blob` | Raw binary data | Variable | `b"\x00\xFF..."` |
| `null` | Null/missing value | 0 bytes | `null`, `None` |

### Secondary / Composite Data Types

| Type | Description | Example |
|------|-------------|---------|
| `list` | Ordered sequence of same-type elements | `[1.0, 2.0, 3.0, 4.0]` |
| `nested_list` | List of lists (multi-level) | `[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]` |
| `array` | Fixed-size numerical array (f64) | `[0.001, -0.023, 0.045, 0.012]` |
| `nested_array` | Multi-dimensional array (2D, 3D, ND) | `[[[1,2],[3,4]], [[5,6],[7,8]]]` |
| `dict` / `dictionary` | Key-value pairs (string keys) | `{"energy": 0.5, "spin": 1}` |
| `nested_dict` | Dictionary with nested dictionaries | `{"molecule": {"name": "H2O", "bonds": 2}}` |
| `tuple` | Fixed-size ordered collection | `(3.14, "pi", true)` |
| `set` | Unordered unique elements | `{1, 2, 3, 4, 5}` |
| `matrix` | 2D numerical matrix (rows × cols) | `[[1,0,0],[0,1,0],[0,0,1]]` |
| `tensor` | N-dimensional numerical tensor | `shape: [4, 4, 4], data: [...]` |
| `vector` | 1D numerical vector | `[0.1, 0.2, 0.3, ..., 0.9]` |
| `sparse_matrix` | Sparse representation (row, col, val) | `[(0,0,1.0), (1,1,2.0), (2,2,3.0)]` |
| `time_series` | Timestamped values | `[{"t": 0, "v": 1.2}, {"t": 1, "v": 1.5}]` |
| `graph` | Nodes and edges | `{"nodes": [0,1,2], "edges": [[0,1],[1,2]]}` |
| `dataframe` | Tabular data (columns × rows) | `{"col1": [1,2,3], "col2": [4,5,6]}` |

### SDK Data Type Support (All Languages)

#### Python
```python
import numpy as np

# Primary types
input_int = 42
input_float = 3.14159
input_complex = complex(0.707, 0.707)
input_string = "hemoglobin"

# List
input_list = [1.0, 2.0, 3.0, 4.0, 5.0]

# Nested list
input_nested_list = [
    [0.1, 0.2, 0.3],
    [0.4, 0.5, 0.6],
    [0.7, 0.8, 0.9]
]

# NumPy array (recommended for large data)
input_array = np.random.randn(65536).tolist()

# Nested array (multi-dimensional)
input_nested_array = np.random.randn(256, 256).tolist()

# Dictionary
input_dict = {
    "molecule": "C6H12O6",
    "energy": -1.234,
    "bonds": 24
}

# Nested dictionary
input_nested_dict = {
    "system": {
        "molecule": {"name": "hemoglobin", "atoms": 9672},
        "parameters": {"temperature": 310.15, "pressure": 101.325},
        "quantum": {"qubits": 65536}  # depth is auto-selected by the engine
    }
}

# Tuple
input_tuple = (3.14, 2.718, 1.618)

# DataFrame (via pandas)
import pandas as pd
df = pd.DataFrame({
    "position": [0.1, 0.2, 0.3],
    "momentum": [1.0, 2.0, 3.0],
    "spin": [0.5, -0.5, 0.5]
})
input_dataframe = df.to_dict(orient="list")

# Time series
input_timeseries = [
    {"timestamp": "2026-05-19T00:00:00Z", "value": 100.5},
    {"timestamp": "2026-05-19T01:00:00Z", "value": 101.2},
    {"timestamp": "2026-05-19T02:00:00Z", "value": 99.8}
]

# API call with any data type
import requests
payload = {
    "domain": "chemistry",
    "qubits": 65536,
    "input_data": input_array,  # or any type above
    "metadata": input_nested_dict
}
resp = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
```

#### Rust
```rust
use serde_json::json;

// Primary types
let input_int: i64 = 42;
let input_float: f64 = 3.14159;
let input_bool: bool = true;

// Array / Vector
let input_array: Vec<f64> = vec![0.001, -0.023, 0.045, 0.012];

// Nested array (2D)
let input_nested: Vec<Vec<f64>> = vec![
    vec![1.0, 2.0, 3.0],
    vec![4.0, 5.0, 6.0],
    vec![7.0, 8.0, 9.0],
];

// Dictionary (HashMap)
use std::collections::HashMap;
let mut input_dict: HashMap<&str, f64> = HashMap::new();
input_dict.insert("energy", -1.234);
input_dict.insert("spin", 0.5);

// Nested dictionary (JSON object)
let input_nested_dict = json!({
    "molecule": {
        "name": "glucose",
        "formula": "C6H12O6",
        "atoms": 24
    },
    "parameters": {
        "temperature": 298.15,
        "solvent": "water"
    }
});

// Tuple
let input_tuple: (f64, f64, f64) = (3.14, 2.718, 1.618);

// Full API payload
let payload = json!({
    "domain": "biology",
    "qubits": 65536,
    "input_data": input_array,
    "metadata": input_nested_dict
});
```

#### C++
```cpp
#include <vector>
#include <map>
#include <string>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

// Primary types
int64_t input_int = 42;
double input_float = 3.14159;
bool input_bool = true;

// Array / Vector
std::vector<double> input_array = {0.001, -0.023, 0.045, 0.012};

// Nested array (2D vector)
std::vector<std::vector<double>> input_nested = {
    {1.0, 2.0, 3.0},
    {4.0, 5.0, 6.0},
    {7.0, 8.0, 9.0}
};

// Dictionary (map)
std::map<std::string, double> input_dict = {
    {"energy", -1.234},
    {"spin", 0.5},
    {"mass", 12.011}
};

// Nested dictionary (JSON)
json input_nested_dict = {
    {"molecule", {
        {"name", "ethanol"},
        {"formula", "C2H5OH"},
        {"atoms", 9}
    }},
    {"quantum", {
        {"qubits", 65536}   // depth is auto-selected by the engine
    }}
};

// Full payload
json payload = {
    {"domain", "chemistry"},
    {"qubits", 65536},
    {"input_data", input_array},
    {"metadata", input_nested_dict}
};
```

#### Julia
```julia
# Primary types
input_int = 42
input_float = 3.14159
input_complex = 0.707 + 0.707im

# Array
input_array = randn(Float64, 65536)

# Nested array (matrix)
input_nested = [
    1.0 2.0 3.0;
    4.0 5.0 6.0;
    7.0 8.0 9.0
]

# Dictionary
input_dict = Dict(
    "energy" => -1.234,
    "spin" => 0.5,
    "bonds" => 6
)

# Nested dictionary
input_nested_dict = Dict(
    "molecule" => Dict(
        "name" => "caffeine",
        "formula" => "C8H10N4O2",
        "atoms" => 24
    ),
    "parameters" => Dict(
        "temperature" => 300.0,
        "pressure" => 101.325
    )
)

# Tuple
input_tuple = (3.14, 2.718, 1.618)

# Set
input_set = Set([1, 2, 3, 4, 5])

# Named tuple (struct-like)
input_named = (molecule="water", bonds=2, angle=104.5)

# API call
using HTTP, JSON3
payload = Dict(
    "domain" => "physics",
    "qubits" => 65536,
    "input_data" => collect(input_array),
    "metadata" => input_nested_dict
)
resp = HTTP.post("http://localhost:8080/api/v1/quantum/execute",
    ["Content-Type" => "application/json"],
    JSON3.write(payload))
```

### Data Type Conversion Rules

| Input Type | Engine Conversion | Notes |
|-----------|-------------------|-------|
| `int` / `float` | Direct f64 amplitude | Single value → 1 amplitude |
| `list` / `array` | Each element → 1 amplitude | Length becomes qubit dimension |
| `nested_list` | Flattened to 1D array | `[[1,2],[3,4]]` → `[1,2,3,4]` |
| `dict` | Values extracted as amplitudes | Keys preserved in metadata |
| `nested_dict` | Recursively flattened | Deep values become amplitude array |
| `complex` | Re/Im interleaved | `(a+bi)` → `[a, b]` |
| `matrix` | Row-major flattened | 256×256 → 65536 amplitudes |
| `tensor` | Row-major flattened to 1D | All dimensions collapsed |
| `string` | UTF-8 bytes → normalized floats | Each byte → amplitude |
| `dataframe` | Column-major flattened | Each column concatenated |
| `time_series` | Values extracted in time order | Timestamps stored in metadata |
| `graph` | Adjacency matrix → flattened | N nodes → N×N amplitudes |
| `sparse_matrix` | Expanded to dense, then flattened | Zero-filled |

### Auto-Padding
If your input length is not a power of 2, the engine automatically pads with zeros to the next power of 2. For maximum performance, provide exactly **65536** values.

### How Qubit Count is Allocated

The engine automatically determines the optimal qubit allocation for your data through internal analysis (normalization, entropy measurement, and complexity evaluation). You do not need to calculate or specify qubit counts — provide your amplitude data and the engine handles qubit selection.

**Examples:**
```python
# 100 stock prices → engine auto-selects optimal qubits
data = [price for price in stock_prices[:100]]

# 65536 molecular orbital values → engine allocates up to 65536 qubits
data = molecular_amplitudes[:65536]

# 10000 sensor readings → engine auto-selects optimal qubits
data = sensor_readings[:10000]
```

**Best Practice:** Provide exactly 65536 values for maximum qubit utilization and optimal quantum accuracy.

### Physical & Scientific Data Types

The engine natively understands physical quantities with units:

| Physical Type | Unit | Example | Use Case |
|--------------|------|---------|----------|
| `energy` | eV, Hartree, J, kcal/mol | `{"value": -1.234, "unit": "hartree"}` | Molecular energies, band gaps |
| `temperature` | K, °C, °F | `{"value": 310.15, "unit": "K"}` | Thermodynamics, biological systems |
| `pressure` | Pa, atm, bar | `{"value": 101325, "unit": "Pa"}` | Fluid dynamics, chemical reactions |
| `length` | m, Å, nm, bohr | `{"value": 1.54, "unit": "angstrom"}` | Bond lengths, lattice constants |
| `mass` | kg, amu, Da | `{"value": 55845, "unit": "amu"}` | Atomic/molecular mass |
| `time` | s, fs, ps, ns | `{"value": 100, "unit": "fs"}` | Molecular dynamics, reaction rates |
| `frequency` | Hz, THz, cm⁻¹ | `{"value": 3000, "unit": "cm-1"}` | Spectroscopy, phonons |
| `charge` | e, C | `{"value": -2, "unit": "e"}` | Ions, electrochemistry |
| `magnetic_field` | T, G, A/m | `{"value": 1.5, "unit": "tesla"}` | NMR, magnetism |
| `angle` | rad, deg | `{"value": 109.5, "unit": "deg"}` | Bond angles, crystal geometry |
| `velocity` | m/s, km/s | `{"value": 1500, "unit": "m/s"}` | Fluid flow, wave propagation |
| `density` | kg/m³, g/cm³ | `{"value": 1000, "unit": "kg/m3"}` | Materials, fluids |
| `voltage` | V, mV | `{"value": -0.07, "unit": "V"}` | Electrochemistry, neural signals |
| `concentration` | mol/L, mM, μM | `{"value": 0.15, "unit": "mol/L"}` | Solutions, drug concentrations |
| `wavefunction` | amplitude | `[0.707, 0.0, 0.707, 0.0]` | Quantum states directly |

#### Physical Data Example (Python):
```python
# Molecular system with physical units
payload = {
    "domain": "chemistry",
    "qubits": 65536,
    "input_data": orbital_amplitudes,  # f64 array
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

### User-Defined Data Types (UDT)

Define your own custom data types with specific encoding rules for domain-specific applications:

#### Defining a Custom Type
```python
# Register a custom data type
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
        {"name": "b_factor", "type": "float", "encoding": "normalized"},
        {"name": "occupancy", "type": "float", "encoding": "direct"}
    ],
    "flatten_order": "row_major",
    "padding": "auto_power_of_two"
}

# Register the type
resp = requests.post("http://localhost:8080/api/v1/types/register", json=custom_type)
type_id = resp.json()["type_id"]
```

#### Using a Custom Type
```python
# Use your registered type in a quantum execution
protein_data = [
    {"residue_id": 1, "x_coord": 12.5, "y_coord": 8.3, "z_coord": 15.2,
     "residue_type": "ALA", "secondary_structure": "helix", 
     "b_factor": 15.3, "occupancy": 1.0},
    {"residue_id": 2, "x_coord": 13.1, "y_coord": 9.0, "z_coord": 14.8,
     "residue_type": "GLY", "secondary_structure": "helix",
     "b_factor": 12.1, "occupancy": 1.0},
    # ... more residues
]

payload = {
    "domain": "biology",
    "qubits": 65536,
    "input_type": type_id,  # Use your custom type
    "input_data": protein_data,
    "metadata": {"protein": "hemoglobin", "chain": "A"}
}
resp = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
```

#### UDT Encoding Strategies

| Encoding | Description | Best For |
|----------|-------------|----------|
| `direct` | Value used as-is (f64) | Coordinates, energies, amplitudes |
| `normalized` | Min-max scaled to [0, 1] | B-factors, scores, percentages |
| `one_hot` | Category → binary vector | Residue types, element types |
| `categorical` | Category → integer index | Enum-like fields |
| `ordinal` | Sequential integer encoding | IDs, positions, ranks |
| `log_scale` | log₂(value) encoding | Frequencies, concentrations |
| `phase` | Map to [0, 2π] phase angle | Angles, cyclic quantities |
| `binary` | Bit-level encoding | Flags, binary properties |

#### UDT Composition (Nested Types)
```python
# Compose types from other types
molecular_system_type = {
    "type_name": "molecular_system",
    "fields": [
        {"name": "atoms", "type": "protein_structure", "is_array": True},
        {"name": "bonds", "type": "custom:bond_type", "is_array": True},
        {"name": "global_energy", "type": "float"},
        {"name": "charge_distribution", "type": "array", "element_type": "float"},
        {"name": "metadata", "type": "dict"}
    ]
}
```

#### UDT API Endpoints
- `POST /api/v1/types/register` — Register new custom type
- `GET /api/v1/types/list` — List all registered types
- `GET /api/v1/types/<type_id>` — Get type definition
- `DELETE /api/v1/types/<type_id>` — Remove a type
- `POST /api/v1/types/validate` — Validate data against a type

---

### Automatic Depth Selection

> **Important:** Circuit depth is **NOT** a user-configurable parameter.  
> The VQE engine automatically determines the optimal depth based on:
> - Input data complexity (Shannon entropy)
> - Problem domain characteristics
> - Available qubit count
> - Entanglement structure detected by the engine's encoder
>
> Users do NOT need to specify depth. The engine guarantees optimal correlation coverage at the selected depth.

### Algorithm Selection & Algorithm Bridge

> ⚠️ **CRITICAL: You MUST select the correct algorithm for your problem.**  
> **Selecting the wrong algorithm will produce incorrect results.**  
> Read the algorithm list carefully and choose the one that matches your problem type.

The quantum engine provides a **pre-built VQE execution substrate**. The **Algorithm Bridge** compiles your selected algorithm onto this substrate — making the engine universal.

**You specify the algorithm. The Algorithm Bridge handles compilation to VQE.**

---

### Complete Algorithm Reference (63 Algorithms)

#### Category 1: Variational Algorithms
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Variational Quantum Eigensolver | `vqe` | Ground state energy, molecular Hamiltonians, chemistry |
| Quantum Approximate Optimization | `qaoa` | Combinatorial optimization, portfolio, scheduling, routing |
| Variational Quantum Simulation | `vqs` | Real/imaginary time evolution of quantum systems |
| Quantum Natural Gradient | `qng` | Variational parameter optimization with Fisher metric |
| Rotosolve | `rotosolve` | Analytical minimization of variational circuits |

#### Category 2: Quantum Phase & Eigenvalue
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Quantum Phase Estimation | `qpe` | Energy eigenvalues, ground state computation, physics |
| Iterative Phase Estimation | `iqpe` | Resource-efficient phase estimation |
| Quantum Power Method | `qpm` | Dominant eigenvalue extraction |
| Quantum Singular Value Decomposition | `qsvd` | Matrix decomposition, PCA, dimensionality reduction |
| Quantum Principal Component Analysis | `qpca` | Data compression, feature extraction |

#### Category 3: Quantum Fourier & Transform
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Quantum Fourier Transform | `qft` | Frequency analysis, spectral methods, fluid dynamics, signals |
| Inverse Quantum Fourier Transform | `iqft` | Inverse frequency domain problems |
| Quantum Wavelet Transform | `qwt` | Multi-resolution analysis, image processing |
| Quantum Hadamard Transform | `qht` | Boolean analysis, error correction preprocessing |

#### Category 4: Quantum Search & Sampling
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Grover Search | `grover` | Unstructured search, database lookup, SAT problems |
| Quantum Amplitude Estimation | `qae` | Monte Carlo speedup, integration, option pricing |
| Quantum Monte Carlo | `monte_carlo` | Statistical sampling, risk analysis, integration |
| Quantum Amplitude Amplification | `qaa` | Boosting success probability of quantum subroutines |
| Quantum Walk | `quantum_walk` | Graph problems, spatial search, network analysis |

#### Category 5: Linear Algebra & Systems
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Harrow-Hassidim-Lloyd (HHL) | `hhl` | Linear systems Ax=b, differential equations |
| Quantum Linear Solver | `qls` | Sparse linear systems with quantum speedup |
| Quantum Matrix Inversion | `qmi` | Matrix inversion, regression |
| Quantum LU Decomposition | `qlu` | Direct linear system solving |
| Block Encoding | `block_encoding` | Quantum signal processing, matrix arithmetic |

#### Category 6: Quantum Simulation & Dynamics
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Trotter-Suzuki Evolution | `trotter` | Real-time quantum dynamics, Hamiltonian simulation |
| DMRG (Density Matrix RG) | `dmrg` | 1D strongly correlated systems, ground states |
| Time-Evolving Block Decimation | `tebd` | 1D quantum lattice time evolution |
| Quantum Lanczos | `lanczos` | Low-lying eigenvalues, spectroscopy |
| Krylov Subspace Methods | `krylov` | Sparse Hamiltonian evolution |

#### Category 7: Quantum Machine Learning
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Quantum Neural Network | `qnn` | Classification, regression, pattern recognition |
| Quantum Support Vector Machine | `qsvm` | Classification with kernel methods |
| Quantum k-Means | `qkmeans` | Clustering, unsupervised learning |
| Quantum Boltzmann Machine | `qbm` | Generative models, distribution learning |
| Quantum Kernel Estimation | `qke` | Feature map learning, similarity metrics |
| Quantum Transfer Learning | `qtl` | Domain adaptation, few-shot learning |

#### Category 8: Error Mitigation & Correction
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Zero-Noise Extrapolation | `zne` | Noise mitigation by extrapolating to zero noise |
| Probabilistic Error Cancellation | `pec` | Quasi-probability error cancellation |
| Clifford Data Regression | `cdr` | Training-based error mitigation |
| Symmetry Verification | `symmetry_verify` | Detecting errors via symmetry checks |
| Quantum Error Correction (Steane) | `steane` | Full error correction (7-qubit) |

#### Category 9: Quantum Cryptography & Security
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Quantum Key Distribution | `qkd` | Secure key exchange |
| Quantum Random Number Generation | `qrng` | True randomness, cryptographic seeds |
| Shor's Algorithm | `shor` | Integer factorization |
| Quantum Digital Signature | `qds` | Message authentication |

#### Category 10: Tensor Network Methods
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Matrix Product State | `mps` | 1D quantum systems, area-law entanglement |
| Multi-scale Entanglement RG | `mera` | Critical systems, scale-invariant problems |
| Projected Entangled Pair States | `peps` | 2D quantum systems, lattice models |
| Tree Tensor Network | `ttn` | Hierarchical systems, molecular simulations |
| Tensor Train Decomposition | `tensor_train` | High-dimensional function approximation |

#### Category 11: Classical-Quantum Hybrid
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Coupled Cluster (CCSD) | `ccsd` | High-accuracy molecular chemistry |
| Quantum-Classical Neural ODE | `qnode` | Differential equation learning |
| Quantum Belief Propagation | `qbp` | Graphical models, Bayesian inference |
| Quantum Semidefinite Programming | `qsdp` | Convex optimization, relaxations |
| Quantum Interior Point | `qip` | Convex optimization, linear programming |

#### Category 12: Specialized Quantum Algorithms
| Algorithm | Key | Best For |
|-----------|-----|----------|
| Quantum Counting | `quantum_count` | Counting solutions to search problems |
| Quantum Mean Estimation | `qme` | Statistical mean with quantum speedup |
| Quantum Gradient Descent | `qgd` | Parameter optimization in quantum circuits |
| Bernstein-Vazirani | `bv` | Finding hidden linear functions |
| Simon's Algorithm | `simon` | Finding hidden periods |
| Quantum Topological Data Analysis | `qtda` | Persistent homology, topological features |
| Quantum Metropolis Sampling | `metropolis` | Thermal state preparation, MCMC |
| Quantum Gibbs Sampling | `gibbs` | Thermal equilibrium states, partition functions |

---

### Algorithm Selection Guide

> **Wrong algorithm = wrong results.** Match your problem to the correct algorithm:

| My Problem | Use This Algorithm |
|-----------|-------------------|
| Finding lowest energy of a molecule | `vqe` |
| Optimizing a portfolio / routing problem | `qaoa` |
| Solving linear system Ax = b | `hhl` |
| Frequency/spectral analysis | `qft` |
| Searching unsorted data | `grover` |
| Statistical sampling / Monte Carlo | `monte_carlo` |
| Physics time evolution | `trotter` |
| 1D strongly correlated electrons | `dmrg` |
| Neural network / classification | `qnn` |
| Reducing noise in results | `zne` |
| High-accuracy molecular chemistry | `ccsd` |
| 2D lattice quantum system | `peps` |
| Quantum key distribution | `qkd` |
| Integer factorization | `shor` |

---

### Request Format

```json
{
  "domain": "finance",
  "algorithm": "qaoa",
  "qubits": 65536,
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "portfolio",
    "task": "optimization"
  }
}
```

The Algorithm Bridge compiles your selected algorithm onto the VQE execution substrate automatically.

---

## Runtime

Active 24/7 — No time restrictions on this build.

The quantum engine runs continuously with no session limits or cooldown periods.

## Full Access Includes:

⏰ Unlimited runtime — no cooldown, no time limits

📦 More packages — additional specialized domains

🔌 Extensions & Plugins — custom algorithm extensions

🎯 UDF (User-Defined Functions) — custom quantum routines

📊 User-Defined Data Types — custom input schemas

💾 Persistence — quantum state storage & retrieval

🔐 Advanced Security — enhanced encryption, audit logs

📈 Monitoring — real-time performance dashboards

🏗️ Infrastructure — dedicated compute resources

📊 Dashboard — web-based management console

🌐 Unified Multi-Domain Engine — seamless cross-domain orchestration

🏢 Multi-Datacenter — geo-distributed quantum compute

🔄 Streaming Pipeline — real-time quantum data streams

⚡ Maximum Qubits — beyond 65536, scale to quadrillions

🎁 Custom Packages — bespoke domain packages on request

Contact: For paid tier access, contact Shahnawaz Alam

---

## Biomolecules Domain — 14 Quantum Biology Sub-Modules

The **biomolecules** domain contains 14 specialized sub-modules providing comprehensive quantum biology coverage:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **DNA/RNA** | Nucleotide base encoding, Watson-Crick pairing, hybridization thermodynamics |
| 2 | **Drug Discovery** | Lipinski's Rule of Five, Veber rules, Ghose filter, QED scoring |
| 3 | **Enzyme Catalysis** | Michaelis-Menten kinetics, inhibition types, diffusion-limited catalysis |
| 4 | **Glycobiology** | Monosaccharide classification, glycosidic bonds, lectin binding |
| 5 | **Membrane Biophysics** | Ion channels, Nernst/Goldman equations, membrane potential |
| 6 | **Metabolic Networks** | Flux balance analysis, Gibbs free energy, compartment modeling |
| 7 | **Molecular Dynamics** | Force fields (AMBER/CHARMM), Lennard-Jones, Coulomb, trajectory integration |
| 8 | **Neurochemistry** | 10 neurotransmitter types, receptor binding, synaptic dynamics |
| 9 | **Photosynthesis** | Chromophore types, quantum yield, exciton energy transfer |
| 10 | **Protein Folding** | 20 amino acids, Ramachandran analysis, energy landscapes |
| 11 | **Protein-Protein Interactions** | Interface properties, SASA, binding free energy |
| 12 | **Quantum Virology** | Capsid geometry, icosahedral symmetry, T-number classification |
| 13 | **Structural Biology** | X-ray scattering factors, structure factor calculations |
| 14 | **Systems Biology** | Hill functions, gene regulatory networks, cooperativity |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/biology/README.md`](packages/biology/README.md) for full API documentation per sub-module.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "drug_discovery", "task": "drug_likeness" }
}
```

**Demo endpoint:** `POST /api/v1/quantum/biomolecules/demo`

---

## Physics Domain — 13 Quantum Physics Sub-Modules

The **physics** domain contains 13 specialized sub-modules providing comprehensive quantum physics coverage from field theory to cosmology:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **Quantum Field Theory** | Lorentz 4-vectors, Dirac spinors, Feynman diagrams, renormalization, scattering amplitudes |
| 2 | **Quantum Electrodynamics** | Vacuum polarization, anomalous magnetic moment (5-loop), Lamb shift, Schwinger effect |
| 3 | **Quantum Chromodynamics** | SU(3) color algebra, running α_s (4-loop), confinement, DGLAP splitting, jet physics |
| 4 | **Relativistic Quantum Mechanics** | Klein-Gordon, Dirac hydrogen, Zitterbewegung, Klein paradox, Mott scattering |
| 5 | **Quantum Gravity** | Hawking radiation, black hole entropy, Unruh effect, Loop Quantum Gravity, GUP |
| 6 | **Quantum Entanglement Theory** | CHSH/Mermin/Svetlichny Bell tests, concurrence, negativity, teleportation, distillation |
| 7 | **Quantum Optics** | Fock/coherent/squeezed states, Jaynes-Cummings, g⁽²⁾ correlations, HOM effect |
| 8 | **Quantum Thermodynamics** | Quantum Otto/Carnot cycles, Jarzynski equality, Landauer's principle, quantum batteries |
| 9 | **Quantum Chaos** | RMT ensembles (GOE/GUE/GSE), OTOC, ETH, spectral form factor, SYK model |
| 10 | **Open Quantum Systems** | Lindblad master equation, T₁/T₂ decoherence, quantum channels, Zeno effect |
| 11 | **Quantum Phase Transitions** | Transverse-field Ising, critical exponents, BKT transition, Kibble-Zurek mechanism |
| 12 | **Quantum Metrology** | Quantum Fisher information, SQL vs Heisenberg limit, Ramsey interferometry |
| 13 | **Quantum Cosmology** | Wheeler-DeWitt equation, inflation observables, primordial power spectrum, quantum bounce |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/physics/README.md`](packages/physics/README.md) for full API documentation per sub-module.

```json
{
  "domain": "physics",
  "algorithm": "qpe",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "quantum_field_theory", "task": "scattering_amplitude" }
}
```

**Demo endpoint:** `POST /api/v1/quantum/physics/demo`

---

## Mathematics Domain — 11 Quantum Mathematics Sub-Modules

The **mathematics** domain contains 11 specialized sub-modules providing comprehensive quantum mathematical foundations:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **Quantum Algebra** | Lie algebras (SU, SO, Sp, E₆-E₈), Clifford algebras, Pauli/Weyl algebras |
| 2 | **Quantum Information Theory** | Von Neumann/Rényi entropy, quantum channels, Fisher information, Holevo bound |
| 3 | **Quantum Topology** | Jones polynomial, braid groups, Chern-Simons theory, TQFT partition functions |
| 4 | **Quantum Differential Geometry** | Fiber bundles, gauge fields, Berry connection, Fubini-Study metric, Chern numbers |
| 5 | **Quantum Functional Analysis** | Hilbert space, spectral decomposition, trace class operators, POVM |
| 6 | **Quantum Probability** | Quantum random walks, quantum Markov chains, non-commutative probability |
| 7 | **Quantum Harmonic Analysis** | Wigner function, Husimi Q, Glauber P, Moyal star product |
| 8 | **Quantum Category Theory** | Monoidal/dagger categories, quantum logic lattice, Frobenius algebras |
| 9 | **Quantum Optimization Theory** | SDP relaxations, quantum game theory, Nash equilibrium, QAOA mapping |
| 10 | **Quantum Number Theory** | Shor's factoring, discrete logarithm, Stabilizer/CSS/Toric/Surface codes |
| 11 | **Advanced Quantum Probability** | Free probability (Voiculescu), Wigner semicircle, Marchenko-Pastur, Tracy-Widom, quantum CLT, quantum martingales, concentration inequalities, quantum optimal transport (Wasserstein), quantum copula, Schatten class |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/mathematics/README.md`](packages/mathematics/README.md) for full API documentation per sub-module.

```json
{
  "domain": "mathematics",
  "algorithm": "hhl",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "quantum_topology", "task": "jones_polynomial" }
}
```

**Demo endpoint:** `POST /api/v1/quantum/mathematics/demo`

---

## Chemistry Domain — 5 Quantum Chemistry Sub-Modules

The **chemistry** domain contains 5 specialized sub-modules providing comprehensive quantum chemistry coverage from electronic structure to variational eigensolvers:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **Algorithms** | VQE, QPE, ADAPT-VQE, QITE, quantum dynamics, excited state VQE, subspace VQE |
| 2 | **Geometry** | 3D vector operations, bond length/angle computations, molecular geometry analysis |
| 3 | **Molecular** | Hamiltonian construction, Jordan-Wigner mapping, 1e/2e integrals, expectation values |
| 4 | **Orbital Optimization** | Active space selection (CAS, SCI, natural orbital, entanglement-based), embedding engines |
| 5 | **VQE Chemistry** | UCCSD/HEA/k-UpCCGSD ansatz, ground & excited state energy computation |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/chemistry/README.md`](packages/chemistry/README.md) for full API documentation per sub-module.

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "vqe_chemistry", "task": "ground_state_energy", "molecule": "C6H6" }
}
```

**Demo endpoint:** `POST /api/v1/quantum/chemistry/demo`

---

## Finance Domain — 6 Quantum Finance Sub-Modules

The **finance** domain contains 6 specialized sub-modules providing comprehensive quantum-accelerated financial modeling, from market data ingestion to portfolio optimization and trading execution:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **Market Data** | Bloomberg, Refinitiv, Yahoo Finance, Alpha Vantage feed integration, real-time ingestion |
| 2 | **Monte Carlo** | Control variates, antithetic, importance sampling, GBM, Ornstein-Uhlenbeck, Heston |
| 3 | **Portfolio** | Markowitz, risk parity, min variance, max Sharpe, Black-Litterman, hierarchical risk parity |
| 4 | **Quantum Algorithms** | Quantum Amplitude Estimation (QAE), QSVM, Quantum Generative Models |
| 5 | **Risk Metrics** | VaR, CVaR/Expected Shortfall, max drawdown, Sharpe ratio, Sortino ratio |
| 6 | **Trading System** | Order types (market, limit, stop, FOK, IOC), risk management, trade execution |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/finance/README.md`](packages/finance/README.md) for full API documentation per sub-module.

```json
{
  "domain": "finance",
  "algorithm": "qaoa",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "portfolio", "task": "markowitz_optimization", "num_assets": 65536 }
}
```

**Demo endpoint:** `POST /api/v1/quantum/finance/demo`

---

## Fluid Mechanics Domain — 6 Quantum CFD Sub-Modules

The **fluid_mechanics** domain contains 6 specialized sub-modules providing comprehensive quantum-accelerated computational fluid dynamics from incompressible Navier-Stokes to quantum-native linear solvers:

| # | Sub-Module | Key Capabilities |
|---|-----------|------------------|
| 1 | **Navier-Stokes** | Incompressible/compressible solver, multi-regime (subsonic to hypersonic), FVM |
| 2 | **Turbulence** | DNS, RANS (k-ε, k-ω, k-ω SST), LES (Smagorinsky, WALE, dynamic), DES/DDES/IDDES |
| 3 | **Compressible** | Euler/Navier-Stokes/LES with Roe, HLLC, AUSM+ flux schemes for shock-capturing |
| 4 | **Multiphase** | VOF, level set, CLSVOF, phase field, front tracking, CSF/CSS surface tension |
| 5 | **Heat Transfer** | Conduction, convection, conjugate, radiation (S2S, discrete ordinates, P1) |
| 6 | **Quantum CFD** | HHL, VQLS, QSVT, VQE solvers for fluid mechanics, error mitigation |

**Usage:** Set `"config": {"sub_module": "<name>"}` in the execute request body. See [`packages/fluid_mechanics/README.md`](packages/fluid_mechanics/README.md) for full API documentation per sub-module.

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "qft",
  "input_data": ["...65536 floats..."],
  "config": { "sub_module": "turbulence", "task": "les_simulation", "model": "k_omega_sst" }
}
```

**Demo endpoint:** `POST /api/v1/quantum/fluid_mechanics/demo`

---

## Table of Contents

- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Complete Algorithm Reference (63 Algorithms)](#complete-algorithm-reference-63-algorithms)
- [Algorithm Summary Table](#algorithm-summary-table)
- [Data Import Guide](#data-import-guide)
- [Authentication & Security](#authentication--security)
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
    "input_data": data  # 65536 values → engine allocates 65536 qubits
})
print(resp.json())
```

### 4. Run All Examples

```bash
pip install numpy requests
python quantum_usage_examples.py              # Run all 63 algorithms
python quantum_usage_examples.py --list       # List all categories
python quantum_usage_examples.py vqe_family   # Run single category
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

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/quantum/status` | Engine status (qubits, memory, tier) |
| `GET` | `/api/v1/quantum/domains` | List available domains |
| `POST` | `/api/v1/quantum/execute` | **Execute quantum computation** |
| `POST` | `/api/v1/quantum/optimizer/run` | Run VQE with specific optimizer |
| `POST` | `/api/v1/quantum/vqs/evolve` | VQS time evolution |
| `POST` | `/api/v1/quantum/pipeline/execute` | Full quantum pipeline |
| `POST` | `/api/v1/multidimensional/query` | Multidimensional range query |

---

## Complete Algorithm Reference (63 Algorithms)

**ARCHITECTURAL KEY POINT:** All algorithms route through the **Algorithm Bridge** onto the pre-built VQE circuit substrate. The `algorithm` field is metadata for orchestration — execution always goes through the same unified parametric circuit. Only the parameter vector changes.

---

### Category A: VQE Family (8 variants)

The core variational quantum eigensolver and its specialized variants.

| # | Algorithm | Description | When to Use | Key Fields |
|---|-----------|-------------|-------------|------------|
| A1 | Standard VQE | Variational ground-state energy solver | Default for energy minimization | `"algorithm": "vqe"` |
| A2 | ADAPT-VQE | Iteratively grows ansatz from operator pool | When circuit depth must be minimized | `"algorithm": "adapt_vqe"` |
| A3 | Subspace VQE | Solves multiple eigenstates simultaneously | Excited states, spectroscopy | `"algorithm": "subspace_vqe", "num_eigenstates": 6` |
| A4 | Hardware-Aware VQE | Circuit adapted to device connectivity | Noisy hardware deployment | `"algorithm": "hardware_aware_vqe", "topology": "heavy_hex"` |
| A5 | VQE + Measurement Reduction | Fewer shots via Pauli grouping | Large Hamiltonians (many terms) | `"algorithm": "vqe_measurement_reduction"` |
| A6 | VQE + Quantum Fisher | Natural gradient using Fisher information | Barren plateau avoidance | `"algorithm": "vqe_quantum_fisher"` |
| A7 | VQE + Error Mitigation | Built-in noise correction | Noisy intermediate-scale | `"algorithm": "vqe_error_mitigated", "mitigation": "zne"` |
| A8 | VQE + Advanced Optimizer | Meta-learned optimization | Fast convergence on new molecules | `"algorithm": "vqe_advanced_optimizer"` |

---

### Category B: VQE Advanced Optimizers (6)

Classical optimizers that drive the VQE variational loop. Use endpoint `/api/v1/quantum/optimizer/run`.

| # | Optimizer | Description | When to Use |
|---|-----------|-------------|-------------|
| B1 | SPSA | Simultaneous Perturbation Stochastic Approximation | Noisy cost functions, hardware |
| B2 | CMA-ES | Covariance Matrix Adaptation Evolution Strategy | Global optimization, few parameters |
| B3 | L-BFGS-B | Limited-memory BFGS with box constraints | Smooth landscapes, many parameters |
| B4 | QNG | Quantum Natural Gradient (Fisher metric) | Avoiding barren plateaus |
| B5 | Rotosolve | Analytical single-parameter rotation | Rz/Ry gates, exact 1D minima |
| B6 | Nelder-Mead | Simplex direct search (derivative-free) | Non-differentiable landscapes |

```json
{"algorithm": "vqe", "optimizer": "qng", "max_iterations": 500}
```

---

### Category C: VQE Advanced Ansätze (5)

Parametric circuit structures for the VQE substrate.

| # | Ansatz | Description | When to Use |
|---|--------|-------------|-------------|
| C1 | UCCSD | Unitary Coupled Cluster Singles & Doubles | Chemistry (gold standard) |
| C2 | QubitAdapt-VQE | Iteratively grows qubit operator pool | Minimal circuit depth |
| C3 | Symmetry-Preserving | Respects molecular/system symmetries | Symmetry-constrained problems |
| C4 | k-UpCCGSD | k-fold Unitary pair Coupled Cluster GSD | Strongly correlated systems |
| C5 | LDCA | Low-Depth Circuit Ansatz (log-depth) | Hardware with limited coherence |

```json
{"algorithm": "vqe", "ansatz": "uccsd", "excitation_order": "singles_doubles"}
```

---

### Category D: QAOA Variants (5)

Quantum Approximate Optimization Algorithm variants for combinatorial problems.

| # | Variant | Description | When to Use |
|---|---------|-------------|-------------|
| D1 | Standard QAOA | Fixed p-layer mixer/cost schedule | General combinatorial optimization |
| D2 | Adaptive QAOA | Dynamically adds layers until convergence | Unknown optimal depth |
| D3 | Continuous QAOA | Continuous-time quantum walk formulation | Time-continuous cost functions |
| D4 | Multi-Angle QAOA | Independent angle per constraint | Problems with many constraints |
| D5 | Warm-Start QAOA | Initialized from classical relaxation | When classical approximation exists |

```json
{"algorithm": "qaoa", "qaoa_variant": "adaptive", "max_layers": 20}
```

---

### Category E: HHL Family (4)

Quantum linear algebra algorithms with exponential speedup for sparse systems.

| # | Algorithm | Description | When to Use |
|---|-----------|-------------|-------------|
| E1 | Standard HHL | Harrow-Hassidim-Lloyd for Ax=b | Sparse well-conditioned systems |
| E2 | Preconditioned HHL | Better conditioned linear solve | Ill-conditioned matrices |
| E3 | QSVT | Quantum Singular Value Transformation | General matrix functions |
| E4 | Quantum Regression | Quantum-enhanced least squares | Regression/fitting |

```json
{"algorithm": "qsvt", "problem_type": "matrix_function", "function": "matrix_inversion"}
```

---

### Category F: Grover & Quantum Search (2)

| # | Algorithm | Description | When to Use |
|---|-----------|-------------|-------------|
| F1 | Grover Search | O(√N) unstructured quantum search | Unstructured search, database queries |
| F2 | Quantum Binary Search (QBS) | O(log N) structured quantum search | Structural search, sorted data, ordered indices |

```json
{"algorithm": "grover", "search_space_size": 65536, "target_states": [42, 1337]}
```

---

### Category G: Error Mitigation (5)

Post-processing techniques to reduce noise in quantum results.

| # | Method | Description | When to Use |
|---|--------|-------------|-------------|
| G1 | ZNE | Zero-Noise Extrapolation (Richardson) | General noise reduction |
| G2 | PEC | Probabilistic Error Cancellation | Known noise model |
| G3 | Virtual Distillation | Multi-copy state purification | High-fidelity required |
| G4 | CDR | Clifford Data Regression | Near-Clifford circuits |
| G5 | Readout Mitigation | Measurement error correction | Readout-dominated noise |

```json
{"mitigation_method": "zne", "noise_factors": [1.0, 1.5, 2.0, 2.5, 3.0]}
```

---

### Category H: Measurement Reduction (3)

Reduce measurement overhead for expectation value estimation.

| # | Method | Description | When to Use |
|---|--------|-------------|-------------|
| H1 | Term Grouper | Groups commuting Pauli terms | Large Hamiltonians |
| H2 | Classical Shadow | Randomized measurements for many observables | Many observables simultaneously |
| H3 | Adaptive Shot Allocator | Variance-aware shot budget distribution | Fixed shot budget optimization |

```json
{"measurement_strategy": "classical_shadow", "num_shadows": 10000}
```

---

### Category I: Numerical/Scientific Solvers (7)

PDE solvers and scientific computing on the quantum substrate.

| # | Method | Description | When to Use |
|---|--------|-------------|-------------|
| I1 | FDM | Finite Difference Method | Structured grids, simple domains |
| I2 | FEM | Finite Element Method | Complex geometries, unstructured mesh |
| I3 | FVM | Finite Volume Method | Conservation laws, compressible flow |
| I4 | IMEX | Implicit-Explicit time stepping | Stiff reaction-diffusion systems |
| I5 | Multigrid | Hierarchical elliptic PDE solver | Elliptic equations, fast convergence |
| I6 | PDE General | General quantum-accelerated PDE framework | Heat/wave/diffusion equations |
| I7 | SINDy | Sparse Identification of Nonlinear Dynamics | Data-driven model discovery |

```json
{"problem_type": "pde_solver", "pde_method": "fem", "equation": "heat_equation_3d"}
```

---

### Category J: Specialized Quantum (5)

Domain-specific quantum primitives and algorithms.

| # | Algorithm | Description | When to Use |
|---|-----------|-------------|-------------|
| J1 | QFT | Quantum Fourier Transform | Frequency analysis, phase kickback |
| J2 | QPE | Quantum Phase Estimation | Eigenvalue extraction |
| J3 | Quantum Monte Carlo | Projector/diffusion Monte Carlo | Ground states of lattice models |
| J4 | Belief Propagation | Quantum message passing on factor graphs | Graphical model inference |
| J5 | Knowledge Compilation | Boolean function to quantum circuit | Circuit synthesis |

```json
{"algorithm": "qpe", "problem_type": "phase_estimation", "precision_bits": 16}
```

---

### Category K: Condensed Matter (4)

Lattice quantum many-body models at scale.

| # | Model | Description | When to Use |
|---|-------|-------------|-------------|
| K1 | Heisenberg | XXZ antiferromagnet on square lattice | Magnetic materials |
| K2 | Hubbard | Strongly correlated electron model | High-Tc superconductors |
| K3 | Ising | Transverse-field quantum spin chain | Phase transitions |
| K4 | Lattice Gauge Theory | SU(3) gauge field on lattice | QCD, high-energy hadronic physics |

```json
{"problem_type": "condensed_matter", "model": "hubbard", "hopping_t": 1.0, "interaction_u": 4.0}
```

---

### Category L: Time Evolution (3)

Quantum dynamics simulation algorithms.

| # | Algorithm | Description | When to Use |
|---|-----------|-------------|-------------|
| L1 | VQS | Variational Quantum Simulation (McLachlan) | Real-time dynamics |
| L2 | TEBD | Time-Evolving Block Decimation | 1D systems, long times |
| L3 | QITE | Quantum Imaginary Time Evolution | Ground state preparation, thermal states |

```json
// VQS endpoint:
POST /api/v1/quantum/vqs/evolve
{"num_sites": 65536, "time_steps": 50, "dt_seconds": 0.02, "hamiltonian": "heisenberg_xxz"}
```

---

### Category M: Advanced Quantum (6)

Cutting-edge quantum algorithms for specialized applications.

| # | Algorithm | Description | When to Use |
|---|-----------|-------------|-------------|
| M1 | Shor's Algorithm | Integer factorization (exponential speedup) | Cryptanalysis, number theory |
| M2 | Quantum Lindblad Solver | Open quantum system dynamics | Decoherence, dissipation |
| M3 | Quantum Thermodynamics | Partition function & free energy | Thermal equilibrium properties |
| M4 | Quantum Metrology | Heisenberg-limited parameter estimation | Precision sensing |
| M5 | QNN | Quantum Neural Network (variational classifier) | Classification, generative models |
| M6 | QPINN | Quantum Physics-Informed Neural Network | PDE solving with physics constraints |

```json
{"algorithm": "shor", "problem_type": "integer_factoring", "number_to_factor": 18446744073709551557}
```

---

## Algorithm Summary Table

| Category | Count | Algorithms |
|----------|-------|------------|
| A. VQE Family | 8 | Standard, ADAPT, Subspace, Hardware-Aware, Measurement Reduction, Quantum Fisher, Error Mitigated, Advanced Optimizer |
| B. VQE Optimizers | 6 | SPSA, CMA-ES, L-BFGS-B, QNG, Rotosolve, Nelder-Mead |
| C. VQE Ansätze | 5 | UCCSD, QubitAdapt, Symmetry-Preserving, k-UpCCGSD, LDCA |
| D. QAOA Variants | 5 | Standard, Adaptive, Continuous, Multi-Angle, Warm-Start |
| E. HHL Family | 4 | Standard HHL, Preconditioned HHL, QSVT, Quantum Regression |
| F. Grover & Quantum Search | 2 | Grover Search, Quantum Binary Search (QBS) |
| G. Error Mitigation | 5 | ZNE, PEC, Virtual Distillation, CDR, Readout Mitigation |
| H. Measurement Reduction | 3 | Term Grouper, Classical Shadow, Adaptive Shot Allocator |
| I. Numerical/Scientific | 7 | FDM, FEM, FVM, IMEX, Multigrid, PDE General, SINDy |
| J. Specialized Quantum | 5 | QFT, QPE, Quantum Monte Carlo, Belief Propagation, Knowledge Compilation |
| K. Condensed Matter | 4 | Heisenberg, Hubbard, Ising, Lattice Gauge Theory |
| L. Time Evolution | 3 | VQS, TEBD, QITE |
| M. Advanced Quantum | 6 | Shor, Lindblad Solver, Thermodynamics, Metrology, QNN, QPINN |
| **TOTAL** | **63** | |

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
```

### 2. Create Table & Insert

```bash
curl -X POST http://localhost:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query":"CREATE TABLE experiments (id INT, domain TEXT, energy REAL, fidelity REAL)"}'
```

### 3. Bulk Import

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

---

## Authentication & Security

### API Key Mode

When `NAWAZ1_API_KEY` is set, all quantum endpoints require `X-API-Key` header:

```bash
NAWAZ1_API_KEY=my-secret-key-123 ./nawaz1-server

curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "X-API-Key: my-secret-key-123" \
  -d '{"domain":"chemistry","algorithm":"vqe","input_data":[...]}'
```

### JWT Authentication

For data operations (query, import), use JWT tokens obtained from `/api/v1/auth/login`.

---

## Running the Examples

### Files in this repository

| File | Description |
|------|-------------|
| `quantum_usage_examples.py` | All **63 algorithms** at 65536-qubit scale (Python + numpy) |
| `data_import_examples.py` | Auth, tables, import, query (Python) |
| `run_all_demos.sh` | Full demo runner (Bash) |
| `run_all_demos.ps1` | Full demo runner (PowerShell) |
| `README.md` | This documentation |

### Prerequisites

- **Server:** nawaz1-server binary running
- **Python:** 3.8+ with `numpy` and `requests` (`pip install numpy requests`)

### Run Individual Categories

```bash
python quantum_usage_examples.py vqe_family          # Category A
python quantum_usage_examples.py vqe_optimizers      # Category B
python quantum_usage_examples.py vqe_ansatz          # Category C
python quantum_usage_examples.py qaoa_variants       # Category D
python quantum_usage_examples.py hhl_family          # Category E
python quantum_usage_examples.py grover              # Category F
python quantum_usage_examples.py error_mitigation    # Category G
python quantum_usage_examples.py measurement_reduction  # Category H
python quantum_usage_examples.py numerical_solvers   # Category I
python quantum_usage_examples.py specialized_quantum # Category J
python quantum_usage_examples.py condensed_matter    # Category K
python quantum_usage_examples.py time_evolution      # Category L
python quantum_usage_examples.py advanced_quantum    # Category M
python quantum_usage_examples.py algorithms          # ALL categories
python quantum_usage_examples.py --list              # Show all options
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
