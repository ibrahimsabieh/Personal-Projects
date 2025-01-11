import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from config import dataset

# Define the dataset as an adjacency matrix
data = dataset("Longest")

# Define the nodes to be traversed
traversal_nodes = [0, 9, 24]  # Starting at node 2 and ending at node 4

# Create a graph using NetworkX
G = nx.Graph()

# Add nodes to the graph
num_nodes = data.shape[0]
for i in range(num_nodes):
    G.add_node(i)

for i in range(num_nodes):
    for j in range(i + 1, num_nodes):
        weight = data[i][j]
        G.add_edge(i, j, weight=weight)

# Create a list of edge colors for highlighting the traversal path
traversal_edges = []

for i in range(len(traversal_nodes) - 1):
    traversal_edges.append((traversal_nodes[i], traversal_nodes[i + 1]))
    traversal_edges.append((traversal_nodes[i + 1], traversal_nodes[i]))

# Create a list of node colors based on traversal path
node_colors = [
    "lightgreen"
    if node == traversal_nodes[0]
    else "pink"
    if node == traversal_nodes[-1]
    else "lightblue"
    for node in G.nodes()
]

plt.figure(figsize=(6, 4))

# Calculate the sum of weights for the traversed edges
traversed_weight_sum = sum(data[i][j] for i, j in traversal_edges) / 2

# Draw the graph
pos = nx.spring_layout(G, seed=42, k=10)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=20,
    node_color=node_colors,
    font_size=9,
    font_color="black",
    font_weight="bold",
)
labels = nx.get_edge_attributes(G, "weight")

# Draw the edges with specified colors
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=traversal_edges,
    edge_color="b",
    width=3,
)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=[edge for edge in G.edges() if edge not in traversal_edges],
    edge_color="black",
    width=1.5,
)

# Draw the edge labels with custom colors
for edge, label in labels.items():
    color = "green" if edge in traversal_edges else "red"
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels={edge: label},
        font_size=9,
        font_color=color,
        font_weight="bold",
    )

# Display the graph
plt.title("Algorithm Traversal")

# Add labels for the green (start) and red (goal) nodes outside the graph
plt.text(
    pos[traversal_nodes[0]][0] - 0.05,
    pos[traversal_nodes[0]][1] - 0.15,
    "Start",
    fontsize=9,
    color="green",
    fontweight="bold",
)
plt.text(
    pos[traversal_nodes[-1]][0] + 0.05,
    pos[traversal_nodes[-1]][1] + 0.05,
    "Goal",
    fontsize=9,
    color="red",
    fontweight="bold",
)

# Reposition the "Shortest Path Found" text
plt.text(
    0.70,
    0.90,  # Adjust the y-coordinate
    f"Shortest Path Found: {traversed_weight_sum}",
    transform=plt.gca().transAxes,
    fontsize=9,
    bbox=dict(facecolor="white", edgecolor="black", boxstyle="round"),
)

plt.show()
