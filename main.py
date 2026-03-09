## imports

from automaton import *

## program

testFile = input("Enter the number of the file you want to test:\n")

fa = Automaton(testFile+".txt")
print(fa.transitions)
fa.display_automaton()


