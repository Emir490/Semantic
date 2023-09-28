# Lista para guardar errores semánticos
semantic_errors = []

# Tabla de símbolos para mantener un registro de las variables y su tipo
symbol_table = {}

# Función para comprobar la declaración de una variable
def check_declaration(identifier, p):
    # Verificar si la variable ya ha sido declarada
    if identifier in symbol_table:
        semantic_errors.append(f"Error semántico: La variable {identifier} ya está declarada")
        return False  # Falso indica que hay un error
    return True  # Verdadero indica que no hay errores

# Función para comprobar la asignación a una variable
def check_assignment(identifier, exp_type):
    # Verificar si la variable ha sido declarada
    if identifier not in symbol_table:
        semantic_errors.append(f"Error semántico: La variable {identifier} no está declarada")
        return False  # Falso indica que hay un error

    # Verificar si la variable es constante (no se puede reasignar)
    if symbol_table[identifier]['is_const']:
        semantic_errors.append(f"Error semántico: No se puede asignar a la constante {identifier}")
        return False  # Falso indica que hay un error

    # Verificar si el tipo de la expresión es compatible con el tipo de la variable
    if exp_type != symbol_table[identifier]['type']:
        semantic_errors.append(f"Error de tipo: Tipos incompatibles para {identifier}")
        return False  # Falso indica que hay un error

    return True  # Verdadero indica que no hay errores
