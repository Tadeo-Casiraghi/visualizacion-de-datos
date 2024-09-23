import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx

def latlon_to_mercator(lat, lon, x0=0, y0=0, R=6378137, scale=1):
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    x = R * lon_rad + x0
    y = R * math.log(math.tan(math.pi / 4 + lat_rad / 2)) + y0
    return x / scale, y / scale

def plot_graph(G, pos):
    """
    Plots the graph. If net_flow is True, it plots only the net flow.
    
    Parameters:
    G (networkx.DiGraph): The original graph.
    pos (dict): Node positions.
    """
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
            arrowsize=20,
            connectionstyle=f'arc3,rad={rad}'
        )

    # Draw labels on nodes
    # nx.draw_networkx_labels(G, pos, font_size=3)
    
    plt.axis('equal')
    ax = plt.gca()
    ax.set_axis_off()
    # ax.set_facecolor('gray')
    plt.savefig('test.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)
    plt.show()