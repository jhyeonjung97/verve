import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_merged_tsv(filenames):
    """
    Reads TSV files, merges their data based on patterns, and plots the merged result.
    
    Parameters:
    - filenames: List of filenames of the TSV files.
    """
    plt.figure(figsize=(14, 8))
    data_frames = {}
    for file in filenames:
        identifier = file.split('/')[0]
        df = pd.read_csv(file, delimiter='\t', index_col='Pattern')
        for pattern in df.columns:
            if pattern not in data_frames:
                data_frames[pattern] = pd.DataFrame()
            data_frames[pattern][identifier] = df[pattern]
    num_patterns = len(data_frames)
    cols = 2
    rows = num_patterns // cols + (num_patterns % cols > 0)
    fig, axes = plt.subplots(rows, cols, figsize=(14, 4 * rows), constrained_layout=True)

    for i, (pattern, df_pattern) in enumerate(data_frames.items()):
        ax = axes.flatten()[i] if num_patterns > 1 else axes
        df_pattern.plot(ax=ax, marker='o', linestyle='-')
        ax.set_title(pattern)
        ax.set_xlabel('Elements')
        ax.set_ylabel('Value')
        ax.grid(True)
        ax.legend()

    plt.suptitle('Comparison of Patterns Across Files')
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        plot_merged_tsv(sys.argv[1:])
    else:
        print("Please specify the TSV files to be plotted.")