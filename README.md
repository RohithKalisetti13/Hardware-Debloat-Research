# Hardware Debloat via Ghidra Static Analysis + DECAF Runtime Enforcement

This repository presents a research project focused on enhancing control-flow integrity (CFI) for embedded and high-assurance systems through **static control flow analysis using Ghidra** and **dynamic runtime validation via the DECAF framework**.

>  [Read the Full Research Paper](./Scholarly%20Paper.pdf)

---

## Project Overview

In modern embedded and IoT devices, controlling access to hardware resources based on valid execution paths is essential for securing against control-flow hijacking attacks (ROP, COP, JOP). This project tackles the problem of **hardware debloating** by analyzing binaries with Ghidra and restricting hardware access at runtime using DECAF.

We developed a **Ghidra plugin** that:
- Statistically extracts control flow graphs (CFGs)
- Identifies direct and computed (indirect) calls
- Handles unresolved calls through **overestimation**
- Supports recursive depth-controlled analysis
- Integrates seamlessly with DECAF for runtime CFI enforcement

---

## Repository Contents

| File/Folder | Description |
|-------------|-------------|
| `recursive_syscall.c` | C file for syscall tracking and runtime introspection |
| `depthTracing.py` | Ghidra plugin for static control flow graph extraction  |
| `Scholarly Paper.pdf` | Full research write-up submitted under GMU ECE |
| `GHIDRA_SETUP.md` | Guide to install Ghidra and run the plugin |
| `.gitignore` | Clean ignores for system/cache files |

---

## Key Features

- **Recursive Call Tracing** with max-depth control
- **Computed Call Analysis** (via Ghidra p-code engine)
- **Overestimation for Unresolved Targets**
- **CFG Generation** per function
- **DECAF Integration**: Compare runtime call stack to valid paths
- Protects against ROP/COP-style control flow hijacking

---

## Results (as shown in the paper)

- Generated valid control flow graphs for test binaries
- Accurately traced recursive call chains
- Identified indirect calls and overestimated targets
- Integrated CFGs into DECAF for real-time hardware gating

> The system successfully restricted hardware access for illegal execution flows with **minimal runtime overhead**.

---

## Running the Plugin

See [GHIDRA_SETUP.md](./GHIDRA_SETUP.md) for detailed step-by-step setup and usage instructions.

---

## Citation

If you reference this work, please cite:

Rohith Kumar Kalisetti, "Hardware Debloating through Recursive Syscall Analysis and Control Flow Enforcement", GMU Scholarly Research, 2024.


---

## License

This repository is shared for academic and demonstration purposes. You may fork it for scholarly reuse with attribution.


