import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse

def plot_patterns_from_multiple_tsv(filenames, output, xlabel, ylabel, labels, colors, markers, a, b, row):

    metal_rows = {
        '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
        '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
        '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
        }
    
    if row:
        indice = metal_rows[row]
    else:
        indice = [f'{a}\n{b}\n{c}' for a, b, c in zip(metal_rows['3d'], metal_rows['4d'], metal_rows['5d'])]

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

    for j, pattern in enumerate(merged_df.columns):
        x = range(len(merged_df[pattern]))
        filtered_df = merged_df[pattern].dropna()
        if filtered_df.empty:
            print(f"No values found for pattern: {pattern}")
            continue
        plt.plot(x, filtered_df, 
                 marker=markers[j % len(markers)], 
                 color=colors[j % len(colors)], 
                 label=labels[j % len(labels)])
    if 'hexa_ratio' in df.columns:
        plt.plot(x, [1.633]*len(x), linestyle=':', label='hexa_ratio0', color='black')

    merged_df.to_csv(tsv_filename, sep='\t')
    print(f"Merged data saved to {tsv_filename}")

    plt.xticks(np.arange(len(indice)), indice, fontsize=12) #9
    plt.yticks(fontsize=12) #9
    plt.xlabel(xlabel, fontsize=12) #9
    plt.ylabel(ylabel, fontsize=12) #9
    plt.legend(prop={'size': 10}, ncol=1) #7
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
    parser.add_argument('-l', '--labels', nargs='+', default=['Tetragonal_WZ', 'Tetragonal_ZB', 'Square_planar_CuO', 'Square_planar_NbO', 'Octahedral_RS'])
    parser.add_argument('-r', '--row', type=str, default=None)
    parser.add_argument('-c', '--colors', nargs='+', default=['#d62728', '#ff7f0e', '#2ca02c', '#279ff2', '#9467bd'],
                        help='Colors to plot')
    parser.add_argument('-m', '--markers', nargs='+', default=['v', 'v', 's', 's', 'o'],
                        help='Colors to plot')
    parser.add_argument('-a', type=float, default=8)
    parser.add_argument('-b', type=float, default=6)
    
    args = parser.parse_args()        
    plot_patterns_from_multiple_tsv(args.files, args.output, args.xlabel, args.ylabel, args.labels, args.colors, args.markers, args.a, args.b, args.row)

