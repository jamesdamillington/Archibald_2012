# Archibald_2012
Reproducing the savanna fire simulation model described in Archibald et al. (2011) *PNAS* doi: [10.1073/pnas.1118648109](https://doi.org/10.1073/pnas.1118648109)

_mu_ is ignition frequency, fires km-2 yr-1  (number of ignition events in a landscape)
_rho_ is initial probability that a cell is flammable
*p_spread* is probability of fire spreading from one cell to an adjacent cell

> "A 100 × 100 cell spatially explicit fire propagation model was set up with no interaction on the diagonals and no wrapping at the edges. Obstructions to fire (nonflammable cells) were randomly laid down on this grid with proportion ρ.  ... Ignitions occurred randomly in the grid, and if an ignition occurred in a flammable cell its probability of spreading to an adjacent flammable cell was λ. Each model run occurred over one growth year; there was no regrowth of fuels, and a cell that burned remained burned until the end of the model run." 

Outputs are measures of initial landscape state and fires that burned in the simulated year


