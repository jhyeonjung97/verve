import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse

def plot_patterns_from_multiple_tsv(filenames, output, xlabel, ylabel, labels, sumup):

    metal_rows = {
        '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
        '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
        '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
        }
    
    merged_df = None
    summed_df = None
    merged_indice = None
    
    png_filename = f"merged_{output}.png"   
    tsv_filename = f"merged_{output}.tsv"
    sum_filename = f"summed_{output}.tsv"
    
    plt.figure(figsize=(8, 6))
    # plt.figure(figsize=(4, 3))

    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#279ff2', '#9467bd']
    markers = ['s', 'd', 'p', 'o', '>', '<', 'D']
    

    for j, file in enumerate(filenames):
        df = pd.read_csv(file, delimiter='\t').iloc[:, 1:]
        df.columns = labels[j] if isinstance(labels[j], list) else [labels[j]]
        if sumup:
            summed_df = df if summed_df is None else summed_df + df
        else:
            merged_df = pd.concat([merged_df, df], axis=1)

    if not sumup:
        for j, pattern in enumerate(merged_df.columns):
            x = range(len(merged_df[pattern]))
            filtered_df = merged_df[pattern].dropna()
            if filtered_df.empty:
                print(f"No values found for pattern: {pattern}")
                continue
            plt.plot(x, filtered_df, marker=markers[j % len(markers)], color=colors[j % len(colors)], label=labels[j % len(labels)])
        if 'hexa_ratio' in df.columns:
            plt.plot(x, [1.633]*len(x), linestyle=':', label='hexa_ratio0', color='black')
    else:
        summed_df.to_csv(sum_filename, sep='\t')
        print(f"Summed data saved to {sum_filename}")
        exit()
    
    merged_df.to_csv(tsv_filename, sep='\t')
    print(f"Merged data saved to {tsv_filename}")

    # for row in metal_rows:
    #     merged_indices = metal_rows[row] if merged_indices is None else merged_indices + metal_rows[row]
    for row in metal_rows.values():  # Iterate over the list of metal symbols
        merged_indices += ' '.join(row) + '\n'
    plt.xticks(np.arange(len(metal_rows['3d'])), merged_indices)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    # plt.xlabel(xlabel, fontsize=9)
    # plt.ylabel(ylabel, fontsize=9)
    # plt.xticks(fontsize=9)
    # plt.yticks(fontsize=9)
    # plt.grid(True)
    # plt.legend(prop={'size': 7}, ncol=1)
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
    parser.add_argument('--sum', dest='sumup', action='store_true', default=False, help="sum up multiple tsv files")
    parser.add_argument('-l', '--labels', nargs='+', default=['Octahedral', 'Wurtzite', 'Zinc_Blende', 'CuO', 'NbO'], 
                        help="Custom labels for each file")
    parser.add_argument('-c', '--colors', nargs='+', default=['#d62728', '#ff7f0e', '#2ca02c', '#279ff2', '#9467bd'],
                        help='Colors to plot')
    parser.add_argument('-m', '--markers', nargs='+', default=['s', 'd', 'p', 'o', '>', '<', 'D'],
                        help='Colors to plot')
    
    args = parser.parse_args()        
    plot_patterns_from_multiple_tsv(args.files, args.output, args.xlabel, args.ylabel, args.labels, args.sumup)

