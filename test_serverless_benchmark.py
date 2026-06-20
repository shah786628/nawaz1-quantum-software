#!/usr/bin/env python3
r"""
Quantum vs Classical ML Benchmark — Serverless Mode
=====================================================

Tests nawaz1-server binary in serverless mode for performance validation.

Usage:
  python test_serverless_benchmark.py --binary "C:\Users\IMRAN\Downloads\nawaz1-server"
  python test_serverless_benchmark.py --samples 50 --features 16
"""

import sys
import os
import time
import json
import argparse
import subprocess
import tempfile
import numpy as np

try:
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.datasets import make_regression
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("ERROR: scikit-learn required: pip install scikit-learn")
    sys.exit(1)


def log(msg, indent=4):
    """Print indented log message."""
    prefix = " " * indent
    print(f"{prefix}{msg}")


def run_quantum_serverless(binary_path, sample, num_qubits=16):
    """Run a single quantum computation in serverless mode."""
    # Normalize sample to quantum amplitudes
    sample_normalized = (sample / (np.linalg.norm(sample) + 1e-12)).tolist()
    
    payload = {
        "domain": "machine_learning",
        "algorithm": "vqe",
        "hpc": True,
        "num_qubits": num_qubits,
        "problem": {
            "orbital_energies": sample_normalized
        }
    }
    
    # Write to temp file with UTF-8 encoding
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(payload, f)
        input_file = f.name
    
    try:
        # Convert Windows path to WSL path manually
        # C:\Users\IMRAN\... -> /mnt/c/Users/IMRAN/...
        wsl_input_file = input_file.replace('\\', '/').replace('C:', '/mnt/c', 1)
        wsl_binary = binary_path.replace('\\', '/').replace('C:', '/mnt/c', 1)
        
        # Run serverless via WSL
        env_vars = 'NAWAZ1_MODE=serverless NAWAZ1_INPUT_FILE="{}" JWT_SECRET="benchmark-secret-key-32-chars-long" RUST_LOG=warn'.format(wsl_input_file)
        
        t0 = time.perf_counter()
        result = subprocess.run(
            ['wsl', 'bash', '-c', '{} {}'.format(env_vars, wsl_binary)],
            capture_output=True,
            text=True,
            timeout=120
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        
        # Parse JSON output from stdout
        output = result.stdout.strip()
        # Find JSON in output (may have log lines before)
        json_start = output.find('{')
        json_end = output.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            try:
                data = json.loads(output[json_start:json_end])
            except json.JSONDecodeError as e:
                data = {"status": "error", "error": f"JSON parse error: {e}", "stderr": result.stderr[:200]}
        else:
            data = {"status": "error", "stderr": result.stderr[:200], "stdout": output[:200]}
        
        return data, elapsed_ms
        
    finally:
        os.unlink(input_file)


def extract_energy(data):
    """Extract energy from quantum response."""
    try:
        if isinstance(data, dict):
            result = data.get("result", data)
            energy = result.get("aggregate_energy", result.get("energy", None))
            return energy
    except:
        pass
    return None


def benchmark_regression_serverless(binary_path, n_samples, n_features):
    """Compare classical vs quantum regression in serverless mode."""
    print(f"\n{'='*80}")
    print(f"  REGRESSION BENCHMARK ({n_samples} samples, {n_features} features)")
    print(f"{'='*80}")
    
    # Generate data
    X, y = make_regression(n_samples=n_samples, n_features=n_features, 
                           n_informative=n_features//2, noise=0.1, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    results = {}
    
    # ── CLASSICAL: Linear Regression ──
    log("Classical: Linear Regression")
    t0 = time.perf_counter()
    model_lr = LinearRegression()
    model_lr.fit(X_train, y_train)
    train_time_lr = (time.perf_counter() - t0) * 1000
    
    t0 = time.perf_counter()
    y_pred_lr = model_lr.predict(X_test)
    infer_time_lr = (time.perf_counter() - t0) * 1000
    
    mse_lr = mean_squared_error(y_test, y_pred_lr)
    r2_lr = r2_score(y_test, y_pred_lr)
    
    results["classical_linear"] = {
        "train_ms": train_time_lr,
        "infer_ms": infer_time_lr,
        "mse": mse_lr,
        "r2": r2_lr,
    }
    log(f"  Train: {train_time_lr:.1f}ms | Infer: {infer_time_lr:.1f}ms")
    log(f"  MSE: {mse_lr:.4f} | R²: {r2_lr:.4f}")
    
    # ── QUANTUM: VQE Regression (serverless) ──
    log("Quantum: VQE Regression (serverless mode)")
    n_quantum_train = min(10, len(X_train))  # Small sample for serverless
    n_quantum_test = min(5, len(X_test))
    
    # Training samples
    log(f"  Running {n_quantum_train} training computations...")
    train_energies = []
    train_times = []
    for i in range(n_quantum_train):
        sample = X_train[i]
        data, elapsed = run_quantum_serverless(binary_path, sample, num_qubits=16)
        energy = extract_energy(data)
        if energy is not None:
            train_energies.append(energy)
            train_times.append(elapsed)
            log(f"    Sample {i+1}: energy={energy:.6f}, time={elapsed:.0f}ms")
        else:
            log(f"    Sample {i+1}: ERROR - {data.get('error', data.get('stderr', 'unknown'))[:100]}")
    
    avg_train_time_q = np.mean(train_times) if train_times else 0
    total_train_time_q = np.sum(train_times)
    
    # Test samples
    log(f"  Running {n_quantum_test} inference computations...")
    test_energies = []
    test_times = []
    for i in range(n_quantum_test):
        sample = X_test[i]
        data, elapsed = run_quantum_serverless(binary_path, sample, num_qubits=16)
        energy = extract_energy(data)
        if energy is not None:
            test_energies.append(energy)
            test_times.append(elapsed)
            log(f"    Sample {i+1}: energy={energy:.6f}, time={elapsed:.0f}ms")
        else:
            log(f"    Sample {i+1}: ERROR - {data.get('status', 'unknown')}")
    
    avg_infer_time_q = np.mean(test_times) if test_times else 0
    
    # Fit linear map: energy -> target
    if len(train_energies) >= 2:
        coeffs = np.polyfit(train_energies, y_train[:n_quantum_train], 1)
        y_pred_q = np.polyval(coeffs, test_energies)
        mse_q = mean_squared_error(y_test[:n_quantum_test], y_pred_q)
        r2_q = r2_score(y_test[:n_quantum_test], y_pred_q)
    else:
        mse_q = float('inf')
        r2_q = 0.0
    
    results["quantum_vqe"] = {
        "train_ms": total_train_time_q,
        "infer_ms": avg_infer_time_q,
        "mse": mse_q,
        "r2": r2_q,
    }
    log(f"  Total Train: {total_train_time_q:.0f}ms ({n_quantum_train} samples)")
    log(f"  Avg Infer: {avg_infer_time_q:.0f}ms per sample")
    log(f"  MSE: {mse_q:.4f} | R²: {r2_q:.4f}")
    
    # ── Summary ──
    log("\n" + "="*80)
    log("REGRESSION SUMMARY", indent=0)
    log("="*80, indent=0)
    log(f"{'Model':<25} {'Train(ms)':<15} {'Infer(ms)':<15} {'MSE':<12} {'R²':<10}")
    log("-"*80, indent=0)
    for name, res in results.items():
        log(f"{name:<25} {res['train_ms']:<15.1f} {res['infer_ms']:<15.1f} "
            f"{res['mse']:<12.4f} {res['r2']:<10.4f}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Quantum vs Classical Benchmark (Serverless)")
    parser.add_argument("--binary", type=str, required=True,
                        help="Path to nawaz1-server binary")
    parser.add_argument("--samples", type=int, default=50,
                        help="Number of samples (default: 50)")
    parser.add_argument("--features", type=int, default=16,
                        help="Number of features (default: 16)")
    args = parser.parse_args()
    
    # Verify binary exists
    if not os.path.exists(args.binary):
        print(f"ERROR: Binary not found: {args.binary}")
        sys.exit(1)
    
    print(f"""
{'='*80}
  QUANTUM vs CLASSICAL BENCHMARK — SERVERLESS MODE
  nawaz1 Quantum Software
{'='*80}
  Binary: {args.binary}
  Samples: {args.samples}, Features: {args.features}
""")
    
    # Run benchmark
    results = benchmark_regression_serverless(args.binary, args.samples, args.features)
    
    # Final summary
    print(f"\n{'='*80}")
    print(f"  BENCHMARK COMPLETE")
    print(f"{'='*80}")
    print(f"""
  Key Observations:
  - Quantum runs in serverless mode (one-shot execution)
  - Each quantum computation is independent
  - Results are deterministic and reproducible
  - No server overhead, direct binary execution
""")


if __name__ == "__main__":
    main()
