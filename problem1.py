import networkx as nx
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, label):
        self.label = label
        self.edges = []


class Edge:
    def __init__(self, label, vertex1, vertex2):
        self.label = label
        self.vertices = [vertex1, vertex2]


class HomogenousAmalgamatedStar:
    def __init__(self, n):
        self.vertices = [Vertex(i) for i in range(3 * n + 1)]
        self.edges = []

        self.central_vertex = self.vertices[0]
        self.outer_vertices = self.vertices[1:]

        # Connect central vertex to outer vertices
        for v in self.outer_vertices:
            edge_label = self.calculate_edge_label()
            edge = Edge(edge_label, self.central_vertex, v)
            self.central_vertex.edges.append(edge)
            v.edges.append(edge)
            self.edges.append(edge)

        # Connect outer vertices to form triangles
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

    def calculate_edge_label(self):
        edge_count = len(self.edges)
        if edge_count < (3 * len(self.vertices) + 1) / 2:
            return edge_count + 1
        else:
            return 3 * len(self.vertices) + 1 - edge_count

    def to_networkx_graph(self):
        G = nx.Graph()

        # Add vertices
        for vertex in self.vertices:
            G.add_node(vertex.label)

        # Add edges
        for edge in self.edges:
            G.add_edge(edge.vertices[0].label, edge.vertices[1].label, label=edge.label)

        return G

# Create a HomogenousAmalgamatedStar instance
n = 3
homogenous_star = HomogenousAmalgamatedStar(n)

# Convert the graph to a NetworkX graph
G = homogenous_star.to_networkx_graph()

# Draw the graph
pos = nx.spring_layout(G)  # Positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold")
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Show the plot
plt.title("Homogenous Amalgamated Star Graph")
plt.show()
