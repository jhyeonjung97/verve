import sys
import pandas as pd
import matplotlib.pyplot as plt

def read_and_plot_tsv_files(filenames, xlabel, ylabel, output_filename):
    """
    Reads multiple TSV files from given filenames, merges their data, and plots the merged result.
    
    Parameters:
    - filenames: List of filenames of the TSV files.
    - xlabel: Label for the x-axis.
    - ylabel: Label for the y-axis.
    - output_filename: Filename for the saved plot.
    """
    plt.figure(figsize=(10, 6))

    # Iterate through each provided TSV filename
    for tsv_file in filenames:
        # Read the TSV file into a DataFrame
        df = pd.read_csv(tsv_file, delimiter='\t')
        
        # Plot the data
        plt.plot(df.iloc[:,0], df.iloc[:,1], marker='o', linestyle='-', label=tsv_file)
    
    plt.title('Merged Data from TSV Files')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation='vertical')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_filename, bbox_inches="tight")
    print(f"Figure saved as {output_filename}")
    plt.close()

if __name__ == "__main__":
    # Command-line usage: python tsv.py file1.tsv file2.tsv ... fileN.tsv
    if len(sys.argv) > 1:
        filenames = sys.argv[1:]  # Exclude the script name itself
        read_and_plot_tsv_files(filenames, xlabel='X-Axis Label', ylabel='Y-Axis Label', output_filename='merged_plot.png')
    else:
        print("No TSV files provided. Please specify the files as arguments.")
