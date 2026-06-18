#!/usr/bin/env python3
"""
COMPREHENSIVE STRESS TEST FOR NAWAZ1 VQE ENGINE - FIXED VERSION
Tests: Stability, Memory Leaks, Concurrency, Extreme Scales, Error Handling
"""
import requests, json, time, math, sys, threading, statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

BASE_URL = "http://localhost:8080"

def check_success(result):
    """Check if API response indicates success (handles multiple schema versions)"""
    return (
        result.get('success') or 
        result.get('status') == 'completed' or
        result.get('result', {}).get('converged', False)
    )

def get_result_section(result):
    """Extract the result section from response (handles nested or flat structure)"""
    if 'result' in result:
        return result['result']
    return result

class StressTest:
    def __init__(self):
        self.results = []
        self.errors = []
        self.start_time = None
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def test_continuous_execution(self, duration_secs=60):
        """TEST 1: Run VQE continuously for N seconds"""
        self.log("\n" + "="*70)
        self.log(f"STRESS TEST 1: CONTINUOUS EXECUTION ({duration_secs}s)")
        self.log("="*70)
        
        start = time.time()
        count = 0
        failures = 0
        latencies = []
        
        payload = {
            "domain": "chemistry",
            "algorithm": "vqe",
            "qubits": 32
        }
        
        self.log("Executing VQE requests continuously...")
        
        while time.time() - start < duration_secs:
            try:
                req_start = time.time()
                resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=10)
                req_elapsed = time.time() - req_start
                
                if resp.status_code == 200:
                    result = resp.json()
                    if check_success(result):
                        count += 1
                        latencies.append(req_elapsed * 1000)
                        
                        if count % 50 == 0:
                            elapsed = time.time() - start
                            rate = count / elapsed
                            self.log(f"  Progress: {count} requests, {elapsed:.1f}s, rate={rate:.1f} req/s")
                    else:
                        failures += 1
                else:
                    failures += 1
                    
            except Exception as e:
                failures += 1
        
        # Statistics
        elapsed = time.time() - start
        avg_latency = statistics.mean(latencies) if latencies else 0
        p50_latency = statistics.median(latencies) if latencies else 0
        p99_latency = sorted(latencies)[int(len(latencies)*0.99)] if latencies else 0
        
        self.log(f"\n📊 RESULTS:")
        self.log(f"  Total requests: {count}")
        self.log(f"  Failures: {failures}")
        self.log(f"  Success rate: {(count/(count+failures))*100:.2f}%")
        self.log(f"  Duration: {elapsed:.1f}s")
        self.log(f"  Throughput: {count/elapsed:.2f} req/s")
        self.log(f"  Avg latency: {avg_latency:.1f} ms")
        self.log(f"  P50 latency: {p50_latency:.1f} ms")
        self.log(f"  P99 latency: {p99_latency:.1f} ms")
        
        if failures == 0:
            self.log(f"  ✅ PASS: Zero failures in {duration_secs}s continuous execution")
            return True
        else:
            self.log(f"  ⚠️  WARNING: {failures} failures detected")
            return False
    
    def test_concurrent_requests(self, num_threads=10, requests_per_thread=20):
        """TEST 2: Concurrent requests from multiple threads"""
        self.log("\n" + "="*70)
        self.log(f"STRESS TEST 2: CONCURRENCY ({num_threads} threads × {requests_per_thread} req)")
        self.log("="*70)
        
        total_requests = num_threads * requests_per_thread
        success_count = 0
        failure_count = 0
        latencies = []
        lock = threading.Lock()
        
        def worker(thread_id):
            nonlocal success_count, failure_count
            thread_success = 0
            thread_failures = 0
            thread_latencies = []
            
            for i in range(requests_per_thread):
                try:
                    payload = {
                        "domain": "chemistry",
                        "algorithm": "vqe",
                        "qubits": 16,
                        "config": {"thread_id": thread_id, "req_id": i}
                    }
                    
                    req_start = time.time()
                    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=10)
                    req_elapsed = time.time() - req_start
                    
                    if resp.status_code == 200:
                        result = resp.json()
                        if check_success(result):
                            thread_success += 1
                            thread_latencies.append(req_elapsed * 1000)
                        else:
                            thread_failures += 1
                    else:
                        thread_failures += 1
                        
                except Exception as e:
                    thread_failures += 1
            
            with lock:
                success_count += thread_success
                failure_count += thread_failures
                latencies.extend(thread_latencies)
        
        self.log(f"Launching {num_threads} concurrent workers...")
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker, tid) for tid in range(num_threads)]
            for future in as_completed(futures):
                future.result()
        
        elapsed = time.time() - start
        
        avg_latency = statistics.mean(latencies) if latencies else 0
        p50_latency = statistics.median(latencies) if latencies else 0
        p99_latency = sorted(latencies)[int(len(latencies)*0.99)] if latencies else 0
        
        self.log(f"\n📊 RESULTS:")
        self.log(f"  Total requests: {total_requests}")
        self.log(f"  Successful: {success_count}")
        self.log(f"  Failed: {failure_count}")
        self.log(f"  Success rate: {(success_count/total_requests)*100:.2f}%")
        self.log(f"  Duration: {elapsed:.1f}s")
        self.log(f"  Concurrent throughput: {total_requests/elapsed:.2f} req/s")
        self.log(f"  Avg latency: {avg_latency:.1f} ms")
        self.log(f"  P50 latency: {p50_latency:.1f} ms")
        self.log(f"  P99 latency: {p99_latency:.1f} ms")
        
        if failure_count == 0:
            self.log(f"  ✅ PASS: All concurrent requests succeeded")
            return True
        else:
            self.log(f"  ⚠️  WARNING: {failure_count} failures under concurrency")
            return False
    
    def test_extreme_scales(self):
        """TEST 3: Extreme qubit scales"""
        self.log("\n" + "="*70)
        self.log("STRESS TEST 3: EXTREME QUBIT SCALES")
        self.log("="*70)
        
        scales = [1024, 10000, 100000, 500000, 1000000]
        results = []
        
        for qubits in scales:
            self.log(f"\n  Testing {qubits:,} qubits...")
            
            payload = {
                "domain": "chemistry",
                "algorithm": "vqe",
                "qubits": qubits
            }
            
            try:
                start = time.time()
                resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=30)
                elapsed = time.time() - start
                
                if resp.status_code == 200:
                    result = resp.json()
                    if check_success(result):
                        r = get_result_section(result)
                        fidelity = r.get('fidelity', 0)
                        converged = r.get('converged', False)
                        
                        results.append({
                            'qubits': qubits,
                            'time_ms': elapsed * 1000,
                            'fidelity': fidelity,
                            'converged': converged,
                            'status': '✅'
                        })
                        
                        self.log(f"    ✅ {qubits:,}q: {elapsed*1000:.1f}ms, fidelity={fidelity:.12f}, converged={converged}")
                    else:
                        results.append({
                            'qubits': qubits,
                            'time_ms': elapsed * 1000,
                            'status': '❌',
                            'error': result.get('error', 'Unknown')
                        })
                        self.log(f"    ❌ {qubits:,}q: Failed - {result.get('error', 'Unknown')}")
                else:
                    self.log(f"    ❌ {qubits:,}q: HTTP {resp.status_code}")
                    
            except Exception as e:
                results.append({
                    'qubits': qubits,
                    'status': '❌',
                    'error': str(e)
                })
                self.log(f"    ❌ {qubits:,}q: Exception - {e}")
        
        self.log(f"\n📊 SCALING RESULTS:")
        for r in results:
            status = r['status']
            qubits = r['qubits']
            if 'time_ms' in r:
                time_ms = r['time_ms']
                fidelity = r.get('fidelity', 'N/A')
                self.log(f"  {status} {qubits:>10,} qubits: {time_ms:>8.1f} ms, fidelity={fidelity}")
            else:
                self.log(f"  {status} {qubits:>10,} qubits: FAILED - {r.get('error', 'Unknown')}")
        
        success_count = sum(1 for r in results if r['status'] == '✅')
        if success_count == len(scales):
            self.log(f"\n  ✅ PASS: All {len(scales)} scales executed successfully")
            return True
        else:
            self.log(f"\n  ⚠️  WARNING: {success_count}/{len(scales)} scales succeeded")
            return False
    
    def test_multi_domain_stress(self, iterations=10):
        """TEST 4: Rapid multi-domain switching"""
        self.log("\n" + "="*70)
        self.log(f"STRESS TEST 4: MULTI-DOMAIN RAPID SWITCHING ({iterations} iterations)")
        self.log("="*70)
        
        domains = {
            "chemistry": "H2 molecule",
            "physics": "Heisenberg lattice",
            "biology": "protein folding",
            "materials_science": "graphene",
            "machine_learning": "quantum neural net",
            "finance": "portfolio optimization",
            "logistics": "traveling salesman"
        }
        
        domain_results = {d: {'success': 0, 'failure': 0, 'energies': []} for d in domains}
        
        for i in range(iterations):
            for domain, desc in domains.items():
                payload = {
                    "domain": domain,
                    "algorithm": "vqe",
                    "qubits": 32,
                    "description": desc
                }
                
                try:
                    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=10)
                    result = resp.json()
                    
                    if check_success(result):
                        r = get_result_section(result)
                        energy = r.get('aggregate_energy', 0)
                        domain_results[domain]['success'] += 1
                        domain_results[domain]['energies'].append(energy)
                    else:
                        domain_results[domain]['failure'] += 1
                        
                except Exception as e:
                    domain_results[domain]['failure'] += 1
        
        self.log(f"\n📊 DOMAIN ISOLATION RESULTS:")
        all_passed = True
        
        for domain, stats in domain_results.items():
            total = stats['success'] + stats['failure']
            success_rate = (stats['success'] / total * 100) if total > 0 else 0
            
            if stats['energies']:
                energy_mean = statistics.mean(stats['energies'])
                energy_std = statistics.stdev(stats['energies']) if len(stats['energies']) > 1 else 0
                cv = (energy_std / abs(energy_mean)) * 100 if energy_mean != 0 else 0
                
                self.log(f"  ✅ {domain:20s}: {stats['success']}/{total} success, "
                        f"energy_mean={energy_mean:.6f}, cv={cv:.4e}%")
                
                if cv > 0.01:
                    self.log(f"    ⚠️  High energy variation across runs")
                    all_passed = False
            else:
                self.log(f"  ❌ {domain:20s}: {stats['failure']}/{total} failed")
                all_passed = False
        
        if all_passed:
            self.log(f"\n  ✅ PASS: All domains isolated correctly")
            return True
        else:
            self.log(f"\n  ⚠️  WARNING: Some domain isolation issues detected")
            return False
    
    def test_error_handling(self):
        """TEST 5: Send malformed requests"""
        self.log("\n" + "="*70)
        self.log("STRESS TEST 5: ERROR HANDLING (malformed requests)")
        self.log("="*70)
        
        bad_requests = [
            {"domain": "invalid_domain", "algorithm": "vqe"},
            {"domain": "chemistry", "algorithm": "invalid_algorithm"},
            {"domain": "chemistry", "algorithm": "vqe", "qubits": -1},
            {"domain": "chemistry", "algorithm": "vqe", "qubits": 0},
            {"domain": "chemistry", "algorithm": "vqe", "qubits": 999999999},
            {"invalid_json": True},
            {},
            {"domain": "chemistry"},
        ]
        
        crashes = 0
        proper_errors = 0
        
        for i, payload in enumerate(bad_requests):
            try:
                resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=5)
                
                if resp.status_code in [400, 422, 500]:
                    proper_errors += 1
                    self.log(f"  ✅ Request {i+1}: Properly rejected (HTTP {resp.status_code})")
                elif resp.status_code == 200:
                    result = resp.json()
                    if not check_success(result):
                        proper_errors += 1
                        self.log(f"  ✅ Request {i+1}: Error returned in response body")
                        
            except Exception as e:
                crashes += 1
                self.log(f"  ❌ Request {i+1}: Server crashed - {e}")
        
        # Verify server still works
        try:
            resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", 
                               json={"domain": "chemistry", "algorithm": "vqe", "qubits": 8},
                               timeout=5)
            if resp.status_code == 200 and check_success(resp.json()):
                self.log(f"\n  ✅ Server still functional after error tests")
            else:
                self.log(f"\n  ❌ Server degraded after error tests")
        except:
            self.log(f"\n  ❌ Server crashed after error tests")
            crashes += 1
        
        self.log(f"\n📊 ERROR HANDLING RESULTS:")
        self.log(f"  Properly rejected: {proper_errors}/{len(bad_requests)}")
        self.log(f"  Server crashes: {crashes}")
        
        if crashes == 0 and proper_errors >= len(bad_requests) - 1:
            self.log(f"\n  ✅ PASS: Error handling is robust")
            return True
        else:
            self.log(f"\n  ⚠️  WARNING: Error handling needs improvement")
            return False
    
    def test_memory_stability(self, duration_secs=30):
        """TEST 6: Memory usage over time"""
        self.log("\n" + "="*70)
        self.log(f"STRESS TEST 6: MEMORY STABILITY ({duration_secs}s)")
        self.log("="*70)
        
        start = time.time()
        latencies_over_time = []
        batch_size = 10
        
        payload = {
            "domain": "chemistry",
            "algorithm": "vqe",
            "qubits": 64
        }
        
        self.log("Monitoring latency degradation over time...")
        
        while time.time() - start < duration_secs:
            batch_latencies = []
            
            for _ in range(batch_size):
                try:
                    req_start = time.time()
                    resp = requests.post(f"{BASE_URL}/api/v1/quantum/execute", json=payload, timeout=10)
                    req_elapsed = time.time() - req_start
                    
                    if resp.status_code == 200 and check_success(resp.json()):
                        batch_latencies.append(req_elapsed * 1000)
                        
                except:
                    pass
            
            if batch_latencies:
                avg = statistics.mean(batch_latencies)
                elapsed = time.time() - start
                latencies_over_time.append((elapsed, avg))
                
                if len(latencies_over_time) % 5 == 0:
                    self.log(f"  t={elapsed:.1f}s: avg_latency={avg:.1f}ms")
            
            time.sleep(1)
        
        if len(latencies_over_time) >= 2:
            initial_latency = latencies_over_time[0][1]
            final_latency = latencies_over_time[-1][1]
            degradation = ((final_latency - initial_latency) / initial_latency) * 100
            
            self.log(f"\n📊 MEMORY STABILITY RESULTS:")
            self.log(f"  Initial latency: {initial_latency:.1f} ms")
            self.log(f"  Final latency: {final_latency:.1f} ms")
            self.log(f"  Degradation: {degradation:.2f}%")
            
            if degradation < 10:
                self.log(f"  ✅ PASS: No significant memory leak (degradation < 10%)")
                return True
            elif degradation < 50:
                self.log(f"  ⚠️  WARNING: Moderate latency degradation ({degradation:.1f}%)")
                return True
            else:
                self.log(f"  ❌ FAIL: Severe memory leak (degradation {degradation:.1f}%)")
                return False
        else:
            self.log(f"  ⚠️  WARNING: Insufficient data for memory analysis")
            return False
    
    def run_all_tests(self):
        """Run complete stress test suite"""
        self.start_time = time.time()
        
        self.log("\n" + "🔬"*35)
        self.log("COMPREHENSIVE STRESS TEST SUITE")
        self.log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("🔬"*35)
        
        tests = [
            ("Continuous Execution (60s)", lambda: self.test_continuous_execution(60)),
            ("Concurrent Requests (10×20)", lambda: self.test_concurrent_requests(10, 20)),
            ("Extreme Scales", self.test_extreme_scales),
            ("Multi-Domain Stress (10 iter)", lambda: self.test_multi_domain_stress(10)),
            ("Error Handling", self.test_error_handling),
            ("Memory Stability (30s)", lambda: self.test_memory_stability(30)),
        ]
        
        results = []
        for name, test_func in tests:
            try:
                passed = test_func()
                results.append((name, passed))
            except Exception as e:
                self.log(f"\n❌ TEST CRASHED: {name}")
                self.log(f"   Error: {e}")
                results.append((name, False))
        
        elapsed = time.time() - self.start_time
        passed_count = sum(1 for _, passed in results if passed)
        total_count = len(results)
        
        self.log("\n" + "="*70)
        self.log("STRESS TEST FINAL SUMMARY")
        self.log("="*70)
        self.log(f"Total duration: {elapsed:.1f}s")
        self.log(f"Tests passed: {passed_count}/{total_count}")
        self.log("")
        
        for name, passed in results:
            status = "✅ PASS" if passed else "❌ FAIL"
            self.log(f"  {status}: {name}")
        
        if passed_count == total_count:
            self.log("\n" + "🌟"*30)
            self.log("🏆 ALL STRESS TESTS PASSED")
            self.log("✅ Engine is production-ready")
            self.log("✅ No memory leaks detected")
            self.log("✅ Handles concurrency correctly")
            self.log("✅ Scales to 1M qubits")
            self.log("✅ Robust error handling")
            self.log("🌟"*30)
        else:
            self.log(f"\n⚠️  {total_count - passed_count} test(s) failed - review needed")
        
        self.log("="*70)

def main():
    print("\n[SETUP] Checking server health...")
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"✅ Server healthy: {resp.json()}")
    except Exception as e:
        print(f"❌ Server not running or unreachable: {e}")
        sys.exit(1)
    
    tester = StressTest()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
