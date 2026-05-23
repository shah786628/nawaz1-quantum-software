# VQE Engine: Complete Input Data Guide

## Overview

The nawaz1 Unified Quantum VQE Engine accepts scientific problem data through the **`problem`** field in API requests. This guide shows all supported input formats with working examples.

---

## 📋 API Endpoint

```
POST /api/v1/quantum/execute
Content-Type: application/json
```

---

## 🎯 Input Data Formats

The VQE engine supports **THREE** ways to provide input data:

### 1. **Molecule Field** (Chemistry - Pre-computed)
For common molecules with pre-computed integrals.

### 2. **Problem.orbital_energies** (Chemistry/Physics - Custom Hamiltonian)
For custom Hamiltonian coefficients.

### 3. **Problem.interaction_energies** (Physics - Interaction Models)
For physics interaction models (Ising, Heisenberg, etc.).

---

## ✅ Format 1: Molecule Field (Easiest)

### Use Case
Quantum chemistry calculations for common molecules.

### Supported Molecules
- **H₂** (Hydrogen molecule) - 4 qubits
- **LiH** (Lithium Hydride) - 8 qubits

### Example: H₂ Ground State Energy

```python
import requests

payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 4,
    "molecule": "H2",          # Pre-computed H2 integrals
    "bond_length": 0.74        # Bond length in Angstroms
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()

# Expected output:
# {
#   "status": "completed",
#   "molecule": "H2",
#   "result": {
#     "ground_state_energy_hartree": -1.137,
#     "electronic_energy_hartree": -1.852,
#     "nuclear_repulsion_hartree": 0.715,
#     "converged": true,
#     "iterations": 42
#   }
# }
```

### Example: LiH Molecule

```python
payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 8,
    "molecule": "LiH",
    "bond_length": 1.595  # Equilibrium bond length
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
```

---

## ✅ Format 2: Problem.orbital_energies (Custom Hamiltonian)

### Use Case
When you have custom Hamiltonian coefficients from quantum chemistry calculations.

### Example: H₂ Hamiltonian (Qubit Operator)

```python
import requests

# H2 Hamiltonian at 0.74 Å (from quantum chemistry calculation)
# Terms: I, Z0, Z1, Z0Z1, Y0X1X0Y1
h2_hamiltonian = [
    -1.0523732457727362,   # Identity term
     0.39793742484318045,  # Z0
    -0.39793742484318045,  # Z1
    -0.01128010425623538,  # Z0⊗Z1
     0.18093119978423148   # Y0⊗X1⊗X0⊗Y1
]

payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
        "orbital_energies": h2_hamiltonian
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()

# Expected output:
# {
#   "status": "completed",
#   "result": {
#     "aggregate_energy": -1.137,
#     "fidelity": 0.999999999999,
#     "converged": true,
#     "iteration_count": 42,
#     "energy_history": [...]
#   }
# }
```

### Example: Transverse Field Ising Model

```python
import requests

# TFIM Hamiltonian coefficients
# H = -J Σ Z_i Z_{i+1} - h Σ X_i
ising_hamiltonian = [
    -1.0,   # J (coupling strength)
    -0.5,   # h (transverse field)
    -0.5,   # h
     0.1    # Small perturbation
]

payload = {
    "domain": "physics",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
        "orbital_energies": ising_hamiltonian
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
```

---

## ✅ Format 3: Problem.interaction_energies (Physics Models)

### Use Case
Physics interaction models (Ising, Heisenberg, Hubbard, etc.).

### Example: Ising Model

```python
import requests

# Ising model: H = -J Σ σ_i^z σ_{i+1}^z
# 4-spin chain with J=1.0
ising_interaction = [
    -1.0,   # Spin 1-2 interaction
    -1.0,   # Spin 2-3 interaction
    -1.0,   # Spin 3-4 interaction
     0.0    # Boundary term
]

payload = {
    "domain": "physics",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
        "interaction_energies": ising_interaction
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
```

### Example: Heisenberg Model

```python
import requests

# Heisenberg model: H = J Σ (X_i X_{i+1} + Y_i Y_{i+1} + Z_i Z_{i+1})
heisenberg_interaction = [
    1.0,    # J (exchange coupling)
    1.0,    # XX term
    1.0,    # YY term
    1.0     # ZZ term
]

payload = {
    "domain": "physics",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
        "interaction_energies": heisenberg_interaction
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
```

---

## 📊 Complete Examples by Domain

### Chemistry Domain

#### Example 1: H₂ Molecule Scan (Bond Length Variation)

```python
import requests
import matplotlib.pyplot as plt

bond_lengths = [0.5, 0.6, 0.7, 0.74, 0.8, 0.9, 1.0, 1.2]
energies = []

for bond_length in bond_lengths:
    payload = {
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4,
        "molecule": "H2",
        "bond_length": bond_length
    }
    
    response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
    result = response.json()
    
    energy = result['result']['ground_state_energy_hartree']
    energies.append(energy)
    print(f"Bond: {bond_length:.2f} Å → Energy: {energy:.6f} Hartree")

# Plot dissociation curve
plt.plot(bond_lengths, energies, 'o-')
plt.xlabel('Bond Length (Å)')
plt.ylabel('Ground State Energy (Hartree)')
plt.title('H₂ Dissociation Curve')
plt.grid(True)
plt.savefig('h2_dissociation.png')
plt.show()
```

#### Example 2: Custom Molecular Orbital Energies

```python
import requests

# Orbital energies from Hartree-Fock calculation
# For a custom molecule (example values)
orbital_energies = [
    -20.5,   # Core orbital 1
    -12.3,   # Core orbital 2
     -0.5,   # HOMO
      0.3,   # LUMO
      1.2,   # LUMO+1
      2.5    # LUMO+2
]

payload = {
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 6,
    "problem": {
        "orbital_energies": orbital_energies
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
```

---

### Physics Domain

#### Example 1: Quantum Harmonic Oscillator

```python
import requests
import numpy as np

# Harmonic oscillator Hamiltonian: H = p²/2m + ½mω²x²
# Discretized on 8 qubits
num_qubits = 8
h_oscillator = []

for i in range(num_qubits):
    # Kinetic + Potential terms
    h_oscillator.append(0.5 * (i + 1))

payload = {
    "domain": "physics",
    "algorithm": "vqe",
    "qubits": num_qubits,
    "problem": {
        "orbital_energies": h_oscillator
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()

print(f"Ground state energy: {result['result']['aggregate_energy']:.6f}")
```

#### Example 2: Lattice Gauge Theory (Schwinger Model)

```python
import requests

# Schwinger model (1+1D QED) on lattice
# H = -i Σ (ψ†_n e^{iθ} ψ_{n+1} - h.c.) + m Σ (-1)^n ψ†_n ψ_n
mass_term = 1.0  # Fermion mass
gauge_coupling = 0.5  # Gauge coupling

schwinger_hamiltonian = [
    mass_term,
    gauge_coupling,
    -mass_term,  # Staggered mass
    gauge_coupling
]

payload = {
    "domain": "physics",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
        "interaction_energies": schwinger_hamiltonian
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()
```

---

### Finance Domain

#### Example: Portfolio Optimization

```python
import requests

# Portfolio optimization as QUBO problem
# Minimize risk while maximizing return
# H = Σ w_i μ_i - λ Σ Σ w_i w_j σ_ij
portfolio_hamiltonian = [
    0.1,    # Asset 1 expected return
    0.15,   # Asset 2 expected return
    0.12,   # Asset 3 expected return
   -0.5,    # Risk penalty (covariance)
   -0.3,    # Covariance 1-2
   -0.4     # Covariance 1-3
]

payload = {
    "domain": "finance",
    "algorithm": "vqe",
    "qubits": 6,
    "problem": {
        "orbital_energies": portfolio_hamiltonian
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()

print(f"Optimal portfolio energy: {result['result']['aggregate_energy']:.6f}")
```

---

### Machine Learning Domain

#### Example: Quantum Neural Network Training

```python
import requests

# QNN loss landscape (simplified)
# H = Σ L(y_pred, y_true) * parameters
training_hamiltonian = [
    0.8,    # Loss for sample 1
    0.6,    # Loss for sample 2
    0.9,    # Loss for sample 3
    0.7     # Loss for sample 4
]

payload = {
    "domain": "ml",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
        "orbital_energies": training_hamiltonian
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()

print(f"Training loss: {result['result']['aggregate_energy']:.6f}")
```

---

### Optimization Domain

#### Example: Traveling Salesman Problem (TSP)

```python
import requests

# TSP encoded as QUBO
# 3 cities, distance matrix:
#   A  B  C
# A 0 10 15
# B 10 0  20
# C 15 20 0

tsp_hamiltonian = [
    10,    # Distance A-B
    15,    # Distance A-C
    20,    # Distance B-C
   -5,     # Constraint penalty
   -5,     # Constraint penalty
   -5      # Constraint penalty
]

payload = {
    "domain": "optimization",
    "algorithm": "vqe",
    "qubits": 6,
    "problem": {
        "orbital_energies": tsp_hamiltonian
    }
}

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
result = response.json()

print(f"TSP solution energy: {result['result']['aggregate_energy']:.6f}")
```

---

## ⚠️ Common Mistakes

### ❌ WRONG: Using `input_data` at Top Level

```python
# ❌ THIS WON'T WORK!
payload = {
    "domain": "chemistry",
    "qubits": 4,
    "input_data": [0.5, 0.5, 0.5, 0.5]  # ENGINE IGNORES THIS!
}
```

**Why it fails:** The VQE engine uses the `extract_input_data()` function which looks for data in the `problem` field, not top-level `input_data`.

### ✅ CORRECT: Use `problem` Field

```python
# ✅ THIS WORKS!
payload = {
    "domain": "chemistry",
    "qubits": 4,
    "problem": {
        "orbital_energies": [0.5, 0.5, 0.5, 0.5]  # ENGINE USES THIS!
    }
}
```

---

## 🔬 Advanced Usage

### Example: Batch Processing Multiple Molecules

```python
import requests
import concurrent.futures

molecules = [
    {"name": "H2", "bond": 0.74},
    {"name": "H2", "bond": 0.80},
    {"name": "H2", "bond": 0.90},
    {"name": "LiH", "bond": 1.595},
]

def run_vqe(mol):
    payload = {
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4 if mol['name'] == 'H2' else 8,
        "molecule": mol['name'],
        "bond_length": mol['bond']
    }
    
    response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
    return response.json()

# Run in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(run_vqe, mol) for mol in molecules]
    
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        print(f"Molecule: {result['molecule']}, Energy: {result['result']['ground_state_energy_hartree']}")
```

### Example: Variational Quantum Eigensolver Parameter Sweep

```python
import requests
import numpy as np

# Sweep bond lengths to find equilibrium geometry
bond_lengths = np.linspace(0.5, 2.0, 30)
energies = []

for bond in bond_lengths:
    payload = {
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4,
        "molecule": "H2",
        "bond_length": float(bond)
    }
    
    response = requests.post("http://localhost:8080/api/v1/quantum/execute", json=payload)
    result = response.json()
    
    energy = result['result']['ground_state_energy_hartree']
    energies.append(energy)
    
# Find minimum (equilibrium)
min_idx = np.argmin(energies)
equilibrium_bond = bond_lengths[min_idx]
equilibrium_energy = energies[min_idx]

print(f"Equilibrium bond length: {equilibrium_bond:.3f} Å")
print(f"Equilibrium energy: {equilibrium_energy:.6f} Hartree")
```

---

## 📊 Response Structure

### Standard VQE Response

```json
{
  "execution_id": "qexec_abc123",
  "status": "completed",
  "domain": "chemistry",
  "algorithm": "vqe",
  "num_qubits_requested": 4,
  "num_qubits_simulated": 4096,
  "result": {
    "aggregate_energy": -1.137,
    "line_energies": [-1.137, -1.136, -1.138],
    "parallel_lines_used": 16,
    "compression_ratio": 4096,
    "fidelity": 0.999999999999,
    "execution_time_us": 523000,
    "l3_circuit_time_us": 520000,
    "converged": true,
    "iteration_count": 42,
    "barren_plateau_detected": false,
    "energy_history": [-0.5, -0.8, -1.0, -1.1, -1.137],
    "cumulative_truncation_error": 1e-13
  },
  "real_computation": true
}
```

### Chemistry-Specific Response (with molecule field)

```json
{
  "execution_id": "qexec_xyz789",
  "status": "completed",
  "domain": "chemistry",
  "molecule": "H2",
  "basis_set": "sto-3g",
  "result": {
    "ground_state_energy_hartree": -1.137,
    "electronic_energy_hartree": -1.852,
    "nuclear_repulsion_hartree": 0.715,
    "converged": true,
    "iterations": 42,
    "energy_history": [...]
  },
  "real_computation": true,
  "routed_via": "AlgorithmBridge"
}
```

---

## 🎓 Key Takeaways

1. **Use `problem` field** for custom Hamiltonian data
2. **Use `molecule` field** for pre-computed molecules (H₂, LiH)
3. **Don't use `input_data`** at top level (it's ignored)
4. **Data must be physically meaningful** (normalized amplitudes or Hamiltonian coefficients)
5. **Engine auto-selects** optimal qubit width based on data complexity

---

## 📚 Additional Resources

- **GitHub Repository:** https://github.com/shah786628/nawaz1-quantum-software
- **API Documentation:** See quantum_handlers.rs for implementation details
- **Quantum Chemistry Module:** nawaz1_quantum::chemistry
- **VQE Engine:** nawaz1_engine::quantum_vqe_engine

---

## 🔧 Troubleshooting

### Issue: Energy returns 0 or meaningless values

**Cause:** Using `input_data` instead of `problem` field.

**Solution:**
```python
# ❌ Wrong
"input_data": [0.5, 0.5, 0.5, 0.5]

# ✅ Correct
"problem": {
    "orbital_energies": [0.5, 0.5, 0.5, 0.5]
}
```

### Issue: Engine returns error about unsupported molecule

**Cause:** Molecule doesn't have pre-computed integrals.

**Solution:** Use custom Hamiltonian via `problem.orbital_energies` or provide molecule with pre-computed data (H₂, LiH).

### Issue: Results not converging

**Cause:** Hamiltonian coefficients may be invalid or poorly scaled.

**Solution:**
- Check Hamiltonian is Hermitian (real coefficients)
- Normalize input data if using amplitudes
- Increase `max_iterations` in config

---

## ✨ Summary

| Input Method | Use Case | Example |
|--------------|----------|---------|
| `molecule` + `bond_length` | Pre-computed molecules | H₂, LiH |
| `problem.orbital_energies` | Custom Hamiltonian | Any quantum system |
| `problem.interaction_energies` | Physics models | Ising, Heisenberg |

**Remember:** The VQE engine is designed for **scientific problem data**, not arbitrary arrays. Always provide physically meaningful input for accurate results.
