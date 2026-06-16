# Contributing to Nawaz1 Quantum Software

Thank you for your interest in contributing! This guide explains how to get involved, report issues, and submit improvements.

---

## Ways to Contribute

| Type | What It Looks Like |
|------|-------------------|
| **Bug reports** | Found incorrect output, a crash, or unexpected behavior? File an issue |
| **Feature requests** | Have an idea for a new domain, algorithm, or tutorial? Open a feature request |
| **Documentation** | Improve existing docs, add tutorials, fix typos |
| **Examples** | Add Python examples, Jupyter notebooks, or integration guides |
| **Plugins** | Build a domain plugin using the Extension Plugin system |
| **Community support** | Answer questions in issues, review pull requests |

---

## Reporting Bugs

Use the [Bug Report issue template](https://github.com/shah786628/nawaz1-quantum-software/issues/new?template=bug_report.md) and include:

1. **Environment:** OS, CPU architecture, binary version
2. **Steps to reproduce:** exact commands or API calls
3. **Expected behavior:** what should have happened
4. **Actual behavior:** what actually happened, including error messages
5. **Logs:** relevant output from `/api/v1/health` and server logs

### Quick Bug Report (curl)

```bash
# Get version info to include in your report
curl http://localhost:8080/api/v1/version

# Get health status
curl http://localhost:8080/api/v1/health
```

---

## Suggesting Features

Use the [Feature Request issue template](https://github.com/shah786628/nawaz1-quantum-software/issues/new?template=feature_request.md) and describe:

1. **Use case:** what problem are you trying to solve?
2. **Proposed solution:** how should it work?
3. **Alternatives considered:** what else have you tried?

---

## Developing a Domain Plugin

The Extension Plugin system lets you add custom algorithms without modifying the engine. Your plugin implements a single trait and runs on the same VQE execution substrate as all built-in domains.

### Plugin Architecture

```
Your custom algorithm
  -> implements AlgorithmPlugin trait
  -> passes multi-layer security validation
  -> compiled onto VQE execution substrate via Algorithm Interface
  -> engine auto-selects qubit width (you don't choose)
```

### Python Plugin Example

Here is a minimal plugin that wraps a custom optimization algorithm:

```python
"""
Example: Custom Portfolio Optimizer Plugin

This plugin encodes a custom risk-adjusted portfolio scoring function
and submits it to the VQE engine for optimization.
"""
import requests
import numpy as np

class CustomPortfolioPlugin:
    """Custom portfolio optimization using domain-specific scoring."""

    def __init__(self, server_url="http://localhost:8080"):
        self.server_url = server_url

    def score_assets(self, returns, volatility, correlation_penalty=0.1):
        """
        Custom scoring: Sharpe ratio with correlation penalty.

        Args:
            returns: list of expected annual returns
            volatility: list of annual volatilities
            correlation_penalty: penalty for correlated assets
        Returns:
            list of orbital energies (negative = preferred)
        """
        returns = np.array(returns)
        volatility = np.array(volatility)

        # Base score: risk-adjusted return (Sharpe-like)
        scores = -(returns / volatility)

        # Penalty: assets with similar returns are penalized
        for i in range(len(returns)):
            for j in range(i + 1, len(returns)):
                similarity = abs(returns[i] - returns[j])
                scores[i] += correlation_penalty * (1 - similarity)
                scores[j] += correlation_penalty * (1 - similarity)

        return scores.tolist()

    def optimize(self, returns, volatility):
        """Submit custom-scored portfolio to the VQE engine."""
        orbital_energies = self.score_assets(returns, volatility)

        response = requests.post(
            f"{self.server_url}/api/v1/quantum/execute",
            json={
                "domain": "finance",
                "algorithm": "qaoa",
                "qubits": len(returns),
                "problem": {
                    "orbital_energies": orbital_energies
                }
            }
        )
        return response.json()


# Usage
if __name__ == "__main__":
    plugin = CustomPortfolioPlugin()
    result = plugin.optimize(
        returns=[0.15, 0.12, 0.08, 0.18, 0.25],
        volatility=[0.22, 0.20, 0.25, 0.30, 0.55]
    )
    print(f"Optimal energy: {result['result']['aggregate_energy']:.6f}")
    print(f"Converged: {result['result']['converged']}")
```

For the full plugin API specification, see [`packages/extension_plugin/README.md`](packages/extension_plugin/README.md).

---

## Adding Documentation or Tutorials

We welcome improvements to the docs. When adding a tutorial:

1. Place it in `docs/tutorials/` with a descriptive filename
2. Include a time estimate and difficulty level at the top
3. Provide complete, runnable Python code
4. Show expected output for every step
5. Link back to relevant package READMEs and the main docs index

Update `docs/INDEX.md` to include a link to your new tutorial.

---

## Adding Examples

Python examples go in the `examples/` directory. Guidelines:

- Include a `# Usage:` comment at the top showing how to run it
- Handle the case where the server is not running (print a helpful message)
- Use `numpy` and `requests` only (no additional dependencies)
- Test that it runs successfully against a live server before submitting

---

## Code Style

### Python Examples and Tutorials

- Follow PEP 8 (4-space indentation, snake_case functions)
- Use type hints where they improve clarity
- Include docstrings for functions and classes
- Keep imports at the top of the file

### Markdown Documentation

- Use ATX-style headers (`#`, `##`, `###`)
- Use fenced code blocks with language tags (` ```python `)
- Tables for structured data; lists for sequential steps
- Link to other docs using relative paths

---

## Pull Request Process

1. Fork the repository and create a feature branch from `main`
2. Make your changes (documentation, examples, plugins, or test scripts)
3. Ensure all existing tests still pass:
   ```bash
   python test_physical_laws.py
   python test_energy_determinism.py
   ```
4. Submit a pull request with a clear description of what you changed and why
5. A maintainer will review and provide feedback

### What We Look For

- Clear, helpful changes that improve the user experience
- Documentation that is accurate and well-tested
- Examples that are runnable and include expected output
- Respect for the existing code style and structure

---

## Community Guidelines

- Be respectful and constructive in all interactions
- Focus on the technical merit of proposals
- Help newcomers — quantum computing has a steep learning curve
- Credit others' work and ideas appropriately

---

## Questions?

- Open an issue with the `question` label
- Check existing issues and discussions first
- Reference the [documentation index](docs/INDEX.md) for specific topics

---

## License

By contributing, you agree that your contributions will be licensed under the same proprietary license as the project. See [README.md](README.md#license) for full terms.
