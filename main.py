## imports

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

        if choice == 'q':
            clear()
            print(f"\n  {CYAN}Goodbye!{RESET}\n")
            sys.exit(0)

        elif choice == 'l':
            clear()
            banner()
            automaton = load_automaton()

        elif automaton is None:
            clear()
            banner()
            error("No automaton loaded. Use [l] first.")
            pause()

        elif choice == '1':
            clear()
            banner()
            action_display(automaton)
        elif choice == '2':
            clear()
            banner()
            action_is_deterministic(automaton)
        elif choice == '3':
            clear()
            banner()
            action_is_complete(automaton)
        elif choice == '4':
            clear()
            banner()
            action_is_standard(automaton)
        elif choice == '5':
            clear()
            banner()
            action_determination(automaton)
        elif choice == '6':
            clear()
            banner()
            action_completion(automaton)
        elif choice == '7':
            clear()
            banner()
            action_standardization(automaton)
        elif choice == '8':
            clear()
            banner()
            action_minimisation(automaton)
        elif choice == '9':
            clear()
            banner()
            action_mermaid(automaton)
        elif choice == '10':
            clear()
            banner()
            action_full_pipeline(automaton)
        else:
            clear()
            banner()
            error(f"Unknown option '{choice}'. Please try again.")
            pause()


if __name__ == "__main__":
    main()
