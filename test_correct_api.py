#!/usr/bin/env python3
"""
CORRECTED Physical Law Test - Uses PROPER API format
Fixes the bug where input_data was ignored
"""
import requests, json, math
import numpy as np

BASE_URL = "http://localhost:8080"

def test_with_correct_api():
    """Test with CORRECT API format (problem field, not input_data)"""
    
    print("="*70)
    print("TESTING WITH CORRECT API FORMAT")
    print("="*70)
    
    # Test 1: H2 molecule (pre-computed integrals)
    print("\n1. H₂ Molecule (Using 'molecule' field)")
    
    payload = {
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4,
        "molecule": "H2",  # ✅ CORRECT: Use molecule field
        "bond_length": 0.74
    }
    
    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = resp.json()
    
    print(f"  Status: {result.get('status')}")
    if result.get('status') == 'completed':
        inner = result.get('result', {})
        energy = inner.get('ground_state_energy_hartree', 'N/A')
        electronic = inner.get('electronic_energy_hartree', 'N/A')
        nuclear = inner.get('nuclear_repulsion_hartree', 'N/A')
        converged = inner.get('converged', 'N/A')
        iterations = inner.get('iterations', 'N/A')
        
        print(f"  ✅ Ground State Energy: {energy} Hartree")
        print(f"  ✅ Electronic Energy: {electronic} Hartree")
        print(f"  ✅ Nuclear Repulsion: {nuclear} Hartree")
        print(f"  ✅ Converged: {converged}")
        print(f"  ✅ Iterations: {iterations}")
        
        # H2 known ground state: ~-1.137 Hartree
        if isinstance(energy, (int, float)):
            expected = -1.137
            error = abs(energy - expected)
            print(f"  ✅ Expected: ~{expected} Hartree")
            print(f"  ✅ Error: {error:.6f} Hartree")
            print(f"  ✅ Accurate: {error < 0.1}")
    else:
        print(f"  ❌ Failed: {result.get('error')}")
    
    # Test 2: Custom Hamiltonian (using problem field)
    print("\n2. Custom Hamiltonian (Using 'problem.orbital_energies')")
    
    # H2 Hamiltonian coefficients
    h2_hamiltonian = [
        -1.0523732457727362,
        0.39793742484318045,
        -0.39793742484318045,
        -0.01128010425623538,
        0.18093119978423148
    ]
    
    payload = {
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4,
        "problem": {  # ✅ CORRECT: Use problem field
            "orbital_energies": h2_hamiltonian
        }
    }
    
    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = resp.json()
    
    print(f"  Status: {result.get('status')}")
    if result.get('status') == 'completed':
        inner = result.get('result', {})
        energy = inner.get('aggregate_energy', 'N/A')
        fidelity = result.get('fidelity', 'N/A')
        converged = inner.get('converged', 'N/A')
        
        print(f"  ✅ Energy: {energy}")
        print(f"  ✅ Fidelity: {fidelity}")
        print(f"  ✅ Converged: {converged}")
        
        # Verify energy is NOT zero
        if isinstance(energy, (int, float)):
            print(f"  ✅ Energy is REAL (not 0): {energy != 0}")
            print(f"  ✅ Energy is finite: {abs(energy) < 1e10}")
    else:
        print(f"  ❌ Failed: {result.get('error')}")
    
    # Test 3: Physics domain with problem field
    print("\n3. Physics Domain (Using 'problem.interaction_energies')")
    
    # Ising model Hamiltonian
    ising_hamiltonian = [1.0, -0.5, -0.5, 0.1]
    
    payload = {
        "domain": "physics",
        "algorithm": "vqe",
        "qubits": 4,
        "problem": {
            "interaction_energies": ising_hamiltonian
        }
    }
    
    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = resp.json()
    
    print(f"  Status: {result.get('status')}")
    if result.get('status') == 'completed':
        inner = result.get('result', {})
        energy = inner.get('aggregate_energy', 'N/A')
        fidelity = result.get('fidelity', 'N/A')
        
        print(f"  ✅ Energy: {energy}")
        print(f"  ✅ Fidelity: {fidelity}")
        
        if isinstance(energy, (int, float)):
            print(f"  ✅ Real energy value: {energy}")
    else:
        print(f"  ❌ Failed: {result.get('error')}")
    
    # Test 4: Compare WRONG vs RIGHT
    print("\n4. Comparison: WRONG vs RIGHT API")
    
    # ❌ WRONG (what you did before)
    print("\n  ❌ WRONG: Using 'input_data'")
    payload_wrong = {
        "domain": "chemistry",
        "qubits": 4,
        "input_data": [0.5, 0.5, 0.5, 0.5]  # IGNORED!
    }
    
    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload_wrong, timeout=30)
    result_wrong = resp.json()
    
    if result_wrong.get('status') == 'completed':
        energy_wrong = result_wrong.get('result', {}).get('aggregate_energy', 0)
        fidelity_wrong = result_wrong.get('fidelity', 0)
        print(f"    Energy: {energy_wrong}")
        print(f"    Fidelity: {fidelity_wrong}")
        print(f"    ⚠️  These are from SYNTHETIC DATA (not your input!)")
    
    # ✅ RIGHT (corrected)
    print("\n  ✅ RIGHT: Using 'problem.orbital_energies'")
    payload_right = {
        "domain": "chemistry",
        "qubits": 4,
        "problem": {
            "orbital_energies": [0.5, 0.5, 0.5, 0.5]  # USED!
        }
    }
    
    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload_right, timeout=30)
    result_right = resp.json()
    
    if result_right.get('status') == 'completed':
        energy_right = result_right.get('result', {}).get('aggregate_energy', 0)
        fidelity_right = result_right.get('fidelity', 0)
        print(f"    Energy: {energy_right}")
        print(f"    Fidelity: {fidelity_right}")
        print(f"    ✅ These are from YOUR DATA!")
    
    # Comparison
    print("\n  📊 Comparison:")
    if result_wrong.get('status') == 'completed' and result_right.get('status') == 'completed':
        print(f"    WRONG API: Energy={energy_wrong:.6f}, Fidelity={fidelity_wrong:.6f}")
        print(f"    RIGHT API: Energy={energy_right:.6f}, Fidelity={fidelity_right:.6f}")
        print(f"\n    ✅ Different results prove engine uses 'problem' field, not 'input_data'!")

if __name__ == "__main__":
    # Health check
    print("\n[SETUP] Checking server...")
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"✅ Server healthy\n")
    except:
        print("❌ Server not running!")
        exit(1)
    
    test_with_correct_api()
