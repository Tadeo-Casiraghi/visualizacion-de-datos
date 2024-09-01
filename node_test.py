import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Define your matrix as a list of tuples
edges = [
    ('A', 'B', 1),
    ('A', 'C', 2),
    ('A', 'D', 3),
    ('B', 'A', 4),
    ('B', 'C', 5),
    ('B', 'D', 6),
    ('C', 'A', 7),
    ('C', 'B', 8),
    ('C', 'D', 9),
    ('D', 'A', 10),
    ('D', 'B', 11),
    ('D', 'C', 12)
]

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph
G.add_weighted_edges_from(edges)

# Manually define node positions
pos = {
    'A': (0, 0),
    'B': (1, 1),
    'C': (1, -1),
    'D': (6, 0)
}

# Draw nodes at specified positions
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=5000)

# Draw curved edges with thickness proportional to the weight
for u, v, d in G.edges(data=True):
    rad = 0.2 
    nx.draw_networkx_edges(
        G, pos, edgelist=[(u, v)],
        width=d['weight'],
        alpha=0.6,
        edge_color='blue' if d['weight'] % 2 == 0 else 'red',
        arrowstyle='->',
        arrowsize=20,
        connectionstyle=f'arc3,rad={rad}'  # This adds curvature to the edges
    )

# Draw labels on nodes
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

# Display the graph
plt.title("Network Graph with Custom Node Positions")
plt.show()
