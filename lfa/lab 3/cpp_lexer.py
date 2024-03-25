import re
from prettytable import PrettyTable


TOKEN_TYPES = [
    ('NUMBER', r'\b\d+(\.\d*)?([eE][+-]?\d+)?\b'),
    ('KEYWORD', r'\b(auto|const|double|float|int|short|struct|break|continue|else|for|long|switch|void|case|default|char|do|if|return|static|while|namespace|using|bool|true|false|class|public|private|protected|this|throw|try|catch)\b'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('LEFT_PAREN', r'\('),
    ('RIGHT_PAREN', r'\)'),
    ('LEFT_SQUARE', r'\['),
    ('RIGHT_SQUARE', r'\]'),
    ('LEFT_CURLY', r'\{'),
    ('RIGHT_CURLY', r'\}'),
    ('LESS_THAN', r'<'),
    ('GREATER_THAN', r'>'),
    ('EQUAL', r'='),
    ('DOUBLE_EQUAL', r'=='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('ASTERISK', r'\*'),
    ('SLASH', r'/'),
    ('HASH', r'#'),
    ('DOT', r'\.'),
    ('COMMA', r','),
    ('COLON', r':'),
    ('SEMICOLON', r';'),
    ('SINGLE_QUOTE', r'\''),
    ('DOUBLE_QUOTE', r'"'),
    ('COMMENT', r'\/\/.*|\/\*(.|\n)*?\*\/'),
    ('PIPE', r'\|'),
    ('END', r'\0'),
    ('UNEXPECTED', r'.')
]


def tokenize(code):
    tokens = []
    while code:
        code = code.strip()
        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                value = match.group(0)
                tokens.append((token_type, value))
                code = code[len(value):]
                break
        else:
            raise SyntaxError(f'Illegal character: {code[0]}')
    return tokens


cpp_code = """
#include <iostream>
using namespace std;

int main() {
    for (int i = 0; i <= 10; ++i) {
        for (int j = 0; j <= 10; ++j) {
            cout << i << " * " << j << " = " << i * j << endl;
        }
        cout << "----------" << endl;
    }
    return 0;
}
"""

tokens = tokenize(cpp_code)
pt = PrettyTable()
pt.field_names = ["Token Type", "Token Value"]

for token in tokens:
    pt.add_row([token[0], token[1]])

print(pt)
