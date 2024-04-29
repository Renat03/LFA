import random


class Grammar:
    def __init__(self, vn, vt, p, s):
        self.non_terminals = vn
        self.terminals = vt
        self.rules = p
        self.start_symbol = s

    def generate_strings(self, count):
        words = []
        while len(words) != count:
            word = "S"
            while word.lower() != word:
                random_transition = random.randint(0, len(self.rules[word[-1]]) - 1)
                word = word.replace(word[-1], self.rules[word[-1]][random_transition])
            if word not in words:
                words.append(word)
        return words

    def to_finite_automaton(self):
        from automaton import FiniteAutomaton
        states = self.non_terminals + ['X']
        alphabet = self.terminals
        transition_function = {'X': {}}
        start = self.start_symbol
        accept = ['X']

        for non_terminal in self.non_terminals:
            transition_function[non_terminal] = {}
            for production in self.rules[non_terminal]:
                if len(production) == 1:
                    transition_function[non_terminal][production] = 'X'
                elif len(production) == 2:
                    transition_function[non_terminal][production[0]] = production[1]

        return FiniteAutomaton(states, alphabet, transition_function, start, accept)

    def classify(self):
        is_regular = True
        is_context_free = True
        is_context_sensitive = True

        for lhs, rhs_list in self.rules.items():
            for rhs in rhs_list:
                if not (len(rhs) == 1 and rhs in self.terminals) and not \
                        (len(rhs) == 2 and ((rhs[0] in self.terminals and rhs[1] in self.non_terminals) or
                                            (rhs[0] in self.non_terminals and rhs[1] in self.terminals))):
                    is_regular = False
                if lhs not in self.non_terminals:
                    is_context_free = False
                if len(rhs) < len(lhs):
                    is_context_sensitive = False

        if is_regular:
            return "Type 3 (Regular)"
        elif is_context_free:
            return "Type 2 (Context-free)"
        elif is_context_sensitive:
            return "Type 1 (Context-sensitive)"
        else:
            return "Type 0 (Recursively enumerable)"

