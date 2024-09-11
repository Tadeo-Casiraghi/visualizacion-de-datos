from extractor2 import SheetExtractor
import networkx as nx
import matplotlib.pyplot as plt
import math
import matplotlib.colors as mcolors
import numpy as np
from mpl_toolkits.basemap import Basemap


def latlon_to_mercator(lat, lon, x0=0, y0=0, R=6378137, scale=1):
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    x = R * lon_rad + x0
    y = R * math.log(math.tan(math.pi / 4 + lat_rad / 2)) + y0
    return x / scale, y / scale

def compute_net_flow(G):
    """
    Computes the net flow between edges and returns a new graph with only the net flow.
    
    Parameters:
    G (networkx.DiGraph): The original graph with directed edges.

    Returns:
    networkx.DiGraph: A new graph with net flow edges.
    """
    net_flow_G = nx.DiGraph()
    processed_pairs = set()  # Keep track of processed pairs

    for u, v, data in G.edges(data=True):
        if (v, u) in processed_pairs:
            # Skip if reverse edge is already processed
            continue

        if G.has_edge(v, u):
            reverse_weight = G[v][u]['weight']
            net_flow = data['weight'] - reverse_weight

            if net_flow > 0:
                net_flow_G.add_edge(u, v, weight=net_flow, color_value=data['color_value'])
            elif net_flow < 0:
                net_flow_G.add_edge(v, u, weight=-net_flow, color_value=G[v][u]['color_value'])

            # Mark this pair as processed
            processed_pairs.add((u, v))
            processed_pairs.add((v, u))
        else:
            # No reverse edge, just add the original
            net_flow_G.add_edge(u, v, weight=data['weight'], color_value=data['color_value'])

    return net_flow_G

def plot_graph(G, pos, x, y , size, net_flow=False):
    """
    Plots the graph. If net_flow is True, it plots only the net flow.
    
    Parameters:
    G (networkx.DiGraph): The original graph.
    pos (dict): Node positions.
    net_flow (bool): Flag to plot net flow. If False, it plots both arrows.
    """
    if net_flow:
        G = compute_net_flow(G)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='black', node_size=1)

    norm = mcolors.Normalize(vmin=0, vmax=1)
    cmap = plt.get_cmap('coolwarm')

    # Draw curved edges with thickness proportional to the weight
    for u, v, d in G.edges(data=True):
        edge_color = cmap(norm(d['color_value']))
        rad = 0  # Adjust curvature for better visualization
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v)],
            width=d['weight'],
            alpha=1,
            edge_color=[edge_color],
            arrowstyle='->',
            arrowsize=5,
            connectionstyle=f'arc3,rad={rad}'
        )

    # Draw labels on nodes
    nx.draw_networkx_labels(G, pos, font_size=3)

    plt.scatter(x, y, s=size, alpha=0.5, c='blue', edgecolors='black')

    plt.title("Network Graph with Custom Node Positions" + (" (Net Flow)" if net_flow else ""))
    plt.axis('equal')
    ax = plt.gca()
    ax.set_facecolor('gray')
    plt.savefig('test.png', dpi = 600)
    plt.show()

# Example usage
# Load data from your `SheetExtractor` here
test = SheetExtractor('datos_migracion\c2022_tp_migraciones_c15.xlsx')
edges = test.create_edges(ponderated=False, maximum=8, reference=1, colors=1)

# Create the graph
G = nx.DiGraph()
for u, v, weight, color_value in edges:
    G.add_edge(u, v, weight=weight, color_value=color_value)

# Calculate positions
x0, y0 = -34.6037, -58.3816  # Origin of the projection
pos = {provincia: latlon_to_mercator(lat, lon,x0 = 8350000, y0 =  7380000, scale=1) for provincia, (lat, lon) in test.latlong.items()}

plt.figure(figsize=(20,20))

map = Basemap(projection='merc', 
                  llcrnrlat=-55, urcrnrlat=-20, 
                  llcrnrlon=-75, urcrnrlon=-53, 
                  resolution='i')

    # Draw map boundaries, coastlines, and countries
map.drawcoastlines()
map.drawcountries()
map.drawstates()  # This will help to draw province boundaries
map.drawmapboundary()

x = []
y = []
size = []
for prov, value in pos.items():
    x.append(value[0])
    y.append(value[1])
    size.append(test.importacion[prov])


# Toggle the net_flow flag here
net_flow = True  # Set to True for net flow, False for both arrows

# Plot the graph based on the flag
# plot_graph(G, pos, x, y, size, net_flow=net_flow)

neto = {}

for origen, destino, flow, _ in edges:
    if origen not in neto:
        neto[origen] = -flow
    else:
        neto[origen] -= flow
    if destino not in neto:
        neto[destino] = flow
    else:
        neto[destino] += flow


plt.figure()
sorted_data = dict(sorted(neto.items(), key=lambda item: item[1]))

# Extract sorted keys and values
categories = list(sorted_data.keys())
values = list(sorted_data.values())

# Create a horizontal bar graph
plt.barh(categories, values, color='skyblue')

# Add titles and labels
plt.title('Horizontal Bar Graph Example')
plt.xlabel('Values')
plt.ylabel('Categories')

# Show the plot
plt.show()

suma = 0
for value in neto.values():
    suma += value

