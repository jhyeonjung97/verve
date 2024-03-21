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
    all_indexes = []
    for file in filenames:
        df = pd.read_csv(file, delimiter='\t', index_col=0).T
        all_indexes.extend(df.index.astype(float))
        
    merged_index = pd.Index(np.unique(all_indexes)).sort_values()
   
    for i, file in enumerate(filenames):
        label = labels[i] if labels and i < len(labels) else file.split('/')[-1].replace('.tsv', '')
        df = pd.read_csv(file, delimiter='\t', index_col=0).T
        # df.index = df.index.astype(float)
        df_interpolated = df.reindex(df.index.union(merged_index)).interpolate(method='index').reindex(merged_index)
        for pattern in df.columns:
            plt.plot(merged_index, df_interpolated[pattern], df[pattern], 
                     arker='o', linestyle='-', label=f"{label}")
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

