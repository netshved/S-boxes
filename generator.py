import itertools
import json

import networkx as nx
from itertools import combinations

def generate_graphs(from_nodes, to_nodes, G):
    # Генерация комбинаций дуг
    combinations_to_node = list(combinations(from_nodes, 2))
    all_graphs = set()  # Используем множество для автоматического исключения повторов
     # Создание графов
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
                                            # Сохраняем уникальные графы по их множеству рёбер
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
    # Загружаем исходные графы
    with open(input_file, 'r') as infile:
        all_graphs = json.load(infile)

    # Определяем вершины для маркировки
    vertices_to_label = [3, 4, 5, 6, 7, 8]

    # Генерируем все возможные комбинации меток
    label_combinations = list(itertools.product(labels, repeat=len(vertices_to_label)))
    total_combinations = len(label_combinations)

    print(f"Total graphs: {len(all_graphs)}")
    print(f"Total label combinations: {total_combinations}")

    # Открываем файл для записи
    with open(output_file, 'w') as outfile:
        outfile.write('[')  # Начало JSON массива

        graph_counter = 0  # Счетчик обработанных графов
        unique_id = 0  # Уникальный идентификатор графов
        chunk = []  # Текущая порция графов

        # Проходим по каждому графу
        for graph_index, (graph_id, graph_data) in enumerate(all_graphs.items()):
            # Создаем граф
            graph = nx.DiGraph()
            graph.add_nodes_from(graph_data['nodes'])
            graph.add_edges_from(graph_data['edges'])

            # Фиксированные метки для входных и выходных вершин
            fixed_labels = {
                0: "x1", 1: "x2", 2: "x3",
                9: "y1", 10: "y2", 11: "y3"
            }

            # Применяем все комбинации меток
            for combination in label_combinations:
                labeled_graph = graph.copy()

                # Создаем отображение вершин на метки
                mapping = {v: label for v, label in zip(vertices_to_label, combination)}
                full_mapping = {**fixed_labels, **mapping}

                # Обновляем метки вершин
                nx.set_node_attributes(labeled_graph, full_mapping, 'label')

                # Форматируем граф для сохранения
                chunk.append({
                    'id': unique_id,
                    'nodes': list(labeled_graph.nodes(data=True)),
                    'edges': list(labeled_graph.edges(data=True))
                })

                unique_id += 1

                # Записываем порцию в файл, если она достигла нужного размера
                if len(chunk) >= chunk_size:
                    json.dump(chunk, outfile, separators=(',', ':'))
                    outfile.write(',')  # Разделяем порции запятой
                    chunk.clear()

            # Логируем прогресс
            if graph_index % 10 == 0:
                print(f"Processed {graph_index + 1}/{len(all_graphs)} graphs...")

        # Записываем оставшиеся графы
        if chunk:
            json.dump(chunk, outfile, separators=(',', ':'))

        outfile.write(']')  # Конец JSON массива

    print(f"Total labeled graphs generated: {unique_id}")