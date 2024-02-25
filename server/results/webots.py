# File: graph_resutls.py      
# Date: 13-01-24     
# Description: This script is scientifically written and makes graphs of the results of a PSO run
# Author: Martijn Schippers

import json
import matplotlib.pyplot as plt
import statistics

from random import randint

plt.rcParams.update({
    # "text.usetex": True
    "font.family": "serif",  # Use a serif font
    "font.size": 10,  # Font size typically 10pt in IEEE papers
    "axes.labelsize": 12,  # Label font size
    "axes.titlesize": 12,  # Title font size
    "legend.fontsize": 12,  # Legend font size
    "xtick.labelsize": 12,  # X-axis tick font size
    "ytick.labelsize": 12,  # Y-axis tick font size
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
json_file_path = 'results_webots_run_2.json'

# Load data from the JSON file
data = load_data_from_json(json_file_path)

# TODO: make average fitness value graph, average personal best and global best
# get average fitness score, per generation
nr_particles = len(data)
nr_generations = len(data[0]["fitness"])
# nr_generations = 30
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
std_fitness = []
avg_rw_mean_values = []
std_rw_mean = []
avg_rw_var = []
std_rw_variance = []
avg_tao_values = []
avg_p_c_values = []
std_tao = []
std_p_c = []

# obtain average values and standard deviations of different dimensions of the results
for gen_nr in range(0, nr_generations):
    # fitness value
    avg_fit_val.append(get_average(gen_nr, nr_particles, "fitness"))
    std_fitness.append(get_std_var(gen_nr))
    avg_pb_val.append(get_average(gen_nr, nr_particles, "pb"))
    
    # random walk mean
    avg_rw_mean_values.append(get_average(gen_nr, nr_particles, "rw_mean"))
    std_rw_mean.append(get_std_var(gen_nr, "rw_mean"))

    # random walk variance
    avg_rw_var.append(get_average(gen_nr, nr_particles, "rw_variance"))
    std_rw_variance.append(get_std_var(gen_nr, "rw_variance"))

    # tao
    avg_tao_values.append(get_average(gen_nr, nr_particles, "tao"))
    std_tao.append(get_std_var(gen_nr, "tao"))

    # p_c
    avg_p_c_values.append(get_average(gen_nr, nr_particles, "p_c"))
    std_p_c.append(get_std_var(gen_nr, "p_c"))


# plot 
# average fitness value
plt.figure(figsize = (5, 4))
plt.plot(x_axis_values, avg_fit_val, label=f'Average fitness value', color = colors[0], linestyle = line_styles[0], marker=line_markers[0])
# # average pb value
plt.plot(x_axis_values, avg_pb_val, label=f'Average personal best value', color = colors[1], linestyle = line_styles[1], marker=line_markers[1])
# standard deviation per generation
plt.plot(x_axis_values, std_fitness, label=f'Standard deviation', color = colors[2], linestyle = line_styles[2], marker=line_markers[2])
plt.xlabel('Generation')
plt.ylabel('Fitness value')
plt.title('The average fitness values for 20 particles over 11 generations')
plt.legend()
plt.ylim([0, 1])
plt.tight_layout()
plt.show()

# plot the paramters rwmean, tao and p_c
fig, ax1 = plt.subplots(figsize=(5, 4))
# Plotting on the first axis (ax1)
ax1.plot(x_axis_values, avg_rw_mean_values, label='rw_mean', color=colors[0], linestyle=line_styles[0], marker=line_markers[0])
ax1.plot(x_axis_values, avg_tao_values, label='tao', color=colors[1], linestyle=line_styles[1], marker=line_markers[1])
ax1.plot(x_axis_values, avg_rw_var, label='rw_variance', color=colors[2], linestyle=line_styles[2], marker=line_markers[2])
# Setting labels and title for the first axis
ax1.set_xlabel('Generation')
ax1.set_ylabel('rw_mean and tao', color='black')
ax1.tick_params('y', colors='black')
# Creating a second y-axis
ax2 = ax1.twinx()
ax2.plot(x_axis_values, avg_p_c_values, label='p_c', color=colors[2], linestyle='-', marker='^')

# Setting labels and title for the second axis
ax2.set_ylabel('p_c', color='black')
ax2.tick_params('y', colors='black')

# Adding legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# Setting the title
plt.title('The average parameter values for 20 particles over 11 generations')

# Display the plot
plt.show()

# standard deviation parameters rw_mean, rw_variance, tao, p_c
# Create the primary axis
fig, ax1 = plt.subplots(figsize=(5, 4))

# Plot the first three curves on the primary axis
ax1.plot(x_axis_values, std_rw_mean, label='rw mean', color=colors[0], linestyle='-', marker='o')
ax1.plot(x_axis_values, std_rw_variance, label='rw_variance', color=colors[1], linestyle='-', marker='s')
ax1.plot(x_axis_values, std_tao, label='tao', color=colors[2], linestyle='-', marker='^')

# Set labels for the primary axis
ax1.set_xlabel('Generation')
ax1.set_ylabel('value', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='upper left')

# Create the secondary axis
ax2 = ax1.twinx()

# Plot the 'std_p_c' on the secondary axis
ax2.plot(x_axis_values, std_p_c, label='p_c', color='purple', linestyle='-', marker='D')

# Set labels for the secondary axis
ax2.set_ylabel('value', color='black')
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='upper right')

plt.title('Standard Deviation')
plt.tight_layout()
plt.show()