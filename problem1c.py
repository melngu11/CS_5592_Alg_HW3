"""
STACK IMPLENTATION
"""


import time as time

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

        stack = []
        edge_count = 1

        # Connect central vertex to outer vertices
        for v in self.outer_vertices:
            edge = Edge(edge_count, self.central_vertex, v)
            self.central_vertex.edges.append(edge)
            v.edges.append(edge)
            self.edges.append(edge)
            edge_count += 1

        # Connect outer vertices to form triangles
        for i in range(len(self.outer_vertices)):
            v1 = self.outer_vertices[i]
            v2 = self.outer_vertices[(i + 1) % len(self.outer_vertices)]
            v3 = self.outer_vertices[(i + 2) % len(self.outer_vertices)]

            edge1 = Edge(edge_count, v1, v2)
            edge2 = Edge(edge_count + 1, v1, v3)

            stack.append((v1, v2, v3))
            stack.append((v1, v3, v2))

            v1.edges.append(edge1)
            v1.edges.append(edge2)
            v2.edges.append(edge1)
            v3.edges.append(edge2)

            self.edges.append(edge1)
            self.edges.append(edge2)

            edge_count += 2

        # Edge irregular k-labeling
        while stack:
            v1, v2, v3 = stack.pop()
            edge1 = Edge(edge_count, v1, v2)
            edge2 = Edge(edge_count + 1, v1, v3)

            v1.edges.append(edge1)
            v1.edges.append(edge2)
            v2.edges.append(edge1)
            v3.edges.append(edge2)

            self.edges.append(edge1)
            self.edges.append(edge2)

            edge_count += 2

    def print_graph_info(self):
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

# start the timer
start_time = time.time()
homogenous_star = HomogenousAmalgamatedStar(n)



# Print graph information
homogenous_star.print_graph_info()
# execution time
execution_time = time.time() - start_time
print("Execution time: ", execution_time, "seconds")
