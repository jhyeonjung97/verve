import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import argparse

print(f"\033[92m{os.getcwd()}\033[0m")

def plot_patterns_from_multiple_tsv(filenames, output, xlabel, ylabel, labels, a, b, row, fontsize):
        
    metal_rows = {
        '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
        '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
        '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
        }
    
    if row:
        indice = metal_rows[row]
        markers = ['v', 'v', 's', 's', 'o']
        colors = ['#d62728', '#ff7f0e', '#2ca02c', '#279ff2', '#9467bd']
    else:
        indice = [f'{a}\n{b}\n{c}' for a, b, c in zip(metal_rows['3d'], metal_rows['4d'], metal_rows['5d'])]
        if '1_Tetrahedral_WZ' in os.getcwd():
            coordination = 'WZ'
            markers = ['v'] * len(filenames)
            colors = plt.cm.Reds(np.linspace(0.1, 0.9, len(filenames)))
        elif '2_Tetrahedral_ZB' in os.getcwd():
            coordination = 'ZB'
            markers = ['v'] * len(filenames)
            colors = plt.cm.Oranges(np.linspace(0.1, 0.9, len(filenames)))
        elif '3_Square_Planar_TN' in os.getcwd():
            coordination = 'TN'
            markers = ['s'] * len(filenames)
            colors = plt.cm.Greens(np.linspace(0.1, 0.9, len(filenames)))
        elif '4_Square_Planar_33' in os.getcwd():
            coordination = '33'
            markers = ['s'] * len(filenames)
            colors = plt.cm.Blues(np.linspace(0.1, 0.9, len(filenames)))
        elif '5_Octahedral_RS' in os.getcwd():
            coordination = 'RS'
            markers = ['o'] * len(filenames)
            colors = plt.cm.Purples(np.linspace(0.1, 0.9, len(filenames)))        

    merged_df = None
    summed_df = None
    
    png_filename = f"merged_{output}.png"   
    tsv_filename = f"merged_{output}.tsv"
    sum_filename = f"summed_{output}.tsv"
    
    plt.figure(figsize=(a, b))

    if len(filenames) > len(labels):
        print(f"Warning: More filenames ({len(filenames)}) than labels ({len(labels)}). Excess filenames will be ignored.")
        filenames = filenames[:len(labels)]

    for j, file in enumerate(filenames):
        df = pd.read_csv(file, delimiter='\t').iloc[:, 1:]
        df.columns = labels[j] if isinstance(labels[j], list) else [labels[j]]
        merged_df = pd.concat([merged_df, df], axis=1)

    for j, column in enumerate(merged_df.columns):
        filtered_x = []
        filtered_values = []
        x = merged_df.index
        values = merged_df[column]
        for i, v in enumerate(values):
            if not np.isnan(v):
                filtered_x.append(i)
                filtered_values.append(v)
        if not filtered_values:
            print(f"No values found for pattern: {column}")
            continue
        plt.plot(filtered_x, filtered_values, marker=markers[j], color=colors[j], label=column)
    
    if 'hexa_ratio' in df.columns:
        plt.plot(x, [1.633]*len(x), linestyle=':', label='hexa_ratio0', color='black')
        
    if 'norm_formation' in output:
        exp_path = '/pscratch/sd/j/jiuy97/3_V_shape/monoxides.tsv'
        exp_df = pd.read_csv(exp_path, delimiter='\t')
        exp_df['dH_form'] = exp_df['dH_form'] / 96.48
        exp_colors = {'WZ': '#d62728', 'ZB': '#ff7f0e', 'LT': '#ffd70e', 'TN': '#2ca02c', '33': '#279ff2', 'RS': '#9467bd'}
        exp_markers = {'WZ': 'v', 'ZB': 'v', 'LT': '^', 'TN': 's', '33': 's', 'RS': 'o'}
        if row:
            for i in exp_df.index:
                if exp_df['row'][i] == row:
                    exp_marker = exp_markers.get(exp_df['Coordination'][i], '*')
                    exp_color = exp_colors.get(exp_df['Coordination'][i], '#8a8a8a')
                    plt.scatter(exp_df['numb'][i], exp_df['dH_form'][i], 
                                marker=exp_marker, color=exp_color, edgecolors=exp_color, facecolors='white')
        else:
            for i in exp_df.index:
                if exp_df['Coordination'][i] == coordination:
                    if exp_df['row'][i] == '5d':
                        color = colors[-1]; marker = makers[-1]
                    elif exp_df['row'][i] == '4d':
                        color = colors[-2]; marker = makers[-2]
                    elif exp_df['row'][i] == '3d':
                        color = colors[-3]; marker = makers[-3]
                    plt.scatter(exp_df['numb'][i], exp_df['dH_form'][i],
                                marker=marker, color=color, edgecolors=exp_color, facecolors='white')
    
    merged_df.to_csv(tsv_filename, sep='\t')
    print(f"Merged data saved to {tsv_filename}")

    plt.xticks(np.arange(len(indice)), indice, fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.legend(prop={'size': fontsize}, ncol=1)
    # plt.grid(True)
    plt.tight_layout()
    plt.gcf().savefig(png_filename, bbox_inches="tight")
    print(f"Figure saved as {png_filename}")
    plt.close()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot TSV data.')
    parser.add_argument('files', nargs='+', help='The TSV files to plot.')
    parser.add_argument('-o', '--output', type=str, default='', help="The filename for the output PNG file.")
    parser.add_argument('-x', '--xlabel', type=str, default='Element or Lattice parameter (Å)', help="xlabel")
    parser.add_argument('-y', '--ylabel', type=str, default='Energy (eV) or Charge (e)', help="ylabel")
    parser.add_argument('-l', '--labels', nargs='+', default=['Tetragonal_WZ', 'Tetragonal_ZB', 'Square_planar_TN', 'Square_planar_33', 'Octahedral_RS'])
    parser.add_argument('-r', '--row', type=str, default=None)
    parser.add_argument('-a', type=float, default=8)
    parser.add_argument('-b', type=float, default=6)
    parser.add_argument('--font', type=float, default=10)
    
    args = parser.parse_args()        
    plot_patterns_from_multiple_tsv(args.files, args.output, args.xlabel, args.ylabel, args.labels, 
                                    args.a, args.b, args.row, fontsize=args.font)

