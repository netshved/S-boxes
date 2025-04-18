
def criterion(sbox_function):
    """
    Проверяет, удовлетворяет ли S-блок условию:
    Уравнение s(x ⊕ α) ⊕ s(x) = β имеет не более 2 решений для всех ненулевых α, β ∈ {0,1}^3.

    Аргументы:
    sbox_function (callable): Функция S-блока, принимающая список из 3 бит и возвращающая список из 3 бит.

    Возвращает:
    bool: True, если критерий выполняется, иначе False.
    """
    from itertools import product

    # Генерация всех ненулевых α и β в виде списков битов
    non_zero = [list(bits) for bits in product([0, 1], repeat=3) if bits != (0, 0, 0)]
    a_inputs = non_zero  # α
    b_inputs = non_zero  # β

    def bits_to_int(bits):
        return sum(bit << i for i, bit in enumerate(bits))

    for alpha_bits in a_inputs:
        alpha_int = bits_to_int(alpha_bits)
        for beta_bits in b_inputs:
            beta_int = bits_to_int(beta_bits)
            solution_count = 0
            for x in range(8):
                x_bits = [(x >> i) & 1 for i in range(3)]
                # Вычисляем x ⊕ α
                x_alpha_int = x ^ alpha_int
                # Преобразуем x_alpha в битовый список
                x_alpha_bits = [(x_alpha_int >> i) & 1 for i in range(3)]
                s_x = sbox_function(x_bits)
                s_x_alpha = sbox_function(x_alpha_bits)
                s_x_int = bits_to_int(s_x)
                s_x_alpha_int = bits_to_int(s_x_alpha)

                if s_x_alpha_int ^ s_x_int == beta_int:
                    solution_count += 1
                    if solution_count > 2:
                        return False
    return True

def is_sbox_bijective(sbox_func):
    """
    Проверяет, является ли S-блок (функция sbox_func) биективным.
    """

    inputs = [
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ]

    outputs = set()

    for input_bits in inputs:
        output_bits = sbox_func(input_bits)

        # Проверяем корректность выхода
        if not (isinstance(output_bits, list) and len(output_bits) == 3 and all(b in [0, 1] for b in output_bits)):
            raise ValueError(f"Неверный формат выхода: {output_bits}")

        output_tuple = tuple(output_bits)
        outputs.add(output_tuple)

    return len(outputs) == 8
