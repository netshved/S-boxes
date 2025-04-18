import json
import networkx as nx
import matplotlib.pyplot as plt

filename = "graphs.json"

# Метки для узлов (по твоему примеру)
node_labels = {
    0: "x1", 1: "x2", 2: "x3",
    3: "or", 4: "nand", 5: "nand",
    6: "and", 7: "and", 8: "or",
    9: "y1", 10: "y2", 11: "y3"
}

def draw_graph_with_labels(graph_data, graph_id,  highlighted_edges=None):
    import matplotlib.pyplot as plt
    import networkx as nx

    highlighted_edges = [
        (0, 3), (0, 4), (1, 3), (1, 5),
        (2, 4), (2, 5), (6, 9), (7, 10), (8, 11)
    ]

    G = nx.DiGraph()
    G.add_nodes_from([n for n, _ in graph_data["nodes"]])
    G.add_edges_from([(src, dst) for src, dst, _ in graph_data["edges"]])

    # Извлечение меток
    node_labels = {n: attrs.get("label", str(n)) for n, attrs in graph_data["nodes"]}

    # Позиции вручную: 4 столбца по 3 узла
    pos = {
        0: (0, -0),
        1: (0, -1),
        2: (0, -2),
        3: (1, -0),
        4: (1, -1),
        5: (1, -2),
        6: (2, -0),
        7: (2, -1),
        8: (2, -2),
        9: (3, -0),
        10: (3, -1),
        11: (3, -2),
    }

    plt.figure(figsize=(8, 4))

    # Проверка на наличие дуг перед выделением
    highlight_candidates = highlighted_edges or []
    red_edges = [edge for edge in highlight_candidates if G.has_edge(*edge)]
    gray_edges = [e for e in G.edges() if e not in red_edges]

    # Рисуем
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)

    nx.draw_networkx_edges(G, pos, edgelist=gray_edges, edge_color='blue', arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='red', arrows=True)

    plt.title(f"graph {graph_id}")
    plt.axis('off')
    plt.show()

# Загрузка всех графов
# with open(filename, "r", encoding="utf-8") as f:
#     graphs = json.load(f)
#
# # Визуализация по одному
# for graph_id, graph_data in graphs.items():
#     draw_graph(graph_data, graph_id)
#     input("Press Enter for next graph...")

# highlighted = [(0, 3), (1, 4), (2, 5), (6, 9), (7, 10), (8, 11)]
def draw_graph_simple(graph_data, graph_id, highlighted_edges=None):
    highlighted_edges = [
        (0, 3), (0, 4), (1, 3), (1, 5),
        (2, 4), (2, 5), (6, 9), (7, 10), (8, 11)
    ]
    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.DiGraph()
    G.add_nodes_from([n for n, _ in graph_data["nodes"]])
    G.add_edges_from([(src, dst) for src, dst, _ in graph_data["edges"]])

    # Позиции вручную: 4 столбца по 3 узла
    pos = {
        0: (0, -0),
        1: (0, -1),
        2: (0, -2),
        3: (1, -0),
        4: (1, -1),
        5: (1, -2),
        6: (2, -0),
        7: (2, -1),
        8: (2, -2),
        9: (3, -0),
        10: (3, -1),
        11: (3, -2),
    }

    plt.figure(figsize=(8, 4))

    # Проверка наличия ребра перед тем как красить красным
    highlight_candidates = highlighted_edges or []
    red_edges = [edge for edge in highlight_candidates if G.has_edge(*edge)]
    gray_edges = [e for e in G.edges() if e not in red_edges]

    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, labels={n: str(n) for n in G.nodes()}, font_size=10)

    nx.draw_networkx_edges(G, pos, edgelist=gray_edges, edge_color='blue', arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='red', arrows=True)

    plt.title(f"graph {graph_id}")
    plt.axis('off')
    plt.show()