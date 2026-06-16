# Nawaz1 Documentation

Welcome to the Nawaz1 Quantum Software documentation. This is your starting point for everything from first launch to production deployment.

---

## Important: Read Before Using the Engine

**Every user MUST understand these four rules before sending any request:**

1. **Correct Hamiltonian** — Your input data (orbital energies, interaction energies, or problem parameters) must represent a physically valid Hamiltonian. Wrong or random values will produce meaningless results. Always verify your Hamiltonian is Hermitian and physically meaningful.

2. **Correct Algorithm** — You MUST select the right algorithm for your problem. Using `vqe` for a search problem or `grover` for molecular energy will give wrong answers. See the [Algorithm Selection Guide](../README.md#supported-algorithms-108) to match your problem to the correct algorithm.

3. **Qubits = Power of 2** — When manually specifying qubit count, it MUST be a power of 2: `4`, `8`, `16`, `32`, `64`, `128`, `256`, `512`, `1024`, `2048`, `4096`, `8192`, `16384`, `32768`, `65536`, etc. Non-power-of-2 values will be rejected or produce incorrect results.

4. **Read the Input Data Guide** — Before writing any code, read the [VQE Input Data Guide](../VQE_INPUT_DATA_GUIDE.md) and [All Algorithms Input Methods](../ALL_ALGORITHMS_INPUT_METHODS.md) to understand the correct `problem` field format for your algorithm.

---

## Getting Started

New to Nawaz1? Start here.

| Guide | Description |
|-------|-------------|
| [Quick Start](QUICKSTART.md) | Download, launch, and run your first quantum computation in under 5 minutes |
| [Architecture Overview](ARCHITECTURE.md) | Understand how the engine, API, and domain packages fit together |
| [Benchmarks](BENCHMARKS.md) | Reference performance figures across qubit scales |

---

## Tutorials

Step-by-step walkthroughs for real-world use cases.

| Tutorial | Domain | Time |
|----------|--------|------|
| [Chemistry: Ground State of H2O](tutorials/chemistry_h2o.md) | Quantum Chemistry | 5 min |
| [Finance: Portfolio Optimization with QAOA](tutorials/finance_qaoa.md) | Quantum Finance | 5 min |
| [ML: Quantum Kernel Classification](tutorials/ml_quantum_kernel.md) | Quantum Machine Learning | 5 min |
| [Continuum QFT Solvation](SOLVATION_QFT.md) | Chemistry / Biology / Physics | 10 min |
| [Database Package](DATABASE_PACKAGE.md) | SQL / Vector / Graph / Geo / Security / Probabilistic / ML | 10 min |

---

## Reference Documentation

Deep-dive technical guides for each subsystem.

| Document | What It Covers |
|----------|---------------|
| [README](../README.md) | Full feature list, API reference, configuration, deployment |
| [VQE Input Data Guide](../VQE_INPUT_DATA_GUIDE.md) | How to format `problem` field data for the VQE engine |
| [All Algorithms Input Methods](../ALL_ALGORITHMS_INPUT_METHODS.md) | Input format for every one of the 108 supported algorithms |
| [Input Data Technical Notes](../INPUT_DATA_TECHNICAL_NOTES.md) | Encoding rules, normalization, and data-type constraints |
| [Examples Directory](../examples/) | Runnable Python scripts for all input formats |

---

## Domain Packages

Each of the 17 domain packages has its own README with algorithms, input formats, and examples.

| Package | Documentation |
|---------|--------------|
| Chemistry | [`packages/chemistry/README.md`](../packages/chemistry/README.md) |
| Biology | [`packages/biology/README.md`](../packages/biology/README.md) |
| Physics | [`packages/physics/README.md`](../packages/physics/README.md) |
| Finance | [`packages/finance/README.md`](../packages/finance/README.md) |
| Materials Science | [`packages/materials_science/README.md`](../packages/materials_science/README.md) |
| Machine Learning | [`packages/machine_learning/README.md`](../packages/machine_learning/README.md) |
| Mathematics | [`packages/mathematics/README.md`](../packages/mathematics/README.md) |
| Fluid Mechanics | [`packages/fluid_mechanics/README.md`](../packages/fluid_mechanics/README.md) |
| Turbulence / CFD | [`packages/turbulence_cfd/README.md`](../packages/turbulence_cfd/README.md) |
| Heat Transfer | [`packages/heat_transfer/README.md`](../packages/heat_transfer/README.md) |
| Logistics | [`packages/logistics/README.md`](../packages/logistics/README.md) |
| Graphics | [`packages/graphics/README.md`](../packages/graphics/README.md) |
| Time Evolution | [`packages/time_evolution/README.md`](../packages/time_evolution/README.md) |
| Error Mitigation | [`packages/error_mitigation/README.md`](../packages/error_mitigation/README.md) |
| Cross Domain | [`packages/cross_domain/README.md`](../packages/cross_domain/README.md) |
| Extension Plugin | [`packages/extension_plugin/README.md`](../packages/extension_plugin/README.md) |
| SDK | [`packages/sdk/README.md`](../packages/sdk/README.md) |

---

## Community

| Resource | Description |
|----------|-------------|
| [Contributing Guide](../CONTRIBUTING.md) | How to report bugs, suggest features, and submit pull requests |
| [Roadmap](../ROADMAP.md) | Public project roadmap and upcoming features |
| [Issue Tracker](https://github.com/shah786628/nawaz1-quantum-software/issues) | Report bugs and request features |

---

## Deployment

| Method | Best For |
|--------|---------|
| [Docker / Docker Compose](../README.md#deployment) | Quick local or cloud deployment |
| [Systemd Service](../README.md#deployment) | Bare-metal Linux production servers |
| [Kubernetes](../README.md#deployment) | Cluster-scale production with auto-scaling |

---

## Support

- **Issues:** [github.com/shah786628/nawaz1-quantum-software/issues](https://github.com/shah786628/nawaz1-quantum-software/issues)
- **Author:** Shahnawaz Alam
