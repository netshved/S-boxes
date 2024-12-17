
def logic_or(a, b):
    return a | b

def logic_and(a, b):
    return a & b

def logic_nand(a, b):
    return ~(a & b) & 1  # Ограничиваем результат до 1 бита

def logic_xor(a, b):
    return a ^ b
