import matplotlib.pyplot as plt
from ase.io import read
from statistics import mean
import pandas as pd
from scipy.interpolate import make_interp_spline
import numpy as np

# Define the metals and initialize dataframes
metals = ['Cr', 'Mn', 'Fe', 'Co', 'Ni']
df = pd.DataFrame()
df_mag = pd.DataFrame()
numb = [0] * 5

# Filenames for saving the data and plots
tsv_filename = 'heo_relative_energy.tsv'
png_filename = 'heo_relative_energy.png'
tsv_mag_filename = 'heo_magnetic_moments.tsv'
png_mag_filename = 'heo_magnetic_moments.png'

# Placeholder for pure perovskite energies (example values, replace with actual values)
pure_perovskite = [1.0, 1.1, 1.2, 1.3, 1.4]

def main():
    for i in range(60):
        path = f'/scratch/x2755a09/4_HEO/{i:02d}_/final_with_calculator.json'
        atoms = read(path)
        energy = atoms.get_total_energy()
        for j in range(5):
            metal = metals[j]
            numb[j] = len([atom for atom in atoms if atom.symbol == metal])
            magmom = mean([atoms.get_magnetic_moments()[atom.index] for atom in atoms if atom.symbol == metal])
            df_mag.at[metal, i] = magmom
        relative_energy = energy - sum(numb[j] * pure_perovskite[j] for j in range(5))
        df.at['energy', i] = relative_energy

    # Save data to TSV files
    df.to_csv(tsv_filename, sep='\t')
    df_mag.to_csv(tsv_mag_filename, sep='\t')

    # Plotting the data
    plotting(df=df, ylabel='Relative energy (eV)', png_filename=png_filename)
    plotting(df=df_mag, ylabel='Magnetic moments', png_filename=png_mag_filename)
    
def plotting(df, ylabel, png_filename):
    plt.figure(figsize=(10, 6))
    for col in df.columns:
        data = df[col]
        x_new = np.linspace(data.index.min(), data.index.max(), 300)
        spl = make_interp_spline(data.index, data, k=3)
        smooth_data = spl(x_new)
        plt.plot(x_new, smooth_data, label=col)
    plt.xlabel('Index')
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(png_filename)
    plt.show()

if __name__ == "__main__":
    main()
