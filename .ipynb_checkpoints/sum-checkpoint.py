import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

print(f"\033[92m{os.getcwd()}\033[0m")


def process_files(add_files, subtract_files, output,
                 xlabel, ylabel, labels, row, a, b, fontsize):

    metal_rows = {
        '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
        '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
        '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
        }   

    summed_df = None
    
    png_filename = f"summed_{output}.png"   
    tsv_filename = f"summed_{output}.tsv"
    
    # Process addition files
    for filename in add_files:
        df = pd.read_csv(filename, delimiter='\t')
        if summed_df is None:
            summed_df = df
        else:
            summed_df.iloc[:, 1:] += df.iloc[:, 1:]  # Add values excluding the first column

    # Process subtraction files
    for filename in subtract_files:
        df = pd.read_csv(filename, delimiter='\t')
        if summed_df is None:
            summed_df = -df  # Subtract values for initialization, excluding the first column
        else:
            summed_df.iloc[:, 1:] -= df.iloc[:, 1:]  # Subtract values excluding the first column

    summed_df[0][0] = np.nan

    if row:
        indice = metal_rows[row]
        markers = ['v', 'v', '^', 's', 's', 'o']
        colors = ['#d62728', '#ff7f0e', '#ffd70e', '#2ca02c', '#279ff2', '#9467bd']
    else:
        indice = [f'{a}\n{b}\n{c}' for a, b, c in zip(metal_rows['3d'], metal_rows['4d'], metal_rows['5d'])]
        if '1_Tetrahedral_WZ' in os.getcwd():
            coordination = 'WZ'
            markers = ['v'] * len(summed_df.columns)
            colors = plt.cm.Reds(np.linspace(0.1, 0.9, len(summed_df.columns)))
        elif '2_Tetrahedral_ZB' in os.getcwd():
            coordination = 'ZB'
            markers = ['v'] * len(summed_df.columns)
            colors = plt.cm.Oranges(np.linspace(0.1, 0.9, len(summed_df.columns)))
        elif '3_Tetragonal_LT' in os.getcwd():
            coordination = 'LT'
            markers = ['^'] * len(summed_df.columns)
            colors = plt.cm.Wistia(np.linspace(0.1, 0.9, len(summed_df.columns)))
        elif '4_Square_Planar_TN' in os.getcwd():
            coordination = 'TN'
            markers = ['s'] * len(summed_df.columns)
            colors = plt.cm.Greens(np.linspace(0.1, 0.9, len(summed_df.columns)))
        elif '5_Square_Planar_33' in os.getcwd():
            coordination = '33'
            markers = ['s'] * len(summed_df.columns)
            colors = plt.cm.Blues(np.linspace(0.1, 0.9, len(summed_df.columns)))
        elif '6_Octahedral_RS' in os.getcwd():
            coordination = 'RS'
            markers = ['o'] * len(summed_df.columns)
            colors = plt.cm.Purples(np.linspace(0.1, 0.9, len(summed_df.columns)))     
            
    # Save the processed DataFrame
    if summed_df is not None:
        summed_df.to_csv(f'{tsv_filename}', index=False, sep='\t')
        print(f"Summed data saved to {tsv_filename}")
        plot_data(summed_df, png_filename, xlabel, ylabel, labels, row, a, b, fontsize, markers, colors)
        print(f"Summed data saved to {png_filename}")

def plot_data(summed_df, png_filename, xlabel, ylabel, labels, row, a, b, fontsize, markers, colors):
    
    plt.figure(figsize=(10, 6))
    for j, column in enumerate(summed_df.columns):
        filtered_x = []
        filtered_values = []
        x = summed_df.index
        values = summed_df[column]
        for i, v in enumerate(values):
            if not np.isnan(v):
                filtered_x.append(i)
                filtered_values.append(v)
        if not filtered_values:
            print(f"No values found for pattern: {column}")
            continue
        plt.plot(filtered_x, filtered_values, marker=markers[j], color=colors[j], label=column)
    
    if 'hexa_ratio' in summed_df.columns:
        plt.plot(x, [1.633]*len(x), linestyle=':', label='hexa_ratio0', color='black')
        
    if 'norm_formation' in png_filename:
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
                    if exp_df['row'][i] == '3d':
                        exp_color = colors[2]; exp_marker = markers[2]
                    elif exp_df['row'][i] == '4d':
                        exp_color = colors[3]; exp_marker = markers[3]
                    elif exp_df['row'][i] == '5d':
                        exp_color = colors[4]; exp_marker = markers[4]
                    plt.scatter(exp_df['numb'][i], exp_df['dH_form'][i],
                                marker=exp_marker, color=exp_color, edgecolors=exp_color, facecolors='white')    

    # plt.xticks(np.arange(len(indice)), indice, fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.legend(prop={'size': fontsize}, ncol=1)
    plt.tight_layout()
    plt.gcf().savefig(png_filename, bbox_inches="tight")
    print(f"Figure saved as {png_filename}")
    plt.close()
    
def main():
    parser = argparse.ArgumentParser(description='Process and plot TSV files.')
    parser.add_argument('-p', '--plus', nargs='+', help='Files to sum', default=[])
    parser.add_argument('-m', '--minus', nargs='+', help='Files to subtract', default=[])
    parser.add_argument('-o', '--output', help='Output file name', default='output')
    parser.add_argument('-x', '--xlabel', type=str, default='Element or Lattice parameter (Å)', help="xlabel")
    parser.add_argument('-y', '--ylabel', type=str, default='Energy (eV) or Charge (e)', help="ylabel")
    parser.add_argument('-l', '--labels', nargs='+', default=['Tetrahedral_WZ', 'Tetrahedral_ZB', 'Tetragonal_LT', 'Square_planar_TN', 'Square_planar_33', 'Octahedral_RS'])
    parser.add_argument('-r', '--row', type=str, default=None)
    parser.add_argument('-a', type=float, default=8)
    parser.add_argument('-b', type=float, default=6)
    parser.add_argument('--fontsize', type=float, default=10)
    args = parser.parse_args()

    # Execute file processing
    process_files(args.plus, args.minus, args.output, 
                  args.xlabel, args.ylabel, args.labels, 
                  args.row, args.a, args.b, args.fontsize)

if __name__ == "__main__":
    main()
