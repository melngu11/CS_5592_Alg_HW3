import time as time

class Vertex:
    def __init__(self, label):
        # Initialize a Vertex object with a label and an empty list to store incident edges
        self.label = label
        self.edges = []

class Edge:
    def __init__(self, label, vertex1, vertex2):
        # Initialize an Edge object with a label and a list containing the two incident vertices
        self.label = label
        self.vertices = [vertex1, vertex2]

class HomogenousAmalgamatedStar:
    def __init__(self, n):
        # Initialize a HomogenousAmalgamatedStar object with vertices, edges, and other attributes
        self.vertices = [Vertex(i) for i in range(3 * n + 1)]  # Create vertices
        self.edges = []  # Initialize an empty list to store edges
        self.central_vertex = self.vertices[0]  # Set the central vertex
        self.outer_vertices = self.vertices[1:]  # Set the outer vertices

        stack = []  # Initialize a stack to keep track of vertices
        edge_count = 1  # Initialize the edge count

        # Connect the central vertex to outer vertices
        for v in self.outer_vertices:
            edge = Edge(edge_count, self.central_vertex, v)  # Create an edge
            self.central_vertex.edges.append(edge)  # Add the edge to the central vertex
            v.edges.append(edge)  # Add the edge to the outer vertex
            self.edges.append(edge)  # Add the edge to the list of edges
            edge_count += 1  # Increment the edge count

        # Connect outer vertices to form triangles
        for i in range(len(self.outer_vertices)):
            v1 = self.outer_vertices[i]  # Current outer vertex
            v2 = self.outer_vertices[(i + 1) % len(self.outer_vertices)]  # Next outer vertex
            v3 = self.outer_vertices[(i + 2) % len(self.outer_vertices)]  # Second next outer vertex

            # Create two edges forming a triangle and add them to the stack
            edge1 = Edge(edge_count, v1, v2)
            edge2 = Edge(edge_count + 1, v1, v3)
            stack.append((v1, v2, v3))
            stack.append((v1, v3, v2))

            # Update vertex edges and add edges to the list of edges
            v1.edges.append(edge1)
            v1.edges.append(edge2)
            v2.edges.append(edge1)
            v3.edges.append(edge2)
            self.edges.append(edge1)
            self.edges.append(edge2)

            edge_count += 2  # Increment the edge count

        # Edge irregular k-labeling
        while stack:
            v1, v2, v3 = stack.pop()  # Pop vertices from the stack
            # Create two edges forming a triangle and update vertex edges and the list of edges
            edge1 = Edge(edge_count, v1, v2)
            edge2 = Edge(edge_count + 1, v1, v3)
            v1.edges.append(edge1)
            v1.edges.append(edge2)
            v2.edges.append(edge1)
            v3.edges.append(edge2)
            self.edges.append(edge1)
            self.edges.append(edge2)
            edge_count += 2  # Increment the edge count

    def print_graph_info(self):
        # Print information about the graph, including vertices, edges, and their connections
        print("Number of Vertices:", len(self.vertices))
        print("Number of Edges:", len(self.edges))

        print("\nVertices:")
        for vertex in self.vertices:
            print("Vertex:", vertex.label)
            print("Connected Edges:", [edge.label for edge in vertex.edges])

        print("\nEdges:")
        for edge in self.edges:
            print("Edge:", edge.label)
            print("Connected Vertices:", [vertex.label for vertex in edge.vertices])
            print()

# Create a HomogenousAmalgamatedStar instance
n = 3

# Start the timer
start_time = time.time()
homogenous_star = HomogenousAmalgamatedStar(n)

# Print graph information
homogenous_star.print_graph_info()

# Calculate and print execution time
execution_time = time.time() - start_time
print("Execution time: ", execution_time, "seconds")
