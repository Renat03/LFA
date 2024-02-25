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


        # print(f"states: {states}")
        # print(f"alphabet: {alphabet}")
        # print(f"transition function: {transition_function}")
        # print(f"start: {start}")
        # print(f"accept: {accept}")


        return FiniteAutomaton(states, alphabet, transition_function, start, accept)


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


s = 'S'
vn = ['S', 'L', 'B']
vt = ['a', 'b', 'c']
p = {
    'S': ['aB'],
    'B': ['bB', 'cL'],
    'L': ['cL', 'aS', 'b']
}

grammar = Grammar(vn, vt, p, s)
generated_words = grammar.generate_strings(5)
print("Generated words:")
print(generated_words)

print("\n\nCheck if the words are accepted:")
for i in generated_words:
    print(f"{i} - {grammar.to_finite_automaton().string_belong_to_language(i)}")

print("\n\nChecking random words:")
random_words = ['check', 'word', 'cab', 'abc', 'acb']
for i in random_words:
    print(f"{i} - {grammar.to_finite_automaton().string_belong_to_language(i)}")
