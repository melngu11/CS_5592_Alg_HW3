import networkx as nx
import psutil
import matplotlib.pyplot as plt
import time

class Graph:
    def __init__(self, n, m):
        self.n = n  # Number of arms
        self.m = m  # Number of leaves per arm
        self.order = n * m + n + 1  # Total number of vertices
        self.adj_list = {i: [] for i in range(self.order)}
        self.edge_labels = {}
        self.vertex_labels = {}  # Stores vertex labels
        self.edge_label_counter = 1  # Initialize edge label counter

    def add_edge(self, u, v):
        if u not in self.adj_list or v not in self.adj_list:
            raise IndexError(f"Vertex index out of bounds: {u} or {v}")
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
        # Ensure vertex labels are assigned and compute edge weight as their sum
        edge_weight = self.vertex_labels.get(u, u) + self.vertex_labels.get(v, v)
        self.edge_labels[(u, v)] = edge_weight
        self.edge_labels[(v, u)] = edge_weight

    def assign_vertex_labels(self):
        self.vertex_labels = {vertex: vertex for vertex in range(self.order)}
       
    # Using power of 2 to assign labels to ensure uniqueness    
    # def assign_vertex_labels(self):
    # self.vertex_labels = {vertex: 2**vertex for vertex in range(self.order)}


    def output_labels_and_weights(self, filename='graph2_output.txt'):
        with open(filename, 'w') as file:
            file.write("Vertex Labels:\n")
            for vertex, label in self.vertex_labels.items():
                file.write(f"Vertex {vertex}: Label {label}\n")

            file.write("\nEdge Weights:\n")
            for (vertex1, vertex2), weight in self.edge_labels.items():
                file.write(f"Edge ({vertex1}, {vertex2}): Weight {weight}\n")
                
    def compute_theoretical_complexity(self):
        # The complexity is primarily dictated by the number of edges
        num_edges = self.n + self.n * self.m
        return f"O({num_edges})"
    
    def build_graph(self):
        # Connecting center to each arm
        for arm in range(1, self.n + 1):
            self.add_edge(0, arm)
            # Connecting arm to its leaves
            for leaf in range(1, self.m + 1):
                # Correctly index leaves to avoid overlap between arms
                leaf_node = self.n + (arm - 1) * self.m + leaf
                self.add_edge(arm, leaf_node)
                
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

def build_and_visualize_graph(n, m):
    graph = Graph(n, m)
    graph.build_graph()
    graph.assign_vertex_labels()
    graph.output_labels_and_weights()
    complexity = graph.compute_theoretical_complexity()
    print(f"Theoretical Time Complexity: {complexity}")

    # Visualize the graph only if it is of manageable size
    if n * m < 100:  # Adjust this threshold based on your needs
        plt.figure(figsize=(12, 12))
        G = nx.Graph()
        for (vertex1, vertex2), edge_label in graph.edge_labels.items():
            G.add_edge(vertex1, vertex2, label=str(edge_label))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', width=2, linewidths=1, node_size=500, font_size=12)
        edge_labels_for_drawing = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_for_drawing, font_color='red', font_size=10)
        plt.title('Homogeneous Amalgamated Star Graph')
        plt.axis('off')
        plt.show()
    else:
        print("Graph is too large for effective visualization.")

def main():
    user_input = input("Enter 'test' to find the hardware limits or 'build' to specify n and m: ").strip().lower()

    if user_input == "test":
        print("Testing hardware limits. This might take a while...")
        max_n, max_m = test_limits(1, 1, 1)  # Start with n = 1, m = 1 and increment by 1
        print(f"Maximum supported n: {max_n}, Maximum supported m: {max_m}")
    elif user_input == "build":
        n = int(input("Enter the number of arms (n): "))
        m = int(input("Enter the number of leaves per arm (m): "))
        build_and_visualize_graph(n, m)
    else:
        print("Invalid input. Please enter 'test' or 'build'.")

if __name__ == "__main__":
    main()
