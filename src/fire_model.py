import numpy as np

UNBURNT = 0
BURNING = 1
BURNT = 2

class FireModel:
    def __init__(self, grid_size, p_natural_ignition, p_human_ignition, p_spread):
        self.grid_size = grid_size
        self.p_natural_ignition = p_natural_ignition
        self.p_human_ignition = p_human_ignition
        self.p_spread = p_spread
        self.grid = np.zeros((grid_size, grid_size), dtype=int)

    def step(self):
        self.ignite()
        self.spread_fire()
        self.update_grid()

    def ignite(self):
        natural = np.random.rand(*self.grid.shape) < self.p_natural_ignition
        human = np.random.rand(*self.grid.shape) < self.p_human_ignition
        ignition = (natural | human) & (self.grid == UNBURNT)
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

    def update_grid(self):
        self.grid[self.grid == BURNING] = BURNT

    def reset(self):
        self.grid.fill(UNBURNT)

    def get_grid(self):
        return self.grid.copy()