import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, n, m):
        self.n = n  # Number of arms
        self.m = m  # Number of leaves per arm
        self.order = n * m + n + 1  # Total number of vertices
        self.adj_list = {i: [] for i in range(self.order)}
        self.edge_labels = {}

    def add_edge(self, u, v, label):
        # Check if the edge already exists to avoid duplication
        if (u, v) not in self.edge_labels and (v, u) not in self.edge_labels:
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
            self.edge_labels[(u, v)] = label
            self.edge_labels[(v, u)] = label

def main(n, m):
    graph = Graph(n, m)
    edge_label = 1  # Initialize the edge label.

    # Labeling central vertex to arms edges distinctly
    for arm in range(1, n + 1):
        graph.add_edge(0, arm, edge_label)
        edge_label += 1

    # Labeling edges from arms to leaves
    # Ensure each arm to leaf edge has a unique label
    for arm in range(1, n + 1):
        for leaf in range(1, m + 1):
            leaf_node = n + (arm - 1) * m + leaf
            graph.add_edge(arm, leaf_node, edge_label)
            edge_label += 1

    # Prepare for visualization
    plt.figure(figsize=(12, 12))
    G = nx.Graph()

    # Add nodes and labeled edges to the NetworkX graph
    for (vertex1, vertex2), edge_label in graph.edge_labels.items():
        G.add_edge(vertex1, vertex2, label=str(edge_label))

    # Position nodes using spring layout and draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', width=2, linewidths=1, node_size=500, font_size=12)
    edge_labels_for_drawing = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_for_drawing, font_color='red', font_size=10)

    # Display the graph
    plt.title('Homogeneous Amalgamated Star Graph with Edge-Irregular Labeling')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    n = 12  # Number of arms
    m = 3  # Number of leaves per arm
    main(n, m)
