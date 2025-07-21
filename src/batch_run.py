import csv
from fire_model import FireModel

def run_batch(params_csv, results_csv):
    with open(params_csv, newline='') as f:
        reader = csv.DictReader(f)
        params_list = list(reader)

    results = []
    for params in params_list:
        model = FireModel(
            int(params['grid_size']),
            float(params['p_natural_ignition']),
            float(params['p_human_ignition']),
            float(params['p_spread']),
            float(params['rho'])
        )
        initial_measures = model.get_initial_measures()
        model.run_simulation(int(params['steps']))
        final_measures = model.get_final_measures()
        row = {**params, **initial_measures, **final_measures}
        results.append(row)

    # Write all results to CSV
    fieldnames = list(results[0].keys())
    with open(results_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python batch_run.py params.csv results.csv")
    else:
        run_batch(sys.argv[1], sys.argv[2])