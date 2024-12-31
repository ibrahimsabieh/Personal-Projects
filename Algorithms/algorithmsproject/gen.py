import networkx as nx
import numpy as np
import random

# Create a weighted graph
G = nx.Graph()

# Number of nodes in the graph
num_nodes = 100

# Add nodes to the graph
G.add_nodes_from(range(num_nodes))

# Generate random weighted edges
for u in G.nodes():
    for v in G.nodes():
        if u != v and not G.has_edge(u, v):
            weight = random.randint(1, 15)
            G.add_edge(u, v, weight=weight)

# Generate the adjacency matrix
adjacency_matrix = nx.to_numpy_array(G)

# Convert the adjacency matrix to a list of lists
adjacency_matrix_as_list = adjacency_matrix.tolist()
print(adjacency_matrix_as_list)

