from fire_model import FireModel
import matplotlib.pyplot as plt

def animate_model(steps=100, grid_size=100, p_natural_ignition=0.0001, p_human_ignition=0.0005, p_spread=0.2, rho= 1):
    model = FireModel(grid_size, p_natural_ignition, p_human_ignition, p_spread, rho)
    plt.ion()
    fig, ax = plt.subplots(figsize=(6,6))
    
    cmap = plt.cm.get_cmap('YlOrRd', 4)  # 4 discrete colors
    im = ax.imshow(model.get_grid(), cmap=cmap, vmin=-1, vmax=2)
    
    ax.axis('off')
    for step in range(steps):
        model.step()
        im.set_data(model.get_grid())
        ax.set_title(f"Step {step+1}")
        plt.pause(0.1)
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    animate_model()