import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Function to map reflectivity to radar colors
def reflectivity_to_color(reflectivity):
    # Define the reflectivity thresholds and corresponding colors
    reflectivity_colors = [
        (5, "#0000FF"),   # Blue for light rain
        (15, "#00FF00"),  # Green for moderate rain
        (25, "#FFFF00"),  # Yellow for heavy rain
        (35, "#FFA500"),  # Orange for very heavy rain
        (45, "#FF0000"),  # Red for intense rain
        (55, "#800080"),  # Purple for extreme rain
        (65, "#FFFFFF"),  # White for hail
    ]

    for threshold, color in reflectivity_colors:
        if reflectivity < threshold:
            return color, reflectivity < 15  # Return color and transparency flag
    return "#FFFFFF", False  # Default to white for values beyond the defined range

# Load the CSV data
data = pd.read_csv('/Users/trevorwiebe/Ktor/radar_backend/radar_data/csv_files/20240621_090454_cropped.csv')

# Normalize latitude and longitude to a grid
lat_min, lat_max = data['latitude'].min(), data['latitude'].max()
lon_min, lon_max = data['longitude'].min(), data['longitude'].max()

# Define the grid size
lat_grid_size = int((lat_max - lat_min) * 100) + 1  # Adjust the multiplier as needed for resolution
lon_grid_size = int((lon_max - lon_min) * 100) + 1  # Adjust the multiplier as needed for resolution

# Create an empty image array with an alpha channel
image_array = np.zeros((lat_grid_size, lon_grid_size, 4), dtype=np.uint8)

# Fill the image array with colors based on reflectivity
for index, row in data.iterrows():
    lat_index = int((row['latitude'] - lat_min) * 100)  # Adjust the multiplier as needed for resolution
    lon_index = int((row['longitude'] - lon_min) * 100)  # Adjust the multiplier as needed for resolution
    
    if 0 <= lat_index < lat_grid_size and 0 <= lon_index < lon_grid_size:
        color, transparent = reflectivity_to_color(row['reflectivity'])
        rgb_color = mcolors.hex2color(color)
        rgba_color = [int(255 * c) for c in rgb_color] + [0 if transparent else 255]  # Add alpha channel
        image_array[lat_index, lon_index] = rgba_color

# Convert the image array to an image
plt.imshow(image_array)
plt.axis('off')  # Turn off axis labels
plt.savefig('radar_image.png', bbox_inches='tight', pad_inches=0, transparent=True)