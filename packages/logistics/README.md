# Quantum Logistics Package

## Overview

The Logistics package provides quantum-accelerated combinatorial optimization through the unified VQE engine at 2^53-qubit scale, powered by 63 quantum algorithms. It encompasses **6 specialized sub-modules** covering vehicle routing, scheduling, facility location, traveling salesman, network flow, and bin packing — solving classically NP-hard optimization problems with up to 2^53 decision variables in a single quantum execution.

**API Endpoint:** `POST http://localhost:8080/api/v1/quantum/logistics`

**Demo Endpoint:** `POST http://localhost:8080/api/v1/quantum/logistics/demo`

---

## The 6 Quantum Logistics Sub-Modules

| # | Sub-Module | Key Domain Areas |
|---|-----------|------------|
| 1 | Vehicle Routing  | Fleet optimization, multi-depot VRP, time windows, capacity constraints |
| 2 | Scheduling  | Job scheduling, resource allocation, shift planning, project scheduling |
| 3 | Facility Location  | Warehouse placement, distribution center optimization, coverage maximization |
| 4 | Traveling Salesman  | Route optimization, tour planning, shortest path, multi-city routing |
| 5 | Network Flow  | Supply chain flow, min-cost max-flow, network capacity, distribution optimization |
| 6 | Bin Packing  | Container loading, space optimization, cutting stock, 3D packing |

---

## 1. Vehicle Routing (VRP)


Solves vehicle routing problems at fleet scale with multi-depot support, time windows, capacity constraints, and heterogeneous vehicle profiles. Encodes the VRP as a QUBO over edge-selection variables and minimizes total route cost via QAOA.

**Key Capabilities:**
- Capacitated VRP (CVRP) with per-vehicle load limits
- Vehicle Routing with Time Windows (VRPTW) and hard/soft window penalties
- Multi-Depot VRP (MDVRP) with depot-to-customer assignment
- Heterogeneous fleet support (mixed truck sizes, electric vehicles, range limits)
- Pickup-and-delivery (PDVRP) and split-delivery variants
- Dynamic re-routing with real-time disruption handling

**When to Use:** Last-mile delivery optimization, fleet dispatching for distribution networks, urban courier routing, and same-day logistics planning across thousands of stops.

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "input_data": [1.23, 4.56, 2.34, "...N cost-matrix amplitudes..."],
  "config": {
    "sub_module": "vehicle_routing",
    "task": "capacitated_vrp",
    "num_vehicles": 200,
    "num_locations": 10000,
    "vehicle_capacity": 1000,
    "time_windows": true,
    "depot_strategy": "multi_depot",
    "qaoa_layers": 12,
    "mixer": "xy"
  }
}
```

---

## 2. Scheduling


Provides quantum-accelerated scheduling across job-shop, flow-shop, resource-constrained, and shift-planning problems. Models precedence, resource, and deadline constraints as a unified Hamiltonian and minimizes makespan or weighted tardiness.

**Key Capabilities:**
- Job-shop scheduling (JSSP) with arbitrary machine routings
- Flow-shop and open-shop scheduling with sequence-dependent setup times
- Resource-Constrained Project Scheduling (RCPSP) with renewable/non-renewable resources
- Shift planning and crew rostering with skill matching
- Parallel machine scheduling with precedence DAGs
- Multi-objective scheduling (makespan, tardiness, energy cost)

**When to Use:** Manufacturing line scheduling, hospital staff rostering, airline crew assignment, project portfolio scheduling, and cloud workload placement under SLA constraints.

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "input_data": [0.42, 1.18, 0.97, "...N schedule amplitudes..."],
  "config": {
    "sub_module": "scheduling",
    "task": "job_shop_scheduling",
    "num_jobs": 512,
    "num_machines": 64,
    "objective": "minimize_makespan",
    "precedence_constraints": true,
    "setup_times": "sequence_dependent",
    "qaoa_layers": 10
  }
}
```

---

## 3. Facility Location


Solves uncapacitated and capacitated facility location problems including warehouse placement, distribution center siting, and coverage maximization. Encodes opening costs and assignment costs jointly into a QUBO suitable for VQE evaluation.

**Key Capabilities:**
- Uncapacitated Facility Location Problem (UFLP)
- Capacitated Facility Location Problem (CFLP) with per-facility throughput limits
- p-Median and p-Center problems for service-level guarantees
- Maximum Coverage Location Problem (MCLP) with demand weighting
- Hub-and-spoke network design with hub-arc cost discounts
- Multi-tier distribution network optimization (plant → DC → store)

**When to Use:** Strategic warehouse placement, retail store siting, EV charging-station deployment, emergency-service positioning, and global supply chain network redesign.

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "input_data": [3.14, 2.71, 1.41, "...N location-cost amplitudes..."],
  "config": {
    "sub_module": "facility_location",
    "task": "capacitated_facility_location",
    "num_candidate_sites": 4096,
    "num_demand_points": 1024,
    "max_open_facilities": 50,
    "facility_capacity": 25000,
    "objective": "minimize_total_cost",
    "qaoa_layers": 8
  }
}
```

---

## 4. Traveling Salesman (TSP)


Solves the classical and generalized TSP using QAOA-TSP with city-permutation encoding. Supports symmetric, asymmetric, and time-dependent distance matrices, plus multi-objective tours combining distance, time, and energy cost.

**Key Capabilities:**
- Symmetric and asymmetric TSP (STSP / ATSP)
- Multiple Traveling Salesman Problem (mTSP) for parallel tours
- Generalized TSP (GTSP) with city clusters
- Time-dependent TSP for traffic-aware routing
- Prize-collecting TSP with optional city visits
- Tour planning with start/end constraints and forbidden edges

**When to Use:** Drone delivery tour planning, route optimization for service technicians, sequencing for PCB drilling and 3D-printer toolpaths, and tourist itinerary construction across thousands of points of interest.

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "input_data": [12.4, 8.7, 15.2, "...N distance amplitudes..."],
  "config": {
    "sub_module": "traveling_salesman",
    "task": "asymmetric_tsp",
    "num_cities": 4096,
    "distance_metric": "euclidean",
    "tour_constraints": {
      "start_city": 0,
      "return_to_start": true,
      "forbidden_edges": []
    },
    "qaoa_layers": 14
  }
}
```

---

## 5. Network Flow


Optimizes flow across supply-chain and distribution networks including maximum flow, minimum-cost flow, and multi-commodity flow problems. Models capacity, conservation, and lower-bound constraints inside the VQE circuit for end-to-end network optimization.

**Key Capabilities:**
- Maximum flow (max-flow / min-cut) on directed capacitated graphs
- Minimum-cost flow with arc costs and demand balance
- Multi-commodity flow with shared capacity constraints
- Transportation and transshipment problems
- Network interdiction and resilience analysis
- Stochastic network flow with demand uncertainty

**When to Use:** End-to-end supply chain flow optimization, oil and gas pipeline scheduling, electricity grid dispatch, telecom bandwidth allocation, and water distribution network design.

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "input_data": [0.83, 1.27, 2.04, "...N capacity amplitudes..."],
  "config": {
    "sub_module": "network_flow",
    "task": "min_cost_max_flow",
    "num_nodes": 1024,
    "num_arcs": 524288,
    "source_nodes": [0, 1, 2],
    "sink_nodes": [65533, 65534, 65535],
    "objective": "minimize_transport_cost",
    "qaoa_layers": 10
  }
}
```

---

## 6. Bin Packing


Solves one-, two-, and three-dimensional bin-packing and cutting-stock problems for container loading and material utilization. Encodes item-to-bin assignment and rotation as a QUBO, with rotational and stacking constraints for 3D loading scenarios.

**Key Capabilities:**
- 1D bin packing (item lengths into fixed-length bins)
- 2D bin packing for sheet cutting and pallet layout
- 3D bin packing with rotation, stacking, and weight-distribution constraints
- Cutting-stock problem for raw-material yield maximization
- Variable-sized bin packing (VSBPP)
- Online and offline packing with arrival uncertainty

**When to Use:** Container and truck loading, warehouse pallet building, e-commerce parcel sortation, sheet-metal and textile cutting optimization, and shipping-cost minimization for e-commerce fulfillment.

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "input_data": [0.55, 0.78, 1.12, "...N item-size amplitudes..."],
  "config": {
    "sub_module": "bin_packing",
    "task": "three_d_bin_packing",
    "num_items": 8192,
    "num_bins": 256,
    "bin_dimensions": [1200, 1000, 2400],
    "rotation_allowed": true,
    "stacking_constraints": true,
    "weight_limit_per_bin": 25000,
    "qaoa_layers": 8
  }
}
```

---

## General Request Format

All sub-modules are accessed through the unified quantum execution endpoint:

```
POST http://localhost:8080/api/v1/quantum/logistics
```

**Request body:**

```json
{
  "domain": "logistics",
  "algorithm": "qaoa",
  "input_data": [/* N float amplitude values encoding the QUBO/Ising problem (up to 2^53) */],
  "config": {
    "sub_module": "<feature_name>"
  }
}
```

**Demo endpoint (no input_data required):**

```
POST http://localhost:8080/api/v1/quantum/logistics/demo
```

**Example response:**

```json
{
  "status": "success",
  "result": {
    "optimal_routes": [[0, 45, 123, 67, 0], [0, 89, 234, 56, 0]],
    "total_cost": 45678.9,
    "total_distance": 123456.7,
    "feasibility": true,
    "optimality_gap": 0.002,
    "observables": {
      "vehicle_utilization": 0.87,
      "average_route_length": 617.3,
      "constraint_violations": 0
    },
    "qubit_count": 1024,
    "wall_time_ms": 2876
  }
}
```

---

## Scale

- **Qubits:** Up to 2^53
- **Decision variables:** Up to 2^53 binary/integer variables
- **Maximum nodes/cities:** 2^53 locations per problem instance
- **Problem encoding:** QUBO / Ising formulation via amplitude encoding

---

## Supported Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **QAOA** | General combinatorial optimization (all 5 QAOA variants) |
| **QAOA-MaxCut** | Graph partitioning, network design, clustering |
| **QAOA-TSP** | Traveling salesman and tour-routing problems |
| **QAOA-Scheduling** | Job-shop, flow-shop, and project scheduling |
| **QAOA-Coloring** | Resource allocation, conflict-free assignment |
| **Grover** | Search over feasible solutions in constrained spaces |
| **QBS** | Quantum Binary Search for ordered solution lookup |
| **VQE** | Minimum-energy configuration of logistics Hamiltonians |

---

## Python Example (Full Workflow)

```python
import requests
import numpy as np

API = "http://localhost:8080/api/v1/quantum/logistics"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}

# Encode logistics problem (engine supports up to 2^53 variables) as amplitudes
rng = np.random.RandomState(42)
cost_matrix = rng.rand(1024)  # Example; engine supports up to 2^53
amplitudes = (cost_matrix / np.linalg.norm(cost_matrix)).tolist()

# Example 1: Vehicle Routing (VRP) with capacity and time windows
vrp_response = requests.post(API, headers=HEADERS, json={
    "domain": "logistics",
    "algorithm": "qaoa",
    "input_data": amplitudes,
    "config": {
        "sub_module": "vehicle_routing",
        "task": "capacitated_vrp",
        "num_vehicles": 200,
        "num_locations": 10000,
        "vehicle_capacity": 1000,
        "time_windows": True,
        "qaoa_layers": 8
    }
})
print("VRP result:", vrp_response.json())

# Example 2: Traveling Salesman across 4096 cities
tsp_response = requests.post(API, headers=HEADERS, json={
    "domain": "logistics",
    "algorithm": "qaoa",
    "input_data": amplitudes,
    "config": {
        "sub_module": "traveling_salesman",
        "task": "asymmetric_tsp",
        "num_cities": 4096,
        "distance_metric": "euclidean",
        "qaoa_layers": 14
    }
})
print("TSP result:", tsp_response.json())

# Example 3: Network flow optimization for supply chain
flow_response = requests.post(API, headers=HEADERS, json={
    "domain": "logistics",
    "algorithm": "qaoa",
    "input_data": amplitudes,
    "config": {
        "sub_module": "network_flow",
        "task": "min_cost_max_flow",
        "num_nodes": 1024,
        "objective": "minimize_transport_cost",
        "qaoa_layers": 10
    }
})
print("Network flow result:", flow_response.json())
```

---

## Use Cases

| Industry / Research Area | Relevant Sub-Modules |
|--------------------------|---------------------|
| **Last-Mile Delivery & E-Commerce** | Vehicle Routing, Bin Packing, Traveling Salesman |
| **Airline Operations** | Scheduling, Network Flow, Facility Location |
| **Warehouse Robotics & Automation** | Vehicle Routing, Scheduling, Traveling Salesman |
| **Global Supply Chain Resilience** | Network Flow, Facility Location, Scheduling |
| **Port & Container Operations** | Bin Packing, Scheduling, Network Flow |
| **Telecom Network Design** | Network Flow, Facility Location |
| **Emergency Response & Healthcare** | Facility Location, Vehicle Routing, Scheduling |
| **Manufacturing & Job Shops** | Scheduling, Bin Packing, Network Flow |
| **Smart Grid & Energy Distribution** | Network Flow, Facility Location |
| **Field-Service Routing** | Traveling Salesman, Vehicle Routing, Scheduling |
| **Retail Store & EV-Charger Siting** | Facility Location, Network Flow |
| **Cutting Stock & Material Yield** | Bin Packing, Scheduling |

---

## Input Method

### API Endpoint
```
POST http://localhost:8080/api/v1/quantum/logistics
```

### Request Format
```json
{
  "problem": "vehicle_routing",
  "config": {
    "num_qubits": 1024,
    "optimizer": "SPSA",
    "max_iterations": 100
  },
  "input_data": [1.23, 4.56, 2.34, "...Born-normalized floats..."]
}
```

### Supported Problem Types
- `"vehicle_routing"` — Fleet optimization with capacity and time windows
- `"supply_chain_optimization"` — End-to-end supply chain network flow

### Data Input Options
- **Direct API**: Send JSON payload with amplitudes (Born-normalized floats)
- **File Import**: Upload binary/CSV data files via the import endpoint
- **Streaming**: For large datasets, use chunked streaming mode

---

## Hamiltonian Selection

### Available Hamiltonians
| Hamiltonian Type | Description | Use Case |
|---|---|---|
| QUBO | Quadratic unconstrained binary optimization | General combinatorial problems |
| TSP | Traveling salesman encoding | Route optimization |
| MaxCut | Graph partitioning Hamiltonian | Network design, clustering |
| Ising (Scheduling) | Spin-glass encoding of constraints | Job-shop, resource allocation |

### Configuration
```json
{
  "hamiltonian": {
    "type": "qubo",
    "parameters": {
      "num_variables": 1024,
      "constraint_type": "capacity",
      "penalty_weight": 10.0
    }
  }
}
```

### Encoding Options
- **Jordan-Wigner**: For quantum walk-based route exploration
- **Bravyi-Kitaev**: Reduced gate depth for large optimization problems
- **Direct Encoding**: For combinatorial optimization (QUBO/Ising native)

---

## Supported Scale

| Parameter | Maximum Value |
|---|---|
| **Qubits** | 2^53 (9,007,199,254,740,992) |
| **Bond Dimension** | 2^53 |
| **Precision** | IEEE 754 double (64-bit float) |

The quantum engine supports computations from small-scale (8 qubits) up to the theoretical maximum of 2^53 qubits with matching bond dimension, enabling simulation of molecular systems from simple hydrogen molecules to complex biological macromolecules and beyond.

