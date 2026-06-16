# Nawaz1 Database Package — Native + External Integration

nawaz1 provides **two database modes**:

1. **Native Database** — Built-in SQL, bulk import, file import, vector storage, graph traversal, geospatial, security, probabilistic, ML — no external database needed
2. **External Database Integration** — Python connector pattern bridges any external database (PostgreSQL, MongoDB, Neo4j, Milvus, etc.) to the VQE engine

---

## Part 1: Native Database (Built-In)

nawaz1 **IS** a database. No external database needed.

### Native API Endpoints

| Endpoint | Capability |
|----------|-----------|
| `POST /api/v1/auth/register` | Register user |
| `POST /api/v1/auth/login` | JWT token |
| `POST /api/v1/query` | SQL: CREATE, INSERT, SELECT, UPDATE, DELETE |
| `POST /api/v1/bulk-import` | Bulk row import |
| `POST /api/v1/import` | CSV/binary file import |
| `POST /api/v1/quantum/execute` | One-shot VQE computation |
| `POST /api/v1/quantum/pipeline/execute` | Full quantum pipeline |
| `GET /api/v1/quantum/status` | Engine status |

### 1. SQL (Native)

```bash
# Create table
curl -X POST http://localhost:8080/api/v1/query \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "CREATE TABLE experiments (id INT, domain TEXT, energy REAL, fidelity REAL)"}'

# Insert
curl -X POST http://localhost:8080/api/v1/query \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "INSERT INTO experiments VALUES (1, '\''chemistry'\'', -1.137, 0.9998)"}'

# Query with aggregation
curl -X POST http://localhost:8080/api/v1/query \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "SELECT domain, COUNT(*), AVG(energy) FROM experiments GROUP BY domain"}'
```

**Supported SQL:** CREATE TABLE, DROP TABLE, INSERT, SELECT, WHERE, ORDER BY, LIMIT, UPDATE, DELETE, GROUP BY, COUNT, SUM, AVG, MIN, MAX

### 2. Vector (Native)

Store embeddings as orbital energies. VQE energy = similarity score.

```python
embedding = (embedding / np.linalg.norm(embedding)).tolist()
response = requests.post("http://localhost:8080/api/v1/quantum/execute", json={
    "domain": "machine_learning", "algorithm": "vqe", "qubits": 128,
    "problem": {"orbital_energies": embedding}
})
# Lower energy = higher similarity
```

### 3. Graph (Native)

Encode adjacency matrix as orbital energies. QAOA finds optimal paths/partitions.

```python
graph_data = adjacency_matrix.flatten().tolist()
response = requests.post("http://localhost:8080/api/v1/quantum/execute", json={
    "domain": "logistics", "algorithm": "qaoa", "qubits": 64,
    "problem": {"orbital_energies": graph_data}
})
```

### 4. Geospatial (Native)

Encode lat/lon coordinates. Grover-accelerated spatial search.

```python
locations = [40.7128, -74.0060, 34.0522, -118.2437, ...]  # lat,lon pairs
response = requests.post("http://localhost:8080/api/v1/quantum/execute", json={
    "domain": "mathematics", "algorithm": "grover", "qubits": 16,
    "problem": {"orbital_energies": locations}
})
```

### 5. Security (Native)

Built-in database security: JWT auth for data operations, API key for quantum endpoints, AES-GCM-256 encryption at rest, SQL injection prevention, cross-user isolation, and VQE-powered anomaly detection on security event data.

```bash
# ── Step 1: Register + Login (JWT) ──
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"analyst","password":"Pass123!","email":"a@b.com"}'

TOKEN=$(curl -s -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"analyst","password":"Pass123!"}' | jq -r .token)

# ── Step 2: Create security audit table (JWT-protected) ──
curl -X POST http://localhost:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query":"CREATE TABLE security_events (id INT, event_type TEXT, severity REAL, source_ip TEXT, ts TEXT)"}'

# ── Step 3: Insert security events ──
curl -X POST http://localhost:8080/api/v1/bulk-import \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"table":"security_events","columns":["id","event_type","severity","source_ip","ts"],
    "rows":[[1,"login_fail",0.85,"10.0.0.5","2026-01-15T10:00:00Z"],
           [2,"port_scan",0.92,"10.0.0.9","2026-01-15T10:01:00Z"],
           [3,"brute_force",0.78,"10.0.0.5","2026-01-15T10:02:00Z"],
           [4,"data_export",0.45,"10.0.0.3","2026-01-15T10:03:00Z"]]}'

# ── Step 4: Query high-severity events (SQL) ──
curl -X POST http://localhost:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query":"SELECT event_type, severity, source_ip FROM security_events WHERE severity > 0.8 ORDER BY severity DESC"}'

# ── Step 5: VQE anomaly detection on event features ──
# Encode security event features (severity, frequency, risk) as orbital energies
curl -X POST http://localhost:8080/api/v1/quantum/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"domain":"machine_learning","algorithm":"vqe","num_qubits":16,
    "problem":{"orbital_energies":[0.85,0.12,0.45,0.92,0.03,0.78,0.15,0.67,0.91,0.34,0.56,0.23,0.88,0.72,0.41,0.95]}}'
# Lower aggregate_energy = more anomalous cluster
```

**Database security layers:**

| Layer | Protection |
|-------|------------|
| JWT auth | Required for all data operations (query, import, bulk-import) |
| API key | Optional `X-API-Key` header for quantum endpoints (set via `NAWAZ1_API_KEY` env var) |
| AES-GCM-256 | Encryption at rest for all stored data |
| SQL injection | Malicious payloads blocked or safely handled |
| Cross-user isolation | Users cannot access each other's tables |
| Rate limiting | Abuse prevention on all endpoints |
| VQE anomaly scoring | Quantum-powered threat detection on security event data |

### 6. Probabilistic (Native)

Orbital energies = probability amplitudes (Born rule). VQE computes posterior inference.

```python
cpt = [0.3, 0.7, 0.1, 0.9, 0.8, 0.2]  # P(A), P(B|A)
evidence = [0.0, 1.0]  # A=1 observed
combined = cpt + evidence + [0.0, 1.0] + [0.0] * 8
response = requests.post("http://localhost:8080/api/v1/quantum/execute", json={
    "domain": "mathematics", "algorithm": "vqe", "qubits": 16,
    "problem": {"orbital_energies": combined}
})
```

### 7. ML Feature Store (Native)

SQL tables + quantum feature selection via QAOA.

```python
# Create feature table
requests.post(f"{SERVER}/query", headers=headers,
    json={"query": "CREATE TABLE features (id INT, name TEXT, importance REAL, model TEXT)"})

# Bulk import
requests.post(f"{SERVER}/bulk-import", headers=headers,
    json={"table": "features", "columns": ["id","name","importance","model"],
          "rows": [[1,"credit_score",0.85,"xgboost"],[2,"income",0.72,"xgboost"]]})

# Quantum feature selection
response = requests.post(f"{SERVER}/quantum/execute", json={
    "domain": "machine_learning", "algorithm": "qaoa", "qubits": 8,
    "problem": {"orbital_energies": [0.85, 0.72, 0.45, 0.91, 0.33, 0.67, 0.12, 0.78]}
})
```

### 8. File Metadata (Native)

Import CSV/binary files. Engine extracts metadata automatically.

```bash
# Import CSV
curl -X POST http://localhost:8080/api/v1/import -F "file=@data.csv"

# Bulk import structured metadata
curl -X POST http://localhost:8080/api/v1/bulk-import \
  -d '{"table":"files","columns":["name","size","type"],
    "rows":[["report.pdf",1048576,"pdf"],["data.csv",524288,"csv"]]}'
```

### Accumulator Tiers

| Tier | Qubits | Query Capabilities |
|------|--------|-------------------|
| 3Q | 3 | COUNT, SUM, AVG, MIN, MAX, VARIANCE, SKEWNESS, ENTROPY |
| 32Q | 32 | + percentile, median, mode, kurtosis, moments, correlation |
| 64Q | 64 | + autocorrelation, volatility, FFT, extreme value theory |
| 256Q | 256 | + anomaly score, feature importance, cluster validity |
| 512Q | 512 | + topology (Betti, Chern), phase space, symmetry |
| 1024Q | 1024 | + holographic physics, complexity science, RG flow |

---

## Part 2: External Database Integration (Python Connector)

For connecting nawaz1 to **external databases** (PostgreSQL, MySQL, MongoDB, Neo4j, Milvus, etc.), use the Python connector pattern:

```
External DB → Python Connector → Extract Metadata → Encode as orbital_energies → VQE Engine → Result
```

**Plugins do NOT open network sockets.** Your Python app connects to the external database, extracts relevant data, and sends it to the VQE engine.

### Supported External Databases

| Type | Databases | Best Algorithm |
|------|----------|---------------|
| SQL | PostgreSQL, MySQL, SQLite | `qaoa` (join ordering, index selection) |
| Vector | Milvus, Pinecone, Weaviate, Qdrant, ChromaDB | `vqe` (HNSW, IVF optimization) |
| Graph | Neo4j, Neptune, JanusGraph, TigerGraph | `qaoa` (shortest path, community) |
| Geospatial | PostGIS, MongoDB Geo, Elasticsearch Geo | `grover` (K-NN, bounding box) |
| Security | Splunk, Sentinel, CrowdStrike, Wazuh | `vqe` (threat anomaly scoring) |
| Probabilistic | pgmpy, PyMC, Stan, GPyTorch | `vqe` (Bayesian inference) |
| ML | MLflow, W&B, Feast, Tecton, Hopsworks | `qaoa` (feature selection) |

### Python Connector Example (SQLite)

```python
import sqlite3, requests, numpy as np

# 1. Connect to external database
conn = sqlite3.connect("my_database.db")
cur = conn.cursor()

# 2. Extract table statistics
cur.execute("SELECT COUNT(*) FROM orders")
row_count = cur.fetchone()[0]
cur.execute("PRAGMA table_info(orders)")
col_count = len(cur.fetchall())

# 3. Encode as orbital_energies
stats = [np.log10(row_count), col_count, 0.003, 5.2, 3.5, 0.85, 2.1, 4.0]

# 4. Send to VQE engine
response = requests.post("http://localhost:8080/api/v1/quantum/execute", json={
    "domain": "mathematics", "algorithm": "qaoa", "qubits": 8,
    "problem": {"orbital_energies": stats}
})
print(f"Query plan energy: {response.json()['result']['aggregate_energy']}")
```

### Python Connector Example (PostgreSQL)

```python
import psycopg2, requests

conn = psycopg2.connect("dbname=mydb user=admin")
cur = conn.cursor()
cur.execute("SELECT reltuples, relpages FROM pg_class WHERE relname = 'orders'")
row_count, pages = cur.fetchone()

stats = [np.log10(row_count), pages, 0.003] + [0.0] * 13
response = requests.post("http://localhost:8080/api/v1/quantum/execute", json={
    "domain": "mathematics", "algorithm": "qaoa", "qubits": 16,
    "problem": {"orbital_energies": stats}
})
```

### Python Connector Example (Neo4j Graph)

```python
from neo4j import GraphDatabase
import requests, numpy as np

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
with driver.session() as session:
    result = session.run("MATCH (n) RETURN count(n) AS nodes")
    n_nodes = result.single()["nodes"]
    adj_result = session.run(
        "MATCH (a)-[r]->(b) RETURN id(a) AS src, id(b) AS dst, weight(r) AS w")
    
    adj = np.zeros((n_nodes, n_nodes))
    for record in adj_result:
        adj[record["src"], record["dst"]] = record["w"]

graph_data = adj.flatten().tolist() + [float(n_nodes), 4.0, 2.0, 0.5]
response = requests.post("http://localhost:8080/api/v1/quantum/execute", json={
    "domain": "logistics", "algorithm": "qaoa", "qubits": 128,
    "problem": {"orbital_energies": graph_data}
})
```

### Python Connector Example (Milvus Vector DB)

```python
from pymilvus import connections, Collection
import requests, numpy as np

connections.connect(host="localhost", port="19530")
collection = Collection("embeddings")

# Extract collection stats
stats = collection.get_stats()
n_vectors = int(stats["row_count"])
dim = collection.schema.fields[-1].params.get("dim", 128)

# Encode query + index metadata
query_vec = np.random.normal(0, 1, dim)
query_vec = (query_vec / np.linalg.norm(query_vec)).tolist()
meta = [float(dim), float(n_vectors), 0.95, 16.0, 200.0, 100.0, 4096.0, 128.0]

combined = query_vec + meta
while len(combined) < 256:
    combined.append(0.0)

response = requests.post("http://localhost:8080/api/v1/quantum/execute", json={
    "domain": "machine_learning", "algorithm": "vqe", "qubits": 256,
    "problem": {"orbital_energies": combined[:256]}
})
```

### Security: Why External Connectors Are Safe

| Layer | Protection |
|-------|-----------|
| No direct DB connection | VQE engine never touches external databases |
| Orbital energies only | Engine only accepts normalized float vectors |
| Binary-only | No source code to reverse engineer |
| One-way encoding | Can't reconstruct original data from amplitudes |
| Kill-switch | Binary can be remotely disabled |

---

## Full Workflow: Native + External Combined

```python
import requests

SERVER = "http://localhost:8080/api/v1"

# ── Native: Authenticate ──
token = requests.post(f"{SERVER}/auth/login",
    json={"username": "admin", "password": "admin123"}).json()["token"]
headers = {"Authorization": f"Bearer {token}"}

# ── Native: Create table + import data ──
requests.post(f"{SERVER}/query", headers=headers,
    json={"query": "CREATE TABLE molecules (id INT, name TEXT, energy REAL, fidelity REAL)"})
requests.post(f"{SERVER}/bulk-import", headers=headers,
    json={"table": "molecules", "columns": ["id","name","energy","fidelity"],
          "rows": [[1,"H2",-1.137,0.9998],[2,"LiH",-7.882,0.9995]]})

# ── Native: Query data ──
result = requests.post(f"{SERVER}/query", headers=headers,
    json={"query": "SELECT * FROM molecules WHERE fidelity > 0.999"}).json()

# ── External: Pull data from PostgreSQL, send to VQE ──
import psycopg2
pg = psycopg2.connect("dbname=prod")
pg_cur = pg.cursor()
pg_cur.execute("SELECT orbital_energy FROM hamiltonians WHERE molecule = 'H2O'")
external_data = [row[0] for row in pg_cur.fetchall()]

# ── Quantum: Run VQE on combined native + external data ──
response = requests.post(f"{SERVER}/quantum/execute", json={
    "domain": "chemistry", "algorithm": "vqe", "qubits": 16,
    "problem": {"orbital_energies": external_data}
}).json()
print(f"Energy: {response['result']['aggregate_energy']}")

# ── Native: Store result back ──
requests.post(f"{SERVER}/query", headers=headers,
    json={"query": f"INSERT INTO molecules VALUES (3, 'H2O', {response['result']['aggregate_energy']}, {response['result']['fidelity']})"})
```

---

## Important Rules

1. **JWT token required** for all data operations (query, import, bulk-import)
2. **Correct Hamiltonian** — orbital_energies must represent valid problem data
3. **Qubits = Power of 2** — 4, 8, 16, 32, 64, 128, 256, ...
4. **Use `problem.orbital_energies`** — Not `input_data` (which is ignored)
5. **No external DB credentials in engine** — Python connector handles auth

---

## Related Documentation

- [Data Import Examples](../data_import_examples.py) — Complete Python examples
- [Quick Start](QUICKSTART.md) — Get started in 5 minutes
- [Architecture](ARCHITECTURE.md) — How the engine works
- [All Algorithms](../ALL_ALGORITHMS_INPUT_METHODS.md) — 108 algorithms reference
- [Solvation QFT](SOLVATION_QFT.md) — Cross-domain chemistry/biology/physics
