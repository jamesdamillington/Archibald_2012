import numpy as np
import pylandstats as pls

NON_FLAMMABLE = -1
UNBURNT = 0
BURNING = 1
BURNT = 2

class FireModel:
    def __init__(self, grid_size, grid_res, mu, p_spread, rho):
        self.grid_size = grid_size
        self.grid_res = grid_res
        self.mu = mu
        self.p_spread = p_spread
        self.rho = rho
        self.grid = self.initialize_grid()
        self.initial_grid = self.grid.copy()  # Store initial grid for initial measures
        self.time = 0

    def initialize_grid(self):
        # Flammable with probability rho, else non-flammable
        flammable = np.random.rand(self.grid_size, self.grid_size) < self.rho
        grid = np.full((self.grid_size, self.grid_size), NON_FLAMMABLE, dtype=int)
        grid[flammable] = UNBURNT
        return grid

    def ignite(self):
        # Find all unburnt cells
        unburnt_indices = np.argwhere(self.grid == UNBURNT)
        if len(unburnt_indices) == 0:
            print("No unburnt cells to ignite.")
            return
        # Randomly select one unburnt cell to ignite
        x, y = unburnt_indices[np.random.choice(len(unburnt_indices))]
        self.grid[x, y] = BURNING

    def spread_fire(self):
        new_burning = np.zeros_like(self.grid, dtype=bool)
        burning_indices = np.argwhere(self.grid == BURNING)
        for x, y in burning_indices:
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid.shape[0] and 0 <= ny < self.grid.shape[1]:
                    if self.grid[nx, ny] == UNBURNT and np.random.rand() < self.p_spread:
                        new_burning[nx, ny] = True
        self.grid[new_burning] = BURNING

    def step_fire(self):
        if not np.any(self.grid == BURNING):
            self.ignite()
        while np.any(self.grid == BURNING):
            burning_indices = np.argwhere(self.grid == BURNING)
            self.spread_fire()
            # Only set cells that were burning before the spread to BURNT
            for x, y in burning_indices:
                self.grid[x, y] = BURNT

    def step_year(self, fires):
        for _ in range(fires):
            self.step_fire()
        self.time += 1

    def run_simulation(self, years, fires_yr):
        for _ in range(years):
            self.step_year(fires=fires_yr)

    def get_grid(self):
        return self.grid

    # ---- Initial State Measures using pylandstats ----
    def calculate_initial_flammable_fraction(self):
        flammable = (self.initial_grid != NON_FLAMMABLE)
        total_cells = self.initial_grid.size
        return np.sum(flammable) / total_cells if total_cells > 0 else 0.0

    def calculate_initial_num_flammable_clusters(self):
        flammable_mask = (self.initial_grid != NON_FLAMMABLE).astype(int)
        ls = pls.Landscape(flammable_mask, neighborhood_rule=4, res=(self.grid_res, self.grid_res))
        df = ls.compute_class_metrics_df(metrics=['number_of_patches'])
        return int(df['number_of_patches'].values[0]) if not df.empty else 0

    def get_initial_measures(self):
        return {
            "initial_flammable_fraction": self.calculate_initial_flammable_fraction(),
            "initial_num_flammable_clusters": self.calculate_initial_num_flammable_clusters()
        }

    # ---- Final State Measures using pylandstats ----
    def calculate_burned_fraction(self):
        flammable = (self.grid != NON_FLAMMABLE)
        burnt = (self.grid == BURNT)
        if np.sum(flammable) == 0:
            return 0.0
        return np.sum(burnt) / np.sum(flammable)

    def calculate_num_fires(self):
        burnt_mask = (self.grid == BURNT).astype(int)
        ls = pls.Landscape(burnt_mask, neighborhood_rule=4, res=(self.grid_res, self.grid_res))
        df = ls.compute_class_metrics_df(metrics=['number_of_patches'])
        return int(df['number_of_patches'].values[0]) if not df.empty else 0

    def calculate_median_fire_size(self):
        burnt_mask = (self.grid == BURNT).astype(int)
        ls = pls.Landscape(burnt_mask, neighborhood_rule=4, res=(self.grid_res, self.grid_res))
        df = ls.compute_patch_metrics_df(metrics=['area'])
        # Only consider patches of class 1 (burnt)
        fire_areas = df.loc[df['class_val'] == 1, 'area'] if 'class_val' in df.columns else []
        if len(fire_areas) == 0:
            return 0.0
        return float(np.median(fire_areas))

    def get_final_measures(self):
        return {
            "burned_fraction": self.calculate_burned_fraction(),
            "num_fires": self.calculate_num_fires(),
            "median_fire_size_ha": self.calculate_median_fire_size()
        }