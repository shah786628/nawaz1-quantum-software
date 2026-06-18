# Quick Setup Guide - Telemetry & Kill-Switch System

## Repository Configuration

### Your Existing Repositories

**Public Repository** (binary distribution ONLY):
- `shah786628/nawaz1-quantum-software`
- Contains: Linux binaries (x86_64, ARM64)
- NO telemetry or security data

**Private Repository** (RE security & telemetry):
- Your existing private "shah" repository
- Contains: Telemetry logs, kill-switch data, RE attack forensics
- Only you can access this

## Environment Setup

### 1. Set GitHub PAT Token

```bash
# Create GitHub PAT with repo access
# https://github.com/settings/tokens

export GITHUB_TELEMETRY_TOKEN="ghp_your_token_here"
```

### 2. Configure Private Repository (Optional)

The system defaults to using `shah786628/shah` as your private repo. To customize:

```bash
export TELEMETRY_REPO_OWNER="shah786628"
export TELEMETRY_REPO_NAME="shah"
export TELEMETRY_REPO_BRANCH="main"
```

### 3. Add to Your Shell Profile

For permanent configuration, add to `~/.bashrc` or `~/.zshrc`:

```bash
# Nawaz1 Telemetry Configuration
export GITHUB_TELEMETRY_TOKEN="ghp_your_token_here"
export TELEMETRY_REPO_OWNER="shah786628"
export TELEMETRY_REPO_NAME="shah"
export TELEMETRY_REPO_BRANCH="main"
```

## Private Repository Setup

Create the telemetry directory structure in your private "shah" repo:

```bash
# Clone your private repo
git clone git@github.com:shah786628/shah.git
cd shah

# Create telemetry directory structure
mkdir -p telemetry/analytics
mkdir -p kill_switch

# Initialize empty files
echo '{"machines":[],"total_machines":0}' > telemetry/machines.json
echo '{"incidents":[],"total_incidents":0}' > telemetry/auto_kill_incidents.json
echo '{"revoked_tags":[],"total_revoked":0}' > kill_switch/revoked_tags.json
echo 'INACTIVE' > kill_switch/global_kill.txt

# Commit and push
git add .
git commit -m "Initialize telemetry structure"
git push origin main
```

## Testing

### Test Dashboard Connection

```bash
# Test dashboard can access your private repo
python3 telemetry_dashboard.py --check-global

# Expected output: "Global kill-switch is INACTIVE"
```

### Test with New Binary

Once you build the new binary:

```bash
# Run binary (will generate machine tag)
./nawaz1-server

# Check if machine registered
python3 telemetry_dashboard.py --list-machines
```

## Build Instructions

### Build New Binaries with Telemetry

```bash
cd nawaz1_dev

# Set environment for build
export GITHUB_TELEMETRY_TOKEN="ghp_your_token_here"
export TELEMETRY_REPO_OWNER="shah786628"
export TELEMETRY_REPO_NAME="shah"

# Build x86_64 Linux binary
cargo build --release --target x86_64-unknown-linux-gnu

# Build ARM64 Linux binary (requires cross-compilation setup)
cargo build --release --target aarch64-unknown-linux-gnu

# Copy to bin directory
mkdir -p ../nawaz1-quantum-software/bin/x86_64
mkdir -p ../nawaz1-quantum-software/bin/arm64

cp target/x86_64-unknown-linux-gnu/release/nawaz1-server \
   ../nawaz1-quantum-software/bin/x86_64/

cp target/aarch64-unknown-linux-gnu/release/nawaz1-server \
   ../nawaz1-quantum-software/bin/arm64/
```

### Update Public GitHub Release

```bash
cd nawaz1-quantum-software

# Remove old v2.1.0 release (RE security weak)
gh release delete v2.1.0 --yes

# Create new v2.2.0 release
gh release create v2.2.0 \
  --title "Nawaz1 Quantum Software v2.2.0" \
  --notes "Added telemetry & 3-tier kill-switch system" \
  bin/x86_64/nawaz1-server \
  bin/arm64/nawaz1-server

# Commit binaries to repo
git add bin/
git commit -m "Add v2.2.0 binaries with telemetry"
git push origin main
```

## Dashboard Usage Examples

```bash
# List all registered machines
python3 telemetry_dashboard.py --list-machines

# Review auto-kill incidents
python3 telemetry_dashboard.py --review-incidents

# Revoke specific machine (reversible)
python3 telemetry_dashboard.py --revoke-tag a3f5e9b2... --reason "Suspicious activity"

# Un-revoke machine (restore access)
python3 telemetry_dashboard.py --unrevoke-tag 9a2b2dda... --reason "Testing complete"

# Show analytics
python3 telemetry_dashboard.py --analytics

# Activate global kill-switch (PERMANENT - use with caution!)
python3 telemetry_dashboard.py --global-kill --reason "Source code compromised"
```

## Troubleshooting

### Issue: "Repository not found"

**Solution:** Ensure your PAT token has access to the private "shah" repo:
- Token needs `repo` scope (full control of private repositories)
- Regenerate token if needed

### Issue: "403 Forbidden"

**Solution:** Check repository permissions:
- You must be the owner or have admin access
- Verify repo name is correct (case-sensitive)

### Issue: Binary still shows revoked tag

**Solution:** Your machine tag `9a2b2dda...` is per-tag revoked. Options:
1. Un-revoke the tag: `python3 telemetry_dashboard.py --unrevoke-tag 9a2b2dda...`
2. Build new binary (will generate new tag)

## Security Notes

✅ **Private repo** contains ALL sensitive telemetry data  
✅ **Public repo** contains ONLY binaries (no telemetry)  
✅ **Environment variables** keep repo configuration flexible  
✅ **GitHub PAT** required for all telemetry operations  
✅ **Owner-only access** to kill-switch controls  

## Support

- Owner: Shahnawaz Alam
- Email: shahnawaz512001@gmail.com
- GitHub: https://github.com/shah786628
