import numpy as np

def plot_cities(ax):
    # Get lat and lng of Germany's main cities. 
    top_cities = {
    'Berlin': (13.404954, 52.520008), 
    'Köln': (6.953101, 50.935173),
    'Düsseldorf': (6.782048, 51.227144),
    'Frankfurt am Main': (8.682127, 50.110924),
    'Hamburg': (9.993682, 53.551086),
    'Leipzig': (12.387772, 51.343479),
    'München': (11.576124, 48.137154),
    'Dortmund': (7.468554, 51.513400),
    'Stuttgart': (9.181332, 48.777128),
    'Nürnberg': (11.077438, 49.449820),
    'Hannover': (9.73322, 52.37052)
    }
    for c in top_cities.keys():
        # Plot city name.
        ax.text(x=top_cities[c][0], 
                # Add small shift to avoid overlap with point.
                y=top_cities[c][1] + 0.1, 
                s=c, 
                fontsize=12,
                ha='center')
        # Plot city location centroid.
        ax.plot(top_cities[c][0], 
                top_cities[c][1], 
                marker='o',
                c='black', 
                alpha=0.5)


def plot_cbar(ax,vmin,vmax,cmap,label=None):
    gradient = np.linspace(vmax, vmin, 256)
    gradient = np.vstack((gradient, gradient)).T
    pos1 = ax.get_position() # get the original position 
    pos2 = [pos1.x0 - (pos1.width / 2), pos1.y0,  pos1.width / 1, pos1.height / 1.5] 
    ax.set_position(pos2) # set a new position
    ax.imshow(gradient,cmap=cmap,aspect=.15)
    ax.set_axis_on()
    ax.yaxis.tick_right()
    ax.set_yticks(range(10,247,59)) # 5 ticks
    ax.set_yticklabels([f'{x:.2g}' for x in np.linspace(vmax*1.039, vmin*0.961, 5)]) # scale to match 10/256 and 246/256
    ax.set_xticks([])
    if label:
        ax.set_ylabel(label)
        ax.yaxis.set_label_position("right")