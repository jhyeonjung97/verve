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

    # Dictionary to hold data frames for each pattern
    data_frames = {}

    for file in filenames:
        # Extract the identifier (e.g., "1_afm", "2_fm") from the filename for legend
        identifier = file.split('/')[0]
        
        # Read the TSV file into a DataFrame
        df = pd.read_csv(file, delimiter='\t', index_col='Pattern')
        
        # Transpose the DataFrame to have patterns as columns, elements as rows
        df_transposed = df.T

        # Plot each pattern with elements as x-axis
        for pattern in df_transposed.columns:
            if pattern not in data_frames:
                data_frames[pattern] = pd.DataFrame()
            data_frames[pattern][identifier] = df_transposed[pattern]

    # Plotting each pattern in a subplot
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
    # Expecting the command-line usage to be:
    # python script_name.py file1.tsv file2.tsv ...
    if len(sys.argv) > 1:
        plot_merged_tsv(sys.argv[1:])
    else:
        print("Please specify the TSV files to be plotted.")