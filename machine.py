# Supongamos que ya tienes una función que mapea cuádruplos a instrucciones de ensamblador
from assembly import generate_assembly

def generate_machine_code(quads):
    machine_code = []
    for quad in quads:
        assembly_instr = generate_assembly(quad)
        # Aquí necesitarías convertir la instrucción de ensamblador a código de máquina
        # Este es un paso no trivial y depende de la arquitectura objetivo
        machine_instr = convert_to_machine_code(assembly_instr)
        machine_code.append(machine_instr)
    return machine_code

def convert_to_machine_code(assembly_instr):
    # Esta función es altamente específica para la arquitectura
    # Deberás reemplazar la lógica de ejemplo con la conversión real
    # Aquí solo se muestra un ejemplo de cómo podría verse la función
    opcode, operands = parse_assembly_instruction(assembly_instr)
    binary_opcode = opcode_to_binary(opcode)
    binary_operands = operands_to_binary(operands)
    return binary_opcode + binary_operands

def parse_assembly_instruction(assembly_instr):
    # Divide la instrucción por espacios para separar el opcode de los operandos
    parts = assembly_instr.strip().split()

    # El primer elemento es el opcode
    opcode = parts[0].upper()  # Convertimos a mayúsculas para estandarizar
    
    # El resto de los elementos son operandos, algunos podrían estar separados por comas
    # Aquí asumimos que todos los operandos están separados por un espacio para simplificar
    operands = parts[1:]

    # Devolvemos el opcode y una lista de operandos
    return opcode, operands 

def opcode_to_binary(opcode):
    # Convierte un opcode de ensamblador a su equivalente binario
    # Este es un ejemplo simplificado
    return {
        'ADD': '0001',
        'MOV': '0010',
        # ...otros opcodes...
    }.get(opcode, '1111')  # '1111' podría representar un opcode desconocido

def operands_to_binary(operands):
    # Convierte operandos de ensamblador a su representación binaria
    # Este es un ejemplo simplificado
    # Necesitarás una lógica detallada para manejar registros, direcciones, etc.
    return ''.join(format(ord(x), 'b') for x in operands)

# Uso del generador de código de máquina
# machine_code = generate_machine_code(quad_list)
