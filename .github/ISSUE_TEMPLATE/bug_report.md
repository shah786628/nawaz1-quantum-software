---
name: Bug Report
about: Report incorrect behavior, crashes, or unexpected results
title: "[Bug] "
labels: bug
assignees: ''
---

## Describe the Bug

A clear and concise description of what the bug is.

## Environment

| Field | Value |
|-------|-------|
| OS | (e.g., Ubuntu 24.04 LTS) |
| CPU Architecture | (e.g., x86_64, ARM64) |
| Binary Version | (paste output of `curl http://localhost:8080/api/v1/version`) |
| Deployment Method | (bare binary / Docker / Kubernetes / WSL2) |

## Steps to Reproduce

1. Start the server: `./bin/x86_64/nawaz1-server`
2. Run this request:
   ```bash
   curl -X POST http://localhost:8080/api/v1/quantum/execute \
     -H "Content-Type: application/json" \
     -d '{...}'
   ```
3. Observe the response

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened. Include the full JSON response or error message.

## Health Check Output

```bash
curl http://localhost:8080/api/v1/health
# Paste output here
```

## Logs

Relevant server log output (set `NAWAZ1_LOG_LEVEL=debug` for verbose logs):

```
# Paste logs here
```

## Additional Context

Any other information that might help diagnose the issue (screenshots, related issues, etc.).
