# archibald_2011
Reproducing the savanna fire simulation model described in Archibald et al. (2011) in PNAS

_mu_ is ignition frequency, fires km-2 yr-1  (number of ignition events in a landscape)
_rho_ is initial probability that a cell is flammable
*p_spread* is probability of fire spreading from one cell to an adjacent cell

*grid_size*

*steps*


> "The parameter μ is the number of ignition events in a landscape. Humans can affect ρ by changing the proportion of cultivated and grazed land, or by building roads, μ by igniting more fires, and λ by altering the times of year when fires occur"

But,

> Ignitions occurred randomly in the grid, and if an ignition occurred in a flammable cell its probability of spreading to an adjacent flammable cell was λ. Each model run occurred over one growth year; there was no regrowth of fuels, and a cell that burned remained burned until the end of the model run. 

So actually, ignition frequency is specified as number of fires in a given run. i.e. no need for *steps*



