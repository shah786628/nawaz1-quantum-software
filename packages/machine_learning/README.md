# Quantum Machine Learning Package

## Overview

The Machine Learning package provides quantum-native neural networks, kernel methods, and classification algorithms through the unified VQE engine at 2^53-qubit scale. It enables quantum neural networks (QNN), physics-informed neural networks (QPINN), quantum kernel evaluation, and feature map encoding.

## Key Features

- **Quantum Neural Networks (QNN)** — parameterized circuits as trainable quantum models
- **Quantum PINN** — physics-informed quantum networks for PDE-constrained learning
- **Quantum kernels** — exponentially large feature spaces for classification
- **Quantum feature maps** — amplitude, angle, and IQP encoding of classical data
- **Quantum classifiers** — binary and multi-class quantum classification
- **Quantum generative models** — quantum GANs and Born machines
- **Quantum reservoir computing** — temporal pattern recognition
- **Quantum transfer learning** — hybrid classical-quantum model architectures

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **QNN** | Quantum Neural Network training and inference |
| **QPINN** | Physics-Informed Quantum Neural Networks for PDEs |
| **Quantum Kernel** | Kernel-based classification in quantum feature space |
| **VQE** | Variational optimization of quantum ML models |
| **QAOA** | Combinatorial optimization for ML hyperparameters |
| **Grover** | Quantum-enhanced data search and filtering |

## Scale

- **Qubits:** Up to 2^53 (9,007,199,254,740,992)
- **Feature dimension:** Up to 2^53 input features
- **Training data:** Amplitude-encoded datasets of arbitrary size

## Input Data Format

The input data array encodes the ML problem as N floating-point amplitudes (up to 2^53) representing the quantum-encoded dataset or model parameters.

```json
{
  "domain": "machine_learning",
  "algorithm": "qnn",
  "input_data": [/* N float values: amplitude-encoded training data (up to 2^53) */],
  "config": {
    "task": "classification",
    "num_classes": 10,
    "layers": 6,
    "entanglement": "full",
    "optimizer": "adam",
    "learning_rate": 0.01
  }
}
```

**Input encoding:**
- Amplitudes represent the normalized feature vector of input data
- Multiple samples can be batch-encoded using amplitude superposition
- Labels encoded separately in config or as part of the amplitude structure

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "machine_learning",
    "algorithm": "qnn",
    "input_data": [0.032, -0.015, 0.047, ... /* N feature amplitudes (up to 2^53) */],
    "config": {
      "task": "classification",
      "num_classes": 10,
      "layers": 8,
      "entanglement": "circular",
      "optimizer": "adam",
      "learning_rate": 0.001,
      "epochs": 100
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Encode dataset as quantum feature vector (up to 2^53 dimensions)
features = np.random.randn(1024)  # Example; engine supports up to 2^53
amplitudes = (features / np.linalg.norm(features)).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "machine_learning",
        "algorithm": "qnn",
        "input_data": amplitudes,
        "config": {
            "task": "classification",
            "num_classes": 5,
            "layers": 6,
            "entanglement": "full",
            "optimizer": "adam",
            "learning_rate": 0.01
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
    "predictions": [0.92, 0.03, 0.01, 0.02, 0.02],
    "predicted_class": 0,
    "confidence": 0.92,
    "training_loss": 0.0234,
    "accuracy": 0.9847,
    "observables": {
      "kernel_alignment": 0.89,
      "expressibility": 0.95,
      "entangling_capability": 0.87,
      "effective_dimension": 4521
    },
    "qubit_count": 1024,
    "wall_time_ms": 1893
  }
}
```

## Use Cases

1. **Medical Imaging** — Quantum-enhanced classification of MRI/CT scans with exponential feature spaces
2. **Natural Language Processing** — Quantum embedding of text for semantic similarity and classification
3. **Anomaly Detection** — Quantum kernel methods for detecting rare events in high-dimensional data
4. **Drug Response Prediction** — QPINN models for predicting patient-specific drug efficacy
5. **Climate Modeling** — Physics-informed quantum networks for weather and climate prediction
6. **Financial Forecasting** — Quantum generative models for market regime classification
7. **Materials Discovery** — Quantum ML for predicting material properties from atomic structure

---

## Input Method

### API Endpoint
```
POST http://localhost:8080/api/v1/quantum/execute
```

### Request Format
```json
{
  "problem": "quantum_classification",
  "config": {
    "num_qubits": 1024,
    "optimizer": "SPSA",
    "max_iterations": 100
  },
  "input_data": [0.032, -0.015, 0.047, "...Born-normalized floats..."]
}
```

### Supported Problem Types
- `"quantum_classification"` — Binary and multi-class quantum classification
- `"kernel_estimation"` — Quantum kernel evaluation in exponential feature spaces

### Data Input Options
- **Direct API**: Send JSON payload with amplitudes (Born-normalized floats)
- **File Import**: Upload binary/CSV data files via the import endpoint
- **Streaming**: For large datasets, use chunked streaming mode

---

## Hamiltonian Selection

### Available Hamiltonians
| Hamiltonian Type | Description | Use Case |
|---|---|---|
| Quantum Kernel | Exponential feature space inner products | Classification, regression |
| Variational Classifier | Parameterized quantum circuit model | Multi-class classification |
| Quantum Neural Network | Layered parameterized ansatz | Deep quantum learning |
| Physics-Informed (QPINN) | PDE-constrained quantum network | Scientific ML |

### Configuration
```json
{
  "hamiltonian": {
    "type": "quantum_kernel",
    "parameters": {
      "feature_map": "iqp",
      "entanglement": "full",
      "reps": 2,
      "num_classes": 10
    }
  }
}
```

### Encoding Options
- **Jordan-Wigner**: For physics-informed quantum ML models
- **Bravyi-Kitaev**: Reduced gate depth for large feature spaces
- **Direct Encoding**: For amplitude-encoded data (default for ML)

---

## Supported Scale

| Parameter | Maximum Value |
|---|---|
| **Qubits** | 2^53 (9,007,199,254,740,992) |
| **Bond Dimension** | 2^53 |
| **Precision** | IEEE 754 double (64-bit float) |

The quantum engine supports computations from small-scale (8 qubits) up to the theoretical maximum of 2^53 qubits with matching bond dimension, enabling simulation of molecular systems from simple hydrogen molecules to complex biological macromolecules and beyond.

