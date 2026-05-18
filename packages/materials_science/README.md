# Quantum Materials Science Package

## Overview

The Materials Science package provides quantum simulation of crystalline materials, superconductors, topological phases, magnetism, optical properties, and novel materials through the unified L3 VQE circuit at 65536-qubit scale. It encompasses **12 specialized sub-modules** covering the full spectrum of computational materials science — from atomic-scale crystal structure to many-body electron correlations and 2D materials.

**API Endpoint:** `POST http://localhost:8080/api/v1/quantum/execute`

**Demo Endpoint:** `POST http://localhost:8080/api/v1/quantum/materials_science/demo`

---

## The 12 Quantum Materials Science Sub-Modules

| # | Sub-Module | Source | Key Domain |
|---|-----------|--------|------------|
| 1 | Crystal Lattice | `crystal_lattice.rs` | Crystallography |
| 2 | Electronic Structure | `electronic_structure.rs` | DFT & Hartree-Fock |
| 3 | Magnetism | `magnetism.rs` | Spin & Magnetic Phenomena |
| 4 | Many-Body Perturbation | `many_body_perturbation.rs` | Green's Functions & GW |
| 5 | Optical Properties | `optical_properties.rs` | Light–Matter Interaction |
| 6 | Phonon Dynamics | `phonon_dynamics.rs` | Lattice Dynamics |
| 7 | Strongly Correlated | `strongly_correlated.rs` | DMFT & Hubbard |
| 8 | Superconductivity | `superconductivity.rs` | BCS & High-Tc |
| 9 | Surface & Interface | `surface_interface.rs` | Catalysis & Adsorption |
| 10 | Topological Phases | `topological_phases.rs` | Topological Invariants |
| 11 | Transport | `transport.rs` | Electronic & Thermal Transport |
| 12 | Two-Dimensional Materials | `two_dimensional_materials.rs` | Graphene & van der Waals |

---

## 1. Crystal Lattice

**Source:** `crystal_lattice.rs`

Quantum-accurate crystal structure and lattice calculations at atomic resolution, including Bohr-radius-scale conversions and lattice vector optimization.

**Key Capabilities:**
- 14 Bravais lattice classification (cubic, tetragonal, orthorhombic, hexagonal, etc.)
- Unit cell optimization and lattice constant refinement
- Bohr-radius / Ångström / picometer conversions for atomic-scale analysis
- Reciprocal lattice computation and Brillouin zone construction
- Wyckoff position assignment and space group symmetry detection
- Crystal defects: vacancies, interstitials, substitutional sites
- Strain tensor analysis and elastic constants

**When to Use:** Crystal structure determination, lattice constant prediction, defect formation energy, crystallographic phase identification.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "crystal_lattice",
    "task": "unit_cell_optimization",
    "material": "Si",
    "lattice_type": "cubic_diamond",
    "lattice_constant_angstrom": 5.431
  }
}
```

---

## 2. Electronic Structure

**Source:** `electronic_structure.rs`

Quantum electronic structure calculations with full support for exchange-correlation functionals (LDA, GGA, Meta-GGA), Hartree-Fock theory, and orbital analysis at 65536-qubit scale.

**Key Capabilities:**
- Density Functional Theory (DFT) with LDA, GGA (PBE, BLYP), Meta-GGA (SCAN, TPSS)
- Hartree-Fock (RHF, UHF, ROHF) self-consistent field
- Exchange-correlation functional library and benchmarking
- Kohn-Sham orbital decomposition and density of states (DOS)
- Band structure along high-symmetry k-paths
- Mulliken / Löwdin / Bader charge population analysis
- Hybrid functionals (B3LYP, HSE06, PBE0) with exact exchange

**When to Use:** Band gap prediction, ground-state energy, charge density, orbital analysis, materials property prediction.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "electronic_structure",
    "task": "band_structure",
    "material": "Si",
    "functional": "pbe",
    "k_path": "L-G-X-W-K-G",
    "num_bands": 32
  }
}
```

---

## 3. Magnetism

**Source:** `magnetism.rs`

Magnetic property calculations covering atomic moments, Landé g-factors, vacuum permeability, and magnetic field interactions in materials.

**Key Capabilities:**
- Bohr magneton (μ_B = 9.274 × 10⁻²⁴ J/T) computations
- Landé g-factor for atomic and ionic states
- Vacuum permeability μ₀ and magnetic susceptibility χ_m
- Magnetic field interactions (Zeeman effect, dipole-dipole)
- Magnetic ordering: ferromagnetic, antiferromagnetic, ferrimagnetic, helimagnetic
- Curie / Néel temperature prediction
- Spin-orbit coupling and magnetocrystalline anisotropy
- Heisenberg / Ising / XY model exchange parameters

**When to Use:** Magnetic phase diagrams, permanent magnet design, spintronics, magnetic anisotropy engineering.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "magnetism",
    "task": "magnetic_ordering",
    "material": "Fe2O3",
    "exchange_model": "heisenberg",
    "external_field_tesla": 1.0,
    "temperature_kelvin": 300.0
  }
}
```

---

## 4. Many-Body Perturbation

**Source:** `many_body_perturbation.rs`

Many-body perturbation theory using Green's functions G(k, ω), the GW approximation, and quasiparticle self-consistent calculations beyond mean-field DFT.

**Key Capabilities:**
- One-particle Green's function G(k, ω) construction
- GW approximation (G₀W₀, scGW, QSGW) for quasiparticle energies
- Bethe-Salpeter equation (BSE) for optical excitations
- Self-energy Σ(k, ω) computation and analytical continuation
- Spectral function A(k, ω) and ARPES simulation
- T-matrix and FLEX approximations
- Random Phase Approximation (RPA) screened Coulomb W

**When to Use:** Quasiparticle band gaps, accurate ionization potentials, photoemission spectra, beyond-DFT quasiparticle physics.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "many_body_perturbation",
    "task": "gw_quasiparticle",
    "material": "GaAs",
    "scheme": "g0w0",
    "num_bands": 100,
    "frequency_grid_points": 256
  }
}
```

---

## 5. Optical Properties

**Source:** `optical_properties.rs`

Optical and dielectric properties of materials, including frequency-dependent dielectric function, absorption spectra, fine-structure constant, and light-matter interaction.

**Key Capabilities:**
- Frequency-dependent dielectric function ε(ω) = ε₁(ω) + iε₂(ω)
- Absorption coefficient α(ω) and refractive index n(ω)
- Fine-structure constant α ≈ 1/137.036 in optical formulas
- Drude-Lorentz model for metals and semiconductors
- Excitonic absorption (Wannier-Mott and Frenkel)
- Optical transitions (direct vs indirect band gaps)
- Reflectivity, transmittance, ellipsometric Ψ/Δ
- Nonlinear optics: second-harmonic generation, Kerr effect

**When to Use:** Photovoltaic absorber design, transparent conductor engineering, LED and laser materials, ellipsometry analysis.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "optical_properties",
    "task": "dielectric_function",
    "material": "GaN",
    "energy_range_eV": [0.0, 10.0],
    "energy_points": 1024,
    "include_excitons": true
  }
}
```

---

## 6. Phonon Dynamics

**Source:** `phonon_dynamics.rs`

Lattice dynamics, phonon dispersion, and thermal properties from first principles, including THz–meV unit conversions and Debye-model approximations.

**Key Capabilities:**
- Phonon dispersion ω(q) along high-symmetry paths
- Density of phonon states (PhDOS) and projected PhDOS
- THz / meV / cm⁻¹ / Kelvin frequency conversions
- Debye temperature θ_D and Debye-model heat capacity
- Anharmonic effects and phonon-phonon scattering
- Thermal conductivity (lattice contribution) via Boltzmann transport
- Electron-phonon coupling λ for transport and superconductivity
- Grüneisen parameter γ for thermal expansion

**When to Use:** Thermal conductivity prediction, thermoelectric optimization, Raman/IR spectra, Debye temperature determination.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "phonon_dynamics",
    "task": "phonon_dispersion",
    "material": "Si",
    "q_path": "L-G-X-W",
    "supercell": [4, 4, 4],
    "include_anharmonic": true
  }
}
```

---

## 7. Strongly Correlated

**Source:** `strongly_correlated.rs`

Strongly correlated electron systems beyond the mean-field regime — Dynamical Mean-Field Theory (DMFT), Hubbard models, and Mott metal-insulator transitions.

**Key Capabilities:**
- DMFT self-consistent loop with quantum impurity solvers
- Single-band and multi-band Hubbard model construction
- Mott metal-insulator transition characterization
- Slave-boson and slave-fermion mean-field theories
- Anderson impurity model (single, two-channel, multi-orbital)
- DMFT + DFT (LDA+DMFT) for realistic correlated materials
- Quasiparticle weight Z and effective mass m*/m
- Hund's coupling J effects in multi-orbital systems

**When to Use:** Correlated transition-metal oxides, heavy-fermion systems, Mott insulators, high-Tc cuprate parent compounds.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "strongly_correlated",
    "task": "dmft_self_consistency",
    "material": "V2O3",
    "hubbard_u_eV": 4.0,
    "hund_j_eV": 0.7,
    "num_orbitals": 3
  }
}
```

---

## 8. Superconductivity

**Source:** `superconductivity.rs`

Superconductor properties from BCS theory through high-Tc and unconventional pairing — critical fields, coherence lengths, and the magnetic flux quantum.

**Key Capabilities:**
- BCS gap equation Δ(T) and Tc determination
- Critical fields H_c1, H_c2, H_c (Type-I / Type-II classification)
- Coherence length ξ and London penetration depth λ_L
- Magnetic flux quantum Φ₀ = h / 2e ≈ 2.067 × 10⁻¹⁵ Wb
- Eliashberg theory with electron-phonon spectral function α²F(ω)
- Unconventional pairing: d-wave, p-wave, s±-wave
- Vortex lattice and Abrikosov flux state
- Josephson effect and SQUID modeling

**When to Use:** High-Tc materials discovery, superconducting magnet design, Josephson-junction devices, vortex physics.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "superconductivity",
    "task": "bcs_gap_equation",
    "material": "MgB2",
    "pairing_symmetry": "s_wave",
    "temperature_kelvin": 10.0
  }
}
```

---

## 9. Surface & Interface

**Source:** `surface_interface.rs`

Surface physics, heterogeneous catalysis, interface electronic states, and work-function engineering for energy and electronic devices.

**Key Capabilities:**
- Adsorption energy E_ads on metal and oxide surfaces
- Catalytic reaction barrier estimation (transition states)
- Work function Φ and surface dipole calculation
- Schottky barrier height at metal-semiconductor interfaces
- Band alignment at heterojunctions (Type I / II / III)
- Surface reconstructions (e.g., Si(100)-2×1, Au(111) herringbone)
- Image-charge corrections for charged defects at surfaces
- Sabatier-principle volcano plots for catalyst screening

**When to Use:** Heterogeneous catalyst design, transistor interface engineering, photocatalysis, surface science research.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "surface_interface",
    "task": "adsorption_energy",
    "surface": "Pt(111)",
    "adsorbate": "CO",
    "coverage": 0.25,
    "site": "atop"
  }
}
```

---

## 10. Topological Phases

**Source:** `topological_phases.rs`

Topological insulators, Chern insulators, Weyl/Dirac semimetals, edge states, and topological invariants for non-trivial band topology.

**Key Capabilities:**
- Chern number C ∈ ℤ and ℤ₂ topological invariant calculation
- Topological insulators: 2D quantum spin Hall, 3D strong/weak TI
- Weyl and Dirac semimetal nodal-point identification
- Edge / surface state Hamiltonian and Fermi-arc visualization
- Wilson loops and hybrid Wannier-charge centers
- Berry curvature Ω(k) integration over the Brillouin zone
- Higher-order topological insulators (corner / hinge states)
- Time-reversal, particle-hole, and chiral symmetry classification (AZ table)

**When to Use:** Topological qubit substrate design, topological photonics, robust spin transport, Majorana platforms.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "topological_phases",
    "task": "chern_number",
    "material": "Bi2Se3",
    "k_grid": [64, 64, 1],
    "num_occupied_bands": 8
  }
}
```

---

## 11. Transport

**Source:** `transport.rs`

Electronic, thermal, and thermoelectric transport — conductance quantum, Lorenz number, Fermi-Dirac statistics, and Seebeck/Peltier coefficients.

**Key Capabilities:**
- Conductance quantum G₀ = 2e²/h ≈ 7.748 × 10⁻⁵ S
- Lorenz number L₀ = π²/3 (k_B/e)² and Wiedemann-Franz law
- Fermi-Dirac distribution and chemical potential evaluation
- Boltzmann transport equation (BTE) for σ, κ, S
- Seebeck coefficient S(T) and thermoelectric figure of merit ZT
- Peltier and Thomson coefficients
- Hall coefficient and magnetoresistance
- Ballistic, diffusive, and quantum-coherent transport regimes

**When to Use:** Thermoelectric ZT optimization, semiconductor device physics, quantum point contacts, mesoscopic transport.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "transport",
    "task": "thermoelectric_zt",
    "material": "Bi2Te3",
    "temperature_kelvin": 300.0,
    "carrier_concentration_cm3": 1e19
  }
}
```

---

## 12. Two-Dimensional Materials

**Source:** `two_dimensional_materials.rs`

Two-dimensional materials including graphene, transition-metal dichalcogenides (TMDs), heterostructures, and van der Waals interactions.

**Key Capabilities:**
- Graphene electronic structure: Dirac cones, Klein tunneling, pseudo-spin
- TMDs: MoS₂, WSe₂, MoTe₂ — direct/indirect band gaps, valley physics
- Twisted bilayer graphene and moiré superlattices (magic angles)
- van der Waals heterostructure stacking and band alignment
- Spin-valley coupling and Berry curvature in TMDs
- Excitons in 2D: Wannier-Mott with reduced screening
- Ripples, strain engineering, and pseudo-magnetic fields
- Layer-dependent properties (monolayer → bulk crossover)

**When to Use:** Graphene electronics, valleytronics, 2D photodetectors, twisted-bilayer superconductivity, vdW device design.

```json
{
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...65536 floats..."],
  "config": {
    "sub_module": "two_dimensional_materials",
    "task": "moire_band_structure",
    "material": "twisted_bilayer_graphene",
    "twist_angle_degrees": 1.05,
    "num_moire_bands": 20
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
  "domain": "materials_science",
  "algorithm": "vqe",
  "input_data": [/* 65536 float amplitude values */],
  "config": {
    "sub_module": "<module_name>"
  }
}
```

**Demo endpoint (no input_data required):**

```
POST http://localhost:8080/api/v1/quantum/materials_science/demo
```

---

## Scale

- **Qubits:** 65536
- **Maximum unit cell:** 8192 atoms with periodic boundaries
- **k-point mesh:** Up to 256×256×1 Brillouin zone sampling
- **Total materials science source:** 12 modules covering crystal-to-correlated-electron physics

---

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **VQE** | Ground state of crystal Hamiltonians |
| **DMFT** | Dynamical Mean-Field Theory for correlated electrons |
| **QPE** | Precise band gap and eigenvalue computation |
| **Quantum Monte Carlo** | Electron correlation in periodic systems |
| **ADAPT-VQE** | Adaptive ansatz for complex crystal structures |
| **QITE** | Thermal properties and phase transitions |

---

## Python Example (Full Workflow)

```python
import requests
import numpy as np

API = "http://localhost:8080/api/v1/quantum/execute"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}

# Generate 65536 amplitude-encoded materials state
rng = np.random.RandomState(42)
amplitudes = rng.normal(0, 1, 65536)
amplitudes = (amplitudes / np.linalg.norm(amplitudes)).tolist()

# Example: Topological phases - Chern number
response = requests.post(API, headers=HEADERS, json={
    "domain": "materials_science",
    "algorithm": "vqe",
    "input_data": amplitudes,
    "config": {
        "sub_module": "topological_phases",
        "task": "chern_number",
        "material": "Bi2Se3"
    }
})
print(response.json())

# Example: Superconductivity - BCS gap
response = requests.post(API, headers=HEADERS, json={
    "domain": "materials_science",
    "algorithm": "vqe",
    "input_data": amplitudes,
    "config": {
        "sub_module": "superconductivity",
        "task": "bcs_gap_equation",
        "material": "MgB2",
        "temperature_kelvin": 10.0
    }
})
print(response.json())
```

---

## Use Cases

| Research Area | Relevant Sub-Modules |
|---------------|---------------------|
| **High-Tc Superconductor Discovery** | Superconductivity, Strongly Correlated, Electronic Structure |
| **Battery & Energy Materials** | Crystal Lattice, Electronic Structure, Transport |
| **Semiconductor Design** | Electronic Structure, Optical Properties, Many-Body Perturbation |
| **Topological Quantum Computing** | Topological Phases, Two-Dimensional Materials |
| **Thermoelectrics** | Transport, Phonon Dynamics, Electronic Structure |
| **Heterogeneous Catalysis** | Surface & Interface, Electronic Structure |
| **Spintronics & Magnetism** | Magnetism, Topological Phases, Two-Dimensional Materials |
| **Photovoltaics & LEDs** | Optical Properties, Electronic Structure |
| **2D Devices & Valleytronics** | Two-Dimensional Materials, Topological Phases |
| **Correlated Quantum Materials** | Strongly Correlated, Many-Body Perturbation, Magnetism |
