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
        transition_table = [[' ', ' '] + self.alphabet]

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

            transition_table.append(table)

        for line in transition_table:
            for value in line:
                print(f"{value:^{6}}", end="")
            print()


    def is_standard(self):
        if len(self.initialStates) > 1 or len(self.initialStates) == 0:
            print('This automaton is not standard because there is not only one initial state.\n')
            return False

        for source in self.transitions:
            for symbol in self.transitions[source]:
                if self.initialStates[0] in self.transitions[source][symbol]:
                    print('This automaton is not standard because there are transitions arriving at the initial state.\n')
                    return False

        print('This automaton is standard.\n')
        return True

    def standardization(self):
        newInitialState = str(len(self.states))

        for initialState in self.initialStates:
            if initialState in self.finalStates and newInitialState not in self.finalStates:
                self.finalStates.append(newInitialState)

        self.transitions[newInitialState] = {}

        for initialState in self.initialStates:
            if initialState in self.transitions:
                for symbol in self.transitions[initialState]:
                    if symbol not in self.transitions[newInitialState]:
                        self.transitions[newInitialState][symbol] = self.transitions[initialState][symbol].copy()
                    else:
                        for target in self.transitions[initialState][symbol]:
                            if target not in self.transitions[newInitialState][symbol]:
                                self.transitions[newInitialState][symbol].append(target)

        self.states.append(newInitialState)
        self.initialStates = [newInitialState]




    def is_deterministic(self):
        if len(self.initialStates) > 1:
            print('This automata is not deterministic because it has more than one initial state.\n')
            return False
        for state in self.states:
            for alphabet in self.alphabet:
                if alphabet in self.transitions[state]:
                    nb_transitions = len(self.transitions[state][alphabet])
                    if nb_transitions > 1:
                        print(f'This automata is not deterministic because the state {state} has {nb_transitions} transitions on the same letter {alphabet}:{self.transitions[state][alphabet]} \n')
                        return False
        print('This automata is deterministic.\n')
        return True



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

        for transitions in self.transitions.items():

            liste = list(self.alphabet)

            for letters in transitions[1]:
                if letters in liste:
                    liste.remove(letters)

            for letter in liste:
                transitions[1][letter] = [trash_state]

    def minimisation(self):

        previous_partitions = []
        current_partitions = [sorted(self.finalStates)]+[sorted(state for state in self.states
                                                          if state not in self.finalStates)]
        while current_partitions != previous_partitions:
            print(current_partitions,'\n')
            previous_partitions = current_partitions
            current_partitions = []
            for group in previous_partitions:
                dico = {}
                for state in group:
                    dico[state] = ''
                    for alphabet in self.alphabet:
                        if alphabet in self.transitions[state]:
                            if self.transitions[state][alphabet][0] in self.finalStates:
                                dico[state]+='1' # 1 if the transit state is terminal
                            else:
                                dico[state]+='0' # 0 if the transit state is non terminal
                        else:
                            dico[state]+='-' # - if the there is no transit state
                new_groups = {}
                for state, transitions in dico.items():
                    if transitions not in new_groups:
                        new_groups[transitions] = []
                    new_groups[transitions].append(state)
                for grp in new_groups:
                    current_partitions.append(sorted(new_groups[grp]))

        transitions_table = {}
        initial_states = []
        final_states = []

        for group in current_partitions:
            is_final = False
            is_initial = False
            transitions_table["".join(group)] = {}
            for alphabet in self.alphabet:
                target_state = ''
                for state in group:
                    if state in self.finalStates:
                        is_final = True
                    if state in self.initialStates:
                        is_initial = True
                    target_state += self.transitions[state][alphabet][0]
                transitions_table["".join(group)][alphabet] =["".join(sorted(target_state))]
            if is_final:
                final_states.append("".join(group))
            if is_initial:
                initial_states.append("".join(group))

        print(f'The transitions table is: {transitions_table}\n'
              f'The initial states is: {initial_states}\n'
              f'The final states is: {final_states}\n')
        self.transitions = transitions_table
        self.initialStates = initial_states
        self.finalStates = final_states
        self.states = self.transitions.keys()

    def create_mermaid_graph_from_automaton(self, filename=None):
        if filename is None:
            filename = self.filename.split('.')[0]
        with open(filename+".mmd",'w') as f:
            f.write('---\n'
                    'config:\n'
                    '   theme: neo\n'
                    '   look: neo\n'
                    '   layout: elk\n'
                    '---\n'
                    '\n'
                    'flowchart LR\n')
            for state in self.states:
                if state in self.finalStates:
                    string =f'{state}((({state})))\n'
                else:
                    string =f'{state}(({state}))\n'
                f.write(string)

            for source_state in self.transitions:
                for alphabet in self.transitions[source_state]:
                    for target_state in self.transitions[source_state][alphabet]:
                        f.write(f'{source_state} -->|{alphabet}|{target_state}\n')

            for i,state in enumerate(self.initialStates):
                f.write(f'start{i}(( ))--> {state}\n')

    def read_word(self):
        word = str(input(""))
        return word

    def recognize_word(self, word):
        current_sates = set(self.initialStates)

        for symbol in word:

            if symbol not in self.alphabet:
                print(f"Symbol {symbol} is not in alphabet : {self.alphabet}")
                return False

            next_states = set()
            for state in current_sates:
                if symbol in self.transitions[state]:
                    next_states.update(self.transitions[state][symbol])

            current_sates = next_states
            if not current_sates:
                return False

        for state in current_sates:
            if state in self.finalStates:
                return True











