# Quantum Physics Package

## Overview

The Physics package provides quantum simulation of fundamental physical systems through the unified L3 VQE circuit at 65536-qubit scale. It encompasses **13 specialized sub-modules** covering the full spectrum of quantum physics — from quantum field theory and quantum gravity to quantum cosmology and metrology.

**API Endpoint:** `POST http://localhost:8080/api/v1/quantum/execute`

**Demo Endpoint:** `POST http://localhost:8080/api/v1/quantum/physics/demo`

---

## The 13 Quantum Physics Sub-Modules

| # | Sub-Module | Source | Key Domain |
|---|-----------|--------|------------|
| 1 | Quantum Field Theory | `quantum_field_theory.rs` | QFT & Gauge Theory |
| 2 | Quantum Electrodynamics | `quantum_electrodynamics.rs` | QED Interactions |
| 3 | Quantum Chromodynamics | `quantum_chromodynamics.rs` | Strong Force |
| 4 | Relativistic Quantum Mechanics | `relativistic_quantum_mechanics.rs` | Relativistic Dynamics |
| 5 | Quantum Gravity | `quantum_gravity.rs` | Planck-Scale Physics |
| 6 | Quantum Entanglement Theory | `quantum_entanglement_theory.rs` | Bell Inequalities |
| 7 | Quantum Optics | `quantum_optics.rs` | Photonic States |
| 8 | Quantum Thermodynamics | `quantum_thermodynamics.rs` | Quantum Heat Engines |
| 9 | Quantum Chaos | `quantum_chaos.rs` | Random Matrix Theory |
| 10 | Open Quantum Systems | `open_quantum_systems.rs` | Decoherence |
| 11 | Quantum Phase Transitions | `quantum_phase_transitions.rs` | Critical Phenomena |
| 12 | Quantum Metrology | `quantum_metrology.rs` | Precision Measurement |
| 13 | Quantum Cosmology | `quantum_cosmology.rs` | Early Universe |

---

## 1. Quantum Field Theory

**Source:** `quantum_field_theory.rs`

Core quantum field theory with scalar field, gauge theory, and lattice QCD simulations. Encodes fundamental physical constants (speed of light, Planck's constant, α_QED) for ab initio field-theoretic calculations.

**Key Capabilities:**
- Lorentz 4-vectors and Minkowski metric operations
- Dirac gamma matrices and spinor field representations
- Scalar, fermion, and gauge propagators (Feynman rules)
- Feynman diagram evaluation and loop corrections
- Renormalization: beta functions, RG flow, counterterms
- Standard Model particles (CKM matrix, quark/lepton properties)
- Path integral formulation and functional methods
- Spontaneous symmetry breaking (Mexican hat potential, Higgs mechanism)
- Scattering amplitudes (Mandelstam variables, ee→μμ, Compton, Møller, Bhabha)
- Effective Field Theory (Wilson coefficients, Fermi theory, SMEFT)

**When to Use:** Particle physics calculations, cross-section predictions, running coupling constants, BSM physics constraints.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_field_theory",
    "task": "scattering_amplitude",
    "process": "ee_to_mumu",
    "center_of_mass_energy": 91.2,
    "coupling_constant": 0.00729735
  }
}
```

---

## 2. Quantum Electrodynamics

**Source:** `quantum_electrodynamics.rs`

QED calculations including lepton masses (electron, muon, tau), Bohr radius, and Thomson cross-section. Quantum electromagnetic interactions at multi-loop precision.

**Key Capabilities:**
- Vacuum polarization and running coupling α(q²) (Uehling potential)
- Electromagnetic form factors (Dirac and Pauli)
- Anomalous magnetic moment (electron/muon to 5-loop precision)
- Lamb shift computation (hydrogen fine structure)
- Pair production and annihilation cross-sections
- Schwinger effect (vacuum pair creation in strong fields)
- Bremsstrahlung radiation spectra
- Euler-Heisenberg effective Lagrangian
- Positronium and muonium bound state spectroscopy

**When to Use:** Precision QED tests, lepton g-2 calculations, atomic spectroscopy, strong-field QED phenomena.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_electrodynamics",
    "task": "anomalous_magnetic_moment",
    "particle": "muon",
    "loop_order": 5
  }
}
```

---

## 3. Quantum Chromodynamics

**Source:** `quantum_chromodynamics.rs`

Strong interaction physics with QCD coupling constants, quark condensate, gluon condensate. Lattice QCD simulations at 65536-qubit scale.

**Key Capabilities:**
- SU(3) color algebra (Gell-Mann matrices, structure constants)
- Running coupling α_s(Q²) at 4-loop order (RK4 integration)
- Confinement modeling (Cornell potential, quarkonium spectroscopy)
- Deep inelastic scattering (DGLAP splitting functions, parton distributions)
- Jet physics and event shape variables
- Heavy Quark Effective Theory (HQET)
- Perturbative QCD (K-factors, NLO/NNLO corrections)
- QCD sum rules (SVZ, Borel transform)

**When to Use:** Hadron spectroscopy, jet cross-sections, parton distribution fitting, heavy quark physics.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_chromodynamics",
    "task": "running_coupling",
    "energy_scale_gev": 91.2,
    "loop_order": 4,
    "n_flavors": 5
  }
}
```

---

## 4. Relativistic Quantum Mechanics

**Source:** `relativistic_quantum_mechanics.rs`

Klein-Gordon and Dirac equation implementations. Relativistic particle dynamics with Compton wavelength and Rydberg energy calculations.

**Key Capabilities:**
- Klein-Gordon equation (Coulomb problem, bound states)
- Dirac hydrogen atom (exact Sommerfeld formula)
- Zitterbewegung (trembling motion of Dirac particles)
- Klein paradox (barrier transmission in relativistic regime)
- Relativistic corrections (Darwin term, spin-orbit coupling)
- Foldy-Wouthuysen transformation (non-relativistic limit)
- Mott scattering (relativistic Coulomb scattering)
- Helicity and chirality projections

**When to Use:** Relativistic atomic physics, heavy-element calculations, positron physics, relativistic correction evaluation.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "relativistic_quantum_mechanics",
    "task": "dirac_hydrogen",
    "principal_quantum_number": 2,
    "angular_momentum": 1,
    "nuclear_charge": 92
  }
}
```

---

## 5. Quantum Gravity

**Source:** `quantum_gravity.rs`

Planck-scale physics including gravitational constant, Planck mass/length/time/energy/temperature. Quantum gravity simulations bridging general relativity and quantum mechanics.

**Key Capabilities:**
- Schwarzschild and Kerr black hole solutions
- Hawking radiation spectrum and temperature
- Black hole entropy (Bekenstein-Hawking formula)
- Black hole evaporation dynamics
- Unruh effect (accelerated observer radiation)
- Loop Quantum Gravity (area quantization, spin foam amplitudes)
- Generalized Uncertainty Principle (minimum length, remnant mass)
- Black hole information paradox (Page curve, scrambling time)
- Graviton properties and semiclassical gravity

**When to Use:** Black hole thermodynamics, quantum gravitational corrections, Planck-scale phenomenology, holographic entropy.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_gravity",
    "task": "hawking_radiation",
    "black_hole_mass_solar": 10.0,
    "spin_parameter": 0.7
  }
}
```

---

## 6. Quantum Entanglement Theory

**Source:** `quantum_entanglement_theory.rs`

Bell inequality tests (CHSH, Mermin, Svetlichny, TiltedBell). Measures and quantifies quantum entanglement in multi-party systems.

**Key Capabilities:**
- CHSH inequality violation (Tsirelson bound 2√2)
- Mermin inequality for N-party GHZ states
- Svetlichny inequality (genuine tripartite nonlocality)
- Entanglement measures: concurrence, negativity, entanglement of formation
- Quantum teleportation fidelity
- Entanglement distillation (BBPSSW protocol)
- Multipartite states: GHZ, W, cluster, Dicke
- Entanglement dynamics (sudden death and revival)

**When to Use:** Bell test experiments, entanglement verification, quantum network certification, quantum communication protocols.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_entanglement_theory",
    "task": "bell_inequality",
    "inequality_type": "chsh",
    "num_parties": 2,
    "state_type": "maximally_entangled"
  }
}
```

---

## 7. Quantum Optics

**Source:** `quantum_optics.rs`

Fock state operations, photonic quantum states, coherent state manipulation. Quantum optical systems with vacuum permittivity and cavity QED dynamics.

**Key Capabilities:**
- Fock states (number states, creation/annihilation operators)
- Coherent states (Glauber states, displacement operator)
- Squeezed states (single-mode and two-mode squeezing)
- Thermal states (Bose-Einstein distribution)
- Jaynes-Cummings model (Rabi oscillations, collapse-revival, Purcell effect)
- Photon correlations: g⁽²⁾(τ), antibunching, bunching
- Beam splitter transformations (Hong-Ou-Mandel effect)
- Wigner function phase-space representation
- Quantum noise limits (shot noise, squeezed light)

**When to Use:** Cavity QED design, photon statistics analysis, quantum state engineering, quantum communication hardware.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_optics",
    "task": "jaynes_cummings",
    "atom_cavity_coupling": 0.05,
    "detuning": 0.0,
    "photon_number": 10,
    "time_steps": 100
  }
}
```

---

## 8. Quantum Thermodynamics

**Source:** `quantum_thermodynamics.rs`

Quantum Otto cycle and heat engine implementations. Quantum thermodynamic processes with temperature-dependent dynamics and work extraction.

**Key Capabilities:**
- Quantum Otto cycle (efficiency and power output)
- Quantum Carnot engine (maximum efficiency bound)
- Jarzynski equality (nonequilibrium work relations)
- Crooks fluctuation theorem
- Landauer's principle (minimum erasure cost: kT ln2)
- Quantum batteries (ergotropy, charging power)
- Thermodynamic uncertainty relations
- Quantum work and heat definitions

**When to Use:** Quantum heat engine design, nanoscale thermodynamics, information-to-energy conversion, quantum battery optimization.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_thermodynamics",
    "task": "quantum_otto_cycle",
    "hot_temperature": 1000.0,
    "cold_temperature": 300.0,
    "compression_ratio": 4.0
  }
}
```

---

## 9. Quantum Chaos

**Source:** `quantum_chaos.rs`

Random matrix theory ensembles (GOE, GUE, GSE, Poisson). Quantum chaotic dynamics and level statistics for complex quantum systems.

**Key Capabilities:**
- Random Matrix Theory ensembles: GOE, GUE, GSE
- Level spacing statistics (Wigner surmise vs Poisson)
- Out-of-time-order correlator (OTOC, MSS scrambling bound)
- Eigenstate Thermalization Hypothesis (ETH) verification
- Spectral form factor (dip-ramp-plateau)
- Quantum kicked rotor (dynamical localization)
- SYK model (Sachdev-Ye-Kitaev) spectral properties

**When to Use:** Quantum chaos diagnostics, scrambling time estimates, thermalization studies, many-body chaos characterization.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_chaos",
    "task": "level_statistics",
    "ensemble": "gue",
    "matrix_dimension": 1024,
    "num_samples": 10000
  }
}
```

---

## 10. Open Quantum Systems

**Source:** `open_quantum_systems.rs`

Density matrix representations and Bloch vector formalism. Decoherence, dissipative quantum dynamics, and quantum channel characterization.

**Key Capabilities:**
- Lindblad master equation evolution
- Decoherence modeling (T₁ relaxation, T₂ dephasing)
- Quantum channels: depolarizing, amplitude damping, phase damping
- Channel capacities (classical and quantum)
- Non-Markovianity measures (BLP, spectral density)
- Quantum Zeno effect (frequent measurement freezing)
- Decoherence-free subspaces identification

**When to Use:** Noise characterization, quantum error analysis, open system dynamics, quantum device decoherence modeling.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "open_quantum_systems",
    "task": "lindblad_evolution",
    "t1_relaxation": 50e-6,
    "t2_dephasing": 30e-6,
    "evolution_time": 100e-6,
    "num_qubits": 4
  }
}
```

---

## 11. Quantum Phase Transitions

**Source:** `quantum_phase_transitions.rs`

Transverse field Ising model and phase diagram analysis. Quantum critical phenomena and symmetry breaking at 65536-qubit scale.

**Key Capabilities:**
- Transverse-field Ising model (exact 1D solution)
- Critical exponents (2D/3D Ising, Heisenberg, mean-field universality)
- Scaling relations (hyperscaling, Rushbrooke, Josephson)
- BKT transition (Berezinskii-Kosterlitz-Thouless, XY model)
- Kibble-Zurek mechanism (defect formation in quenches)
- Bose-Hubbard model (superfluid-Mott insulator transition)

**When to Use:** Phase diagram mapping, critical exponent extraction, quantum simulator benchmarking, topological phase identification.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_phase_transitions",
    "task": "transverse_ising",
    "lattice_size": 256,
    "transverse_field": 1.0,
    "coupling_j": 1.0,
    "temperature": 0.0
  }
}
```

---

## 12. Quantum Metrology

**Source:** `quantum_metrology.rs`

Quantum Fisher information and parameter estimation. Precision measurement using quantum resources at the Heisenberg limit.

**Key Capabilities:**
- Quantum Fisher Information (QFI) computation
- Standard Quantum Limit (SQL) vs Heisenberg limit scaling
- Ramsey interferometry (atomic clock precision)
- Mach-Zehnder interferometer (phase sensitivity)
- Quantum magnetometry (SQUID-level sensitivity)
- Quantum gravimetry (gravitational sensing)
- Adaptive phase estimation protocols
- Cramér-Rao bound saturation

**When to Use:** Quantum sensor design, atomic clock optimization, gravitational wave detection, magnetic field imaging.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_metrology",
    "task": "fisher_information",
    "num_probe_particles": 1000,
    "state_type": "noon_state",
    "parameter": "phase"
  }
}
```

---

## 13. Quantum Cosmology

**Source:** `quantum_cosmology.rs`

Early universe quantum dynamics with CMB temperature, Hubble constant, cosmological parameters. Quantum aspects of cosmology and the origin of structure.

**Key Capabilities:**
- Wheeler-DeWitt equation (mini-superspace quantization)
- Tunneling wave functions (Vilenkin, Hartle-Hawking no-boundary)
- Slow-roll inflation (spectral index n_s, tensor-to-scalar ratio r)
- Primordial power spectrum (Planck 2018 consistency)
- Loop quantum cosmology (quantum bounce, singularity resolution)
- De Sitter quantum effects (Gibbons-Hawking temperature)
- Spectral running and higher-order inflationary observables

**When to Use:** Inflationary model comparison, CMB prediction, quantum origin of perturbations, early universe dynamics.

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "quantum_cosmology",
    "task": "inflation_observables",
    "model": "slow_roll",
    "e_folds": 60,
    "hubble_parameter": 67.4
  }
}
```

---

## General Request Format

All sub-modules are accessed through the unified quantum execution endpoint:

```
POST http://localhost:8080/api/v1/quantum/execute
```

**Request body:**

```json
{
  "domain": "physics",
  "algorithm": "vqe",
  "input_data": [/* 65536 float amplitude values */],
  "config": {
    "sub_module": "<module_name>"
  }
}
```

**Demo endpoint (no input_data required):**

```
POST http://localhost:8080/api/v1/quantum/physics/demo
```

---

## Scale

- **Qubits:** 65536
- **Maximum lattice:** 256×256 sites (65536 spins)
- **Total physics source:** 13 modules covering all fundamental physics domains

---

## Python Example (Full Workflow)

```python
import requests
import numpy as np

API = "http://localhost:8080/api/v1/quantum/execute"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}

# Generate 65536 amplitude-encoded quantum state
rng = np.random.RandomState(42)
amplitudes = rng.normal(0, 1, 65536)
amplitudes = (amplitudes / np.linalg.norm(amplitudes)).tolist()

# Example: Quantum field theory scattering
response = requests.post(API, headers=HEADERS, json={
    "domain": "physics",
    "algorithm": "vqe",
    "input_data": amplitudes,
    "config": {
        "sub_module": "quantum_field_theory",
        "task": "scattering_amplitude",
        "process": "ee_to_mumu",
        "center_of_mass_energy": 91.2
    }
})
print(response.json())

# Example: Black hole Hawking radiation
response = requests.post(API, headers=HEADERS, json={
    "domain": "physics",
    "algorithm": "vqe",
    "input_data": amplitudes,
    "config": {
        "sub_module": "quantum_gravity",
        "task": "hawking_radiation",
        "black_hole_mass_solar": 10.0
    }
})
print(response.json())
```

---

## Use Cases

| Research Area | Relevant Sub-Modules |
|---------------|---------------------|
| **Particle Physics & Collider** | Quantum Field Theory, QED, QCD |
| **Precision Atomic Physics** | QED, Relativistic Quantum Mechanics |
| **Black Hole & Gravity** | Quantum Gravity, Quantum Cosmology |
| **Quantum Information** | Quantum Entanglement Theory, Quantum Optics |
| **Condensed Matter & Materials** | Quantum Phase Transitions, Open Quantum Systems |
| **Quantum Computing Hardware** | Open Quantum Systems, Quantum Chaos, Quantum Metrology |
| **Cosmology & Early Universe** | Quantum Cosmology, Quantum Gravity |
| **Quantum Thermodynamics** | Quantum Thermodynamics, Quantum Chaos |
| **Sensing & Measurement** | Quantum Metrology, Quantum Optics |
| **Fundamental Tests** | Quantum Entanglement Theory, QED, Relativistic QM |
