#!/usr/bin/env python3
"""
Nawaz1 Quantum VQE Engine - Complete Usage Examples
===================================================
Demonstrates ALL 16 quantum domains, 4 algorithms, VQS evolution,
pipeline execution, and multidimensional queries.

Author: Shahnawaz Alam
License: Proprietary
Copyright (c) 2026 Shahnawaz Alam. All rights reserved.

Requirements:
    - Python 3.8+
    - requests library (pip install requests)
    - Nawaz1 server running (default: http://localhost:8080)

Usage:
    python quantum_usage_examples.py              # Run all examples
    python quantum_usage_examples.py chemistry    # Run single domain
    python quantum_usage_examples.py --list       # List all domains
"""

import requests
import json
import sys
import os
import time

# =============================================================================
# Configuration
# =============================================================================
HOST = os.environ.get("NAWAZ1_HOST", "localhost")
PORT = os.environ.get("NAWAZ1_PORT", "8080")
BASE_URL = f"http://{HOST}:{PORT}/api/v1"
API_KEY = os.environ.get("NAWAZ1_API_KEY", "")

def get_headers():
    """Build request headers with optional API key."""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["X-API-Key"] = API_KEY
    return headers

def execute_quantum(payload, label=""):
    """Send a quantum execution request and display results."""
    url = f"{BASE_URL}/quantum/execute"
    print(f"\n{'='*70}")
    print(f"  {label}")
    print(f"{'='*70}")
    print(f"  Endpoint: POST {url}")
    print(f"  Payload:  {json.dumps(payload, indent=2)[:200]}...")
    
    try:
        start = time.time()
        resp = requests.post(url, json=payload, headers=get_headers(), timeout=120)
        elapsed = (time.time() - start) * 1000
        
        print(f"  Status:   {resp.status_code}")
        print(f"  Time:     {elapsed:.1f} ms")
        
        if resp.status_code == 200:
            result = resp.json()
            print(f"  Response: {json.dumps(result, indent=2)[:500]}")
            return result
        else:
            print(f"  Error:    {resp.text[:300]}")
            return None
    except requests.exceptions.ConnectionError:
        print("  ERROR: Cannot connect to server. Is nawaz1-server running?")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

# =============================================================================
# DOMAIN 1: Chemistry - Molecular Simulation
# =============================================================================
def demo_chemistry():
    """
    Chemistry domain: Simulates molecular ground-state energies using VQE.
    Applications: Drug discovery, catalyst design, materials prediction.
    """
    print("\n" + "="*70)
    print("  DOMAIN: CHEMISTRY - Molecular Quantum Simulation")
    print("  Computes ground-state energies via Variational Quantum Eigensolver")
    print("="*70)
    
    # Hydrogen molecule (H2) - full 65536-qubit precision
    execute_quantum({
        "domain": "chemistry",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "molecule": "H2",
        "bond_length": 0.74  # Equilibrium bond length in Angstroms
    }, "H2 Molecule - 65536 Qubits, Full Precision VQE")
    
    # Lithium Hydride (LiH) - quantum chemistry benchmark
    execute_quantum({
        "domain": "chemistry",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "molecule": "LiH",
        "bond_length": 1.6  # Equilibrium bond length
    }, "LiH Molecule - 65536 Qubits, Ground State Energy")
    
    # Water molecule (H2O) - biologically relevant
    execute_quantum({
        "domain": "chemistry",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "molecule": "H2O",
        "bond_length": 0.96  # O-H bond length
    }, "H2O Water Molecule - 65536 Qubits")

# =============================================================================
# DOMAIN 2: Physics - Lattice Models & Condensed Matter
# =============================================================================
def demo_physics():
    """
    Physics domain: Simulates quantum lattice models.
    Applications: Superconductivity, magnetism, phase transitions.
    """
    print("\n" + "="*70)
    print("  DOMAIN: PHYSICS - Quantum Lattice Models")
    print("  Simulates Heisenberg, Ising, and Hubbard models")
    print("="*70)
    
    # Heisenberg spin chain - antiferromagnetic
    execute_quantum({
        "domain": "physics",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "model": "heisenberg",
        "lattice_size": 8,
        "coupling_j": 1.0,
        "dimension": 1
    }, "Heisenberg Spin Chain - 65536 Qubits, J=1.0")
    
    # Transverse-field Ising model - quantum phase transition
    execute_quantum({
        "domain": "physics",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "model": "ising",
        "lattice_size": 6,
        "transverse_field": 0.5,
        "coupling_j": 1.0
    }, "Transverse-Field Ising Model - 65536 Qubits, h/J=0.5")
    
    # Hubbard model - strongly correlated electrons
    execute_quantum({
        "domain": "physics",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "model": "hubbard",
        "lattice_size": 4,
        "hopping_t": 1.0,
        "interaction_u": 4.0
    }, "Hubbard Model - 65536 Qubits, U/t=4.0")

# =============================================================================
# DOMAIN 3: Finance - Portfolio & Risk
# =============================================================================
def demo_finance():
    """
    Finance domain: Portfolio optimization and risk analysis.
    Applications: Asset allocation, VaR, credit risk modeling.
    """
    print("\n" + "="*70)
    print("  DOMAIN: FINANCE - Quantum Portfolio Optimization")
    print("  Optimizes asset allocation using quantum annealing principles")
    print("="*70)
    
    # Portfolio optimization - 8 assets
    execute_quantum({
        "domain": "finance",
        "num_qubits": 65536,
        "algorithm": "qaoa",
        "problem_type": "portfolio_optimization",
        "num_assets": 8,
        "risk_tolerance": 0.3,
        "expected_returns": [0.05, 0.08, 0.12, 0.03, 0.15, 0.07, 0.09, 0.11],
        "budget": 1.0
    }, "Portfolio Optimization - 65536 Qubits, 8 Assets, QAOA")
    
    # Risk analysis - Value at Risk
    execute_quantum({
        "domain": "finance",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "risk_analysis",
        "confidence_level": 0.95,
        "time_horizon_days": 10,
        "portfolio_value": 1000000.0
    }, "Value at Risk - 65536 Qubits, 95% confidence")

# =============================================================================
# DOMAIN 4: Materials Science - Crystal & Band Structure
# =============================================================================
def demo_materials_science():
    """
    Materials science domain: Crystal structure and electronic band gaps.
    Applications: Solar cells, batteries, semiconductors.
    """
    print("\n" + "="*70)
    print("  DOMAIN: MATERIALS SCIENCE - Crystal Structure Simulation")
    print("  Predicts electronic band gaps and crystal properties")
    print("="*70)
    
    # Silicon band gap calculation
    execute_quantum({
        "domain": "materials_science",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "material": "silicon",
        "crystal_structure": "diamond_cubic",
        "lattice_constant": 5.43,  # Angstroms
        "property": "band_gap"
    }, "Silicon Band Gap - 65536 Qubits, Diamond Cubic")
    
    # Graphene electronic structure
    execute_quantum({
        "domain": "materials_science",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "material": "graphene",
        "crystal_structure": "hexagonal",
        "lattice_constant": 2.46,
        "property": "electronic_structure"
    }, "Graphene Electronic Structure - 65536 Qubits")

# =============================================================================
# DOMAIN 5: Biomolecules - Protein & Drug Discovery
# =============================================================================
def demo_biomolecules():
    """
    Biomolecules domain: Protein folding and drug-target interactions.
    Applications: Drug design, enzyme catalysis, molecular docking.
    """
    print("\n" + "="*70)
    print("  DOMAIN: BIOMOLECULES - Protein Folding & Drug Discovery")
    print("  Simulates biomolecular interactions at quantum level")
    print("="*70)
    
    # Protein folding energy - small peptide
    execute_quantum({
        "domain": "biomolecules",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "protein_folding",
        "sequence": "ALANINE-GLYCINE-VALINE",
        "num_residues": 3,
        "force_field": "amber"
    }, "Protein Folding - 65536 Qubits, Ala-Gly-Val")
    
    # Drug-target binding affinity
    execute_quantum({
        "domain": "biomolecules",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "drug_discovery",
        "ligand": "aspirin",
        "target": "COX-2",
        "interaction": "binding_affinity"
    }, "Drug Discovery - 65536 Qubits, Aspirin/COX-2")

# =============================================================================
# DOMAIN 6: Machine Learning - Quantum Neural Networks
# =============================================================================
def demo_machine_learning():
    """
    Machine learning domain: Quantum neural networks and kernel methods.
    Applications: Classification, generative models, feature maps.
    """
    print("\n" + "="*70)
    print("  DOMAIN: MACHINE LEARNING - Quantum Neural Networks")
    print("  Quantum-enhanced ML with variational circuits")
    print("="*70)
    
    # Quantum Neural Network - classification
    execute_quantum({
        "domain": "machine_learning",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "qnn_classification",
        "num_layers": 4,
        "num_features": 4,
        "data": [0.1, 0.5, 0.3, 0.8, 0.2, 0.9, 0.4, 0.7]
    }, "Quantum Neural Network - 65536 Qubits, Classification")
    
    # Quantum Kernel estimation
    execute_quantum({
        "domain": "machine_learning",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "quantum_kernel",
        "kernel_type": "fidelity",
        "data": [0.3, 0.7, 0.1, 0.9, 0.5, 0.6]
    }, "Quantum Kernel - 65536 Qubits, Fidelity Kernel")

# =============================================================================
# DOMAIN 7: Logistics - Routing & Supply Chain
# =============================================================================
def demo_logistics():
    """
    Logistics domain: Vehicle routing and supply chain optimization.
    Applications: TSP, delivery routing, warehouse placement.
    """
    print("\n" + "="*70)
    print("  DOMAIN: LOGISTICS - Quantum Routing Optimization")
    print("  Solves combinatorial optimization problems")
    print("="*70)
    
    # Vehicle routing problem - 5 cities
    execute_quantum({
        "domain": "logistics",
        "num_qubits": 65536,
        "algorithm": "qaoa",
        "problem_type": "routing",
        "num_cities": 5,
        "distances": [
            [0, 10, 15, 20, 25],
            [10, 0, 35, 25, 30],
            [15, 35, 0, 30, 20],
            [20, 25, 30, 0, 15],
            [25, 30, 20, 15, 0]
        ]
    }, "Vehicle Routing - 65536 Qubits, 5 Cities TSP")
    
    # Supply chain optimization
    execute_quantum({
        "domain": "logistics",
        "num_qubits": 65536,
        "algorithm": "qaoa",
        "problem_type": "supply_chain",
        "num_warehouses": 3,
        "num_customers": 5,
        "capacity": [100, 150, 200]
    }, "Supply Chain - 65536 Qubits, 3 Warehouses")

# =============================================================================
# DOMAIN 8: Nuclear - Nuclear Structure & Reactions
# =============================================================================
def demo_nuclear():
    """
    Nuclear domain: Nuclear shell model and reaction simulations.
    Applications: Nuclear energy, isotope production, fusion research.
    """
    print("\n" + "="*70)
    print("  DOMAIN: NUCLEAR - Nuclear Structure Simulation")
    print("  Quantum simulation of nuclear shell models")
    print("="*70)
    
    # Deuterium nucleus - simplest nuclear system
    execute_quantum({
        "domain": "nuclear",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "nucleus": "deuterium",
        "protons": 1,
        "neutrons": 1,
        "interaction": "nuclear_force"
    }, "Deuterium Nucleus - 65536 Qubits, Nuclear Force")
    
    # Helium-4 - alpha particle
    execute_quantum({
        "domain": "nuclear",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "nucleus": "helium-4",
        "protons": 2,
        "neutrons": 2,
        "interaction": "shell_model"
    }, "Helium-4 Alpha Particle - 65536 Qubits")

# =============================================================================
# DOMAIN 9: Mathematics - Linear Algebra & Optimization
# =============================================================================
def demo_mathematics():
    """
    Mathematics domain: Quantum linear algebra and optimization.
    Applications: Linear systems, eigenvalue problems, combinatorial opt.
    """
    print("\n" + "="*70)
    print("  DOMAIN: MATHEMATICS - Quantum Linear Algebra")
    print("  Solves linear systems and eigenvalue problems")
    print("="*70)
    
    # Linear system via HHL algorithm
    execute_quantum({
        "domain": "mathematics",
        "num_qubits": 65536,
        "algorithm": "hhl",
        "problem_type": "linear_system",
        "matrix": [[2, -1], [-1, 2]],
        "vector": [1, 0]
    }, "Linear System Ax=b - 65536 Qubits, HHL Algorithm")
    
    # Eigenvalue problem
    execute_quantum({
        "domain": "mathematics",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "eigenvalue",
        "matrix": [[4, 1], [1, 3]]
    }, "Eigenvalue Problem - 65536 Qubits, Hermitian Matrix")

# =============================================================================
# DOMAIN 10: Error Mitigation - Noise Reduction
# =============================================================================
def demo_error_mitigation():
    """
    Error mitigation domain: Quantum error correction and noise suppression.
    Applications: Improving fidelity of noisy quantum computations.
    """
    print("\n" + "="*70)
    print("  DOMAIN: ERROR MITIGATION - Quantum Noise Reduction")
    print("  Zero-noise extrapolation and error-aware computation")
    print("="*70)
    
    # Zero-noise extrapolation
    execute_quantum({
        "domain": "error_mitigation",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "mitigation_method": "zero_noise_extrapolation",
        "noise_factors": [1.0, 1.5, 2.0, 2.5],
        "target_observable": "energy"
    }, "Zero-Noise Extrapolation - 65536 Qubits")
    
    # Measurement error mitigation
    execute_quantum({
        "domain": "error_mitigation",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "mitigation_method": "measurement_error",
        "num_calibration_circuits": 16
    }, "Measurement Error Mitigation - 65536 Qubits")

# =============================================================================
# DOMAIN 11: Graphics - Quantum Rendering
# =============================================================================
def demo_graphics():
    """
    Graphics domain: Quantum-accelerated rendering and ray tracing.
    Applications: Path tracing, global illumination, scene optimization.
    """
    print("\n" + "="*70)
    print("  DOMAIN: GRAPHICS - Quantum Rendering")
    print("  Quantum-accelerated ray tracing and scene optimization")
    print("="*70)
    
    # Quantum ray tracing
    execute_quantum({
        "domain": "graphics",
        "num_qubits": 65536,
        "algorithm": "grover",
        "problem_type": "ray_tracing",
        "scene_objects": 64,
        "resolution": [128, 128],
        "max_bounces": 4
    }, "Quantum Ray Tracing - 65536 Qubits, 64 objects")
    
    # Scene optimization
    execute_quantum({
        "domain": "graphics",
        "num_qubits": 65536,
        "algorithm": "qaoa",
        "problem_type": "scene_optimization",
        "num_lights": 8,
        "render_quality": "high"
    }, "Scene Optimization - 65536 Qubits, 8 Lights")

# =============================================================================
# DOMAIN 12: Real-Time - Streaming Quantum State
# =============================================================================
def demo_real_time():
    """
    Real-time domain: Streaming quantum state evolution.
    Applications: Live monitoring, adaptive control, sensor fusion.
    """
    print("\n" + "="*70)
    print("  DOMAIN: REAL-TIME - Streaming Quantum State")
    print("  Real-time quantum state monitoring and evolution")
    print("="*70)
    
    # Streaming quantum state
    execute_quantum({
        "domain": "real_time",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "state_monitoring",
        "update_interval_ms": 100,
        "num_snapshots": 10,
        "observable": "magnetization"
    }, "Real-Time State Monitoring - 65536 Qubits")
    
    # Adaptive quantum control
    execute_quantum({
        "domain": "real_time",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "adaptive_control",
        "target_state": [0.707, 0, 0, 0.707],
        "feedback_gain": 0.1
    }, "Adaptive Quantum Control - 65536 Qubits")

# =============================================================================
# DOMAIN 13: Fluid Mechanics - Navier-Stokes & CFD
# =============================================================================
def demo_fluid_mechanics():
    """
    Fluid mechanics domain: Quantum CFD via lattice Boltzmann methods.
    Applications: Aerodynamics, pipe flow, ocean currents.
    """
    print("\n" + "="*70)
    print("  DOMAIN: FLUID MECHANICS - Quantum CFD")
    print("  Navier-Stokes simulation via quantum lattice methods")
    print("="*70)
    
    # Pipe flow simulation
    execute_quantum({
        "domain": "fluid_mechanics",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "navier_stokes",
        "reynolds_number": 100,
        "geometry": "pipe",
        "grid_size": [32, 32],
        "viscosity": 0.01
    }, "Pipe Flow - 65536 Qubits, Re=100 Laminar")
    
    # Airfoil simulation
    execute_quantum({
        "domain": "fluid_mechanics",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "external_flow",
        "geometry": "naca0012",
        "mach_number": 0.3,
        "angle_of_attack": 5.0
    }, "NACA 0012 Airfoil - 65536 Qubits, Mach 0.3")

# =============================================================================
# DOMAIN 14: Turbulence CFD - Turbulent Flow Simulation
# =============================================================================
def demo_turbulence_cfd():
    """
    Turbulence CFD domain: Large eddy and direct numerical simulation.
    Applications: Jet engines, wind turbines, combustion.
    """
    print("\n" + "="*70)
    print("  DOMAIN: TURBULENCE CFD - Turbulent Flow Simulation")
    print("  Quantum-enhanced turbulence modeling")
    print("="*70)
    
    # Turbulent channel flow
    execute_quantum({
        "domain": "turbulence_cfd",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "channel_flow",
        "reynolds_number": 5000,
        "turbulence_model": "les",
        "grid_size": [64, 32, 32]
    }, "Turbulent Channel Flow - 65536 Qubits, Re=5000")
    
    # Jet mixing simulation
    execute_quantum({
        "domain": "turbulence_cfd",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "jet_mixing",
        "jet_velocity": 100.0,
        "ambient_velocity": 10.0,
        "temperature_ratio": 1.5
    }, "Jet Mixing - 65536 Qubits, Velocity Ratio 10:1")

# =============================================================================
# DOMAIN 15: Heat Transfer - Thermal Transport
# =============================================================================
def demo_heat_transfer():
    """
    Heat transfer domain: Conduction, convection, and radiation.
    Applications: Electronics cooling, building thermal design, engines.
    """
    print("\n" + "="*70)
    print("  DOMAIN: HEAT TRANSFER - Thermal Transport Simulation")
    print("  Quantum simulation of heat conduction and convection")
    print("="*70)
    
    # Heat conduction in a plate
    execute_quantum({
        "domain": "heat_transfer",
        "num_qubits": 65536,
        "algorithm": "hhl",
        "problem_type": "conduction",
        "geometry": "plate",
        "dimensions": [0.1, 0.1],  # meters
        "thermal_conductivity": 237.0,  # Aluminum W/(m·K)
        "boundary_temperatures": [100, 25, 25, 25]  # Celsius: top, right, bottom, left
    }, "Heat Conduction - 65536 Qubits, Aluminum Plate")
    
    # Natural convection
    execute_quantum({
        "domain": "heat_transfer",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "problem_type": "convection",
        "rayleigh_number": 1e6,
        "prandtl_number": 0.71,  # Air
        "geometry": "cavity",
        "hot_wall_temp": 350.0,
        "cold_wall_temp": 300.0
    }, "Natural Convection - 65536 Qubits, Ra=1e6")

# =============================================================================
# DOMAIN 16: Core Gates - Fundamental Quantum Operations
# =============================================================================
def demo_core_gates():
    """
    Core gates domain: Low-level quantum gate operations.
    Applications: Custom circuits, algorithm development, benchmarking.
    """
    print("\n" + "="*70)
    print("  DOMAIN: CORE GATES - Fundamental Quantum Operations")
    print("  Direct quantum gate manipulation and circuit execution")
    print("="*70)
    
    # Grover's search
    execute_quantum({
        "domain": "core_gates",
        "num_qubits": 65536,
        "algorithm": "grover",
        "search_space_size": 64,
        "target_states": [42]
    }, "Grover's Search - 65536 Qubits, Find |42⟩")
    
    # Bell state preparation
    execute_quantum({
        "domain": "core_gates",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "circuit_type": "bell_state",
        "measurement_basis": "computational"
    }, "Bell State Preparation - 65536 Qubits")

# =============================================================================
# ALGORITHM DEMONSTRATIONS (via Algorithm Bridge)
# =============================================================================
def demo_algorithms():
    """
    Demonstrates all 4 algorithms available through the Algorithm Bridge:
    1. VQE  - Variational Quantum Eigensolver (default, optimization)
    2. QAOA - Quantum Approximate Optimization (combinatorial)
    3. HHL  - Harrow-Hassidim-Lloyd (linear systems)
    4. Grover - Quantum search (unstructured search)
    """
    print("\n" + "="*70)
    print("  ALGORITHM BRIDGE - All 4 Quantum Algorithms")
    print("  The bridge routes to the optimal algorithm automatically")
    print("="*70)
    
    # VQE - default algorithm for energy minimization
    execute_quantum({
        "domain": "chemistry",
        "num_qubits": 65536,
        "algorithm": "vqe",
        "molecule": "H2",
        "bond_length": 0.74
    }, "Algorithm: VQE - 65536 Qubits, Variational Eigensolver")
    
    # QAOA - combinatorial optimization
    execute_quantum({
        "domain": "finance",
        "num_qubits": 65536,
        "algorithm": "qaoa",
        "problem_type": "portfolio_optimization",
        "num_assets": 8,
        "risk_tolerance": 0.3
    }, "Algorithm: QAOA - 65536 Qubits, Optimization")
    
    # HHL - solving linear systems
    execute_quantum({
        "domain": "mathematics",
        "num_qubits": 65536,
        "algorithm": "hhl",
        "problem_type": "linear_system",
        "matrix": [[2, -1], [-1, 2]],
        "vector": [1, 0]
    }, "Algorithm: HHL - 65536 Qubits, Linear System")
    
    # Grover - quantum search
    execute_quantum({
        "domain": "core_gates",
        "num_qubits": 65536,
        "algorithm": "grover",
        "search_space_size": 256,
        "target_states": [137]
    }, "Algorithm: Grover - 65536 Qubits, Quantum Search")

# =============================================================================
# VQS TIME EVOLUTION
# =============================================================================
def demo_vqs_evolution():
    """
    Variational Quantum Simulation - time evolution of quantum systems.
    Simulates Hamiltonian dynamics over discrete time steps.
    """
    print("\n" + "="*70)
    print("  VQS TIME EVOLUTION - Quantum Dynamics")
    print("  Simulates time-dependent quantum systems")
    print("="*70)
    
    url = f"{BASE_URL}/quantum/vqs/evolve"
    payload = {
        "num_qubits": 65536,
        "time_steps": 20,
        "dt_seconds": 0.05,
        "hamiltonian": "heisenberg",
        "initial_state": "neel"
    }
    
    print(f"\n  Endpoint: POST {url}")
    print(f"  Payload:  {json.dumps(payload, indent=2)}")
    
    try:
        start = time.time()
        resp = requests.post(url, json=payload, headers=get_headers(), timeout=120)
        elapsed = (time.time() - start) * 1000
        print(f"  Status:   {resp.status_code}")
        print(f"  Time:     {elapsed:.1f} ms")
        if resp.status_code == 200:
            result = resp.json()
            print(f"  Response: {json.dumps(result, indent=2)[:500]}")
    except Exception as e:
        print(f"  ERROR: {e}")

# =============================================================================
# PIPELINE EXECUTION
# =============================================================================
def demo_pipeline():
    """
    Pipeline execution: L1 → L2 → L3 multidimensional quantum processing.
    Processes data through the full encoding → tensor → VQE pipeline.
    """
    print("\n" + "="*70)
    print("  PIPELINE EXECUTION - L1→L2→L3 Quantum Processing")
    print("  Full pipeline: encoding → tensor geometry → VQE execution")
    print("="*70)
    
    url = f"{BASE_URL}/quantum/pipeline/execute"
    payload = {
        "domain": "chemistry",
        "num_qubits": 65536,
        "molecule": "H2",
        "bond_length": 0.74
    }
    
    print(f"\n  Endpoint: POST {url}")
    print(f"  Payload:  {json.dumps(payload, indent=2)}")
    
    try:
        start = time.time()
        resp = requests.post(url, json=payload, headers=get_headers(), timeout=120)
        elapsed = (time.time() - start) * 1000
        print(f"  Status:   {resp.status_code}")
        print(f"  Time:     {elapsed:.1f} ms")
        if resp.status_code == 200:
            result = resp.json()
            print(f"  Response: {json.dumps(result, indent=2)[:500]}")
    except Exception as e:
        print(f"  ERROR: {e}")

# =============================================================================
# MULTIDIMENSIONAL QUERY
# =============================================================================
def demo_multidimensional():
    """
    Multidimensional query: spatial/temporal range queries on quantum data.
    Uses the engine's built-in multidimensional indexing.
    """
    print("\n" + "="*70)
    print("  MULTIDIMENSIONAL QUERY - Spatial/Temporal Indexing")
    print("  Range queries on quantum-indexed multidimensional data")
    print("="*70)
    
    url = f"{BASE_URL}/multidimensional/query"
    payload = {
        "type": "range",
        "dimensions": 3,
        "data_points": 64,
        "bounds": {
            "min": [0.0, 0.0, 0.0],
            "max": [1.0, 1.0, 1.0]
        }
    }
    
    print(f"\n  Endpoint: POST {url}")
    print(f"  Payload:  {json.dumps(payload, indent=2)}")
    
    try:
        start = time.time()
        resp = requests.post(url, json=payload, headers=get_headers(), timeout=120)
        elapsed = (time.time() - start) * 1000
        print(f"  Status:   {resp.status_code}")
        print(f"  Time:     {elapsed:.1f} ms")
        if resp.status_code == 200:
            result = resp.json()
            print(f"  Response: {json.dumps(result, indent=2)[:500]}")
    except Exception as e:
        print(f"  ERROR: {e}")

# =============================================================================
# UTILITY: Health & Status
# =============================================================================
def check_server():
    """Check if the server is running and display status."""
    print("="*70)
    print("  NAWAZ1 QUANTUM VQE ENGINE - Server Check")
    print("="*70)
    
    # Health check
    try:
        resp = requests.get(f"{BASE_URL}/health", headers=get_headers(), timeout=5)
        print(f"  Health:  {resp.status_code} - {resp.text[:100]}")
    except:
        print("  Health:  UNREACHABLE - Server not running!")
        print(f"  Please start: nawaz1-server (listening on {HOST}:{PORT})")
        return False
    
    # Quantum status
    try:
        resp = requests.get(f"{BASE_URL}/quantum/status", headers=get_headers(), timeout=5)
        print(f"  Status:  {resp.text[:200]}")
    except:
        pass
    
    # Available domains
    try:
        resp = requests.get(f"{BASE_URL}/quantum/domains", headers=get_headers(), timeout=5)
        print(f"  Domains: {resp.text[:300]}")
    except:
        pass
    
    print()
    return True

# =============================================================================
# MAIN
# =============================================================================
ALL_DEMOS = {
    "chemistry": demo_chemistry,
    "physics": demo_physics,
    "finance": demo_finance,
    "materials_science": demo_materials_science,
    "biomolecules": demo_biomolecules,
    "machine_learning": demo_machine_learning,
    "logistics": demo_logistics,
    "nuclear": demo_nuclear,
    "mathematics": demo_mathematics,
    "error_mitigation": demo_error_mitigation,
    "graphics": demo_graphics,
    "real_time": demo_real_time,
    "fluid_mechanics": demo_fluid_mechanics,
    "turbulence_cfd": demo_turbulence_cfd,
    "heat_transfer": demo_heat_transfer,
    "core_gates": demo_core_gates,
    "algorithms": demo_algorithms,
    "vqs": demo_vqs_evolution,
    "pipeline": demo_pipeline,
    "multidimensional": demo_multidimensional,
}

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          NAWAZ1 QUANTUM VQE ENGINE - Usage Examples                 ║
║          All 16 Domains + 4 Algorithms + Pipeline                  ║
║          Copyright (c) 2026 Shahnawaz Alam                         ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--list":
            print("Available demos:")
            for name in ALL_DEMOS:
                print(f"  - {name}")
            sys.exit(0)
        elif arg in ALL_DEMOS:
            if check_server():
                ALL_DEMOS[arg]()
        else:
            print(f"Unknown demo: {arg}")
            print(f"Available: {', '.join(ALL_DEMOS.keys())}")
            sys.exit(1)
    else:
        # Run all demos
        if not check_server():
            print("\nServer not available. Examples shown without execution.")
            print("Start server with: nawaz1-server")
            sys.exit(1)
        
        for name, fn in ALL_DEMOS.items():
            try:
                fn()
            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                sys.exit(0)
            except Exception as e:
                print(f"\n[ERROR in {name}]: {e}")
        
        print("\n" + "="*70)
        print("  ALL DEMOS COMPLETE")
        print("="*70)
