# Quick Start Guide

Get Nawaz1 Quantum Software running and send your first quantum computation in under 5 minutes. No quantum physics background required.

---

## Prerequisites

- A Linux machine (x86_64 or ARM64) — physical, VM, or WSL2 on Windows
- Python 3.8+ with `requests` and `numpy` installed (`pip install requests numpy`)
- `curl` (pre-installed on most Linux systems)

> **Not on Linux?** Use WSL2 (Windows), or UTM/Lima (macOS) with Ubuntu 24.04.

---

## Before You Start: 4 Rules You MUST Know

> **Read these carefully before sending any API request. Incorrect usage will produce wrong results.**

1. **Correct Hamiltonian** — Your input data must represent a physically valid Hamiltonian (Hermitian, real coefficients). Random or meaningless values will give garbage output. Verify your data before sending.

2. **Correct Algorithm** — Select the algorithm that matches your problem type:
   - Molecular energy → `vqe`
   - Portfolio/combinatorial optimization → `qaoa`
   - Linear systems (Ax=b) → `hhl`
   - Unstructured search → `grover`
   - Derivative pricing → `monte_carlo`
   
   See the [Algorithm Selection Guide](../README.md#supported-algorithms-108) for the full list.

3. **Qubits = Power of 2** — When you set the `qubits` field manually, it **MUST** be a power of 2:
   `4`, `8`, `16`, `32`, `64`, `128`, `256`, `512`, `1024`, `2048`, `4096`, `8192`, `16384`, `32768`, `65536`, etc.
   Non-power-of-2 values will be rejected or produce incorrect results.

4. **Read the Input Data Guide** — Before writing any code, read:
   - [VQE Input Data Guide](../VQE_INPUT_DATA_GUIDE.md) — how to format the `problem` field
   - [All Algorithms Input Methods](../ALL_ALGORITHMS_INPUT_METHODS.md) — input format for all 108 algorithms

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/shah786628/nawaz1-quantum-software.git
cd nawaz1-quantum-software
```

---

## Step 2 — Start the Server

Choose the binary matching your CPU architecture:

### x86_64 (Intel / AMD)

```bash
chmod +x bin/x86_64/nawaz1-server
./bin/x86_64/nawaz1-server
```

### ARM64 (AWS Graviton, Raspberry Pi 4+, Apple Silicon VMs)

```bash
chmod +x bin/arm64/nawaz1-server
./bin/arm64/nawaz1-server
```

**Expected output:**

```
[INFO] Nawaz1 Quantum Engine starting...
[INFO] Listening on 0.0.0.0:8080
[INFO] Health endpoint: http://localhost:8080/api/v1/health
```

Leave the terminal open — the server is now running.

---

## Step 3 — Verify the Server is Healthy

Open a second terminal and run:

```bash
curl http://localhost:8080/api/v1/health
```

**Expected output:**

```json
{"status": "healthy", "version": "1.0.0", "uptime_seconds": 12}
```

If you see `"status": "healthy"`, the engine is ready.

---

## Step 4 — Run Your First Quantum Computation

Let's find the ground-state energy of a hydrogen molecule (H2). This is the "Hello World" of quantum chemistry.

Save the following as `first_quantum.py`:

```python
import requests

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "chemistry",
        "algorithm": "vqe",
        "molecule": "H2",
        "bond_length": 0.74
    }
)

result = response.json()
print(f"Status:       {result['status']}")
print(f"Qubits used:  {result['num_qubits_simulated']}")
print(f"Energy:       {result['result']['aggregate_energy']:.6f} Hartree")
print(f"Fidelity:     {result['result']['fidelity']:.15f}")
print(f"Converged:    {result['result']['converged']}")
```

Run it:

```bash
python first_quantum.py
```

**Expected output:**

```
Status:       completed
Qubits used:  4
Energy:       -1.137270 Hartree
Fidelity:     0.999999999999998
Converged:    True
```

The energy value (around -1.137 Hartree) is the ground-state energy of H2 at its equilibrium bond length — a real physical quantity verified against experimental data.

---

## Step 5 — Try a Custom Hamiltonian

Instead of a named molecule, supply your own quantum system data:

```python
import requests

# Custom 4-orbital Hamiltonian (energies in Hartree)
orbital_energies = [-1.0523732457727362, 0.39793742484318045,
                    -0.39793742484318045, -0.01128010425623538,
                     0.18093119978423148]

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "chemistry",
        "algorithm": "vqe",
        "qubits": 4,
        "problem": {
            "orbital_energies": orbital_energies
        }
    }
)

result = response.json()
print(f"Energy: {result['result']['aggregate_energy']:.6f} Hartree")
```

> **Important:** Use the `problem` field for custom data — not `input_data`. See the [VQE Input Data Guide](../VQE_INPUT_DATA_GUIDE.md) for full details.

---

## Step 6 — Try QAOA Portfolio Optimization

The QAOA algorithm solves combinatorial optimization problems like portfolio selection:

```python
import requests

# 5-asset portfolio: encode return/risk as orbital energies
# Negative = high return, positive = high risk
assets = [-0.12, -0.08, 0.05, -0.15, 0.03]

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "finance",
        "algorithm": "qaoa",
        "qubits": 5,
        "problem": {
            "orbital_energies": assets
        }
    }
)

result = response.json()
print(f"Status:       {result['status']}")
print(f"Algorithm:    {result['algorithm']}")
print(f"Energy:       {result['result']['aggregate_energy']:.6f}")
print(f"Converged:    {result['result']['converged']}")
```

Lower (more negative) energy means a better portfolio allocation.

---

## Using curl Instead of Python

All examples above work with `curl`:

```bash
# Health check
curl http://localhost:8080/api/v1/health

# H2 molecule
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "chemistry",
    "algorithm": "vqe",
    "molecule": "H2",
    "bond_length": 0.74
  }'

# Custom Hamiltonian
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "chemistry",
    "algorithm": "vqe",
    "qubits": 4,
    "problem": {
      "orbital_energies": [-1.052, 0.398, -0.398, -0.011, 0.181]
    }
  }'
```

---

## Using Docker (Alternative)

If you prefer containers, you can skip the binary entirely:

```bash
# Build the image
docker build -t nawaz1-quantum .

# Run the server
docker run -d --name nawaz1 -p 8080:8080 nawaz1-quantum

# Verify
curl http://localhost:8080/api/v1/health
```

Or use Docker Compose:

```bash
docker compose up -d
curl http://localhost:8080/api/v1/health
```

---

## Response Structure

Every API response follows this structure:

```json
{
  "execution_id": "qexec_...",
  "status": "completed",
  "domain": "chemistry",
  "algorithm": "vqe",
  "num_qubits_requested": 4,
  "num_qubits_simulated": 4,
  "real_computation": true,
  "result": {
    "aggregate_energy": -1.13727,
    "fidelity": 0.999999999999998,
    "converged": true,
    "iteration_count": 1
  }
}
```

| Field | Meaning |
|-------|---------|
| `status` | `completed`, `error`, or `timeout` |
| `real_computation` | `true` = real quantum simulation, not synthetic data |
| `aggregate_energy` | The computed energy in Hartree (lower = more stable) |
| `fidelity` | How close the result is to the exact answer (1.0 = perfect) |
| `converged` | Whether the optimizer found a stable solution |

---

## Next Steps

| What You Want | Where to Go |
|--------------|-------------|
| Understand the system architecture | [Architecture Overview](ARCHITECTURE.md) |
| Run a chemistry simulation tutorial | [Chemistry: Ground State of H2O](tutorials/chemistry_h2o.md) |
| Run a finance optimization tutorial | [Finance: Portfolio Optimization](tutorials/finance_qaoa.md) |
| Run a machine learning tutorial | [ML: Quantum Kernel Classification](tutorials/ml_quantum_kernel.md) |
| See all 108 algorithms | [All Algorithms Input Methods](../ALL_ALGORITHMS_INPUT_METHODS.md) |
| Input data format deep dive | [VQE Input Data Guide](../VQE_INPUT_DATA_GUIDE.md) |
| Run the bundled Python examples | `python examples/vqe_input_examples.py` |
| Deploy to production | [Deployment section in README](../README.md#deployment) |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `curl: connection refused` | Server not running — check Step 2 |
| Energy returns `0` | You used `input_data` instead of `problem` — see Step 5 |
| `"error"` status with molecule name | Only `H2` and `LiH` are supported with the `molecule` field; use `problem.orbital_energies` for others |
| Binary won't start on macOS/Windows | Nawaz1 is Linux-only; run inside WSL2 or a Linux VM |
| Permission denied on binary | Run `chmod +x bin/x86_64/nawaz1-server` first |

---

## Support

- **Issues:** [github.com/shah786628/nawaz1-quantum-software/issues](https://github.com/shah786628/nawaz1-quantum-software/issues)
- **Full Documentation:** [docs/INDEX.md](INDEX.md)
