import networkx as nx
import matplotlib.pyplot as plt
import time 


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
    Assigns vertex and edge labels to the graph using edge irregular k-labeling scheme.

    Edge Irregular k-labeling:
    assigns labels to both vertices and edges such that the maximum label on any edge incident to a vertex is the label of that vertex. 
    
    Args:
        graph (Graph): The graph object to which labels will be assigned.
        
    Returns:
        tuple: A tuple containing dictionaries of vertex labels and edge labels.
    """
    vertex_labels = {}  # Dictionary to store vertex labels
    edge_labels = {}  # Dictionary to store edge labels
    k = (3 * graph.n + 1) // 2
    
    # Greedy labeling starting from central vertex
    vertex_labels[0] = min(graph.n + 1, k)  # Labeling the center vertex
    for i in range(1, graph.n + 1):
        vertex_labels[i] = min(i, k)
        vertex_labels[graph.n + i] = min(i, k)
        vertex_labels[2 * graph.n + i] = min(i, k)

    # Assigning edge labels
    for vertex, neighbors in graph.adj_list.items():
        for neighbor in neighbors:
            edge_label = max(vertex_labels[vertex], vertex_labels[neighbor])
            edge_labels[(vertex, neighbor)] = edge_label
            edge_labels[(neighbor, vertex)] = edge_label

    return vertex_labels, edge_labels



def main(n):
    # Number of outer vertices in the star
    # n = int(input("Enter the value of n: "))

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
    
    '''
        # Visualize graph using networkx library
    G = nx.Graph()
    for vertex, neighbors in graph.adj_list.items():
        for neighbor in neighbors:
            G.add_edge(vertex, neighbor, label=edge_labels[(vertex, neighbor)])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, labels=vertex_labels, node_size=1000)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title('Homogeneous Amalgamated Star Graph with Edge Irregular K-Labeling')
    plt.show()
    
    '''


def test_code(n):
    start_time = time.time()
    # Call the main function or relevant code here with the specified value of n
    main(n)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time for n={n}: {execution_time} seconds")


if __name__ == "__main__":
    # Test the code for increasing values of n
    for n in range(3, 1000, 20): # Adjust the range and step size as needed
        test_code(n)
