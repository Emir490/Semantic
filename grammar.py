from ply import yacc
import lexer 

tokens = lexer.tokens
symbol_table = {}

def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statement statements_tail'''
    p[0] = [p[1]] + p[2]

def p_statements_tail(p):
    '''statements_tail : statement statements_tail
                       | '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_declaration_statement(p):
    '''declaration_statement : LET IDENTIFIER COLON type ASSIGN expression SEMICOLON
                             | CONST IDENTIFIER COLON type ASSIGN expression SEMICOLON
                             | LET IDENTIFIER ASSIGN expression SEMICOLON
                             | CONST IDENTIFIER ASSIGN expression SEMICOLON
                             | LET IDENTIFIER SEMICOLON'''
    
    identifier = p[2]
    
    if identifier in symbol_table:
        print(f"Semantic Error: Variable {identifier} is already declared")
        return
    
    if p[2] == 'COLON':
        p[0] = ('typed_declaration', p[1], p[2], p[4], p[6])
    else:
        p[0] = ('untyped_declaration', p[1], p[2], p[4])
        
    if len(p) > 4 and p[3] == ':':
        type_ = p[4]
        symbol_table[identifier] = {'type': type_, 'is_const': p[1] == 'const'}
        
def p_assignment_statement(p):
    '''assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON'''
    identifier = p[1]
    if identifier not in symbol_table:
        print(f"Semantic Error: Variable {identifier} is not declared")
        return

    if symbol_table[identifier]['is_const']:
        print(f"Semantic Error: Cannot assign to constant {identifier}")
        return

    exp_type = p[3][2]
    if exp_type != symbol_table[identifier]['type']:
        print(f"Type Error: Incompatible types for {identifier}")
        return

def p_type(p):
    '''type : TYPE_NUMBER
            | TYPE_STRING
            | TYPE_BOOLEAN'''
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF expression block else_clause'''
    p[0] = ('if_statement', p[2], p[3], p[4])  # Corrected index references

def p_else_clause(p):
    '''else_clause : ELSE block
                   | empty'''
    p[0] = p[1]

def p_empty(p):
    '''empty : '''
    p[0] = None

def p_statement(p):
    '''statement : declaration_statement
                 | if_statement
                 | assignment_statement'''
    p[0] = p[1]

def p_expression(p):
    '''expression : NUMBER
                  | STRING
                  | BOOLEAN'''
                  
    if isinstance(p[1], bool):
        p[0] = ('expression', p[1], 'boolean')
    elif isinstance(p[1], str):
        p[0] = ('expression', p[1], 'string')
    elif isinstance(p[1], int):
        p[0] = ('expression', p[1], 'number')

def p_block(p):
    '''block : LBRACE statements RBRACE'''
    p[0] = p[2]

def p_error(p):
    print(f"Syntax error at '{p.value}'")

# Build the parser
parser = yacc.yacc()
