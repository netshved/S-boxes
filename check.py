from itertools import product
import numpy as np
from collections import defaultdict, deque
import R1
import R2
import R3

filename_1 = "data/graphs.json"
filename_2 = "data/labeled_graphs.json"
filename_3 = "data/checked_graphs_id.txt"


filename_1_new = "data/graphs_new.json"

filename_2_new = "data/labeled_graphs_new.json"

filename_3_new = "data/checked_graphs_id_new.txt"

# def check_bijective(sbox):
#     # Создаем два множества: одно для входов, другое для выходов
#     inputs = set()
#     outputs = set()
#
#     # Перебираем все возможные входы от 0 до 7 (для 3-битных входов)
#     for i in range(8):
#         input_bits = [int(x) for x in format(i, '03b')]  # Преобразуем число в 3 бита
#         output_bits = sbox(input_bits)  # Получаем выход для этого входа
#
#         # Преобразуем выход в кортеж, чтобы можно было добавить в множество
#         output_bits_tuple = tuple(output_bits)
#
#         # Добавляем вход и выход в множества
#         inputs.add(tuple(input_bits))
#         outputs.add(output_bits_tuple)
#
#     # Если количество уникальных входов и выходов одинаково, и множества равны, то функция биективна
#     return len(inputs) == 8 and len(outputs) == 8 and inputs == outputs

def sbox_function_to_table(sbox_func):
    """Преобразует функцию S-блока в таблицу истинности."""
    sbox_table = []
    for x in range(8):
        # Получаем входные биты (например, x=3 → [0, 1, 1])
        input_bits = [(x >> (2 - i)) & 1 for i in range(3)]

        output_bits = sbox_func(input_bits)
        output_value = (output_bits[0] << 2) | (output_bits[1] << 1) | output_bits[2]
        sbox_table.append(output_value)
    return sbox_table

def check(graph_json, sbox_func, graph_id, output_file):
    """Основная функция проверки"""
    try:
        # Преобразуем функцию в таблицу
        sbox_table = sbox_function_to_table(sbox_func)

        r1 = R1.criterion(sbox_func)

        r3 = R3.criterion(graph_json)
        r2 = R2.criterion(graph_json)

        # isbijective = is_sbox_bijective(sbox_func)

        if r1 and r2 and r3:
            with open(output_file, 'a') as f:
                f.write(f"{graph_id}\n")

        print(f"Результаты для графа {graph_id}:")
        # print(f"- биективность: {'Да' if isbijective else 'Нет'}")
        print(f"- R1 (Дифференциальная устойчивость): {'Да' if r1 else 'Нет'}")
        print(f"- R2 (Нелинейность = 2): {'Да' if r2 else 'Нет'}")
        print(f"- R3 (Алгебраическая степень = 2): {'Да' if r3 else 'Нет'}")

    except Exception as e:
        print(f"Ошибка при обработке графа {graph_id}: {str(e)}")
