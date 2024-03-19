import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_patterns_from_multiple_tsv(filenames):
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
    
    plt.title('Property Values Across Elements from Multiple Files')
    plt.xlabel('Elements')
    plt.ylabel('Property Value')
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        plot_patterns_from_multiple_tsv(sys.argv[1:])
    else:
        print("Please specify the path to the TSV files.")
