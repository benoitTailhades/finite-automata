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

    def is_deterministic(self):

        if (len(self.initialStates)) > 1:
            print("\nAutomaton non deterministic:")
            print("Reason: More than one entry\n")


        for transition in self.transitions.items():
            for items in transition[1].items():
                if len(items[1]) > 1:
                    print("The letter '" + items[0] + "' points to " + items[1][0] + " and " + items[1][1])

    def is_complete(self):
        i = 0
        for transitions in self.transitions.items():
            if len(transitions[1]) != len(self.alphabet):
                print("There is " + str(len(self.alphabet)-len(transitions[1])) + " transition(s) missing on the state line " + str(int(transitions[0])+1))
                i +=1
        return i==0

    def completion(self):
        if self.is_complete():
            print("The automaton is already complete")
            return

        trash_state = "P"

        if trash_state not in self.states:
            self.states.append(trash_state)
            self.transitions[trash_state] = {}

        for letters in self.alphabet:
            self.transitions[trash_state][letters] = [trash_state]

        for state in self.states:
            if state == trash_state:
                continue

            for symbol in self.alphabet:
                if symbol not in self.transitions[state] or not self.transitions[state][symbol]:
                    self.transitions[state][symbol] = [trash_state]



