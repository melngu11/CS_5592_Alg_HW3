"""
ADJACENCY LIST IMPLEMENTATION
"""
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, n):
        self.n = n
        self.vertices = 3 * n + 1
        self.adjacency_list = {v: [] for v in range(1, self.vertices + 1)}
        self.labels = {v: None for v in range(1, self.vertices + 1)}
        self.weights = {}
    
    def add_edge(self, u, v, weight):
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)
        self.weights[(u, v)] = weight
        self.weights[(v, u)] = weight
    
    def assign_labels(self):
        k = (3 * self.n + 1) // 2
        labels_used = set()
        for v in range(1, self.vertices + 1):
            neighbors_labels = {self.labels[u] for u in self.adjacency_list[v] if self.labels[u] is not None}
            available_labels = set(range(1, k + 1)) - neighbors_labels
            if available_labels:
                label = min(available_labels)
            else:
                label = max(labels_used) + 1
            self.labels[v] = label
            labels_used.add(label)
        
    def print_labels_and_weights(self):
        print("Vertex Labels:")
        for v, label in self.labels.items():
            print(f"Vertex {v}: Label {label}")
        print("\nEdge Weights:")
        for edge, weight in self.weights.items():
            print(f"Edge {edge}: Weight {weight}")

# Test
n = 3
star_graph = Graph(n)

# Adding edges and weights
for i in range(1, star_graph.vertices):
    star_graph.add_edge(i, star_graph.vertices, i)

# Assigning labels
star_graph.assign_labels()

# Printing labels and weights
star_graph.print_labels_and_weights()

# Create a graph from the adjacency list
G = nx.Graph(star_graph.adjacency_list)

# Draw the graph
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=1500)
labels = {i: star_graph.labels[i] for i in range(1, star_graph.vertices + 1)}
nx.draw_networkx_labels(G, pos, labels=labels)

# Draw edge weights
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
