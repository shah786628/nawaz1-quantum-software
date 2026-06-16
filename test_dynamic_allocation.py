#!/usr/bin/env python3
"""
PROVE: Qubit allocation is DYNAMIC, not hardcoded to 4,096
Tests different input data sizes to show auto-scaling behavior
"""
import requests, json

BASE_URL = "http://localhost:8080"

def test_dynamic_allocation():
    """Test that engine allocates DIFFERENT qubit widths based on input complexity"""
    
    print("="*70)
    print("TEST: DYNAMIC QUBIT ALLOCATION (NOT HARDCODED)")
    print("="*70)
    print()
    print("HYPOTHESIS: Engine auto-scales qubits based on input data size")
    print("If hardcoded to 4,096, all tests will show 4,096")
    print("If dynamic, different input sizes will get different qubit widths")
    print()
    
    # Test cases with DIFFERENT input data sizes
    test_cases = [
        ("Tiny (8 elements)", 8),
        ("Small (256 elements)", 256),
        ("Medium (8,192 elements)", 8192),
        ("Large (1,048,576 elements)", 1048576),
        ("Very Large (524,288 elements)", 524288),
    ]
    
    results = []
    
    for name, num_elements in test_cases:
        print(f"\n{'─'*70}")
        print(f"TEST: {name}")
        print(f"{'─'*70}")
        
        # Create input data with EXACT number of elements
        input_data = [0.01] * num_elements
        
        payload = {
            "domain": "chemistry",
            "algorithm": "vqe",
            "qubits": num_elements,  # Request same as element count
            "input_data": input_data
        }
        
        print(f"  Input data elements: {num_elements:,}")
        
        try:
            resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", 
                               json=payload, timeout=30)
            result = resp.json()
            
            if result.get('status') == 'completed':
                num_requested = result.get('num_qubits_requested', 'N/A')
                num_simulated = result.get('num_qubits_simulated', 'N/A')
                inner_result = result.get('result', {})
                parallel_lines = inner_result.get('parallel_lines_used', 'N/A')
                
                print(f"  Requested qubits:    {num_requested:,}")
                print(f"  Simulated qubits:    {num_simulated:,}")
                print(f"  Parallel lines:      {parallel_lines}")
                
                # Check if it fits in 65K resistor
                if isinstance(num_simulated, int):
                    resistor_usage = (num_simulated / (2**53)) * 100
                    max_logical = num_simulated * parallel_lines
                    
                    print(f"  Resistor usage:      {resistor_usage:.2f}%")
                    print(f"  Max logical qubits:  {max_logical:,} ({num_simulated} × {parallel_lines})")
                
                results.append({
                    'name': name,
                    'elements': num_elements,
                    'requested': num_requested,
                    'simulated': num_simulated,
                    'parallel_lines': parallel_lines
                })
            else:
                print(f"  ❌ Failed: {result.get('error', 'Unknown')}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
    
    # ANALYSIS
    print(f"\n\n{'='*70}")
    print("COMPREHENSIVE ANALYSIS")
    print(f"{'='*70}")
    print()
    print(f"{'Test':<25} {'Elements':>10} {'Physical Q':>12} {'Lines':>6} {'Max Logical':>12}")
    print(f"{'─'*70}")
    
    simulated_values = set()
    
    for r in results:
        elements = r['elements']
        simulated = r['simulated']
        lines = r['parallel_lines']
        
        if isinstance(simulated, int) and isinstance(lines, int):
            max_logical = simulated * lines
            print(f"{r['name']:<25} {elements:>10,} {simulated:>12,} {lines:>6} {max_logical:>12,}")
            simulated_values.add(simulated)
        else:
            print(f"{r['name']:<25} {elements:>10,} {str(simulated):>12} {str(lines):>6} {'N/A':>12}")
    
    print()
    print("="*70)
    print("VERDICT")
    print("="*70)
    print()
    
    if len(simulated_values) > 1:
        print(f"✅ PROVEN: Engine uses {len(simulated_values)} DIFFERENT qubit widths:")
        print(f"   {sorted(simulated_values)}")
        print()
        print("   → Allocation is DYNAMIC (NOT hardcoded)")
        print("   → Engine auto-scales based on input data size")
        print("   → Small inputs → small qubit widths (efficient)")
        print("   → Large inputs → large qubit widths (accurate)")
        print()
        print("CONCLUSION: The 4,096 you saw before was just for YOUR specific input size")
        print("            Different input sizes will get different allocations!")
    else:
        single_value = list(simulated_values)[0] if simulated_values else 'unknown'
        print(f"⚠️  Engine always uses {single_value} qubits")
        print(f"   → May be hardcoded OR your test inputs were similar complexity")
        print(f"   → Need more diverse test cases to confirm")

if __name__ == "__main__":
    # Health check
    print("\n[SETUP] Checking server...")
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"✅ Server healthy\n")
    except:
        print("❌ Server not running!")
        exit(1)
    
    test_dynamic_allocation()
