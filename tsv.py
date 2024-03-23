import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def plot_patterns_from_multiple_tsv(filenames, png_filename, xlabel, ylabel, labels):
    """
    Reads multiple TSV files, where the first column of each file indicates patterns and the first row indicates elements.
    Then, plots each pattern across elements from all files.
    
    Parameters:
    - filenames: List of filenames of the TSV files.
    """
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
    final_indices = pd.Index([index.strip() for index in merged_indices])

    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#279ff2', '#9467bd']
    markers = ['s', 'd', 'o', '<', 'D']
    # colors = ['#d62728', '#ff7f0e', '#39d439', '#2ca02c', '#279ff2', '#1f77b4', '#9467bd']
    # markers = ['s', 'd', 'p', 'o', '>', '<', 'D']

    n = len(filenames)
    for j, file in enumerate(reversed(filenames)):  # Correctly reversed with enumeration
        label_index = n - j - 1
        label = labels[label_index] if labels and label_index < len(labels) else file.split('/')[-1].replace('.tsv', '')
        df = pd.read_csv(file, delimiter='\t', index_col=0).T
        print(df.columns)
        if pattern in df.columns:
            data = df[pattern].dropna()  # Vectorized approach to drop NaN values
            x = data.index
            plt.plot(x, data, marker=markers[label_index], color=colors[label_index], label=label)

    # filenames.reverse()
    # for i, file in enumerate(filenames):
    #     j = n-i-1
    #     label = labels[j] if labels and j < len(labels) else file.split('/')[-1].replace('.tsv', '')
    #     df = pd.read_csv(file, delimiter='\t', index_col=0).T
    #     x = []
    #     filtered_df = []
    #     for i, v in enumerate(df[pattern]):
    #         if v is not np.nan:
    #             x.append(i)
    #             filtered_df.append(v)
    #     for pattern in df.columns:
    #         plt.plot(x, filtered_df, marker=markers[j], color=colors[j], 
    #                  # linewidth=1, 
    #                  label=f"{label}")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
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
    parser.add_argument('-o', '--output', dest='filename', type=str, default='merged', help="The filename for the output PNG file.")
    parser.add_argument('-x', '--xlabel', type=str, default='Element or Lattice parameter (Å)', help="xlabel")
    parser.add_argument('-y', '--ylabel', type=str, default='Energy (eV) or Charge (e)', help="ylabel")
    parser.add_argument('-l', '--labels', nargs='*', help="Custom labels for each file", default=None)
    args = parser.parse_args()
    png_filename = f"merged_{args.filename}.png"    
    plot_patterns_from_multiple_tsv(args.files, png_filename, args.xlabel, args.ylabel, args.labels)

