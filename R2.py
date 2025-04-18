import json
from collections import defaultdict
from collections import defaultdict

def extract_functions(graph):
    # Словарь меток узлов {id: label}
    nodes = {node_id: data["label"] for node_id, data in graph["nodes"]}
    # Словарь входящих рёбер {узел: [родители]}
    edges_to = defaultdict(list)
    for src, dest, _ in graph["edges"]:
        edges_to[dest].append(src)

    # Логические операции с явными именами
    operations = {
        "op_and": lambda a, b: a & b,
        "op_or": lambda a, b: a | b,
        "op_nand": lambda a, b: ~(a & b) & 1,
        "op_nor": lambda a, b: ~(a | b) & 1,
        "op_xor": lambda a, b: a ^ b
    }

    # Соответствие меток операций именам функций
    operation_mapping = {
        "and": "op_and",
        "or": "op_or",
        "nand": "op_nand",
        "nor": "op_nor",
        "xor": "op_xor"
    }

    def build_expr(node_id, visited):
        """Рекурсивно строит выражение для узла."""
        if node_id in visited:
            return ""
        visited.add(node_id)
        label = nodes[node_id]

        # Если узел — входной бит
        if label in {"x1", "x2", "x3"}:
            return f"x{int(label[1:]) - 1}"

        if label in {"y1", "y2", "y3"}:
            parents = edges_to.get(node_id, [])
            if len(parents) != 1:
                raise ValueError(f"Выходной узел {node_id} ({label}) должен иметь 1 родителя, получено {len(parents)}")
            return build_expr(parents[0], visited)

        parents = edges_to.get(node_id, [])
        if len(parents) != 2:
            raise ValueError(f"Операция {node_id} ({label}) требует 2 родителя, получено {len(parents)}")

        left = build_expr(parents[0], visited.copy())
        right = build_expr(parents[1], visited.copy())
        op_name = operation_mapping[label]
        return f"{op_name}({left}, {right})"

    output_nodes = [9, 10, 11]
    functions = []
    for output_node in output_nodes:
        try:
            expr = build_expr(output_node, set())
            func = eval(f"lambda x0, x1, x2: {expr}", operations)
            functions.append(func)
        except Exception as e:
            raise ValueError(f"Ошибка в узле {output_node}: {str(e)}")

    return tuple(functions)

from sympy.discrete.transforms import fwht


def compute_nonlinearity(truth_tables):
    """
    Вычисляет нелинейность S-блока на основе таблиц истинности координатных функций.

    Аргументы:
        truth_tables (list): Список из 3 таблиц истинности (по одной на каждый бит выхода).
                             Формат: [[y1_0, y1_1, ...], [y2_0, ...], [y3_0, ...]]

    Возвращает:
        int: Нелинейность S-блока (максимально возможное значение = 2)
    """
    nonlinearities = []

    for table in truth_tables:
        # Проверка длины таблицы (должна быть 8)
        if len(table) != 8:
            raise ValueError("Таблица истинности должна содержать 8 элементов")

        bipolar = [1 if x == 0 else -1 for x in table]

        wht = fwht(bipolar)

        max_coeff = max(abs(x) for x in wht[1:])

        nonlinearity = (8 - max_coeff) // 2
        nonlinearities.append(nonlinearity)
    return min(nonlinearities)

def generate_truth_tables(coordinate_functions):
    """
    Генерирует таблицы истинности для каждой координатной функции.

    Аргументы:
        coordinate_functions (list): Список функций [y1_func, y2_func, y3_func]

    Возвращает:
        list: Список таблиц истинности в формате:
            [
                [y1(0,0,0), y1(0,0,1), ..., y1(1,1,1)],  # Для y1
                [y2(0,0,0), y2(0,0,1), ..., y2(1,1,1)],  # Для y2
                [y3(0,0,0), y3(0,0,1), ..., y3(1,1,1)]   # Для y3
            ]
    """
    truth_tables = []

    for func in coordinate_functions:
        table = []
        # Перебираем все 8 комбинаций входных битов (0-7)
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
        for x in inputs:

            result = func(x[0], x[1], x[2])
            table.append(result)
        truth_tables.append(table)

    return truth_tables

def generate_truth_table(func):
    """
    Генерирует таблицу истинности для одной булевой функции.

    Аргументы:
        func (callable): Функция, принимающая три бита (x0, x1, x2) и возвращающая 0 или 1.

    Возвращает:
        list: Таблица истинности в формате:
            [func(0,0,0), func(0,0,1), ..., func(1,1,1)]
    """
    truth_table = []
    inputs = [
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 1),
        (1, 0, 0),
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 1),
    ]
    for x in inputs:
        result = func(*x)
        truth_table.append(result)
    return truth_table


def criterion(graph):
    y1_func, y2_func, y3_func = extract_functions(graph)
    truth_tables = generate_truth_tables([y1_func, y2_func, y3_func])
    nonlin = compute_nonlinearity(truth_tables)
    if nonlin == 2:
        return True
    return False
#
#     return r2