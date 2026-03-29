# 🤖 Finite Automaton Toolkit

> EFREI P2 INT 2025/2026 — Finite Automata and Regular Expressions Project

**Authors:** Nolann Fotso · Loic Giannini · Benoit Tailhades · Abigail Mialaret

---

## Overview

A Python command-line toolkit for studying and transforming finite automata (FA). The program loads automata from text files and walks the user through a full pipeline: property checks, standardization, determinization, completion, minimization, word recognition, and complementary language construction.

---

## Project Structure

```
.
├── main.py            # Entry point — interactive menu loop
├── automaton.py       # Automaton class with all FA algorithms
├── ui_functions.py    # Menu actions + trace generation pipeline
├── ui_utils.py        # Terminal styling helpers (colors, prompts)
├── data/              # Input automaton files (FA1.txt, FA2.txt, …)
├── traces/            # Generated execution trace files
└── mermaid_output/    # Exported .mmd graph files
```

---

## Getting Started

### Requirements

- Python 3.10 or higher (uses `match` / structural pattern matching)
- No external dependencies

### Running the program

```bash
python main.py
```

At startup you will be asked which automaton to load. Type a number (e.g. `5` to load `data/FA5.txt`) and press Enter.

---

## Automaton File Format

Files live in `data/` and follow this structure:

```
<number of alphabet symbols>
<number of states>
<count of initial states> <state1> <state2> …
<count of final states>   <state1> <state2> …
<number of transitions>
<source> <symbol> <target>
…
```

**Example** — automaton with alphabet `{a, b}`, 5 states, 1 initial state (0), 1 final state (4), 6 transitions:

```
2
5
1 0
1 4
6
0 a 0
0 b 0
0 a 1
1 b 2
2 a 3
3 a 4
```

States are numbered from `0`. The alphabet is always the first *n* lowercase letters (`a`, `b`, `c`, …). The symbol `E` is reserved for epsilon transitions (the program handles synchronization automatically on load).

---

## Features

| Key | Action |
|-----|--------|
| `l` | Load a different automaton |
| `1` | Display the transition table |
| `2` | Check determinism |
| `3` | Check completeness |
| `4` | Check standardness |
| `5` | Determinize (subset construction) |
| `6` | Complete (add sink/trash state `P`) |
| `7` | Standardize (create single initial state) |
| `8` | Minimize (Myhill–Nerode partition refinement) |
| `9` | Export Mermaid graph (`.mmd`) |
| `10` | Test word recognition |
| `11` | Test word recognition on the complementary automaton |
| `12` | Run full pipeline (display → complete → minimize → export) |
| `q` | Quit |

---

## Algorithms

### Standardization
Creates a single new initial state that merges the transitions of all existing initial states. If any original initial state was accepting, the new state is also marked accepting.

### Determinization
Subset construction (powerset construction). Each DFA state is a set of NFA states, labeled by concatenating state numbers (e.g. `"023"`, or `"1.2.12"` when any number exceeds one digit). A sink state `P` is added for empty subsets.

### Completion
Adds a sink state `P` (if not already present) and routes all missing transitions there. `P` loops on every symbol.

### Minimization
Myhill–Nerode partition refinement:
1. Initial partition: `{final states}` | `{non-final states}`
2. Each iteration splits groups whose members disagree on which group a symbol leads to.
3. Repeats until the partition is stable.

The program prints every intermediate partition and the signature of each state at each step.

### Word Recognition
Reads the entire word as a string first (no letter-by-letter testing), then simulates the automaton step by step, printing the active state set after each symbol. Type `end` to exit the recognition loop.

### Complementary Automaton
Swaps final and non-final states on a complete deterministic automaton. The CDFA is used as the base (it is already complete and deterministic), so the complement is built in one pass.

### Epsilon Removal (Synchronization)
Loaded automatically when the file contains `E`-transitions. Computes epsilon-closures and rebuilds the automaton as a standard NFA without epsilon transitions.

---

## Execution Traces

Traces record everything printed to the screen during the full pipeline for a given automaton. They are required for submission alongside the source code.

### Generate all traces at once

```bash
python ui_functions.py
```

This runs `generate_all_traces` for automata `FA1.txt` through `FA44.txt` and writes the results to `traces/FA1.txt` … `traces/FA44.txt`. Files for automata that do not exist are skipped.

### Generate a single trace programmatically

```python
from ui_functions import generate_trace
generate_trace(5)   # processes data/FA5.txt → traces/FA5.txt
```

---

## Mermaid Export

Option `9` exports the current automaton to a `.mmd` file in `mermaid_output/`. Final states are rendered with triple parentheses `(((state)))`, regular states with double parentheses `((state))`, and initial states have an invisible entry arrow.

You can preview `.mmd` files on [mermaid.live](https://mermaid.live) or inside any Markdown editor that supports Mermaid diagrams.

---

## Notes

- **Determinization of an already-deterministic automaton is blocked** — the program checks first and reports an error if you try.
- **Minimization requires a complete DFA** — run completion and determinization first (or use the full pipeline).
- State names in the determinized/minimized automaton encode their origin: `"1.2.3"` means the set `{1, 2, 3}`; `"12.3"` means `{12, 3}`.
- The program supports automata of any size (no hard limit on states or alphabet).

---

## License

Academic project — EFREI Paris, 2025/2026.
