import re
import enum
from graphviz import Digraph

class TokenType(enum.Enum):
    WHITESPACE = 1
    COMMENT = 2
    KEYWORD = 3
    IDENTIFIER = 4
    OPERATOR = 5
    LITERAL = 6
    PUNCTUATOR = 7

def lexer(cpp):
    tokens = []
    while cpp:
        cpp = cpp.lstrip()
        match_found = False
        for token_type, token_regex in TOKENS:
            regex = re.compile(token_regex)
            match = regex.match(cpp)
            if match:
                value = match.group(0).strip()
                if token_type != TokenType.WHITESPACE:
                    tokens.append((token_type, value))
                cpp = cpp[match.end():]
                match_found = True
                break
        if not match_found:
            raise SyntaxError(f'Unknown C++ syntax: {cpp}')
    return tokens

class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        return f"{self.type}({self.value}, {self.children})"

def parse(tokens):
    root = ASTNode("Program")
    current_node = root
    stack = []

    i = 0
    while i < len(tokens):
        token_type, value = tokens[i]
        if token_type == TokenType.KEYWORD and value in ["int", "char", "float", "double"]:
            if i + 1 < len(tokens) and tokens[i + 1][0] == TokenType.IDENTIFIER:
                declaration_node = ASTNode("Declaration", value=value + " " + tokens[i + 1][1])
                current_node.children.append(declaration_node)
                i += 1
        elif value == '{':
            stack.append(current_node)
            current_node = ASTNode("Block")
            stack[-1].children.append(current_node)
        elif value == '}':
            current_node = stack.pop()
        elif value == '=':
            if i + 1 < len(tokens) and tokens[i + 1][0] == TokenType.LITERAL:
                assignment_node = ASTNode("Assignment", value=tokens[i - 1][1] + " = " + tokens[i + 1][1])
                current_node.children.append(assignment_node)
                i += 1 
        i += 1

    return root


def add_nodes_edges(tree, graph=None):
    if graph is None:
        graph = Digraph()
        graph.node(name=str(id(tree)), label=f'{tree.type}({tree.value})')

    for child in tree.children:
        graph.node(name=str(id(child)), label=f'{child.type}({child.value})')
        graph.edge(str(id(tree)), str(id(child)))
        add_nodes_edges(child, graph)

    return graph

TOKENS = [
    (TokenType.WHITESPACE, r'\s+'),
    (TokenType.COMMENT, r'//.*|/\*[^*]*\*+([^/*][^*]*\*+)*\/'),
    (TokenType.KEYWORD, r'\b(int|char|float|double|return|if|else|while|for)\b'),
    (TokenType.IDENTIFIER, r'\b[_a-zA-Z][_a-zA-Z0-9]*\b'),
    (TokenType.LITERAL, r'\b\d+(\.\d+)?\b'),
    (TokenType.OPERATOR, r'[+\-*/=<>!&|^]+'),
    (TokenType.PUNCTUATOR, r'[{}();,]')
]

cpp_code = """
int main() {
    int x = 10;
    int y;
    y = 20;
    return 0;
}"""

tokens = lexer(cpp_code)
ast = parse(tokens)
graph = add_nodes_edges(ast)
graph.render('cpp_ast', format='png', view=True)
