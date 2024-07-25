import matplotlib.pyplot as plt
from ase.io import read
from statistics import mean
import pandas as pd
import numpy as np
import os
import glob
import re

# Define the metals and initialize dataframes
prvs = {'Cr': -329.68518914, 'Mn': -317.97145238, 'Fe': -306.60147094, 'Co': -286.30355237, 'Ni': -279.92522654}
clrs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
df = pd.DataFrame()
df_mag = pd.DataFrame()
numb = [0] * 5

# Filenames for saving the data and plots
tsv_filename = 'heo_relative_energy.tsv'
png_filename = 'heo_relative_energy.png'
tsv_mag_filename = 'heo_magnetic_moments.tsv'
png_mag_filename = 'heo_magnetic_moments.png'
png_gap_filename = 'heo_band_gap.png'

pattern = re.compile(r"Band Gap:\s+([\d.]+)\s+eV")
    
for i in range(60):
    path = f'/scratch/x2755a09/4_HEO/{i:02d}_/final_with_calculator.json'
    gap_path = f'/scratch/x2755a09/4_HEO/{i:02d}_/gap.txt'
    if not os.path.exists(path):
        print(f"Path does not exist: {path}")
    atoms = read(path)
    energy = atoms.get_total_energy()
    for j, metal in enumerate(prvs.keys()):
        numb[j] = len([atom for atom in atoms if atom.symbol == metal])
        magmom = mean([abs(atoms.get_magnetic_moments()[atom.index]) for atom in atoms if atom.symbol == metal])
        df_mag.at[i, metal] = magmom
    relative_energy = energy - sum(numb[j] * prvs[metal] / 8 for j, metal in enumerate(prvs.keys()))
    df.at[i, 'energy'] = relative_energy
    if os.path.exists(gap_path):
        with open(gap_path, 'r') as file:
            contents = file.read()
            match = pattern.search(contents)
            if match:
                df.at[i, 'bandgap'] = float(match.group(1))
            else:
                print(f"No band gap found in {gap_path}")
    else:
        print(f"Gap file does not exist: {gap_path}")

# Save data to TSV files
df.to_csv(tsv_filename, sep='\t', float_format='%.2f')
print(f"Data saved to {tsv_filename}")
df_mag.to_csv(tsv_mag_filename, sep='\t', float_format='%.2f')
print(f"Data saved to {tsv_mag_filename}")

# Plotting the data
plt.figure(figsize=(8, 6))
plt.hist(df['energy'].dropna(), bins=np.arange(-2.0, 0.1, 0.1), alpha=0.5, width=0.09)
plt.xlabel('Relative energy (eV)')
plt.ylabel('Frequency')
plt.xticks(np.arange(-2.0, 0.1, 0.2))
plt.savefig(png_gap_filename, bbox_inches="tight")
print(f"Figure saved as {png_gap_filename}")
plt.close()

# Plotting the data
plt.figure(figsize=(8, 6))
plt.hist(df['bandgap'].dropna(), bins=np.arange(0.0, 0.5, 0.1),alpha=0.5, width=0.09)
plt.xlabel('Band gap (eV)')
plt.ylabel('Frequency')
plt.xticks(np.arange(0.0, 0.5, 0.1))
plt.xlim(-0.05, 0.55)
plt.savefig(png_filename, bbox_inches="tight")
print(f"Figure saved as {heo_band_gap}")
plt.close()

# Plotting the magnetic moments histogram
for k, column in enumerate(df_mag.columns):
    plt.figure(figsize=(8, 6))
    plt.hist(df_mag[column].dropna(), bins=np.arange(0, 5, 0.1), alpha=0.5, color=clrs[k], label=str(column), width=0.09)
    plt.xlabel('Magnetic Moments')
    plt.ylabel('Frequency')
    plt.xticks(np.arange(0, 5, 1))
    plt.xlim(-0.5, 5.5)
    plt.legend(title="B sites")
    plt.savefig(f'heo_magnetic_moments_{column}.png', bbox_inches="tight")
    print(f"Figure saved as heo_magnetic_moments_{column}.png")
    plt.close()

plt.figure(figsize=(8, 6))
bins = np.arange(0, 5, 0.2)
bin_width = 0.2 / (len(df_mag.columns) + 1)  # Calculate new width for each bar
for idx, column in enumerate(df_mag.columns):
    plt.hist(df_mag[column].dropna(), bins=bins + idx * bin_width, alpha=0.5, label=str(column), width=bin_width)
plt.xlabel('Magnetic Moments')
plt.ylabel('Frequency')
plt.xticks(np.arange(0, 5, 1))
plt.xlim(-0.5, 5.5)
plt.legend(title="B sites")
plt.savefig(png_mag_filename, bbox_inches="tight")
print(f"Figure saved as {png_mag_filename}")
plt.close()