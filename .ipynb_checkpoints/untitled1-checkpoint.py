import pandas as pd
import matplotlib.pyplot as plt

exp_path = '/pscratch/sd/j/jiuy97/3_V_shape/monoxides.tsv'
exp_df = pd.read_csv(exp_path, delimiter='\t')
exp_df['dH_form'] = exp_df['dH_form'] / 96.48

# coordinations = ['WZ', 'ZB', 'TN', '33', 'RS']
exp_colors = {'WZ': '#d62728',
              'ZB': '#ff7f0e',
              'LT': '
              'TN': '#2ca02c', 
              '33': '#279ff2', 
              'RS': '#9467bd'}
exp_markers = {'WZ': 'v',
              'ZB': 'v', 
              'TN': 's', 
              '33': 's', 
              'RS': 'o',
              'LT': '#9467bd'}

for i in exp_df.index:
    if exp_df['row'][i] == '3d':
        marker = exp_markers.get(exp_df['Coordination'][i], '*')
        color = exp_colors.get(exp_df['Coordination'][i], 'k')
        plt.scatter(filtered_x, filtered_values, marker='o', color=colors[j % len(colors)], label=column)
