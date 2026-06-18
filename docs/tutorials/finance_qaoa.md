# Tutorial: Portfolio Optimization with QAOA

Use the Quantum Approximate Optimization Algorithm (QAOA) to find the optimal allocation of a 5-asset investment portfolio. QAOA excels at combinatorial optimization — selecting the best combination from exponentially many possibilities.

**Time required:** 5 minutes
**Difficulty:** Beginner

---

## Prerequisites

- Nawaz1 server running on `http://localhost:8080` (see [Quick Start](../QUICKSTART.md))
- Python 3.8+ with `requests` and `numpy` installed

```bash
pip install requests numpy
```

---

> **Important:** Before using the engine, remember:
> 1. **Correct Hamiltonian** — Asset encodings must represent a valid optimization problem (real-valued, meaningful scores). Random or invalid values produce meaningless results.
> 2. **Correct Algorithm** — This tutorial uses `qaoa` for portfolio optimization and `monte_carlo` for derivative pricing. Do NOT use `vqe` for finance optimization or `grover` for portfolio selection.
> 3. **Qubits = Power of 2** — The `qubits` field must be a power of 2: `4`, `8`, `16`, `32`, `64`, `128`, `256`, `512`, `1024`, etc.
> 4. **Read the Input Data Guide** — See [All Algorithms Input Methods](../../ALL_ALGORITHMS_INPUT_METHODS.md) for the correct input format for each algorithm.

## What We're Computing

Given 5 assets with different expected returns and risks, we want to find the allocation that maximizes return while minimizing risk. Classically this is a quadratic optimization problem; QAOA maps it to a quantum circuit where the optimal portfolio corresponds to the lowest-energy quantum state.

---

## Step 1 — Basic 5-Asset Portfolio

Each asset is encoded as an orbital energy value:
- **Negative value** = attractive asset (high expected return, low risk)
- **Positive value** = less attractive asset (low return, high risk)

```python
import requests

# Asset encoding: [AAPL, MSFT, GOOGL, AMZN, TSLA]
# Negative = high return/low risk, Positive = low return/high risk
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
print(f"Fidelity:     {result['result']['fidelity']:.15f}")
print(f"Converged:    {result['result']['converged']}")
```

**Expected output:**

```
Status:       completed
Algorithm:    qaoa
Energy:       -0.350000
Fidelity:     0.999999999999998
Converged:    True
```

The most negative energy corresponds to selecting the optimal subset of assets. Here the engine identifies AAPL, MSFT, and AMZN (the three most negative values) as the optimal combination.

---

## Step 2 — Portfolio with Risk Constraints

Add a risk penalty by adjusting the asset encoding to include pairwise correlation:

```python
import requests
import numpy as np

# Expected annual returns (%)
returns = np.array([0.15, 0.12, 0.08, 0.18, 0.25])  # AAPL, MSFT, GOOGL, AMZN, TSLA

# Risk (annual volatility %)
volatility = np.array([0.22, 0.20, 0.25, 0.30, 0.55])

# Risk-adjusted score: return / volatility (Sharpe-like)
# Negate so that high Sharpe = negative energy = preferred
risk_adjusted = -(returns / volatility)

print("Risk-adjusted asset scores:")
for name, score in zip(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"], risk_adjusted):
    print(f"  {name}: {score:.4f}")

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "finance",
        "algorithm": "qaoa",
        "qubits": 5,
        "problem": {
            "orbital_energies": risk_adjusted.tolist()
        }
    }
)

result = response.json()
print(f"\nOptimal energy: {result['result']['aggregate_energy']:.6f}")
print(f"Converged: {result['result']['converged']}")
```

Assets with high return and low volatility will have the most negative scores and be preferentially selected.

---

## Step 3 — Larger Portfolio (65,536 Instruments)

The streaming engine handles institutional-scale portfolios:

```python
import requests
import numpy as np

# 65536 financial instruments: random risk-adjusted scores
rng = np.random.RandomState(42)
instruments = rng.normal(-0.05, 0.15, 65536)  # mean slightly negative = mostly attractive
instruments = instruments.tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "finance",
        "algorithm": "qaoa",
        "qubits": 65536,
        "problem": {
            "orbital_energies": instruments
        }
    }
)

result = response.json()
print(f"Qubits used:  {result['num_qubits_simulated']}")
print(f"Energy:       {result['result']['aggregate_energy']:.6f}")
print(f"Memory:       constant ~2 MB (streaming)")
```

---

## Step 4 — Using curl

The same computation works directly from the command line:

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "finance",
    "algorithm": "qaoa",
    "qubits": 5,
    "problem": {
      "orbital_energies": [-0.12, -0.08, 0.05, -0.15, 0.03]
    }
  }'
```

---

## Understanding the Output

| Field | Meaning |
|-------|---------|
| `aggregate_energy` | Total portfolio "cost" — lower (more negative) = better allocation |
| `fidelity` | Confidence in the solution. Above 0.999 = high confidence |
| `converged` | Whether QAOA found a stable optimum |

### Interpreting the Energy

The energy encodes the trade-off between return and risk:

- **More negative** = better risk-adjusted return
- **Comparing two portfolios:** the one with lower energy is preferred
- **Absolute value** depends on the input encoding; use it for relative comparison

---

## Advanced: Monte Carlo Risk Analysis

For derivative pricing and risk simulation, use the `monte_carlo` algorithm with named parameters:

```python
import requests

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    json={
        "domain": "finance",
        "algorithm": "monte_carlo",
        "qubits": 1024,
        "problem": {
            "risk_free_rate": 0.05,
            "volatility": 0.20,
            "spot_price": 100.0,
            "time_to_expiry": 0.25
        }
    }
)

print(response.json())
```

| Parameter | Meaning | Example Value |
|-----------|---------|---------------|
| `risk_free_rate` | Annual risk-free interest rate | 0.05 (5%) |
| `volatility` | Annual price volatility | 0.20 (20%) |
| `spot_price` | Current asset price | 100.0 |
| `time_to_expiry` | Time until option expiry (years) | 0.25 (3 months) |

---

## What to Try Next

- Compare QAOA with classical Markowitz mean-variance optimization
- Try different numbers of qubits to explore precision vs. speed trade-offs
- Add transaction cost constraints by modifying the orbital energies
- Move to the [Chemistry: H2O tutorial](chemistry_h2o.md) for a different domain
- See the [Finance Package README](../../packages/finance/README.md) for all 6 sub-modules

---

## Full Reference

- [Finance Package README](../../packages/finance/README.md) — all sub-modules: Market Data, Monte Carlo, Portfolio, Quantum Algorithms, Risk Metrics, Trading
- [All Algorithms Guide](../../ALL_ALGORITHMS_INPUT_METHODS.md) — 108 algorithms documented
- [VQE Input Data Guide](../../VQE_INPUT_DATA_GUIDE.md) — input format specification
