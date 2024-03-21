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
    plt.figure(figsize=(14, 8))
    all_indices_sets = []
    longest_length = 0
    for file in filenames:
        df = pd.read_csv(file, delimiter='\t', index_col=0).T
        if len(df.index.tolist()) > longest_length:
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
    # Iterate through each position up to the longest_length
    for j in range(longest_length):
        # Concatenate the index label at position j from each unique set, if available
        for indices in unique_indices_sets:
            if j < len(indices):  # Check if j is within the bounds of the current set of indices
                merged_indices[j] += str(indices[j]) + " "  # Concatenate with a space for readability
    final_indices = pd.Index([index.strip() for index in merged_indices])
    
    print(final_indices)
    # for i, indices in enumerate(unique_indices_sets):
    #     for j in range(1, longest_length):
    #         merged_indices[j] += str(indices[i][j])
    # final_indices = pd.Index(merged_indices)
    

    for file in filenames:
        df = pd.read_csv(file, delimiter='\t', index_col=0).T
        current_indices = df.index.tolist()  # Convert the current set of indices to a list
        current_length = len(current_indices)  # Find the length of the current set of indices
        
        # If the current set of indices is longer than any we've seen before, update our records
        if current_length > longest_length:
            longest_indices = current_indices
            longest_length = current_length
        
    print(unique_indices_sets)
    # 
   
    for i, file in enumerate(filenames):
        label = labels[i] if labels and i < len(labels) else file.split('/')[-1].replace('.tsv', '')
        df = pd.read_csv(file, delimiter='\t', index_col=0).T
        for pattern in df.columns:
            plt.plot(merged_index, df[pattern], marker='o', linestyle='-', label=f"{label}")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(merged_index, rotation=45)
    # plt.xticks(np.arange(len(dir_names)), dir_names, rotation='vertical')
    # plt.grid(True)
    plt.legend()
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

