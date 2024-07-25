import matplotlib.pyplot as plt
from ase.io import read
from statistics import mean
import pandas as pd
import numpy as np
import os
import re

# Define the metals and initialize dataframes
prvs = ['Cr', 'Mn', 'Fe', 'Co', 'Ni']
clrs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
df = pd.DataFrame()
df_mag = pd.DataFrame()
df_ref = pd.DataFrame()
numb = [0] * 5

# Filenames for saving the data and plots
tsv_filename = 'heo_relative_energy.tsv'
png_filename = 'heo_relative_energy.png'
tsv_mag_filename = 'heo_magnetic_moments.tsv'
tsv_ref_filename = 'heo_references.tsv'
png_mag_filename = 'heo_magnetic_moments.png'
png_gap_filename = 'heo_band_gap.png'
png_dos_filename = 'heo_density_of_states.png'

# Regular expressions to extract band gap and DOS information
pattern_gap = re.compile(r"Band Gap:\s+([\d.]+)\s+eV")
pattern_dos = re.compile(r"Average Energy \(band center\):\s+([-+]?\d*\.\d+|\d+)")

def main():
    for i in range(5):
        path = f'/scratch/x2755a09/4_HEO/pure/{i+1}_{prvs[i]}/final_with_calculator.json'
        gap_path = f'/scratch/x2755a09/4_HEO/pure/{i+1}_{prvs[i]}/gap.txt'
        dos_path = f'/scratch/x2755a09/4_HEO/pure/{i+1}_{prvs[i]}/dos.txt'
        
        # Read total energy and magnetic moments from JSON file
        if os.path.exists(path):
            atoms = read(path)
            df_ref.at[i, 'energy'] = atoms.get_total_energy()
            df_ref.at[i, 'magmom'] = mean([abs(atoms.get_magnetic_moments()[atom.index]) for atom in atoms if atom.symbol == prvs[i]])
        
        # Read band gap from text file
        if os.path.exists(gap_path):
            with open(gap_path, 'r') as file:
                lines = file.read()
                match = pattern_gap.search(lines)
                if match:
                    df_ref.at[i, 'bandgap'] = float(match.group(1))
        
        # Read DOS information from text file and calculate Md2Op
        if os.path.exists(dos_path):
            with open(dos_path, 'r') as file:
                lines = file.read()
                matches = pattern_dos.findall(lines)
                if len(matches) == 2:
                    df_ref.at[i, 'Md2Op'] = float(matches[0]) - float(matches[1])
                    
    for i in range(60):
        path = f'/scratch/x2755a09/4_HEO/{i:02d}_/final_with_calculator.json'
        gap_path = f'/scratch/x2755a09/4_HEO/{i:02d}_/gap.txt'
        dos_path = f'/scratch/x2755a09/4_HEO/{i:02d}_/dos.txt'
        if os.path.exists(path):
            atoms = read(path)
            energy = atoms.get_total_energy()
            for m, metal in enumerate(prvs):
                numb[m] = len([atom for atom in atoms if atom.symbol == metal])
                df_mag.at[i, metal] = mean([abs(atoms.get_magnetic_moments()[atom.index]) for atom in atoms if atom.symbol == metal])
            relative_energy = energy - sum(numb[m] * df_ref.at[m, 'energy'] / 8 for m, metal in enumerate(prvs))
            df.at[i, 'energy'] = relative_energy
        if os.path.exists(gap_path):
            with open(gap_path, 'r') as file:
                lines = file.read()
                match = pattern_gap.search(lines)
                if match:
                    df.at[i, 'bandgap'] = float(match.group(1))
        if os.path.exists(dos_path):
            with open(dos_path, 'r') as file:
                lines = file.read()
                matches = pattern_dos.findall(lines)
                if len(matches) == 2:
                    df.at[i, 'Md2Op'] = float(matches[0]) - float(matches[1])

    saving(df, tsv_filename)
    saving(df_mag, tsv_mag_filename)
    saving(df_ref, tsv_ref_filename)

    for i in range(5):
        df_ref.at[i, 'energy'] = 0
        
    # plotting('energy', np.arange(-2.0, 0.0, 0.1), 'Relative energy (eV)', np.arange(-2.0, 0.1, 0.2), -2.1, 0.1, 0.09, png_filename)
    plotting('bandgap', np.arange(0.0, 2.2, 0.1), 'Band gap (eV)', np.arange(0.0, 2.3, 0.2), -0.1, 2.3, 0.09, png_gap_filename)
    # plotting('Md2Op', np.arange(0.0, 0.5, 0.05), 'M3d - O2p (eV)', np.arange(0.0, 0.5, 0.1), -0.05, 0.55, 0.045, png_dos_filename)

    # for i, column in enumerate(df_mag.columns):
    #     plt.figure(figsize=(8, 6))
    #     plt.hist(df_mag[column].dropna(), bins=np.arange(0, 6, 0.1), alpha=0.5, color=clrs[i], label=str(column), width=0.09)
    #     plt.axvline(x=df_ref.at[i, 'magmom'], color=clrs[i], linestyle='--')
    #     plt.xlabel('Magnetic Moments')
    #     plt.ylabel('Frequency')
    #     plt.xticks(np.arange(0, 6, 1))
    #     plt.xlim(-0.5, 5.5)
    #     plt.legend(title="B sites")
    #     plt.savefig(f'heo_magnetic_moments_{column}.png', bbox_inches="tight")
    #     print(f"Figure saved as heo_magnetic_moments_{column}.png")
    #     plt.close()
    
    # plt.figure(figsize=(8, 6))
    # bins = np.arange(0, 6, 0.2)
    # bin_width = 0.2 / (len(df_mag.columns) + 1)  # Calculate new width for each bar
    # for idx, column in enumerate(df_mag.columns):
    #     plt.hist(df_mag[column].dropna(), bins=bins + idx * bin_width, alpha=0.5, label=str(column), width=bin_width)
    # plt.xlabel('Magnetic Moments')
    # plt.ylabel('Frequency')
    # plt.xticks(np.arange(0, 6, 1))
    # plt.xlim(-0.5, 5.5)
    # plt.legend(title="B sites")
    # plt.savefig(png_mag_filename, bbox_inches="tight")
    # print(f"Figure saved as {png_mag_filename}")
    # plt.close()

def saving(df, filename):
    df.to_csv(filename, sep='\t', float_format='%.2f')
    print(f"Data saved to {filename}")

def plotting(pattern, bins, xlabel, xticks, xmin, xmax, width, filename):
    plt.figure(figsize=(8, 6))
    plt.hist(df[pattern].dropna(), bins=bins, alpha=0.5, width=width)
    for i in range(5):
        plt.axvline(x=df_ref.at[i, pattern], color=clrs[i], linestyle='--')
    plt.axvline(x=0, color='gray', linestyle='--')
    plt.xlabel(xlabel)
    plt.ylabel('Frequency')
    plt.xticks(xticks)
    plt.xlim(xmin, xmax)
    plt.savefig(filename, bbox_inches="tight")
    print(f"Figure saved as {filename}")
    plt.close()

if __name__ == '__main__':
    main()