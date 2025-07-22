import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import numpy as np
import pytest
from fire_model import FireModel, NON_FLAMMABLE, UNBURNT, BURNING, BURNT

def test_grid_initialization():
    model = FireModel(grid_size=10, grid_res=50, mu=0.1, p_spread=0.2, rho=0.5)
    grid = model.grid
    assert grid.shape == (10, 10), "Grid should be 10x10"
    assert np.all(np.isin(grid, [NON_FLAMMABLE, UNBURNT])), "Grid should only contain NON_FLAMMABLE or UNBURNT cells"

def test_initial_flammable_fraction():
    model = FireModel(grid_size=20, grid_res=50, mu=0.1, p_spread=0.2, rho=0.7)
    frac = model.calculate_initial_flammable_fraction()
    assert 0.0 <= frac <= 1.0, "Initial flammable fraction should be between 0 and 1"

def test_ignite_changes_some_cells():
    model = FireModel(grid_size=10, grid_res=50, mu=1.0, p_spread=0.2, rho=1.0)
    before = np.sum(model.grid == BURNING)
    model.ignite()
    after = np.sum(model.grid == BURNING)
    assert after > before, "Ignite should increase the number of burning cells"

def test_spread_fire_only_to_adjacent():
    model = FireModel(grid_size=5, grid_res=50, mu=0.0, p_spread=1.0, rho=1.0)
    model.grid[:] = UNBURNT
    model.grid[2,2] = BURNING
    model.spread_fire()
    # The center and its four direct neighbors should be burning
    expected = {(2,2), (1,2), (3,2), (2,1), (2,3)}
    burning_cells = set(map(lambda x: (int(x[0]), int(x[1])), np.argwhere(model.grid == BURNING)))
    assert burning_cells == expected, "Fire should only spread to the four adjacent cells"

def test_step_year_increments_time():
    model = FireModel(grid_size=5, grid_res=50, mu=0.0, p_spread=0.0, rho=1.0)
    t0 = model.time
    model.step_year(1)
    assert model.time == t0 + 1, "step_year should increment the time by 1"

def test_initial_num_flammable_clusters():
    model = FireModel(grid_size=10, grid_res=1, mu=1.0, p_spread=1.0, rho=1.0)
    clusters = model.calculate_initial_num_flammable_clusters()
    assert isinstance(clusters, int), "Number of clusters should be an integer"
    assert clusters >= 0, "Number of clusters should be non-negative"

def test_burned_fraction_and_num_fires():
    model = FireModel(grid_size=10, grid_res=1, mu=1.0, p_spread=1.0, rho=1.0)
    model.step_fire()
    frac = model.calculate_burned_fraction()
    fires = model.calculate_num_fires()
    assert 0.0 <= frac <= 1.0, "Burned fraction should be between 0 and 1"
    assert fires >= 0, "Number of fires should be non-negative"

def test_median_fire_size():
    model = FireModel(grid_size=10, grid_res=1, mu=1.0, p_spread=1.0, rho=1.0)
    model.step_fire()
    median_size = model.calculate_median_fire_size()
    assert median_size >= 0.0, "Median fire size should be non-negative"

def test_step_fire_full_burn():
    # All cells flammable, fire should burn entire grid
    model = FireModel(grid_size=100, grid_res=1, mu=1.0, p_spread=1.0, rho=1.0)
    model.grid[:] = UNBURNT
    model.step_fire()
    assert np.all(model.grid == BURNT), "Not all cells burned when p_spread=1 and rho=1"

def test_step_fire_no_spread():
    # Fire should only burn one cell if p_spread=0
    model = FireModel(grid_size=100, grid_res=1, mu=1.0, p_spread=0.0, rho=1.0)
    model.grid[:] = UNBURNT
    model.step_fire()
    assert np.sum(model.grid == BURNT) == 1, "More than one cell burned when p_spread=0"

def test_step_fire_no_flammable_cells():
    # No flammable cells, nothing should burn
    model = FireModel(grid_size=100, grid_res=1, mu=1.0, p_spread=1.0, rho=0.0)
    model.step_fire()
    assert np.sum(model.grid == BURNT) == 0, "Cells burned when there should be none"

def test_grid_initialization_all_flammable():
    model = FireModel(grid_size=100, grid_res=1, mu=1.0, p_spread=1.0, rho=1.0)
    # All cells should be UNBURNT (flammable)
    assert np.all(model.grid == UNBURNT), "Not all cells initialized as UNBURNT when they should be"