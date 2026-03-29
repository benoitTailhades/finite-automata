from automaton import Automaton
from ui_utils import *
import sys
import os
import copy


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
    result,msg = automaton.is_complete()
    if result:
        success("The automaton is complete.")
    else:
        warn("The automaton is NOT complete (see missing transitions below).")
        warn(msg)
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

def action_check_word_complementary_automaton(automaton: Automaton):
    section("WORD RECOGNITION FOR COMPLEMENTARY AUTOMATON")
    info("New Complementary Automaton")
    new_automaton = automaton.complementary_automaton()
    success("Complementary Automaton complete.")
    info("Transition :")
    new_automaton.display_automaton()
    info(f"Alphabet: {', '.join(new_automaton.alphabet)}")
    word = prompt("Enter a word to check (leave empty for epsilon) write \'end\' to end the word recognitions:").strip()
    while word != "end":
        # recognize_word handles the logic and prints its own success/failure messages
        result = new_automaton.recognize_word(word)

        if result:
            success(f"The word '{word}' is accepted by the automaton.")
        else:
            warn(f"The word '{word}' is rejected.")
        word = prompt(
            "Enter a word to check (leave empty for epsilon) write \'end\' to end the word recognitions:").strip()

    pause()



TRACE_DIR = "traces/"
TEST_WORDS = ["", "a", "aa", "ab", "ba", "aab", "aba", "bba", "abab", "aaab"]


def generate_trace(fa_number: int):
    """
    Generate a text execution trace for automaton FA{fa_number}.txt.

    Redirects sys.stdout to a file in the traces/ directory while running
    the full pipeline, then restores the original stdout. If the source file
    does not exist, the function skips silently and prints a warning.

    The output file is named traces/FA{fa_number}.txt and mirrors exactly
    what would appear on screen during an interactive session.

    Args:
        fa_number (int): The index of the automaton to process (e.g. 1 for FA1.txt).
    """
    filename = f"FA{fa_number}.txt"
    filepath = f"data/{filename}"

    if not os.path.isfile(filepath):
        print(f"[SKIP] {filepath} not found.")
        return

    os.makedirs(TRACE_DIR, exist_ok=True)
    trace_path = f"{TRACE_DIR}FA{fa_number}.txt"

    # Save the original stdout before redirecting to the trace file.
    original_stdout = sys.stdout
    with open(trace_path, 'w', encoding='utf-8') as f:
        sys.stdout = f
        try:
            _run_pipeline(filename, fa_number)
        finally:
            # Always restore stdout, even if the pipeline raises an exception.
            sys.stdout = original_stdout

    print(f"[OK] Trace written: {trace_path}")


def _run_pipeline(filename: str, fa_number: int):
    """
    Run the full automaton pipeline and print all results to stdout.

    This function is called with stdout already redirected to a trace file.
    It covers all steps required by the project specification:
        1. Load and display the automaton.
        2. Check standardness, determinism, and completeness.
        3. Standardize if needed.
        4. Determinize and complete to obtain a CDFA.
        5. Minimize the CDFA.
        6. Test word recognition on the CDFA.
        7. Build and display the complementary automaton.

    Args:
        filename (str): The automaton file name (e.g. "FA5.txt").
        fa_number (int): The automaton index, used only for display purposes.
    """
    sep = "=" * 60

    print(sep)
    print(f"  AUTOMATON FA{fa_number}")
    print(sep)

    # ── 1. Load and display ─────────────────────────────────────
    print("\n[1] LOADING AND DISPLAY")
    print("-" * 40)
    fa = Automaton(filename)
    fa.display_automaton()

    # ── 2. Property checks ──────────────────────────────────────
    print("\n[2] PROPERTIES")
    print("-" * 40)

    is_std, msg_std = fa.is_standard()
    print(f"Standard     : {'YES' if is_std else 'NO'} — {msg_std.strip()}")

    is_det, msg_det = fa.is_deterministic()
    print(f"Deterministic: {'YES' if is_det else 'NO'} — {msg_det.strip()}")

    # is_complete prints its own per-state messages, so we just capture the bool.
    print("Complete     : ", end="")
    is_cpl,msg = fa.is_complete()
    if is_cpl:
        print("YES")
    else:
        print("NO (see missing transitions below)\n")
        print(msg)

    # ── 3. Standardization ──────────────────────────────────────
    print("\n[3] STANDARDIZATION")
    print("-" * 40)
    if not is_std:
        fa.standardization()
        print("Automaton after standardization:")
        fa.display_automaton()
    else:
        print("Already standard — no action taken.")

    # ── 4. Determinization and completion ───────────────────────
    print("\n[4] DETERMINIZATION AND COMPLETION")
    print("-" * 40)

    # Re-check after potential standardization, since that may have changed the FA.
    is_det2, _ = fa.is_deterministic()
    is_cpl2,_ = fa.is_complete()

    if is_det2 and is_cpl2:
        print("Already a CDFA — no action taken.")
        cdfa = fa
    elif is_det2 and not is_cpl2:
        print("Deterministic but incomplete — applying completion.")
        fa.completion()
        cdfa = fa
    else:
        print("Non-deterministic — applying determinization then completion.")
        fa.determinize()
        fa.completion()
        cdfa = fa

    print("\nResulting CDFA:")
    cdfa.display_automaton()

    # ── 5. Minimization ─────────────────────────────────────────
    print("\n[5] MINIMIZATION")
    print("-" * 40)
    # Work on a deep copy so the CDFA remains intact for the steps below.
    mfa = copy.deepcopy(cdfa)
    mfa.minimisation()

    # ── 6. Word recognition ─────────────────────────────────────
    print("\n[6] WORD RECOGNITION")
    print("-" * 40)
    print(f"Words tested: {TEST_WORDS}")
    print("(tested on the CDFA)\n")
    for word in TEST_WORDS:
        cdfa.recognize_word(word)

    # ── 7. Complementary automaton ──────────────────────────────
    print("\n[7] COMPLEMENTARY AUTOMATON")
    print("-" * 40)
    # Build the complement by swapping final and non-final states.
    # The CDFA is used as the base (it is already complete and deterministic).
    print("Base automaton used: CDFA")
    comp = cdfa.complementary_automaton()

    print("Complementary automaton (final states inverted):")
    comp.display_automaton()
    print("\nWords tested on the complementary automaton:")
    for word in TEST_WORDS:
        comp.recognize_word(word)

    print(f"\n{sep}")
    print(f"  END — FA{fa_number}")
    print(sep)


def generate_all_traces(fa_list: list[int]):
    """
    Generate execution traces for a list of automaton indices.

    Iterates over each index in fa_list and calls generate_trace().
    Automata whose files do not exist are skipped with a warning.

    Args:
        fa_list (list[int]): List of automaton indices to process.
    """
    print(f"Generating {len(fa_list)} trace(s)...\n")
    for n in fa_list:
        generate_trace(n)
    print("\nDone.")


if __name__ == "__main__":
    # Launch the generation of the execution trace for all the finite automata
    all_numbers = list(range(1, 45))
    generate_all_traces(all_numbers)





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
    ("11", "Check word recognition for complementary automaton"),
    ("12", "Run full pipeline  (display → complete → minimise → export)"),
    ("─",  "─" * 40),
    ("l",  "Load a different automaton"),
    ("q",  "Quit"),
]
