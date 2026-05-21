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

## Example 4 — Nuclear Reactor Safety

**Stages:** Physics (neutron transport) → Heat Transfer (coolant thermal field) → Materials Science (fuel rod integrity) → Fluid Mechanics (coolant flow / turbulence).

This pipeline answers a question no single domain can: *"Will this reactor core remain within safe operating limits across a 60-year service life?"*

### Stage 1 — Physics: Neutron Flux Across the Core Lattice

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": "[ 65536 amplitudes encoding the neutron density field over the 17x17x264 fuel-assembly lattice ]",
  "config": {
    "sub_module":          "quantum_transport",
    "task":                "neutron_flux_distribution",
    "reactor_type":        "PWR_Westinghouse_4loop",
    "thermal_power_MW":    3411.0,
    "fuel_enrichment_pct": 4.95,
    "burnup_GWd_per_tU":   45.0,
    "lattice_pitch_cm":    1.26,
    "moderator":           "light_water",
    "boron_ppm":           1200,
    "energy_groups":       2,
    "boundary":            "vacuum_radial_reflective_axial"
  }
}
```

### Stage 2 — Heat Transfer: Coolant Temperature Distribution

```json
{
  "domain": "heat_transfer",
  "algorithm": "hhl",
  "input_data": "[ 65536 amplitudes piped from physics flux_amplitudes ]",
  "config": {
    "sub_module":               "conduction_convection",
    "task":                     "coolant_temperature_field",
    "inlet_temperature_C":      292.0,
    "outlet_target_C":          327.0,
    "system_pressure_MPa":      15.5,
    "mass_flow_kg_per_s":       18800.0,
    "fuel_thermal_conductivity":3.6,
    "cladding_material":        "Zircaloy-4",
    "peak_linear_power_kW_per_m":42.5,
    "axial_nodes":              264
  }
}
```

### Stage 3 — Materials Science: Fuel Rod Integrity Under Thermal + Radiation Stress

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": "[ 65536 amplitudes piped from heat_transfer temperature_amplitudes ]",
  "config": {
    "sub_module":          "structural_radiation",
    "task":                "creep_and_radiation_damage",
    "alloy":               "Zircaloy-4",
    "fast_neutron_fluence_n_per_cm2": 1.2e22,
    "operating_temperature_C":        345.0,
    "hoop_stress_MPa":                95.0,
    "service_life_years":             60,
    "failure_criterion":              "1pct_clad_strain_or_DBTT_breach"
  }
}
```

### Stage 4 — Fluid Mechanics: Coolant Turbulence Optimization

```json
{
  "domain": "fluid_mechanics",
  "algorithm": "vqe",
  "input_data": "[ 65536 amplitudes piped from materials_science stress_amplitudes ]",
  "config": {
    "sub_module":      "navier_stokes",
    "task":            "turbulent_subchannel_flow",
    "reynolds_number": 5.2e5,
    "prandtl_number":  0.85,
    "grid_size":       [256, 256],
    "turbulence_model":"k_epsilon_realizable",
    "objective":       "minimize_DNB_margin_loss"
  }
}
```

### Python Orchestration

```python
# 1) PHYSICS — neutron flux field
core_amps = normalize(np.random.default_rng(4).normal(size=65536)).tolist()
phys = execute("physics", "vqe", core_amps, {
    "sub_module": "quantum_transport",
    "task":       "neutron_flux_distribution",
    "reactor_type":"PWR_Westinghouse_4loop",
    "thermal_power_MW":3411.0,
    "fuel_enrichment_pct":4.95,
    "boron_ppm":1200,
    "energy_groups":2
})

# 2) HEAT TRANSFER — coolant thermal field driven by neutron flux
heat_in = amplitudes_from_result(phys, key="flux_amplitudes")
heat = execute("heat_transfer", "hhl", heat_in, {
    "sub_module":"conduction_convection",
    "task":"coolant_temperature_field",
    "system_pressure_MPa":15.5,
    "mass_flow_kg_per_s":18800.0,
    "peak_linear_power_kW_per_m":42.5
})

# 3) MATERIALS SCIENCE — fuel rod creep + radiation damage
mat_in = amplitudes_from_result(heat, key="temperature_amplitudes")
mat = execute("materials_science", "vqe", mat_in, {
    "sub_module":"structural_radiation",
    "task":"creep_and_radiation_damage",
    "alloy":"Zircaloy-4",
    "fast_neutron_fluence_n_per_cm2":1.2e22,
    "service_life_years":60
})

# 4) FLUID MECHANICS — turbulent subchannel flow optimization
flow_in = amplitudes_from_result(mat, key="stress_amplitudes")
flow = execute("fluid_mechanics", "vqe", flow_in, {
    "sub_module":"navier_stokes",
    "task":"turbulent_subchannel_flow",
    "reynolds_number":5.2e5,
    "turbulence_model":"k_epsilon_realizable",
    "objective":"minimize_DNB_margin_loss"
})

print("60-year DNB margin (lower-bound) =", flow["result"]["dnb_margin_min"])
print("expected fuel rod survival probability =", mat["result"]["survival_probability"])
```

**Why chained:** the cladding failure probability requires the *coupled* answer of neutron flux × thermal gradient × radiation embrittlement × coolant turbulence. Any single domain in isolation gives a misleading safety case.

---

## Example 5 — Autonomous Vehicle System

**Stages:** Machine Learning (LiDAR object detection) → Physics (multi-body collision dynamics) → Logistics (multi-vehicle route coordination) → Real-Time (sub-millisecond decision pipeline).

### Stage 1 — Machine Learning: LiDAR Point Cloud Quantum Classification

```json
{
  "domain": "machine_learning",
  "algorithm": "vqe",
  "input_data": "[ 65536 amplitudes encoding a downsampled LiDAR point cloud of the 200m forward scene ]",
  "config": {
    "sub_module":          "quantum_kernel",
    "task":                "lidar_object_detection",
    "scan_rate_hz":        20,
    "points_per_frame":    131072,
    "classes":             ["car","truck","bicycle","pedestrian","barrier","unknown"],
    "feature_kernel":      "quantum_rbf",
    "embedding_qubits":    16,
    "min_confidence":      0.92
  }
}
```

### Stage 2 — Physics: Multi-Body Collision Prediction

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": "[ 65536 trajectory amplitudes piped from ML detection_amplitudes ]",
  "config": {
    "sub_module":           "classical_mechanics",
    "task":                 "multi_body_trajectory_prediction",
    "horizon_seconds":      3.0,
    "time_step_ms":         20,
    "num_agents":           24,
    "ego_mass_kg":          1820,
    "friction_coefficient": 0.78,
    "tire_model":           "pacejka_2002",
    "collision_threshold_m":0.30
  }
}
```

### Stage 3 — Logistics: Multi-Vehicle Coordination With Time Windows

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "input_data": "[ 65536 amplitudes piped from physics trajectory_amplitudes ]",
  "config": {
    "sub_module":      "vehicle_routing",
    "task":            "fleet_coordination",
    "fleet_size":      48,
    "depot_count":     6,
    "service_radius_km":35.0,
    "time_window_min": 8,
    "objective":       "minimize_weighted_lateness_plus_collision_risk"
  }
}
```

### Stage 4 — Real-Time: Sub-Millisecond Quantum Inference Pipeline

```json
{
  "domain": "real_time",
  "algorithm": "vqe",
  "input_data": "[ 65536 amplitudes piped from logistics route_amplitudes ]",
  "config": {
    "sub_module":            "online_inference",
    "task":                  "drive_decision",
    "deadline_microseconds": 800,
    "decision_set":          ["accelerate","cruise","brake","lane_change_left","lane_change_right","emergency_stop"],
    "safety_margin_sigma":   6.0,
    "fallback_policy":       "minimum_risk_maneuver"
  }
}
```

```python
# 1) ML — LiDAR object detection
lidar_amps = normalize(np.random.default_rng(5).normal(size=65536)).tolist()
det = execute("machine_learning", "vqe", lidar_amps, {
    "sub_module":"quantum_kernel",
    "task":"lidar_object_detection",
    "min_confidence":0.92
})

# 2) PHYSICS — predict trajectories of all detected agents
phys_in = amplitudes_from_result(det, key="detection_amplitudes")
traj = execute("physics", "vqe", phys_in, {
    "sub_module":"classical_mechanics",
    "task":"multi_body_trajectory_prediction",
    "horizon_seconds":3.0,
    "num_agents":24
})

# 3) LOGISTICS — coordinate fleet under predicted trajectories
log_in = amplitudes_from_result(traj, key="trajectory_amplitudes")
fleet = execute("logistics", "qaoa", log_in, {
    "sub_module":"vehicle_routing",
    "task":"fleet_coordination",
    "fleet_size":48
})

# 4) REAL-TIME — emit a single drive decision under an 800 us deadline
rt_in = amplitudes_from_result(fleet, key="route_amplitudes")
decision = execute("real_time", "vqe", rt_in, {
    "sub_module":"online_inference",
    "task":"drive_decision",
    "deadline_microseconds":800
})

print("emit ->", decision["result"]["action"], "in", decision["result"]["latency_us"], "us")
```

**Why chained:** the safe action depends on *who is in the scene* (ML), *where they are going* (Physics), *what the rest of the fleet is doing* (Logistics), and *whether the answer arrives before the next control tick* (Real-Time). A monolithic model cannot honor all four constraints simultaneously.

---

## Example 6 — Global Supply Chain Resilience

**Stages:** Finance (currency / commodity hedging) → Logistics (multi-echelon network flow) → Machine Learning (demand forecasting) → Mathematics (global constrained optimization).

### Stage 1 — Finance: Currency & Commodity Risk Optimization

```json
{
  "domain": "finance",
  "algorithm": "qaoa",
  "input_data": "[ 65536 amplitudes encoding a 12-currency, 8-commodity joint return distribution ]",
  "config": {
    "sub_module":         "portfolio",
    "task":               "fx_commodity_hedge",
    "currencies":         ["USD","EUR","JPY","CNY","GBP","INR","BRL","MXN","KRW","SGD","AUD","ZAR"],
    "commodities":        ["crude","copper","aluminum","lithium","cobalt","wheat","corn","natgas"],
    "risk_aversion":      2.4,
    "horizon_quarters":   8,
    "max_position_pct":   12.0
  }
}
```

### Stage 2 — Logistics: Multi-Echelon Flow Under Disruption Scenarios

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "input_data": "[ 65536 amplitudes piped from finance hedge_amplitudes ]",
  "config": {
    "sub_module":           "network_flow",
    "task":                 "resilient_multi_echelon",
    "tiers":                ["raw","component","subassembly","final","distribution"],
    "nodes":                412,
    "lanes":                3870,
    "disruption_scenarios": ["port_strike","sanctions","earthquake","cyber_outage","fuel_spike"],
    "service_level_target": 0.985,
    "lead_time_buffer_pct": 18.0
  }
}
```

### Stage 3 — Machine Learning: Quantum Kernel Demand Forecasting

```json
{
  "domain": "machine_learning",
  "algorithm": "vqe",
  "input_data": "[ 65536 amplitudes piped from logistics flow_amplitudes ]",
  "config": {
    "sub_module":      "quantum_kernel",
    "task":            "demand_regression",
    "skus":            18420,
    "features":        ["price","seasonality","macro_index","weather","promo","social_signal"],
    "horizon_weeks":   26,
    "loss":            "pinball_p90"
  }
}
```

### Stage 4 — Mathematics: Global Landed-Cost Minimization

```json
{
  "domain": "mathematics",
  "algorithm": "qaoa",
  "input_data": "[ 65536 amplitudes piped from ML forecast_amplitudes ]",
  "config": {
    "sub_module":   "quantum_optimization_theory",
    "task":         "global_landed_cost_min",
    "constraints":  ["service_level>=0.985","co2_per_unit<=2.4","working_capital_max=950e6"],
    "objective":    "minimize_total_landed_cost",
    "horizon_quarters":8
  }
}
```

```python
# 1) FINANCE — hedge currency + commodity risk
fin_amps = normalize(np.random.default_rng(6).normal(size=65536)).tolist()
fin = execute("finance", "qaoa", fin_amps, {
    "sub_module":"portfolio",
    "task":"fx_commodity_hedge",
    "horizon_quarters":8
})

# 2) LOGISTICS — multi-echelon flow under disruption scenarios
log_in = amplitudes_from_result(fin, key="hedge_amplitudes")
log = execute("logistics", "qaoa", log_in, {
    "sub_module":"network_flow",
    "task":"resilient_multi_echelon",
    "service_level_target":0.985
})

# 3) ML — demand forecasting at SKU resolution
ml_in = amplitudes_from_result(log, key="flow_amplitudes")
fc = execute("machine_learning", "vqe", ml_in, {
    "sub_module":"quantum_kernel",
    "task":"demand_regression",
    "horizon_weeks":26
})

# 4) MATHEMATICS — optimize global landed cost under all coupled constraints
opt_in = amplitudes_from_result(fc, key="forecast_amplitudes")
opt = execute("mathematics", "qaoa", opt_in, {
    "sub_module":"quantum_optimization_theory",
    "task":"global_landed_cost_min",
    "horizon_quarters":8
})

print("optimal landed cost =", opt["result"]["total_landed_cost_usd"])
print("worst-case service level =", opt["result"]["service_level_p5"])
```

**Why chained:** hedging affects which lanes are economic; lanes affect achievable service levels; service levels feed forecast variance; the global optimum is the fixed point of all four. Solving them sequentially as independent problems double-counts costs and underestimates tail risk.

---

## Example 7 — Quantum Drug Design to Market (5-Domain Pipeline)

**Stages:** Chemistry (molecular screening) → Biology (protein binding) → Materials Science (drug formulation) → Finance (market valuation) → Machine Learning (patient outcome prediction).

This is the deepest cross-domain example: a single candidate molecule walks through *five* quantum domains, each consuming the previous stage's quantum-accurate output.

### Stage 1 — Chemistry: Molecular Screening

```json
{
  "domain": "chemistry",
  "algorithm": "vqe",
  "input_data": "[ 65536 amplitudes encoding the candidate's electronic Hamiltonian ]",
  "config": {
    "sub_module":  "vqe_chemistry",
    "task":        "ground_state_energy",
    "molecule":    "candidate_smiles_CC1=CC=C(C=C1)C2=CC(=NN2C3=CC=C(C=C3)S(=O)(=O)N)C(F)(F)F",
    "basis_set":   "cc-pVTZ",
    "ansatz":      "uccsd",
    "spin":        0,
    "charge":      0
  }
}
```

### Stage 2 — Biology: Protein Binding

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": "[ 65536 amplitudes piped from chemistry wavefunction_amplitudes ]",
  "config": {
    "sub_module":          "drug_discovery",
    "task":                "binding_affinity",
    "target_pdb":          "6LU7",
    "ligand_ground_energy":"from_chemistry_stage",
    "ph":                  7.4,
    "ionic_strength_mM":   150,
    "include_water":       true
  }
}
```

### Stage 3 — Materials Science: Drug Formulation

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": "[ 65536 amplitudes piped from biology binding_amplitudes ]",
  "config": {
    "sub_module":     "soft_matter",
    "task":           "tablet_formulation_stability",
    "excipients":     ["microcrystalline_cellulose","lactose_monohydrate","magnesium_stearate","croscarmellose_sodium"],
    "polymorph":      "Form_II",
    "humidity_pct":   60.0,
    "shelf_life_target_months":36
  }
}
```

### Stage 4 — Finance: Market Valuation

```json
{
  "domain": "finance",
  "algorithm": "qaoa",
  "input_data": "[ 65536 amplitudes piped from materials_science stability_amplitudes ]",
  "config": {
    "sub_module":     "portfolio",
    "task":           "drug_pipeline_valuation",
    "binding_dG":     "from_biology_stage",
    "stability_score":"from_materials_stage",
    "horizon_years":  12,
    "discount_rate":  0.085,
    "phase_success_priors":[0.63,0.31,0.58,0.85]
  }
}
```

### Stage 5 — Machine Learning: Patient Outcome Prediction

```json
{
  "domain": "machine_learning",
  "algorithm": "vqe",
  "input_data": "[ 65536 amplitudes piped from finance valuation_amplitudes ]",
  "config": {
    "sub_module":  "quantum_kernel",
    "task":        "patient_outcome_regression",
    "cohort_size": 24000,
    "endpoints":   ["progression_free_survival_months","grade3_AE_rate","quality_adjusted_life_years"],
    "covariates":  ["age","sex","biomarker_panel","comorbidity_index","prior_lines"],
    "validation":  "5fold_stratified"
  }
}
```

```python
# 1) CHEMISTRY — molecular ground state
mol_amps = normalize(np.random.default_rng(7).normal(size=65536)).tolist()
chem = execute("chemistry", "vqe", mol_amps, {
    "sub_module":"vqe_chemistry","task":"ground_state_energy",
    "molecule":"candidate_smiles_celecoxib_analog","basis_set":"cc-pVTZ","ansatz":"uccsd"
})

# 2) BIOLOGY — bind into target protein
bio_in = amplitudes_from_result(chem, key="wavefunction_amplitudes")
bio = execute("biomolecules", "vqe", bio_in, {
    "sub_module":"drug_discovery","task":"binding_affinity",
    "target_pdb":"6LU7","ligand_ground_energy":chem["result"]["energy"]
})

# 3) MATERIALS SCIENCE — formulate the bound active into a stable tablet
mat_in = amplitudes_from_result(bio, key="binding_amplitudes")
mat = execute("materials_science", "vqe", mat_in, {
    "sub_module":"soft_matter","task":"tablet_formulation_stability",
    "shelf_life_target_months":36
})

# 4) FINANCE — value the resulting clinical asset
fin_in = amplitudes_from_result(mat, key="stability_amplitudes")
fin = execute("finance", "qaoa", fin_in, {
    "sub_module":"portfolio","task":"drug_pipeline_valuation",
    "binding_dG":bio["result"]["energy"],
    "stability_score":mat["result"]["stability_score"],
    "horizon_years":12
})

# 5) ML — predict per-patient outcome distribution
ml_in = amplitudes_from_result(fin, key="valuation_amplitudes")
out = execute("machine_learning", "vqe", ml_in, {
    "sub_module":"quantum_kernel","task":"patient_outcome_regression",
    "cohort_size":24000
})

print("expected NPV (USD)         =", fin["result"]["expected_value"])
print("median PFS (months)        =", out["result"]["pfs_p50"])
print("grade-3 AE rate (lower CI) =", out["result"]["ae3_p5"])
```

**Why chained:** every commercial decision in pharma is a *joint* answer over chemistry, biology, formulation, market, and clinical outcome. Cutting any one stage out forces the rest to assume defaults — and those defaults are exactly where billion-dollar clinical failures hide.

---

## Recommended Orchestration Patterns

| Pattern | When | Sketch |
|---------|------|--------|
| **Linear chain** | Each stage strictly consumes the previous one. | `A → B → C` |
| **Fan-out / Fan-in** | One stage feeds several parallel domains, results merged. | `A → {B, C, D} → E` |
| **Iterative loop** | Stages re-run until a coupled fixed-point converges (e.g., aero + structural). | `(A ↔ B) until ‖Δ‖ < ε` |
| **Sensitivity sweep** | Vary an upstream parameter, re-run the downstream chain. | `A(θ_i) → B → C  ∀ θ_i` |

---

## Extreme Orchestration Patterns

The four patterns below appear once a pipeline has more than three stages and the coupling between domains becomes non-trivial. They are not "advanced syntax" — they are different *topologies* of how quantum results flow.

### Pattern A — Parallel Fan-Out With Convergence

Run several independent quantum domains in parallel against the same upstream amplitudes, then converge their outputs in a downstream optimizer (typically `mathematics`) for multi-objective trade-off.

```python
from concurrent.futures import ThreadPoolExecutor

# Upstream stage produces a shared feature vector
seed = normalize(np.random.default_rng(8).normal(size=65536)).tolist()

def run_phys():  return execute("physics",   "vqe", seed, {"sub_module":"thermodynamics","task":"entropy_field"})
def run_chem():  return execute("chemistry", "vqe", seed, {"sub_module":"vqe_chemistry","task":"reaction_energy"})
def run_bio():   return execute("biomolecules","vqe",seed, {"sub_module":"systems_biology","task":"pathway_flux"})

# Fan out — three domains run concurrently
with ThreadPoolExecutor(max_workers=3) as pool:
    phys, chem, bio = [f.result() for f in
                       (pool.submit(run_phys), pool.submit(run_chem), pool.submit(run_bio))]

# Converge — concatenate all three result vectors and pad to 65536
fused = np.concatenate([
    np.asarray(phys["result"]["entropy_amplitudes"], dtype=float),
    np.asarray(chem["result"]["reaction_amplitudes"], dtype=float),
    np.asarray(bio["result"]["pathway_amplitudes"],  dtype=float),
])
fused = normalize(np.pad(fused, (0, max(0, 65536 - fused.size)))[:65536]).tolist()

# Multi-objective optimizer on the fused amplitudes
opt = execute("mathematics", "qaoa", fused, {
    "sub_module":"quantum_optimization_theory",
    "task":"multi_objective_pareto",
    "objectives":["minimize_entropy_production","maximize_reaction_yield","preserve_pathway_flux"],
    "weights":[0.4, 0.4, 0.2]
})
```

**When:** the three upstream domains are *independent given* the seed amplitudes. Fan-out cuts wall-clock latency by ~3× because the L3 VQE circuit calls run concurrently against the shared 65536-qubit substrate.

### Pattern B — Iterative Convergence Loop

Some couplings are circular: chemistry needs a temperature field, the temperature field is set by material thermal conductivity, the conductivity depends on the chemistry. Solve by Picard iteration until the change between successive sweeps falls below a tolerance.

```python
def picard_step(amps):
    chem = execute("chemistry", "vqe", amps, {
        "sub_module":"vqe_chemistry","task":"reaction_energy"
    })
    phys_in = amplitudes_from_result(chem, key="reaction_amplitudes")
    phys = execute("physics", "vqe", phys_in, {
        "sub_module":"thermodynamics","task":"temperature_field"
    })
    mat_in = amplitudes_from_result(phys, key="temperature_amplitudes")
    mat  = execute("materials_science", "vqe", mat_in, {
        "sub_module":"thermal","task":"effective_conductivity"
    })
    return amplitudes_from_result(mat, key="conductivity_amplitudes"), {
        "energy":      chem["result"]["energy"],
        "T_max":       phys["result"]["t_max"],
        "k_eff":       mat["result"]["k_effective"]
    }

amps    = normalize(np.random.default_rng(9).normal(size=65536)).tolist()
prev_k  = float("inf")
for it in range(20):
    amps, scalars = picard_step(amps)
    delta_k = abs(scalars["k_eff"] - prev_k)
    print(f"iter {it:02d}  T_max={scalars['T_max']:.2f}  k_eff={scalars['k_eff']:.4f}  Δk={delta_k:.2e}")
    if delta_k < 1e-4:
        print("converged")
        break
    prev_k = scalars["k_eff"]
```

**When:** stages mutually depend on one another's scalar outputs. Always cap the iteration count and log Δ at every step — divergence is the failure mode and it must be caught before it consumes the cluster.

### Pattern C — Hierarchical Pipeline (Pipeline-of-Pipelines)

Each top-level stage is itself a complete cross-domain mini-pipeline. The outer pipeline composes the *summaries* of the inner pipelines, not their raw amplitudes — this keeps orchestration tractable as the system scales.

```python
def inner_drug_design(seed):
    """Inner pipeline: chemistry → biology → materials. Returns a compact summary."""
    chem = execute("chemistry","vqe",seed,
                   {"sub_module":"vqe_chemistry","task":"ground_state_energy"})
    bio  = execute("biomolecules","vqe",
                   amplitudes_from_result(chem,key="wavefunction_amplitudes"),
                   {"sub_module":"drug_discovery","task":"binding_affinity"})
    mat  = execute("materials_science","vqe",
                   amplitudes_from_result(bio,key="binding_amplitudes"),
                   {"sub_module":"soft_matter","task":"tablet_formulation_stability"})
    return {
        "amplitudes": amplitudes_from_result(mat, key="stability_amplitudes"),
        "scalars":    {"E0":chem["result"]["energy"],
                       "dG":bio["result"]["energy"],
                       "S": mat["result"]["stability_score"]}
    }

def inner_market(amps, scalars):
    """Inner pipeline: finance → ML. Returns valuation + outcome forecasts."""
    fin = execute("finance","qaoa", amps, {
        "sub_module":"portfolio","task":"drug_pipeline_valuation",
        "binding_dG":scalars["dG"],"stability_score":scalars["S"]})
    ml  = execute("machine_learning","vqe",
                  amplitudes_from_result(fin,key="valuation_amplitudes"),
                  {"sub_module":"quantum_kernel","task":"patient_outcome_regression"})
    return {"NPV":fin["result"]["expected_value"],
            "PFS_p50":ml["result"]["pfs_p50"]}

# Outer pipeline composes two inner pipelines
seeds = [normalize(np.random.default_rng(s).normal(size=65536)).tolist() for s in range(4)]
candidates = []
for i, seed in enumerate(seeds):
    design = inner_drug_design(seed)
    market = inner_market(design["amplitudes"], design["scalars"])
    candidates.append({"id":i, **design["scalars"], **market})

best = max(candidates, key=lambda c: c["NPV"])
print("best candidate:", best)
```

**When:** the problem decomposes into reusable sub-pipelines that you want to compose, swap, or run in batch. Hierarchical pipelines also make caching tractable — a single inner sub-pipeline can be memoized and reused across many outer runs.

### Pattern D — Streaming Sensitivity Sweep

Sweep an upstream parameter (e.g., temperature, dose, exchange rate) and stream the downstream chain for every value. Useful for risk maps, design-of-experiments, and Monte-Carlo-style quantum studies.

```python
def downstream(amps, scalar_kw):
    bio = execute("biomolecules","vqe",amps,
                  {"sub_module":"drug_discovery","task":"binding_affinity", **scalar_kw})
    fin = execute("finance","qaoa",
                  amplitudes_from_result(bio,key="binding_amplitudes"),
                  {"sub_module":"portfolio","task":"drug_pipeline_valuation"})
    return fin["result"]["expected_value"]

doses = [25, 50, 100, 200, 400, 800]   # mg
seed  = normalize(np.random.default_rng(10).normal(size=65536)).tolist()
sweep = {d: downstream(seed, {"dose_mg": d}) for d in doses}
print("dose -> NPV map:", sweep)
```

**When:** a single scalar is the dominant uncertainty and you need its full influence map across the downstream pipeline before committing to a design point.

---

## Tips for Robust Pipelines

- **Always re-normalize.** Each `amplitudes_from_result` call should re-Born-normalize the vector before sending it on.
- **Persist intermediates.** Save each stage's full JSON response — it lets you re-run the tail of the pipeline cheaply when only later parameters change.
- **Watch the qubit budget.** Every stage allocates `next_power_of_two(len(input_data))` qubits. Pad/truncate to the desired width (typically 65536) at every hand-off.
- **Use `config` for scalars, `input_data` for vectors.** Energies, affinities, and Reynolds numbers belong in `config`; field samples and amplitude vectors belong in `input_data`.
- **Fail fast.** If `response["success"] != true` at stage *k*, abort the pipeline before stage *k+1* — propagating bad amplitudes silently corrupts every downstream result.
