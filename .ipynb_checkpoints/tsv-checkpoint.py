import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def plot_patterns_from_multiple_tsv(filenames, png_filename, xlabel, ylabel):
    """
    Reads multiple TSV files, where the first column of each file indicates patterns and the first row indicates elements.
    Then, plots each pattern across elements from all files.
    
    Parameters:
    - filenames: List of filenames of the TSV files.
    """
    plt.figure(figsize=(14, 8))
    for file in filenames:
        label = file.split('/')[-1].replace('.tsv', '')
        df = pd.read_csv(file, delimiter='\t', index_col=0).T
        for pattern in df.columns:
            plt.plot(df.index, df[pattern], marker='o', linestyle='-', label=f"{label}")
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
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
    args = parser.parse_args()
    png_filename = f"merged_{args.filename}.png"    
    plot_patterns_from_multiple_tsv(args.files, png_filename, args.xlabel, args.ylabel)

