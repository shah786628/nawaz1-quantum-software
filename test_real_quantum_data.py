#!/usr/bin/env python3
"""
Test with PROPER input data to get real quantum computation results
"""
import requests, json, math
import numpy as np

BASE_URL = "http://localhost:8080"

def test_with_real_quantum_data():
    """Test with chemistry Hamiltonian data that produces REAL energies"""
    
    print("="*70)
    print("TESTING WITH REAL QUANTUM DATA")
    print("="*70)
    
    # Test 1: H2 molecule with proper Hamiltonian
    print("\n1. H₂ Molecule (Real Chemistry)")
    
    # H2 Hamiltonian terms (simplified)
    # Coefficients from quantum chemistry calculation
    h2_coefficients = [
        -1.0523732457727362,  # Identity term
        0.39793742484318045,  # Z0
        -0.39793742484318045, # Z1
        -0.01128010425623538, # Z0*Z1
        0.18093119978423148   # Y0*X1*X0*Y1 (simplified)
    ]
    
    payload = {
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4,
        "input_data": h2_coefficients,
        "molecule": "H2",
        "bond_length": 0.74
    }
    
    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = resp.json()
    
    print(f"  Status: {result.get('status')}")
    print(f"  Full response keys: {list(result.keys())}")
    
    if result.get('status') == 'completed':
        print(f"  Requested qubits: {result.get('num_qubits_requested')}")
        print(f"  Simulated qubits: {result.get('num_qubits_simulated')}")
        print(f"  Fidelity: {result.get('fidelity')}")
        
        inner = result.get('result', {})
        print(f"  Energy: {inner.get('energy')}")
        print(f"  Converged: {inner.get('converged')}")
        print(f"  Iterations: {inner.get('iterations')}")
    else:
        print(f"  Error: {result.get('error')}")
        print(f"  Full response: {json.dumps(result, indent=2)}")
    
    # Test 2: Random normalized amplitudes
    print("\n2. Normalized Quantum State (Random)")
    
    # Generate properly normalized quantum state
    raw_amplitudes = np.random.randn(8)
    normalized = raw_amplitudes / np.linalg.norm(raw_amplitudes)
    
    payload = {
        "domain": "physics",
        "algorithm": "vqe",
        "qubits": 8,
        "input_data": normalized.tolist()
    }
    
    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = resp.json()
    
    print(f"  Status: {result.get('status')}")
    if result.get('status') == 'completed':
        print(f"  Fidelity: {result.get('fidelity')}")
        inner = result.get('result', {})
        print(f"  Energy: {inner.get('energy')}")
        print(f"  Converged: {inner.get('converged')}")
    
    # Test 3: Check actual response structure
    print("\n3. Response Structure Analysis")
    
    payload = {
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4,
        "input_data": [0.5, 0.5, 0.5, 0.5]
    }
    
    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = resp.json()
    
    print(f"  Top-level keys: {sorted(result.keys())}")
    print(f"  Full response:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_with_real_quantum_data()
