# Contador para variables temporales
temp_counter = 0

# Lista para almacenar el código intermedio generado
intermediate_code = []

# Función para añadir una línea de código intermedio a la lista
def add_intermediate_code(code_line):
    intermediate_code.append(code_line)

# Función para generar un nuevo identificador temporal
def new_temp():
    global temp_counter  # Usar la variable global temp_counter
    temp = f"t{temp_counter}"  # Crear un nuevo identificador temporal
    temp_counter += 1  # Incrementar el contador
    return temp  # Devolver el nuevo identificador

# Función para generar código intermedio para asignaciones
def generate_assignment_code(identifier, expression):
    temp = new_temp()  # Obtener un nuevo identificador temporal
    code_line = f"{temp} = {expression}"  # Generar la línea de código para la asignación
    add_intermediate_code(code_line)  # Añadir la línea al código intermedio
    code_line = f"{identifier} = {temp}"  # Generar la línea de código para almacenar en la variable destino
    add_intermediate_code(code_line)  # Añadir la línea al código intermedio

# Función para generar código intermedio para declaraciones
def generate_declaration_code(declaration_type, identifier, type_, expression=None):
    if expression:  # Si hay una expresión (inicialización)
        code_line = f"{declaration_type} {identifier}:{type_} = {expression};"  
    else:  # Si no hay inicialización
        code_line = f"{declaration_type} {identifier}:{type_};"
    add_intermediate_code(code_line)  # Añadir la línea al código intermedio

# Función para generar código intermedio para operaciones aritméticas
def generate_arithmetic_code(op, operand1, operand2):
    temp = new_temp()  # Obtener un nuevo identificador temporal
    code_line = f"{temp} = {operand1} {op} {operand2}"  # Generar la línea de código para la operación
    add_intermediate_code(code_line)  # Añadir la línea al código intermedio
    return temp  # Devolver el identificador temporal que almacena el resultado
