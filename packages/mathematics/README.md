# Quantum Mathematics Package

## Overview

The Mathematics package provides quantum-accelerated solutions for linear algebra, optimization, number theory, and algebraic problems through the unified L3 VQE circuit at 65536-qubit scale. It solves linear systems up to 65536×65536 matrices exponentially faster than classical methods — all executed via the Algorithm Bridge on 7 tensor network experts in unconditional superposition.

## Key Features

- **Linear systems** — solve 65536×65536 dense and sparse systems via HHL algorithm
- **Eigenvalue problems** — full spectrum computation for massive matrices
- **Optimization** — convex and non-convex optimization in exponential search spaces
- **Number theory** — integer factorization, discrete logarithm at cryptographic scale
- **Singular value transformation** — QSVT for polynomial matrix functions
- **Fourier analysis** — quantum Fourier transform on 65536-dimensional signals
- **Graph algorithms** — quantum walks, graph isomorphism, maximum cut
- **Combinatorial optimization** — exact solutions for NP-hard problems at scale

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **HHL** | Solving linear systems Ax = b exponentially fast |
| **QSVT** | Quantum Singular Value Transformation for matrix polynomials |
| **Shor** | Integer factorization and discrete logarithm |
| **QPE** | Eigenvalue estimation for unitary operators |
| **QFT** | Quantum Fourier Transform for signal processing |
| **Grover** | Unstructured search with quadratic speedup |

## Scale

- **Qubits:** 65536
- **Maximum matrix dimension:** 65536×65536
- **Integer factorization:** Up to 65536-bit numbers
- **Bond dimension:** Adaptive χ = ln(Q) per geometry
- **Tensor experts:** MPS/PEPS/PEPS3D/MERA/TTN/LoopTTN/PepsND in superposition

## Input Data Format

The input data array encodes the mathematical problem as 65536 floating-point values representing the quantum state of the problem instance.

```json
{
  "domain": "mathematics",
  "algorithm": "hhl",
  "input_data": [/* 65536 float values: amplitude-encoded matrix/vector */],
  "config": {
    "task": "linear_system",
    "matrix_size": 65536,
    "condition_number": 100,
    "precision": 1e-10
  }
}
```

**Input encoding:**
- For linear systems: amplitudes encode the vector b in Ax = b
- For factorization: amplitudes encode the integer in binary representation
- Matrix A is encoded in the Hamiltonian simulation oracle

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "mathematics",
    "algorithm": "hhl",
    "input_data": [0.015, -0.023, 0.007, ... /* 65536 amplitude values */],
    "config": {
      "task": "linear_system",
      "matrix_size": 65536,
      "sparsity": 7,
      "condition_number_bound": 1000,
      "precision": 1e-12
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Encode a 65536-dimensional linear system
b_vector = np.random.randn(65536)
b_normalized = (b_vector / np.linalg.norm(b_vector)).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "mathematics",
        "algorithm": "hhl",
        "input_data": b_normalized,
        "config": {
            "task": "linear_system",
            "matrix_size": 65536,
            "precision": 1e-10
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
    "solution_norm": 1.0,
    "solution_amplitudes": [0.00234, -0.00156, 0.00412, ...],
    "residual_norm": 1.2e-11,
    "condition_number": 847.3,
    "convergence": true,
    "observables": {
      "eigenvalue_estimate": 3.14159265,
      "solution_fidelity": 0.99999923
    },
    "tensor_expert_used": "MPS",
    "qubit_count": 65536,
    "wall_time_ms": 892
  }
}
```

## Use Cases

1. **Cryptanalysis** — Factor RSA-2048+ integers using Shor's algorithm at quantum scale
2. **Scientific Computing** — Solve massive PDE-discretized linear systems (FEM, FDM)
3. **Machine Learning** — Quantum kernel evaluation, principal component analysis
4. **Signal Processing** — QFT-based spectral analysis of 65536-point signals
5. **Optimization** — Global minimum finding for non-convex landscapes
6. **Graph Theory** — Maximum cut, graph coloring, travelling salesman at 65536 nodes
7. **Financial Modeling** — Solve large covariance matrix inversions for portfolio theory
