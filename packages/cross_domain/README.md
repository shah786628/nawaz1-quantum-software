# Cross-Domain Package — Multi-Physics Quantum Pipelines

## Overview

Most real-world problems are **multi-physics**: a drug candidate has a quantum-chemical Hamiltonian, a biological binding partner, and a market price; an aircraft component is shaped by fluid flow, thermal stress, and material microstructure. The Cross-Domain package describes how to **chain multiple Nawaz1 quantum domains together**, piping the output of one execution as input to the next.

The pattern is intentionally simple: each domain is an HTTP call against the unified endpoint

```
POST http://localhost:8080/api/v1/quantum/execute
```

and a "cross-domain run" is just a sequence of those calls where one stage's output `result` (energies, embeddings, distributions, optimized parameters) becomes the next stage's `input_data` or `config`.

---

## When to Use Cross-Domain

Reach for cross-domain pipelines when **a single domain cannot capture the full problem**:

- The problem spans multiple physical or mathematical domains (e.g., chemistry + biology + finance).
- You need quantum-accurate coupling between scales (electronic structure → mesoscopic dynamics → macroscopic decision).
- A single VQE pass is **necessary but not sufficient** — its output is a *feature* for a downstream optimization.
- Stages must remain auditable, swappable, and individually re-runnable (e.g., re-run only the finance stage when market data changes).

For pure single-domain problems, call that domain directly. Cross-domain adds latency and orchestration complexity that only pays off when stages truly couple.

---

## API Pattern: Pipe One Domain Into the Next

All chaining happens **client-side**. The engine itself is stateless across `/quantum/execute` calls — your orchestrator keeps the data flowing.

```python
import numpy as np, requests
ENDPOINT = "http://localhost:8080/api/v1/quantum/execute"

def execute(domain, algorithm, input_data, config=None):
    r = requests.post(ENDPOINT, json={
        "domain": domain,
        "algorithm": algorithm,
        "input_data": list(input_data),
        "config": config or {}
    }, timeout=300)
    r.raise_for_status()
    return r.json()

def normalize(v):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    return (v / n) if n > 0 else v

def amplitudes_from_result(prev, key="amplitudes", size=65536):
    """Lift a previous stage's amplitude payload into a normalized 65536-vector."""
    arr = np.asarray(prev["result"].get(key, prev["result"].get("output", [])), dtype=float)
    if arr.size < size:
        arr = np.pad(arr, (0, size - arr.size))
    elif arr.size > size:
        arr = arr[:size]
    return normalize(arr).tolist()
```

The two reusable primitives are:

1. **`amplitudes_from_result(...)`** — turn the previous stage's vector output into the next stage's `input_data` (always 65536 floats for the full-scale engine).
2. **`config` carry-over** — pull scalars (energies, optimized angles, binding affinities) from `prev["result"]` into the next stage's `config` so the downstream domain knows what physics to honor.

---

## Example 1 — Drug Discovery Pipeline

**Stages:** Chemistry (molecular Hamiltonian) → Biology (protein folding & binding) → Finance (market pricing of the candidate).

```python
# 1) CHEMISTRY: VQE ground state of the candidate molecule
mol_amps = normalize(np.random.default_rng(1).normal(size=65536)).tolist()
chem = execute("chemistry", "vqe", mol_amps, {
    "sub_module": "vqe_chemistry",
    "task":       "ground_state_energy",
    "molecule":   "candidate_smiles_CC(=O)Oc1ccccc1C(=O)O",
    "ansatz":     "uccsd"
})
ground_state_energy = chem["result"]["energy"]

# 2) BIOLOGY: feed chemistry amplitudes + ground-state energy into protein folding
bio_input = amplitudes_from_result(chem)
bio = execute("biomolecules", "vqe", bio_input, {
    "sub_module":          "drug_discovery",
    "task":                "binding_affinity",
    "target_pdb":          "1HBB",
    "ligand_ground_energy": ground_state_energy
})
binding_dG = bio["result"]["energy"]   # ΔG_binding in kcal/mol

# 3) FINANCE: price the candidate using binding affinity as a quality signal
fin_input = amplitudes_from_result(bio)
fin = execute("finance", "qaoa", fin_input, {
    "sub_module":   "portfolio",
    "task":         "drug_pipeline_valuation",
    "binding_dG":   binding_dG,
    "horizon_years": 7
})
print("expected_NPV =", fin["result"]["expected_value"])
```

**Why chained:** the molecular ground state determines binding pose, binding affinity determines clinical-success probability, which determines NPV. Each stage *requires* the previous one's quantum-accurate result.

---

## Example 2 — Aerospace Engineering

**Stages:** Fluid Mechanics (Navier-Stokes around the airfoil) → Heat Transfer (thermal stress on the skin) → Materials Science (structural integrity under combined load).

```python
# 1) FLUID MECHANICS: aerodynamic flow field
flow_in = normalize(np.random.default_rng(2).normal(size=65536)).tolist()
fluid = execute("fluid_mechanics", "vqe", flow_in, {
    "sub_module":      "navier_stokes",
    "task":            "compressible_flow",
    "mach":            0.85,
    "reynolds_number": 1e7,
    "grid_size":       [256, 256]
})
pressure_field = fluid["result"]["pressure_amplitudes"]

# 2) HEAT TRANSFER: surface heating from compressed flow
heat_in = amplitudes_from_result(fluid, key="pressure_amplitudes")
heat = execute("heat_transfer", "hhl", heat_in, {
    "sub_module":           "conduction",
    "task":                 "thermal_stress",
    "boundary_pressure":    "from_fluid_stage",
    "thermal_conductivity": 167.0,   # Aluminum 7075
    "grid_size":            [256, 256]
})

# 3) MATERIALS SCIENCE: structural failure analysis under combined thermal + aero load
mat_in = amplitudes_from_result(heat, key="temperature_amplitudes")
mat = execute("materials_science", "vqe", mat_in, {
    "sub_module": "structural",
    "task":       "fatigue_lifetime",
    "alloy":      "Al-7075-T6",
    "load_case":  "thermo_aero_coupled"
})
print("predicted_cycles_to_failure =", mat["result"]["cycles_to_failure"])
```

**Why chained:** the airfoil's stress state is the *combined* effect of pressure load (fluid stage) and temperature gradient (heat stage). Materials science cannot honestly answer "will it crack?" without both.

---

## Example 3 — Climate Science

**Stages:** Fluid Mechanics (ocean currents) → Physics (quantum thermodynamics of the atmospheric column) → Mathematics (large-scale optimization over the coupled system).

```python
# 1) FLUID MECHANICS: ocean circulation pattern
ocean_in = normalize(np.random.default_rng(3).normal(size=65536)).tolist()
ocean = execute("fluid_mechanics", "vqe", ocean_in, {
    "sub_module":      "navier_stokes",
    "task":            "ocean_circulation",
    "grid_size":       [256, 256],
    "salinity_coupled": True
})

# 2) PHYSICS: quantum thermodynamics of the atmosphere driven by ocean SST
atm_in = amplitudes_from_result(ocean, key="sst_amplitudes")
atm = execute("physics", "vqe", atm_in, {
    "sub_module": "quantum_thermodynamics",
    "task":       "atmospheric_entropy_production",
    "model":      "radiative_convective"
})

# 3) MATHEMATICS: optimize emissions trajectory under the coupled climate response
opt_in = amplitudes_from_result(atm, key="entropy_amplitudes")
opt = execute("mathematics", "qaoa", opt_in, {
    "sub_module":     "quantum_optimization_theory",
    "task":           "emissions_pathway",
    "horizon_years":  80,
    "constraint":     "warming_below_1_5C"
})
print("optimal_emissions_curve =", opt["result"]["trajectory"])
```

**Why chained:** atmospheric entropy production depends on ocean SST; the optimal emissions trajectory depends on the full coupled response. None of the three domains alone yields a defensible answer.

---

## Recommended Orchestration Patterns

| Pattern | When | Sketch |
|---------|------|--------|
| **Linear chain** | Each stage strictly consumes the previous one. | `A → B → C` |
| **Fan-out / Fan-in** | One stage feeds several parallel domains, results merged. | `A → {B, C, D} → E` |
| **Iterative loop** | Stages re-run until a coupled fixed-point converges (e.g., aero + structural). | `(A ↔ B) until ‖Δ‖ < ε` |
| **Sensitivity sweep** | Vary an upstream parameter, re-run the downstream chain. | `A(θ_i) → B → C  ∀ θ_i` |

---

## Tips for Robust Pipelines

- **Always re-normalize.** Each `amplitudes_from_result` call should re-Born-normalize the vector before sending it on.
- **Persist intermediates.** Save each stage's full JSON response — it lets you re-run the tail of the pipeline cheaply when only later parameters change.
- **Watch the qubit budget.** Every stage allocates `next_power_of_two(len(input_data))` qubits. Pad/truncate to the desired width (typically 65536) at every hand-off.
- **Use `config` for scalars, `input_data` for vectors.** Energies, affinities, and Reynolds numbers belong in `config`; field samples and amplitude vectors belong in `input_data`.
- **Fail fast.** If `response["success"] != true` at stage *k*, abort the pipeline before stage *k+1* — propagating bad amplitudes silently corrupts every downstream result.
