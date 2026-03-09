from encodings.punycode import *


class Automaton:
    def __init__(self,filename):
        self.filename = filename
        self.alphabet = []
        self.states = []
        self.initialStates = []
        self.finalStates = []
        self.transitions = dict()
        self.read_automaton_from_file()

    def read_automaton_from_file(self):
        with open(self.filename) as f:
            lines = f.readlines()

        alphabetSize = int(lines[0])
        for i in range(alphabetSize):
            self.alphabet.append(chr(ord('a') + i))

        nbStates = int(lines[1])
        for i in range(nbStates):
            self.states.append(str(i))

        self.initialStates = lines[2].split()[1:]

        self.finalStates = lines[3].split()[1:]

        nbTransitions = int(lines[4])

        for i in range(5, 5 + nbTransitions):
            line = lines[i]

            source = line[0]
            symbol = line[1]
            target = line[2]
            if source not in self.transitions.keys():
                self.transitions[source] = {}
                self.transitions[source][symbol] = [target]
            else:
                if symbol not in self.transitions[source].keys():
                    self.transitions[source][symbol] = [target]
                else:
                    self.transitions[source][symbol].append(target)

        for state in self.states:
            if str(state) not in self.transitions.keys():
                self.transitions[str(state)] = {}

    def display_automaton(self):
        transitionTable = []
        transitionTable.append([' ', ' '] + self.alphabet)

        for state in self.states:
            if state in self.initialStates and state in self.finalStates:
                table = ['<-->', state]
            elif state in self.initialStates:
                table = ['-->', state]
            elif state in self.finalStates:
                table = ['<--', state]
            else:
                table = [' ', state]

            for alphabet in self.alphabet:
                if alphabet in self.transitions[state]:
                    table.append(",".join(self.transitions[state][alphabet]))
                else:
                    table.append('---')

            transitionTable.append(table)

        for line in transitionTable:
            for value in line:
                print(f"{value:^{6}}", end="")
            print()














