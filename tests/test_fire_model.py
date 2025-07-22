import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import numpy as np
import pytest
from fire_model import FireModel, NON_FLAMMABLE, UNBURNT, BURNING, BURNT

def test_grid_initialization():
    model = FireModel(grid_size=10, p_natural_ignition=0.1, p_human_ignition=0.1, p_spread=0.2, rho=0.5)
    grid = model.grid
    assert grid.shape == (10, 10)
    assert np.all(np.isin(grid, [NON_FLAMMABLE, UNBURNT]))

def test_initial_flammable_fraction():
    model = FireModel(grid_size=20, p_natural_ignition=0.1, p_human_ignition=0.1, p_spread=0.2, rho=0.7)
    frac = model.calculate_initial_flammable_fraction()
    assert 0.0 <= frac <= 1.0

def test_ignite_changes_some_cells():
    model = FireModel(grid_size=10, p_natural_ignition=1.0, p_human_ignition=0.0, p_spread=0.2, rho=1.0)
    before = np.sum(model.grid == BURNING)
    model.ignite()
    after = np.sum(model.grid == BURNING)
    assert after > before

def test_spread_fire_only_to_adjacent():
    model = FireModel(grid_size=5, p_natural_ignition=0.0, p_human_ignition=0.0, p_spread=1.0, rho=1.0)
    model.grid[:] = UNBURNT
    model.grid[2,2] = BURNING
    model.spread_fire()
    # The center and its four direct neighbors should be burning
    expected = {(2,2), (1,2), (3,2), (2,1), (2,3)}
    burning_cells = set(map(lambda x: (int(x[0]), int(x[1])), np.argwhere(model.grid == BURNING)))
    assert burning_cells == expected

def test_update_burnt():
    model = FireModel(grid_size=5, p_natural_ignition=0.0, p_human_ignition=0.0, p_spread=0.0, rho=1.0)
    model.grid[:] = UNBURNT
    model.grid[1,1] = BURNING
    model.update_burnt()
    assert model.grid[1,1] == BURNT

def test_step_increments_time():
    model = FireModel(grid_size=5, p_natural_ignition=0.0, p_human_ignition=0.0, p_spread=0.0, rho=1.0)
    t0 = model.time
    model.step()
    assert model.time == t0 + 1

def test_initial_num_flammable_clusters():
    model = FireModel(grid_size=10, p_natural_ignition=0.1, p_human_ignition=0.1, p_spread=0.2, rho=1.0)
    clusters = model.calculate_initial_num_flammable_clusters()
    assert isinstance(clusters, int)
    assert clusters >= 0

def test_burned_fraction_and_num_fires():
    model = FireModel(grid_size=10, p_natural_ignition=1.0, p_human_ignition=0.0, p_spread=0.0, rho=1.0)
    model.run_simulation(1)
    frac = model.calculate_burned_fraction()
    fires = model.calculate_num_fires()
    assert 0.0 <= frac <= 1.0
    assert fires >= 0

def test_median_fire_size():
    model = FireModel(grid_size=10, p_natural_ignition=1.0, p_human_ignition=0.0, p_spread=0.0, rho=1.0)
    model.run_simulation(1)
    median_size = model.calculate_median_fire_size()
    assert median_size >= 0.0