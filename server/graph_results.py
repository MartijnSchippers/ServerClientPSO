import json
import matplotlib.pyplot as plt
import statistics

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

# TODO: make average fitness value graph, average personal best and global best
# get average fitness score, per generation
nr_particles = len(data)
nr_generations = len(data[0]["fitness"])
avg_fitness = []
def get_average(gen_nr, nr_particles, keyword):
    sum = 0.0
    for particle in data:
        sum += particle[keyword][gen_nr]
    return sum / nr_particles

def get_std_var(gen_nr, keyword = "fitness"):
    numbers = []
    for particle in data:
        numbers.append(particle[keyword][gen_nr])
    return statistics.pstdev(numbers)

x_axis_values = [x for x in range(1, nr_generations + 1)]
avg_fit_val = []
avg_pb_val = []
std_var = []
avg_x_values = []
avg_y_values = []
std_x = []
std_y = []
for gen_nr in range(0, nr_generations):
    avg_fit_val.append(get_average(gen_nr, nr_particles, "fitness"))
    avg_pb_val.append(get_average(gen_nr, nr_particles, "pb"))
    std_var.append(get_std_var(gen_nr))
    avg_x_values.append(get_average(gen_nr, nr_particles, "x"))
    avg_y_values.append(get_average(gen_nr, nr_particles, "y"))
    std_x.append(get_std_var(gen_nr, keyword = "x"))
    std_y.append(get_std_var(gen_nr, keyword = "y"))

# plot 
# average fitness value
plt.plot(x_axis_values, avg_fit_val, label=f'Average fitness value', color = colors[0], linestyle = line_styles[0], marker=line_markers[0])
# average pb value
plt.plot(x_axis_values, avg_pb_val, label=f'Average personal best value', color = colors[1], linestyle = line_styles[1], marker=line_markers[1])
# standard deviation per generation
plt.plot(x_axis_values, std_var, label=f'Standard deviation', color = colors[2], linestyle = line_styles[2], marker=line_markers[2])
plt.xlabel('Generation')
plt.ylabel('Fitness value')
plt.title('fitness values for 10 generations')
plt.legend()
plt.show()

# average value parameters x and y
plt.plot(x_axis_values, avg_x_values, label=f'x', color = colors[0], linestyle = line_styles[0], marker=line_markers[0])
plt.plot(x_axis_values, avg_y_values, label='y', color = colors[1], linestyle = line_styles[1], marker=line_markers[1])
plt.axhline(y = 1, color = 'r', label = 'optimal value')
plt.xlabel('Generation')
plt.ylabel('value')
plt.title('parameter values for 10 particles')
plt.legend()
plt.show()

# standard deviation parameters x and y
plt.plot(x_axis_values,std_x, label=f'x', color = colors[0], linestyle = line_styles[0], marker=line_markers[0])
plt.plot(x_axis_values, std_y, label='y', color = colors[1], linestyle = line_styles[1], marker=line_markers[1])
plt.xlabel('Generation')
plt.ylabel('value')
plt.title('standard deviation')
plt.legend()
plt.show()