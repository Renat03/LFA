import random


class Grammar:
    def __init__(self, vn, vt, p, s):
        self.non_terminals = vn
        self.terminals = vt
        self.rules = p
        self.start_symbol = s

    def generate_strings(self):
        words = []
        while len(words) != 5:
            str = "S"
            while str.lower() != str:
                str = str.replace(str[len(str) - 1],
                                  self.rules[str[len(str) - 1]][random.randint(0, len(self.rules[str[len(str) - 1]]) - 1)])
            if str not in words:
                words.append(str)
        return words

    def to_automaton(self):
        states = self.non_terminals + ['X']
        alphabet = self.terminals
        transition_function = {}
        transition_function['X'] = {}
        start = self.start_symbol
        accept = ['X']

        for non_terminal in self.non_terminals:
            transition_function[non_terminal] = {}
            for production in self.rules.get(non_terminal, []):
                if len(production) == 1:
                    transition_function[non_terminal][production] = 'X'
                elif len(production) == 2:
                    transition_function[non_terminal][production[0]] = production[1]

        return FiniteAutomaton(states, alphabet, transition_function, start, accept)


class FiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start = start
        self.accept = accept

    def check(self, word):
        current_state = self.start
        for char in word:
            if char in self.transition_function.get(current_state, {}):
                current_state = self.transition_function[current_state][char]
            else:
                return False
        return current_state in self.accept


if __name__ == "__main__":
    s = 'S'
    vn = ['S', 'L', 'B']
    vt = ['a', 'b', 'c']
    p = {
        'S': ['aB'],
        'B': ['bB', 'cL'],
        'L': ['cL', 'aS', 'b']
    }

    grammar = Grammar(vn, vt, p, s)
    generated_words = grammar.generate_strings()
    print("Generated words:")
    print(generated_words)

    print("\nCheck if the words are accepted:")
    for i in generated_words:
        print(f"{i} - {grammar.to_automaton().check(i)}")

    print("\nChecking random words:")
    random_words = ['check', 'word', 'cab']
    for i in random_words:
        print(f"{i} - {grammar.to_automaton().check(i)}")
