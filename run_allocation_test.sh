#!/bin/bash
# Run qubit allocation deep analysis

set -e

# Kill any existing servers
pkill -f nawaz1-server 2>/dev/null || true
sleep 2

# Setup
export JWT_SECRET="allocation_test_$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 32 | head -n 1)"
echo "Starting nawaz1-server..."

# Start server
/opt/nawaz1/nawaz1-server &>/tmp/allocation_test.log &
SERVER_PID=$!
echo "Server started (PID: $SERVER_PID)"
sleep 4

# Check server is alive
if curl -s http://localhost:8080/api/v1/health >/dev/null; then
    echo "Server is healthy, running qubit allocation analysis..."
    echo ""
    
    # Run Python analysis
    python3 /mnt/c/Users/IMRAN/.qoder/nawaz1-quantum-software/test_qubit_allocation.py
    
    echo ""
    echo "Analysis complete."
else
    echo "ERROR: Server failed to start"
    cat /tmp/allocation_test.log
fi

# Cleanup
kill $SERVER_PID 2>/dev/null || true
echo "Server stopped."
