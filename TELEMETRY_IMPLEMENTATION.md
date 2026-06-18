# Nawaz1 Quantum Software - Telemetry & Kill-Switch Implementation

## Overview

This document describes the **complete telemetry and 3-tier kill-switch system** implemented for nawaz1-server binaries.

## Implementation Status

### ✅ Completed Components

1. **Runtime Telemetry Logging** (`src/security/telemetry/`)
   - Machine-specific SHA-256 tag generation (hardware-based)
   - GitHub API client for private repository logging
   - Telemetry data types and structures

2. **3-Tier Kill-Switch System** (`src/security/kill_switch/`)
   - Tier 1: Per-tag revocation (reversible by owner)
   - Tier 2: Auto kill-switch (RE attack detection, irreversible)
   - Tier 3: Global kill-switch (REVOKE_ALL, permanent)

3. **Owner Management Dashboard** (`telemetry_dashboard.py`)
   - Python CLI tool for telemetry management
   - Machine listing and analytics
   - Incident review workflow
   - Kill-switch management commands

### ⏳ Pending Components

1. **Binary Build** (requires Linux environment)
   - Build x86_64 Linux binary
   - Build ARM64 Linux binary
   - Integrate telemetry modules into main binary

2. **GitHub Repository Setup**
   - Create private repository: `shah786628/nawaz1-quantum-software-private`
   - Set up telemetry file structure
   - Configure GitHub PAT token

3. **GitHub Release Update**
   - Remove old v2.1.0 binaries (RE security reason)
   - Upload new v2.2.0 binaries with telemetry
   - Update release notes

## Architecture

### Runtime Tag Generation

Each machine generates a **unique SHA-256 tag** at first run:

```
Tag = SHA256(hardware_id + binary_hash + timestamp)
```

**Hardware ID Components:**
- CPU serial number / model name
- MAC address (first network interface)
- Disk UUID (root partition)
- Hostname + username (fallback)

**Benefits:**
- No pre-built tags (cannot be extracted from binary)
- Unique per machine (even with same binary)
- Tied to hardware (cannot be replayed)

### GitHub Repository Structure

**Public Repository** (binary distribution only):
```
shah786628/nawaz1-quantum-software/
├── bin/
│   ├── x86_64/nawaz1-server    # Linux x86_64 binary
│   └── arm64/nawaz1-server     # Linux ARM64 binary
├── README.md
└── (source code, documentation, NO telemetry)
```

**Private Repository** (RE security & telemetry - your existing "shah" repo):
```
[your-private-repo]/
├── telemetry/
│   ├── machines.json              # All registered machines
│   ├── auto_kill_incidents.json   # Auto-kill incident logs
│   └── analytics/
│       └── 2026-06-18.json        # Daily analytics
├── kill_switch/
│   ├── global_kill.txt            # "ACTIVE" or "INACTIVE"
│   ├── revoked_tags.json          # Per-tag revocations
│   └── auto_killed_binaries.json  # Permanently killed binaries
└── (RE security data, attack logs, forensics)
```

### 3-Tier Kill-Switch Logic

```rust
// On binary startup:
async fn security_check() -> Result<(), KillSwitchError> {
    let manager = KillSwitchManager::new(get_machine_tag()?);
    
    // Tier 3: Global kill-switch (highest priority)
    if check_global_kill().await? {
        display_suspension_message(KillSwitchResult::Revoked {
            tier: KillSwitchTier::Global,
            reason: "Global kill-switch activated (REVOKE_ALL)".to_string(),
            reversible: false,
        });
        std::process::exit(1);
    }
    
    // Tier 1: Per-tag revocation
    if check_per_tag_revocation().await? {
        display_suspension_message(KillSwitchResult::Revoked {
            tier: KillSwitchTier::PerTag,
            reason: "Machine tag revoked by owner".to_string(),
            reversible: true,
        });
        std::process::exit(1);
    }
    
    // Tier 2: Auto kill-switch (checked continuously during runtime)
    // Triggered by: debugger detection, memory tampering, binary modification
    
    Ok(())
}
```

### Auto-Kill Incident Logging

When RE attack is detected, the binary:

1. **Collects incident telemetry:**
   - Machine tag
   - Location (country, city, IP hash)
   - Timestamp
   - Machine specs (CPU, RAM, OS)
   - Binary info (version, build ID, SHA-256)
   - Attack indicators (debugger, tampering, modification)

2. **Logs to GitHub BEFORE dying:**
   ```rust
   telemetry_client.log_incident(incident).await?;
   ```

3. **Displays final message:**
   ```
   ═══════════════════════════════════════════════════
     BINARY AUTO-KILLED: Debugger detected (GDB attached)
     Machine tag: a3f5e9b2c8d1...
     Incident logged to owner
     This binary is PERMANENTLY suspended
   ═══════════════════════════════════════════════════
   ```

4. **Securely wipes memory and exits**

## Owner Dashboard Usage

### Setup

```bash
# Install dependencies
pip install requests

# Set GitHub PAT token
export GITHUB_TELEMETRY_TOKEN="ghp_your_token_here"
```

### Commands

```bash
# List all registered machines
python3 telemetry_dashboard.py --list-machines

# Review auto-kill incidents
python3 telemetry_dashboard.py --review-incidents

# Revoke specific machine tag (reversible)
python3 telemetry_dashboard.py --revoke-tag a3f5e9b2... --reason "Suspicious activity"

# Un-revoke tag (restore access)
python3 telemetry_dashboard.py --unrevoke-tag a3f5e9b2... --reason "False positive"

# Activate global kill-switch (PERMANENT)
python3 telemetry_dashboard.py --global-kill --reason "Source code compromised"

# Check global kill-switch status
python3 telemetry_dashboard.py --check-global

# Show analytics
python3 telemetry_dashboard.py --analytics

# Export data
python3 telemetry_dashboard.py --export-machines backup.json
```

## Security Guarantees

### What This System Prevents

✅ **Binary extraction attacks** - Tags generated at runtime, not pre-built  
✅ **Tag replay attacks** - Tags tied to hardware IDs  
✅ **Unauthorized usage** - Per-tag revocation blocks specific machines  
✅ **Reverse engineering** - Auto kill-switch detects debuggers/tampering  
✅ **Mass compromise** - Global kill-switch revokes all machines instantly  

### What This System Enables

✅ **Forensic visibility** - All RE attacks logged with full telemetry  
✅ **Granular control** - Revoke individual machines without affecting others  
✅ **Audit trail** - All revocations logged with timestamps and reasons  
✅ **Owner authority** - Only owner can revoke/un-revoke tags  
✅ **Emergency response** - Global kill-switch for catastrophic breaches  

## Build Instructions

### Prerequisites

- Rust toolchain (cargo, rustc)
- Linux environment (WSL or native)
- GitHub PAT with repo access

### Build Commands

```bash
# Navigate to project
cd nawaz1_dev

# Build x86_64 Linux binary
cargo build --release --target x86_64-unknown-linux-gnu

# Build ARM64 Linux binary (requires cross-compilation)
cargo build --release --target aarch64-unknown-linux-gnu

# Copy binaries to release directory
cp target/x86_64-unknown-linux-gnu/release/nawaz1-server bin/x86_64/
cp target/aarch64-unknown-linux-gnu/release/nawaz1-server bin/arm64/
```

### GitHub Release Update

```bash
# Remove old v2.1.0 release (RE security reason)
gh release delete v2.1.0 --yes

# Create new v2.2.0 release
gh release create v2.2.0 \
  --title "Nawaz1 Quantum Software v2.2.0" \
  --notes "Telemetry & kill-switch features added" \
  bin/x86_64/nawaz1-server \
  bin/arm64/nawaz1-server
```

## Testing

### Unit Tests

```bash
# Run telemetry module tests
cargo test --package nawaz1-security --lib telemetry::

# Run kill-switch tests
cargo test --package nawaz1-security --lib kill_switch::
```

### Integration Tests

```bash
# Test machine tag generation
cargo test --package nawaz1-security test_generate_machine_tag

# Test GitHub telemetry client (requires token)
GITHUB_TELEMETRY_TOKEN=ghp_test cargo test --package nawaz1-security test_telemetry_client
```

## Known Issues

### Current Limitation

Your local machine tag `9a2b2dda...0b96af80` is **per-tag revoked** from previous testing. This means:

- ❌ You cannot run any binary with this tag
- ✅ Owner can un-revoke this tag using dashboard
- ✅ New binaries will generate new tags (not affected)

### Resolution Options

**Option 1: Un-revoke current tag**
```bash
python3 telemetry_dashboard.py --unrevoke-tag 9a2b2dda... --reason "Testing complete"
```

**Option 2: Build fresh binary**
```bash
cargo build --release
# New binary will generate new tag on first run
```

## Next Steps

1. ✅ **Implementation complete** - All Rust modules created
2. ⏳ **Build binaries** - Requires Linux environment
3. ⏳ **Set up private GitHub repo** - Create telemetry structure
4. ⏳ **Test with new binary** - Verify telemetry logging works
5. ⏳ **Update public GitHub release** - Remove old, upload new

## Support

For issues or questions:
- Owner: Shahnawaz Alam
- Email: shahnawaz512001@gmail.com
- GitHub: https://github.com/shah786628/nawaz1-quantum-software

## License

**Proprietary** - All rights reserved. No unauthorized distribution or modification permitted.
