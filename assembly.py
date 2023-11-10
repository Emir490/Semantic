# Diccionario que mapea operaciones de cuádruplos a instrucciones de ensamblador
assembly_ops = {
    '+': 'ADD',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'DIV'
}

# Lista para mantener las instrucciones de ensamblador generadas
assembly_code = []

def generate_assembly(quad):
    op, arg1, arg2, result = quad
    
    # Mapear la operación a su equivalente en ensamblador
    asm_op = assembly_ops.get(op)
    if asm_op:
        # Generar código de ensamblador para una operación binaria
        assembly_code.append(f"{asm_op} {result}, {arg1}, {arg2}")
    elif op == '=':
        # Generar código de ensamblador para una asignación
        assembly_code.append(f"MOV {result}, {arg1}")  # MOV destino, fuente