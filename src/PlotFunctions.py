import numpy as np
import matplotlib.pyplot as plt

# Spatial Exploration

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

# Temporal exploration

def create_temporal_plots(c1_cases_yearly, c1_years,
                 c2_cases_yearly, c2_years,
                 flat_c1_cases_monthly, flat_c2_cases_monthly, x_labels_monthly,
                 c1_key_name, c2_key_name,
                 years):
    
    # Direct comparison with yearly data
    fig, axs = plt.subplots(1, 3, figsize=(15, 6))
    axs[0].plot(c1_years, c1_cases_yearly)
    axs[0].set_title(c1_key_name)
    axs[1].plot(c2_years, c2_cases_yearly, color='red')
    axs[1].set_title(c2_key_name)
    axs[2].plot(c1_years, c1_cases_yearly)
    axs[2].plot(c2_years, c2_cases_yearly, color='red')
    axs[2].set_title("Direct comparison")
    axs[2].legend([c1_key_name, c2_key_name])
    plt.show()
    plt.close()
   

    

    # plot monthly crimes over the years
    fig, axs = plt.subplots(2, 1, figsize=(15, 18))
    axs[0].plot(x_labels_monthly, flat_c1_cases_monthly)
    axs[0].set_title(f'{c1_key_name} from {years[0]} to {years[-1]}')
    axs[0].tick_params(axis='x', rotation=90)
    axs[0].grid(True)

    axs[1].plot(x_labels_monthly, flat_c2_cases_monthly)
    axs[1].set_title(f'{c2_key_name} from {years[0]} to {years[-1]}')
    axs[1].tick_params(axis='x', rotation=90)
    axs[1].grid(True)

    for year in years:
        tick = 'Dez. ' + str(year)
        axs[0].axvline(x=tick, color='red')
        axs[1].axvline(x=tick, color='red')

    n = 3  # Keeps every 7th label
    [l.set_visible(False) for (i,l) in enumerate(axs[0].xaxis.get_ticklabels()) if i % n != 0]
    [l.set_visible(False) for (i,l) in enumerate(axs[1].xaxis.get_ticklabels()) if i % n != 0]

    plt.show()

    
    # Compare them directly in one plot
    y_ticks=2000
    fig, axs = plt.subplots(sharey=True, layout='constrained', figsize=(15,9))
    axs.fill_between(x_labels_monthly, flat_c1_cases_monthly)
    axs.fill_between(x_labels_monthly, flat_c2_cases_monthly)
    axs.set(yscale='linear', title=f'{c1_key_name} vs. {c1_key_name}')
    axs.legend([c1_key_name, c2_key_name])
    axs.tick_params(axis='x', rotation=90)
    axs.grid(True)
    monthly_max = max(np.max(flat_c2_cases_monthly), np.max(flat_c1_cases_monthly))
    monthly_y_ticks = np.arange(0, np.ceil(monthly_max/1000)*1000, y_ticks)
    axs.set_yticks(monthly_y_ticks)
    [l.set_visible(False) for (i,l) in enumerate(axs.xaxis.get_ticklabels()) if i % n != 0] # Keep every n-th label
    
    for year in years:
        tick = 'Dez. ' + str(year)
        axs.axvline(x=tick, color='red')

    plt.show()

    # Plot the sum of them (with given sum key if given)
    # Find the maximum length of the two lists
    max_length = max(len(flat_c1_cases_monthly), len(flat_c2_cases_monthly))
    # Pad the shorter list with zeros to make them equal in length
    flat_c1_cases_padded = np.pad(flat_c1_cases_monthly, (0, max_length - len(flat_c1_cases_monthly)))
    flat_c2_cases_padded = np.pad(flat_c2_cases_monthly, (0, max_length - len(flat_c2_cases_monthly)))
    
    y_ticks_combined=5000
    
    fig, axs = plt.subplots(sharey=True, layout='constrained', figsize=(15,9))
    axs.fill_between(x_labels_monthly, flat_c1_cases_padded, alpha=0.5)
    axs.fill_between(x_labels_monthly, flat_c2_cases_padded+flat_c1_cases_padded, flat_c1_cases_padded, alpha=0.5)
    axs.legend([c1_key_name, c2_key_name])
    axs.set(yscale='linear', title=f'{c1_key_name} + {c1_key_name}')
    
    axs.tick_params(axis='x', rotation=90)
    axs.grid(True)
    monthly_max_combined = np.max(flat_c2_cases_padded+flat_c1_cases_padded)
    monthly_y_ticks_combined = np.arange(0, np.ceil(monthly_max_combined/1000)*1000, y_ticks_combined)
    axs.set_yticks(monthly_y_ticks_combined)
    [l.set_visible(False) for (i,l) in enumerate(axs.xaxis.get_ticklabels()) if i % n != 0] # keep every n-th label

    for year in years:
        tick = 'Dez. ' + str(year)
        axs.axvline(x=tick, color='red')

    plt.show()

    # Compute Correlation coefficient for all cases in a year
    print(f"Pearson product-moment correlation coefficients of {c1_key_name} and {c2_key_name} with yearly data: \n{np.corrcoef(c1_cases_yearly, c2_cases_yearly)}") 
    print(f"Pearson product-moment correlation coefficients of {c1_key_name} and {c2_key_name} with monthly data: \n{np.corrcoef(flat_c1_cases_monthly, flat_c2_cases_monthly)}")