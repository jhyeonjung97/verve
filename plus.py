import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def process_files(add_files, subtract_files, output_filename):
    # Initialize the DataFrame result
    df_result = None

    # Process addition files
    for filename in add_files:
        df = pd.read_csv(filename, delimiter='\t')
        if df_result is None:
            df_result = df
        else:
            df_result.iloc[:, 1:] += df.iloc[:, 1:]  # Add values excluding the first column

    # Process subtraction files
    for filename in subtract_files:
        df = pd.read_csv(filename, delimiter='\t')
        if df_result is None:
            df_result = -df.iloc[:, 1:]  # Subtract values for initialization, excluding the first column
            df_result.insert(0, df.columns[0], df.iloc[:, 0])  # Add back the first column unchanged
        else:
            df_result.iloc[:, 1:] -= df.iloc[:, 1:]  # Subtract values excluding the first column

    # Save the processed DataFrame
    if df_result is not None:
        df_result.to_csv(f'{output_filename}.tsv', index=False, sep='\t')
        plot_data(df_result, output_filename)

def plot_data(df, output_filename):
    plt.figure(figsize=(10, 6))
    for column in df.columns[1:]:  # Skip plotting the first column
        plt.plot(df.iloc[:, 0], df[column], marker='o', label=column)  # Assuming the first column is a suitable x-axis
    plt.xlabel('Index')
    plt.ylabel('Values')
    plt.title('Data Plot')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{output_filename}.png')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Process and plot TSV files.')
    parser.add_argument('-p', '--plus', nargs='+', help='Files to sum', default=[])
    parser.add_argument('-m', '--minus', nargs='+', help='Files to subtract', default=[])
    parser.add_argument('-o', '--output', help='Output file name', default='output')
    args = parser.parse_args()

    # Execute file processing
    process_files(args.plus, args.minus, args.output)

if __name__ == "__main__":
    main()
