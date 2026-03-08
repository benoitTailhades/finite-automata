## imports

from automaton import *

## program

testFile = input("Enter the number of the file you want to test:\n")

fa = read_automaton_from_file(testFile+".txt")
display_automaton(fa)


