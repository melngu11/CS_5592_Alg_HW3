import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np

class Graph:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.order = m*n+1
        self.adj_list = {i: [] for i in range(self.order)}
        self.edge_labels = {}

    def add_edge(self, u, v, label):
        if (u, v) not in self.edge_labels and (v, u) not in self.edge_labels:
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
            self.edge_labels[(u, v)] = label
            self.edge_labels[(v, u)] = label

def assign_labels(graph):
    label = 1  # Initialize label starting from 1 for uniqueness

    # Iterate over the adjacency list to assign labels to edges directly
    for u in graph.adj_list.keys():
        for v in graph.adj_list[u]:
            # Check if the edge is already labeled (considering undirected graph)
            if (u, v) not in graph.edge_labels and (v, u) not in graph.edge_labels:
                graph.edge_labels[(u, v)] = label
                graph.edge_labels[(v, u)] = label  # Reflect label for undirected edge
                label += 1  # Increment label for the next edge

    # No need to return vertex_labels as they are not used for edge uniqueness
    return graph.edge_labels


def main(n, m):
    graph = Graph(n, m)
    label = 1  # Initialize the edge label.

    # Iterate over the sections and vertices within each section.
    for j in range(1, m + 1):
        for i in range(1, n + 1):
            # Calculate correct node indexing within allocated range.
            node_index = (j - 1) * n + i

            # Ensure the indexing is within the bounds and corresponds to initialized nodes.
            assert node_index < graph.order, "Node index is out of bounds."

            # Add edges from the center to the outer vertices.
            graph.add_edge(0, node_index, label)
            label += 1

            # Add edges to connect each node to two other nodes in its section.
            # Carefully handle the node indexing to avoid going out of bounds.
            next_node = (j - 1) * n + (i % n) + 1
            next_next_node = (j - 1) * n + ((i + 1) % n) + 1

            graph.add_edge(node_index, next_node, label)
            label += 1
            graph.add_edge(node_index, next_next_node, label)
            label += 1

    # Use the graph's edge labels directly
    edge_labels = graph.edge_labels

    # Writing edge labels to a file
    with open('graph_labels.txt', 'w') as file:
        file.write("Edge Labels:\n")
        for edge, label in edge_labels.items():
            file.write(f"{edge}: Label {label}\n")

    # Graph visualization
    plt.figure(figsize=(12, 12))
    G = nx.Graph()

    # Adding edges to the NetworkX graph for visualization
    for (vertex1, vertex2), label in edge_labels.items():
        G.add_edge(vertex1, vertex2, label=str(label))  # Ensure label is a string

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', width=2, linewidths=1, node_size=500, font_size=12)
    edge_labels_for_drawing = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_for_drawing, font_color='red', font_size=10)
    plt.title('Homogeneous Amalgamated Star Graph with Distinct Edge Labeling')
    plt.axis('off')
    plt.show()

def test_code(n, m):
    start_time = time.time()
    # Call the main function or relevant code here with the specified value of n
    main(n,m)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time for n={n} m={m}: {execution_time} seconds")

if __name__ == "__main__":
    n = 3  # Example values; adjust as necessary for your testing
    m = 2
    test_code(n, m)
