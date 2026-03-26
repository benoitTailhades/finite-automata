## imports
import sys

from ui_functions import *

## program

def main():
    clear()
    banner()
    automaton: Automaton | None = None

    # Ask to load an automaton at startup
    automaton = load_automaton()

    while True:
        clear()
        banner()

        if automaton:
            print(f"  {DIM}Loaded:{RESET} {CYAN}{automaton.filename}{RESET}  "
                  f"{DIM}States:{RESET} {len(list(automaton.states))}  "
                  f"{DIM}Alphabet:{RESET} {' '.join(automaton.alphabet)}")
        else:
            warn("No automaton loaded. Press [l] to load one.")

        draw_menu(MENU_ITEMS)
        choice = prompt("Your choice:").strip().lower()

        clear()
        if choice == 'q':
            print(f"\n  {CYAN}Goodbye!{RESET}\n")
            sys.exit(0)

        else:
            banner()
            match choice:
                case 'l':
                    automaton = load_automaton()
                case _ if automaton is None:
                    error("No automaton loaded. Use [l] first.")
                    pause()
                case '1':
                    action_display(automaton)
                case '2':
                    action_is_deterministic(automaton)
                case '3':
                    action_is_complete(automaton)
                case '4':
                    action_is_standard(automaton)
                case '5':
                    action_determination(automaton)
                case '6':
                    action_completion(automaton)
                case '7':
                    action_standardization(automaton)
                case '8':
                    action_minimisation(automaton)
                case '9':
                    action_mermaid(automaton)
                case '10':
                    action_check_word(automaton)
                case '11':
                    action_full_pipeline(automaton)
                case _:
                    error(f"Unknown option '{choice}'. Please try again.")
                    pause()



if __name__ == "__main__":
    main()
