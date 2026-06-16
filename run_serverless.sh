#!/bin/bash
# Nawaz1 Quantum Engine — Serverless Mode Runner
# Executes a single quantum computation from a JSON file and exits.
# No server, no auth, no network listeners — just compute and output.
#
# Usage:
#   ./run_serverless.sh examples/serverless_protein.txt
#   cat examples/serverless_protein.txt | ./run_serverless.sh
#   echo '{"num_qubits":1000000,"domain":"chemistry","algorithm":"vqe","problem":{"orbital_energies":[-0.345,-0.289]}}' | ./run_serverless.sh

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

export JWT_SECRET="serverless-no-auth-required-minimum-32chars"
export RUST_LOG=warn
export NAWAZ1_MODE=serverless

if [ $# -ge 1 ] && [ -f "$1" ]; then
    # Input from file
    export NAWAZ1_INPUT_FILE="$1"
    "$BINARY"
else
    # Input from stdin
    "$BINARY"
fi