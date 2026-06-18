#!/bin/bash
# Run comprehensive stress test

set -e

# Kill any existing servers
pkill -f nawaz1-server 2>/dev/null || true
sleep 2

# Setup
export JWT_SECRET="stress_test_$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 32 | head -n 1)"
echo "Starting nawaz1-server for stress testing..."

# Start server
/opt/nawaz1/nawaz1-server &>/tmp/stress_test.log &
SERVER_PID=$!
echo "Server started (PID: $SERVER_PID)"
sleep 4

# Check server is alive
if curl -s http://localhost:8080/api/v1/health >/dev/null; then
    echo "Server is healthy, starting stress test suite..."
    echo ""
    
    # Run Python stress test
    python3 /mnt/c/Users/IMRAN/.qoder/nawaz1-quantum-software/stress_test_v2.py
    
    echo ""
    echo "Stress test complete."
else
    echo "ERROR: Server failed to start"
    cat /tmp/stress_test.log
fi

# Cleanup
kill $SERVER_PID 2>/dev/null || true
echo "Server stopped."
