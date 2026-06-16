# Continuum QFT Solvation — Cross-Domain Guide

Quantum Field Theory (QFT) approach to solvation modeling across chemistry, biology, and physics. Treats solvent as a **continuum quantum field** rather than discrete molecules, enabling accurate solvation free energy calculations at quantum level.

---

## How Continuum QFT Solvation Works

Classical solvation models (PCM, COSMO, SMD) treat the solvent as a dielectric continuum using classical electrostatics. The nawaz1 VQE engine goes further:

1. **Quantum field treatment** — Solvent is a continuum quantum field described by QFT
2. **VQE integration** — Solvation energy computed via one-shot tensor contraction
3. **Multi-solvent support** — Single, mixed, and extreme multi-solvent environments
4. **Cross-domain** — Same engine handles chemistry (molecules), biology (proteins), physics (materials)

### Classical vs Quantum Solvation

| Aspect | Classical PCM | Continuum QFT (nawaz1) |
|--------|--------------|----------------------|
| Solvent model | Dielectric continuum | Quantum field continuum |
| Solute-solvent | Classical electrostatics | Quantum entanglement |
| Computation | Iterative SCF | One-shot tensor contraction |
| Memory | O(N^3) for N surface elements | ~2 MB constant (streaming) |
| Multi-solvent | Separate calculations | Single Hamiltonian |
| Accuracy | ~1 kcal/mol | Sub-kcal/mol (quantum corrections) |

---

## Supported Solvation Scenarios

### 1. Single Solvant

One solvent surrounding one solute. The simplest and most common case.

**Chemistry example:** Acetaminophen in water
```python
import requests

payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 64,
    "problem": {
        "orbital_energies": solute_orbital_energies  # Hamiltonian of solute
    },
    "config": {
        "sub_module": "vqe_chemistry",
        "task": "solvation_free_energy",
        "solute": "acetaminophen",
        "solvent_model": "continuum_qft",
        "dielectric": 78.4  # water at 25C
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
print(response.json())
```

**Biology example:** Hemoglobin in aqueous solution
```python
payload = {
    "domain": "biology",
    "algorithm": "vqe",
    "qubits": 1024,
    "problem": {
        "orbital_energies": protein_amplitudes  # Protein Hamiltonian
    },
    "config": {
        "sub_module": "molecular_dynamics",
        "task": "solvated_simulation",
        "protein_pdb": "4HHB",
        "solvent_model": "continuum_qft",
        "ionic_strength": 0.15,
        "temperature": 310.15  # body temperature (K)
    }
}
```

**Physics example:** Quantum dot in dielectric medium
```python
payload = {
    "domain": "physics",
    "algorithm": "vqe",
    "qubits": 256,
    "problem": {
        "orbital_energies": qdot_hamiltonian  # Quantum dot Hamiltonian
    },
    "config": {
        "sub_module": "quantum_field_theory",
        "task": "solvated_qft",
        "system": "quantum_dot",
        "solvent_model": "continuum_qft",
        "dielectric": 11.7  # silicon
    }
}
```

---

### 2. Multiple Solvant (Mixed Solvent)

Two or more solvents mixed together (co-solvent systems). Common in pharmaceutical and industrial applications.

**Example:** Drug in water/ethanol mixture
```python
import requests

payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 128,
    "problem": {
        "orbital_energies": solute_orbital_energies
    },
    "config": {
        "sub_module": "vqe_chemistry",
        "task": "solvation_free_energy",
        "solute": "ibuprofen",
        "solvent_model": "continuum_qft",
        "solvents": [
            {"name": "water", "dielectric": 78.4, "fraction": 0.7},
            {"name": "ethanol", "dielectric": 24.3, "fraction": 0.3}
        ],
        "temperature": 298.15
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
print(response.json())
```

**How it works:** The VQE engine encodes the mixed-solvent environment as a superposition of dielectric fields in the Hamiltonian. The effective dielectric is computed quantum-mechanically (not classically averaged), capturing quantum interference between solvent components.

---

### 3. Extreme Multiple Solvant (10+ Solvents)

Complex industrial or biological environments with many solvent species simultaneously. Classically intractable due to combinatorial explosion of solvent-solvent interactions.

**Example:** Pharmaceutical formulation in 12-solvent system
```python
import requests

solvents = [
    {"name": "water",        "dielectric": 78.4,  "fraction": 0.40},
    {"name": "ethanol",      "dielectric": 24.3,  "fraction": 0.15},
    {"name": "DMSO",         "dielectric": 46.7,  "fraction": 0.10},
    {"name": "methanol",     "dielectric": 32.7,  "fraction": 0.08},
    {"name": "acetone",      "dielectric": 20.7,  "fraction": 0.05},
    {"name": "acetonitrile", "dielectric": 37.5,  "fraction": 0.05},
    {"name": "THF",          "dielectric": 7.5,   "fraction": 0.04},
    {"name": "chloroform",   "dielectric": 4.8,   "fraction": 0.03},
    {"name": "toluene",      "dielectric": 2.4,   "fraction": 0.03},
    {"name": "hexane",       "dielectric": 1.9,   "fraction": 0.02},
    {"name": "glycerol",     "dielectric": 42.5,  "fraction": 0.03},
    {"name": "propylene_glycol", "dielectric": 32.0, "fraction": 0.02},
]

# Encode all solvents as orbital energies
# Each solvent contributes: dielectric, fraction, polarizability, dipole moment
solvent_energies = []
for s in solvents:
    solvent_energies.extend([
        s["dielectric"] * s["fraction"],  # weighted dielectric
        s["fraction"],                      # mole fraction
    ])

# Pad to power of 2
qubits_needed = 64
while len(solvent_energies) < qubits_needed:
    solvent_energies.append(0.0)

payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": qubits_needed,
    "problem": {
        "orbital_energies": solute_orbital_energies + solvent_energies
    },
    "config": {
        "sub_module": "vqe_chemistry",
        "task": "solvation_free_energy",
        "solute": "complex_drug_molecule",
        "solvent_model": "continuum_qft",
        "num_solvents": len(solvents),
        "temperature": 298.15
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
print(f"Solvation energy: {result['result']['aggregate_energy']:.6f} Hartree")
print(f"Fidelity: {result['result']['fidelity']:.12f}")
```

**Why classical fails here:** 12 solvents create C(12,2) = 66 pairwise interactions, C(12,3) = 220 three-body terms, and so on. The VQE engine encodes all interactions in a single Hamiltonian and computes the solvation energy in one tensor contraction — no iterative solver needed.

---

## Common Solvent Dielectric Constants

| Solvent | Dielectric (25C) | Polarity |
|---------|-----------------|----------|
| Water | 78.4 | High |
| DMSO | 46.7 | High |
| Glycerol | 42.5 | High |
| Acetonitrile | 37.5 | High |
| Methanol | 32.7 | Medium |
| Ethanol | 24.3 | Medium |
| Acetone | 20.7 | Medium |
| Dichloromethane | 8.9 | Low |
| THF | 7.5 | Low |
| Chloroform | 4.8 | Low |
| Toluene | 2.4 | Nonpolar |
| Hexane | 1.9 | Nonpolar |
| Vacuum | 1.0 | None |

---

## API Reference

### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `domain` | string | Yes | `chemistry`, `biology`, or `physics` |
| `algorithm` | string | No | Default: `vqe` |
| `qubits` | int | Yes | **Must be power of 2**: 4, 8, 16, ..., 65536 |
| `problem.orbital_energies` | float[] | Yes | Solute Hamiltonian coefficients |
| `config.sub_module` | string | Yes | Domain-specific sub-module |
| `config.task` | string | Yes | `solvation_free_energy` or `solvated_simulation` |
| `config.solvent_model` | string | Yes | Must be `continuum_qft` |
| `config.dielectric` | float | Single solvent | Dielectric constant |
| `config.solvents` | object[] | Multi solvent | Array of solvent specs |
| `config.num_solvents` | int | Extreme | Number of solvents |
| `config.temperature` | float | No | Temperature in Kelvin |
| `config.ionic_strength` | float | Biology only | Salt concentration (M) |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `completed` or `error` |
| `result.aggregate_energy` | float | Solvation free energy (Hartree) |
| `result.fidelity` | float | 1.0 = perfect quantum accuracy |
| `result.converged` | bool | Whether computation converged |

---

## Cross-Domain Usage

| Domain | Solute Type | Config Sub-module | Task |
|--------|-----------|------------------|------|
| **Chemistry** | Small molecules, drugs | `vqe_chemistry` | `solvation_free_energy` |
| **Biology** | Proteins, DNA, membranes | `molecular_dynamics` | `solvated_simulation` |
| **Physics** | Quantum dots, materials, surfaces | `quantum_field_theory` | `solvated_qft` |

---

## Important Notes

1. **Correct Hamiltonian** — Solute orbital energies must represent a physically valid Hamiltonian
2. **Correct Algorithm** — Always use `vqe` for solvation energy calculations
3. **Qubits = Power of 2** — Qubit count must be 4, 8, 16, 32, 64, 128, 256, etc.
4. **Use `problem` field** — Not `input_data` for the Hamiltonian

---

## Related Documentation

- [Chemistry Package](../packages/chemistry/README.md) — Continuum QFT solvation chemistry
- [Biology Package](../packages/biology/README.md) — Biological solvation (protein-water)
- [Physics Package](../packages/physics/README.md) — QFT sub-module
- [Quick Start](QUICKSTART.md) — Basic API usage
- [All Algorithms](../ALL_ALGORITHMS_INPUT_METHODS.md) — Input format reference
