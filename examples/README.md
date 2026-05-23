# VQE Engine Input Data Examples

This directory contains complete working examples demonstrating all supported input data formats for the nawaz1 Unified Quantum VQE Engine.

---

## 📚 Examples

### [`vqe_input_examples.py`](vqe_input_examples.py)
Complete working examples for all input formats:
- ✅ H₂ molecule (pre-computed integrals)
- ✅ Custom Hamiltonian (orbital energies)
- ✅ Ising model (interaction energies)
- ✅ Heisenberg model (quantum magnetism)
- ✅ Portfolio optimization (finance)
- ✅ WRONG vs RIGHT comparison

**Run:**
```bash
python vqe_input_examples.py
```

---

## 🎯 Quick Start

### 1. Start the VQE Engine Server

```bash
cd /opt/nawaz1
./nawaz1-server &
```

### 2. Run Examples

```bash
cd examples
python vqe_input_examples.py
```

---

## 📋 Input Formats Summary

| Format | Use Case | Field | Example |
|--------|----------|-------|---------|
| **Molecule** | Pre-computed molecules | `molecule` + `bond_length` | H₂, LiH |
| **Orbital Energies** | Custom Hamiltonian | `problem.orbital_energies` | Any quantum system |
| **Interaction Energies** | Physics models | `problem.interaction_energies` | Ising, Heisenberg |

---

## ⚠️ Important

### ❌ WRONG: Using `input_data`

```python
# This WON'T WORK!
payload = {
    "domain": "chemistry",
    "qubits": 4,
    "input_data": [0.5, 0.5, 0.5, 0.5]  # IGNORED!
}
```

### ✅ CORRECT: Use `problem` field

```python
# This WORKS!
payload = {
    "domain": "chemistry",
    "qubits": 4,
    "problem": {
        "orbital_energies": [0.5, 0.5, 0.5, 0.5]  # USED!
    }
}
```

---

## 📖 Full Documentation

See [`../VQE_INPUT_DATA_GUIDE.md`](../VQE_INPUT_DATA_GUIDE.md) for complete documentation with:
- Detailed examples for all domains
- Advanced usage patterns
- Troubleshooting guide
- API response structure

---

## 🔗 Resources

- **Main Repository:** https://github.com/shah786628/nawaz1-quantum-software
- **Engine Source:** https://github.com/shah786628/nawaz1_dev
- **API Documentation:** `nawaz1_dev/src/api/quantum_handlers.rs`

---

## 🎓 Learning Path

1. **Start with:** `vqe_input_examples.py` (run all examples)
2. **Read:** `VQE_INPUT_DATA_GUIDE.md` (understand formats)
3. **Experiment:** Modify examples for your use case
4. **Explore:** Check engine source code for implementation details

---

## ✨ Key Points

1. ✅ Use `problem` field for custom data
2. ✅ Use `molecule` field for H₂, LiH
3. ✅ Data must be physically meaningful
4. ✅ Engine auto-selects optimal qubit width
5. ✅ Results include energy, fidelity, convergence info

---

## 🐛 Troubleshooting

### Energy returns 0?
- Check you're using `problem` field, not `input_data`
- Verify Hamiltonian coefficients are valid

### Engine returns error?
- Check molecule name (only H₂, LiH supported with `molecule` field)
- Verify data array is not empty

### Results not converging?
- Check Hamiltonian is Hermitian (real coefficients)
- Increase `max_iterations` in config

---

## 📝 License

Proprietary - Nawaz1 Quantum Software

## 👤 Author

Shahnawaz Alam
