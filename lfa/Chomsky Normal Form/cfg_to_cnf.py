import unittest


class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def remove_start_symbol_from_rhs(self):
        if any(self.start_symbol in production for values in self.productions.values() for production in values):
            new_start_symbol = 'X'
            self.productions[new_start_symbol] = [self.start_symbol]
            self.start_symbol = new_start_symbol
            self.non_terminals.append(new_start_symbol)

    def create_new_productions(self, production, symbol):
        return [production[:i] + production[i+1:] for i in range(len(production)) if production[i] == symbol]

    def eliminate_null_productions(self):
        null_producing_symbols = {key for key, values in self.productions.items() if 'ε' in values}
        for symbol in null_producing_symbols:
            self.productions[symbol].remove('ε')
            for key, values in list(self.productions.items()):
                new_productions = [new_prod for production in values if symbol in production for new_prod in self.create_new_productions(production, symbol)]
                self.productions[key].extend(new_prod for new_prod in new_productions if new_prod not in values)

    def eliminate_unit_productions(self):
        changes = True
        while changes:
            changes = False
            for key, values in list(self.productions.items()):
                unit_productions = [prod for prod in values if prod in self.non_terminals and prod != key]
                for production in unit_productions:
                    changes = True
                    values.remove(production)
                    values.extend(new_prod for new_prod in self.productions[production] if new_prod not in values)

    def eliminate_inaccessible_symbols(self):
        accessible = {self.start_symbol}
        queue = [self.start_symbol]
        while queue:
            current = queue.pop(0)
            for production in self.productions.get(current, []):
                for symbol in production:
                    if symbol in self.non_terminals and symbol not in accessible:
                        accessible.add(symbol)
                        queue.append(symbol)

        self.non_terminals = [nt for nt in self.non_terminals if nt in accessible]
        self.productions = {key: values for key, values in self.productions.items() if key in accessible}

    def substitute_terminals_in_non_single_productions(self):
        terminal_to_nonterminal = {}
        for key, productions in list(self.productions.items()):
            for production in productions:
                if len(production) > 1:
                    new_production = ''
                    for char in production:
                        if char in self.terminals:
                            if char not in terminal_to_nonterminal:
                                new_nonterminal = next(chr(i) for i in range(65, 91) if chr(i) not in self.non_terminals)
                                self.non_terminals.append(new_nonterminal)
                                terminal_to_nonterminal[char] = new_nonterminal
                                self.productions[new_nonterminal] = [char]
                            new_production += terminal_to_nonterminal[char]
                        else:
                            new_production += char
                    productions[productions.index(production)] = new_production

    def shorten_productions(self):
        binary_nonterminal_map = {}
        for key, productions in list(self.productions.items()):
            for production in productions:
                if len(production) > 2:
                    new_production = production
                    while len(new_production) > 2:
                        last_two = new_production[-2:]
                        if last_two not in binary_nonterminal_map:
                            new_nonterminal = next(chr(i) for i in range(65, 91) if chr(i) not in self.non_terminals)
                            self.non_terminals.append(new_nonterminal)
                            binary_nonterminal_map[last_two] = new_nonterminal
                            self.productions[new_nonterminal] = [last_two]
                        new_production = new_production[:-2] + binary_nonterminal_map[last_two]
                    productions[productions.index(production)] = new_production

    def convert_to_cnf(self):
        self.remove_start_symbol_from_rhs()
        self.eliminate_null_productions()
        self.eliminate_unit_productions()
        self.eliminate_inaccessible_symbols()
        self.substitute_terminals_in_non_single_productions()
        self.shorten_productions()


class TestGrammarMethods(unittest.TestCase):
    def setUp(self):
        self.grammar = Grammar(['S', 'A', 'B', 'D'], 
            ['a', 'b', 'd'], 
        {
            'S': ['dB', 'AB'],
            'A': ['d', 'dS', 'ε', 'aAaAb'],
            'B': ['a', 'aS', 'A'],
            'D': ['Aba']
        }, 
        'S')

    def test_remove_start_symbol_from_rhs(self):
        self.grammar.remove_start_symbol_from_rhs()
        self.assertNotIn(self.grammar.start_symbol, [prod for values in self.grammar.productions.values() for prod in values])
        self.assertIn('X', self.grammar.non_terminals)

    def test_eliminate_null_productions(self):
        self.grammar.eliminate_null_productions()
        for values in self.grammar.productions.values():
            self.assertNotIn('ε', values)

    def test_eliminate_unit_productions(self):
        self.grammar.eliminate_unit_productions()
        for values in self.grammar.productions.values():
            for prod in values:
                self.assertFalse(len(prod) == 1 and prod.isupper())

    def test_shorten_production(self):
        self.grammar.substitute_terminals_in_non_single_productions()
        self.grammar.shorten_productions()
        for values in self.grammar.productions.values():
            for prod in values:
                self.assertTrue(len(prod) <= 2)

if __name__ == '__main__':
    unittest.main()

#non_terminals = ['S', 'A', 'B', 'D']
#terminals = ['a', 'b', 'd']
#productions = {
    #'S': ['dB', 'AB'],
    #'A': ['d', 'dS', 'ε', 'aAaAb'],
    #'B': ['a', 'aS', 'A'],
    #'D': ['Aba']
#}
#start_symbol = 'S'

#grammar = Grammar(non_terminals, terminals, productions, start_symbol)
#grammar.convert_to_cnf()

#print('Non-terminals:', grammar.non_terminals)
#print('Terminals:', grammar.terminals)
#print('Productions:')
#for key, value in grammar.productions.items():
    #print(f'{key} -> {value}')
#print('Start Symbol: ', grammar.start_symbol, '\n')
