from encodings.punycode import *


class Automaton:
    def __init__(self):
        self.alphabet = []
        self.states = []
        self.initialStates = []
        self.finalStates = []
        self.transitions = dict()


def read_automaton_from_file(filename):
    fa = Automaton()

    with open(filename) as f:
        lines = f.readlines()

    alphabetSize = int(lines[0])
    for i in range(alphabetSize):
        fa.alphabet.append(chr(ord('a')+i))

    nbStates = int(lines[1])
    for i in range(nbStates):
        fa.states.append(str(i))

    fa.initialStates = lines[2].split()[1:]

    fa.finalStates = lines[3].split()[1:]

    nbTransitions = int(lines[4])

    for i in range(5,5+nbTransitions):
        line = lines[i]

        source = line[0]
        symbol = line[1]
        target = line[2]

        key = (source, symbol)

        if key not in fa.transitions:
            fa.transitions[key] = []

        fa.transitions[key].append(target)

    return fa


def display_automaton(fa):
    transitionTable = []
    transitionTable.append([' ',' '] + fa.alphabet)

    for state in fa.states:
        if state in fa.initialStates and state in fa.finalStates:
            table = ['<-->',state]
        elif state in fa.initialStates:
            table = ['-->',state]
        elif state in fa.finalStates:
            table = ['<--',state]
        else:
            table = [' ',state]

        for symbol in fa.alphabet:
            if (state, symbol) in fa.transitions:
                table.append(",".join(fa.transitions[(state, symbol)]))
            else:
                table.append('---')

        transitionTable.append(table)

    for line in transitionTable:
        for value in line:
            print(f"{value:^{6}}", end="")
        print()










