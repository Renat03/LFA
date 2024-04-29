class BreakFromLoops(Exception):
    pass


class Grammar():
    def __init__(self, vn, vt, p, s):
        self.Vn = vn
        self.Vt = vt
        self.P = p
        self.S = s

    def print_grammar(self):
        print('Vn:', self.Vn)
        print('Vt:', self.Vt)
        print('P:')
        for key, value in self.P.items():
            print(f'{key} -> {value}')
        print('S: ', self.S, '\n')

    def cfg_to_cnf(self):
        self.start_symbol_rhs_removal()
        self.remove_null_productions()
        self.remove_unit_productions()
        self.remove_inaccessible_symbols()
        self.replace_terminals_with_nonterminals()
        self.reduce_production_length()

    def start_symbol_rhs_removal(self):
        try:
            for value in self.P.values():
                for production in value:
                    for character in production:
                        if character == self.S:
                            raise BreakFromLoops
        except:
            new_P = {'X': [self.S]}
            new_P.update(self.P)
            self.P = new_P
            self.S = 'X'
            self.Vn.append(self.S)

    def create_new_productions(self, production, character):
        results = []
        for i in range(len(production)):
            if production[i] == character:
                new_production = production[:i] + production[i+1:]
                results.append(new_production)
        return results

    def remove_null_productions(self):
        count_null = 0
        null_prods = []
        for key, value in self.P.items():
            for production in value:
                if production == 'ε':
                    count_null += 1
                    null_prods.append(key)
                    value.remove(production)
        for i in range(count_null):
            new_P = self.P
            for key, value in self.P.items():
                for production in value:
                    for character in production:
                        if character == null_prods[i]:
                            new_productions = self.create_new_productions(production, null_prods[i])
                            for j in new_productions:
                                if j not in new_P[key]:
                                    new_P[key].append(j)
                            break
            self.P = new_P

    def remove_unit_productions(self):
        for key, value in self.P.items():
            for production in value:
                if key == production:
                    self.P[key].remove(production)
        changes = True
        while changes:
            changes = False
            for key, value in self.P.items():
                for production in value:
                    if production in self.Vn:
                        changes = True
                        self.P[key].remove(production)
                        for prod in self.P[production]:
                            if prod not in self.P[key]:
                                self.P[key].append(prod)

    def remove_inaccessible_symbols(self):
        accessible = set([self.S])
        queue = [self.S]

        while queue:
            current = queue.pop(0)
            for production in self.P.get(current, []):
                for symbol in production:
                    if symbol in self.Vn and symbol not in accessible:
                        accessible.add(symbol)
                        queue.append(symbol)

        self.Vn = [nt for nt in self.Vn if nt in accessible]
        for nt in list(self.P.keys()):
            if nt not in accessible:
                del self.P[nt]


    def replace_terminals_with_nonterminals(self):
        def new_nonterminal(existing):
            for char in (chr(i) for i in range(65, 91)):
                if char not in existing:
                    return char
            raise ValueError("Ran out of single-letter nonterminal symbols!")

        terminal_to_nonterminal = {}
        new_P = {}
        for key, productions in self.P.items():
            new_productions = []
            for prod in productions:
                if len(prod) > 1:
                    new_prod = ''
                    for char in prod:
                        if char in self.Vt:
                            if char not in terminal_to_nonterminal:
                                new_nt = new_nonterminal(self.Vn)
                                self.Vn.append(new_nt)
                                terminal_to_nonterminal[char] = new_nt
                                new_P[new_nt] = [char]
                            new_prod += terminal_to_nonterminal[char]
                        else:
                            new_prod += char
                    new_productions.append(new_prod)
                else:
                    new_productions.append(prod)
            new_P[key] = new_productions
        self.P.update(new_P)

    def reduce_production_length(self):
        def new_nonterminal(existing):
            for char in (chr(i) for i in range(65, 91)):
                if char not in existing:
                    return char
            raise ValueError("Ran out of single-letter nonterminal symbols!")

        existing_binaries = {}
        new_productions_dict = {}
        for key, productions in list(self.P.items()):
            new_productions = []
            for production in productions:
                if len(production) > 2:
                    while len(production) > 2:
                        last_two = production[-2:]
                        if last_two not in existing_binaries:
                            new_nt = new_nonterminal(set(self.Vn) | set(new_productions_dict.keys()))
                            self.Vn.append(new_nt)
                            new_productions_dict[new_nt] = [last_two]
                            existing_binaries[last_two] = new_nt
                        production = production[:-2] + existing_binaries[last_two]
                    new_productions.append(production)
                else:
                    new_productions.append(production)
            self.P[key] = new_productions
        self.P.update(new_productions_dict)

# Define the grammar
vn = ['S', 'A', 'B', 'D']
vt = ['a', 'b', 'd']
p = {
    'S': ['dB', 'AB'],
    'A': ['d', 'dS','ε', 'aAaAb'],
    'B': ['a', 'aS', 'A'],
    'D': ['Aba']
}
s = 'S'

# Create the Grammar object and print the CNF
grammar = Grammar(vn, vt, p, s)
grammar.cfg_to_cnf()
grammar.print_grammar()
