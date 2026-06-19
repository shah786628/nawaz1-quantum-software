# Nawaz1 Quantum Engine

Proprietary quantum computing engine. Binary-only distribution.

## Runtime Requirements

**All binaries run in ANY environment — native OS, WSL, VM, containers, debug or release mode.**

### Supported Platforms:
- **Linux x86_64**: `bin/x86_64/nawaz1-server` (bare-metal, WSL, VM, containers)
- **Linux ARM64**: `bin/arm64/nawaz1-server` (AWS Graviton, Raspberry Pi, bare-metal, VMs)

### Runtime Freedom:
- ✅ **Any environment** — Native OS, WSL, VM, Docker, cloud instances
- ✅ **Debug or release mode** — No restrictions, runs everywhere
- ✅ **No auto kill-switch** — Binary never disables itself based on environment detection

### Security Protection (Non-Intrusive):
All binaries include enterprise-grade RE protection that **never blocks execution**:
- **Debugger Detection**: Logs debugger presence for telemetry (does NOT block execution)
- **Dual-Key AES-256+QKD**: Quantum-inspired encryption protects binary integrity
- **Attack Detection**: Monitors AES-GCM decryption failures → immediate key rotation (<1ms) if unauthorized key usage detected
- **Binary Integrity**: Verification prevents unauthorized modifications
- **Owner-Controlled Revocation**: Per-tag and global kill-switch (manual, owner-only)

**No false positives. No environment restrictions. Runs everywhere.**

---

## Download

See [nawaz1-quantum-software](https://github.com/shah786628/nawaz1-quantum-software) for binaries and documentation.

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

Proprietary. All rights reserved.
