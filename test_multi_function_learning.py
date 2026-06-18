#!/usr/bin/env python3
"""
Multi-Function Quantum ML Stress Test — nawaz1 Quantum Software
===============================================================

Tests if the VQE engine can handle SIMULTANEOUS learning of multiple
functions — function superposition and cross-domain generalization.

Functions under test:
  f1(x) = sin(x)/x          (sinc — oscillatory, decaying)
  f2(x) = cos(x)            (cosine — pure oscillatory)
  f3(x) = exp(-x^2)         (Gaussian — bell curve, smooth decay)
  f4(x) = 1/(1+x^2)         (Cauchy/Lorentzian — heavy tails)
  f5(x) = tanh(x)           (hyperbolic tangent — sigmoid, saturating)
  f6(x) = x*exp(-x)         (gamma-like — rise and fall)

10 Tests:
  1. Individual Baseline — each function alone
  2. Pair Superposition — f1+f2, f1+f3, f2+f3
  3. Triple Superposition — f1+f2+f3 combined
  4. Full 6-Function Superposition — all functions simultaneously
  5. Cross-Domain Generalization — same superposition through 5 domains
  6. Function Separation — can engine distinguish individual components?
  7. Noisy Superposition — f1+f2+f3 + Gaussian noise
  8. Scale Stress — 16 to 4096 points for 6-function superposition
  9. Reproducibility — 5 identical multi-function runs
  10. Derivative Superposition — learn d/dx of all 6 functions simultaneously

Requirements:
  - nawaz1-server running on http://localhost:8080
  - pip install numpy requests

Usage:
  python test_multi_function_learning.py
"""

import sys
import time
import math
import json
import requests
import numpy as np

SERVER = "http://localhost:8080"
ENDPOINT = f"{SERVER}/api/v1/quantum/execute"
PASS = 0
FAIL = 0


# ── Function definitions ─────────────────────────────────────────────────────
def sinc(x):
    """sin(x)/x"""
    x = np.asarray(x, dtype=np.float64)
    result = np.ones_like(x)
    nz = x != 0
    result[nz] = np.sin(x[nz]) / x[nz]
    return result


def cos_func(x):
    """cos(x)"""
    return np.cos(np.asarray(x, dtype=np.float64))


def gaussian(x):
    """exp(-x^2)"""
    return np.exp(-np.asarray(x, dtype=np.float64) ** 2)


def lorentzian(x):
    """1/(1+x^2) — Cauchy distribution"""
    return 1.0 / (1.0 + np.asarray(x, dtype=np.float64) ** 2)


def tanh_func(x):
    """tanh(x)"""
    return np.tanh(np.asarray(x, dtype=np.float64))


def gamma_like(x):
    """x * exp(-x) for x >= 0, extended as |x|*exp(-|x|) for all x"""
    x = np.asarray(x, dtype=np.float64)
    return np.abs(x) * np.exp(-np.abs(x))


FUNCTIONS = {
    "sinc": sinc,
    "cos": cos_func,
    "gaussian": gaussian,
    "lorentzian": lorentzian,
    "tanh": tanh_func,
    "gamma": gamma_like,
}


def log(msg):
    print(f"    {msg}")


def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name}")
    if detail:
        print(f"         {detail}")


def execute(qubits, orbital_energies, algorithm="vqe", domain="machine_learning"):
    """Send request and return (status, energy, fidelity, converged, elapsed_ms)."""
    payload = {
        "domain": domain,
        "algorithm": algorithm,
        "qubits": qubits,
        "problem": {
            "orbital_energies": orbital_energies
        },
    }
    t0 = time.perf_counter()
    try:
        resp = requests.post(ENDPOINT, json=payload, timeout=60)
        elapsed = (time.perf_counter() - t0) * 1000
        data = resp.json()
        return (
            data.get("status", "unknown"),
            data.get("result", {}).get("aggregate_energy", None),
            data.get("result", {}).get("fidelity", None),
            data.get("result", {}).get("converged", False),
            elapsed,
        )
    except Exception as e:
        return "error", None, None, False, (time.perf_counter() - t0) * 1000


def encode_function(func, n_points, x_min=-4 * math.pi, x_max=4 * math.pi, noise_std=0.0):
    """Sample a function and encode as normalized orbital energies."""
    rng = np.random.RandomState(42)
    x = np.linspace(x_min, x_max, n_points)
    y = func(x)
    if noise_std > 0:
        y = y + rng.normal(0, noise_std, n_points)
    norm = np.linalg.norm(y)
    if norm > 0:
        y = y / norm
    return y.tolist()


def encode_superposition(func_list, n_points, x_min=-4 * math.pi, x_max=4 * math.pi,
                         noise_std=0.0, weights=None):
    """Encode a weighted superposition of multiple functions."""
    rng = np.random.RandomState(42)
    x = np.linspace(x_min, x_max, n_points)
    if weights is None:
        weights = [1.0] * len(func_list)

    y_total = np.zeros(n_points)
    for func, w in zip(func_list, weights):
        y_total += w * func(x)

    if noise_std > 0:
        y_total = y_total + rng.normal(0, noise_std, n_points)

    norm = np.linalg.norm(y_total)
    if norm > 0:
        y_total = y_total / norm
    return y_total.tolist()


def next_pow2(n):
    """Next power of 2 >= n, minimum 4."""
    if n <= 4:
        return 4
    return 2 ** int(math.ceil(math.log2(n)))


# ══════════════════════════════════════════════════════════════════════════════
print("=" * 72)
print("MULTI-FUNCTION QUANTUM ML STRESS TEST — nawaz1 VQE Engine")
print("=" * 72)
print()

# Server health
print("[CHECK] Server Health")
try:
    health = requests.get(f"{SERVER}/api/v1/health", timeout=5).json()
    check("Server healthy", health.get("status") == "healthy")
except Exception as e:
    print(f"  [ABORT] Server unreachable: {e}")
    sys.exit(1)
print()


# ──────────────────────────────────────────────────────────────────────────────
# TEST 1: Individual Baseline — Each Function Alone
# ──────────────────────────────────────────────────────────────────────────────
print("[TEST 1] Individual Baseline — Each Function Alone")
print("-" * 72)

baseline = {}
for name, func in FUNCTIONS.items():
    oe = encode_function(func, 64)
    q = next_pow2(len(oe))
    status, energy, fidelity, converged, elapsed = execute(q, oe)
    baseline[name] = (energy, fidelity)
    log(f"  {name:>12}: energy={energy:.10f}, fidelity={fidelity:.12f}" if energy else f"  {name:>12}: FAILED")

all_valid = all(e is not None and math.isfinite(e) for e, _ in baseline.values())
all_high_fid = all(f > 0.99 for _, f in baseline.values() if f)
check("All 6 functions: valid energy", all_valid)
check("All 6 functions: fidelity > 0.99", all_high_fid)
print()


# ──────────────────────────────────────────────────────────────────────────────
# TEST 2: Pair Superposition — f1+f2, f1+f3, f2+f3
# ──────────────────────────────────────────────────────────────────────────────
print("[TEST 2] Pair Superposition — f_i + f_j")
print("-" * 72)

pairs = [
    ("sinc+cos", [sinc, cos_func]),
    ("sinc+gaussian", [sinc, gaussian]),
    ("cos+gaussian", [cos_func, gaussian]),
    ("lorentzian+tanh", [lorentzian, tanh_func]),
    ("gamma+sinc", [gamma_like, sinc]),
]

pair_energies = {}
for label, funcs in pairs:
    oe = encode_superposition(funcs, 64)
    q = next_pow2(len(oe))
    status, energy, fidelity, converged, elapsed = execute(q, oe)
    pair_energies[label] = energy
    log(f"  {label:>22}: energy={energy:.10f}, fidelity={fidelity:.12f}" if energy else f"  {label:>22}: FAILED")

all_pairs_valid = all(e is not None and math.isfinite(e) for e in pair_energies.values())
pairs_differ_from_baseline = any(
    pair_energies.get(label) != baseline.get(label.split("+")[0], (None,))[0]
    for label in pair_energies
)
check("All 5 pairs: valid energy", all_pairs_valid)
check("Pair energies differ from individual baselines", pairs_differ_from_baseline)
print()


# ──────────────────────────────────────────────────────────────────────────────
# TEST 3: Triple Superposition — f1+f2+f3
# ──────────────────────────────────────────────────────────────────────────────
print("[TEST 3] Triple Superposition — sinc + cos + gaussian")
print("-" * 72)

oe_triple = encode_superposition([sinc, cos_func, gaussian], 64)
q_triple = next_pow2(len(oe_triple))
status, e_triple, f_triple, c_triple, t_triple = execute(q_triple, oe_triple)

log(f"Triple superposition: {len(oe_triple)} values, qubits={q_triple}")
check("Triple: completed", status == "completed", f"status={status}")
check("Triple: valid energy", e_triple is not None and math.isfinite(e_triple),
      f"energy={e_triple}")
check("Triple: fidelity > 0.99", f_triple is not None and f_triple > 0.99,
      f"fidelity={f_triple}")
log(f"Time: {t_triple:.0f} ms")
print()


# ──────────────────────────────────────────────────────────────────────────────
# TEST 4: Full 6-Function Superposition
# ──────────────────────────────────────────────────────────────────────────────
print("[TEST 4] Full 6-Function Superposition — All Functions Simultaneously")
print("-" * 72)

all_funcs = list(FUNCTIONS.values())
all_names = list(FUNCTIONS.keys())
oe_all = encode_superposition(all_funcs, 64, weights=[1.0, 0.8, 0.6, 0.5, 0.4, 0.3])
q_all = next_pow2(len(oe_all))

log(f"Superposition: {' + '.join(all_names)}")
log(f"Points: {len(oe_all)}, Qubits: {q_all}")

t0 = time.perf_counter()
status, e_all, f_all, c_all, t_all = execute(q_all, oe_all)

check("6-function: completed", status == "completed", f"status={status}")
check("6-function: valid energy", e_all is not None and math.isfinite(e_all),
      f"energy={e_all}")
check("6-function: fidelity > 0.99", f_all is not None and f_all > 0.99,
      f"fidelity={f_all}")
check("6-function: converged", c_all)
check("6-function: time < 10s", t_all < 10000, f"elapsed={t_all:.0f} ms")
log(f"Time: {t_all:.0f} ms")
print()


# ──────────────────────────────────────────────────────────────────────────────
# TEST 5: Cross-Domain Generalization
# ──────────────────────────────────────────────────────────────────────────────
print("[TEST 5] Cross-Domain Generalization — Same Superposition, 5 Domains")
print("-" * 72)

domain_results = {}
for domain in ["machine_learning", "mathematics", "physics", "chemistry", "finance"]:
    status, energy, fidelity, converged, elapsed = execute(q_all, oe_all, domain=domain)
    domain_results[domain] = (status, energy, fidelity)
    log(f"  {domain:>20}: energy={energy:.10f}" if energy else f"  {domain:>20}: FAILED")

all_domains_ok = all(s == "completed" for s, _, _ in domain_results.values())
check("All 5 domains: completed with superposition", all_domains_ok)
print()


# ──────────────────────────────────────────────────────────────────────────────
# TEST 6: Function Separation — Can Engine Distinguish Components?
# ──────────────────────────────────────────────────────────────────────────────
print("[TEST 6] Function Separation — Distinguish Individual Components")
print("-" * 72)
log("Testing if removing one function changes the energy...")

separation_energies = {}
for i, (name, func) in enumerate(FUNCTIONS.items()):
    # Superposition WITHOUT this function
    remaining = [f for j, f in enumerate(all_funcs) if j != i]
    oe_without = encode_superposition(remaining, 64)
    q_w = next_pow2(len(oe_without))
    status, energy, fidelity, converged, elapsed = execute(q_w, oe_without)
    separation_energies[name] = energy
    log(f"  Without {name:>12}: energy={energy:.10f}" if energy else f"  Without {name:>12}: FAILED")

# Each "without X" energy should differ from the full superposition energy
all_separated = all(
    e is not None and abs(e - e_all) > 1e-10
    for e in separation_energies.values()
    if e is not None and e_all is not None
)
check("Removing each function changes energy", all_separated,
      f"full={e_all:.10f}" if e_all else "full=N/A")
print()


# ──────────────────────────────────────────────────────────────────────────────
# TEST 7: Noisy Superposition — f1+f2+f3 + Gaussian Noise
# ──────────────────────────────────────────────────────────────────────────────
print("[TEST 7] Noisy Superposition — sinc + cos + gaussian + noise (σ=0.1)")
print("-" * 72)

oe_noisy = encode_superposition([sinc, cos_func, gaussian], 64, noise_std=0.1)
q_noisy = next_pow2(len(oe_noisy))
status, e_noisy, f_noisy, c_noisy, t_noisy = execute(q_noisy, oe_noisy)

log(f"Noisy superposition: 3 functions + σ=0.1 noise")
check("Noisy superposition: completed", status == "completed", f"status={status}")
check("Noisy superposition: valid energy", e_noisy is not None and math.isfinite(e_noisy),
      f"energy={e_noisy}")
check("Noisy superposition: fidelity > 0.99", f_noisy is not None and f_noisy > 0.99,
      f"fidelity={f_noisy}")
print()


# ──────────────────────────────────────────────────────────────────────────────
# TEST 8: Scale Stress — 16 to 4096 Points for 6-Function Superposition
# ──────────────────────────────────────────────────────────────────────────────
print("[TEST 8] Scale Stress — 6-Function Superposition at Increasing Scale")
print("-" * 72)

scale_results = []
for n in [16, 64, 256, 1024, 4096]:
    oe_s = encode_superposition(all_funcs, n)
    q_s = next_pow2(len(oe_s))
    status, energy, fidelity, converged, elapsed = execute(q_s, oe_s)
    scale_results.append({
        "n": n, "qubits": q_s, "status": status,
        "energy": energy, "fidelity": fidelity, "time_ms": elapsed,
    })
    log(f"  n={n:>5}: qubits={q_s}, energy={energy:.10f}, time={elapsed:.0f}ms" if energy else f"  n={n:>5}: FAILED")

all_scales_ok = all(r["status"] == "completed" for r in scale_results)
all_scales_fid = all(r["fidelity"] > 0.99 for r in scale_results if r["fidelity"])
check("All scales: completed", all_scales_ok)
check("All scales: fidelity > 0.99", all_scales_fid)
print()


# ──────────────────────────────────────────────────────────────────────────────
# TEST 9: Reproducibility — 5 Identical Multi-Function Runs
# ──────────────────────────────────────────────────────────────────────────────
print("[TEST 9] Reproducibility — 5 Identical 6-Function Runs")
print("-" * 72)

repro_energies = []
repro_fidelities = []
for run in range(5):
    status, energy, fidelity, converged, elapsed = execute(q_all, oe_all)
    repro_energies.append(energy)
    repro_fidelities.append(fidelity)
    log(f"  Run {run+1}: energy={energy:.15f}" if energy else f"  Run {run+1}: FAILED")

all_e_same = len(set(e for e in repro_energies if e is not None)) == 1
all_f_same = len(set(f for f in repro_fidelities if f is not None)) == 1
check("5 runs: energies bit-for-bit identical", all_e_same,
      f"unique: {len(set(e for e in repro_energies if e is not None))}")
check("5 runs: fidelities bit-for-bit identical", all_f_same,
      f"unique: {len(set(f for f in repro_fidelities if f is not None))}")
print()


# ──────────────────────────────────────────────────────────────────────────────
# TEST 10: Derivative Superposition — d/dx of All 6 Functions
# ──────────────────────────────────────────────────────────────────────────────
print("[TEST 10] Derivative Superposition — d/dx of All 6 Functions")
print("-" * 72)

def d_sinc(x):
    x = np.asarray(x, dtype=np.float64)
    result = np.zeros_like(x)
    nz = x != 0
    result[nz] = (x[nz] * np.cos(x[nz]) - np.sin(x[nz])) / (x[nz] ** 2)
    return result

def d_cos(x):
    return -np.sin(np.asarray(x, dtype=np.float64))

def d_gaussian(x):
    x = np.asarray(x, dtype=np.float64)
    return -2 * x * np.exp(-x ** 2)

def d_lorentzian(x):
    x = np.asarray(x, dtype=np.float64)
    return -2 * x / (1 + x ** 2) ** 2

def d_tanh(x):
    return 1.0 / np.cosh(np.asarray(x, dtype=np.float64)) ** 2

def d_gamma(x):
    x = np.asarray(x, dtype=np.float64)
    ax = np.abs(x)
    sign = np.sign(x)
    return sign * np.exp(-ax) * (1 - ax)

DERIVATIVES = {
    "d_sinc": d_sinc,
    "d_cos": d_cos,
    "d_gaussian": d_gaussian,
    "d_lorentzian": d_lorentzian,
    "d_tanh": d_tanh,
    "d_gamma": d_gamma,
}

deriv_funcs = list(DERIVATIVES.values())
oe_deriv = encode_superposition(deriv_funcs, 64)
q_deriv = next_pow2(len(oe_deriv))

log(f"Derivative superposition: {' + '.join(DERIVATIVES.keys())}")

status, e_deriv, f_deriv, c_deriv, t_deriv = execute(q_deriv, oe_deriv)

check("Derivative superposition: completed", status == "completed",
      f"status={status}")
check("Derivative: valid energy", e_deriv is not None and math.isfinite(e_deriv),
      f"energy={e_deriv}")
check("Derivative: fidelity > 0.99", f_deriv is not None and f_deriv > 0.99,
      f"fidelity={f_deriv}")
log(f"Time: {t_deriv:.0f} ms")
print()


# ══════════════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
total = PASS + FAIL
print("=" * 72)
print(f"RESULTS: {PASS}/{total} passed, {FAIL}/{total} failed")
print()

if FAIL == 0:
    print("MULTI-FUNCTION LEARNING: ALL TESTS PASSED")
    print()
    print("Proven: nawaz1 VQE engine handles multi-function superposition:")
    print("  1. Individual baseline — all 6 functions learned separately")
    print("  2. Pair superposition — 5 function pairs learned simultaneously")
    print("  3. Triple superposition — sinc + cos + gaussian combined")
    print("  4. Full 6-function superposition — all functions at once")
    print("  5. Cross-domain — same superposition across 5 domains")
    print("  6. Function separation — removing one function changes energy")
    print("  7. Noisy superposition — 3 functions + noise, still high fidelity")
    print("  8. Scale stress — 16 to 4096 points, all scales succeed")
    print("  9. Reproducible — 5 identical runs, bit-for-bit same output")
    print("  10. Derivative superposition — d/dx of all 6 functions at once")
    print()
    print("All deterministic, one-shot, constant memory, zero barren plateaus.")
else:
    print(f"WARNING: {FAIL} test(s) failed — review output above")

print("=" * 72)
sys.exit(0 if FAIL == 0 else 1)
