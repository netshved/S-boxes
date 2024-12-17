import json

# парсинг одного графа
import ijson
from collections import defaultdict
import check as ch

filename_1 = "data/graphs.json"
filename_2 = "data/labeled_graphs.json"
filename_3 = "data/checked_graphs_id.txt"

def logic_or(a, b):
    return a | b

def logic_and(a, b):
    return a & b

def logic_nand(a, b):
    return ~(a & b) & 1  # Ограничиваем результат до 1 бита

def logic_xor(a, b):
    return a ^ b

def process_large_graph_file(file_path, output_path, input_bits):
    """
    Обрабатывает большой JSON-файл с графами по одному графу за раз и записывает результат в файл.
    """
    with open(file_path, "r", encoding="utf-8") as file, open(output_path, "w", encoding="utf-8") as output_file:
        graphs = ijson.items(file, "item.item")  # Считываем вложенные графы
        for graph_json in graphs:
            try:
                graph_id = graph_json.get("id", "unknown")
                sbox = build_sbox(graph_json)
                try:

                    ch.check(sbox, graph_id, filename_3)
                except Exception as e:
                    print(f"Ошибка при проверке s-блока: {e}")
                result = sbox(input_bits)
                output_file.write(f"\nS-box ID: {graph_id}\n")
                output_file.write("\n".join(str(item) for item in result))


            except Exception as e:
                 print(f"Ошибка при обработке графа: {e}")

def build_sbox(graph):
    # Маппинг операций на функции
    operations = {
        "or": logic_or,
        "and": logic_and,
        "nand": logic_nand,
        "xor": logic_xor
    }

    # Словарь меток узлов
    labels = {node_id: data["label"] for node_id, data in graph["nodes"]}

    # Строим зависимости
    edges_to = defaultdict(list)  # Куда идут рёбра
    edges_from = defaultdict(list)  # Откуда приходят рёбра

    for src, dest, _ in graph["edges"]:
        edges_to[dest].append(src)
        edges_from[src].append(dest)

    # Ищем входные и выходные вершины
    inputs = {node_id for node_id, label in labels.items()
              if not edges_to[node_id] and label.startswith("x")}
    outputs = {node_id for node_id, label in labels.items()
               if not edges_from[node_id] and label.startswith("y")}

    # Порядок вычислений
    computation_order = []
    computed = set(inputs)
    to_compute = set(labels.keys()) - inputs

    # Пошагово определяем порядок вычислений
    while to_compute:
        for node in list(to_compute):
            if all(src in computed for src in edges_to[node]):
                computation_order.append(node)
                computed.add(node)
                to_compute.remove(node)

    # Генерация последовательности операций
    intermediate_vars = {}
    output_vars = {}
    variable_count = len(inputs) + 1
    sequence = []

    for node in computation_order:
        if node in outputs:
            output_vars[node] = edges_to[node][0]  # Связываем с источником
            continue

        if node not in edges_to:
            continue

        operation = labels[node]
        if operation not in operations:
            raise ValueError(f"Неизвестная операция: {operation}")

        inputs_for_node = [intermediate_vars.get(src, labels[src]) for src in edges_to[node]]

        # Создаем новое промежуточное значение
        new_var = f"x{variable_count}"
        variable_count += 1
        intermediate_vars[node] = new_var

        # Формируем строку операции
        op_str = f"{inputs_for_node[0]} {operation} {inputs_for_node[1]} = {new_var}"
        sequence.append(op_str)

    # Создаем финальные связи для выходов
    for output in outputs:
        source = edges_to[output][0]
        output_var = intermediate_vars.get(source, labels[source])
        sequence.append(f"{output_var} -> {labels[output]}")

    # Создаем функцию для выполнения S-блока
    def sbox_function(x):
        """
        Реализация S-блока. На вход подаётся список входных бит.
        """
        values = {f"x{i + 1}": bit for i, bit in enumerate(x)}

        for step in sequence:
            if "=" in step:
                left, right = step.split("=")
                left = left.strip()
                right = right.strip()

                parts = left.split()
                a, op, b = parts[0], parts[1], parts[2]
                values[right] = operations[op](values[a], values[b])

            elif "->" in step:
                left, right = step.split("->")
                left = left.strip()
                right = right.strip()
                values[right] = values[left]

        return [values[labels[output]] for output in outputs]

    return sbox_function
