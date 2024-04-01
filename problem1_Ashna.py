import networkx as nx
import matplotlib.pyplot as plt
import math

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
    


def edge_irregular_k_labeling(graph, vertex_labels):
    """
    Assigns edge labels to the graph using edge irregular k-labeling scheme.

    Args:
        graph (Graph): The graph object to which labels will be assigned.

    Returns:
        dict: Dictionary containing edge labels.
    """
    edge_labels = {}
    
    for u in range(graph.order):
        for v in graph.adj_list[u]:
            edge_label = vertex_labels[u] + vertex_labels[v]
            edge_labels[(u, v)] = edge_label
            edge_labels[(v, u)] = edge_label

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
    
    for i in range(graph.order):
        vertex_labels[i] = min(i, k)

    return vertex_labels



def visualize_graph(graph, edge_labels, vertex_labels):
    """
    Visualizes the graph using NetworkX.

    Args:
        graph (Graph): The graph object.
        edge_labels (dict): Dictionary containing edge labels.
    """
    G = nx.Graph()
    G.add_nodes_from(range(graph.order))

    for u, neighbors in graph.adj_list.items():
        for v in neighbors:
            G.add_edge(u, v, label=edge_labels[(u, v)])

    pos = nx.spring_layout(G)  # Position nodes using the spring layout algorithm
    nx.draw(G, pos, with_labels=False, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')

    # Draw vertex labels
    nx.draw_networkx_labels(G, pos, labels=vertex_labels, font_color='black', font_size=10)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Homogeneous Amalgamated Star S(n, 3) Visualization")
    plt.show()

        


def main(n):
    # Initialize graph
    graph = Graph(n)

    # Adding edges for the homogeneous amalgamated star
    for i in range(1, n + 1):
        graph.add_edge(0, i, 0)
        graph.add_edge(i, n + i, 0)
        graph.add_edge(i, 2 * n + i, 0)

    # Assign labels to vertices and edges
    vertex_labels = vertex_k_labeling(graph)
    edge_labels = edge_irregular_k_labeling(graph, vertex_labels)

    # Output labels (if needed)
    visualize_graph(graph, edge_labels, vertex_labels)

    return graph, vertex_labels, edge_labels

if __name__ == "__main__":
    n = 3  # Adjust the value of n as needed
    graph, vertex_labels, edge_labels = main(n)
    print("Vertex Labels:")
    for vertex, label in vertex_labels.items():
        print(f"Vertex {vertex}: Label {label}")
    print("Edge Labels:")
    for edge, label in edge_labels.items():
        print(f"Edge {edge}: Label {label}")


    
