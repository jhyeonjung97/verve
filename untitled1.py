import pandas as pd
exp_path = '/pscratch/sd/j/jiuy97/3_V_shape/monoxides.tsv'
exp_df = pd.read_csv(exp_path, delimiter='\t')
exp_df['dH_form'] = exp_df['dH_form'] / 96.48

for data in exp_df:
    if exp_df['row'] == '3d':
        plt.plot(filtered_x, filtered_values, marker='o', color=colors[j % len(colors)], label=column)
