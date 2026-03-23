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

    def  is_deterministic(self):
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

    def get_state_name(self, state_list):

        sorted_states = sorted(list(set(state_list)), key=lambda x: int(x) if x.isdigit() else x)
        if any(len(s) > 1 for s in sorted_states):
            return ".".join(sorted_states)
        return "".join(sorted_states)

    def determinize(self):

        if self.is_deterministic():
            print("AUtomaton already deterministic.")
            return


        new_transitions = {}
        new_states = []
        new_final_states = []

        start_set = tuple(sorted(self.initialStates))
        start_name = self.get_state_name(start_set)

        states_to_process = [start_set]
        processed_states = []
        new_states.append(start_name)

        while states_to_process:
            current_set = states_to_process.pop(0)
            current_name = self.get_state_name(current_set)

            if current_set in processed_states:
                continue
            processed_states.append(current_set)

            if any(s in self.finalStates for s in current_set):
                if current_name not in new_final_states:
                    new_final_states.append(current_name)

            new_transitions[current_name] = {}

            for char in self.alphabet:
                target_set_list = []
                for s in current_set:
                    if s in self.transitions and char in self.transitions[s]:
                        target_set_list.extend(self.transitions[s][char])

                target_set = tuple(sorted(list(set(target_set_list))))

                if not target_set:
                    target_name = "P"
                else:
                    target_name = self.get_state_name(target_set)

                new_transitions[current_name][char] = [target_name]

                if target_set and target_set not in processed_states and target_set not in states_to_process:
                    states_to_process.append(target_set)
                    if target_name not in new_states:
                        new_states.append(target_name)

        if any(new_transitions[s][c] == ["P"] for s in new_transitions for c in self.alphabet):
            if "P" not in new_states:
                new_states.append("P")
                new_transitions["P"] = {char: ["P"] for char in self.alphabet}

        self.states = new_states
        self.initialStates = [start_name]
        self.finalStates = new_final_states
        self.transitions = new_transitions

        print(f"The determinization is over. New initial state : {self.initialStates} ")








