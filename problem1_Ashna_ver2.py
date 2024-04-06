import math

# setting up n value, k value, and order of graph
n = 8
k = math.ceil((3 * n + 1) / 2)
order = 3 * n + 1
# intializing list of vertex labels
vertex_labels = {i: None for i in range(order)}
# set the center vertex label to be 1
vertex_labels[0] = 1

# Case 1
if n % 4 == 0 or n % 4 == 2 or n % 4 == 3:
    # labeling all the internal vertices (for this case it will go from 1, 8)
    for i in range(1, n + 1):
        vertex = i
        if 1 <= i <= math.ceil(n / 4) + 1:
            vertex_labels[vertex] = 3 * i - 2
        elif math.ceil(n / 4) + 1 <= i <= n:
            vertex_labels[vertex] = 2 * math.ceil(n / 4) + i
    
    # labeling all the external vertices (this should go from 9 to 24)
    vertex += 1
    for i in range(1, (math.ceil(n / 4) + 1)):
        for j in range(1, 3):  
                vertex_labels[vertex] =  j + 1
                vertex = vertex + 1
   
    for i in range((math.ceil(n / 4) + 1), n + 1):
        for j in range(1, 3):
            vertex_labels[vertex] = n + i + j - 1 - 2 * math.ceil(n / 4)
            vertex = vertex + 1

    
# Output vertex labels
print("Vertex Labels:")
for vertex, label in vertex_labels.items():
    print(f"Vertex {vertex}: Label {label}")








