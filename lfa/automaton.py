from collections import defaultdict
from graphviz import Digraph


class FiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start = start
        self.accept = accept

    def string_belong_to_language(self, word):
        current_state = self.start
        for char in word:
            if char in self.transition_function[current_state]:
                current_state = self.transition_function[current_state][char]
            else:
                return False
        return current_state in self.accept

    def to_regular_grammar(self):
        from grammar import Grammar
        vn = [state for state in self.states if state != 'X']
        vt = self.alphabet  # Terminals
        p = {state: [] for state in vn}  # Production rules
        s = self.start

        for state, transitions in self.transition_function.items():
            p[state] = []
            for input_symbol, next_states in transitions.items():
                for next_state in next_states:
                    if next_state in self.accept:
                        p[state].append(input_symbol + next_state)
                        p[state].append(input_symbol)
                    else:
                        p[state].append(input_symbol + next_state)

        return Grammar(vn, vt, p, s)

    def is_deterministic(self):
        for state, transitions in self.transition_function.items():
            for symbol, next_states in transitions.items():
                if len(next_states) > 1:
                    return False
        return True

    def to_dfa(self):
        initial_dfa_state = frozenset([self.start])
        dfa_transitions = defaultdict(dict)
        dfa_states = {initial_dfa_state}
        states_to_process = [initial_dfa_state]
        dfa_accept_states = set()

        while states_to_process:
            current_dfa_state = states_to_process.pop()
            for symbol in self.alphabet:
                next_states_set = frozenset(
                    sum([self.transition_function[nfa_state].get(symbol, []) for nfa_state in current_dfa_state], [])
                )
                if next_states_set:
                    dfa_transitions[current_dfa_state][symbol] = next_states_set
                    if next_states_set not in dfa_states:
                        dfa_states.add(next_states_set)
                        states_to_process.append(next_states_set)
                    if any(state in self.accept for state in next_states_set):
                        dfa_accept_states.add(next_states_set)

        state_names = {state: 'q{}'.format(i) for i, state in enumerate(dfa_states)}
        dfa_start = state_names[initial_dfa_state]
        dfa_states_named = [state_names[state] for state in dfa_states]
        dfa_accept_named = [state_names[state] for state in dfa_accept_states]

        dfa_transitions_named = {}
        for state, transitions in dfa_transitions.items():
            transition_dict = {}
            for symbol, next_state_set in transitions.items():
                transition_dict[symbol] = [state_names[next_state_set]]
            dfa_transitions_named[state_names[state]] = transition_dict

        return FiniteAutomaton(dfa_states_named, self.alphabet, dfa_transitions_named, dfa_start, dfa_accept_named)

    def visualize(self, filename='finite_automaton'):
        dot = Digraph()

        for state in self.states:
            if state in self.accept:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')

        dot.node('', shape='none')
        dot.edge('', self.start)

        for state, transitions in self.transition_function.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    dot.edge(state, next_state, label=symbol)
        dot.render(filename, format='png', cleanup=True)
