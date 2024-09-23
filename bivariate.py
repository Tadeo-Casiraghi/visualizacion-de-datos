import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

def create_bivariate_palette(custom_pal):
    # Define the number of values per variable
    n_values = 5
    
    # Create a grid for the two variables
    x = np.arange(n_values)
    y = np.arange(n_values)
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(6, 6))

    # Iterate over the grid and apply the custom palette
    for i in range(n_values):
        for j in range(n_values):
            # Generate the key for the palette lookup
            key = f"{i+1}-{j+1}"
            color = custom_pal.get(key, "#FFFFFF")  # Default to white if not found
            
            # Convert hex color to RGB using matplotlib's to_rgba
            rgba_color = to_rgba(color)
            
            # Draw the rectangle with the corresponding color
            rect = plt.Rectangle((i, j), 1, 1, facecolor=rgba_color)
            ax.add_patch(rect)
    
    # Set the ticks and labels
    # ax.set_xticks(np.arange(n_values) + 0.5)
    # ax.set_yticks(np.arange(n_values) + 0.5)
    # ax.set_xticklabels([f"V1-{i+1}" for i in range(n_values)])
    # ax.set_yticklabels([f"V2-{i+1}" for i in range(n_values)])
    
    # Adjust the axis limits and aspect ratio
    ax.set_xlim(0, n_values)
    ax.set_ylim(0, n_values)
    ax.set_aspect('equal')
    
    # Hide the grid lines
    # ax.grid(False)
    # ax.set_axisbelow(True)

    ax.set_axis_off()
    
    # Set axis labels
    # ax.set_xlabel('ICV (alto es mejor)')
    # ax.set_ylabel('Quantil de movimiento (mas == mas gente de afuera)')

    plt.savefig("legend.svg", format="svg", bbox_inches='tight', pad_inches=0, transparent=True)

    # Display the plot
    plt.show()

# Example custom palette
custom_pal = { 
    "1-1" : "#d3d3d3",  # low x, low y 
    "2-1" : "#b6cdcd", 
    "3-1" : "#97c5c5", 
    "4-1" : "#75bebe", 
    "5-1" : "#52b6b6",  # high x, low y 
    "1-2" : "#cab6c5", 
    "2-2" : "#aeb0bf", 
    "3-2" : "#91aab9", 
    "4-2" : "#70a4b2", 
    "5-2" : "#4e9daa", 
    "1-3" : "#c098b9", 
    "2-3" : "#a593b3", 
    "3-3" : "#898ead", 
    "4-3" : "#6b89a6", 
    "5-3" : "#4a839f", 
    "1-4" : "#b77aab", 
    "2-4" : "#9e76a6", 
    "3-4" : "#8372a0", 
    "4-4" : "#666e9a", 
    "5-4" : "#476993", 
    "1-5" : "#ad5b9c",  # low x, high y 
    "2-5" : "#955898", 
    "3-5" : "#7c5592", 
    "4-5" : "#60528d", 
    "5-5" : "#434e87"  # high x, high y 
}

# Call the function to create the plot with the custom palette
create_bivariate_palette(custom_pal)
