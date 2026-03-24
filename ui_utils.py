import os

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