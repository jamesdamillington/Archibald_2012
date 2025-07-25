# Archibald 2012
Reproducing the savanna fire simulation model described in Archibald et al. (2011) *PNAS* doi: [10.1073/pnas.1118648109](https://doi.org/10.1073/pnas.1118648109)

## Original Model
_mu_ is ignition frequency, fires km-2 yr-1  (number of ignition events in a landscape)
_rho_ is initial probability that a cell is flammable
*p_spread* is probability of fire spreading from one cell to an adjacent cell
*grid_size* is in cells (one side of the grid)
*grid_res* is in m

> "A 100 × 100 cell spatially explicit fire propagation model was set up with no interaction on the diagonals and no wrapping at the edges. Obstructions to fire (nonflammable cells) were randomly laid down on this grid with proportion ρ.  ... Ignitions occurred randomly in the grid, and if an ignition occurred in a flammable cell its probability of spreading to an adjacent flammable cell was λ. Each model run occurred over one growth year; there was no regrowth of fuels, and a cell that burned remained burned until the end of the model run." 

Outputs are measures of initial landscape state and fires that burned in the simulated year

With *grid_size* == 100 and *grid_res* == 500, total area = 2500 km-2 which means the following attempted number of fires ignited (not all fires may be possible if there is insufficent unburned area remaining):
- mu 0.0004: 1 fire
- mu 0.0020: 5 fires
- mu 0.0400: 100 fires

Results match Fig 1 in Archibald _et al._ (2012):
![alt text](results/fig2_faceted.png)

## Additions

### Roads
The `add_linear_nonflammable` function add 'roads' (linear rows of non-flammable cells) to introduce fuel discontinuities. This shows how the original Archibald *et al.* results can be modified (note: next two figs are for *grid_size* == 101). 

- Adding _two_ roads to create _four_ equal size areas where vegetation can grow results in different relationships for low mu (ignition rate) but not otherwise:
![alt text](results/fig2_grid101_cross.png)

- Adding _four_ roads to create _nine_ equal size areas where vegetation can grow results in different relationships for low and intermediate mu (ignition rate) but not high:
![alt text](results/fig2_grid101_fourlines.png)

### Contagion
Code to calculate the CONTAGION landscape metric has been added but not yet analysed

### Fields
To do: allow initial flammable cells to be non-randomly located, and rather clustered to better represent real-world landscpes

To do: examine classes of vegetation with differentiated spread probabilities (and ignition rates?)
