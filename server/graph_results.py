import json
import matplotlib.pyplot as plt
from random import randint

plt.rcParams.update({
    # "text.usetex": True
    "font.family": "serif",  # Use a serif font
    "font.size": 10,  # Font size typically 10pt in IEEE papers
    "axes.labelsize": 8,  # Label font size
    "axes.titlesize": 8,  # Title font size
    "legend.fontsize": 8,  # Legend font size
    "xtick.labelsize": 8,  # X-axis tick font size
    "ytick.labelsize": 8,  # Y-axis tick font size
    "lines.linewidth": 1.5,  # Line width
    "lines.markersize": 3,  # Marker size
    "figure.figsize": (3.39, 2.54),  # Figure size in inches (single column)
})
line_styles = [
    "-",      # Solid line
    "--",     # Dashed line
    "-.",     # Dash-dot line
    ":",      # Dotted line
    "solid",  # Solid line (equivalent to "-")
    "dashed", # Dashed line (equivalent to "--")
    "dashdot",# Dash-dot line (equivalent to "-.")
    "dotted", # Dotted line (equivalent to ":")
]
colors = []
for i in range(10):
    colors.append('#%06X' % randint(0, 0xFFFFFF))

line_markers = [
    ".",    # Point marker
    ",",    # Pixel marker
    "o",    # Circle marker
    "v",    # Triangle down marker
    "^",    # Triangle up marker
    "<",    # Triangle left marker
    ">",    # Triangle right marker
    "1",    # Tri down marker
    "2",    # Tri up marker
    "3",    # Tri left marker
    "4",    # Tri right marker
    "s",    # Square marker
    "p",    # Pentagon marker
    "*",    # Star marker
    "h",    # Hexagon1 marker
    "H",    # Hexagon2 marker
    "+",    # Plus marker
    "x",    # X marker
    "D",    # Diamond marker
    "d",    # Thin diamond marker
]


# Function to load data from a JSON file
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Example data file path
json_file_path = 'results.json'

# Load data from the JSON file
data = load_data_from_json(json_file_path)

# Extracting x-axis values (assuming both lists have the same length)
x_values = list(range(1, len(data["results"][0]) + 1))

# Plotting the data
nr_rows = len(data["results"])
for i in range(0, nr_rows):
    plt.plot(x_values, data["results"][i], label=f'Particle {i + 1}')

# Adding labels and title
plt.xlabel('Generation')
plt.ylabel('Fitness value')
plt.title('Fitness values over time')

# Adding legend
plt.legend()

# Display the graph
plt.show()
