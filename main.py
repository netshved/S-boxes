import itertools
import json

import networkx as nx
from itertools import combinations


filename_1 = "graphs.json"
filename_2 = "graphs_marked1.json"
filename_3 = "checked_graphs_id.txt"
filename_4 = "graphs_marked3.json"
# Исходный граф
G = nx.DiGraph()
nodes = range(12)
G.add_nodes_from(nodes)
edges = [(0, 3), (0, 4), (1, 3), (1, 5), (2, 4), (2, 5), (6, 9), (7, 10), (8, 11)]
G.add_edges_from(edges)

# Узлы для комбинаций
from_nodes = [0, 1, 2, 3, 4, 5]
to_nodes = [6, 7, 8]

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
 # Итог
print("Количество уникальных графов:", len(all_graphs))