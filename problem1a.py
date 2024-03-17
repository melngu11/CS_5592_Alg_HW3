"""
CLASS (NODE/POINTER) IMPLEMENTATION
"""


# Importing the required libraries
import networkx as nx
import matplotlib.pyplot as plt
import time as time

# Defining the Vertex class to represent vertices in the graph
class Vertex:
    def __init__(self, label):
        self.label = label  # Unique label for the vertex
        self.edges = []     # List to store the incident edges of the vertex

# Defining the Edge class to represent edges in the graph
class Edge:
    def __init__(self, label, vertex1, vertex2):
        self.label = label               # Unique label for the edge
        self.vertices = [vertex1, vertex2]  # List containing the two vertices incident to the edge

# Defining the HomogenousAmalgamatedStar class to create the graph structure
class HomogenousAmalgamatedStar:
    def __init__(self, n):
        # Creating vertices and initializing the graph's attributes
        self.vertices = [Vertex(i) for i in range(3 * n + 1)]
        self.edges = []
        self.central_vertex = self.vertices[0]
        self.outer_vertices = self.vertices[1:]

        # Connecting central vertex to outer vertices
        for v in self.outer_vertices:
            edge_label = self.calculate_edge_label()
            edge = Edge(edge_label, self.central_vertex, v)
            self.central_vertex.edges.append(edge)
            v.edges.append(edge)
            self.edges.append(edge)

        # Connecting outer vertices to form triangles
        for i in range(len(self.outer_vertices)):
            v1 = self.outer_vertices[i]
            v2 = self.outer_vertices[(i + 1) % len(self.outer_vertices)]
            v3 = self.outer_vertices[(i + 2) % len(self.outer_vertices)]
            edge_label1 = self.calculate_edge_label()
            edge_label2 = self.calculate_edge_label()
            edge1 = Edge(edge_label1, v1, v2)
            edge2 = Edge(edge_label2, v1, v3)
            v1.edges.append(edge1)
            v1.edges.append(edge2)
            v2.edges.append(edge1)
            v3.edges.append(edge2)
            self.edges.append(edge1)
            self.edges.append(edge2)

    # Method to calculate edge labels based on the current edge count
    def calculate_edge_label(self):
        edge_count = len(self.edges)
        if edge_count < (3 * len(self.vertices) + 1) / 2:
            return edge_count + 1
        else:
            return 3 * len(self.vertices) + 1 - edge_count

    # Method to convert the graph to a NetworkX graph
    def to_networkx_graph(self):
        G = nx.Graph()

        # Adding vertices to the NetworkX graph
        for vertex in self.vertices:
            G.add_node(vertex.label)

        # Adding edges to the NetworkX graph
        for edge in self.edges:
            G.add_edge(edge.vertices[0].label, edge.vertices[1].label, label=edge.label)

        return G

# Creating an instance of the HomogenousAmalgamatedStar class
n = 3

# Start the timer
start_time = time.time()
homogenous_star = HomogenousAmalgamatedStar(n)
# Converting the graph to a NetworkX graph
G = homogenous_star.to_networkx_graph()

# Drawing the graph using NetworkX and Matplotlib
pos = nx.spring_layout(G)  # Determining positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold")  # Drawing nodes
edge_labels = nx.get_edge_attributes(G, 'label')  # Getting edge labels
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # Drawing edge labels

# Calculate and print execution time
execution_time = time.time() - start_time
print("Execution time: ", execution_time, "seconds")

# Displaying the plot
plt.title("Homogenous Amalgamated Star Graph")
plt.show()



