## imports

from automaton import *

## program

testFile = input("Enter the number of the file you want to test:\n")

fa = Automaton(testFile+".txt")

fa.display_automaton()
print(fa.transitions)
#fa.is_deterministic()
#fa.is_complete()
fa.completion()

