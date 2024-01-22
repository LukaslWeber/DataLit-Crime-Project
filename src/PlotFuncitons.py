import numpy as np

def plot_cities(ax):
    # Get lat and lng of Germany's main cities. 
    top_cities = {
    'Berlin': (1489825.814677,6894090.067075),
    'Köln': (774015.662754,6609834.57817),
    'Frankfurt am Main': (966489.956643,6465508.13095),
    'Hamburg': (1112491.59139,7085591.65015),
    'Leipzig': (1379000.4711,6682277.55847),
    'München': (1288648.22904,6129702.78025),
    'Dortmund': (831395.628242,6712615.65422),
    'Stuttgart': (1022061.20304,6237128.94263),
    'Nürnberg': (1233134.75745,6351533.97836),
    'Hannover': (1083497.09418,6867399.4956)
    }
    for c in top_cities.keys():
        # Plot city name.
        ax.text(x=top_cities[c][0], 
                # Add small shift to avoid overlap with point.
                y=top_cities[c][1]+25000, 
                s=c, 
                # fontsize=12,
                ha='center')
        # Plot city location centroid.
        ax.plot(top_cities[c][0], 
                top_cities[c][1], 
                marker='o',
                c='black', 
                alpha=0.5,
                markersize=3)


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