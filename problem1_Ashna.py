class Graph:
    def __init__(self, n):
        """
        Initializes a graph object with a given number of nodes.

        Args:
            n (int): The number of nodes.
        """
        self.n = n
        self.adj_list = {i: [] for i in range(3 * n + 1)}  # Adjacency list representation of the graph
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
        self.edge_labels[(u, v)] = label  # Storing the edge label
        self.edge_labels[(v, u)] = label  # Storing the edge label for the opposite direction


def assign_labels(graph):
    """
    Assigns vertex and edge labels to the graph using edge irregular k-labeling and vertex k-labeling scheme.

    Edge Irregular k-labeling:
    assigns labels to both vertices and edges such that the maximum label on any edge incident to a vertex is the label of that vertex.

    Vertex k-labeling:
    assigns labels to vertices such that the maximum label on any edge incident to a vertex is at most k.

    Args:
        graph (Graph): The graph object to which labels will be assigned.

    Returns:
        tuple: A tuple containing dictionaries of vertex labels and edge labels.
    """
    vertex_labels = {}  # Dictionary to store vertex labels
    edge_labels = {}  # Dictionary to store edge labels
    k = (3 * graph.n + 1) // 2

    # Labeling the center vertex
    vertex_labels[0] = min(graph.n + 1, k)

    # Labeling the outer vertices
    for i in range(1, graph.n + 1):
        label = min(i, k)
        vertex_labels[i] = label
        vertex_labels[graph.n + i] = label
        vertex_labels[2 * graph.n + i] = label

    # Adjust vertex 0 labeling for even and odd n
    if graph.n % 2 == 0:  # When n is even
        vertex_labels[0] = 3 * graph.n // 2
    else:  # When n is odd
        vertex_labels[0] = (3 * graph.n + 1) // 2

    # Assigning edge labels
    for vertex, neighbors in graph.adj_list.items():
        for neighbor in neighbors:
            edge_label = min(vertex_labels[vertex], vertex_labels[neighbor])  # Use minimum of incident vertex labels
            edge_labels[(vertex, neighbor)] = edge_label
            edge_labels[(neighbor, vertex)] = edge_label

    return vertex_labels, edge_labels



def verify_labels(graph, vertex_labels, edge_labels):
    """
    Verifies the correctness of vertex and edge labels.

    Args:
        graph (Graph): The graph object.
        vertex_labels (dict): Dictionary containing vertex labels.
        edge_labels (dict): Dictionary containing edge labels.

    Raises:
        AssertionError: If the labels are incorrect.
    """
    for vertex, neighbors in graph.adj_list.items():
        # Verify vertex labeling
        max_edge_label = max(edge_labels[(vertex, neighbor)] for neighbor in neighbors)
        assert vertex_labels[vertex] == max_edge_label, f"Vertex {vertex} labeling is incorrect"

        # Verify edge labeling
        for neighbor in neighbors:
            assert edge_labels[(vertex, neighbor)] <= max(vertex_labels[vertex], vertex_labels[neighbor]), \
                f"Edge label between {vertex} and {neighbor} is incorrect"


def main(n):
    # Initialize graph
    graph = Graph(n)

    # Adding edges for the star graph
    for i in range(1, n + 1):
        graph.add_edge(0, i, 0)
        graph.add_edge(i, n + i, 0)
        graph.add_edge(i, 2 * n + i, 0)

    # Assign labels to vertices and edges
    vertex_labels, edge_labels = assign_labels(graph)

    # Output labels
    print("Vertex Labels:")
    for vertex, label in vertex_labels.items():
        print(f"Vertex {vertex}: Label {label}")
    print("Edge Labels:")
    for edge, label in edge_labels.items():
        print(f"Edge {edge}: Label {label}")

    # Verify labels
    verify_labels(graph, vertex_labels, edge_labels)


if __name__ == "__main__":
    # Test the code for a specific value of n
    n = 5  # Adjust the value of n as needed
    main(n)
