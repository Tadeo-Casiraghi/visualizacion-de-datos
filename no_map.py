from extra_mig import SheetExtractor
import networkx as nx
import numpy as np
from myfunctions import latlon_to_mercator, plot_graph



# Example usage
# Load data from your `SheetExtractor` here
test = SheetExtractor('datos_migracion\c2022_tp_migraciones_c15.xlsx')
edges = test.create_edges(neto = True, ponderated=False, maximum=8, reference=1, colors=0)
# Create the graph
G = nx.DiGraph()
for u, v, weight, color_value in edges:
    G.add_edge(u, v, weight=weight, color_value=color_value)

# Calculate positions
x0, y0 = -34.6037, -58.3816  # Origin of the projection
pos = {provincia: latlon_to_mercator(lat, lon, x0, y0, scale=1000000) for provincia, (lat, lon) in test.latlong.items()}

# Plot the graph based on the flag
plot_graph(G, pos)
