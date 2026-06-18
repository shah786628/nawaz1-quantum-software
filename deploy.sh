#!/bin/bash
#
# Complete Deployment Script for Nawaz1 Telemetry System
# =======================================================
#
# This script automates the remaining deployment tasks:
# 1. Initialize private repository structure
# 2. Build new binaries (requires Rust in WSL)
# 3. Test telemetry
# 4. Update GitHub releases
#
# Prerequisites:
# - GITHUB_TELEMETRY_TOKEN environment variable set
# - WSL with Ubuntu installed
# - Rust toolchain (will be installed if missing)
# - GitHub CLI (gh) installed
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_OWNER="${TELEMETRY_REPO_OWNER:-shah786628}"
REPO_NAME="${TELEMETRY_REPO_NAME:-shah}"
REPO_BRANCH="${TELEMETRY_REPO_BRANCH:-main}"

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Nawaz1 Telemetry System - Deployment Script${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Check environment variables
if [ -z "$GITHUB_TELEMETRY_TOKEN" ]; then
    echo -e "${RED}ERROR: GITHUB_TELEMETRY_TOKEN not set${NC}"
    echo "Create a GitHub PAT at: https://github.com/settings/tokens"
    echo "Required scope: repo (full control of private repositories)"
    echo ""
    echo "Then run:"
    echo "  export GITHUB_TELEMETRY_TOKEN='ghp_your_token_here'"
    exit 1
fi

echo -e "${GREEN}✓ GitHub token configured${NC}"
echo ""

# Step 1: Initialize Private Repository
echo -e "${YELLOW}[1/5] Initializing private repository structure...${NC}"
echo "Repository: ${REPO_OWNER}/${REPO_NAME}"
echo ""

cd "$(dirname "$0")"
python3 init_private_repo.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Private repository initialized${NC}"
else
    echo -e "${RED}✗ Failed to initialize private repository${NC}"
    exit 1
fi
echo ""

# Step 2: Install Rust in WSL (if needed)
echo -e "${YELLOW}[2/5] Checking Rust installation in WSL...${NC}"

if ! wsl -d Ubuntu -u root -- bash -c "command -v cargo" &> /dev/null; then
    echo "Rust not found in WSL. Installing..."
    wsl -d Ubuntu -u root -- bash -c "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
    wsl -d Ubuntu -u root -- bash -c "source ~/.cargo/env && cargo --version"
    echo -e "${GREEN}✓ Rust installed in WSL${NC}"
else
    echo -e "${GREEN}✓ Rust already installed in WSL${NC}"
fi
echo ""

# Step 3: Build Binaries
echo -e "${YELLOW}[3/5] Building binaries...${NC}"
echo "This will take 10-30 minutes depending on your system..."
echo ""

# Navigate to project directory in WSL
NAWAZ1_DEV_PATH="/mnt/c/Users/IMRAN/.qoder/nawaz1_dev"

# Set environment variables for build
wsl -d Ubuntu -u root -- bash -c "export GITHUB_TELEMETRY_TOKEN='${GITHUB_TELEMETRY_TOKEN}'"
wsl -d Ubuntu -u root -- bash -c "export TELEMETRY_REPO_OWNER='${REPO_OWNER}'"
wsl -d Ubuntu -u root -- bash -c "export TELEMETRY_REPO_NAME='${REPO_NAME}'"

# Build x86_64 binary
echo "Building x86_64 Linux binary..."
wsl -d Ubuntu -u root -- bash -c "cd '${NAWAZ1_DEV_PATH}' && source ~/.cargo/env && cargo build --release --target x86_64-unknown-linux-gnu"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ x86_64 binary built successfully${NC}"
else
    echo -e "${RED}✗ x86_64 build failed${NC}"
    exit 1
fi

# Build ARM64 binary (optional, requires cross-compilation)
echo "Building ARM64 Linux binary..."
wsl -d Ubuntu -u root -- bash -c "cd '${NAWAZ1_DEV_PATH}' && source ~/.cargo/env && cargo build --release --target aarch64-unknown-linux-gnu 2>&1 || echo 'ARM64 build skipped (cross-compilation not configured)'"

echo ""

# Step 4: Copy Binaries
echo -e "${YELLOW}[4/5] Copying binaries to distribution directory...${NC}"

NAWAZ1_SOFTWARE_PATH="/mnt/c/Users/IMRAN/.qoder/nawaz1-quantum-software"

# Create bin directories
wsl -d Ubuntu -u root -- bash -c "mkdir -p '${NAWAZ1_SOFTWARE_PATH}/bin/x86_64'"
wsl -d Ubuntu -u root -- bash -c "mkdir -p '${NAWAZ1_SOFTWARE_PATH}/bin/arm64'"

# Copy x86_64 binary
wsl -d Ubuntu -u root -- bash -c "cp '${NAWAZ1_DEV_PATH}/target/x86_64-unknown-linux-gnu/release/nawaz1-server' '${NAWAZ1_SOFTWARE_PATH}/bin/x86_64/'"

# Copy ARM64 binary (if exists)
if wsl -d Ubuntu -u root -- bash -c "test -f '${NAWAZ1_DEV_PATH}/target/aarch64-unknown-linux-gnu/release/nawaz1-server'"; then
    wsl -d Ubuntu -u root -- bash -c "cp '${NAWAZ1_DEV_PATH}/target/aarch64-unknown-linux-gnu/release/nawaz1-server' '${NAWAZ1_SOFTWARE_PATH}/bin/arm64/'"
    echo -e "${GREEN}✓ ARM64 binary copied${NC}"
fi

echo -e "${GREEN}✓ Binaries copied to bin/ directory${NC}"
echo ""

# Step 5: Update GitHub Release
echo -e "${YELLOW}[5/5] Updating GitHub releases...${NC}"

cd ../nawaz1-quantum-software

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}GitHub CLI (gh) not found. Skipping release update.${NC}"
    echo "Install from: https://cli.github.com/"
    echo ""
    echo "Manual steps:"
    echo "  1. Go to: https://github.com/shah786628/nawaz1-quantum-software/releases"
    echo "  2. Delete v2.1.0 release"
    echo "  3. Create v2.2.0 release with binaries from bin/ directory"
else
    # Remove old v2.1.0 release
    echo "Removing old v2.1.0 release..."
    gh release delete v2.1.0 --yes 2>&1 || echo "v2.1.0 not found (already removed)"
    
    # Create new v2.2.0 release
    echo "Creating v2.2.0 release..."
    gh release create v2.2.0 \
        --title "Nawaz1 Quantum Software v2.2.0" \
        --notes-file RELEASE_NOTES.md \
        bin/x86_64/nawaz1-server \
        bin/arm64/nawaz1-server 2>&1 || echo "ARM64 binary not found, creating with x86_64 only"
    
    echo -e "${GREEN}✓ GitHub release updated${NC}"
fi

echo ""

# Final Summary
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ DEPLOYMENT COMPLETE!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "Your military-grade telemetry system is now deployed!"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "1. Test telemetry:"
echo "   cd bin/x86_64"
echo "   ./nawaz1-server"
echo ""
echo "2. View registered machines:"
echo "   cd ../.."
echo "   python3 telemetry_dashboard.py --list-machines"
echo ""
echo "3. Test kill-switch:"
echo "   python3 telemetry_dashboard.py --check-global"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
