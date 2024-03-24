"""
ADJACENCY MATRIX IMPLENTATION
"""
import time as time
class HomogenousAmalgamatedStar:
    def __init__(self, n):
        # Calculate the order of the graph based on the parameter 'n'
        self.order = 3 * n + 1
        # Initialize an adjacency matrix with zeros
        self.adj_matrix = [[0] * self.order for _ in range(self.order)]

        # Connect the central vertex to the outer vertices
        for i in range(1, self.order):
            # Set the central vertex as adjacent to each outer vertex
            self.adj_matrix[0][i] = 1
            # Set each outer vertex as adjacent to the central vertex
            self.adj_matrix[i][0] = 1

        # Connect outer vertices to form triangles
        for i in range(1, self.order):
            # Calculate the indices of the outer vertices to form triangles
            v1 = i
            v2 = (i % (3 * n)) + 1
            v3 = (i % (3 * n)) + 2
            # Handle cases where v2 or v3 exceeds the order of the graph
            if v2 == 0:
                v2 = 3 * n
            if v3 == 0:
                v3 = 3 * n
            if v2 >= self.order:
                v2 -= self.order
            if v3 >= self.order:
                v3 -= self.order
            # Establish connections between vertices to form triangles
            self.adj_matrix[v1][v2] = 1
            self.adj_matrix[v2][v1] = 1
            self.adj_matrix[v1][v3] = 1
            self.adj_matrix[v3][v1] = 1

    def print_adjacency_matrix(self):
        # Print the adjacency matrix row by row
        for row in self.adj_matrix:
            print(row)


# Create a HomogenousAmalgamatedStar instance with n = 3
n = 3

# Start the timer
start_time = time.time()
homogenous_star = HomogenousAmalgamatedStar(n)


# Print the adjacency matrix of the generated graph
homogenous_star.print_adjacency_matrix()
# Calculate and print execution time
execution_time = time.time() - start_time
print("Execution time: ", execution_time, "seconds")

