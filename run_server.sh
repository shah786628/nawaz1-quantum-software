#!/bin/bash
# Nawaz1 Quantum Engine — Server Mode Runner
# Starts the REST/gRPC/WebSocket server for API-based quantum computation.
#
# Usage:
#   ./run_server.sh                     # Default: localhost:8080
#   NAWAZ1_PORT=3000 ./run_server.sh    # Custom port
#   NAWAZ1_ENV=production ./run_server.sh  # Production mode (requires TLS)

set -euo pipefail

BINARY="$(dirname "$0")/bin/x86_64/nawaz1-server"

# ARM64 detection
if [ "$(uname -m)" = "aarch64" ]; then
    BINARY="$(dirname "$0")/bin/arm64/nawaz1-server"
fi

if [ ! -f "$BINARY" ]; then
    echo "ERROR: Binary not found at $BINARY" >&2
    echo "Download from https://github.com/shah786628/nawaz1-quantum-software" >&2
    exit 1
fi

# Required: JWT secret for authentication (minimum 32 characters)
export JWT_SECRET="${JWT_SECRET:-$(openssl rand -hex 32 2>/dev/null || echo 'default-dev-secret-change-in-production-32ch')}"
export RUST_LOG="${RUST_LOG:-info}"
export NAWAZ1_MODE="${NAWAZ1_MODE:-server}"

echo "Starting Nawaz1 Quantum Engine (server mode)..."
echo "  Binary:  $BINARY"
echo "  Port:    ${NAWAZ1_PORT:-8080}"
echo "  Mode:    server"
echo ""

exec "$BINARY"