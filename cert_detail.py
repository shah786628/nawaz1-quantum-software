import requests, numpy as np, json
BASE = "http://127.0.0.1:8080/api/v1"
N = 65536
np.random.seed(42)

def make_req(domain, algorithm, data, label):
    payload = {"domain": domain, "algorithm": algorithm, "input_data": data.tolist()}
    resp = requests.post(f"{BASE}/quantum/execute", json=payload, timeout=120)
    r = resp.json()
    print(f"\n{'='*70}")
    print(f"[{domain}/{algorithm}] {label}")
    print(f"HTTP {resp.status_code}")
    print(json.dumps(r, indent=2))
    return r

# Chemistry
chem = np.zeros(N)
for i in range(8738):
    e = -500.0 + i * 550.0/8738
    chem[i] = np.exp(-e**2/1000.0) * np.cos(i*0.1)
chem /= np.linalg.norm(chem)
r1 = make_req("chemistry", "vqe", chem, "Hemoglobin MO")

# Physics
phys = np.zeros(N)
for i in range(65536):
    x, y = i%256, i//256
    phys[i] = (-1)**(x+y) * (1.0+0.1*np.sin(2*np.pi*x/256)*np.cos(2*np.pi*y/256))
phys /= np.linalg.norm(phys)
r2 = make_req("physics", "vqe", phys, "Heisenberg AFM")

# Core gates (GHZ)
ghz = np.zeros(N)
ghz[0] = 1/np.sqrt(2)
ghz[N-1] = 1/np.sqrt(2)
r4 = make_req("core_gates", "grover", ghz, "GHZ state")

# Cross-domain comparison
print("\n" + "="*70)
print("CROSS-DOMAIN ENERGY COMPARISON (Authenticity Check)")
print("="*70)
energies = {}
for label, r in [("chemistry", r1), ("physics", r2), ("core_gates", r4)]:
    e = r.get("result", {}).get("aggregate_energy", "N/A")
    qr = r.get("num_qubits_requested", "?")
    qs = r.get("num_qubits_simulated", "?")
    rt = r.get("routed_via", "?")
    disp = r.get("dispatch", "?")
    rc = r.get("real_computation", "?")
    fid = r.get("result", {}).get("fidelity", "?")
    conv = r.get("result", {}).get("converged", "?")
    trun = r.get("result", {}).get("cumulative_truncation_error", "?")
    lines = r.get("result", {}).get("line_energies", [])
    etime = r.get("result", {}).get("execution_time_us", "?")
    energies[label] = e
    print(f"\n  {label}:")
    print(f"    aggregate_energy    = {e}")
    print(f"    qubits (req/sim)    = {qr}/{qs}")
    print(f"    routed_via          = {rt}")
    print(f"    dispatch            = {disp}")
    print(f"    real_computation    = {rc}")
    print(f"    fidelity            = {fid}")
    print(f"    converged           = {conv}")
    print(f"    truncation_error    = {trun}")
    print(f"    execution_time_us   = {etime}")
    print(f"    parallel_lines      = {len(lines)}")
    print(f"    line_energies[0:3]  = {lines[:3]}")

# Uniqueness check
vals = list(energies.values())
unique = len(set(str(v) for v in vals))
print(f"\n  Unique energy values: {unique}/{len(vals)}")
if unique == len(vals):
    print("  [OK] All domains produce DIFFERENT energies -> real domain-specific computation")
else:
    print("  [WARN] Some domains have identical energies -> suspicious")

# Test input sensitivity: same domain, different data
print("\n" + "="*70)
print("INPUT SENSITIVITY TEST (same domain, different data)")
print("="*70)
chem2 = np.zeros(N)
for i in range(8738):
    e = -500.0 + i * 550.0/8738
    chem2[i] = np.exp(-e**2/500.0) * np.sin(i*0.2)  # Different function
chem2 /= np.linalg.norm(chem2)
r5 = make_req("chemistry", "vqe", chem2, "DIFFERENT chemistry input")
e_orig = r1.get("result",{}).get("aggregate_energy")
e_diff = r5.get("result",{}).get("aggregate_energy")
print(f"\n  Chemistry energy (original input): {e_orig}")
print(f"  Chemistry energy (different input): {e_diff}")
if e_orig != e_diff:
    print("  [OK] Different inputs produce different energies -> genuine computation")
else:
    print("  [FAIL] Same energy for different inputs -> possible fake")
