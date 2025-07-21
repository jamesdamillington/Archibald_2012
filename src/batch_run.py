import csv
import numpy as np
from fire_model import FireModel

PARAMS_FILE = "../data/params.csv"
RESULTS_FILE = "../results/results.csv"

def run_simulation(grid_size, p_natural_ignition, p_human_ignition, p_spread, rho, steps):
    model = FireModel(grid_size, p_natural_ignition, p_human_ignition, p_spread, rho)
    for _ in range(steps):
        model.step()
    burnt_fraction = np.mean(model.get_grid() == 2)  # 2 == BURNT
    return burnt_fraction

def batch_run_from_file(params_file, results_file):
    with open(params_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        results = []
        for row in reader:
            grid_size = int(row['grid_size'])
            steps = int(row['steps'])
            p_natural_ignition = float(row['p_natural_ignition'])
            p_human_ignition = float(row['p_human_ignition'])
            p_spread = float(row['p_spread'])
            rho = float(row['rho'])
            n_repeats = int(row.get('n_repeats', 1))
            for repeat in range(n_repeats):
                burnt_fraction = run_simulation(
                    grid_size, p_natural_ignition, p_human_ignition, p_spread, rho, steps
                )
                result = {
                    'grid_size': grid_size,
                    'steps': steps,
                    'p_natural_ignition': p_natural_ignition,
                    'p_human_ignition': p_human_ignition,
                    'p_spread': p_spread,
                    'rho': rho,
                    'repeat': repeat,
                    'burnt_fraction': burnt_fraction
                }
                results.append(result)
    # Write results to CSV
    with open(results_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Batch simulation complete. Results saved to {results_file}")

if __name__ == "__main__":
    batch_run_from_file(PARAMS_FILE, RESULTS_FILE)