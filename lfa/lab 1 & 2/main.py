from automaton import FiniteAutomaton
from grammar import Grammar

if __name__ == '__main__':
    s = 'S'
    vn = ['S', 'L', 'B']
    vt = ['a', 'b', 'c']
    p = {
        'S': ['aB'],
        'B': ['bB', 'cL'],
        'L': ['cL', 'aS', 'b']
    }

    grammar = Grammar(vn, vt, p, s)
    #automaton = grammar.to_finite_automaton()

    # print(f"Automaton states: {automaton.states}")
    # print(f"Automaton alphabet: {automaton.alphabet}")
    # print(f"Automaton transition function: {automaton.transition_function}")
    # print(f"Automaton start: {automaton.start}")
    # print(f"Automaton accept: {automaton.accept}")
    # generated_words = grammar.generate_strings(5)
    # print("Generated words:")
    # print(generated_words)
    #
    # print("\n\nCheck if the words are accepted:")
    # for i in generated_words:
    #     print(f"{i} - {grammar.to_finite_automaton().string_belong_to_language(i)}")
    #
    # print("\n\nChecking random words:")
    # random_words = ['check', 'word', 'cab', 'abc', 'acb']
    # for i in random_words:
    #     print(f"{i} - {grammar.to_finite_automaton().string_belong_to_language(i)}")
    #
    # print()
    #print(grammar.classify())


    states = ['S', 'A', 'B', 'C']
    alphabet = ['a', 'b', 'c']
    accept = ['C']
    transition_function = {
        'S': {'a': ['A'], 'b': ['B']},
        'A': {'b': ['A', 'B']},
        'B': {'c': ['C']},
        'C': {'a': ['A']}
    }
    start = 'S'

    automaton = FiniteAutomaton(states, alphabet, transition_function, start, accept)
    # automaton.visualize('my_automaton')
    # grammar = automaton.to_regular_grammar()
    # print(grammar.rules)
    # print(f"Is the FA deterministic ? {automaton.is_deterministic()}")
    dfa = automaton.to_dfa()
    # dfa.visualize('dfa_visualize')
    # print(automaton.transition_function)
    # print(f"DFA states: {dfa.states}")
    # print(f"DFA alphabet: {dfa.alphabet}")
    # print(f"DFA transition function: {dfa.transition_function}")
    # print(f"DFA start: {dfa.start}")
    # print(f"DFA accept: {dfa.accept}")

