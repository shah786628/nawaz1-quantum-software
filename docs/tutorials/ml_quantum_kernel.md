# Tutorial: Quantum Kernel Classification

Use quantum kernel methods to classify data in an exponentially large quantum feature space. Quantum kernels can find patterns that classical kernels (RBF, polynomial) cannot efficiently represent.

**Time required:** 5 minutes
**Difficulty:** Beginner

---

## Prerequisites

- Nawaz1 server running on `http://localhost:8080` (see [Quick Start](../QUICKSTART.md))
- Python 3.8+ with `requests` and `numpy` installed

```bash
pip install requests numpy
```

---

> **Important:** Before using the engine, remember:
> 1. **Correct Hamiltonian** — Feature vectors must be normalized (unit vectors) before encoding as quantum amplitudes. Unnormalized data will produce incorrect quantum states.
> 2. **Correct Algorithm** — This tutorial uses `vqe` for kernel evaluation and `qnn` for neural network classification. Do NOT use `hhl` or `grover` for ML classification.
> 3. **Qubits = Power of 2** — The `qubits` field must be a power of 2: `4`, `8`, `16`, `32`, `64`, `128`, `256`, etc. Match it to your feature dimension (rounded up to the next power of 2).
> 4. **Read the Input Data Guide** — See [VQE Input Data Guide](../../VQE_INPUT_DATA_GUIDE.md) for correct `problem` field formats.

## What We're Computing

A quantum kernel maps classical data into a quantum feature space using a parameterized quantum circuit, then measures the overlap (inner product) between pairs of encoded states. This overlap becomes the kernel matrix entry used by a classifier (SVM or nearest-centroid).

The advantage: quantum feature spaces can be exponentially large (2^Q dimensions for Q qubits), making certain class boundaries linearly separable that are not in classical space.

---

## Step 1 — Binary Classification (4 features, 2 classes)

Encode a small dataset as quantum amplitudes and run classification:

```python
import requests
import numpy as np

# 8 samples, 4 features each (normalized to unit vectors)
# Class 0: clustered around [1,0,0,0]
# Class 1: clustered around [0,0,0,1]
rng = np.random.RandomState(42)

X_class0 = rng.normal(loc=[1, 0, 0, 0], scale=0.1, size=(4, 4))
X_class1 = rng.normal(loc=[0, 0, 0, 1], scale=0.1, size=(4, 4))
X = np.vstack([X_class0, X_class1])

# Normalize each sample to unit vector (required for amplitude encoding)
X = X / np.linalg.norm(X, axis=1, keepdims=True)

# Flatten all samples into a single amplitude array
amplitudes = X.flatten().tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "machine_learning",
        "algorithm": "vqe",
        "qubits": 4,
        "problem": {
            "orbital_energies": amplitudes
        }
    }
)

result = response.json()
print(f"Status:       {result['status']}")
print(f"Qubits:       {result['num_qubits_simulated']}")
print(f"Energy:       {result['result']['aggregate_energy']:.6f}")
print(f"Fidelity:     {result['result']['fidelity']:.15f}")
print(f"Converged:    {result['result']['converged']}")
```

---

## Step 2 — Quantum Neural Network Classifier

Use the QNN (Quantum Neural Network) algorithm for a trainable classifier:

```python
import requests
import numpy as np

rng = np.random.RandomState(42)

# Generate 64 training samples with 8 features
n_samples, n_features = 64, 8
X = rng.normal(0, 1, (n_samples, n_features))
X = X / np.linalg.norm(X, axis=1, keepdims=True)

# Flatten to amplitude array
amplitudes = X.flatten().tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "machine_learning",
        "algorithm": "qnn",
        "qubits": 8,
        "problem": {
            "orbital_energies": amplitudes
        }
    }
)

result = response.json()
print(f"Status:       {result['status']}")
print(f"Qubits:       {result['num_qubits_simulated']}")
print(f"Energy:       {result['result']['aggregate_energy']:.6f}")
print(f"Converged:    {result['result']['converged']}")
```

The QNN algorithm trains a parameterized quantum circuit as a neural network, using the VQE engine's variational optimization to minimize classification loss.

---

## Step 3 — Quantum Kernel Evaluation

Compute the kernel matrix directly by encoding feature vectors as quantum states and measuring their overlap:

```python
import requests
import numpy as np

# Two feature vectors to compare
vec_a = np.array([0.5, 0.5, 0.5, 0.5])       # Normalized
vec_b = np.array([0.7, 0.1, 0.1, 0.7])       # Normalized
vec_a = vec_a / np.linalg.norm(vec_a)
vec_b = vec_b / np.linalg.norm(vec_b)

# Compute kernel entry K(a,b) by encoding both vectors
# The energy of the combined system reflects the quantum kernel overlap
combined = np.concatenate([vec_a, vec_b]).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "machine_learning",
        "algorithm": "vqe",
        "qubits": 4,
        "problem": {
            "orbital_energies": combined
        }
    }
)

result = response.json()
kernel_value = result['result']['aggregate_energy']
print(f"Quantum kernel K(a,b) = {kernel_value:.6f}")
print(f"Fidelity:              {result['result']['fidelity']:.15f}")
```

A more negative kernel value indicates greater similarity in the quantum feature space.

---

## Step 4 — Scale Up: 65,536-Feature Quantum Kernel

The streaming model handles high-dimensional feature spaces:

```python
import requests
import numpy as np

# 65536-dimensional feature vector (amplitude-encoded)
rng = np.random.RandomState(42)
features = rng.normal(0, 1, 65536)
features = features / np.linalg.norm(features)

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "machine_learning",
        "algorithm": "vqe",
        "qubits": 65536,
        "problem": {
            "orbital_energies": features.tolist()
        }
    }
)

result = response.json()
print(f"Qubits:  {result['num_qubits_simulated']}")
print(f"Energy:  {result['result']['aggregate_energy']:.6f}")
print(f"Memory:  constant ~2 MB (streaming)")
```

This encodes a 65,536-dimensional feature vector in 65,536 qubits using ~2 MB of active memory.

---

## Step 5 — Using curl

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "machine_learning",
    "algorithm": "qnn",
    "qubits": 8,
    "problem": {
      "orbital_energies": [0.35, -0.15, 0.47, -0.22, 0.18, -0.31, 0.42, -0.09]
    }
  }'
```

---

## Understanding the Output

| Field | Meaning |
|-------|---------|
| `aggregate_energy` | Loss function value — lower = better classification |
| `fidelity` | Quality of the quantum state preparation. Above 0.999 = high quality |
| `converged` | Whether the QNN training converged to a stable classifier |

### Quantum vs. Classical Kernels

| Aspect | Classical RBF Kernel | Quantum Kernel |
|--------|--------------------| ---------------|
| Feature space dimension | Same as input | 2^Q (exponentially large) |
| Expressive power | Limited to input space | Can capture entangled patterns |
| Memory scaling | O(N^2) for kernel matrix | O(1) via streaming |

---

## What to Try Next

- Compare quantum kernel accuracy against scikit-learn's SVM with RBF kernel
- Try different entanglement structures (`"entanglement": "circular"` in config)
- Use QAOA to optimize feature selection before classification
- Go back to [Chemistry: H2O tutorial](chemistry_h2o.md) or [Finance: QAOA tutorial](finance_qaoa.md)

---

## Full Reference

- [Machine Learning Package README](../../packages/machine_learning/README.md) — QNN, QPINN, kernels, feature maps
- [All Algorithms Guide](../../ALL_ALGORITHMS_INPUT_METHODS.md) — 108 algorithms documented
- [VQE Input Data Guide](../../VQE_INPUT_DATA_GUIDE.md) — input format specification
