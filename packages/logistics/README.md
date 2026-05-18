# Quantum Logistics Package

## Overview

The Logistics package provides quantum-accelerated combinatorial optimization for vehicle routing, supply chain management, scheduling, and resource allocation through the unified L3 VQE circuit at 65536-qubit scale. It solves NP-hard optimization problems with up to 65536 decision variables.

## Key Features

- **Vehicle routing (VRP)** — optimal fleet routing with 65536 nodes and constraints
- **Supply chain optimization** — multi-echelon inventory and distribution networks
- **Job scheduling** — parallel machine scheduling with precedence constraints
- **Facility location** — optimal warehouse/hub placement across global networks
- **Bin packing** — container loading and resource allocation optimization
- **Network flow** — maximum flow and minimum cost flow at scale
- **Travelling salesman** — exact solutions for TSP with 65536 cities
- **Fleet management** — real-time dynamic routing and rebalancing

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **QAOA** | Combinatorial optimization (all 5 QAOA variants) |
| **QAOA-MaxCut** | Graph partitioning and network design |
| **QAOA-TSP** | Travelling salesman and routing problems |
| **QAOA-Scheduling** | Job shop and flow shop scheduling |
| **QAOA-Coloring** | Resource allocation and conflict resolution |
| **Grover** | Searching feasible solutions in constraint spaces |
| **VQE** | Minimum energy configuration of logistics networks |

## Scale

- **Qubits:** 65536
- **Maximum nodes/cities:** 65536 locations
- **Decision variables:** 65536 binary/integer variables

## Input Data Format

The input data array encodes the optimization problem as 65536 floating-point amplitudes representing the QUBO/Ising formulation.

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "input_data": [/* 65536 float values: QUBO coefficients encoded as amplitudes */],
  "config": {
    "task": "vehicle_routing",
    "num_vehicles": 500,
    "num_locations": 65536,
    "capacity_constraints": true,
    "time_windows": true,
    "qaoa_layers": 12
  }
}
```

**Input encoding:**
- Amplitudes encode the cost matrix or QUBO problem in quantum state form
- Constraints mapped to penalty Hamiltonian terms
- Problem graph structure preserved in the amplitude encoding

## Example API Request

```bash
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NAWAZ1_API_KEY" \
  -d '{
    "domain": "logistics",
    "algorithm": "qaoa",
    "input_data": [1.23, 4.56, 2.34, ... /* 65536 cost/distance values */],
    "config": {
      "task": "vehicle_routing",
      "num_vehicles": 200,
      "num_locations": 10000,
      "capacity": 1000,
      "time_windows": true,
      "qaoa_layers": 8,
      "mixer": "xy"
    }
  }'
```

**Python Example:**

```python
import requests
import numpy as np

# Encode logistics problem as QUBO amplitudes
cost_matrix = np.random.rand(65536)  # Distance/cost encoding
amplitudes = (cost_matrix / np.linalg.norm(cost_matrix)).tolist()

response = requests.post(
    "http://localhost:8080/api/v1/quantum/execute",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "domain": "logistics",
        "algorithm": "qaoa",
        "input_data": amplitudes,
        "config": {
            "task": "vehicle_routing",
            "num_vehicles": 200,
            "num_locations": 10000,
            "qaoa_layers": 8
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
    "optimal_routes": [[0, 45, 123, 67, 0], [0, 89, 234, 56, 0], ...],
    "total_cost": 45678.9,
    "total_distance": 123456.7,
    "num_routes": 200,
    "feasibility": true,
    "optimality_gap": 0.002,
    "observables": {
      "vehicle_utilization": 0.87,
      "average_route_length": 617.3,
      "max_route_time": 480,
      "constraint_violations": 0
    },
    "tensor_expert_used": "LoopTTN",
    "qubit_count": 65536,
    "wall_time_ms": 2876
  }
}
```

## Use Cases

1. **Last-Mile Delivery** — Optimize delivery routes for e-commerce across 65536 addresses
2. **Airline Scheduling** — Crew assignment and flight scheduling for global airline networks
3. **Warehouse Robotics** — Path planning for thousands of autonomous mobile robots
4. **Supply Chain Resilience** — Multi-echelon inventory optimization under disruption scenarios
5. **Port Operations** — Container ship berth allocation and crane scheduling
6. **Telecom Network Design** — Optimal fiber optic routing and cell tower placement
7. **Emergency Response** — Ambulance positioning and disaster evacuation routing
