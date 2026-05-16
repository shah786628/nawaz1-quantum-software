# Quantum Finance Package

## Overview

The Finance package provides quantum-accelerated financial computation through the unified L3 VQE circuit at 65536-qubit scale. It handles portfolio optimization across 65536 assets simultaneously, Monte Carlo pricing with quadratic speedup, risk analysis, and market simulation — all executed via the Algorithm Bridge on 7 tensor network experts in unconditional superposition.

## Key Features

- **Portfolio optimization** — optimize across 65536 assets with full covariance structure
- **Option pricing** — quantum Monte Carlo for exotic derivatives with quadratic speedup
- **Risk analysis** — VaR, CVaR, and tail risk at unprecedented granularity
- **Market simulation** — stochastic process modeling in quantum superposition
- **Credit risk** — portfolio credit loss distribution at obligor-level resolution
- **Algorithmic trading** — quantum-enhanced signal detection and strategy optimization
- **Fraud detection** — Grover-accelerated anomaly search in transaction graphs
- **Interest rate modeling** — multi-factor term structure at 65536-point yield curves

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **QAOA** | Combinatorial portfolio selection and rebalancing |
| **Quantum Monte Carlo** | Derivative pricing with quadratic speedup |
| **VQE** | Ground state of financial Hamiltonians (minimum risk) |
| **Grover** | Searching for arbitrage and fraud in exponential spaces |
| **QPE** | Precise risk metric estimation |
| **HHL** | Solving large covariance/correlation matrix systems |

## Scale

- **Qubits:** 65536
- **Maximum assets:** 65536 simultaneous instruments
- **Monte Carlo paths:** Quadratic speedup over 10^9 classical paths
- **Bond dimension:** Adaptive χ = ln(Q) per geometry
- **Tensor experts:** MPS/PEPS/PEPS3D/MERA/TTN/LoopTTN/PepsND in superposition

## Input Data Format

The input data array encodes the financial problem as 65536 floating-point amplitudes representing portfolio weights, asset returns, or market state vectors.

```json
{
  "domain": "finance",
  "algorithm": "qaoa",
  "input_data": [/* 65536 float values: amplitude-encoded financial state */],
  "config": {
    "task": "portfolio_optimization",
    "num_assets": 65536,
    "risk_aversion": 0.5,
    "constraints": {
      "max_position": 0.05,
      "sector_limits": true
    }
  }
}
```

**Input encoding:**
- Amplitudes represent asset return distributions or portfolio state vectors
- Covariance structure encoded in the problem Hamiltonian
- Constraints mapped to penalty terms in the QAOA cost function

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "finance",
    "algorithm": "qaoa",
    "input_data": [0.012, -0.008, 0.015, ... /* 65536 asset return amplitudes */],
    "config": {
      "task": "portfolio_optimization",
      "num_assets": 65536,
      "risk_aversion": 0.7,
      "objective": "minimize_cvar",
      "confidence_level": 0.95,
      "rebalancing_cost": 0.001
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Encode 65536 asset returns as quantum amplitudes
asset_returns = np.random.randn(65536) * 0.02  # Daily returns
amplitudes = (asset_returns / np.linalg.norm(asset_returns)).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "finance",
        "algorithm": "qaoa",
        "input_data": amplitudes,
        "config": {
            "task": "portfolio_optimization",
            "num_assets": 65536,
            "risk_aversion": 0.5,
            "objective": "max_sharpe_ratio"
        }
    }
)
print(response.json())
```

## Example Response

```json
{
  "status": "success",
  "result": {
    "optimal_weights": [0.023, 0.0, 0.015, 0.047, ...],
    "expected_return": 0.0847,
    "portfolio_risk": 0.1234,
    "sharpe_ratio": 2.41,
    "cvar_95": -0.0312,
    "num_active_positions": 847,
    "observables": {
      "diversification_ratio": 1.87,
      "maximum_drawdown": -0.156,
      "turnover": 0.23
    },
    "tensor_expert_used": "TTN",
    "qubit_count": 65536,
    "wall_time_ms": 1567
  }
}
```

## Use Cases

1. **Institutional Portfolio Management** — Optimize sovereign wealth funds across 65536 global instruments
2. **Exotic Derivative Pricing** — Price path-dependent options (Asian, barrier, lookback) with quantum speedup
3. **Systemic Risk Analysis** — Model interconnected failure cascades across the entire financial system
4. **High-Frequency Trading** — Quantum-enhanced signal extraction from noisy market microstructure
5. **Credit Portfolio Optimization** — CDO tranche pricing with full correlation structure
6. **Regulatory Capital** — Compute precise capital requirements under Basel IV at obligor level
7. **Climate Risk Modeling** — Quantum simulation of long-horizon climate scenarios on portfolio valuation
