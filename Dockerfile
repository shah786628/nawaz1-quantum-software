FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates tini curl && \
    rm -rf /var/lib/apt/lists/*

# Copy both architectures; the entrypoint selects the right one
COPY bin/x86_64/nawaz1-server /usr/local/bin/nawaz1-server-x86_64
COPY bin/arm64/nawaz1-server  /usr/local/bin/nawaz1-server-arm64

# Select the correct binary at build time based on target platform
ARG TARGETARCH
RUN if [ "$TARGETARCH" = "arm64" ]; then \
      cp /usr/local/bin/nawaz1-server-arm64 /usr/local/bin/nawaz1-server; \
    else \
      cp /usr/local/bin/nawaz1-server-x86_64 /usr/local/bin/nawaz1-server; \
    fi && \
    chmod +x /usr/local/bin/nawaz1-server && \
    rm -f /usr/local/bin/nawaz1-server-x86_64 /usr/local/bin/nawaz1-server-arm64

# Run as non-root user
RUN useradd --system --no-create-home --shell /usr/sbin/nologin nawaz1
USER nawaz1

EXPOSE 8080

ENV RUST_LOG=info \
    NAWAZ1_HOST=0.0.0.0 \
    NAWAZ1_PORT=8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -fsS http://localhost:8080/api/v1/health || exit 1

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/nawaz1-server"]
