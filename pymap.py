from extra_mig import SheetExtractor
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from myfunctions import plot_graph
import geopandas as gpd
import seaborn as sns
from matplotlib.ticker import FuncFormatter

maping = False
neto = True
ponderated = False

# Example usage
# Load data from your `SheetExtractor` here
test = SheetExtractor('datos_migracion\c2022_tp_migraciones_c15.xlsx')
edges = test.create_edges(neto = neto, ponderated=ponderated, maximum=30, reference=1, colors=0)

if maping:
    # Create the graph
    G = nx.DiGraph()
    for u, v, weight, color_value in edges:
        G.add_edge(u, v, weight=weight, color_value=color_value)

    # Calculate positions
    x0, y0 = -34.6037, -58.3816  # Origin of the projection
    # pos = {provincia: latlon_to_mercator(lat, lon,x0 = 8350000, y0 =  7380000, scale=1) for provincia, (lat, lon) in test.latlong.items()}
    # pos = {provincia: latlong for provincia, latlong in test.latlong.items()}
    lat = [lat for lat, _ in test.latlong.values()]
    lon = [lon for _, lon in test.latlong.values()]

    # Define source and target coordinate systems
    plate_carree = ccrs.PlateCarree()  # Geographic coordinates (lon, lat)
    mercator = ccrs.Mercator()         # Map projection used for plotting

    # Transform the coordinates from PlateCarree to Mercator
    transformed_coords = mercator.transform_points(plate_carree, np.array(lon), np.array(lat))

    # Extract the transformed x and y coordinates
    pos = {provincia: (x, y) for provincia, (x, y, _) in zip(test.latlong.keys(), transformed_coords)}

    fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={'projection': ccrs.Mercator()})

    # Set the extent of the map: [longitude_min, longitude_max, latitude_min, latitude_max]
    ax.set_extent([-75, -53, -55, -20], crs=ccrs.PlateCarree())

    # Add features such as coastlines and borders
    # ax.coastlines(resolution='50m')
    # ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Load the shapefile for Argentina's provinces
    gdf = gpd.read_file('gadm41_ARG_shp\gadm41_ARG_1.shp')

    # Plot the shapefile data (provinces) on the Cartopy map
    gdf.plot(ax=ax, edgecolor='black', facecolor='none', transform=ccrs.PlateCarree())

    # Optional: Add gridlines
    # ax.gridlines(draw_labels=True)


    # Plot the graph based on the flag
    plot_graph(G, pos)

neto = {}

for origen, destino, flow in test.edges:
    if origen not in neto:
        neto[origen] = -flow
    else:
        neto[origen] -= flow
    if destino not in neto:
        neto[destino] = flow
    else:
        neto[destino] += flow

# Seaborn style settings for better aesthetics
sns.set(style="whitegrid")

# First Plot: Flujo Neto de Migración por Provincia
fig, ax = plt.subplots(figsize=(10, 6))  # Increased figure size for better readability
sorted_data = dict(sorted(neto.items(), key=lambda item: item[1]))

# Extract sorted keys and values
categories = list(sorted_data.keys())
y_pos = np.arange(len(categories))
values = list(sorted_data.values())

# Calculate displacement for text labels
disp = (max(values) - min(values)) / 40

# Create a horizontal bar graph with Seaborn palette
sns.barplot(x=values, y=categories, palette='coolwarm', ax=ax)

# Add titles and labels
ax.set_title('Flujo Neto de Migración por Provincia', fontsize=16)
ax.set_xlabel('Valores Netos', fontsize=12)



# Add text labels based on positive or negative values
for i, (value, name) in enumerate(zip(values, categories)):
    if value < 0:
        ax.text(disp, i, name, va='center', ha='left', color='red')
    else:
        ax.text(-disp, i, name, va='center', ha='right', color='green')

plt.tight_layout()

# Second Plot: Flujo Neto dividido por Población
fig, ax = plt.subplots(figsize=(10, 6))  # Same increased size for consistency

categories = []
values = []
for provincia, valor in sorted_data.items():
    categories.append(provincia)
    values.append(valor / test.poblacion[provincia])

sorted_data = dict(sorted(zip(categories, values), key=lambda item: item[1]))
categories = list(sorted_data.keys())
y_pos = np.arange(len(categories))
values = np.array(list(sorted_data.values())) * 100

disp = (max(values) - min(values)) / 40

# Create a horizontal bar graph with Seaborn palette
sns.barplot(x=values, y=categories, palette='coolwarm', ax=ax)

ax.set_yticks([])

def percent_format(x, _):
    return f'{x:.0f}%'

# Format x-ticks with percentage symbol
ax.xaxis.set_major_formatter(FuncFormatter(percent_format))

# Add titles and labels
# ax.set_title('Flujo Neto de Migración por Provincia dividido por Población', fontsize=16)
# ax.set_xlabel('Porcentaje del Flujo Neto', fontsize=12)

# Add text labels based on positive or negative values
for i, (value, name) in enumerate(zip(values, categories)):
    if value < 0:
        ax.text(disp, i, name, va='center', ha='left')
    else:
        ax.text(-disp, i, name, va='center', ha='right')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

plt.tight_layout()

plt.savefig('barras.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)

plt.show()