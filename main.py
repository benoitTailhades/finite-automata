## imports

from automaton import *

## program

testFile = input("Enter the number of the file you want to test:\n")

fa = Automaton("FA"+testFile+".txt")
fa.display_automaton()

print(fa.transitions)

fa.create_mermaid_graph_from_automaton()


if fa.is_complete() and fa.is_deterministic():
    fa.minimisation()
    fa.create_mermaid_graph_from_automaton(testFile+"_minimisation")



