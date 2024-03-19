import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_patterns_from_tsv(file):
    """
    Reads a TSV file, where the first column indicates patterns and the first row indicates elements.
    Then plots each pattern across elements.
    
    Parameters:
    - file: Filename of the TSV file.
    """
    # Read the TSV file, setting the first column as the index
    df = pd.read_csv(file, delimiter='\t', index_col=0)
    
    # Transpose the DataFrame to make plotting more straightforward
    df_transposed = df.T
    
    plt.figure(figsize=(14, 8))

    # Plot each pattern across elements
    for pattern in df_transposed.columns:
        plt.plot(df_transposed.index, df_transposed[pattern], marker='o', linestyle='-', label=pattern)
    
    plt.title('Property Values Across Elements')
    plt.xlabel('Elements')
    plt.ylabel('Property Value')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        plot_patterns_from_tsv(sys.argv[1])
    else:
        print("Please specify the path to the TSV file.")
