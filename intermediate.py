import time
import sys

# Contador para variables temporales
# Se utiliza para generar nombres de variables temporales únicos
temp_counter = 0

# Lista para almacenar el código intermedio generado
# Guarda cada instrucción intermedia generada durante la compilación
intermediate_code = []

# Registro para la memoria y el tiempo
# Se utiliza para registrar métricas como el tiempo y la memoria utilizada por cada instrucción
instruction_metrics = []

# Lista para almacenar cuádruplos
quad_list = []

# Lista para almacenar tripletas
triplet_list = []

# Función para generar y almacenar cuádruplos
def generate_quad(op, arg1, arg2, result):
    quad = (op, arg1, arg2, result)
    quad_list.append(quad)
    return result

# Función para generar y almacenar tripletas
def generate_triplet(op, arg1, arg2):
    triplet = (op, arg1, arg2)
    triplet_index = len(triplet_list)
    triplet_list.append(triplet)
    return triplet_index

# Función para añadir una línea de código intermedio a la lista
def add_intermediate_code(code_line):
    # Añade la línea de código intermedio dada a la lista 'intermediate_code'
    intermediate_code.append(code_line)

# Función para añadir métricas de tiempo y memoria para una instrucción
def add_metrics(instruction, start_time):
    # Calcular el tiempo final y el tiempo transcurrido
    end_time = time.perf_counter()  # Utilizar perf_counter para mejor resolución temporal
    elapsed_time = end_time - start_time
    
    # Calcular la memoria utilizada por la instrucción
    memory_used = get_size(instruction)
    
    # Agregar las métricas al registro
    instruction_metrics.append({
        'instruction': instruction,
        'time': elapsed_time,
        'memory': memory_used
    })

# Función para generar un nuevo identificador temporal
def new_temp():
    global temp_counter  # Usar la variable global temp_counter para mantener el estado entre llamadas
    temp = f"t{temp_counter}"  # Crear un nuevo identificador temporal
    temp_counter += 1  # Incrementar el contador para futuras variables temporales
    return temp  # Devolver el nuevo identificador

# Función para generar código intermedio para asignaciones
def generate_assignment_code(identifier, expression):
    start_time = time.perf_counter()  # Registra el tiempo de inicio
    # Genera y obtiene el resultado del cuádruplo para la asignación
    result = generate_quad('=', expression, None, identifier)
    # Agrega métricas para esta instrucción
    add_metrics(result, start_time)

# Función para generar código intermedio para declaraciones
def generate_declaration_code(declaration_type, identifier, type_, expression=None):
    start_time = time.perf_counter()  # Registra el tiempo de inicio
    # Verifica si la declaración incluye una inicialización
    if expression:
        result = ('=', expression, None, identifier)
        generate_quad('=', expression, None, identifier)
    else:
        # Para declaraciones sin inicialización, registra el tipo y el identificador
        result = (declaration_type, identifier, type_, None)
    
    quad_list.append(result)
    add_metrics(result, start_time)

# Función para generar código intermedio para operaciones aritméticas
def generate_arithmetic_code(op, operand1, operand2):
    start_time = time.perf_counter()  # Registra el tiempo de inicio
    temp = new_temp()  # Obtiene un nuevo identificador temporal
    # Genera y obtiene el resultado del cuádruplo para la operación aritmética
    result = generate_quad(op, operand1, operand2, temp)
    add_metrics(result, start_time)
    return temp  # Devuelve el identificador temporal que almacena el resultado

# Función para obtener el tamaño en memoria de un objeto
# Utiliza la función sys.getsizeof para determinar el tamaño en bytes
def get_size(obj):
    return sys.getsizeof(obj)
