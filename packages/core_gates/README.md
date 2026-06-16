# Quantum Core Gates Package

## Overview

The Core Gates package provides low-level quantum gate synthesis, circuit optimization, and gate-level control through the unified VQE engine at 2^53-qubit scale. It enables custom circuit construction, gate decomposition, quantum error correction codes, and teleportation protocols.

## Key Features

- **Gate synthesis** — decompose arbitrary unitaries into native gate sets
- **Circuit optimization** — reduce gate count and circuit depth automatically
- **Quantum error correction** — surface codes, Steane codes, and repetition codes
- **Quantum teleportation** — state transfer protocols with Bell measurements
- **Custom gate design** — parameterized gates and pulse-level control
- **Gate fidelity analysis** — compute process fidelity and diamond distance
- **Circuit compilation** — map logical circuits to hardware-constrained topologies
- **Quantum Fourier Transform** — optimized QFT circuits at 2^53-qubit scale

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **Circuit Optimization** | Minimize gate count and depth for quantum circuits |
| **QEC** | Quantum Error Correction code encoding and decoding |
| **Teleportation** | Quantum state transfer via entanglement |
| **QFT** | Quantum Fourier Transform circuit implementation |
| **Grover** | Oracle construction and amplitude amplification |
| **VQE** | Variational circuit parameter optimization |

## Scale

- **Qubits:** Up to 2^53 (9,007,199,254,740,992)
- **Maximum circuit depth:** 10^9 gates (1 billion gate throughput)
- **Gate types:** All standard gates (H, X, Y, Z, CNOT, Toffoli, Rz, Ry, etc.)

## Input Data Format

The input data array encodes the quantum circuit or target unitary as N floating-point values (up to 2^53).

```json
{
  "domain": "core_gates",
  "algorithm": "circuit_optimization",
  "input_data": [/* N float values: circuit parameters or target unitary (up to 2^53) */],
  "config": {
    "task": "optimize",
    "gate_set": ["h", "cnot", "rz", "rx"],
    "target_depth": 100,
    "optimization_level": 3,
    "topology": "all_to_all"
  }
}
```

**Input encoding:**
- For circuit optimization: amplitudes encode gate parameters and circuit structure
- For gate synthesis: amplitudes encode the target unitary matrix elements
- For QEC: amplitudes encode the logical state to be protected

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "core_gates",
    "algorithm": "circuit_optimization",
    "input_data": [0.785, 1.571, 0.0, 3.14159, ... /* N gate parameters (up to 2^53) */],
    "config": {
      "task": "optimize",
      "gate_set": ["h", "cnot", "t", "tdg", "s", "rz"],
      "num_qubits": 1024,
      "original_depth": 50000,
      "target_depth": 10000,
      "preserve_unitary": true,
      "optimization_passes": ["commutation", "cancellation", "synthesis"]
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Encode circuit parameters for optimization
gate_params = np.random.uniform(0, 2*np.pi, 1024)  # Example uses 1024; engine supports up to 2^53.tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "core_gates",
        "algorithm": "circuit_optimization",
        "input_data": gate_params,
        "config": {
            "task": "optimize",
            "gate_set": ["h", "cnot", "rz"],
            "num_qubits": 1024,
            "optimization_level": 3
        }
    }
)
print(response.json())
```

## Example Response

```json
{
  "status": "success",
  "result": {
    "original_gate_count": 245000,
    "optimized_gate_count": 67000,
    "reduction_ratio": 0.727,
    "original_depth": 50000,
    "optimized_depth": 8700,
    "depth_reduction": 0.826,
    "fidelity": 0.99999999,
    "observables": {
      "cnot_count": 23400,
      "single_qubit_count": 43600,
      "t_count": 12300,
      "circuit_volume": 569520000,
      "entangling_depth": 4200
    },
    "qubit_count": 1024,
    "wall_time_ms": 567
  }
}
```

## Use Cases

1. **Quantum Compiler Backend** — Optimize circuits for specific quantum hardware architectures
2. **Fault-Tolerant Computing** — Implement surface code protocols with magic state distillation
3. **Quantum Communication** — Teleportation-based quantum networking and repeater protocols
4. **Algorithm Development** — Rapid prototyping and testing of new quantum algorithms
5. **Hardware Calibration** — Gate characterization and randomized benchmarking circuits
6. **Quantum Memory** — Error correction for quantum data storage and retrieval
7. **Cross-Platform Compilation** — Translate circuits between different quantum instruction sets

---

## Input Method

### API Endpoint
```
POST http://localhost:8080/api/v1/quantum/execute
```

### Request Format
```json
{
  "problem": "gate_synthesis",
  "config": {
    "num_qubits": 1024,
    "optimizer": "SPSA",
    "max_iterations": 100
  },
  "input_data": [0.785, 1.571, 0.0, "...Born-normalized floats..."]
}
```

### Supported Problem Types
- `"gate_synthesis"` — Decompose arbitrary unitaries into native gate sets
- `"circuit_optimization"` — Minimize gate count and circuit depth

### Data Input Options
- **Direct API**: Send JSON payload with amplitudes (Born-normalized floats)
- **File Import**: Upload binary/CSV data files via the import endpoint
- **Streaming**: For large datasets, use chunked streaming mode

---

## Hamiltonian Selection

### Available Hamiltonians
| Hamiltonian Type | Description | Use Case |
|---|---|---|
| Native Gate Set (Rx, Ry, Rz, CNOT, Toffoli) | Standard quantum gates | Circuit construction and optimization |
| Custom Unitary | User-defined unitary matrix | Gate synthesis, custom algorithms |
| Clifford Group | Stabilizer circuit operations | Error correction encoding/decoding |
| Parameterized Gates | Rotation gates with continuous parameters | Variational circuits |

### Configuration
```json
{
  "hamiltonian": {
    "type": "native_gate_set",
    "parameters": {
      "gate_set": ["h", "cnot", "rz", "rx", "t", "tdg"],
      "topology": "all_to_all",
      "optimization_level": 3
    }
  }
}
```

### Encoding Options
- **Jordan-Wigner**: Fermion-to-qubit mapping for fermionic circuits
- **Bravyi-Kitaev**: Reduced gate depth for large circuits
- **Direct Encoding**: Native gate-level circuit representation

---

## Supported Scale

| Parameter | Maximum Value |
|---|---|
| **Qubits** | 2^53 (9,007,199,254,740,992) |
| **Bond Dimension** | 2^53 |
| **Precision** | IEEE 754 double (64-bit float) |

The quantum engine supports computations from small-scale (8 qubits) up to the theoretical maximum of 2^53 qubits with matching bond dimension, enabling simulation of molecular systems from simple hydrogen molecules to complex biological macromolecules and beyond.

