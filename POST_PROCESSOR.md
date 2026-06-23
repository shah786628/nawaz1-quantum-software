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

## Questions?

- GitHub: [@shah786628](https://github.com/shah786628)
- Repository: [nawaz1-quantum-software](https://github.com/shah786628/nawaz1-quantum-software)
- See also: [MATHS.md](MATHS.md) for mathematical capabilities
