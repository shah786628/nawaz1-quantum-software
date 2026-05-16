# Quantum Machine Learning Package

## Overview

The Machine Learning package provides quantum-native neural networks, kernel methods, and classification algorithms through the unified L3 VQE circuit at 65536-qubit scale. It enables quantum neural networks (QNN), physics-informed neural networks (QPINN), quantum kernel evaluation, and feature map encoding — all executed via the Algorithm Bridge on 7 tensor network experts in unconditional superposition.

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

- **Qubits:** 65536
- **Feature dimension:** Up to 65536 input features
- **Training data:** Amplitude-encoded datasets of arbitrary size
- **Bond dimension:** Adaptive χ = ln(Q) per geometry
- **Tensor experts:** MPS/PEPS/PEPS3D/MERA/TTN/LoopTTN/PepsND in superposition

## Input Data Format

The input data array encodes the ML problem as 65536 floating-point amplitudes representing the quantum-encoded dataset or model parameters.

```json
{
  "domain": "machine_learning",
  "algorithm": "qnn",
  "input_data": [/* 65536 float values: amplitude-encoded training data */],
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
    "input_data": [0.032, -0.015, 0.047, ... /* 65536 feature amplitudes */],
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

# Encode dataset as 65536-dimensional quantum feature vector
features = np.random.randn(65536)
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
    "tensor_expert_used": "TTN",
    "qubit_count": 65536,
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
