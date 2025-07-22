import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np

# Load results
df = pd.read_csv('../results/results_2025-07-22.csv')

mu_to_fires = {0.0004: 1, 0.002: 5, 0.04: 100}
mu_order = [0.0004, 0.002, 0.04]
spread_values = sorted(df['p_spread'].unique())

# Group by parameter set and take mean of repeats
grouped = df.groupby(['mu', 'p_spread', 'rho'], as_index=False).mean()

# colormap: green to red (reversed)
cmap = plt.get_cmap('RdYlGn_r')
#colors = [cmap(i / (len(spread_values)-1)) for i in range(len(spread_values))]
norm = Normalize(vmin=0.2, vmax=0.8)  # Use only the central, vibrant part
colors = [cmap(norm(i / (len(spread_values)-1))) for i in range(len(spread_values))]

# Make the figure larger for publication-quality output
fig, axes = plt.subplots(1, len(mu_order), figsize=(8 * len(mu_order), 8), sharey=True)

buffer = 0.03  # Small buffer for axes

for i, mu in enumerate(mu_order):
    ax = axes[i]
    subset = grouped[grouped['mu'] == mu]
    for j, p_spread in enumerate(spread_values):
        sub_spread = subset[subset['p_spread'] == p_spread]
        ax.scatter(sub_spread['rho'], 
                   sub_spread['burned_fraction'],
                   alpha=0.8, 
                   color=colors[j],
                   s=80)
    # Force axes limits to [0-buffer, 1+buffer]
    ax.set_xlim(0-buffer, 1+buffer)
    ax.set_ylim(0-buffer, 1+buffer)
    # Add diagonal dashed line
    ax.plot([0-buffer, 1+buffer], [0-buffer, 1+buffer], ls='--', color='grey', lw=1)
    ax.set_xlabel('Initial flammable fraction (ρ)', fontsize=16)
    ax.set_title(f'{mu_to_fires[mu]} ignitions (mu={mu})', fontsize=16)
    if i == 0:
        ax.set_ylabel('Fraction of landscape burned', fontsize=16)
    ax.tick_params(labelsize=14)

# Create a single legend for p_spread colours outside the right of the panes
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[j], markersize=12)
           for j in range(len(spread_values))]
labels = [f'p_spread={p_spread}' for p_spread in spread_values]
fig.legend(handles, labels, title='p_spread', loc='center left', bbox_to_anchor=(0.88, 0.5), borderaxespad=0., fontsize=14, title_fontsize=15)

plt.suptitle('Fraction burned vs. flammable fraction\nFaceted by ignitions', fontsize=18)
plt.tight_layout(rect=[0, 0, 0.88, 1])
plt.savefig('../results/fig2_faceted.png', dpi=400, bbox_inches='tight')
plt.close()