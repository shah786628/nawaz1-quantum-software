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
All binaries include built-in protection mechanisms:
- **Debugger Detection**: Automatically detects and blocks debuggers
- **Auto Protection**: Binary disables itself after tampering attempts
- **Binary Integrity**: Verification prevents unauthorized modifications
- **Execution Logging**: All runs logged for security monitoring

**WARNING: Running in debug mode will permanently disable the binary.**

---

## Download

See [nawaz1-quantum-software](https://github.com/shah786628/nawaz1-quantum-software) for binaries and documentation.

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

Proprietary. All rights reserved.
