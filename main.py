import itertools
import json

import generator as gen
import save as s
import parser as p
import check as ch

import networkx as nx
from itertools import combinations


filename_1 = "data/graphs.json"
filename_2 = "data/labeled_graphs.json"
filename_3 = "data/checked_graphs_id.txt"
# filename_4 = "graphs_marked3.json"

# Исходный граф
G = nx.DiGraph()
nodes = range(12)
G.add_nodes_from(nodes)
edges = [(0, 3), (0, 4), (1, 3), (1, 5), (2, 4), (2, 5), (6, 9), (7, 10), (8, 11)]
G.add_edges_from(edges)

# Узлы для комбинаций
from_nodes = [0, 1, 2, 3, 4, 5]
to_nodes = [6, 7, 8]

all_graphs = gen.generate_graphs(from_nodes, to_nodes, G)
 # Итог
print("Количество уникальных графов:", len(all_graphs))
s.save_graphs_to_json(all_graphs, filename_1)

labels = ["or", "xor", "and", "nand"]
# gen.generate_labeled_graphs(filename_1, filename_2, labels)
output = "data/s-box_input1.txt"
input_bits = [1, 0, 1]
p.process_large_graph_file(filename_2, output, input_bits)

