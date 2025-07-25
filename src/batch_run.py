import csv
from xml.parsers.expat import model
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
            int(params['grid_res']),
            float(params['mu']),
            float(params['p_spread']),
            float(params['rho'])
            )
            
            x_lines = params.get('x_lines', '[]')
            y_lines = params.get('y_lines', '[]')
                
            x_lines = [] if x_lines == '[]' else [int(x) for x in x_lines.strip('[]').split(',')]
            y_lines = [] if y_lines == '[]' else [int(y) for y in y_lines.strip('[]').split(',')]

            print(x_lines)
            print(y_lines)
            
            model.add_linear_nonflammable(xidx=x_lines, yidx=y_lines)

            initial_measures = model.calc_initial_measures()
            
            #calculate number of fires
            grid_area_km = model.grid_size * model.grid_size * model.grid_res ** 2 / 1e6  # Convert sqm to km^2
            fires_yr = int(float(params['mu']) * grid_area_km)
            #print(fires_yr)
            #print(int(params['years']))

            #model.show_initial_grid()   #use for testing
            model.run_simulation(int(params['years']), fires_yr)

            final_measures = model.calc_final_measures()
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