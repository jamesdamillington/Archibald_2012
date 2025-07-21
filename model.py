import numpy as np
import matplotlib.pyplot as plt

# Model parameters (set based on paper's Table 1, or your scenario)
GRID_SIZE = 100
P_NATURAL_IGNITION = 0.0001    # Probability of natural ignition per cell per timestep
P_HUMAN_IGNITION = 0.0005      # Probability of human ignition per cell per timestep
P_SPREAD = 0.2                 # Probability of fire spreading to a neighbor
STEPS = 100                    # Number of time steps (fire season length)

# Cell states
UNBURNT = 0
BURNING = 1
BURNT = 2

def initialize_grid(size):
    """Initialize the grid with all cells unburnt."""
    return np.zeros((size, size), dtype=int)

def ignite(grid, p_natural, p_human):
    """Randomly ignite cells (natural + human)."""
    natural = np.random.rand(*grid.shape) < p_natural
    human = np.random.rand(*grid.shape) < p_human
    # Only ignite unburnt cells
    ignition = (natural | human) & (grid == UNBURNT)
    grid[ignition] = BURNING

def spread_fire(grid, p_spread):
    """Spread fire from burning cells to unburnt neighbors."""
    new_burning = np.zeros_like(grid, dtype=bool)
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == BURNING:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
                        if grid[nx, ny] == UNBURNT and np.random.rand() < p_spread:
                            new_burning[nx, ny] = True
    grid[new_burning] = BURNING

def update_grid(grid):
    """Advance burning cells to burnt."""
    grid[grid == BURNING] = BURNT

def animate_fire(grid, steps, p_natural, p_human, p_spread):
    plt.ion()
    fig, ax = plt.subplots(figsize=(6,6))
    im = ax.imshow(grid, cmap='YlOrRd', vmin=0, vmax=2)
    ax.set_title("Fire Spread Simulation")
    ax.axis('off')

    for step in range(steps):
        ignite(grid, p_natural, p_human)
        spread_fire(grid, p_spread)
        im.set_data(grid)
        ax.set_title(f"Fire Spread Simulation - Step {step+1}")
        plt.pause(0.1)
        update_grid(grid)
    plt.ioff()
    plt.show()

def main():
    grid = initialize_grid(GRID_SIZE)
    animate_fire(grid, STEPS, P_NATURAL_IGNITION, P_HUMAN_IGNITION, P_SPREAD)

if __name__ == "__main__":
    main()