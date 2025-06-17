# Ghidra Plugin Setup & Execution Guide

This guide outlines how to install Ghidra, configure your Python (Jython) plugin environment, and run the `depthTracing.py` script to analyze binary control flow for hardware debloating.

---

## Step 1: Download and Install Ghidra

1. Visit the official release page:  
   https://github.com/NationalSecurityAgency/ghidra/releases

2. Download the latest release, e.g.:
   ghidra_10.x_PUBLIC_yyyymmdd.zip

3. Extract it:
```bash
unzip ghidra_10.x_PUBLIC_yyyymmdd.zip
cd ghidra_10.x

```
---
## Step 2: Install Java (Required for Ghidra)
Ensure Java 11 or 17 is installed:
`sudo apt update`
`sudo apt install openjdk-17-jdk`
`java -version`

---

## Step 3: Launch Ghidra
`./ghidraRun`
This will start the Ghidra GUI.

---

## Step 4: Configure Ghidra Script Environment

1. In Ghidra, open or create a new project
2. Import your target binary (e.g., .elf, .bin, .o)
3. Go to Window → Script Manager
4. Set your script directory:
   `/home/yourname/ghidra_scripts/`
5. Move your plugin script into that directory:
   `depthTracing.py`

---

## Step 5: Run the Plugin Script

In Script Manager:
Locate `depthTracing.py`
Right-click → Run

---

### What This Plugin Does

1. Scans all functions in the loaded binary
2. Traverses direct and computed calls
3. Captures recursive call paths
  Reports:
   1. Unresolved targets
   2. Call overestimation
   3. Direct call maps per function
4. Constructs a control-flow graph (CFG) for runtime enforcement

---

## Example Console Output

```text
Listing all functions in the program:
Function: main at Address: 0010138a

Captured Function Call Graph - Direct Calls:
Function 'main' directly calls 'open'

Captured Function Call Graph - Computed Calls:
Function '__libc_csu_init' has computed calls to: ...

```
---

## Dependencies

Ghidra 10.x or later
OpenJDK 11 or 17
Python 2.7 (Jython embedded in Ghidra)

---

## Notes

Script uses Ghidra’s headless FlatProgramAPI and FunctionManager
Designed for compatibility with the DECAF runtime validator
Works best on statically linked binaries for syscall-heavy inspection

---

## License and Credit

Plugin developed as part of:

"Hardware Debloating through Recursive Syscall Analysis and Control Flow Enforcement"
Rohith Kumar Kalisetti, GMU Research, 2024



