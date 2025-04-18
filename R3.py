import ijson

from collections import defaultdict, deque
import operation as op

import R2
from sympy import mobius_transform

def anf_degree(truth_table):
    coeffs = mobius_transform(truth_table)
    max_degree = 0
    for i, val in enumerate(coeffs):

        if val % 2 != 0:
            # Число единиц в бинарном представлении индекса = количество переменных
            degree = bin(i).count('1')
            if degree > max_degree:
                max_degree = degree
    return max_degree

def criterion(graph):
    y1_func, y2_func, y3_func = R2.extract_functions(graph)
    truth_tables = R2.generate_truth_tables([y1_func, y2_func, y3_func])
    r3 = check_anf_degree(truth_tables)
    return r3

def check_anf_degree(truth_tables):


    for table in truth_tables:
        if anf_degree(table) > 2:
            return False

    from itertools import product
    non_zero_masks = [
        (0, 0, 1),  # Только f3
        (0, 1, 0),  # Только f2
        (0, 1, 1),  # f2 ⊕ f3
        (1, 0, 0),  # Только f1
        (1, 0, 1),  # f1 ⊕ f3
        (1, 1, 0),  # f1 ⊕ f2
        (1, 1, 1),  # f1 ⊕ f2 ⊕ f3
    ]
    for mask in non_zero_masks:
        combined_table = []
        c1, c2, c3 = mask
        for i in range(8):
            val = (c1 * truth_tables[0][i] ^
                   c2 * truth_tables[1][i] ^
                   c3 * truth_tables[2][i])
            combined_table.append(val % 2)
            degree = anf_degree(combined_table)
            # print(f"Комбинация с маской {mask}: степень = {degree}")
            if degree > 2:
                return False

        return True


# Определяем координатные функции
def f1(x0, x1, x2):
    return (x0 & x1) ^ x2

def f2(x0, x1, x2):
    return (x1 & x2) ^ x0

def f3(x0, x1, x2):
    return (x0 & x2) ^ x1

# Генерируем таблицы истинности
coordinate_tables = R2.generate_truth_tables([f1, f2, f3])

# Проверяем степень АНФ
result = check_anf_degree(coordinate_tables)
print("Степень АНФ ≤ 2 для всех функций и комбинаций:", result)
