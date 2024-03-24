import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, n):
        self.n = n
        self.adj_list = {i: [] for i in range(3 * n + 1)}
        self.edge_labels = {}

    def add_edge(self, u, v, label):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
        self.edge_labels[(u, v)] = label
        self.edge_labels[(v, u)] = label

def assign_labels(graph):
    vertex_labels = {}
    edge_labels = {}
    k = (3 * graph.n + 1) // 2
    
    # Greedy labeling starting from central vertex
    vertex_labels[0] = min(graph.n + 1, k)  # Labeling the center vertex
    for i in range(1, graph.n + 1):
        vertex_labels[i] = min(i, k)
        vertex_labels[graph.n + i] = min(i, k)
        vertex_labels[2 * graph.n + i] = min(i, k)

    # Assigning edge labels
    edge_label_counter = 1
    for vertex, neighbors in graph.adj_list.items():
        for neighbor in neighbors:
            edge_label = max(vertex_labels[vertex], vertex_labels[neighbor])
            edge_labels[(vertex, neighbor)] = edge_label
            edge_labels[(neighbor, vertex)] = edge_label

    return vertex_labels, edge_labels

def main():
    n = int(input("Enter the value of n: "))
    graph = Graph(n)

    # Adding edges for the star graph
    for i in range(1, n + 1):
        graph.add_edge(0, i, 0)
        graph.add_edge(i, n + i, 0)
        graph.add_edge(i, 2 * n + i, 0)

    vertex_labels, edge_labels = assign_labels(graph)

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

    # Output labels
    print("Vertex Labels:")
    for vertex, label in vertex_labels.items():
        print(f"Vertex {vertex}: Label {label}")
    print("Edge Labels:")
    for edge, label in edge_labels.items():
        print(f"Edge {edge}: Label {label}")

if __name__ == "__main__":
    main()
