import itertools
import json

import networkx as nx
from itertools import combinations

from collections import deque


def depends_on_all_inputs(graph, output_node, input_nodes):
    """Проверяет, зависит ли output_node от всех input_nodes (0,1,2)."""
    visited = set()
    queue = deque([output_node])
    dependencies = set()

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        # Если текущий узел — входной бит, добавляем его в зависимости
        if node in input_nodes:
            dependencies.add(node)
        # Идем по обратным ребрам к родителям (входным узлам)
        for parent in graph.predecessors(node):
            if parent not in visited:
                queue.append(parent)

    return dependencies == set(input_nodes)


def is_valid_graph(graph):
    """Проверяет, что все выходные узлы зависят от всех входных."""
    input_nodes = [0, 1, 2]
    output_nodes = [9, 10, 11]

    for output in output_nodes:
        if not depends_on_all_inputs(graph, output, input_nodes):
            return False
    return True


def generate_graphs(from_nodes, to_nodes, G):
    combinations_to_node = list(combinations(from_nodes, 2))
    all_graphs = set()  #  исключения повторов
    for combination_f in combinations_to_node:
        for to_node in to_nodes:
            H = G.copy()
            H.add_edge(combination_f[0], to_node)
            H.add_edge(combination_f[1], to_node)
            for combination_f2 in combinations_to_node:
                if combination_f2 != combination_f:
                    for to_node2 in to_nodes:
                        if to_node2 != to_node:
                            H1 = H.copy()
                            H1.add_edge(combination_f2[0], to_node2)
                            H1.add_edge(combination_f2[1], to_node2)
                            for combination_f3 in combinations_to_node:
                                if combination_f3 != combination_f and combination_f3 != combination_f2:
                                    for to_node3 in to_nodes:
                                        if to_node3 != to_node and to_node3 != to_node2:
                                            H2 = H1.copy()
                                            H2.add_edge(combination_f3[0], to_node3)
                                            H2.add_edge(combination_f3[1], to_node3)
                                            if is_valid_graph(H2):
                                                all_graphs.add(frozenset(H2.edges))
    return all_graphs



def generate_labeled_graphs(input_file, output_file, labels, chunk_size=1000):
    """
    Генерирует графы с уникальными идентификаторами и маркированными вершинами,
    записывая их порциями в выходной JSON-файл.

    :param input_file: Путь к JSON-файлу с исходными графами.
    :param output_file: Путь к JSON-файлу для записи промаркированных графов.
    :param labels: Список доступных операций для маркировки вершин.
    :param chunk_size: Размер порции графов для записи в файл.
    """

    with open(input_file, 'r') as infile:
        all_graphs = json.load(infile)

    vertices_to_label = [3, 4, 5, 6, 7, 8]

    label_combinations = list(itertools.product(labels, repeat=len(vertices_to_label)))
    total_combinations = len(label_combinations)

    print(f"Total graphs: {len(all_graphs)}")
    print(f"Total label combinations: {total_combinations}")

    with open(output_file, 'w') as outfile:
        outfile.write('[')
        graph_counter = 0
        unique_id = 0
        chunk = []

        for graph_index, (graph_id, graph_data) in enumerate(all_graphs.items()):

            graph = nx.DiGraph()
            graph.add_nodes_from(graph_data['nodes'])
            graph.add_edges_from(graph_data['edges'])

            fixed_labels = {
                0: "x1", 1: "x2", 2: "x3",
                9: "y1", 10: "y2", 11: "y3"
            }

            for combination in label_combinations:
                labeled_graph = graph.copy()

                mapping = {v: label for v, label in zip(vertices_to_label, combination)}
                full_mapping = {**fixed_labels, **mapping}

                nx.set_node_attributes(labeled_graph, full_mapping, 'label')

                chunk.append({
                    'id': unique_id,
                    'nodes': list(labeled_graph.nodes(data=True)),
                    'edges': list(labeled_graph.edges(data=True))
                })

                unique_id += 1

                if len(chunk) >= chunk_size:
                    json.dump(chunk, outfile, separators=(',', ':'))
                    outfile.write(',')  # Разделяем порции запятой
                    chunk.clear()

            if graph_index % 10 == 0:
                print(f"Processed {graph_index + 1}/{len(all_graphs)} graphs...")

        if chunk:
            json.dump(chunk, outfile, separators=(',', ':'))

        outfile.write(']')

    print(f"Total labeled graphs generated: {unique_id}")