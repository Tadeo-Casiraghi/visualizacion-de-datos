from extractor2 import SheetExtractor
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math


def latlon_to_mercator(lat, lon, x0=0, y0=0, R=6378137, scale = 1):
    """
    Convert latitude and longitude to Mercator projection coordinates.
    
    Parameters:
    lat (float): Latitude in degrees.
    lon (float): Longitude in degrees.
    x0 (float): X origin (default is 0).
    y0 (float): Y origin (default is 0).
    R (float): Radius of the Earth in meters (default is 6378137, WGS84 standard).

    Returns:
    (float, float): Tuple containing the x and y coordinates in the Mercator projection.
    """
    
    # Convert latitude and longitude from degrees to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    
    # Calculate x and y using the Mercator projection formula
    x = R * lon_rad + x0
    y = R * math.log(math.tan(math.pi / 4 + lat_rad / 2)) + y0
    
    return x/scale, y/scale

test = SheetExtractor('datos_migracion\c2022_tp_migraciones_c15.xlsx')

edges = test.create_edges(ponderated=False, maximum = 5, reference = 1)


# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph
G.add_weighted_edges_from(edges)

# Example usage
x0, y0 = -34.6037, -58.3816  # Origin of the projection

pos = {}
for provincia, (lat, lon) in test.latlong.items():
    pos[provincia] = latlon_to_mercator(lat, lon, x0, y0, scale = 1000000)

# Manually define node positions
# pos = {
#     'A': (0, 0),
#     'B': (1, 1),
#     'C': (1, -1),
#     'D': (6, 0)
# }

# pos = nx.spring_layout(G)

# Draw nodes at specified positions
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=10)

# Draw curved edges with thickness proportional to the weight
for u, v, d in G.edges(data=True):
    rad = 0.2 
    nx.draw_networkx_edges(
        G, pos, edgelist=[(u, v)],
        width=d['weight'],
        alpha=0.6,
        edge_color= 'red',
        arrowstyle='->',
        arrowsize=20,
        connectionstyle=f'arc3,rad={rad}'  # This adds curvature to the edges
    )

# Draw labels on nodes
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

# Display the graph
plt.title("Network Graph with Custom Node Positions")
plt.axis('equal')
plt.show()
