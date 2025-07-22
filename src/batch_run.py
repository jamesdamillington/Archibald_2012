import csv
from fire_model import FireModel

def run_batch(params_csv, results_csv):
    with open(params_csv, newline='') as f:
        reader = csv.DictReader(f)
        params_list = list(reader)

    total_runs = sum(int(params.get('n_repeats', 1)) for params in params_list)
    run_counter = 1
    
    results = []
    for param_idx, params in enumerate(params_list, 1):
        n_repeats = int(params.get('n_repeats', 1))
        for repeat in range(n_repeats):
            print(f"Running simulation {run_counter} of {total_runs} (param set {param_idx}, repeat {repeat+1})")
            
            model = FireModel(
            int(params['grid_size']),
            float(params['mu']),
            float(params['p_spread']),
            float(params['rho'])
            )
            initial_measures = model.get_initial_measures()
            model.run_simulation(int(params['steps']))
            final_measures = model.get_final_measures()
            row = {**params, **initial_measures, **final_measures}
            results.append(row)
            run_counter += 1

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