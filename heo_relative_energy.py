import matplotlib.pyplot as plt
from ase.io import read
from statistics import mean
import pandas as pd
import numpy as np
import os

# Define the metals and initialize dataframes
prvs = {'Cr': -329.68518914, 'Mn': -317.97145238, 'Fe': -306.60147094, 'Co': -286.30355237, 'Ni': -279.92522654}
df = pd.DataFrame()
df_mag = pd.DataFrame()
numb = [0] * 5

# Filenames for saving the data and plots
tsv_filename = 'heo_relative_energy.tsv'
png_filename = 'heo_relative_energy.png'
tsv_mag_filename = 'heo_magnetic_moments.tsv'
png_mag_filename = 'heo_magnetic_moments.png'

def histogram(df, xlabel, png_filename):
    plt.figure(figsize=(12, 8))
    for column in df.columns:
        plt.hist(df[column].dropna(), bins=20, alpha=0.5, label=str(column))
    plt.xlabel(xlabel)
    plt.ylabel('Frequency')
    plt.legend(title="Metals")
    plt.savefig(png_filename)
    plt.show()

def main():
    for i in range(60):
        path = f'/scratch/x2755a09/4_HEO/{i:02d}_/final_with_calculator.json'
        if not os.path.exists(path):
            print(f"Path does not exist: {path}")
            continue
        atoms = read(path)
        energy = atoms.get_total_energy()
        for j, metal in enumerate(prvs.keys()):
            numb[j] = len([atom for atom in atoms if atom.symbol == metal])
            magmom = mean([atoms.get_magnetic_moments()[atom.index] for atom in atoms if atom.symbol == metal])
            df_mag.at[i, metal] = magmom
        relative_energy = energy - sum(numb[j] * prvs[metal] / 8 for j, metal in enumerate(prvs.keys()))
        df.at[i, 'energy'] = relative_energy

    # Save data to TSV files
    df.to_csv(tsv_filename, sep='\t')
    print(f"Data saved to {tsv_filename}")
    df_mag.to_csv(tsv_mag_filename, sep='\t')
    print(f"Data saved to {tsv_mag_filename}")

    # Plotting the data
    histogram(df=df, xlabel='Relative energy (eV)', png_filename=png_filename)
    histogram(df=df_mag, xlabel='Magnetic Moments', png_filename=png_mag_filename)

if __name__ == "__main__":
    main()
