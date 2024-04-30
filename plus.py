import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

print(f"\033[92m{os.getcwd()}\033[0m")

def process_files(add_files, subtract_files, output_filename):

    metal_rows = {
        '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
        '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
        '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
        }
    
    if row:
        indice = metal_rows[row]
        markers = ['v', 'v', '^', 's', 's', 'o']
        colors = ['#d62728', '#ff7f0e', '#ffd70e', '#2ca02c', '#279ff2', '#9467bd']
    else:
        indice = [f'{a}\n{b}\n{c}' for a, b, c in zip(metal_rows['3d'], metal_rows['4d'], metal_rows['5d'])]
        if '1_Tetrahedral_WZ' in os.getcwd():
            coordination = 'WZ'
            markers = ['v'] * len(filenames)
            colors = plt.cm.Reds(np.linspace(0.1, 0.9, len(filenames)))
        elif '2_Tetrahedral_ZB' in os.getcwd():
            coordination = 'ZB'
            markers = ['v'] * len(filenames)
            colors = plt.cm.Oranges(np.linspace(0.1, 0.9, len(filenames)))
        elif '3_Tetragonal_LT' in os.getcwd():
            coordination = 'LT'
            markers = ['^'] * len(filenames)
            colors = plt.cm.Wistia(np.linspace(0.1, 0.9, len(filenames)))
        elif '4_Square_Planar_TN' in os.getcwd():
            coordination = 'TN'
            markers = ['s'] * len(filenames)
            colors = plt.cm.Greens(np.linspace(0.1, 0.9, len(filenames)))
        elif '5_Square_Planar_33' in os.getcwd():
            coordination = '33'
            markers = ['s'] * len(filenames)
            colors = plt.cm.Blues(np.linspace(0.1, 0.9, len(filenames)))
        elif '6_Octahedral_RS' in os.getcwd():
            coordination = 'RS'
            markers = ['o'] * len(filenames)
            colors = plt.cm.Purples(np.linspace(0.1, 0.9, len(filenames)))        

    merged_df = None
    summed_df = None
    
    png_filename = f"merged_{output}.png"   
    tsv_filename = f"merged_{output}.tsv"
    sum_filename = f"summed_{output}.tsv"

    plt.figure(figsize=(a, b))
    
    # Process addition files
    for filename in add_files:
        df = pd.read_csv(filename, delimiter='\t')
        if summed_df is None:
            summed_df = df
        else:
            summed_df.iloc[:, 1:] += df.iloc[:, 1:]  # Add values excluding the first column

    # Process subtraction files
    for filename in subtract_files:
        df = pd.read_csv(filename, delimiter='\t')
        if summed_df is None:
            summed_df = -df.iloc[:, 1:]  # Subtract values for initialization, excluding the first column
            summed_df.insert(0, df.columns[0], df.iloc[:, 0])  # Add back the first column unchanged
        else:
            summed_df.iloc[:, 1:] -= df.iloc[:, 1:]  # Subtract values excluding the first column

    # Save the processed DataFrame
    if summed_df is not None:
        summed_df.to_csv(f'{output_filename}.tsv', index=False, sep='\t')
        plot_data(summed_df, output_filename)

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
    parser.add_argument('-x', '--xlabel', type=str, default='Element or Lattice parameter (Å)', help="xlabel")
    parser.add_argument('-y', '--ylabel', type=str, default='Energy (eV) or Charge (e)', help="ylabel")
    parser.add_argument('-l', '--labels', nargs='+', default=['Tetrahedral_WZ', 'Tetrahedral_ZB', 'Tetragonal_LT', 'Square_planar_TN', 'Square_planar_33', 'Octahedral_RS'])
    parser.add_argument('-r', '--row', type=str, default=None)
    parser.add_argument('-a', type=float, default=8)
    parser.add_argument('-b', type=float, default=6)
    parser.add_argument('--font', type=float, default=10)
    args = parser.parse_args()

    # Execute file processing
    process_files(args.plus, args.minus, args.output, args.xlabel, args.ylabel, args.labels, args.row, args.a, args.b, args.font)

if __name__ == "__main__":
    main()
