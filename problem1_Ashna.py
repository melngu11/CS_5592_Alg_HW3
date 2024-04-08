import math
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, n, k, order):
        """
        Initializes a graph object for homogeneous amalgamated star S(n, 3).

        Args:
            n (int): The number of inner vertices.
            k (int): k value, all vertex labels need to be less than or equal to this value
            order (int): The total number of vertices
        """
        self.n = n
        self.k = k
        self.order = order
        self.adj_list = {i: [] for i in range(order)}  # Adjacency list representation of the graph
        self.edge_weights = {} # Dictionary to store edge weights
        self.vertex_labels = {i: None for i in range(order)} # Dictionary to store vertex labels
    
    def add_edge(self, u, v, weight):
        """
        Adds an edge between two nodes with a given label.

        Args:
            u (int): One end of the edge.
            v (int): The other end of the edge.
            label (int): The label to be assigned to the edge.
        """
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
        self.edge_weights[(u, v)] = weight  # Storing the edge weight
        self.edge_weights[(v, u)] = weight  # Storing the edge weight for the opposite direction

    def vertex_k_labeling(self):
        self.vertex_labels[0] = 1
        # Case 1
        if self.n % 4 == 0 or self.n % 4 == 2 or self.n % 4 == 3:
            # labeling all the internal vertices (for this case it will go from 1, 8)
            for i in range(1, self.n + 1):
                vertex = i
                if 1 <= i <= math.ceil(self.n / 4) + 1:
                    self.vertex_labels[vertex] = 3 * i - 2
                elif math.ceil(self.n / 4) + 1 <= i <= self.n:
                    self.vertex_labels[vertex] = 2 * math.ceil(self.n / 4) + i
    
            # labeling all the external vertices (this should go from 9 to 24)
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
        return self.adj_list
    


def main():
    n = 8
    m = 3
    order = m * n + 1
    k = math.ceil((m * n + 1) / 2)
    graph = Graph(n, k, order)

    outer_verts = n

    # Adding edges for the star graph
    for i in range(1, n + 1):
        graph.add_edge(0, i, 0)  # Connect central vertex to inner vertices
        for j in range(1, m):
            outer_verts += 1
            graph.add_edge(i, outer_verts, 0) # Connect inner vertices to their external vertices
    
    vertex_labels = graph.vertex_k_labeling()
    adj_list = graph.get_adj_list()
    edge_weights = graph.calculate_edge_weights()

    print("===== Vertex Labels =====")
    for vertex, label in vertex_labels.items():
        print(f"Vertex: {vertex}, Label: {label}")
    
    print("===== Adjacency List =====")
    for vertex, neighbors in adj_list.items():
        # Convert the list of neighbors to a string for printing
        neighbors_str = ', '.join(map(str, neighbors))
        # Print the vertex and its neighbors
        print(f"Vertex: {vertex}, neighbors: [{neighbors_str}]")
    
    print("===== Edge Weights =====")
    for edge, weight in edge_weights.items():
        print(f"Edge: {edge}, Weight: {weight}")
    
    
    # Creating a NetworkX graph
    G = nx.Graph()
    G.add_nodes_from(range(order))
    # Adding edges from adjacency list
    for vertex, neighbors in adj_list.items():
        for neighbor in neighbors:
            G.add_edge(vertex, neighbor)

    pos = nx.spring_layout(G)  # positions for all nodes

    # Adding node labels
    labels = {node: str(label) for node, label in vertex_labels.items()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black')

    # Drawing the graph
    nx.draw(G, pos, with_labels=False, node_color='skyblue', node_size=1500)
    # Drawing edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weights, font_color='red')

    # Displaying the graph
    plt.show()
    


if __name__ == "__main__":
    main()






