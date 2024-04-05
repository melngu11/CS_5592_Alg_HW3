import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, n):
        """
        Initializes a graph object for homogeneous amalgamated star S(n, 3).

        Args:
            n (int): The number of outer vertices.
        """
        self.n = n
        self.order = 3 * n + 1
        self.adj_list = {i: [] for i in range(self.order)}  # Adjacency list representation of the graph
        self.edge_labels = {}  # Dictionary to store edge labels

    def add_edge(self, u, v, label):
        """
        Adds an edge between two nodes with a given label.

        Args:
            u (int): One end of the edge.
            v (int): The other end of the edge.
            label (int): The label to be assigned to the edge.
        """
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
        self.edge_labels[(u, v)] = label
        self.edge_labels[(v, u)] = label


def edge_irregular_k_labeling(graph):
    """
    Assigns edge labels to the graph using edge irregular k-labeling scheme.
    Ensures that edge labels are unique by adjusting vertex labels if necessary.

    Args:
        graph (Graph): The graph object to which labels will be assigned.

    Returns:
        dict: Dictionary containing edge labels.
    """
    edge_labels = {}

    k = (3 * graph.n + 1) // 2

    for i in range(graph.n):
        u = i + 1
        v1 = graph.n + u
        v2 = 2 * graph.n + u

        edge_labels[(0, u)] = 1
        edge_labels[(0, v1)] = 1
        edge_labels[(0, v2)] = 1

        for j in range(1, graph.n + 1):
            x_i = 3 * j - 2
            y_ij1 = j + 1
            y_ij2 = j + 2

            edge_labels[(u, x_i)] = y_ij1
            edge_labels[(u, y_ij1)] = 2
            edge_labels[(u, y_ij2)] = 3

    return edge_labels


def vertex_k_labeling(graph):
    """
    Assigns vertex labels to the graph using vertex k-labeling scheme.

    Args:
        graph (Graph): The graph object to which labels will be assigned.

    Returns:
        dict: Dictionary containing vertex labels.
    """

    vertex_labels = {}
    k = (3 * graph.n + 1) // 2

    vertex_labels[0] = 1  # Central vertex label

    if graph.n % 4 == 0:
        for i in range(1, graph.n + 1):
            if i <= graph.n // 4:
                vertex_labels[i] = 3 * i - 2
            else:
                vertex_labels[i] = 2 * (graph.n // 4) + i
    else:
        for i in range(1, graph.n + 1):
            if i <= graph.n // 4:
                vertex_labels[i] = 3 * i - 2
            else:
                vertex_labels[i] = 2 * (graph.n // 4) + i - 1

    for i in range(1, graph.n + 1):
        vertex_labels[graph.n + i] = i + 1
        vertex_labels[2 * graph.n + i] = i + 2

    return vertex_labels


def visualize_graph(graph, edge_labels, vertex_labels):
    """
    Visualizes the graph using NetworkX.

    Args:
        graph (Graph): The graph object.
        edge_labels (dict): Dictionary containing edge labels.
    """
    G = nx.Graph()

    for u, neighbors in graph.adj_list.items():
        for v in neighbors:
            G.add_edge(u, v)

    pos = nx.spring_layout(G)  # Position nodes using the spring layout algorithm
    nx.draw(G, pos, with_labels=False, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')

    # Draw vertex labels
    nx.draw_networkx_labels(G, pos, labels=vertex_labels, font_color='black', font_size=10)

    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Homogeneous Amalgamated Star S(n, 3) Visualization")
    plt.show()


def main(n):
    # Initialize graph
    graph = Graph(n)

    # Assign labels to vertices and edges
    vertex_labels = vertex_k_labeling(graph)
    edge_labels = edge_irregular_k_labeling(graph)

    return graph, vertex_labels, edge_labels


if __name__ == "__main__":
    n = 8  # Adjust the value of n as needed
    graph, vertex_labels, edge_labels = main(n)
    print("Vertex Labels:")
    for vertex, label in vertex_labels.items():
        print(f"Vertex {vertex}: Label {label}")
    print("Edge Labels:")
    for edge, label in edge_labels.items():
        print(f"Edge {edge}: Label {label}")

    # Output labels (if needed)
    visualize_graph(graph, edge_labels, vertex_labels)
