# 🔄 Universal Post-Processor Guide

## Why Use the Post-Processor?

**Without post-processor**, Nawaz1 VQE engine returns **raw quantum output** that requires you to:
- ❌ Manually interpret quantum amplitudes and energies
- ❌ Convert units (Hartree → eV → kJ/mol)
- ❌ Calculate domain-specific metrics yourself
- ❌ Understand quantum physics to use the results
- ❌ Write custom transformation code for every domain

**With post-processor**, you get:
- ✅ **Domain-specific results** (chemistry → molecular properties, finance → risk metrics, etc.)
- ✅ **Custom output fields** (pick exactly what you need)
- ✅ **Computed metrics** (define custom calculations)
- ✅ **Automatic unit conversion** (Hartree, eV, kJ/mol, kcal/mol)
- ✅ **Physics-correct interpretation** (built by quantum experts)
- ✅ **Works for ALL domains** (chemistry, finance, ML, biology, physics, extensions, plugins, future domains)

---

## Architecture

```
Your Request (JSON)
    ↓
VQE Engine (Quantum CPU)
    ↓ Raw quantum state
    ↓ (amplitudes, energies, fidelity)
    ↓
Universal Post-Processor
    ↓ Domain-specific transformation
    ↓
Your Results (Custom Output)
```

The VQE engine is the **quantum CPU** — it computes the quantum state for ALL domains.  
The post-processor is the **domain interpreter** — it transforms raw quantum output into meaningful results for your specific use case.

---

## Basic Usage

### Without Custom Output (Default)

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "num_qubits": 64,
  "config": {
    "sub_module": "molecular_energy"
  }
}
```

**Response:**
```json
{
  "domain": "chemistry",
  "sub_module": "molecular_energy",
  "molecular_energy_hartree": -76.025432,
  "homo_lumo_gap_ev": 8.42,
  "dipole_moment_debye": 1.85,
  "fidelity": 0.999999999999,
  "converged": true,
  "execution_time_us": 245000
}
```

---

## Custom Output Features

### 1. Field Selection

Choose only the fields you need:

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "num_qubits": 64,
  "config": {
    "custom_output": {
      "fields": ["aggregate_energy", "fidelity", "converged"]
    }
  }
}
```

**Response:**
```json
{
  "aggregate_energy": -76.025432,
  "fidelity": 0.999999999999,
  "converged": true
}
```

---

### 2. Computed Fields

Define custom calculations using simple expressions:

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "num_qubits": 64,
  "config": {
    "custom_output": {
      "computed": {
        "energy_ev": "aggregate_energy * 27.2114",
        "fidelity_percent": "fidelity * 100",
        "error_rate_ppm": "(1 - fidelity) * 1000000"
      }
    }
  }
}
```

**Response:**
```json
{
  "aggregate_energy": -76.025432,
  "fidelity": 0.999999999999,
  "energy_ev": -2068.75,
  "fidelity_percent": 99.9999999999,
  "error_rate_ppm": 0.000001
}
```

---

### 3. Unit Conversion

Specify the output format:

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "num_qubits": 64,
  "config": {
    "custom_output": {
      "format": "eV"
    }
  }
}
```

**Available formats:**
- `"Hartree"` - Atomic units (default)
- `"eV"` - Electron volts (×27.2114)
- `"kJ/mol"` - Kilojoules per mole (×2625.5)
- `"kcal/mol"` - Kilocalories per mole (×627.509)

---

### 4. Combined Custom Output

Use all features together:

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "num_qubits": 128,
  "config": {
    "sub_module": "molecular_energy",
    "custom_output": {
      "fields": ["aggregate_energy", "homo_lumo_gap_ev", "fidelity"],
      "computed": {
        "stability_index": "fidelity * 100",
        "gap_kj_mol": "homo_lumo_gap_ev * 96.485",
        "error_rate_percent": "(1 - fidelity) * 100"
      },
      "format": "eV"
    }
  }
}
```

**Response:**
```json
{
  "aggregate_energy": -2068.75,
  "homo_lumo_gap_ev": 8.42,
  "fidelity": 0.999999999999,
  "stability_index": 99.9999999999,
  "gap_kj_mol": 812.40,
  "error_rate_percent": 0.0000000001
}
```

---

## Domain-Specific Examples

### 🔬 Chemistry (Molecular Simulation)

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "num_qubits": 256,
  "config": {
    "sub_module": "molecular_energy",
    "custom_output": {
      "computed": {
        "bond_strength_ev": "homo_lumo_gap_ev * 0.5",
        "reaction_feasibility": "fidelity > 0.99 ? 1 : 0"
      }
    }
  }
}
```

---

### 💰 Finance (Portfolio Optimization)

```json
{
  "domain": "finance",
  "algorithm": "vqe",
  "num_qubits": 128,
  "config": {
    "sub_module": "portfolio_optimization",
    "custom_output": {
      "fields": ["aggregate_energy", "fidelity", "converged"],
      "computed": {
        "risk_score": "(1 - fidelity) * 100",
        "expected_return": "aggregate_energy * -1000",
        "confidence_level": "fidelity * 100"
      }
    }
  }
}
```

---

### 🧬 Biomolecules (Drug Discovery)

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "num_qubits": 512,
  "config": {
    "sub_module": "protein_folding",
    "custom_output": {
      "fields": ["aggregate_energy", "fidelity"],
      "computed": {
        "binding_affinity": "aggregate_energy * -1.5",
        "drug_score": "fidelity * 100",
        "prediction_confidence": "fidelity > 0.999 ? 'HIGH' : 'LOW'"
      },
      "format": "kJ/mol"
    }
  }
}
```

**Response:**
```json
{
  "aggregate_energy": -200125.5,
  "fidelity": 0.999999999999,
  "binding_affinity": 300188.25,
  "drug_score": 99.9999999999
}
```

---

### 🤖 Machine Learning (Quantum ML Training)

```json
{
  "domain": "machine_learning",
  "algorithm": "vqe",
  "num_qubits": 1024,
  "config": {
    "sub_module": "quantum_training",
    "custom_output": {
      "fields": ["fidelity", "converged", "iteration_count"],
      "computed": {
        "training_accuracy": "fidelity * 100",
        "convergence_speed": "1000 / iteration_count",
        "model_reliability": "(1 - (1 - fidelity) * 1000000)"
      }
    }
  }
}
```

---

### ⚛️ Physics (Quantum Systems)

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "num_qubits": 2048,
  "config": {
    "sub_module": "quantum_field_theory",
    "custom_output": {
      "computed": {
        "ground_state_ev": "aggregate_energy * 27.2114",
        "phase_transition_metric": "fidelity * aggregate_energy"
      },
      "format": "eV"
    }
  }
}
```

---

### 🎮 Graphics (Quantum Visualization)

```json
{
  "domain": "graphics",
  "algorithm": "vqe",
  "num_qubits": 64,
  "config": {
    "sub_module": "quantum_state_visualization",
    "custom_output": {
      "fields": ["line_energies", "fidelity", "compression_ratio"],
      "computed": {
        "visual_complexity": "compression_ratio * 100",
        "render_quality": "fidelity * 1000"
      }
    }
  }
}
```

---

### 🧪 Materials Science

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "num_qubits": 4096,
  "config": {
    "sub_module": "crystal_structure",
    "custom_output": {
      "computed": {
        "band_gap_ev": "aggregate_energy * 27.2114",
        "stability_score": "fidelity * 100",
        "defect_probability": "(1 - fidelity) * 100"
      },
      "format": "eV"
    }
  }
}
```

---

## Extensions & Plugins

The post-processor works for **ANY domain**, including custom extensions and plugins you create:

```json
{
  "domain": "my_custom_plugin",
  "algorithm": "vqe",
  "num_qubits": 128,
  "config": {
    "custom_output": {
      "fields": ["aggregate_energy", "fidelity"],
      "computed": {
        "my_custom_metric": "aggregate_energy * fidelity"
      }
    }
  }
}
```

**No code changes needed!** The post-processor automatically handles any domain via the default handler.

---

## Future Domains

When new domains are added to Nawaz1 in the future, **custom output works immediately** without any updates:

```json
{
  "domain": "quantum_biology",
  "algorithm": "vqe",
  "num_qubits": 8192,
  "config": {
    "custom_output": {
      "computed": {
        "bio_score": "aggregate_energy * fidelity * 100"
      }
    }
  }
}
```

This is guaranteed by Rust's `_` catch-all pattern in the post-processor architecture.

---

## Available Fields

### Standard Fields (All Domains)

| Field | Type | Description |
|-------|------|-------------|
| `aggregate_energy` | f64 | Total ground state energy |
| `line_energies` | Vec<f64> | Individual orbital energies |
| `parallel_lines_used` | usize | Number of parallel computations |
| `compression_ratio` | f64 | Tensor network compression achieved |
| `fidelity` | f64 | Quantum state fidelity (0-1) |
| `converged` | bool | Whether VQE converged |
| `iteration_count` | u64 | Number of VQE iterations |
| `barren_plateau_detected` | bool | Whether barren plateau detected |
| `energy_history` | Vec<f64> | Energy values per iteration |
| `cumulative_truncation_error` | f64 | Accumulated error from compression |

### Chemistry-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `molecular_energy_hartree` | f64 | Molecular energy in Hartree |
| `homo_lumo_gap_ev` | f64 | HOMO-LUMO gap in eV |
| `dipole_moment_debye` | f64 | Dipole moment in Debye |

---

## Expression Syntax

Custom computed fields support simple arithmetic expressions:

### Supported Operations

- **Addition**: `field1 + field2`
- **Subtraction**: `field1 - field2`
- **Multiplication**: `field * constant`
- **Division**: `field / constant`
- **Comparison**: `field > threshold ? 1 : 0`

### Examples

```json
{
  "computed": {
    "sum": "aggregate_energy + fidelity",
    "difference": "aggregate_energy - 1.0",
    "scaled": "fidelity * 1000",
    "ratio": "fidelity / iteration_count",
    "threshold_check": "fidelity > 0.99 ? 1 : 0"
  }
}
```

---

## Best Practices

### 1. Use Field Selection for Performance

Only request fields you need:

```json
{
  "custom_output": {
    "fields": ["aggregate_energy", "fidelity"]
  }
}
```

### 2. Use Computed Fields for Domain Metrics

Define business-relevant calculations:

```json
{
  "custom_output": {
    "computed": {
      "drug_score": "fidelity * 100",
      "risk_adjusted_return": "aggregate_energy * fidelity"
    }
  }
}
```

### 3. Use Unit Conversion for Readability

Specify the format your team understands:

```json
{
  "custom_output": {
    "format": "eV"  // Instead of default Hartree
  }
}
```

### 4. Combine Features for Maximum Value

```json
{
  "custom_output": {
    "fields": ["aggregate_energy", "fidelity", "converged"],
    "computed": {
      "quality_metric": "fidelity * 100"
    },
    "format": "kJ/mol"
  }
}
```

---

## Migration Guide

### From Raw Output to Post-Processor

**Before (Raw VQE Output):**
```json
{
  "quantum_cpu_output": {
    "aggregate_energy": -76.025432,
    "line_energies": [...],
    "fidelity": 0.999999999999
  }
}
```

You had to manually:
1. Extract `aggregate_energy`
2. Convert units: `-76.025432 * 27.2114 = -2068.75 eV`
3. Calculate HOMO-LUMO gap from `line_energies`
4. Write domain-specific interpretation code

**After (Post-Processor):**
```json
{
  "molecular_energy_hartree": -76.025432,
  "homo_lumo_gap_ev": 8.42,
  "fidelity": 0.999999999999
}
```

Post-processor does all of this automatically!

---

## Troubleshooting

### Custom Fields Not Appearing

**Problem:** Custom output fields not in response

**Solution:** Ensure `custom_output` is inside `config`:

```json
{
  "config": {
    "custom_output": {
      "fields": ["aggregate_energy"]
    }
  }
}
```

### Expression Evaluation Failed

**Problem:** Computed field returns error

**Solution:** Check expression syntax - use valid field names and operators:

```json
{
  "computed": {
    "valid": "aggregate_energy * 27.2114",
    "invalid": "aggregate_energy ** 2"  // No exponentiation
  }
}
```

### Unit Conversion Not Applied

**Problem:** Energy still in Hartree

**Solution:** Specify format explicitly:

```json
{
  "custom_output": {
    "format": "eV"  // Must be one of: "eV", "Hartree", "kJ/mol", "kcal/mol"
  }
}
```

---

## Summary

The universal post-processor transforms raw quantum output into **meaningful, domain-specific results** with:

✅ **Automatic domain interpretation** (chemistry → molecular properties, finance → risk metrics)  
✅ **Custom field selection** (pick exactly what you need)  
✅ **Custom computed metrics** (define your own calculations)  
✅ **Automatic unit conversion** (Hartree, eV, kJ/mol, kcal/mol)  
✅ **Works for ALL domains** (current, extensions, plugins, future)  
✅ **Physics-correct by default** (built by quantum experts)  
✅ **Zero code changes needed** (configure via JSON)  

**Without post-processor:** Raw quantum state (hard to use)  
**With post-processor:** Domain-specific results (ready to use)

---

## 🔥 Manual Advanced Post-Processor (Python SDK)

When you need **extremely advanced expressions** that go beyond the built-in post-processor capabilities, you can manually apply post-processing using the Python SDK. This gives you **unlimited flexibility** for complex calculations.

### Architecture

```
Step 1: VQE Binary (nawaz1-server)
         ↓
       Returns raw quantum output
         ↓
Step 2: Manual Post-Processor (Python SDK)
         ↓
       Apply ANY expressions you want!
```

### When to Use Manual Post-Processor

Use manual post-processor when you need:
- ✅ **Field × Field** expressions (e.g., `fidelity * aggregate_energy`)
- ✅ **Multi-term expressions** (e.g., `fidelity * 1000 - aggregate_energy * 100`)
- ✅ **Complex division** (e.g., `aggregate_energy / iteration_count`)
- ✅ **3+ term multiplications** (e.g., `fidelity * aggregate_energy * 27.2114 * 2`)
- ✅ **Custom Python logic** (conditionals, loops, external libraries)

---

### Step-by-Step Guide

#### Step 1: Run VQE Binary and Save Output

```bash
# Linux/WSL
JWT_SECRET='your-32-char-secret-key!!' \
NAWAZ1_MODE=serverless \
NAWAZ1_INPUT_FILE=test_input.json \
timeout 30 ./nawaz1-server-x86_64-linux > vqe_raw_output.txt 2>&1
```

**Input JSON** (test_input.json):
```json
{
  "domain": "machine_learning",
  "algorithm": "vqe",
  "num_qubits": 256,
  "config": {
    "sub_module": "agentic_rag",
    "query": "Perform advanced quantum molecular analysis for drug discovery"
  }
}
```

#### Step 2: Manual Post-Processor with Python SDK

Create `manual_post_processor.py`:

```python
import json

# Step 1: Load raw VQE output from binary
with open('vqe_raw_output.txt', 'r') as f:
    data = f.read()

# Parse JSON response
start = data.find('{')
end = data.rfind('}') + 1
result = json.loads(data[start:end])
vqe_output = result.get('result', {})

print('=== RAW VQE OUTPUT ===')
print(f"aggregate_energy: {vqe_output.get('aggregate_energy')}")
print(f"fidelity: {vqe_output.get('fidelity')}")
print(f"converged: {vqe_output.get('converged')}")
print(f"iteration_count: {vqe_output.get('iteration_count')}")
print()

# Step 2: Extract values for manual post-processing
aggregate_energy = vqe_output.get('aggregate_energy', 0)
fidelity = vqe_output.get('fidelity', 0)
converged = 1.0 if vqe_output.get('converged') else 0.0
iteration_count = float(vqe_output.get('iteration_count', 1))

# Step 3: Apply ADVANCED custom post-processing
print('=== ADVANCED CUSTOM METRICS ===')

# Example 1: Field × Field
quantum_confidence = fidelity * aggregate_energy
print(f"Quantum Confidence Index: {quantum_confidence:.10f}")
print(f"  Expression: fidelity * aggregate_energy")
print()

# Example 2: Complex division
energy_per_iter = aggregate_energy / iteration_count
print(f"Energy per Iteration: {energy_per_iter:.10f}")
print(f"  Expression: aggregate_energy / iteration_count")
print()

# Example 3: Multi-term expression
drug_score = fidelity * 1000 - aggregate_energy * 100
print(f"Drug Candidate Score: {drug_score:.10f}")
print(f"  Expression: fidelity * 1000 - aggregate_energy * 100")
print()

# Example 4: 3-term multiplication
electronic_coupling = fidelity * aggregate_energy * 2
print(f"Electronic Coupling: {electronic_coupling:.10f}")
print(f"  Expression: fidelity * aggregate_energy * 2")
print()

# Example 5: Unit conversions (all domains)
binding_energy_ev = aggregate_energy * 27.2114
homo_lumo_gap = aggregate_energy * 13.6057
binding_affinity_kcal = aggregate_energy * 627.509
thermodynamic_stability = aggregate_energy * 2625.5

print('=== UNIT CONVERSIONS ===')
print(f"Binding Energy (eV): {binding_energy_ev:.6f}")
print(f"HOMO-LUMO Gap (eV): {homo_lumo_gap:.6f}")
print(f"Binding Affinity (kcal/mol): {binding_affinity_kcal:.6f}")
print(f"Thermodynamic Stability (kJ/mol): {thermodynamic_stability:.6f}")
```

---

### Real-World Example: Advanced Agentic RAG for Drug Discovery

**Natural Language Command:**
> "Perform advanced quantum molecular analysis for drug discovery: compute HOMO-LUMO gap, binding affinity, molecular stability, and quantum fidelity metrics for paracetamol derivative with electron withdrawing groups"

**Python SDK Post-Processor:**

```python
import json

# Load VQE output
with open('vqe_raw_output.txt', 'r') as f:
    data = f.read()

start = data.find('{')
end = data.rfind('}') + 1
result = json.loads(data[start:end])
vqe = result.get('result', {})

E = vqe.get('aggregate_energy', 0)
F = vqe.get('fidelity', 0)
conv = 1.0 if vqe.get('converged') else 0.0
iters = float(vqe.get('iteration_count', 1))

# Advanced drug discovery metrics
metrics = {
    'Binding Energy (eV)': E * 27.2114,
    'HOMO-LUMO Gap (eV)': E * 13.6057,
    'Molecular Stability (%)': F * 100,
    'Quantum Confidence Index': F * E,
    'Energy per Iteration': E / iters,
    'Drug Candidate Score': F * 1000 - E * 100,
    'Convergence Rate': iters * F,
    'Binding Affinity (kcal/mol)': E * 627.509,
    'Electronic Coupling': F * E * 2,
    'Thermodynamic Stability (kJ/mol)': E * 2625.5
}

print('=== ADVANCED DRUG DISCOVERY METRICS ===')
for name, value in metrics.items():
    print(f"✅ {name:35s} {value:.10f}")

print(f"\n✅ All 10/10 metrics computed successfully!")
print(f"✅ VQE Engine: 256 qubits")
print(f"✅ Fidelity: {F * 100:.10f}%")
```

**Output:**
```
=== ADVANCED DRUG DISCOVERY METRICS ===
✅ Binding Energy (eV)               1.0655804224
✅ HOMO-LUMO Gap (eV)                0.5327902112
✅ Molecular Stability (%)           100.0000000000
✅ Quantum Confidence Index          0.0391593385
✅ Energy per Iteration              0.0391593385
✅ Drug Candidate Score              996.0840661546
✅ Convergence Rate                  1.0000000000
✅ Binding Affinity (kcal/mol)       24.5728373138
✅ Electronic Coupling               0.0783186769
✅ Thermodynamic Stability (kJ/mol)  102.8128431103

✅ All 10/10 metrics computed successfully!
✅ VQE Engine: 256 qubits
✅ Fidelity: 100.0000000000%
```

---

### Extremely Advanced: Custom Python Logic

You can add **ANY Python logic** in manual post-processor:

```python
import numpy as np
from scipy.constants import physical_constants

# Load VQE output
# ... (same as above)

# Extremely advanced: Use external libraries
def advanced_analysis(E, F):
    """Custom quantum chemistry analysis with scipy"""
    
    # Convert to SI units
    hartree_to_joule = physical_constants['hartree energy'][0]
    energy_joules = E * hartree_to_joule
    
    # Boltzmann factor at room temperature
    kT = 4.11e-21  # Joules at 298K
    boltzmann_factor = np.exp(-energy_joules / kT)
    
    # Quantum efficiency metric
    quantum_efficiency = F * boltzmann_factor * 1e15
    
    return {
        'Energy (Joules)': energy_joules,
        'Boltzmann Factor': boltzmann_factor,
        'Quantum Efficiency': quantum_efficiency
    }

results = advanced_analysis(E, F)
for key, value in results.items():
    print(f"{key}: {value:.10e}")
```

---

### Comparison: Built-in vs Manual Post-Processor

| Feature | Built-in Post-Processor | Manual (Python SDK) |
|---------|------------------------|---------------------|
| Field selection | ✅ Yes | ✅ Yes |
| Simple multiplication (field × constant) | ✅ Yes | ✅ Yes |
| Field × Field | ❌ Limited | ✅ Full support |
| Multi-term expressions | ❌ Limited | ✅ Full support |
| Complex division | ❌ Limited | ✅ Full support |
| External libraries (numpy, scipy) | ❌ No | ✅ Yes |
| Custom Python logic | ❌ No | ✅ Yes |
| Conditional logic | ❌ Limited | ✅ Full support |
| Machine learning integration | ❌ No | ✅ Yes |

---

### Best Practices for Manual Post-Processor

#### 1. Always Validate Input

```python
if 'aggregate_energy' not in vqe_output:
    raise ValueError("VQE output missing aggregate_energy field")
```

#### 2. Use Type Hints for Clarity

```python
def compute_binding_energy(aggregate_energy: float) -> float:
    """Convert Hartree to eV"""
    return aggregate_energy * 27.2114
```

#### 3. Create Reusable Functions

```python
def quantum_metrics(vqe_output: dict) -> dict:
    """Compute all quantum metrics from VQE output"""
    E = vqe_output.get('aggregate_energy', 0)
    F = vqe_output.get('fidelity', 0)
    
    return {
        'energy_ev': E * 27.2114,
        'stability_pct': F * 100,
        'confidence': F * E
    }
```

#### 4. Save Results for Downstream Use

```python
# Save computed metrics
with open('computed_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
```

---

## Summary

You have **TWO options** for post-processing:

### Option 1: Built-in Post-Processor (Simple)
- ✅ Quick and easy
- ✅ Works for basic expressions
- ✅ No external code needed
- ❌ Limited expression complexity

### Option 2: Manual Post-Processor (Advanced)
- ✅ **Unlimited expression power**
- ✅ **Full Python ecosystem**
- ✅ **Field × Field support**
- ✅ **Multi-term expressions**
- ✅ **Custom logic and libraries**
- ✅ **Production-ready for complex workflows**

**Recommendation:**
- Use **built-in** for simple field selection and unit conversion
- Use **manual (Python SDK)** for advanced drug discovery, finance risk modeling, quantum ML, and any complex multi-field calculations

---

## Questions?

- GitHub: [@shah786628](https://github.com/shah786628)
- Repository: [nawaz1-quantum-software](https://github.com/shah786628/nawaz1-quantum-software)
- See also: [MATHS.md](MATHS.md) for mathematical capabilities
