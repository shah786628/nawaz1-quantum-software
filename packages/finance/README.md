# Quantum Finance Package

## Overview

The Finance package provides quantum-accelerated financial computation through the unified VQE engine at 2^53-qubit scale. It encompasses **6 specialized sub-modules** covering market data integration, Monte Carlo simulation, portfolio optimization, quantum financial algorithms, risk analytics, and trading systems.

**API Endpoint:** `POST http://localhost:8080/api/v1/quantum/execute`

**Demo Endpoint:** `POST http://localhost:8080/api/v1/quantum/finance/demo`

---

## The 6 Quantum Finance Sub-Modules

| # | Sub-Module | Key Domain |
|---|-----------|------------|
| 1 | Market Data  | Data Feed Integration |
| 2 | Monte Carlo  | Stochastic Simulation |
| 3 | Portfolio  | Portfolio Optimization |
| 4 | Quantum Algorithms  | Quantum Finance Primitives |
| 5 | Risk Metrics  | Risk Analytics |
| 6 | Trading System  | Trade Execution |

---

## 1. Market Data


Manages market data feed integration supporting multiple providers with configuration, real-time data ingestion, and market point representation for quantum financial computations.

**Key Capabilities:**
- Bloomberg data feed integration and configuration
- Refinitiv (Thomson Reuters) real-time market data
- Yahoo Finance historical and streaming data
- Alpha Vantage API integration for equities, forex, and crypto
- Market data point representation (OHLCV, bid/ask, depth)
- Real-time data ingestion with timestamp normalization
- Multi-provider failover and data reconciliation

**When to Use:** Ingesting real-time or historical market data for quantum portfolio optimization, risk calculations, and trading signal generation.

```json
{
  "domain": "finance",
  "algorithm": "qaoa",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "market_data",
    "task": "data_ingestion",
    "provider": "bloomberg",
    "symbols": ["AAPL", "MSFT", "GOOGL", "AMZN"],
    "data_type": "ohlcv",
    "frequency": "1min"
  }
}
```

---

## 2. Monte Carlo


Implements quantum Monte Carlo with variance reduction techniques and stochastic process models for derivative pricing with quadratic quantum speedup.

**Key Capabilities:**
- Control variates for variance reduction
- Antithetic variables for symmetric payoff functions
- Importance sampling with optimal drift selection
- Stratified sampling for uniform coverage
- Quasi-Monte Carlo (Sobol, Halton sequences)
- Geometric Brownian Motion (GBM) for equity price paths
- Ornstein-Uhlenbeck process for mean-reverting assets
- Heston stochastic volatility model

**When to Use:** Pricing exotic derivatives (Asian, barrier, lookback options), computing CVA/DVA, and simulating complex payoff structures with quantum speedup.

```json
{
  "domain": "finance",
  "algorithm": "monte_carlo",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "monte_carlo",
    "task": "option_pricing",
    "option_type": "asian_call",
    "spot": 100.0,
    "strike": 105.0,
    "volatility": 0.25,
    "risk_free_rate": 0.05,
    "maturity_years": 1.0,
    "variance_reduction": "importance_sampling",
    "stochastic_model": "heston"
  }
}
```

---

## 3. Portfolio


Provides portfolio optimization using multiple methods with constraint management for institutional-scale asset allocation across 2^53 simultaneous instruments.

**Key Capabilities:**
- Markowitz mean-variance optimization (efficient frontier)
- Risk parity (equal risk contribution across assets)
- Minimum variance portfolio construction
- Maximum Sharpe ratio (tangency portfolio)
- Black-Litterman model with investor views integration
- Hierarchical Risk Parity (HRP) via clustering
- Constraint management (sector limits, position bounds, turnover)
- Transaction cost-aware rebalancing

**When to Use:** Institutional asset allocation, multi-asset portfolio construction, risk-budgeting, and rebalancing optimization across large instrument universes.

```json
{
  "domain": "finance",
  "algorithm": "qaoa",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "portfolio",
    "task": "portfolio_optimization",
    "method": "black_litterman",
    "num_assets": 1024,
    "risk_aversion": 0.5,
    "constraints": {
      "max_position": 0.05,
      "sector_limits": true,
      "turnover_limit": 0.25
    }
  }
}
```

---

## 4. Quantum Algorithms


Implements quantum financial algorithms including amplitude estimation, support vector machines, and generative models purpose-built for financial applications.

**Key Capabilities:**
- Quantum Amplitude Estimation (QAE) for risk metric computation
- Quantum Support Vector Machines (QSVM) for classification
- Quantum Generative Models (QGM) for synthetic data generation
- Amplitude encoding of financial distributions
- Quantum speedup for expected value computation
- Feature map construction for financial time series
- Quantum kernel estimation for non-linear classification

**When to Use:** Computing risk metrics with quadratic speedup via QAE, classifying market regimes with QSVM, and generating synthetic market scenarios with QGM.

```json
{
  "domain": "finance",
  "algorithm": "monte_carlo",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "quantum_algorithms",
    "task": "amplitude_estimation",
    "algorithm_type": "qae",
    "target_metric": "expected_shortfall",
    "confidence_level": 0.99,
    "num_evaluation_qubits": 8
  }
}
```

---

## 5. Risk Metrics


Computes comprehensive risk metrics for portfolio evaluation with full quantum acceleration for tail risk estimation.

**Key Capabilities:**
- Value at Risk (VaR) at configurable confidence levels
- Expected Shortfall (CVaR / Conditional VaR)
- Maximum drawdown computation over rolling windows
- Sharpe ratio (risk-adjusted return measurement)
- Sortino ratio (downside deviation-adjusted return)
- Portfolio volatility and correlation analysis
- Tail risk decomposition and stress testing

**When to Use:** Portfolio risk evaluation, regulatory capital computation (Basel IV), stress testing, and risk-adjusted performance attribution.

```json
{
  "domain": "finance",
  "algorithm": "monte_carlo",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "risk_metrics",
    "task": "portfolio_risk",
    "metrics": ["var_95", "cvar_99", "max_drawdown", "sharpe", "sortino"],
    "horizon_days": 10,
    "confidence_level": 0.99
  }
}
```

---

## 6. Trading System


Integrates trading system with comprehensive order types, risk management configuration, and trade execution for quantum-enhanced algorithmic trading.

**Key Capabilities:**
- Order types: market, limit, stop, stop-limit, trailing stop, fill-or-kill (FOK), immediate-or-cancel (IOC)
- Order sides: buy and sell with quantity management
- Risk management configuration (position limits, loss thresholds)
- Trade execution engine with latency optimization
- Order book simulation and market impact modeling
- Slippage estimation and transaction cost analysis
- Portfolio-level risk checks before execution

**When to Use:** Algorithmic trading strategy execution, order management, risk-controlled trade placement, and market microstructure analysis.

```json
{
  "domain": "finance",
  "algorithm": "qaoa",
  "input_data": [0.001, -0.003, 0.002, "...N amplitude values..."],
  "config": {
    "sub_module": "trading_system",
    "task": "execute_order",
    "order_type": "limit",
    "side": "buy",
    "symbol": "AAPL",
    "quantity": 1000,
    "limit_price": 175.50,
    "risk_management": {
      "max_position_pct": 0.05,
      "stop_loss_pct": 0.02
    }
  }
}
```

---

## General Request Format

All sub-modules are accessed through the unified quantum execution endpoint:

```
POST http://localhost:8080/api/v1/quantum/execute
```

**Request body:**

```json
{
  "domain": "finance",
  "algorithm": "qaoa",
  "input_data": [/* N float amplitudes (up to 2^53 supported) */],
  "config": {
    "sub_module": "<feature_name>"
  }
}
```

**Demo endpoint (no input_data required):**

```
POST http://localhost:8080/api/v1/quantum/finance/demo
```

---

## Scale

- **Qubits:** Up to 2^53 (9,007,199,254,740,992)
- **Maximum assets:** 2^53 simultaneous instruments
- **Monte Carlo paths:** Quadratic speedup over 10^9 classical paths

---

## Python Example (Full Workflow)

```python
import requests
import numpy as np

API = "http://localhost:8080/api/v1/quantum/execute"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}

# Generate amplitude-encoded financial state
rng = np.random.RandomState(42)
amplitudes = rng.normal(0, 1, 1024)  # Example uses 1024; engine supports up to 2^53
amplitudes = (amplitudes / np.linalg.norm(amplitudes)).tolist()

# Example: Portfolio optimization
response = requests.post(API, headers=HEADERS, json={
    "domain": "finance",
    "algorithm": "qaoa",
    "input_data": amplitudes,
    "config": {
        "sub_module": "portfolio",
        "task": "portfolio_optimization",
        "method": "max_sharpe",
        "num_assets": 1024
    }
})
print(response.json())

# Example: Monte Carlo option pricing
response = requests.post(API, headers=HEADERS, json={
    "domain": "finance",
    "algorithm": "monte_carlo",
    "input_data": amplitudes,
    "config": {
        "sub_module": "monte_carlo",
        "task": "option_pricing",
        "option_type": "asian_call",
        "stochastic_model": "heston"
    }
})
print(response.json())
```

---

## Use Cases

| Research Area | Relevant Sub-Modules |
|---------------|---------------------|
| **Institutional Portfolio Management** | Portfolio, Risk Metrics, Market Data |
| **Exotic Derivative Pricing** | Monte Carlo, Quantum Algorithms |
| **Systemic Risk Analysis** | Risk Metrics, Portfolio, Quantum Algorithms |
| **High-Frequency Trading** | Trading System, Market Data |
| **Credit Portfolio Optimization** | Portfolio, Risk Metrics, Monte Carlo |
| **Regulatory Capital (Basel IV)** | Risk Metrics, Portfolio |
| **Market Regime Classification** | Quantum Algorithms, Market Data |
| **Algorithmic Trading** | Trading System, Market Data, Risk Metrics |

---

## Input Method

### API Endpoint
```
POST http://localhost:8080/api/v1/quantum/execute
```

### Request Format
```json
{
  "problem": "portfolio_optimization",
  "config": {
    "num_qubits": 1024,
    "optimizer": "SPSA",
    "max_iterations": 100
  },
  "input_data": [0.001, -0.003, 0.002, "...Born-normalized floats..."]
}
```

### Supported Problem Types
- `"portfolio_optimization"` — Multi-asset portfolio construction and rebalancing
- `"derivatives_pricing"` — Exotic option pricing with quantum Monte Carlo
- `"risk_analysis"` — VaR, CVaR, and tail risk computation

### Data Input Options
- **Direct API**: Send JSON payload with amplitudes (Born-normalized floats)
- **File Import**: Upload binary/CSV data files via the import endpoint
- **Streaming**: For large datasets, use chunked streaming mode

---

## Hamiltonian Selection

### Available Hamiltonians
| Hamiltonian Type | Description | Use Case |
|---|---|---|
| Ising Model (Portfolio) | Quadratic binary optimization encoding | Portfolio selection and allocation |
| QUBO (Optimization) | Quadratic unconstrained binary optimization | Combinatorial finance problems |
| Stochastic Process | GBM, Heston, Ornstein-Uhlenbeck | Derivative pricing |
| Risk Hamiltonian | Tail risk and correlation structure | Value-at-Risk, stress testing |

### Configuration
```json
{
  "hamiltonian": {
    "type": "ising_portfolio",
    "parameters": {
      "num_assets": 1024,
      "risk_aversion": 0.5,
      "constraints": "sector_limits"
    }
  }
}
```

### Encoding Options
- **Jordan-Wigner**: For quantum amplitude estimation in risk computation
- **Bravyi-Kitaev**: Reduced gate depth for large portfolio problems
- **Direct Encoding**: For combinatorial optimization (QUBO/Ising)

---

## Supported Scale

| Parameter | Maximum Value |
|---|---|
| **Qubits** | 2^53 (9,007,199,254,740,992) |
| **Bond Dimension** | 2^53 |
| **Precision** | IEEE 754 double (64-bit float) |

The quantum engine supports computations from small-scale (8 qubits) up to the theoretical maximum of 2^53 qubits with matching bond dimension, enabling simulation of molecular systems from simple hydrogen molecules to complex biological macromolecules and beyond.

