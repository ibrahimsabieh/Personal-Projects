import networkx as nx

# Create a directed graph
G = nx.Graph()

# Add nodes
G.add_node(0)
G.add_node(1)

# Add a directed edge from node 1 to node 0
G.add_edge(1, 0)

# You can also add more edges as needed, including in the reverse direction if desired.

# To visualize a directed graph
import matplotlib.pyplot as plt

# Draw the graph
pos = nx.spring_layout(G)  # Layout for the nodes
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=500,
    font_size=12,
    font_color="black",
    font_weight="bold",
    arrows=True,
)

# Display the graph
plt.show()
