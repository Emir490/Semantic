from ply import lex

# -------------- Tokens Setup -------------- #
# Reserved words
reserved = {
    'var': 'VAR',
    'let': 'LET',
    'const': 'CONST',
    'if': 'IF',
    'else': 'ELSE',
    'number': 'TYPE_NUMBER',
    'string': 'TYPE_STRING',
    'boolean': 'TYPE_BOOLEAN',
    'function': 'FUNCTION',
    'return': 'RETURN'
}

# List of token names
tokens = [
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'IDENTIFIER', 'EQUALS', 'ASSIGN', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL',
    'AND', 'OR', 'NOT',
    'STRING', 'BOOLEAN', 'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'COLON', 'DOT', 'COMMA'
] + list(reserved.values())

# -------------- Regular Expressions Rules -------------- #
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_EQUALS = r'=='
t_ASSIGN = r'='
t_NOT_EQUAL = r'!='
t_COLON = r'\:'
t_DOT = r'\.'
t_COMMA = r'\,'
t_SEMICOLON = r';'
t_GREATER = r'>'
t_LESS = r'<'
t_GREATER_EQUAL = r'>='
t_LESS_EQUAL = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Ignore whitespace and newline
t_ignore = ' \t\n'

# -------------- Token Functions -------------- #
def t_BOOLEAN(t):
    r'true|false'
    t.type = reserved.get(t.value, 'BOOLEAN')
    t.value = True if t.value == 'true' else False
    return t

def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # Remove the surrounding quotes
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'//.*'
    pass  # No return value. Token discarded

def t_MULTILINE_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    pass  # No return value. Token discarded

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()