"""
ADJACENCY LIST IMPLENTATION
"""

# Importing the necessary libraries
from collections import deque
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
    def assign_labels_greedy(self):
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
        # Method to assign labels to vertices using backtracking with constraint satisfaction
    def assign_labels_backtracking(self):
        # Calculating the maximum label allowed based on the formula provided
        k = (3 * self.n + 1) // 2
        
        # Create a list to store the solution
        solution = [None] * (self.vertices + 1)
        
        # Initialize the labels_used set
        labels_used = set()
        
        # Call the backtracking function to find a valid assignment
        self.backtrack(1, solution, labels_used, k)
        
        # Update the labels dictionary with the solution
        for v in range(1, self.vertices + 1):
            self.labels[v] = solution[v]

    # Backtracking function to assign labels recursively
    def backtrack(self, v, solution, labels_used, k):
        # Base case: if all vertices are assigned labels
        if v == self.vertices + 1:
            return True  # Solution found
        
        # Get the set of labels used by neighboring vertices
        neighbors_labels = {solution[u] for u in self.adjacency_list[v] if solution[u] is not None}
        
        # Find available labels that are not used by neighboring vertices
        available_labels = set(range(1, k + 1)) - neighbors_labels
        
        # Try assigning each available label to the current vertex
        for label in sorted(available_labels):
            solution[v] = label
            labels_used.add(label)
            
            # Recursively call backtrack for the next vertex
            if self.backtrack(v + 1, solution, labels_used, k):
                return True  # Solution found
            
            # Backtrack: remove the label and try the next one
            solution[v] = None
            labels_used.remove(label)
        
        return False  # No solution found


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
    
    def visualize_graph(self):
        G = nx.Graph(self.adjacency_list)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500)
        labels = {i: self.labels[i] for i in range(1, self.vertices + 1)}
        nx.draw_networkx_labels(G, pos, labels=labels, font_color='black')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        nx.draw_networkx_edges(G, pos)
        plt.show()
    
    def bfs(self, start):
        visited = set()
        queue = deque()
        queue.append((start, [start]))  # Keep track of the path
        visited.add(start)
        while queue:
            vertex, path = queue.popleft()
            print(vertex, end=' ')
            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))  # Append neighbor to the current path
                    visited.add(neighbor)
        return path  # Return the path taken during BFS traversal
    
    def dfs(self, start):
        visited = set()
        stack = [(start, [start])]  # Stack to track current vertex and path
        path = []  # Variable to store the final path
        while stack:
            vertex, current_path = stack.pop()
            if vertex not in visited:
                path = current_path  # Update the path
                visited.add(vertex)
                print(vertex, end=' ')
                for neighbor in self.adjacency_list[vertex]:
                    stack.append((neighbor, current_path + [neighbor]))  # Append neighbor to the current path
        return path  # Return the path taken during DFS traversal


# Test code to create and visualize the graph
# Creating a graph object with n = 3
n = 4
star_graph = Graph(n)

# Adding edges and weights to the graph
for i in range(1, star_graph.vertices):
    star_graph.add_edge(i, star_graph.vertices, i)

# Assigning labels to the vertices
star_graph.assign_labels_greedy()
# star_graph.assign_labels_backtracking()

# Printing labels and weights of the graph
star_graph.print_labels_and_weights()
star_graph.visualize_graph()

start_vertex = 1
print("\nBFS Traversal:")
path = star_graph.bfs(start_vertex)
print("\nPath taken during BFS traversal:", path)

print("\nDFS Traversal:")
path = star_graph.dfs(start_vertex)
print("\nPath taken during DFS traversal:", path)

