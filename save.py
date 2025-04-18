import json
import networkx as nx
def save_graphs_to_json(graphs, filename):
    """
    Сохраняет графы в формате JSON.

    Parameters:
        graphs (set): Множество графов, представленных в виде frozenset рёбер.
        filename (str): Имя файла для сохранения.
    """
    graph_dict = {}

    for i, edge_set in enumerate(graphs):
        graph = nx.DiGraph()
        graph.add_edges_from(edge_set)

        for edge in edge_set:
            graph.add_nodes_from(edge)

        graph_dict[i] = {
            'nodes': list(graph.nodes(data=True)),
            'edges': list(graph.edges(data=True))
        }

    with open(filename, 'w') as file1:
        json.dump(graph_dict, file1, indent=4)

# save_graphs_to_json(all_graphs, filename)
