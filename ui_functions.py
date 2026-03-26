from automaton import Automaton
from ui_utils import *


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

def action_check_word(automaton: Automaton):
    section("WORD RECOGNITION")
    info(f"Alphabet: {', '.join(automaton.alphabet)}")
    word = prompt("Enter a word to check (leave empty for epsilon) write \'end\' to end the word recognitions:").strip()
    while word != "end":
        # recognize_word handles the logic and prints its own success/failure messages
        result = automaton.recognize_word(word)

        if result:
            success(f"The word '{word}' is accepted by the automaton.")
        else:
            warn(f"The word '{word}' is rejected.")
        word = prompt("Enter a word to check (leave empty for epsilon) write \'end\' to end the word recognitions:").strip()

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
    ("10", "Check word recognition"),
    ("11", "Run full pipeline  (display → complete → minimise → export)"),
    ("─",  "─" * 40),
    ("l",  "Load a different automaton"),
    ("q",  "Quit"),
]
