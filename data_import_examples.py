#!/usr/bin/env python3
"""
Nawaz1 Quantum VQE Engine - Data Import & SQL Examples
======================================================
Demonstrates authentication, table management, data import (single & batch),
querying, and pipeline execution on imported data.

Author: Shahnawaz Alam
License: Proprietary
Copyright (c) 2026 Shahnawaz Alam. All rights reserved.

Requirements:
    - Python 3.8+
    - requests library (pip install requests)
    - Nawaz1 server running (default: http://localhost:8080)

Usage:
    python data_import_examples.py          # Run all examples
    python data_import_examples.py auth     # Run specific section
"""

import requests
import json
import sys
import os
import time

# =============================================================================
# Configuration
# =============================================================================
HOST = os.environ.get("NAWAZ1_HOST", "localhost")
PORT = os.environ.get("NAWAZ1_PORT", "8080")
BASE_URL = f"http://{HOST}:{PORT}/api/v1"
API_KEY = os.environ.get("NAWAZ1_API_KEY", "")

# Global token storage
TOKEN = None


def get_headers(auth=True):
    """Build request headers with optional auth token and API key."""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["X-API-Key"] = API_KEY
    if auth and TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


# =============================================================================
# SECTION 1: Authentication (Register + Login)
# =============================================================================
def demo_auth():
    """
    Register a new user and login to get a JWT token.
    The token is required for data operations (CREATE, INSERT, SELECT, etc.)
    """
    global TOKEN
    print_section("AUTHENTICATION - Register & Login")
    
    # Step 1: Register a new user
    print("  Step 1: Register new user")
    register_payload = {
        "username": "quantum_user",
        "password": "QuantumPass123!",
        "email": "quantum@example.com"
    }
    print(f"  POST {BASE_URL}/auth/register")
    print(f"  Body: {json.dumps(register_payload)}")
    
    try:
        resp = requests.post(
            f"{BASE_URL}/auth/register",
            json=register_payload,
            headers=get_headers(auth=False),
            timeout=10
        )
        print(f"  Status: {resp.status_code}")
        print(f"  Response: {resp.text[:200]}")
        # Registration may fail if user exists - that's OK
    except Exception as e:
        print(f"  Error: {e}")
    
    print()
    
    # Step 2: Login to get JWT token
    print("  Step 2: Login to obtain JWT token")
    login_payload = {
        "username": "quantum_user",
        "password": "QuantumPass123!"
    }
    print(f"  POST {BASE_URL}/auth/login")
    print(f"  Body: {json.dumps(login_payload)}")
    
    try:
        resp = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_payload,
            headers=get_headers(auth=False),
            timeout=10
        )
        print(f"  Status: {resp.status_code}")
        result = resp.json()
        print(f"  Response: {json.dumps(result, indent=2)[:300]}")
        
        # Extract token (server may use 'token' or 'access_token')
        TOKEN = result.get("token") or result.get("access_token")
        if TOKEN:
            print(f"\n  SUCCESS: JWT Token acquired (first 20 chars): {TOKEN[:20]}...")
            print("  Token will be used in Authorization: Bearer <token> header")
        else:
            print("\n  NOTE: No token in response - server may be in open-access mode")
    except Exception as e:
        print(f"  Error: {e}")
        print("  Continuing without auth (server may be in dev/open mode)")
    
    # Also demonstrate admin login (default credentials)
    print("\n  Alternative: Admin login (default credentials)")
    print('  Body: {"username": "admin", "password": "admin123"}')


# =============================================================================
# SECTION 2: Table Management (CREATE, DROP)
# =============================================================================
def demo_tables():
    """
    Create and manage database tables for storing quantum experiment data.
    Uses SQL-like syntax via the /api/v1/query endpoint.
    """
    print_section("TABLE MANAGEMENT - Create & Manage Tables")
    
    queries = [
        # Drop existing table (cleanup)
        {
            "description": "Drop existing table (if any)",
            "query": "DROP TABLE IF EXISTS quantum_experiments"
        },
        # Create experiment tracking table
        {
            "description": "Create quantum experiments table",
            "query": """CREATE TABLE quantum_experiments (
                id INT PRIMARY KEY,
                domain TEXT,
                molecule TEXT,
                num_qubits INT,
                energy REAL,
                fidelity REAL,
                iterations INT,
                timestamp TEXT
            )"""
        },
        # Create molecular data table
        {
            "description": "Create molecular data table",
            "query": """CREATE TABLE molecules (
                id INT PRIMARY KEY,
                name TEXT,
                formula TEXT,
                bond_length REAL,
                num_atoms INT,
                charge INT,
                multiplicity INT
            )"""
        },
        # Create sensor data table (for real-time domain)
        {
            "description": "Create sensor readings table",
            "query": """CREATE TABLE sensor_readings (
                id INT PRIMARY KEY,
                sensor_id TEXT,
                temperature REAL,
                pressure REAL,
                flow_rate REAL,
                timestamp TEXT
            )"""
        },
    ]
    
    for item in queries:
        print(f"  {item['description']}")
        print(f"  POST {BASE_URL}/query")
        payload = {"query": item["query"].replace("\n", " ").strip()}
        print(f"  SQL: {payload['query'][:100]}...")
        
        try:
            resp = requests.post(
                f"{BASE_URL}/query",
                json=payload,
                headers=get_headers(),
                timeout=10
            )
            print(f"  Status: {resp.status_code} - {resp.text[:100]}")
        except Exception as e:
            print(f"  Error: {e}")
        print()


# =============================================================================
# SECTION 3: Data Import - Single Row Insert
# =============================================================================
def demo_single_insert():
    """
    Insert individual rows into tables.
    Useful for real-time data logging from quantum experiments.
    """
    print_section("SINGLE ROW INSERT - One record at a time")
    
    rows = [
        ("Hydrogen molecule VQE result",
         "INSERT INTO quantum_experiments VALUES (1, 'chemistry', 'H2', 4, -1.137, 0.9998, 45, '2026-01-15T10:30:00Z')"),
        ("Lithium Hydride result",
         "INSERT INTO quantum_experiments VALUES (2, 'chemistry', 'LiH', 12, -7.882, 0.9995, 120, '2026-01-15T10:35:00Z')"),
        ("Water molecule result",
         "INSERT INTO quantum_experiments VALUES (3, 'chemistry', 'H2O', 14, -75.456, 0.9991, 200, '2026-01-15T10:40:00Z')"),
        ("Heisenberg model result",
         "INSERT INTO quantum_experiments VALUES (4, 'physics', 'heisenberg_8', 16, -3.651, 0.9997, 85, '2026-01-15T11:00:00Z')"),
        ("Portfolio optimization result",
         "INSERT INTO quantum_experiments VALUES (5, 'finance', 'portfolio_8', 8, -0.152, 0.9999, 30, '2026-01-15T11:15:00Z')"),
    ]
    
    for desc, sql in rows:
        print(f"  {desc}")
        print(f"  SQL: {sql[:80]}...")
        try:
            resp = requests.post(
                f"{BASE_URL}/query",
                json={"query": sql},
                headers=get_headers(),
                timeout=10
            )
            print(f"  Result: {resp.status_code} - {resp.text[:80]}")
        except Exception as e:
            print(f"  Error: {e}")
        print()


# =============================================================================
# SECTION 4: Batch Import - Multiple Rows
# =============================================================================
def demo_batch_import():
    """
    Insert multiple rows in a single request for high-throughput import.
    Ideal for importing datasets (CSV, experiment logs, sensor data).
    """
    print_section("BATCH IMPORT - Multiple rows in one request")
    
    # Method 1: Multi-value INSERT
    print("  Method 1: Multi-value INSERT statement")
    batch_sql = """INSERT INTO molecules VALUES 
        (1, 'Hydrogen', 'H2', 0.74, 2, 0, 1),
        (2, 'Lithium Hydride', 'LiH', 1.60, 2, 0, 1),
        (3, 'Water', 'H2O', 0.96, 3, 0, 1),
        (4, 'Beryllium Hydride', 'BeH2', 1.30, 3, 0, 1),
        (5, 'Methane', 'CH4', 1.09, 5, 0, 1),
        (6, 'Ammonia', 'NH3', 1.01, 4, 0, 1),
        (7, 'Hydrogen Fluoride', 'HF', 0.92, 2, 0, 1),
        (8, 'Carbon Monoxide', 'CO', 1.13, 2, 0, 1),
        (9, 'Nitrogen', 'N2', 1.10, 2, 0, 1),
        (10, 'Oxygen', 'O2', 1.21, 2, 0, 2)"""
    
    print(f"  SQL: INSERT INTO molecules VALUES (1, ...), (2, ...), ... (10 rows)")
    try:
        resp = requests.post(
            f"{BASE_URL}/query",
            json={"query": batch_sql.replace("\n", " ").strip()},
            headers=get_headers(),
            timeout=30
        )
        print(f"  Result: {resp.status_code} - {resp.text[:150]}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print()
    
    # Method 2: Bulk import endpoint (if available)
    print("  Method 2: Bulk import endpoint (/api/v1/bulk-import)")
    bulk_payload = {
        "table": "sensor_readings",
        "columns": ["id", "sensor_id", "temperature", "pressure", "flow_rate", "timestamp"],
        "rows": [
            [1, "TEMP-001", 298.15, 101.325, 2.5, "2026-01-15T12:00:00Z"],
            [2, "TEMP-001", 298.45, 101.310, 2.6, "2026-01-15T12:01:00Z"],
            [3, "TEMP-001", 299.10, 101.290, 2.4, "2026-01-15T12:02:00Z"],
            [4, "TEMP-002", 310.25, 102.100, 3.1, "2026-01-15T12:00:00Z"],
            [5, "TEMP-002", 310.50, 102.050, 3.0, "2026-01-15T12:01:00Z"],
            [6, "PRESS-001", 295.00, 98.500, 1.8, "2026-01-15T12:00:00Z"],
            [7, "PRESS-001", 295.20, 98.480, 1.9, "2026-01-15T12:01:00Z"],
            [8, "FLOW-001", 300.00, 101.000, 5.5, "2026-01-15T12:00:00Z"],
            [9, "FLOW-001", 300.10, 101.010, 5.6, "2026-01-15T12:01:00Z"],
            [10, "FLOW-001", 300.05, 100.990, 5.4, "2026-01-15T12:02:00Z"],
        ]
    }
    
    print(f"  POST {BASE_URL}/bulk-import")
    print(f"  Body: table={bulk_payload['table']}, {len(bulk_payload['rows'])} rows")
    try:
        resp = requests.post(
            f"{BASE_URL}/bulk-import",
            json=bulk_payload,
            headers=get_headers(),
            timeout=30
        )
        print(f"  Result: {resp.status_code} - {resp.text[:150]}")
    except Exception as e:
        print(f"  Error: {e}")


# =============================================================================
# SECTION 5: Querying Data
# =============================================================================
def demo_query():
    """
    Query imported data using SQL-like syntax.
    Supports SELECT, WHERE, ORDER BY, LIMIT, aggregations.
    """
    print_section("DATA QUERIES - Retrieve and analyze imported data")
    
    queries = [
        ("Select all experiments",
         "SELECT * FROM quantum_experiments"),
        ("Filter by domain (chemistry only)",
         "SELECT * FROM quantum_experiments WHERE domain = 'chemistry'"),
        ("High-fidelity results",
         "SELECT molecule, energy, fidelity FROM quantum_experiments WHERE fidelity > 0.999"),
        ("Order by energy",
         "SELECT domain, molecule, energy FROM quantum_experiments ORDER BY energy"),
        ("Count by domain",
         "SELECT domain, COUNT(*) FROM quantum_experiments GROUP BY domain"),
        ("Molecules with short bonds",
         "SELECT name, formula, bond_length FROM molecules WHERE bond_length < 1.0"),
        ("Sensor temperature readings",
         "SELECT sensor_id, temperature, pressure FROM sensor_readings WHERE temperature > 300"),
    ]
    
    for desc, sql in queries:
        print(f"  {desc}")
        print(f"  SQL: {sql}")
        try:
            resp = requests.post(
                f"{BASE_URL}/query",
                json={"query": sql, "limit": 100, "offset": 0},
                headers=get_headers(),
                timeout=10
            )
            result = resp.json()
            print(f"  Status: {resp.status_code}")
            if "data" in result and "rows" in result.get("data", {}):
                rows = result["data"]["rows"]
                print(f"  Rows returned: {len(rows)}")
                for row in rows[:3]:
                    print(f"    {row}")
                if len(rows) > 3:
                    print(f"    ... ({len(rows) - 3} more)")
            else:
                print(f"  Response: {json.dumps(result)[:200]}")
        except Exception as e:
            print(f"  Error: {e}")
        print()


# =============================================================================
# SECTION 6: Pipeline - Quantum Processing of Imported Data
# =============================================================================
def demo_pipeline_on_data():
    """
    Use the quantum pipeline to process imported molecular data.
    Fetches molecules from the database, then runs VQE on each.
    """
    print_section("PIPELINE - Quantum Processing of Imported Data")
    
    print("  Step 1: Fetch molecules from database")
    molecules = []
    try:
        resp = requests.post(
            f"{BASE_URL}/query",
            json={"query": "SELECT name, formula, bond_length, num_atoms FROM molecules LIMIT 5"},
            headers=get_headers(),
            timeout=10
        )
        result = resp.json()
        if "data" in result and "rows" in result.get("data", {}):
            molecules = result["data"]["rows"]
            print(f"  Found {len(molecules)} molecules")
            for m in molecules:
                print(f"    {m}")
    except Exception as e:
        print(f"  Error fetching: {e}")
        # Use fallback data
        molecules = [
            ["Hydrogen", "H2", 0.74, 2],
            ["Lithium Hydride", "LiH", 1.60, 2],
            ["Water", "H2O", 0.96, 3],
        ]
        print(f"  Using fallback data: {len(molecules)} molecules")
    
    print("\n  Step 2: Run quantum pipeline on each molecule")
    pipeline_url = f"{BASE_URL}/quantum/pipeline/execute"
    
    for mol in molecules[:5]:
        name = mol[0] if isinstance(mol, list) else mol.get("name", "unknown")
        formula = mol[1] if isinstance(mol, list) else mol.get("formula", "H2")
        bond = mol[2] if isinstance(mol, list) else mol.get("bond_length", 0.74)
        atoms = mol[3] if isinstance(mol, list) else mol.get("num_atoms", 2)
        
        # Scale qubits - engine supports full 65536 qubit circuit
        num_qubits = 65536
        
        payload = {
            "domain": "chemistry",
            "num_qubits": num_qubits,
            "molecule": formula,
            "bond_length": float(bond),
            "algorithm": "vqe"
        }
        
        print(f"\n  Processing: {name} ({formula}), {num_qubits} qubits")
        try:
            start = time.time()
            resp = requests.post(
                pipeline_url,
                json=payload,
                headers=get_headers(),
                timeout=60
            )
            elapsed = (time.time() - start) * 1000
            print(f"    Status: {resp.status_code}, Time: {elapsed:.1f}ms")
            if resp.status_code == 200:
                result = resp.json()
                # Store result back
                if "result" in result:
                    energy = result["result"].get("energy", "N/A")
                    fidelity = result["result"].get("fidelity", "N/A")
                    print(f"    Energy: {energy}, Fidelity: {fidelity}")
        except Exception as e:
            print(f"    Error: {e}")
    
    print("\n  Step 3: Store results back to database")
    print("  (Results from pipeline can be inserted back via /api/v1/query)")
    store_sql = "INSERT INTO quantum_experiments VALUES (100, 'pipeline', 'H2', 4, -1.137, 0.9998, 45, '2026-01-15T14:00:00Z')"
    print(f"  Example: {store_sql[:80]}...")


# =============================================================================
# SECTION 7: Update and Delete Operations
# =============================================================================
def demo_update_delete():
    """
    Demonstrate UPDATE and DELETE operations on imported data.
    """
    print_section("UPDATE & DELETE - Modify imported data")
    
    operations = [
        ("Update fidelity for experiment #1",
         "UPDATE quantum_experiments SET fidelity = 0.9999 WHERE id = 1"),
        ("Update iterations for physics experiment",
         "UPDATE quantum_experiments SET iterations = 90 WHERE domain = 'physics'"),
        ("Delete a specific record",
         "DELETE FROM quantum_experiments WHERE id = 5"),
        ("Verify after update",
         "SELECT id, molecule, fidelity, iterations FROM quantum_experiments ORDER BY id"),
    ]
    
    for desc, sql in operations:
        print(f"  {desc}")
        print(f"  SQL: {sql}")
        try:
            resp = requests.post(
                f"{BASE_URL}/query",
                json={"query": sql},
                headers=get_headers(),
                timeout=10
            )
            print(f"  Result: {resp.status_code} - {resp.text[:150]}")
        except Exception as e:
            print(f"  Error: {e}")
        print()


# =============================================================================
# SECTION 8: CSV Import Pattern
# =============================================================================
def demo_csv_import_pattern():
    """
    Shows how to import CSV data in batches (pattern for large files).
    This is a template - modify the CSV path and column mapping for your data.
    """
    print_section("CSV IMPORT PATTERN - Batch import from files")
    
    print("""
  # Python pattern for importing CSV files into nawaz1:
  
  import csv
  
  CSV_FILE = "your_data.csv"
  BATCH_SIZE = 40  # Rows per INSERT (keep under 10000 char SQL limit)
  TABLE = "your_table"
  
  # Read CSV
  with open(CSV_FILE, 'r') as f:
      reader = csv.DictReader(f)
      batch = []
      total = 0
      
      for row in reader:
          # Map CSV columns to SQL values
          values = f"({row['id']}, '{row['name']}', {row['value']})"
          batch.append(values)
          
          if len(batch) >= BATCH_SIZE:
              sql = f"INSERT INTO {TABLE} VALUES " + ",".join(batch)
              resp = requests.post(
                  f"{BASE_URL}/query",
                  json={"query": sql},
                  headers=get_headers(),
                  timeout=30
              )
              total += len(batch)
              batch = []
      
      # Flush remaining
      if batch:
          sql = f"INSERT INTO {TABLE} VALUES " + ",".join(batch)
          requests.post(f"{BASE_URL}/query", json={"query": sql}, headers=get_headers())
          total += len(batch)
      
      print(f"Imported {total} rows")
    """)
    
    # Demonstrate with synthetic data
    print("  Demo: Importing 20 synthetic experiment rows...")
    values = []
    for i in range(20):
        domain = ["chemistry", "physics", "finance", "materials_science"][i % 4]
        energy = -1.0 - (i * 0.5)
        fidelity = 0.999 - (i * 0.0001)
        values.append(f"({i+10}, '{domain}', 'synthetic_{i}', {4+i}, {energy:.3f}, {fidelity:.4f}, {50+i*5}, '2026-01-15T15:{i:02d}:00Z')")
    
    # Split into batches of 10
    for batch_start in range(0, len(values), 10):
        batch = values[batch_start:batch_start+10]
        sql = "INSERT INTO quantum_experiments VALUES " + ",".join(batch)
        print(f"  Batch {batch_start//10 + 1}: {len(batch)} rows")
        try:
            resp = requests.post(
                f"{BASE_URL}/query",
                json={"query": sql},
                headers=get_headers(),
                timeout=30
            )
            print(f"    Status: {resp.status_code}")
        except Exception as e:
            print(f"    Error: {e}")


# =============================================================================
# MAIN
# =============================================================================
SECTIONS = {
    "auth": demo_auth,
    "tables": demo_tables,
    "insert": demo_single_insert,
    "batch": demo_batch_import,
    "query": demo_query,
    "pipeline": demo_pipeline_on_data,
    "update": demo_update_delete,
    "csv": demo_csv_import_pattern,
}

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║      NAWAZ1 QUANTUM ENGINE - Data Import & Management Guide        ║
║      Authentication, Tables, Import, Query, Pipeline               ║
║      Copyright (c) 2026 Shahnawaz Alam                             ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--list":
            print("Available sections:")
            for name in SECTIONS:
                print(f"  - {name}")
            sys.exit(0)
        elif arg in SECTIONS:
            SECTIONS[arg]()
        else:
            print(f"Unknown section: {arg}")
            print(f"Available: {', '.join(SECTIONS.keys())}")
            sys.exit(1)
    else:
        # Run all sections in order
        for name, fn in SECTIONS.items():
            try:
                fn()
            except KeyboardInterrupt:
                print("\n\nInterrupted.")
                sys.exit(0)
            except Exception as e:
                print(f"\n[ERROR in {name}]: {e}")
        
        print("\n" + "="*70)
        print("  DATA IMPORT EXAMPLES COMPLETE")
        print("="*70)
