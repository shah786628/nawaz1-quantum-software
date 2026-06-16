# nawaz1-server Binary Distribution

## Available Binaries

| Platform | Architecture | Status | Path |
|----------|-------------|--------|------|
| Linux | x86_64 | Available | bin/x86_64/nawaz1-server |
| Linux | aarch64 | Available | bin/arm64/nawaz1-server |

## Running the Server

### Linux x86_64

Ensure the binary has execute permission, then run:

    ./bin/x86_64/nawaz1-server

### Linux aarch64

Ensure the binary has execute permission, then run:

    ./bin/arm64/nawaz1-server

## Environment Variables

- NAWAZ1_API_KEY (required): API key for authentication
- JWT_SECRET (required): Secret for JWT token signing
- BIND_ADDR (optional): Listen address (default: 0.0.0.0:8080)

## Security

- All binaries are hardened release builds with symbols stripped
- Binary expiration policy enforced
- Kill-switch revocation mechanism enabled
- No source code is distributed - binary-only deployment

## Binary Distribution

Pre-built binaries are included in the `bin/` directory for immediate use.
