import requests, numpy as np, json
BASE = "http://127.0.0.1:8080/api/v1"
N = 65536

def query(domain, algorithm, data):
    payload = {"domain": domain, "algorithm": algorithm, "input_data": data.tolist()}
    resp = requests.post(f"{BASE}/quantum/execute", json=payload, timeout=120)
    return resp.json()

print("="*70)
print("INPUT SENSITIVITY DEEP TEST")
print("="*70)

# Test 1: Physics with two very different inputs
print("\n--- Physics: Neel order vs random ---")
np.random.seed(42)
phys1 = np.zeros(N)
for i in range(N):
    x, y = i%256, i//256
    phys1[i] = (-1)**(x+y)
phys1 /= np.linalg.norm(phys1)

phys2 = np.random.randn(N)
phys2 /= np.linalg.norm(phys2)

r1 = query("physics", "vqe", phys1)
r2 = query("physics", "vqe", phys2)
e1 = r1["result"]["aggregate_energy"]
e2 = r2["result"]["aggregate_energy"]
le1 = r1["result"]["line_energies"]
le2 = r2["result"]["line_energies"]
print(f"  Physics Neel order energy:  {e1}")
print(f"  Physics random energy:      {e2}")
print(f"  Same? {e1 == e2}")
print(f"  Line energies same? {le1 == le2}")

# Test 2: Same data, different domains
print("\n--- Same data, different domains ---")
data = np.random.randn(N)
data /= np.linalg.norm(data)

for dom in ["chemistry", "physics", "biology", "finance", "mathematics"]:
    alg = "vqe" if dom not in ["mathematics", "finance"] else ("hhl" if dom == "mathematics" else "qaoa")
    r = query(dom, alg, data)
    e = r["result"]["aggregate_energy"]
    qs = r.get("num_qubits_simulated", "?")
    disp = r.get("dispatch", "?")
    print(f"  {dom:20s} ({alg:4s}): energy={e:>20.10f}  qubits_sim={qs}  dispatch={disp}")

# Test 3: Different input sizes via truncation
print("\n--- Different effective input patterns (same domain) ---")
# All zeros except first element vs all zeros except last
d1 = np.zeros(N); d1[0] = 1.0
d2 = np.zeros(N); d2[N-1] = 1.0
d3 = np.zeros(N); d3[N//2] = 1.0
d4 = np.ones(N); d4 /= np.linalg.norm(d4)

for label, d in [("delta at 0", d1), ("delta at end", d2), ("delta at mid", d3), ("uniform", d4)]:
    r = query("physics", "vqe", d)
    e = r["result"]["aggregate_energy"]
    le = r["result"]["line_energies"][:3]
    print(f"  {label:20s}: energy={e:>20.10f}  lines[:3]={le}")

# Test 4: Algorithm variation on same domain
print("\n--- Same domain, different algorithms ---")
data = np.random.randn(N)
data /= np.linalg.norm(data)
for alg in ["vqe", "grover", "qaoa", "hhl"]:
    r = query("physics", alg, data)
    e = r["result"]["aggregate_energy"]
    qs = r.get("num_qubits_simulated", "?")
    print(f"  physics/{alg:6s}: energy={e:>20.10f}  qubits_sim={qs}")

# Test 5: Verify execution_id uniqueness (proves real execution, not cached)
print("\n--- Execution ID uniqueness ---")
ids = []
for i in range(3):
    r = query("physics", "vqe", phys1)
    eid = r.get("execution_id")
    ids.append(eid)
    print(f"  Run {i+1}: execution_id={eid}")
unique_ids = len(set(ids))
print(f"  Unique IDs: {unique_ids}/{len(ids)} -> {'OK unique' if unique_ids == len(ids) else 'DUPLICATES'}")

print("\n" + "="*70)
print("DONE")
