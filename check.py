from itertools import product

filename_1 = "data/graphs.json"
filename_2 = "data/labeled_graphs.json"
filename_3 = "data/checked_graphs_id.txt"

def check_bijective(sbox):
    # Создаем два множества: одно для входов, другое для выходов
    inputs = set()
    outputs = set()

    # Перебираем все возможные входы от 0 до 7 (для 3-битных входов)
    for i in range(8):
        input_bits = [int(x) for x in format(i, '03b')]  # Преобразуем число в 3 бита
        output_bits = sbox(input_bits)  # Получаем выход для этого входа

        # Преобразуем выход в кортеж, чтобы можно было добавить в множество
        output_bits_tuple = tuple(output_bits)

        # Добавляем вход и выход в множества
        inputs.add(tuple(input_bits))
        outputs.add(output_bits_tuple)

    # Если количество уникальных входов и выходов одинаково, и множества равны, то функция биективна
    return len(inputs) == 8 and len(outputs) == 8 and inputs == outputs

def check_nonlinearity(sbox):
    # В S-блоке 3 бита на входе, значит, есть 8 возможных входных значений (от 0 до 7)
    num_bits = 3
    num_inputs = 8

    max_non_linearity = 0

    # Проходим по всем возможным входам и проверяем выходы
    for i in range(num_inputs):
        for j in range(i + 1, num_inputs):
            input_bits_i = [int(x) for x in format(i, '03b')]
            input_bits_j = [int(x) for x in format(j, '03b')]

            output_bits_i = sbox(input_bits_i)
            output_bits_j = sbox(input_bits_j)

            # Считаем количество битовых различий (Hamming distance)
            hamming_distance = sum(b1 != b2 for b1, b2 in zip(output_bits_i, output_bits_j))

            # Нелинейность увеличивается с увеличением Hamming distance
            max_non_linearity = max(max_non_linearity, hamming_distance)

    # Возвращаем максимальную нелинейность
    return max_non_linearity

def is_balanced_and_equilibrated(sbox):
    """
    Проверяет сбалансированность и уравновешенность координатных функций S-блока.

    :param sbox: Функция S-блока. Принимает список из 3 бит (например, [1, 0, 1])
                 и возвращает список из 3 бит (например, [1, 0, 1]).
    :return: Словарь с результатами проверки.
    """
    n = 3  # Количество входных бит
    m = 3  # Количество выходных бит

    # Построим список всех возможных входов (от 0 до 2^n - 1), но в виде списка бит
    inputs = [list(map(int, format(x, f'0{n}b'))) for x in range(2 ** n)]

    # Вычислим выходы S-блока
    outputs = []
    for input_bits in inputs:
        output = sbox(input_bits)  # Получаем список бит
        if not (isinstance(output, list) and len(output) == m):
            raise ValueError(f"sbox({input_bits}) должен вернуть список длины {m}, а не {output}.")
        if not all(bit in [0, 1] for bit in output):
            raise ValueError(f"sbox({input_bits}) вернул {output}, но он содержит недопустимые значения.")
        # Преобразуем список бит в строку, а затем в целое число
        output_value = int(''.join(map(str, output)), 2)
        outputs.append(output_value)

    # Координатные функции: массив значений для каждого бита выходов
    coord_functions = [[(output >> i) & 1 for output in outputs] for i in range(m)]

    # Проверка сбалансированности координатных функций
    def check_balance(func):
        return func.count(0) == func.count(1)

    balanced = all(check_balance(func) for func in coord_functions)

    # Проверка уравновешенности линейных комбинаций координатных функций
    def is_combination_balanced(combo):
        """
        Проверяет, является ли линейная комбинация координатных функций сбалансированной.
        """
        combined_func = [
            sum(combo[i] * coord_functions[i][j] for i in range(m)) % 2
            for j in range(len(inputs))
        ]
        return check_balance(combined_func)

    # Генерация всех ненулевых комбинаций (векторов) длины m
    equilibrated = all(
        is_combination_balanced(list(combo))
        for combo in product([0, 1], repeat=m)
        if any(combo)  # Исключаем нулевой вектор
    )
    # print ("balanced", balanced)
    # print("equilibrated", equilibrated)
    if (balanced == True & equilibrated == True):
        return True
    return False

def check(sbox, graph_id, output):

    flag = False
    # Проверка на биективность

    is_bijective = check_bijective(sbox)


    # Проверка на нелинейность
    non_linearity = check_nonlinearity(sbox)


    balanced_and_equilibrated = is_balanced_and_equilibrated(sbox)


    if is_bijective & non_linearity & balanced_and_equilibrated == True:
        with open(output, 'a') as f:  # Открываем файл в режиме добавления
            f.write(f"{graph_id}\n")  # Записываем число в новую строку


        print(graph_id)

        print("S-блок биективен:", is_bijective)

        print("Максимальная нелинейность S-блока:", non_linearity)

        print("Уравновешенные координатные функции:", balanced_and_equilibrated)

