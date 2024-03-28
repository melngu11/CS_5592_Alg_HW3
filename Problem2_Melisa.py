import networkx as nx
import matplotlib.pyplot as plt
import time 
import numpy as np
import math



class Graph:
    def __init__(self, n, m):
        """
        Initializes a graph object for a homogeneous amalgamated star graph S_n,m.
        
        Args:
            n (int): The number of star graphs amalgamated (number of arms).
            m (int): The number of leaves in each star graph.
        """
        self.n = n
        self.m = m
        self.order = m * n + 1  # Order of S_n,m is m * n + 1
        self.adj_list = {i: [] for i in range(self.order)}  # Adjacency list
        self.edge_labels = {}  # Dictionary to store edge labels

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
        self.edge_labels[(u, v)] = 0  # Initialize edge label
        self.edge_labels[(v, u)] = 0  # Ensure label is undirected

def assign_labels(graph):
    vertex_labels = {0: 1}
    edge_labels = {}
    label = 2
    for arm in range(1, graph.n + 1):
        for leaf in range(1, graph.m + 1):
            vertex = (arm - 1) * graph.m + leaf
            vertex_labels[vertex] = label
            edge_labels[(0, vertex)] = label
            edge_labels[(vertex, 0)] = label  # Reflect edge label for reverse tuple
            label += 1
    graph.edge_labels.update(edge_labels)  # Update the graph's edge labels
    return vertex_labels, edge_labels

def create_amalgamated_star_graph(n, m):
    graph = Graph(n, m)
    for arm in range(1, n + 1):
        for leaf in range(1, m + 1):
            leaf_index = (arm - 1) * m + leaf
            graph.add_edge(0, leaf_index)
    return graph

def write_to_file(filename, data):
    with open(filename, "w") as file:
        file.write(data)
        
def visualize_graph(graph, vertex_labels, edge_labels, n, m):
    """
    Visualizes the homogeneous amalgamated star graph S_n,m using matplotlib and networkx.

    Args:
        graph (Graph): The graph object representing S_n,m.
        vertex_labels (dict): The dictionary of vertex labels.
        edge_labels (dict): The dictionary of edge labels.
        n (int): The number of arms.
        m (int): The number of leaves off each arm.
    """
    plt.figure(figsize=(12, 12))
    G = nx.Graph()
    
    # Add nodes and edges to the NetworkX graph
    for u in graph.adj_list:
        G.add_node(u, label=vertex_labels[u])
        for v in graph.adj_list[u]:
            if (u, v) not in G.edges() and (v, u) not in G.edges():
                G.add_edge(u, v, label=edge_labels.get((u, v), edge_labels.get((v, u))))

    # Central node position
    pos = {0: (0, 0)}

    # Calculate the positions for branch nodes (first leaf of each arm)
    branch_angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    branch_radius = 1  # Radius for branch nodes
    branch_pos = {
        (arm - 1) * m + 1: (
            branch_radius * np.cos(angle),
            branch_radius * np.sin(angle)
        )
        for arm, angle in enumerate(branch_angles, start=1)
    }

    # Calculate the positions for the leaf nodes
    leaf_radius_increment = 0.5  # Incremental radius for each subsequent leaf
    leaf_pos = {}
    for arm in range(1, n + 1):
        for leaf in range(2, m + 1):
            base_leaf_idx = (arm - 1) * m + 1
            leaf_idx = base_leaf_idx + leaf - 1
            angle = math.atan2(*branch_pos[base_leaf_idx][::-1])
            radius = branch_radius + leaf_radius_increment * (leaf - 1)
            leaf_pos[leaf_idx] = (
                radius * np.cos(angle),
                radius * np.sin(angle)
            )

    # Combine positions and offset branch nodes slightly
    pos.update(branch_pos)
    pos.update(leaf_pos)
    
    # Draw nodes using the positions
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), 
            node_color='lightblue', node_size=300, font_size=12)
    
    # Draw edge labels
    edge_labels_dict = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_dict, font_color='red')

    # Set plot title and remove axis
    plt.title(f'Homogeneous Amalgamated Star Graph S_{{n,m}} with n={n}, m={m}')
    plt.axis('off')
    plt.show()

def main(n, m):
    graph = create_amalgamated_star_graph(n, m)
    vertex_labels, edge_labels = assign_labels(graph)
    visualize_graph(graph, vertex_labels, edge_labels, n, m)
    output_data = "Vertex Labels:\n" + "\n".join(f"Vertex {vertex}: Label {label}" for vertex, label in vertex_labels.items())
    output_data += "\n\nEdge Labels:\n" + "\n".join(f"Edge {min(edge)}-{max(edge)}: Label {label}" for edge, label in edge_labels.items())
    write_to_file("graph_labels.txt", output_data)

def test_code(n, m):
    start_time = time.time()
    main(n, m)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time for n={n}, m={m}: {execution_time} seconds")

def user_prompt():
    n = int(input("Enter the number of star graphs amalgamated (n): "))
    m = int(input("Enter the number of leaves in each star graph (m): "))
    test_code(n, m)

if __name__ == "__main__":
    user_prompt()