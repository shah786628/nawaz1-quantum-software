# Quantum Biology Package

## Overview

The Biology package provides quantum simulation of biological systems through the unified L3 VQE circuit at 65536-qubit scale. It enables genomics analysis, protein structure prediction, cell simulation, and biomolecular dynamics at atomic resolution — all executed via the Algorithm Bridge on 7 tensor network experts in unconditional superposition.

## Key Features

- **Protein folding** — quantum energy landscape exploration for tertiary structure prediction
- **Genomic analysis** — sequence alignment and variant calling with quantum speedup
- **Biomolecular dynamics** — full quantum treatment of enzyme catalysis and binding
- **Cell simulation** — multi-scale modeling from molecular to cellular level
- **Drug-target interaction** — quantum-accurate binding free energy calculations
- **Photosynthesis modeling** — quantum coherence in biological light harvesting
- **Neural signaling** — ion channel dynamics and neurotransmitter interactions
- **Evolutionary dynamics** — quantum-enhanced phylogenetic analysis

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **VQE** | Ground state of biomolecular Hamiltonians |
| **ADAPT-VQE** | Adaptive ansatz for complex biological systems |
| **Quantum Monte Carlo** | Sampling conformational ensembles |
| **QITE** | Thermal equilibrium of biological systems |
| **QPE** | Precise energy estimation for binding affinity |
| **Grover** | Searching sequence/structure databases |

## Scale

- **Qubits:** 65536
- **Maximum biomolecule:** 8738 atoms (hemoglobin-scale)
- **Genome coverage:** Full chromosomal-scale analysis
- **Bond dimension:** Adaptive χ = ln(Q) per geometry
- **Tensor experts:** MPS/PEPS/PEPS3D/MERA/TTN/LoopTTN/PepsND in superposition

## Input Data Format

The input data array encodes biological system information as 65536 floating-point amplitudes representing the quantum state of the biomolecular system.

```json
{
  "domain": "biology",
  "algorithm": "vqe",
  "input_data": [/* 65536 float values: amplitude-encoded biomolecular state */],
  "config": {
    "system": "protein",
    "pdb_id": "1HBB",
    "task": "folding_energy",
    "solvent": "water",
    "temperature": 310.15
  }
}
```

**Input encoding:**
- Amplitudes represent the quantum state of atomic orbitals in the biomolecule
- Amino acid sequences can be provided in `config` for automatic encoding
- Environmental parameters (pH, temperature, ionic strength) specified in config

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "biology",
    "algorithm": "vqe",
    "input_data": [0.0012, -0.0034, 0.0021, ... /* 65536 amplitude values */],
    "config": {
      "system": "protein",
      "sequence": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
      "task": "binding_affinity",
      "ligand": "O2",
      "temperature": 310.15,
      "ph": 7.4
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Encode hemoglobin-oxygen system as quantum amplitudes
amplitudes = np.random.randn(65536).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "biology",
        "algorithm": "vqe",
        "input_data": amplitudes,
        "config": {
            "system": "protein",
            "pdb_id": "1HBB",
            "task": "folding_energy",
            "include_solvent": True,
            "temperature": 310.15
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
    "folding_energy": -1247.83,
    "unit": "kcal/mol",
    "binding_affinity": -9.2,
    "rmsd_from_native": 0.87,
    "convergence": true,
    "observables": {
      "secondary_structure": "HHHHHCCCCEEEEEHHHHHH...",
      "contact_map_density": 0.342,
      "radius_of_gyration": 24.7,
      "solvent_accessible_area": 15847.2
    },
    "tensor_expert_used": "MERA",
    "qubit_count": 65536,
    "wall_time_ms": 3421
  }
}
```

## Use Cases

1. **Drug Discovery** — Predict protein-ligand binding with quantum accuracy for lead optimization
2. **Protein Engineering** — Design novel enzymes with targeted catalytic properties
3. **Genomic Medicine** — Quantum-accelerated variant effect prediction and pharmacogenomics
4. **Vaccine Design** — Antigen-antibody interaction modeling at atomic resolution
5. **Cancer Research** — Simulate oncogene protein mutations and drug resistance mechanisms
6. **Synthetic Biology** — Design novel metabolic pathways with quantum-optimized enzyme cascades
7. **Neuroscience** — Model ion channel gating and synaptic transmission at quantum scale
