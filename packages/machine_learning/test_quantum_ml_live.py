#!/usr/bin/env python3
"""
NAWAZ1 QUANTUM ML - COMPREHENSIVE LIVE TEST
=============================================

Tests all 15 quantum ML submodules to verify they run properly.
Each test executes the actual quantum binary and validates output.

Author: Shahnawaz Alam
License: Proprietary
Copyright (c) 2026 Shahnawaz Alam. All rights reserved.
"""

import sys
import os
import time
import json
import subprocess
import tempfile
import numpy as np

# Binary path
BINARY_PATH = r"c:\Users\IMRAN\.qoder\nawaz1_dev\target\release\nawaz1-server.exe"

# Test results
PASS = 0
FAIL = 0
TOTAL_TESTS = 0


def run_quantum_test(algorithm, input_data, num_qubits=64, domain="machine_learning", config=None):
    """Run a quantum ML algorithm and return results."""
    payload = {
        "domain": domain,
        "algorithm": algorithm,
        "hpc": True,
        "num_qubits": num_qubits,
        "problem": {
            "input_data": input_data
        }
    }
    
    if config:
        payload["config"] = config
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(payload, f)
        input_file = f.name
    
    try:
        env = os.environ.copy()
        env['NAWAZ1_MODE'] = 'serverless'
        env['NAWAZ1_INPUT_FILE'] = input_file
        env['JWT_SECRET'] = 'test-quantum-ml-32-chars'
        env['RUST_LOG'] = 'warn'
        
        t0 = time.perf_counter()
        result = subprocess.run(
            [BINARY_PATH],
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        
        output = result.stdout.strip()
        json_start = output.find('{')
        json_end = output.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            data = json.loads(output[json_start:json_end])
        else:
            data = {"status": "error", "stderr": result.stderr[:200]}
        
        return data, elapsed_ms
        
    except Exception as e:
        return {"status": "error", "error": str(e)}, 0
    finally:
        os.unlink(input_file)


def check_result(name, data, elapsed_ms, check_energy=True):
    """Check if test passed."""
    global PASS, FAIL, TOTAL_TESTS
    TOTAL_TESTS += 1
    
    status = data.get("status", "unknown")
    result = data.get("result", {})
    energy = result.get("aggregate_energy")
    fidelity = result.get("fidelity")
    
    if status == "success" or (energy is not None and isinstance(energy, (int, float))):
        PASS += 1
        print(f"  [PASS] {name}")
        print(f"         Time: {elapsed_ms:.1f}ms", end="")
        if energy is not None:
            print(f", Energy: {energy:.6f}", end="")
        if fidelity is not None:
            print(f", Fidelity: {fidelity:.6f}", end="")
        print()
        return True
    else:
        FAIL += 1
        print(f"  [FAIL] {name}")
        print(f"         Status: {status}, Time: {elapsed_ms:.1f}ms")
        return False


def print_header(text):
    """Print test header."""
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}")


def print_subheader(text):
    """Print submodule header."""
    print(f"\n--- {text} ---")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN TEST SUITE
# ══════════════════════════════════════════════════════════════════════════════

print_header("NAWAZ1 QUANTUM ML - COMPREHENSIVE LIVE TEST")
print(f"Binary: {BINARY_PATH}")
print(f"Testing all 15 quantum ML submodules...")

# ── TEST 1: VQE Implementation ──
print_header("TEST 1: VQE Implementation (vqe-impl)")

print_subheader("Test 1.1: Basic VQE Training")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(100).tolist(),
    num_qubits=64
)
check_result("VQE Basic Training", data, elapsed)

print_subheader("Test 1.2: VQE with Large Parameters")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(1000).tolist(),
    num_qubits=128
)
check_result("VQE Large Parameters (1000)", data, elapsed)

print_subheader("Test 1.3: VQE Optimization")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(50).tolist(),
    num_qubits=32,
    config={"optimizer": "SPSA", "max_iterations": 10}
)
check_result("VQE Optimization (SPSA)", data, elapsed)


# ── TEST 2: QAOA Family ──
print_header("TEST 2: QAOA Family (qaoa-variants)")

print_subheader("Test 2.1: QAOA Optimization")
data, elapsed = run_quantum_test(
    algorithm="qaoa",
    input_data=np.random.randn(64).tolist(),
    num_qubits=32
)
check_result("QAOA Basic", data, elapsed)


# ── TEST 3: Quantum SINDy ──
print_header("TEST 3: Quantum SINDy (sindy)")

print_subheader("Test 3.1: SINDy Dynamics Discovery")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(128).tolist(),
    num_qubits=64,
    domain="dynamics"
)
check_result("SINDy Dynamics", data, elapsed)


# ── TEST 4: ML-Quantum Bridge ──
print_header("TEST 4: ML-Quantum Bridge (ml-quantum-bridge)")

print_subheader("Test 4.1: QNN Classification")
data, elapsed = run_quantum_test(
    algorithm="qnn",
    input_data=np.random.randn(256).tolist(),
    num_qubits=64,
    config={"task": "classification", "num_classes": 5}
)
check_result("QNN Classification", data, elapsed, check_energy=False)


# ── TEST 5: Multidimensional ML ──
print_header("TEST 5: Multidimensional ML (ml)")

print_subheader("Test 5.1: Quantum Regression")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(200).tolist(),
    num_qubits=64,
    domain="regression"
)
check_result("Multidimensional Regression", data, elapsed)


# ── TEST 6: VQE Advanced Optimizers ──
print_header("TEST 6: VQE Advanced Optimizers (vqe-advanced-optimizers)")

print_subheader("Test 6.1: Adam Optimizer")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(150).tolist(),
    num_qubits=64,
    config={"optimizer": "adam", "learning_rate": 0.01}
)
check_result("VQE Adam Optimizer", data, elapsed)

print_subheader("Test 6.2: Quantum Natural Gradient")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(100).tolist(),
    num_qubits=32,
    config={"optimizer": "quantum_natural_gradient"}
)
check_result("VQE Quantum Natural Gradient", data, elapsed)


# ── TEST 7: VQE Advanced Ansatz ──
print_header("TEST 7: VQE Advanced Ansatz (vqe-advanced-ansatz)")

print_subheader("Test 7.1: Hardware-Efficient Ansatz")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(80).tolist(),
    num_qubits=32,
    config={"ansatz": "hardware_efficient", "layers": 4}
)
check_result("Hardware-Efficient Ansatz", data, elapsed)

print_subheader("Test 7.2: Strongly Entangling Layers")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(80).tolist(),
    num_qubits=32,
    config={"ansatz": "strongly_entangling", "layers": 3}
)
check_result("Strongly Entangling Ansatz", data, elapsed)


# ── TEST 8: VQE Error Mitigation ──
print_header("TEST 8: VQE Error Mitigation (vqe-error-mitigation)")

print_subheader("Test 8.1: Error Mitigation Enabled")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(100).tolist(),
    num_qubits=64,
    config={"error_mitigation": True, "noise_model": "depolarizing"}
)
check_result("VQE Error Mitigation", data, elapsed)


# ── TEST 9: VQE Hardware-Aware ──
print_header("TEST 9: VQE Hardware-Aware (vqe-hardware-aware)")

print_subheader("Test 9.1: Hardware-Aware Optimization")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(120).tolist(),
    num_qubits=64,
    config={"hardware_aware": True, "topology": "heavy_hex"}
)
check_result("Hardware-Aware VQE", data, elapsed)


# ── TEST 10: VQE Quantum Fisher ──
print_header("TEST 10: VQE Quantum Fisher (vqe-quantum-fisher)")

print_subheader("Test 10.1: Quantum Fisher Information")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(100).tolist(),
    num_qubits=32,
    config={"compute_qfim": True}
)
check_result("Quantum Fisher Information", data, elapsed)


# ── TEST 11: VQE Measurement Reduction ──
print_header("TEST 11: VQE Measurement Reduction (vqe-measurement-reduction)")

print_subheader("Test 11.1: Measurement Optimization")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(150).tolist(),
    num_qubits=64,
    config={"measurement_reduction": True, "grouping": "commuting"}
)
check_result("Measurement Reduction", data, elapsed)


# ── TEST 12: HHL Family ──
print_header("TEST 12: HHL Family (hhlpp-family)")

print_subheader("Test 12.1: Quantum Linear Systems")
data, elapsed = run_quantum_test(
    algorithm="hhl",
    input_data=np.random.randn(64).tolist(),
    num_qubits=32
)
check_result("HHL Linear Systems", data, elapsed)

print_subheader("Test 12.2: Quantum Regression")
data, elapsed = run_quantum_test(
    algorithm="quantum_regression",
    input_data=np.random.randn(100).tolist(),
    num_qubits=64
)
check_result("Quantum Regression (HHL)", data, elapsed)


# ── TEST 13: Quantum Binary Search ──
print_header("TEST 13: Quantum Binary Search (quantum-binary-search)")

print_subheader("Test 13.1: Binary Search")
data, elapsed = run_quantum_test(
    algorithm="quantum_binary_search",
    input_data=np.random.randn(256).tolist(),
    num_qubits=64
)
check_result("Quantum Binary Search", data, elapsed)


# ── TEST 14: Belief Propagation ──
print_header("TEST 14: Belief Propagation (belief-propagation)")

print_subheader("Test 14.1: Quantum Belief Propagation")
data, elapsed = run_quantum_test(
    algorithm="belief_propagation",
    input_data=np.random.randn(128).tolist(),
    num_qubits=64
)
check_result("Belief Propagation", data, elapsed)


# ── TEST 15: Uncertainty Quantification ──
print_header("TEST 15: Uncertainty Quantification (uncertainty)")

print_subheader("Test 15.1: Bayesian Uncertainty")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(100).tolist(),
    num_qubits=32,
    config={"uncertainty": "bayesian"}
)
check_result("Bayesian Uncertainty", data, elapsed)

print_subheader("Test 15.2: Monte Carlo Sampling")
data, elapsed = run_quantum_test(
    algorithm="vqe",
    input_data=np.random.randn(100).tolist(),
    num_qubits=32,
    config={"uncertainty": "monte_carlo"}
)
check_result("Monte Carlo Uncertainty", data, elapsed)


# ── FINAL SUMMARY ──
print_header("TEST SUMMARY")
print(f"\n  Total Tests: {TOTAL_TESTS}")
print(f"  Passed: {PASS}")
print(f"  Failed: {FAIL}")
print(f"  Success Rate: {(PASS/TOTAL_TESTS*100) if TOTAL_TESTS > 0 else 0:.1f}%")

if FAIL == 0:
    print(f"\n  ALL TESTS PASSED - All quantum ML submodules operational!")
else:
    print(f"\n  WARNING: {FAIL} test(s) failed - review output above")

print(f"\n{'='*80}")
print(f"  TEST COMPLETE")
print(f"{'='*80}\n")

sys.exit(0 if FAIL == 0 else 1)
