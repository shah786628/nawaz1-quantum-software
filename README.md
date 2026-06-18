# Nawaz1 Quantum Engine

Proprietary quantum computing engine. Binary-only distribution.

## Runtime Requirements

**CRITICAL: All binaries must run in NATIVE operating system mode — NO debug mode allowed.**

### Supported Platforms:
- **Linux x86_64**: Runs on bare-metal Linux servers (Ubuntu, Debian, CentOS, etc.)
- **Linux ARM64**: Runs on ARM64 Linux servers (AWS Graviton, Raspberry Pi, etc.)
- **Windows x86_64**: Runs on native Windows 10/11 (.exe)

### Runtime Restrictions:
- ❌ **NO debug mode** — Binaries detect and auto-kill when debuggers are attached
- ❌ **NO WSL runtime** — Linux binaries must NOT run in WSL/VM (triggers RE protection)
- ❌ **NO VM/container runtime** — Linux binaries require bare-metal Linux
- ✅ **Native OS only** — Each binary runs directly on its target operating system

### Security Enforcement:
All binaries include advanced reverse-engineering (RE) protection:
- **Debugger Detection**: Automatically detects attached debuggers (Linux: ptrace/TracerPid, Windows: IsDebuggerPresent)
- **Auto Kill-Switch**: Binary self-revokes after 2 RE attack detections
- **Binary Integrity**: SHA-256 hash verification prevents tampering
- **Telemetry Logging**: All execution attempts logged to private repository

**Running in debug mode will trigger the auto kill-switch and permanently revoke the binary.**

---

## Download

See [nawaz1-quantum-software](https://github.com/shah786628/nawaz1-quantum-software) for binaries and documentation.

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

Proprietary. All rights reserved.
