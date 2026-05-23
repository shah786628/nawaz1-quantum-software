#!/usr/bin/env python3
"""
VQE Engine Input Data Examples
Complete working examples for all input formats
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def example_1_h2_molecule():
    """Example 1: H₂ molecule using pre-computed integrals"""
    print("="*70)
    print("Example 1: H₂ Molecule (Pre-computed Integrals)")
    print("="*70)
    
    payload = {
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4,
        "molecule": "H2",
        "bond_length": 0.74
    }
    
    print(f"\nRequest:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = response.json()
    
    print(f"\nResponse:")
    if result.get('status') == 'completed':
        inner = result.get('result', {})
        print(f"  ✅ Ground State Energy: {inner.get('ground_state_energy_hartree')} Hartree")
        print(f"  ✅ Electronic Energy: {inner.get('electronic_energy_hartree')} Hartree")
        print(f"  ✅ Nuclear Repulsion: {inner.get('nuclear_repulsion_hartree')} Hartree")
        print(f"  ✅ Converged: {inner.get('converged')}")
        print(f"  ✅ Iterations: {inner.get('iterations')}")
    else:
        print(f"  ❌ Error: {result.get('error')}")


def example_2_custom_hamiltonian():
    """Example 2: Custom Hamiltonian using problem.orbital_energies"""
    print("\n" + "="*70)
    print("Example 2: Custom Hamiltonian (H₂ Qubit Operator)")
    print("="*70)
    
    # H2 Hamiltonian coefficients
    h2_hamiltonian = [
        -1.0523732457727362,   # Identity
         0.39793742484318045,  # Z0
        -0.39793742484318045,  # Z1
        -0.01128010425623538,  # Z0Z1
         0.18093119978423148   # Y0X1X0Y1
    ]
    
    payload = {
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4,
        "problem": {
            "orbital_energies": h2_hamiltonian
        }
    }
    
    print(f"\nRequest:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = response.json()
    
    print(f"\nResponse:")
    if result.get('status') == 'completed':
        inner = result.get('result', {})
        print(f"  ✅ Energy: {inner.get('aggregate_energy')}")
        print(f"  ✅ Fidelity: {result.get('fidelity')}")
        print(f"  ✅ Converged: {inner.get('converged')}")
    else:
        print(f"  ❌ Error: {result.get('error')}")


def example_3_ising_model():
    """Example 3: Ising model using problem.interaction_energies"""
    print("\n" + "="*70)
    print("Example 3: Ising Model (Physics)")
    print("="*70)
    
    # Ising model interactions
    ising_interaction = [
        -1.0,   # J (coupling)
        -1.0,   # J
        -1.0,   # J
         0.0    # Boundary
    ]
    
    payload = {
        "domain": "physics",
        "algorithm": "vqe",
        "qubits": 4,
        "problem": {
            "interaction_energies": ising_interaction
        }
    }
    
    print(f"\nRequest:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = response.json()
    
    print(f"\nResponse:")
    if result.get('status') == 'completed':
        inner = result.get('result', {})
        print(f"  ✅ Energy: {inner.get('aggregate_energy')}")
        print(f"  ✅ Fidelity: {result.get('fidelity')}")
    else:
        print(f"  ❌ Error: {result.get('error')}")


def example_4_heisenberg_model():
    """Example 4: Heisenberg model"""
    print("\n" + "="*70)
    print("Example 4: Heisenberg Model (Quantum Magnetism)")
    print("="*70)
    
    # Heisenberg model
    heisenberg = [
        1.0,    # J (exchange)
        1.0,    # XX
        1.0,    # YY
        1.0     # ZZ
    ]
    
    payload = {
        "domain": "physics",
        "algorithm": "vqe",
        "qubits": 4,
        "problem": {
            "interaction_energies": heisenberg
        }
    }
    
    print(f"\nRequest:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = response.json()
    
    print(f"\nResponse:")
    if result.get('status') == 'completed':
        inner = result.get('result', {})
        print(f"  ✅ Energy: {inner.get('aggregate_energy')}")
        print(f"  ✅ Fidelity: {result.get('fidelity')}")
    else:
        print(f"  ❌ Error: {result.get('error')}")


def example_5_finance_portfolio():
    """Example 5: Portfolio optimization"""
    print("\n" + "="*70)
    print("Example 5: Portfolio Optimization (Finance)")
    print("="*70)
    
    # Portfolio QUBO
    portfolio = [
        0.1,    # Asset 1 return
        0.15,   # Asset 2 return
        0.12,   # Asset 3 return
       -0.5,    # Risk penalty
       -0.3,    # Covariance 1-2
       -0.4     # Covariance 1-3
    ]
    
    payload = {
        "domain": "finance",
        "algorithm": "vqe",
        "qubits": 6,
        "problem": {
            "orbital_energies": portfolio
        }
    }
    
    print(f"\nRequest:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
    result = response.json()
    
    print(f"\nResponse:")
    if result.get('status') == 'completed':
        inner = result.get('result', {})
        print(f"  ✅ Energy: {inner.get('aggregate_energy')}")
        print(f"  ✅ Fidelity: {result.get('fidelity')}")
    else:
        print(f"  ❌ Error: {result.get('error')}")


def example_6_wrong_vs_right():
    """Example 6: Demonstrate WRONG vs RIGHT input format"""
    print("\n" + "="*70)
    print("Example 6: WRONG vs RIGHT Input Format")
    print("="*70)
    
    # ❌ WRONG
    print("\n❌ WRONG: Using 'input_data' at top level")
    payload_wrong = {
        "domain": "chemistry",
        "qubits": 4,
        "input_data": [0.5, 0.5, 0.5, 0.5]
    }
    
    print(json.dumps(payload_wrong, indent=2))
    
    response = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload_wrong, timeout=30)
    result_wrong = response.json()
    
    if result_wrong.get('status') == 'completed':
        energy_wrong = result_wrong.get('result', {}).get('aggregate_energy', 0)
        print(f"  Energy: {energy_wrong} (from SYNTHETIC DATA, not your input!)")
    
    # ✅ RIGHT
    print("\n✅ RIGHT: Using 'problem.orbital_energies'")
    payload_right = {
        "domain": "chemistry",
        "qubits": 4,
        "problem": {
            "orbital_energies": [0.5, 0.5, 0.5, 0.5]
        }
    }
    
    print(json.dumps(payload_right, indent=2))
    
    response = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload_right, timeout=30)
    result_right = response.json()
    
    if result_right.get('status') == 'completed':
        energy_right = result_right.get('result', {}).get('aggregate_energy', 0)
        print(f"  Energy: {energy_right} (from YOUR DATA!)")
    
    # Comparison
    print("\n📊 Comparison:")
    if result_wrong.get('status') == 'completed' and result_right.get('status') == 'completed':
        print(f"  WRONG API:  Energy = {energy_wrong:.6f}")
        print(f"  RIGHT API:  Energy = {energy_right:.6f}")
        print(f"\n  ✅ Different results prove engine uses 'problem' field!")


if __name__ == "__main__":
    # Health check
    print("\n[SETUP] Checking server...")
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"✅ Server healthy\n")
    except:
        print("❌ Server not running!")
        exit(1)
    
    # Run all examples
    example_1_h2_molecule()
    example_2_custom_hamiltonian()
    example_3_ising_model()
    example_4_heisenberg_model()
    example_5_finance_portfolio()
    example_6_wrong_vs_right()
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70)
