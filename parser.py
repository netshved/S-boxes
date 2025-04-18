import json

# парсинг одного графа
import ijson

from collections import defaultdict, deque
import check as ch
import operation as op

filename_1 = "data/graphs.json"
filename_1_new = "data/graphs_new.json"
filename_2 = "data/labeled_graphs.json"
filename_2_new = "data/labeled_graphs_new.json"
filename_3 = "data/checked_graphs_id.txt"
filename_3_new = "data/checked_graphs_id_new.txt"
def process_large_graph_file(file_path, output_path, input_bits):
    """
    Обрабатывает большой JSON-файл с графами по одному графу за раз и записывает результат в файл.
    """
    with open(file_path, "r", encoding="utf-8") as file, open(output_path, "w", encoding="utf-8") as output_file:
        graphs = ijson.items(file, "item.item")
        for graph_json in graphs:
            try:
                graph_id = graph_json.get("id", "unknown")
                sbox = build_sbox(graph_json)
                try:

                    ch.check(graph_json, sbox, graph_id, filename_3_new)
                except Exception as e:
                    print(f"Ошибка при проверке s-блока: {e}")
                # result = sbox(input_bits)
                output_file.write(f"\nS-box ID: {graph_id}\n")
                # output_file.write("\n".join(str(item) for item in result))

            except Exception as e:
                 print(f"Ошибка при обработке графа: {e}")

def build_sbox(graph):
    operations = {
        "or": lambda a, b: a | b,
        "and": lambda a, b: a & b,
        "nand": lambda a, b: ~(a & b) & 1,
        "xor": lambda a, b: a ^ b,
        "nor": lambda a, b: ~(a | b) & 1
    }

    labels = {node_id: data["label"] for node_id, data in graph["nodes"]}
    edges_to = defaultdict(list)
    edges_from = defaultdict(list)

    for src, dest, _ in graph["edges"]:
        edges_to[dest].append(src)
        edges_from[src].append(dest)

    inputs = sorted(
        [node_id for node_id, label in labels.items() if not edges_to[node_id] and label.startswith("x")],
        key=lambda n: labels[n]
    )
    outputs = {node_id for node_id, label in labels.items() if not edges_from[node_id] and label.startswith("y")}

    # Топологическая сортировка
    in_degree = {node: len(edges_to[node]) for node in labels}
    queue = deque([node for node in labels if in_degree[node] == 0])
    computation_order = []

    while queue:
        node = queue.popleft()
        computation_order.append(node)
        for neighbor in edges_from[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    intermediate_vars = {}
    variable_count = 4
    sequence = []

    for node in computation_order:
        if node in outputs:
            continue

        operation = labels.get(node, None)
        if operation not in operations:
            continue

        parents = edges_to.get(node, [])
        if len(parents) not in [1, 2]:
            raise ValueError(f"Узел {node} имеет {len(parents)} входов (должно быть 1 или 2)")

        input_vars = [intermediate_vars.get(parent, labels[parent]) for parent in parents]
        output_var = f"x{variable_count}"
        variable_count += 1
        intermediate_vars[node] = output_var

        input_vars = []
        for parent in parents:
            if parent in intermediate_vars:
                input_vars.append(intermediate_vars[parent])
            else:
                input_vars.append(labels[parent])

        output_var = f"tmp{variable_count}"
        variable_count += 1
        intermediate_vars[node] = output_var

        if len(input_vars) == 1:
            # Унарная
            sequence.append(f"{input_vars[0]} {operation} = {output_var}")
        else:
            # Бинарная
            sequence.append(f"{input_vars[0]} {operation} {input_vars[1]} = {output_var}")

    # Связываем выходы
    output_mapping = {}
    for output_node in outputs:
        source = edges_to[output_node][0]
        output_mapping[output_node] = intermediate_vars.get(source, labels[source])

    def sbox_function(x):
        values = {labels[node]: bit for node, bit in zip(inputs, x)}
        for step in sequence:
            if "=" in step:
                left, right = step.split("=")
                left = left.strip()
                right = right.strip()
                if " " in left:
                    # Бинарная
                    a, op, b = left.split()
                    values[right] = operations[op](values[a], values[b])
                else:
                    # Унарная
                    op, a = left.split()
                    values[right] = operations[op](values[a])
        return [values[output_mapping[o]] for o in sorted(outputs, key=lambda n: labels[n])]

    return sbox_function