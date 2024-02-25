import json
import matplotlib.pyplot as plt
import statistics

# Function to load data from a JSON file
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Example data file path
json_file_path = 'results_webots.json'

# Load data from the JSON file
data = load_data_from_json(json_file_path)

# TODO: make average fitness value graph, average personal best and global best
# get average fitness score, per generation
nr_particles = len(data)
nr_generations = len(data[0]["fitness"])

best_fit_val = 999999
best_p_idx = 0
best_idx = 0
for p_idx, particle in enumerate(data):
        for idx, fit_val in enumerate(particle["fitness"]):
             if fit_val < best_fit_val:
                  best_fit_val = fit_val
                  best_p_idx = p_idx
                  best_idx = idx

print("best fitness: ", best_fit_val)
print("particle idx: ", best_p_idx)
print("generation index: ", best_idx)