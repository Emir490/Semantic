symbol_table = {}

def check_declaration(identifier, p):
    if identifier in symbol_table:
        print(f"Semantic Error: Variable {identifier} is already declared")
        return False
    return True

def check_assignment(identifier, exp_type):
    if identifier not in symbol_table:
        print(f"Semantic Error: Variable {identifier} is not declared")
        return False
    if symbol_table[identifier]['is_const']:
        print(f"Semantic Error: Cannot assign to constant {identifier}")
        return False
    if exp_type != symbol_table[identifier]['type']:
        print(f"Type Error: Incompatible types for {identifier}")
        return False
    return True