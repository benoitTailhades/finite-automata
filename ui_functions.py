import os
import sys
from automaton import Automaton

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"
GRAY = "\033[37m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    print(f"{CYAN}{BOLD}")
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║          FINITE  AUTOMATON  TOOLKIT  v1.0            ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print(RESET)


def section(title: str):
    width = 56
    pad = (width - len(title) - 2) // 2
    print(f"\n{BLUE}{BOLD}  {'─' * pad} {title} {'─' * pad}{RESET}\n")


def success(msg: str):
    print(f"  {GREEN}✔  {msg}{RESET}")


def warn(msg: str):
    print(f"  {YELLOW}⚠  {msg}{RESET}")


def error(msg: str):
    print(f"  {RED}✘  {msg}{RESET}")


def info(msg: str):
    print(f"  {CYAN}ℹ  {msg}{RESET}")


def prompt(msg: str) -> str:
    return input(f"  {MAGENTA}›{RESET} {msg} ")


def pause():
    input(f"\n  {DIM}Press Enter to return to the menu…{RESET}")


def draw_menu(items: list[tuple[str, str]], title: str = "MAIN MENU"):
    section(title)
    for key, label in items:
        print(f"  {YELLOW}{BOLD}[{key}]{RESET}  {WHITE}{label}{RESET}")
    print()


# ─────────────────────────────────────────────
#  Menu actions
# ─────────────────────────────────────────────

def load_automaton() -> Automaton | None:
    base_path = "data/"
    section("LOAD AUTOMATON")
    path = prompt("Enter the path to the automaton file:").strip()
    path = 'FA' + path + ".txt"
    if not os.path.isfile(base_path+path):
        error(f"File not found: {path}")
        pause()
        return None
    try:
        a = Automaton(path)
        success(f"Automaton loaded from '{path}'")
        info(f"States: {a.states}  |  Alphabet: {a.alphabet}")
        info(f"Initial: {a.initialStates}  |  Final: {a.finalStates}")
        pause()
        return a
    except Exception as e:
        error(f"Failed to load automaton: {e}")
        pause()
        return None


def action_display(automaton: Automaton):
    section("TRANSITION TABLE")
    automaton.display_automaton()
    pause()


def action_is_deterministic(automaton: Automaton):
    section("DETERMINISM CHECK")
    result,msg = automaton.is_deterministic()
    if result:
        success(msg)
    else:
        warn(msg)
    pause()


def action_is_complete(automaton: Automaton):
    section("COMPLETENESS CHECK")
    result = automaton.is_complete()
    if result:
        success("The automaton is complete.")
    else:
        warn("The automaton is NOT complete (see missing transitions above).")
    pause()

def action_is_standard(automaton: Automaton):
    section("STANDARD CHECK")
    result,msg = automaton.is_standard()
    if result:
        success(msg)
    else:
        warn(msg)
    pause()


def action_completion(automaton: Automaton):
    section("COMPLETION")
    automaton.completion()
    success("Completion done. The automaton now has a trash state 'P' if needed.")
    pause()

def action_determination(automaton: Automaton):
    section("DETERMINATION")
    automaton.determinize()
    success("The automaton is now deterministic.")
    pause()



def action_minimisation(automaton: Automaton):
    section("MINIMISATION")
    warn("Note: the automaton must be deterministic and complete before minimising.")
    confirm = prompt("Proceed? (y/n):").strip().lower()
    if confirm == 'y':
        automaton.minimisation()
        success("Minimisation complete.")
    else:
        info("Minimisation cancelled.")
    pause()

def action_standardization(automaton: Automaton):
    section("STANDARDIZATION")
    automaton.standardization()
    success("Standardization complete.")
    pause()


def action_mermaid(automaton: Automaton):
    section("EXPORT MERMAID GRAPH")
    custom = prompt("Custom output filename (without extension) or Enter for default:").strip()
    filename = custom if custom else None
    try:
        automaton.create_mermaid_graph_from_automaton(filename)
        out = (filename or automaton.filename.split('.')[0]) + ".mmd"
        success(f"Mermaid graph written to '{out}'")
    except Exception as e:
        error(f"Export failed: {e}")
    pause()


def action_full_pipeline(automaton: Automaton):
    """Runs: display → determinism check → completion → minimisation → export."""
    section("FULL PIPELINE")
    info("Step 1 – Display current automaton")
    automaton.display_automaton()

    info("Step 2 – Determinism check")
    det = automaton.is_deterministic()

    if not det:
        warn("Automaton is non-deterministic. Minimisation requires a DFA.")
        warn("Skipping completion and minimisation.")
    else:
        info("Step 3 – Completion")
        automaton.completion()
        success("Completion done.")

        info("Step 4 – Minimisation")
        automaton.minimisation()
        success("Minimisation done.")

    info("Step 5 – Export Mermaid graph")
    automaton.create_mermaid_graph_from_automaton()
    out = automaton.filename.split('.')[0] + ".mmd"
    success(f"Graph exported to '{out}'")

    info("Step 6 – Display final automaton")
    automaton.display_automaton()
    pause()




MENU_ITEMS = [
    ("1",  "Display transition table"),
    ("2",  "Check determinism"),
    ("3",  "Check completeness"),
    ("4",  "Check standardism"),
    ("5",  "Determinize the automaton"),
    ("6",  "Complete the automaton (add trash state)"),
    ("7",  "Standardize the automaton"),
    ("8",  "Minimise the automaton"),
    ("9",  "Export Mermaid graph (.mmd)"),
    ("10", "Run full pipeline  (display → complete → minimise → export)"),
    ("─",  "─" * 40),
    ("l",  "Load a different automaton"),
    ("q",  "Quit"),
]
