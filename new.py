# Importing necessary libraries
import math
import networkx as nx
import matplotlib.pyplot as plt
import time
import psutil

# Class definition for a graph
class Graph:
    def __init__(self, n, m):
        """
        Initializes a graph object for homogeneous amalgamated star S(n, 3).

        Args:
            n (int): The number of inner vertices.
            k (int): The maximum value a vertex label can take.
            order (int): The total number of vertices.
        """
        # Initializing graph parameters
        self.n = n
        self.m = m
        self.k = math.ceil((m * n + 1) / 2)
        self.order = math.ceil(m * n + 1)
        # Initializing data structures to represent the graph
        self.adj_list = {i: [] for i in range(self.order)}  # Adjacency list representation of the graph
        self.edge_weights = {}  # Dictionary to store edge weights
        self.vertex_labels = {i: None for i in range(self.order)}  # Dictionary to store vertex labels
    
    def add_edge(self, u, v, weight):
        """
        Adds an edge between two nodes with a given weight.

        Args:
            u (int): One end of the edge.
            v (int): The other end of the edge.
            weight (int): The weight to be assigned to the edge.
        """
        # Adding edge to the adjacency list
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
        # Storing edge weight in both directions
        self.edge_weights[(u, v)] = weight
        self.edge_weights[(v, u)] = weight

    def vertex_k_labeling(self):
        """
        Calculates vertex labels for the graph.
        """
        # Setting label for central vertex
        self.vertex_labels[0] = 1

        # Case 1
        if self.n % 4 == 0 or self.n % 4 == 2 or self.n % 4 == 3:
            # Labeling internal vertices
            for i in range(1, self.n + 1):
                vertex = i
                if 1 <= i <= math.ceil(self.n / 4) + 1:
                    self.vertex_labels[vertex] = 3 * i - 2
                elif math.ceil(self.n / 4) + 1 <= i <= self.n:
                    self.vertex_labels[vertex] = 2 * math.ceil(self.n / 4) + i
    
            # Labeling external vertices
            vertex += 1
            for i in range(1, (math.ceil(self.n / 4) + 1)):
                for j in range(1, 3):  
                    self.vertex_labels[vertex] =  j + 1
                    vertex = vertex + 1
   
            for i in range((math.ceil(self.n / 4) + 1), self.n + 1):
                for j in range(1, 3):
                    self.vertex_labels[vertex] = self.n + i + j - 1 - 2 * math.ceil(self.n / 4)
                    vertex = vertex + 1
        
        return self.vertex_labels
    
    def calculate_edge_weights(self):
        """
        Calculates edge weights based on vertex labels and adjacency list.
        """
        for vertex, neighbors in self.adj_list.items():
            for neighbor in neighbors:
                # Calculate edge weight by summing up the labels of the two vertices
                weight = self.vertex_labels[vertex] + self.vertex_labels[neighbor]
                self.edge_weights[(vertex, neighbor)] = weight
                self.edge_weights[(neighbor, vertex)] = weight
        
        return self.edge_weights
    
    def get_adj_list(self):
        """
        Returns the adjacency list of the graph.
        """
        return self.adj_list
    def visualize_graph(self):
        """
        Visualizes the graph using NetworkX and Matplotlib.
        """
        G = nx.Graph()
        G.add_nodes_from(range(self.order))

        # Adding edges from the internal adjacency list
        for vertex, neighbors in self.adj_list.items():
            for neighbor in neighbors:
                G.add_edge(vertex, neighbor)

        pos = nx.spring_layout(G)  # positions for all nodes

        # Preparing and adding node labels
        labels = {node: str(label) for node, label in self.vertex_labels.items()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black')

        # Extract edge labels for unique edge weights, assuming self.edge_labels is correctly populated
        edge_weights = {(u, v): f"{w}" for (u, v), w in self.edge_labels.items()}

        # Drawing the graph
        nx.draw(G, pos, with_labels=False, node_color='skyblue', node_size=1500)

        # Drawing edge labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weights, font_color='red')

        # Displaying the graph
        plt.show()
    
def available_memory():
    return psutil.virtual_memory().available

def test_limits(initial_n, initial_m, base_increment, memory_limit_ratio=0.8, timeout_seconds=300):
    n, m = initial_n, initial_m
    increment = base_increment
    max_n, max_m = n, m
    memory_limit = available_memory() * memory_limit_ratio
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout_seconds:
            print("Testing timeout reached. Returning the last found values.")
            break

        try:
            graph = Graph(n, m)
            graph.build_graph()

            # Estimate current memory usage
            current_memory_usage = psutil.Process().memory_info().rss

            if current_memory_usage > memory_limit:
                if increment > 1:
                    # If the limit is reached, step back and reduce increment
                    n -= increment
                    m -= increment
                    increment = 1  # Fine-tune with smallest possible increment
                    continue
                break  # Break if already at smallest increment

            max_n, max_m = n, m
            n += increment
            m += increment  # Increment both n and m

        except MemoryError:
            break

    return max_n, max_m

# Main function modifications for clarity and consistency:

def main():
    user_input = input("Enter 'test' to find the hardware limits or 'build' to specify n and m: ").strip().lower()

    if user_input == "test":
        print("Testing hardware limits. This might take a while...")
        max_n, max_m = test_limits(1, 1, 1)
        print(f"Maximum supported n: {max_n}, Maximum supported m: {max_m}")
    elif user_input == "build":
        n = int(input("Enter the number of arms (n): "))
        m = int(input("Enter the number of leaves per arm (m): "))
        graph = Graph(n, m)
        
        # Edge addition adjusted to include all leaves for each arm
        outer_verts = n
        for i in range(1, n + 1):
            graph.add_edge(0, i, 0)  # Central to inner vertices
            for j in range(1, m + 1):  # Correctly account for all m leaves
                outer_verts += 1
                graph.add_edge(i, outer_verts, 0)  # Inner vertex to leaves

        # Compute labels and weights
        vertex_labels = graph.vertex_k_labeling()
        edge_weights = graph.calculate_edge_weights()

        # Visualize the graph
        graph.visualize_graph()
    else:
        print("Invalid input. Please enter 'test' or 'build'.")

if __name__ == "__main__":
    main()
