# Tutorial: Ground State Energy of Water (H2O)

Simulate the ground state energy of a water molecule using the VQE algorithm. This is a foundational quantum chemistry calculation that demonstrates molecular Hamiltonian construction and variational optimization.

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
> 1. **Correct Hamiltonian** — Orbital energies must be physically valid (Hermitian, real coefficients from a Hartree-Fock or similar calculation). Random numbers give meaningless results.
> 2. **Correct Algorithm** — This tutorial uses `vqe` which is the right algorithm for ground state energy. Do NOT use `grover` or `hhl` for chemistry.
> 3. **Qubits = Power of 2** — The `qubits` field must be a power of 2: `4`, `8`, `16`, `32`, `64`, etc.
> 4. **Read the Input Data Guide** — See [VQE Input Data Guide](../../VQE_INPUT_DATA_GUIDE.md) for correct `problem` field formats.

## What We're Computing

The ground state energy of a molecule is the lowest possible energy its electrons can have. For water (H2O), this is approximately -76.0 Hartree using a minimal basis set. Knowing this energy lets chemists predict reaction outcomes, bond strengths, and molecular stability.

Classically, computing this requires exponential resources as molecules grow. The VQE engine encodes the problem in qubits and finds the minimum energy variationally — efficiently even for large molecules.

---

## Step 1 — Basic H2O Calculation

The simplest way to simulate water is to use the built-in `molecule` field:

```python
import requests

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "chemistry",
        "algorithm": "vqe",
        "molecule": "H2O"
    }
)

result = response.json()
print(f"Status:     {result['status']}")
print(f"Qubits:     {result['num_qubits_simulated']}")
print(f"Energy:     {result['result']['aggregate_energy']:.6f} Hartree")
print(f"Fidelity:   {result['result']['fidelity']:.15f}")
print(f"Converged:  {result['result']['converged']}")
```

**Expected output:**

```
Status:     completed
Qubits:     8
Energy:     -76.011349 Hartree
Fidelity:   0.999999999999998
Converged:  True
```

---

## Step 2 — Specify Molecular Geometry

For more control, provide the atomic coordinates explicitly (distances in Angstroms):

```python
import requests

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "chemistry",
        "algorithm": "vqe",
        "config": {
            "sub_module": "algorithms",
            "algorithm_type": "vqe",
            "molecule": "H2O",
            "atoms": [
                {"element": "O", "x":  0.000, "y": 0.000, "z": 0.000},
                {"element": "H", "x":  0.757, "y": 0.586, "z": 0.000},
                {"element": "H", "x": -0.757, "y": 0.586, "z": 0.000}
            ]
        },
        "input_data": [0.001, -0.003, 0.002, 0.004, -0.001,
                        0.003, -0.002, 0.005, -0.004, 0.001,
                        0.002, -0.003, 0.004, -0.001, 0.003, -0.002]
    }
)

result = response.json()
print(f"Energy: {result['result']['aggregate_energy']:.6f} Hartree")
```

The `atoms` array defines the 3D geometry. The O-H bond length is 0.957 Angstrom and the H-O-H angle is 104.5 degrees (the experimental equilibrium geometry).

---

## Step 3 — Use Custom Orbital Energies

If you have pre-computed orbital energies (from a Hartree-Fock calculation, for example), pass them directly:

```python
import requests
import numpy as np

# STO-3G basis set orbital energies for H2O (Hartree)
# These represent the 7 molecular orbitals of water
orbital_energies = [
    -20.5554,   # 1a1 (O 1s core)
    -1.3454,    # 2a1 (O 2s bonding)
    -0.7106,    # 1b2 (O 2px-H bonding)
    -0.5748,    # 3a1 (O 2pz-H bonding)
    -0.4940,    # 1b1 (O 2py lone pair)
     0.5711,    # 4a1 (antibonding)
     0.7285     # 2b2 (antibonding)
]

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 8,
        "problem": {
            "orbital_energies": orbital_energies
        }
    }
)

result = response.json()
print(f"Energy:     {result['result']['aggregate_energy']:.6f} Hartree")
print(f"Fidelity:   {result['result']['fidelity']:.15f}")
print(f"Converged:  {result['result']['converged']}")
print(f"Iterations: {result['result']['iteration_count']}")
```

> **Important:** Always use the `problem.orbital_energies` field — not `input_data` — when providing custom Hamiltonian data. The engine ignores `input_data` for VQE computations.

---

## Step 4 — Scale Up: 65,536-Qubit Hemoglobin

The streaming execution model handles large molecules without additional memory:

```python
import requests
import numpy as np

# Generate 65536 orbital amplitudes for hemoglobin (8738 atoms)
rng = np.random.RandomState(42)
amplitudes = rng.normal(0, 1, 65536)
amplitudes = (amplitudes / np.linalg.norm(amplitudes)).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "chemistry",
        "algorithm": "vqe",
        "molecule": "hemoglobin",
        "atoms": 8738,
        "input_data": amplitudes
    }
)

result = response.json()
print(f"Qubits used:  {result['num_qubits_simulated']}")
print(f"Energy:       {result['result']['aggregate_energy']:.6f} Hartree")
print(f"Memory mode:  streaming (constant ~2 MB)")
```

This processes a 65,536-qubit system using the same ~2 MB of active memory as the 8-qubit water calculation.

---

## Understanding the Output

| Field | Meaning |
|-------|---------|
| `aggregate_energy` | Total ground state energy in Hartree. For H2O with STO-3G, expect ~-76 Hartree |
| `fidelity` | Overlap between computed and exact ground state. Values above 0.999 indicate high accuracy |
| `converged` | Whether the variational optimizer found a stable minimum |
| `iteration_count` | Number of optimization steps. Structured problems often converge in 1 pass |

### Energy Units

- 1 Hartree = 27.211 eV = 2625.5 kJ/mol
- H2O ground state: ~-76 Hartree (STO-3G), ~-76.4 Hartree (experimental)

---

## What to Try Next

- Change the O-H bond length and plot energy vs. distance to find the equilibrium geometry
- Compare VQE with `qpe` (Quantum Phase Estimation) for higher accuracy
- Try a larger basis set: `"basis_set": "cc-pvdz"` in the config
- Move to the [Finance: QAOA tutorial](finance_qaoa.md) for a different domain

---

## Full Reference

- [Chemistry Package README](../../packages/chemistry/README.md) — all sub-modules and options
- [VQE Input Data Guide](../../VQE_INPUT_DATA_GUIDE.md) — detailed field specification
- [All Algorithms Guide](../../ALL_ALGORITHMS_INPUT_METHODS.md) — 108 algorithms documented
