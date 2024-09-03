import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# List of tuples (longitude, latitude) for each province's capital
argentina_provinces_coords = [
    (-57.9545, -27.4500),  # Corrientes
    (-60.5820, -31.4201),  # Córdoba
    (-65.2176, -26.8083),  # Catamarca
    (-65.3019, -24.1823),  # Jujuy
    (-57.9442, -34.6132),  # Buenos Aires (Capital)
    (-68.8458, -32.8908),  # Mendoza
    (-59.0139, -27.7824),  # Chaco
    (-58.8341, -27.3622),  # Formosa
    (-65.4109, -24.7883),  # Salta
    (-67.4891, -33.3016),  # San Luis
    (-66.3377, -33.3016),  # San Juan
    (-60.6953, -31.7366),  # Entre Ríos
    (-64.2909, -36.6167),  # La Pampa
    (-70.2945, -41.1456),  # Neuquén
    (-64.1888, -31.5354),  # Santa Fe
    (-59.0000, -29.1567),  # Santa Fe
    (-71.3052, -42.7660),  # Chubut
    (-67.4833, -28.4695),  # La Rioja
    (-54.6431, -25.6667),  # Misiones
    (-68.3333, -34.6667),  # Río Negro
    (-68.3667, -43.4167),  # Santa Cruz
    (-67.4960, -55.9833),  # Tierra del Fuego
    (-58.2752, -32.4833),  # Entre Ríos
    (-59.0069, -33.3333),  # Buenos Aires (province)
    (-58.9860, -27.3333),  # Formosa
    (-63.4167, -40.5833),  # Río Negro
]


# Function to plot Argentina provinces on a 2D map
def plot_argentina_provinces(coords):
    # Set up the Basemap for Argentina (centered in the region)
    map = Basemap(projection='merc', 
                  llcrnrlat=-55, urcrnrlat=-20, 
                  llcrnrlon=-75, urcrnrlon=-53, 
                  resolution='i')

    # Draw map boundaries, coastlines, and countries
    map.drawcoastlines()
    map.drawcountries()
    map.drawstates()  # This will help to draw province boundaries
    map.drawmapboundary()

    # Plot each province coordinate
    for lon, lat in coords:
        x, y = map(lon, lat)
        map.plot(x, y, marker='o', color='r', markersize=5)
    
    # Show the map
    plt.title("Argentina Provinces")
    plt.show()

# Call the function to plot the provinces
plot_argentina_provinces(argentina_provinces_coords)