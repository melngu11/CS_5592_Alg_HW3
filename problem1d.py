# Importing the necessary libraries
import networkx as nx
import matplotlib.pyplot as plt

# Defining a class for the Graph
class Graph:
    # Constructor to initialize the graph with the given number of nodes (vertices)
    def __init__(self, n):
        self.n = n
        self.vertices = 3 * n + 1  # Calculating the total number of vertices in the graph
        # Initializing the adjacency list, labels, and weights dictionaries for the graph
        self.adjacency_list = {v: [] for v in range(1, self.vertices + 1)}
        self.labels = {v: None for v in range(1, self.vertices + 1)}
        self.weights = {}

    # Method to add an edge between two vertices with a given weight
    def add_edge(self, u, v, weight):
        # Adding the edge to the adjacency list in both directions
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)
        # Storing the weight of the edge in the weights dictionary
        self.weights[(u, v)] = weight
        self.weights[(v, u)] = weight

    # Method to assign labels to vertices using a specific algorithm
    def assign_labels(self):
        # Calculating the maximum label allowed based on the formula provided
        k = (3 * self.n + 1) // 2
        # Set to keep track of labels already used
        labels_used = set()
        # Iterating over each vertex in the graph
        for v in range(1, self.vertices + 1):
            # Finding labels of neighboring vertices that are already assigned
            neighbors_labels = {self.labels[u] for u in self.adjacency_list[v] if self.labels[u] is not None}
            # Finding available labels that are not used by neighboring vertices
            available_labels = set(range(1, k + 1)) - neighbors_labels
            # If there are available labels, assign the minimum one
            if available_labels:
                label = min(available_labels)
            # Otherwise, assign a new label not used by neighboring vertices
            else:
                label = max(labels_used) + 1
            # Assigning the label to the current vertex and updating the set of used labels
            self.labels[v] = label
            labels_used.add(label)

    # Method to print the labels of vertices and weights of edges
    def print_labels_and_weights(self):
        # Printing vertex labels
        print("Vertex Labels:")
        for v, label in self.labels.items():
            print(f"Vertex {v}: Label {label}")
        # Printing edge weights
        print("\nEdge Weights:")
        for edge, weight in self.weights.items():
            print(f"Edge {edge}: Weight {weight}")

# Test code to create and visualize the graph
# Creating a graph object with n = 3
n = 3
star_graph = Graph(n)

# Adding edges and weights to the graph
for i in range(1, star_graph.vertices):
    star_graph.add_edge(i, star_graph.vertices, i)

# Assigning labels to the vertices
star_graph.assign_labels()

# Printing labels and weights of the graph
star_graph.print_labels_and_weights()

# Creating a graph object from the adjacency list using networkx
G = nx.Graph(star_graph.adjacency_list)

# Drawing the graph with vertex labels and edge weights using matplotlib
pos = nx.spring_layout(G)  # Positions for all nodes
nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=1500)  # Drawing nodes
# Drawing labels for nodes
labels = {i: star_graph.labels[i] for i in range(1, star_graph.vertices + 1)}
nx.draw_networkx_labels(G, pos, labels=labels)
# Drawing labels for edges
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Displaying the graph
plt.show()

