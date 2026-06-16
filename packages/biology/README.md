# Quantum Biology Package

## Overview

The Biology package provides quantum simulation of biological systems through the unified VQE engine at 2^53-qubit scale. It encompasses **14 specialized sub-modules** covering the full spectrum of computational biology — from nucleotide thermodynamics to systems-level metabolic modeling.

**API Endpoint:** `POST http://localhost:8080/api/v1/quantum/execute`

**Demo Endpoint:** `POST http://localhost:8080/api/v1/quantum/biomolecules/demo`

---

## The 14 Quantum Biology Sub-Modules

| # | Sub-Module | Key Domain |
|---|-----------|------------|
| 1 | DNA/RNA  | Genomics |
| 2 | Drug Discovery  | Pharmacology |
| 3 | Enzyme Catalysis  | Biochemistry |
| 4 | Glycobiology  | Carbohydrate Science |
| 5 | Membrane Biophysics  | Cell Biology |
| 6 | Metabolic Networks  | Systems Biology |
| 7 | Molecular Dynamics  | Biophysics |
| 8 | Neurochemistry  | Neuroscience |
| 9 | Photosynthesis  | Plant Biology |
| 10 | Protein Folding  | Structural Biology |
| 11 | Protein-Protein Interactions  | Interactomics |
| 12 | Quantum Virology  | Virology |
| 13 | Structural Biology  | Crystallography |
| 14 | Systems Biology  | Network Biology |

---

## 1. DNA/RNA


Quantum-accurate nucleic acid simulation covering base encoding, Watson-Crick pairing thermodynamics, and structural dynamics.

**Key Capabilities:**
- Nucleotide base encoding (A, T/U, G, C) with quantum amplitude representation
- Watson-Crick base pairing energetics and hydrogen bond modeling
- DNA/RNA thermodynamics: melting temperature, free energy of hybridization
- Secondary structure prediction (hairpins, loops, stems)
- Codon translation and reading frame analysis

**When to Use:** Genomic sequence analysis, primer design, RNA folding, mutation thermodynamic impact assessment.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "dna_rna",
    "sequence": "ATCGATCGATCG",
    "task": "hybridization_energy",
    "temperature": 310.15
  }
}
```

---

## 2. Drug Discovery


Comprehensive drug-likeness evaluation and quantum-enhanced virtual screening combining classical ADMET filters with quantum binding affinity calculations.

**Key Capabilities:**
- Lipinski's Rule of Five (MW ≤ 500, LogP ≤ 5, HBD ≤ 5, HBA ≤ 10)
- Veber rules (rotatable bonds ≤ 10, TPSA ≤ 140 Å²)
- Ghose filter (160 ≤ MW ≤ 480, −0.4 ≤ LogP ≤ 5.6)
- QED (Quantitative Estimate of Drug-likeness) scoring
- Quantum binding free energy via VQE on protein-ligand complexes
- Pharmacophore mapping and lead optimization scoring

**When to Use:** Lead compound screening, ADMET prediction, binding affinity ranking, hit-to-lead optimization.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "drug_discovery",
    "task": "drug_likeness",
    "molecule_smiles": "CC(=O)Oc1ccccc1C(=O)O",
    "target_pdb": "1HBB"
  }
}
```

---

## 3. Enzyme Catalysis


Quantum simulation of enzyme kinetics, catalytic mechanisms, and transition state theory at atomic resolution.

**Key Capabilities:**
- Michaelis-Menten kinetics (Km, Vmax, kcat determination)
- Inhibition modeling: competitive, uncompetitive, non-competitive, mixed
- Diffusion-limited catalysis (Smoluchowski limit)
- Transition state stabilization energy calculations
- Enzyme-substrate binding geometry optimization
- Catalytic efficiency (kcat/Km) prediction

**When to Use:** Enzyme engineering, inhibitor design, catalytic mechanism elucidation, industrial biocatalysis optimization.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "enzyme_catalysis",
    "task": "michaelis_menten",
    "enzyme": "lysozyme",
    "substrate_concentration": [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
  }
}
```

---

## 4. Glycobiology


Quantum modeling of carbohydrate structures, glycosidic bond energetics, and sugar-protein interactions.

**Key Capabilities:**
- Monosaccharide classification (aldoses, ketoses, pyranoses, furanoses)
- Glycosidic bond formation/cleavage energetics (α/β linkages)
- Lectin-carbohydrate binding affinity prediction
- Glycan branching pattern analysis
- Blood group antigen modeling

**When to Use:** Glycan structure-function studies, lectin binding prediction, glycoprotein engineering, vaccine carbohydrate design.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "glycobiology",
    "task": "glycosidic_bond_energy",
    "sugar": "glucose",
    "linkage": "beta_1_4"
  }
}
```

---

## 5. Membrane Biophysics


Quantum treatment of biological membrane systems including ion transport, electrochemistry, and channel gating.

**Key Capabilities:**
- Ion channel conductance modeling (Na⁺, K⁺, Ca²⁺, Cl⁻)
- Nernst equation (single-ion equilibrium potential)
- Goldman-Hodgkin-Katz equation (multi-ion resting potential)
- Membrane potential dynamics and action potential propagation
- Lipid bilayer phase transitions and fluidity
- Channel gating kinetics (voltage-gated, ligand-gated)

**When to Use:** Ion channel drug targeting, membrane transport studies, electrophysiology simulation, neuropharmacology.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "membrane_biophysics",
    "task": "membrane_potential",
    "ion_concentrations": {
      "K_in": 140.0, "K_out": 5.0,
      "Na_in": 12.0, "Na_out": 145.0
    },
    "temperature": 310.15
  }
}
```

---

## 6. Metabolic Networks


Quantum-enhanced metabolic pathway analysis combining flux balance with quantum optimization of reaction networks.

**Key Capabilities:**
- Flux balance analysis (FBA) with quantum optimization
- Gibbs free energy calculations for metabolic reactions
- Compartment modeling (cytoplasm, mitochondria, ER)
- Metabolic pathway flux optimization
- Stoichiometric matrix construction and analysis
- Thermodynamic feasibility assessment

**When to Use:** Metabolic engineering, pathway optimization, strain design, biofuel production modeling.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "metabolic_networks",
    "task": "flux_balance",
    "organism": "e_coli",
    "objective": "maximize_biomass"
  }
}
```

---

## 7. Molecular Dynamics


Full quantum molecular dynamics with classical force field integration for large-scale biomolecular trajectory simulation.

**Key Capabilities:**
- Force field evaluation (AMBER, CHARMM, OPLS parameter sets)
- Lennard-Jones 12-6 potential for van der Waals interactions
- Coulomb electrostatics with Ewald summation
- Trajectory integration (Verlet, velocity-Verlet, leapfrog)
- Temperature/pressure coupling (Berendsen, Nosé-Hoover)
- Periodic boundary conditions and minimum image convention

**When to Use:** Protein conformational sampling, ligand unbinding pathways, membrane dynamics, solvation free energy.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "molecular_dynamics",
    "task": "trajectory_simulation",
    "force_field": "amber",
    "timestep_fs": 2.0,
    "steps": 10000,
    "temperature": 300.0
  }
}
```

---

## 8. Neurochemistry


Quantum modeling of neurotransmitter systems, receptor pharmacology, and synaptic signal transduction.

**Key Capabilities:**
- 10 neurotransmitter types: dopamine, serotonin, GABA, glutamate, acetylcholine, norepinephrine, histamine, glycine, endorphin, anandamide
- Receptor binding kinetics (Kd, Ki, EC50, IC50)
- Synaptic vesicle dynamics (release, reuptake, degradation)
- Dose-response curves (Hill equation)
- Neurotransmitter synthesis pathway modeling
- Blood-brain barrier permeability prediction

**When to Use:** CNS drug design, neurotransmitter imbalance modeling, psychopharmacology, addiction research.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "neurochemistry",
    "task": "receptor_binding",
    "neurotransmitter": "dopamine",
    "receptor": "D2",
    "ligand_smiles": "CC(N)Cc1ccc(O)c(O)c1"
  }
}
```

---

## 9. Photosynthesis


Quantum coherence modeling in biological light-harvesting complexes and photosynthetic energy transfer.

**Key Capabilities:**
- Chromophore type classification (chlorophyll a/b, carotenoids, phycobilins)
- Quantum yield calculation for photosynthetic electron transfer
- Exciton dynamics and energy transfer (Förster/Dexter mechanisms)
- Light-harvesting complex geometry optimization
- Reaction center charge separation modeling
- Photoinhibition and photoprotection kinetics

**When to Use:** Artificial photosynthesis design, bioenergy optimization, light-harvesting antenna engineering.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "photosynthesis",
    "task": "exciton_transfer",
    "complex": "LHCII",
    "chromophores": ["chlorophyll_a", "chlorophyll_b", "lutein"]
  }
}
```

---

## 10. Protein Folding


Quantum energy landscape exploration for protein tertiary structure prediction with full amino acid representation.

**Key Capabilities:**
- All 20 standard amino acids with quantum-accurate side chain potentials
- Ramachandran plot analysis (φ/ψ backbone dihedral angles)
- Energy landscape exploration (folding funnels, metastable states)
- Secondary structure prediction (helix, sheet, coil)
- Disulfide bond formation energetics
- Solvent effects on folding thermodynamics

**When to Use:** Ab initio structure prediction, folding pathway analysis, protein engineering, misfolding disease research.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "protein_folding",
    "task": "energy_landscape",
    "sequence": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
    "temperature": 310.15
  }
}
```

---

## 11. Protein-Protein Interactions


Quantum-accurate modeling of macromolecular interfaces, binding energetics, and complex assembly.

**Key Capabilities:**
- Interface property calculation (buried surface area, shape complementarity)
- Solvent-accessible surface area (SASA) computation
- Binding free energy estimation (ΔG_binding)
- Hot-spot residue identification
- Electrostatic complementarity at interfaces
- Protein complex docking score prediction

**When to Use:** Antibody-antigen design, signaling complex modeling, PPI inhibitor development, protein engineering.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "protein_protein_interactions",
    "task": "binding_energy",
    "receptor_pdb": "1A2K",
    "ligand_pdb": "1A2L",
    "interface_residues": [45, 48, 52, 67, 71]
  }
}
```

---

## 12. Quantum Virology


Quantum geometric modeling of viral capsid structures, symmetry operations, and assembly pathways.

**Key Capabilities:**
- Capsid geometry optimization (icosahedral, helical, complex)
- Icosahedral symmetry operations (T-number classification)
- Triangulation number (T) analysis: T=1, T=3, T=4, T=7, T=13...
- Capsid protein subunit packing and quasi-equivalence
- Viral assembly pathway thermodynamics
- Capsid stability under environmental stress

**When to Use:** Antiviral drug design, vaccine nanoparticle engineering, virus-like particle design, structural virology.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "quantum_virology",
    "task": "capsid_geometry",
    "virus": "SARS-CoV-2",
    "t_number": 4,
    "symmetry": "icosahedral"
  }
}
```

---

## 13. Structural Biology


Quantum-enhanced structure determination methods including X-ray crystallography and scattering calculations.

**Key Capabilities:**
- X-ray scattering factor calculations (atomic form factors)
- Structure factor computation (F_hkl)
- Patterson function analysis
- Electron density map calculation
- B-factor (Debye-Waller) temperature factor modeling
- Resolution-dependent data quality assessment

**When to Use:** Crystallographic phasing, structure refinement, electron density interpretation, cryo-EM reconstruction.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "structural_biology",
    "task": "structure_factor",
    "pdb_id": "4HHB",
    "resolution": 2.0,
    "hkl_indices": [[1,0,0], [0,1,0], [1,1,0]]
  }
}
```

---

## 14. Systems Biology


Quantum network biology combining gene regulation modeling with systems-level pathway dynamics.

**Key Capabilities:**
- Hill function activation/repression (cooperativity modeling)
- Gene regulatory network (GRN) dynamics simulation
- Cooperativity coefficient determination
- Toggle switch and oscillator circuit modeling
- Boolean network attractors
- Sensitivity analysis for regulatory parameters

**When to Use:** Synthetic biology circuit design, gene regulation modeling, cellular decision-making, developmental biology.

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "systems_biology",
    "task": "gene_regulatory_network",
    "network_type": "toggle_switch",
    "hill_coefficient": 2.0,
    "num_genes": 50
  }
}
```

---

## General Request Format

> **Algorithm:** The user specifies `"algorithm"` per request. For biological energy minimization (protein folding, ligand binding, conformational sampling) the correct choice is `"algorithm": "vqe"` — VQE is the proper algorithm for energy/eigenvalue problems and is what every example in this package uses. The engine then compiles the requested algorithm onto the VQE execution substrate. Circuit depth is **automatically determined** by the engine based on input complexity; do not include `"depth"` in requests.

All sub-modules are accessed through the unified quantum execution endpoint:

```
POST http://localhost:8080/api/v1/quantum/execute
```

**Request body:**

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [/* N float amplitudes (up to 2^53 supported) */],
  "config": {
    "sub_module": "<feature_name>"
  }
}
```

**Demo endpoint (no input_data required):**

```
POST http://localhost:8080/api/v1/quantum/biomolecules/demo
```

---

## Scale

- **Qubits:** Up to 2^53 (9,007,199,254,740,992)
- **Maximum biomolecule:** 8738 atoms (hemoglobin-scale)

---

## Python Example (Full Workflow)

```python
import requests
import numpy as np

API = "http://localhost:8080/api/v1/quantum/execute"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}

# Generate amplitude-encoded biomolecular state
rng = np.random.RandomState(42)
amplitudes = rng.normal(0, 1, 1024)  # Example uses 1024; engine supports up to 2^53
amplitudes = (amplitudes / np.linalg.norm(amplitudes)).tolist()

# Example: Drug discovery screening
response = requests.post(API, headers=HEADERS, json={
    "domain": "biomolecules",
    "algorithm": "vqe",
    "input_data": amplitudes,
    "config": {
        "sub_module": "drug_discovery",
        "task": "drug_likeness",
        "molecule_smiles": "CC(=O)Oc1ccccc1C(=O)O"
    }
})
print(response.json())

# Example: Protein folding
response = requests.post(API, headers=HEADERS, json={
    "domain": "biomolecules",
    "algorithm": "vqe",
    "input_data": amplitudes,
    "config": {
        "sub_module": "protein_folding",
        "task": "energy_landscape",
        "sequence": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH"
    }
})
print(response.json())
```

---

## Use Cases

| Research Area | Relevant Sub-Modules |
|---------------|---------------------|
| **Drug Discovery & Design** | Drug Discovery, Protein-Protein Interactions, Enzyme Catalysis |
| **Genomics & Precision Medicine** | DNA/RNA, Systems Biology |
| **Neuroscience & CNS Drugs** | Neurochemistry, Membrane Biophysics |
| **Structural Biology** | Structural Biology, Protein Folding, Protein-Protein Interactions |
| **Infectious Disease** | Quantum Virology, Drug Discovery |
| **Metabolic Engineering** | Metabolic Networks, Enzyme Catalysis |
| **Bioenergy** | Photosynthesis, Metabolic Networks |
| **Glycoscience** | Glycobiology, Structural Biology |
| **Biophysics** | Molecular Dynamics, Membrane Biophysics |
| **Synthetic Biology** | Systems Biology, Metabolic Networks, Enzyme Catalysis |

---

### Continuum QFT for Biological Solvation

- Quantum field theoretic treatment of biological solvation environments
- Protein-water quantum interactions at continuum level
- Applications: enzyme catalysis in aqueous environment, membrane-solvent interfaces, drug bioavailability
- Enables accurate modeling of biological systems in their native aqueous environment

```json
{
  "domain": "biomolecules",
  "algorithm": "vqe",
  "input_data": [/* N amplitude floats (up to 2^53 supported) */],
  "config": {
    "sub_module": "molecular_dynamics",
    "task": "solvated_simulation",
    "protein_pdb": "4HHB",
    "solvent_model": "continuum_qft",
    "ionic_strength": 0.15,
    "temperature": 310.15
  }
}
```

---

## Input Method

### API Endpoint
```
POST http://localhost:8080/api/v1/quantum/execute
```

### Request Format
```json
{
  "problem": "protein_folding",
  "config": {
    "num_qubits": 1024,
    "optimizer": "SPSA",
    "max_iterations": 100
  },
  "input_data": [0.001, -0.003, 0.002, "...Born-normalized floats..."]
}
```

### Supported Problem Types
- `"protein_folding"` — Energy landscape exploration for tertiary structure prediction
- `"dna_sequence_analysis"` — Nucleic acid thermodynamics and structural analysis

### Data Input Options
- **Direct API**: Send JSON payload with amplitudes (Born-normalized floats)
- **File Import**: Upload binary/CSV data files via the import endpoint
- **Streaming**: For large datasets, use chunked streaming mode

---

## Hamiltonian Selection

### Available Hamiltonians
| Hamiltonian Type | Description | Use Case |
|---|---|---|
| Protein Interaction | Amino acid interaction potentials | Protein folding, binding affinity |
| Lattice Model | Coarse-grained lattice representation | Large-scale conformational sampling |
| HP Model | Hydrophobic-polar lattice model | Simplified folding studies |
| Force Field | AMBER/CHARMM/OPLS parameterized | Molecular dynamics at quantum accuracy |

### Configuration
```json
{
  "hamiltonian": {
    "type": "protein_interaction",
    "parameters": {
      "force_field": "amber",
      "solvent": "implicit",
      "temperature": 310.15
    }
  }
}
```

### Encoding Options
- **Jordan-Wigner**: Fermion-to-qubit mapping (default for molecular interactions)
- **Bravyi-Kitaev**: Reduced gate depth for large biomolecular systems
- **Direct Encoding**: For pre-computed interaction matrices

---

## Supported Scale

| Parameter | Maximum Value |
|---|---|
| **Qubits** | 2^53 (9,007,199,254,740,992) |
| **Bond Dimension** | 2^53 |
| **Precision** | IEEE 754 double (64-bit float) |

The quantum engine supports computations from small-scale (8 qubits) up to the theoretical maximum of 2^53 qubits with matching bond dimension, enabling simulation of molecular systems from simple hydrogen molecules to complex biological macromolecules and beyond.

