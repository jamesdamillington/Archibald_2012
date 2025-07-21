import numpy as np
import pylandstats as pls

NON_FLAMMABLE = -1
UNBURNT = 0
BURNING = 1
BURNT = 2

class FireModel:
    def __init__(self, grid_size, p_natural_ignition, p_human_ignition, p_spread, rho):
        self.grid_size = grid_size
        self.p_natural_ignition = p_natural_ignition
        self.p_human_ignition = p_human_ignition
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
        mask = self.grid == UNBURNT
        natural = np.random.rand(*self.grid.shape) < self.p_natural_ignition
        human = np.random.rand(*self.grid.shape) < self.p_human_ignition
        ignition = (natural | human) & mask
        self.grid[ignition] = BURNING

    def spread_fire(self):
        new_burning = np.zeros_like(self.grid, dtype=bool)
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.grid[x, y] == BURNING:
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.grid.shape[0] and 0 <= ny < self.grid.shape[1]:
                            if self.grid[nx, ny] == UNBURNT and np.random.rand() < self.p_spread:
                                new_burning[nx, ny] = True
        self.grid[new_burning] = BURNING

    def update_burnt(self):
        self.grid[self.grid == BURNING] = BURNT

    def step(self):
        self.ignite()
        self.spread_fire()
        self.update_burnt()
        self.time += 1

    def run_simulation(self, steps):
        for _ in range(steps):
            self.step()

    def get_grid(self):
        return self.grid

    # ---- Initial State Measures using pylandstats ----
    def calculate_initial_flammable_fraction(self):
        flammable = (self.initial_grid != NON_FLAMMABLE)
        total_cells = self.initial_grid.size
        return np.sum(flammable) / total_cells if total_cells > 0 else 0.0

    def calculate_initial_num_flammable_clusters(self):
        # pylandstats expects classes as integers, so flammable = 1, non-flammable = 0
        flammable_mask = (self.initial_grid != NON_FLAMMABLE).astype(int)
        ls = pls.Landscape(flammable_mask, neighborhood_rule=4, res=(1,1))
        df = ls.compute_class_metrics_df(metrics=['number_of_patches'])
        #print(df.columns)
        # The 'NP' column is "Number of Patches"
        return int(df['number_of_patches'].values[0])

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
        ls = pls.Landscape(burnt_mask, neighborhood_rule=4, res=(1,1))
        df = ls.compute_class_metrics_df( metrics=['number_of_patches'])
        return int(df['number_of_patches'].values[0])

    def calculate_median_fire_size(self):
        burnt_mask = (self.grid == BURNT).astype(int)
        ls = pls.Landscape(burnt_mask, neighborhood_rule=4, res=(1,1))
        df = ls.compute_patch_metrics_df(metrics=['area'])
        #print(df.columns)
        # Only consider patches of class 1 (burnt)
        fire_areas = df.loc[df['class_val'] == 1, 'area']
        if len(fire_areas) == 0:
            return 0.0
        return float(np.median(fire_areas))

    def get_final_measures(self):
        return {
            "burned_fraction": self.calculate_burned_fraction(),
            "num_fires": self.calculate_num_fires(),
            "median_fire_size": self.calculate_median_fire_size()
        }