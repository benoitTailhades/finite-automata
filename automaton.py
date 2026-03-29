from ui_utils import error

class Automaton:
    """
    Represents a finite automaton (FA), either deterministic (DFA) or non-deterministic (NFA).

    The automaton is loaded from a text file following a specific format:
        Line 0: size of the alphabet (integer)
        Line 1: number of states (integer)
        Line 2: initial states, space-separated, first token is the count
        Line 3: final states, space-separated, first token is the count
        Line 4: number of transitions (integer)
        Lines 5+: transitions in the format "source symbol target"

    Attributes:
        LOAD_BASE_PATH (str): Base directory path for reading automaton files.
        SAVE_BASE_PATH (str): Base directory path for writing Mermaid graph files.
        filename (str): Full path to the loaded automaton file.
        alphabet (list[str]): List of symbols in the automaton's alphabet (e.g. ['a', 'b']).
        states (list[str]): List of all state names.
        initialStates (list[str]): List of initial (start) states.
        finalStates (list[str]): List of final (accepting) states.
        transitions (dict): Nested dict mapping source state -> symbol -> list of target states.
    """

    LOAD_BASE_PATH = 'data/'
    SAVE_BASE_PATH = 'mermaid_output/'

    def __init__(self, filename):
        """
        Initializes the Automaton by loading its definition from a file.

        Args:
            filename (str): Name of the file to load (relative to LOAD_BASE_PATH).
        """
        self.filename = self.LOAD_BASE_PATH + filename
        self.alphabet = []
        self.states = []
        self.initialStates = []
        self.finalStates = []
        self.transitions = dict()
        self.read_automaton_from_file()
        raw_alphabet = [list(link.keys()) for link in self.transitions.values()]
        if ["E"] in raw_alphabet:
            self.synchronize()
    def read_automaton_from_file(self):
        """
        Reads and parses the automaton definition from the file specified in self.filename.

        Populates self.alphabet, self.states, self.initialStates, self.finalStates,
        and self.transitions based on the file content.

        The alphabet is built as consecutive lowercase letters starting from 'a'
        (e.g. size 3 -> ['a', 'b', 'c']).

        States are numbered from 0 to nbStates-1 (stored as strings).

        Any state that has no outgoing transitions gets an empty dict entry
        in self.transitions to avoid KeyErrors later.
        """
        with open(self.filename) as f:
            lines = f.readlines()

        # Build alphabet: 'a', 'b', ... up to alphabetSize letters
        alphabetSize = int(lines[0])
        for i in range(alphabetSize):
            self.alphabet.append(chr(ord('a') + i))

        # Build state list: states are named "0", "1", ..., "nbStates-1"
        nbStates = int(lines[1])
        for i in range(nbStates):
            self.states.append(str(i))

        # Parse initial and final states (first token is the count, rest are state names)
        self.initialStates = lines[2].split()[1:]
        self.finalStates = lines[3].split()[1:]

        nbTransitions = int(lines[4])

        # Parse each transition line: "source symbol target"
        for i in range(5, 5 + nbTransitions):
            line = lines[i].split(" ")
            source = line[0]
            symbol = line[1]
            target = line[2].rstrip("\n")  # Strip trailing newline

            # Build the nested transitions dict
            if source not in self.transitions:
                self.transitions[source] = {symbol: [target]}
            else:
                if symbol not in self.transitions[source]:
                    self.transitions[source][symbol] = [target]
                else:
                    self.transitions[source][symbol].append(target)

        # Ensure every state has an entry in transitions (even if empty)
        for state in self.states:
            if str(state) not in self.transitions:
                self.transitions[str(state)] = {}

    def display_automaton(self):
        """
        Prints the automaton's transition table to the console.

        The first column indicates the role of each state:
            '<-->' : both initial and final
            '-->'  : initial only
            '<--'  : final only
            ' '    : regular state

        For each (state, symbol) pair, the target state(s) are shown comma-separated,
        or '---' if no transition exists.
        """

        # Build header row
        transition_table = [[' ', ' '] + self.alphabet]
        max_len = 0
        for state in self.states:
            if len(state) > max_len:
                max_len = len(state)

            # Determine state role prefix
            if state in self.initialStates and state in self.finalStates:
                table = ['<-->', state]
            elif state in self.initialStates:
                table = ['-->', state]
            elif state in self.finalStates:
                table = ['<--', state]
            else:
                table = [' ', state]

            # Fill in transition targets for each alphabet symbol
            for alphabet in self.alphabet:
                if alphabet in self.transitions[state]:
                    table.append(",".join(self.transitions[state][alphabet]))
                else:
                    table.append('---')

            transition_table.append(table)

        # Print table with fixed-width columns
        for line in transition_table:
            for value in line:
                print(f"{value:^{max(6,max_len+2)}}", end="")
            print()

    def is_standard(self)-> tuple[bool,str]:
        """
        Checks whether the automaton is standard.

        An automaton is standard if:
            1. It has exactly one initial state.
            2. No transition leads to that initial state from any other state.

        Prints a message explaining the result in both cases.

        Returns:
            bool: True if the automaton is standard, False otherwise.
        """
        if len(self.initialStates) != 1:
            msg = 'This automaton is not standard because there is not only one initial state.\n'
            return False,msg

        # Check that no transition targets the initial state
        for source in self.transitions:
            for symbol in self.transitions[source]:
                if self.initialStates[0] in self.transitions[source][symbol]:
                    msg = 'This automaton is not standard because there are transitions arriving at the initial state.\n'
                    return False,msg

        msg = 'This automaton is standard.\n'
        return True,msg

    def standardization(self):
        """
        Transforms the automaton into a standard automaton in-place.

        Creates a new initial state (named by the next available integer index)
        that merges the transitions of all existing initial states.

        If any of the original initial states was a final state, the new
        initial state is also marked as final.

        After standardization, self.initialStates contains only the new state.
        """
        print("=" * 60)
        print("STANDARDIZATION - Creating Single Initial State")
        print("=" * 60)

        print(f"Original States          : {self.states}")
        print(f"Original Initial States  : {self.initialStates}")
        print(f"Original Final States    : {self.finalStates}")
        print(f"Original Transitions     : {self.transitions}")
        print()

        # Create new initial state
        print("--- Step 1: Create new initial state ---")
        newInitialState = str(len(self.states))
        print(f"  New initial state created: '{newInitialState}'")
        print()

        # The new initial state is final if any original initial state was final
        print("--- Step 2: Check if new state is final ---")
        isFinal = False
        for initialState in self.initialStates:
            if initialState in self.finalStates and newInitialState not in self.finalStates:
                isFinal = True

        if isFinal:
            self.finalStates.append(newInitialState)
            print(f"  → New state '{newInitialState}' is FINAL")
        else:
            print(f"  → New state '{newInitialState}' is NOT final")
        print()

        # Merge all transitions from original initial states into the new one
        print("--- Step 3: Merge transitions into new initial state ---")
        self.transitions[newInitialState] = {}
        for initialState in self.initialStates:
            if initialState in self.transitions:
                for symbol in self.transitions[initialState]:
                    if symbol not in self.transitions[newInitialState]:
                        self.transitions[newInitialState][symbol] = self.transitions[initialState][symbol].copy()
                        print(f"  → We add the transition : {newInitialState} → {symbol} → {", ".join(self.transitions[initialState][symbol])}")
                    else:
                        for target in self.transitions[initialState][symbol]:
                            if target not in self.transitions[newInitialState][symbol]:
                                self.transitions[newInitialState][symbol].append(target)
                                print(f"  → We add the transition : {newInitialState} → {symbol} → {target}")
        print()

        # Update states
        self.states.append(newInitialState)
        self.initialStates = [newInitialState]

        print("=" * 60)
        print("STANDARDIZATION RESULT")
        print("=" * 60)
        print()

        print(f"New States          : {self.states}")
        print(f"New Initial States  : {self.initialStates}")
        print(f"New Final States    : {self.finalStates}")
        print(f"New Transitions     : {self.transitions}")
        self.display_automaton()

        print("=" * 60)
        print("\n ✔ Standardization complete.\n")

    def is_deterministic(self)-> tuple[bool,str]:
        """
        Checks whether the automaton is deterministic (DFA).

        An automaton is deterministic if:
            1. It has exactly one initial state.
            2. For every (state, symbol) pair, there is at most one transition.

        Prints a message explaining the result.

        Returns:
            bool: True if the automaton is deterministic, False otherwise.
            str: The message to display.
        """
        if len(self.initialStates) > 1:
            msg = 'This automata is not deterministic because it has more than one initial state.\n'
            return False,msg

        for state in self.states:
            for alphabet in self.alphabet:
                if alphabet in self.transitions[state]:
                    nb_transitions = len(self.transitions[state][alphabet])
                    if nb_transitions > 1:
                        msg = (f'This automata is not deterministic because the state {state} '
                              f'has {nb_transitions} transitions on the same letter '
                              f'{alphabet}:{self.transitions[state][alphabet]} \n')

                        return False,msg

        msg = 'This automata is deterministic.\n'
        return True ,msg

    def is_complete(self):
        """
        Checks whether the automaton is complete.

        An automaton is complete if every state has exactly one outgoing transition
        for each symbol in the alphabet.

        Prints the number of missing transitions per state if any are found.

        Returns:
            bool: True if the automaton is complete, False otherwise.
        """
        i = 0
        for transitions in self.transitions.items():
            if len(transitions[1]) != len(self.alphabet):
                print(
                    "There is " + str(len(self.alphabet) - len(transitions[1])) +
                    " transition(s) missing on the state line " + str(int(transitions[0]) + 1)
                )
                i += 1
        return i == 0

    def completion(self):
        """
        Completes the automaton in-place by adding a sink (trash) state "P".

        For every (state, symbol) pair that has no transition, a transition to the
        sink state "P" is added. The sink state itself loops on all symbols.

        If the automaton is already complete, prints a message and returns early.
        """
        if self.is_complete():
            print("The automaton is already complete")
            return

        trash_state = "P"

        # Add the sink state if not already present
        if trash_state not in self.states:
            self.states.append(trash_state)
            self.transitions[trash_state] = {}

        for transitions in self.transitions.items():
            # Find which symbols are missing for this state
            liste = list(self.alphabet)
            for letters in transitions[1]:
                if letters in liste:
                    liste.remove(letters)

            # Add missing transitions pointing to the sink state
            for letter in liste:
                transitions[1][letter] = [trash_state]

    def get_state_name(self, state_list):
        """
        Generates a canonical name for a composite state from a list of state names.

        States are sorted (numerically if all digits, lexicographically otherwise).
        If any state name has more than one character, names are joined with '.';
        otherwise they are concatenated directly.

        Args:
            state_list (list[str] or tuple[str]): Collection of state names to merge.

        Returns:
            str: A single string representing the composite state name.

        Examples:
            ['1', '2', '0'] -> "012"
            ['10', '2']     -> "10.2"
        """
        sorted_states = sorted(list(set(state_list)), key=lambda x: (not x.isdigit(),int(x) if x.isdigit() else x))
        if any(len(s) > 1 for s in sorted_states):
            return ".".join(sorted_states)
        return "".join(sorted_states)

    def determinize(self):
        """
        Converts the automaton to an equivalent DFA using the subset construction algorithm.
        Includes a detailed execution trace.
        """
        if self.is_deterministic()[0]:
            print("Automaton already deterministic.")
            return

        print("=" * 60)
        print("DETERMINIZATION - Subset Construction")
        print("=" * 60)
        print(f"Alphabet    : {self.alphabet}")
        print(f"NFA States  : {self.states}")
        print(f"NFA Initial : {self.initialStates}")
        print(f"NFA Final   : {self.finalStates}")
        print()

        new_transitions = {}
        new_states = []
        new_final_states = []

        # Initial DFA state: set of all NFA initial states
        start_set = tuple(sorted(self.initialStates))
        start_name = self.get_state_name(start_set)

        states_to_process = [start_set]
        processed_states = []
        new_states.append(start_name)

        print("--- Initialization ---")
        print(f"  Starting subset (Initial) : {list(start_set)} -> DFA State '{start_name}'")
        print()

        step = 0
        while states_to_process:
            current_set = states_to_process.pop(0)
            current_name = self.get_state_name(current_set)

            if current_set in processed_states:
                continue

            processed_states.append(current_set)

            print(f"--- Step {step}: Processing DFA state '{current_name}' ---")
            print(f"  Subset elements : {list(current_set)}")

            # Determine Role
            roles = []
            if current_name == start_name:
                roles.append("INITIAL")
            if any(s in self.finalStates for s in current_set):
                roles.append("FINAL")
                if current_name not in new_final_states:
                    new_final_states.append(current_name)

            print(f"  Role            : {', '.join(roles) if roles else 'REGULAR'}")

            new_transitions[current_name] = {}

            for char in self.alphabet:
                target_set_list = []
                # Find all reachable NFA states for this symbol
                for s in current_set:
                    if s in self.transitions and char in self.transitions[s]:
                        target_set_list.extend(self.transitions[s][char])

                # Remove duplicates and sort
                target_set = tuple(sorted(list(set(target_set_list))))

                if not target_set:
                    target_name = "P"
                    print(f"    on '{char}' -> [] (Empty set) -> leads to Sink state 'P'")
                else:
                    target_name = self.get_state_name(target_set)
                    print(f"    on '{char}' -> {list(target_set)} -> leads to DFA state '{target_name}'")

                new_transitions[current_name][char] = [target_name]

                # If this target subset is new, add it to the queue
                if target_set and target_set not in processed_states and target_set not in [s for s in
                                                                                            states_to_process]:
                    states_to_process.append(target_set)
                    if target_name not in new_states:
                        new_states.append(target_name)

            print()
            step += 1

        # Handling the sink state "P" if it was used
        if any("P" in new_transitions[s][c] for s in new_transitions for c in self.alphabet):
            if "P" not in new_states:
                print("--- Adding Sink State 'P' ---")
                new_states.append("P")
                new_transitions["P"] = {char: ["P"] for char in self.alphabet}
                print("  State 'P' added to complete the DFA.")
                print()

        # Update automaton properties
        self.states = new_states
        self.initialStates = [start_name]
        self.finalStates = new_final_states
        self.transitions = new_transitions

        print("=" * 60)
        print("DETERMINIZATION RESULT")
        print("=" * 60)
        print(f"  New States     : {list(self.states)}")
        print(f"  Initial State  : {self.initialStates}")
        print(f"  Final State(s) : {self.finalStates}")
        print(f"  Transitions    :")
        self.display_automaton()
        print("=" * 60)
        print("\n ✔ Determinization complete.\n")

    def minimisation(self):
        """
        Minimizes the automaton using the Myhill-Nerode partition refinement algorithm.

        Assumes the automaton is already a complete DFA. The algorithm iteratively
        refines a partition of states until no further splitting is possible:
            - Initial partition: {final states} and {non-final states}
            - Each iteration splits groups whose states have transitions leading to
              different groups for the same symbol.

        After convergence, each equivalence class becomes a single state in the
        minimal DFA. State names are formed by concatenating the original state names
        within the class.

        Modifies in-place: self.states, self.initialStates, self.finalStates, self.transitions.

        Prints intermediate partitions at each iteration step.
        """
        # Start with the basic partition: final vs non-final states
        previous_partitions = []
        current_partitions = (
                [sorted(self.finalStates)] +
                [sorted(state for state in self.states if state not in self.finalStates)]
        )

        print("=" * 60)
        print("MINIMISATION - Partition refinement")
        print("=" * 60)
        print(f"Alphabet : {self.alphabet}")
        print(f"States   : {self.states}")
        print(f"Final    : {self.finalStates}")
        print(f"Initial  : {self.initialStates}")
        print()
        print("--- Initialisation ---")
        print(f"  P0 (final states)     : {sorted(self.finalStates)}")
        print(f"  P1 (non-final states) : {sorted(s for s in self.states if s not in self.finalStates)}")
        print()

        iteration = 0

        # Refine partitions until stable
        while current_partitions != previous_partitions:
            print(f"--- Iteration {iteration} ---")
            print(f"  Current partition : {current_partitions}")
            previous_partitions = current_partitions
            nb_group = len(current_partitions)
            current_partitions = []

            for group in previous_partitions:
                if len(group) == 1:
                    # Singleton groups cannot be split further
                    print(f"  Group {group} -> singleton, kept as-is")
                    current_partitions.append([group[0]])
                else:
                    print(f"  Processing group {group} :")
                    # Build a signature for each state: which group each symbol leads to
                    dico = {}
                    for state in group:
                        dico[state] = ''
                        for alphabet in self.alphabet:
                            if alphabet in self.transitions[state]:
                                for grp_index in range(nb_group):
                                    if self.transitions[state][alphabet][0] in previous_partitions[grp_index]:
                                        dico[state] += str(grp_index)
                        print(f"    State {state} : signature = '{dico[state]}' ", end="")
                        for alphabet in self.alphabet:
                            if alphabet in self.transitions[state]:
                                target = self.transitions[state][alphabet][0]
                                grp = next(i for i in range(nb_group) if target in previous_partitions[i])
                                print(f"[on '{alphabet}' -> {target} (group {grp})]", end=" ")
                        print()

                    # Group states with identical signatures together
                    new_groups = {}
                    for state, sig in dico.items():
                        if sig not in new_groups:
                            new_groups[sig] = []
                        new_groups[sig].append(state)

                    if len(new_groups) == 1:
                        print(f"    => No split needed, group stays {group}")
                    else:
                        print(f"    => Split into {len(new_groups)} sub-groups :")
                        for sig, members in new_groups.items():
                            print(f"       signature '{sig}' -> {sorted(members)}")

                    for grp in new_groups:
                        current_partitions.append(sorted(new_groups[grp]))

            print(f"  New partition : {current_partitions}")
            print()
            iteration += 1

        print(f"--- Stable partition reached after {iteration} iteration(s) ---")
        print(f"  Final partition : {current_partitions}")
        print()

        # Build the minimal DFA from the final partition
        print("--- Building the minimal DFA ---")
        transitions_table = {}
        initial_states = []
        final_states = []

        # Map each original state to its equivalence class (group)
        new_states = {}
        for state in self.states:
            for group in current_partitions:
                if state in group:
                    new_states[state] = group

        print("  State mapping (original -> minimal state name) :")
        for state, group in new_states.items():
            print(f"    {state} -> '{self.get_state_name(group)}'")
        print()

        for group in current_partitions:
            is_final = False
            is_initial = False
            group_name = self.get_state_name(group)
            transitions_table[group_name] = {}
            print(f"  Building state '{group_name}' (from group {group}) :")

            for alphabet in self.alphabet:
                target_state = None
                for state in group:
                    if state in self.finalStates:
                        is_final = True
                    if state in self.initialStates:
                        is_initial = True
                    # All states in the group transition to the same equivalence class
                    new = new_states[self.transitions[state][alphabet][0]]
                    target_state = new


                target_name = self.get_state_name(target_state)
                transitions_table[group_name][alphabet] = [target_name]
                print(f"    on '{alphabet}' -> '{target_name}'")

            role = []
            if is_initial:
                initial_states.append(group_name)
                role.append("INITIAL")
            if is_final:
                final_states.append(group_name)
                role.append("FINAL")
            print(f"    Role : {', '.join(role) if role else 'regular'}")
            print()

        print("=" * 60)
        print("MINIMISATION RESULT")
        print("=" * 60)
        print(f"  States         : {list(transitions_table.keys())}")
        print(f"  Initial state  : {initial_states}")
        print(f"  Final state(s) : {final_states}")
        print(f"  Transitions    :")
        self.transitions = transitions_table
        self.initialStates = initial_states
        self.finalStates = final_states
        self.states = self.transitions.keys()
        self.display_automaton()
        print("=" * 60)
        print()

    def create_mermaid_graph_from_automaton(self, filename=None):
        """
        Exports the automaton as a Mermaid flowchart diagram to a .mmd file.

        Final states are represented with triple parentheses (((state))),
        regular states with double parentheses ((state)).
        Initial states have an invisible start node pointing to them.

        Args:
            filename (str, optional): Output filename (without extension). Defaults to
                                      the base name of the loaded automaton file.

        Output:
            Writes a .mmd file to SAVE_BASE_PATH using the Mermaid flowchart LR syntax
            with the 'neo' theme and 'elk' layout.
        """
        if filename is None:
            filename = self.filename.split('/')[1].split('.')[0]

        with open(self.SAVE_BASE_PATH + filename + ".mmd", 'w') as f:
            f.write(
                '---\n'
                'config:\n'
                '   theme: neo\n'
                '   look: neo\n'
                '   layout: elk\n'
                '---\n'
                '\n'
                'flowchart LR\n'
            )

            # Declare states: triple parens for final, double parens for regular
            for state in self.states:
                if state in self.finalStates:
                    f.write(f'{state}((({state})))\n')
                else:
                    f.write(f'{state}(({state}))\n')

            # Write all transitions
            for source_state in self.transitions:
                for alphabet in self.transitions[source_state]:
                    for target_state in self.transitions[source_state][alphabet]:
                        f.write(f'{source_state} -->|{alphabet}|{target_state}\n')

            # Add invisible start nodes pointing to each initial state
            for i, state in enumerate(self.initialStates):
                f.write(f'start{i}(( ))--> {state}\n')

    def read_word(self):
        word = str(input("Enter a word to recognize: "))
        print(f"\n[READ] Word entered: '{word}'")
        print(f"[READ] Alphabet: {self.alphabet}")
        print(f"[READ] Word length: {len(word)} symbol(s)\n")
        return word

    def recognize_word(self, word):
        print(f"[RECOGNIZE] Starting recognition of '{word}'")
        print(f"[RECOGNIZE] Initial states: {self.initialStates}")
        print(f"[RECOGNIZE] Final states:   {self.finalStates}\n")

        current_states = set(self.initialStates)

        for i, symbol in enumerate(word):
            print(f"  Step {i + 1}: reading symbol '{symbol}' from states {current_states}")

            if symbol not in self.alphabet:
                print(f"  [ERROR] Symbol '{symbol}' is not in alphabet {self.alphabet}")
                print(f"[RECOGNIZE] Result: REJECTED (invalid symbol)\n")
                return False

            next_states = set()
            for state in current_states:
                if symbol in self.transitions[state]:
                    targets = self.transitions[state][symbol]
                    print(f"    {state} --{symbol}--> {targets}")
                    next_states.update(targets)
                else:
                    print(f"    {state} --{symbol}--> (no transition)")

            current_states = next_states
            print(f"  --> Current states after step {i + 1}: {current_states}\n")

            if not current_states:
                print(f"[RECOGNIZE] Result: REJECTED (no active states remaining)\n")
                return False

        final_reached = [s for s in current_states if s in self.finalStates]
        print(f"[RECOGNIZE] End of word. Active states: {current_states}")
        print(f"[RECOGNIZE] Final states reached: {final_reached if final_reached else 'none'}")

        if final_reached:
            print(f"[RECOGNIZE] Result: ACCEPTED\n")
            return True
        else:
            print(f"[RECOGNIZE] Result: REJECTED (not in a final state)\n")
            return False

    def synchronize(self):
        print(f"[SYNC] Starting synchronization (epsilon removal)")
        print(f"[SYNC] Epsilon symbol: 'E'")
        print(f"[SYNC] Alphabet: {self.alphabet}")
        print(f"[SYNC] Initial states: {self.initialStates}")
        print(f"[SYNC] Final states:   {self.finalStates}\n")

        def epsilon_closure(states, transitions):
            closure = set(states)
            stack = list(states)
            while stack:
                state = stack.pop()
                if 'E' in transitions.get(state, {}):
                    for target in transitions[state]['E']:
                        if target not in closure:
                            print(f"    [E-closure] {state} --E--> {target} (added to closure)")
                            closure.add(target)
                            stack.append(target)
            return closure

        print(f"[SYNC] Computing epsilon-closure of initial states {self.initialStates}:")
        initial_closure = epsilon_closure(self.initialStates, self.transitions)
        print(f"[SYNC] Initial closure: {initial_closure}\n")

        visited = {}
        queue = [frozenset(initial_closure)]
        new_transitions = {}
        new_final_states = []
        new_initial_states = []

        counter = 0
        while queue:
            current_set = queue.pop(0)

            if current_set in visited:
                continue

            state_name = str(counter)
            visited[current_set] = state_name
            counter += 1
            new_transitions[state_name] = {}

            print(f"[SYNC] Processing new state '{state_name}' = {set(current_set)}")

            if frozenset(initial_closure) == current_set:
                new_initial_states.append(state_name)
                print(f"  --> '{state_name}' is an initial state")

            if any(s in self.finalStates for s in current_set):
                new_final_states.append(state_name)
                print(f"  --> '{state_name}' is a final state")

            for symbol in self.alphabet:
                reachable = set()
                for state in current_set:
                    if symbol in self.transitions.get(state, {}):
                        targets = self.transitions[state][symbol]
                        print(f"  {state} --{symbol}--> {targets}")
                        reachable.update(targets)

                if not reachable:
                    print(f"  --{symbol}--> (no transition)")
                    continue

                closed = epsilon_closure(reachable, self.transitions)
                closed_frozen = frozenset(closed)

                target_name = visited[closed_frozen] if closed_frozen in visited else str(counter)
                new_transitions[state_name][symbol] = [target_name]
                print(f"  --{symbol}--> e-closure{set(reachable)} = {set(closed)} => new state '{target_name}'")

                if closed_frozen not in visited:
                    queue.append(closed_frozen)

            print()

        self.states = list(new_transitions.keys())
        self.initialStates = new_initial_states
        self.finalStates = new_final_states
        self.transitions = new_transitions

        print(f"[SYNC] Done.")
        print(f"[SYNC] New states:        {self.states}")
        print(f"[SYNC] New initial states:{self.initialStates}")
        print(f"[SYNC] New final states:  {self.finalStates}")
        print(f"[SYNC] New transitions:   {self.transitions}\n")
        
    def complementary_automaton(self):
        if not self.is complete():
            self.completion()
        if not self.is_deterministic():
            self.determinization_and_completion()
        new_final_states = []
        for state in self.states:
            if state not in self.finalStates:
                new_final_states.append(state)
        self.finalStates = new_final_states
