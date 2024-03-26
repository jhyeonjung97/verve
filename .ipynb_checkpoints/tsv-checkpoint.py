import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse

def plot_patterns_from_multiple_tsv(filenames, output, xlabel, ylabel, labels, sumup):
    """
    Reads multiple TSV files, where the first column of each file indicates patterns and the first row indicates elements.
    Then, plots each pattern across elements from all files.
    
    Parameters:
    - filenames: List of filenames of the TSV files.
    """
    merged_df = pd.DataFrame()
    summed_df = None
    
    png_filename = f"merged_{output}.png"   
    tsv_filename = f"merged_{output}.tsv"
    sum_filename = f"summed_{output}.tsv"
    
    plt.figure(figsize=(8, 6))
    # plt.figure(figsize=(4, 3))
    
    all_indices_sets = []
    longest_length = 0
    for file in filenames:
        df = pd.read_csv(file, delimiter='\t', index_col=0).T
        current_length = len(df.index.tolist())
        if current_length > longest_length:
            longest_length = current_length
        indices_tuple = tuple(df.index)
        all_indices_sets.append(indices_tuple)
    
    seen = set()
    unique_indices_sets = []
    for indices in all_indices_sets:
        if indices not in seen:
            unique_indices_sets.append(indices)
            seen.add(indices)

    merged_indices = ['' for _ in range(longest_length)]
    for i in range(longest_length):
        for indices in unique_indices_sets:
            if i < len(indices):  
                merged_indices[i] += str(indices[i]) + '\n'
            else:
                merged_indices[i] += "NA\n"

    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#279ff2', '#9467bd']
    markers = ['s', 'd', 'p', 'o', '>', '<', 'D']

    # n = len(filenames)
    reversed_filenames = list(reversed(filenames))
    reversed_labels = list(reversed(labels))
    reversed_colors = list(reversed(colors))
    reversed_markers = list(reversed(markers))
    for j, file in enumerate(reversed_filenames):  # Correctly reversed with enumeration
        # label_index = n - j - 1
        df = pd.read_csv(file, delimiter='\t', index_col=0)
        merged_df = pd.concat([merged_df, df], axis=1)
        if summed_df is None:
            summed_df = df.copy()  # First file, so just copy it
        else:
            summed_df = summed_df.add(df, fill_value=0) 
        transposed_df = df.T
        
        if not sumup:
            for pattern in transposed_df.columns:
                x = []
                filtered_df = []
                for i, v in enumerate(transposed_df[pattern]):
                    if not np.isnan(v): 
                        x.append(i)
                        filtered_df.append(v)
                if not filtered_df:
                    print(f"No values found for pattern: {pattern}")
                    continue
                plt.plot(x, filtered_df, marker=reversed_markers[j], color=reversed_colors[j], label = reversed_labels[j])
            if 'hexa_ratio' in transposed_df.columns:
                plt.plot(x, [1.633]*len(x), linestyle=':', label='hexa_ratio0', color=color)
    
    if sumup:
        summed_df.to_csv(sum_filename, sep='\t')
        print(f"Summed data saved to {sum_filename}")
        exit()
        
    merged_df.to_csv(tsv_filename, sep='\t')
    print(f"Merged data saved to {tsv_filename}")
    
    plt.xticks(np.arange(len(merged_indices)), merged_indices)
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
    
    merged_df.to_csv(tsv_filename, sep='\t')
    print(f"Merged data saved to {tsv_filename}")
    
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

