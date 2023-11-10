from ply import yacc
import lexer
from semantic import check_declaration, symbol_table, check_assignment
from intermediate import generate_assignment_code, generate_declaration_code

tokens = lexer.tokens

# Definir la precedencia de los operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOT_EQUAL'),
    ('left', 'LESS', 'LESS_EQUAL', 'GREATER', 'GREATER_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'NOT')
)

# Regla para el programa completo
def p_program(p):
    '''program : statements'''
    p[0] = p[1]

# Regla para múltiples declaraciones
def p_statements(p):
    '''statements : statement statements_tail
                  | '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# Regla para el resto de las declaraciones
def p_statements_tail(p):
    '''statements_tail : statement statements_tail
                       | '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# Regla para declaración de variables
def p_declaration_statement(p):
    '''declaration_statement : LET IDENTIFIER COLON type ASSIGN expression SEMICOLON
                             | CONST IDENTIFIER COLON type ASSIGN expression SEMICOLON
                             | LET IDENTIFIER ASSIGN expression SEMICOLON
                             | CONST IDENTIFIER ASSIGN expression SEMICOLON
                             | LET IDENTIFIER SEMICOLON'''

    identifier = p[2]  # Identificador de la variable

    if not check_declaration(identifier, p):
        return

    if p[3] == 'COLON':  # Declaración con tipo
        type_ = p[4]
        expression = p[6]
        p[0] = ('typed_declaration', p[1], identifier, type_, expression)
        generate_declaration_code(p[1], identifier, type_, expression)
        
    else:  # Declaración sin tipo
        expression = p[4]
        p[0] = ('untyped_declaration', p[1], identifier, expression)
        generate_declaration_code(p[1], p[2], type, expression=p[4])

    # Guardar el tipo en la tabla de símbolos si está presente
    if len(p) > 4 and p[3] == ':':
        type_ = p[4]
        symbol_table[identifier] = {'type': type_, 'is_const': p[1] == 'const'}

# Regla para asignación de variables
def p_assignment_statement(p):
    '''assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON'''

    identifier = p[1]  # Identificador de la variable
    expression = p[3]  # Valor a asignar
    check_assignment(identifier, expression[2])
    
    p[0] = ('assignment', identifier, expression)
    generate_assignment_code(identifier, expression)
    

# Regla para tipos de datos
def p_type(p):
    '''type : TYPE_NUMBER
            | TYPE_STRING
            | TYPE_BOOLEAN'''
    p[0] = p[1]

# Regla para sentencias if
def p_if_statement(p):
    '''if_statement : IF expression block else_clause'''
    p[0] = ('if_statement', p[2], p[3], p[4])

# Regla para cláusula else
def p_else_clause(p):
    '''else_clause : ELSE block
                   | empty'''
    p[0] = p[1]
    
def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''
    if len(p) == 4:
        p[0] = ('return_statement', p[2])
    else:
        p[0] = ('return_statement', None)

# Regla para elementos vacíos (por ejemplo, en cláusula else opcional)
def p_empty(p):
    '''empty : '''
    p[0] = None

# Regla para una sola declaración
def p_statement(p):
    '''statement : declaration_statement
                 | if_statement
                 | assignment_statement
                 | function_declaration
                 | return_statement
                 | expression'''
    p[0] = p[1]

# Regla para expresiones básicas (números, cadenas, booleanos)
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

# Reglas para expresiones aritméticas
def p_expression_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression'''
    p[0] = ('arithmetic_expression', p[1], p[2], p[3])
    
    num1 = p[1][1]
    num2 = p[3][1]
      
    if isinstance(num1, (int, float)) and isinstance(num2, (int, float)):
        if p[2] == '+':
            p[0] = num1 + num2
        elif p[2] == '-':
            p[0] = num1 - num2
        elif p[2] == '*':
            p[0] = num1 * num2
        elif p[2] == '/':
            p[0] = num1 / num2
        elif p[2] == '%':
            p[0] = num1 % num2
        print(f"Evaluated Expression: {num1} {p[2]} {num2} = {p[0]}")
    else:
        # Handle non-numeric operands as required
        print('No expresiones numericas')

# Reglas para expresiones relacionales
def p_expression_relational(p):
    '''expression : expression LESS expression
                  | expression LESS_EQUAL expression
                  | expression GREATER expression
                  | expression GREATER_EQUAL expression
                  | expression EQUALS expression
                  | expression NOT_EQUAL expression'''
    p[0] = ('relational_expression', p[1], p[2], p[3])

# Reglas para expresiones lógicas
def p_expression_logical(p):
    '''expression : expression AND expression
                  | expression OR expression'''
    p[0] = ('logical_expression', p[1], p[2], p[3])

# Regla para la negación lógica
def p_expression_not(p):
    '''expression : NOT_EQUAL expression'''
    p[0] = ('logical_expression', 'NOT', p[2])

# Regla para expresiones agrupadas
def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = ('group_expression', p[2])
    
def p_function_declaration(p):
    '''function_declaration : FUNCTION IDENTIFIER LPAREN param_list RPAREN block'''
    p[0] = ('function_declaration', p[2], p[4], p[6])
    param_str = ', '.join([f"{name}:{type_}" for name, type_ in p[4]])
    # intermediate_code.append(f"function {p[2]}({param_str}) {p[6]}")

# Regla para llamar a una función
def p_function_call(p):
    '''expression : IDENTIFIER LPAREN arg_list RPAREN'''
    p[0] = ('function_call', p[1], p[3])
    arg_str = ', '.join([str(arg[1]) for arg in p[3]])
    # intermediate_code.append(f"{p[1]}({arg_str});") 

# Regla para la lista de parametros
def p_param_list(p):
    '''param_list : param_list_tail
                  | '''
    p[0] = p[1] if len(p) > 1 else []

# Auxiliar para la lisa de parametros
def p_param_list_tail(p):
    '''param_list_tail : IDENTIFIER COLON type COMMA param_list_tail
                       | IDENTIFIER COLON type'''
    if len(p) > 4:
        p[0] = [(p[1], p[3])] + p[5]
    else:
        p[0] = [(p[1], p[3])]

# Regla para lista de argumentos
def p_arg_list(p):
    '''arg_list : arg_list_tail
                | '''
    p[0] = p[1] if len(p) > 1 else []

# Regla para lista de argumentos auxiliar
def p_arg_list_tail(p):
    '''arg_list_tail : expression COMMA arg_list_tail
                     | expression'''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

# Regla para bloques de código
def p_block(p):
    '''block : LBRACE statements RBRACE'''
    p[0] = p[2]

# Manejo de errores
def p_error(p):
    print(f"Error de sintaxis en '{p.value}'")

# Construir el parser
parser = yacc.yacc()