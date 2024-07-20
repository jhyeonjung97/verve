import matplotlib.pyplot as plt
from ase.io import read
from statistics import mean
import glob
import os
import pandas as pd
from scipy.interpolate import make_interp_spline
import numpy as np

# Define the rows and spins
rows = {
    '3d': ['Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu'],
    '4d': ['Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd'],
    '5d': ['Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt']
}
spins = {'LS': '#ff7f0e', 'IS': '#279ff2', 'HS': '#9467bd'}
dzs = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]

# Energies and corrections
nitrogen_E = -16.64503942 # eV, DFT
nitrogen_TS = 0.635139 # eV, at 298.15 K, 1 atm
nitrogen_ZPE = 0.096279 # eV, at 298.15 K, 1 atm
nitrogen = (nitrogen_E - nitrogen_TS + nitrogen_ZPE) / 2

carbon = -9.357363435 # eV, DFT

metal_path = '/scratch/x2755a09/3_MNC/gas/metals.tsv'
metal_df = pd.read_csv(metal_path, delimiter='\t', index_col=0)

def main():
    for row_key, metals in rows.items():
        for i, metal in enumerate(metals):
            df = pd.DataFrame()
            df_rel = pd.DataFrame()
            df_mag = pd.DataFrame()
            df_relaxed = pd.DataFrame()
            df_relaxed_rel = pd.DataFrame()
            df_relaxed_mag = pd.DataFrame()
            
            tsv_filename = f'{row_key}_{i+2}{metal}_Ef.tsv'
            png_filename = f'{row_key}_{i+2}{metal}_Ef.png'
            tsv_rel_filename = f'{row_key}_{i+2}{metal}_rel.tsv'
            png_rel_filename = f'{row_key}_{i+2}{metal}_rel.png'
            tsv_mag_filename = f'{row_key}_{i+2}{metal}_mag.tsv'
            png_mag_filename = f'{row_key}_{i+2}{metal}_mag.png'

            for spin in spins.keys():
                path_pattern = f'/scratch/x2755a09/3_MNC/{row_key}/*_{metal}/*_{spin}'
                matching_paths = glob.glob(path_pattern)

                for path in matching_paths:
                    for j, dz in enumerate(dzs):
                        atoms_path = os.path.join(path, f'{j}_', 'moments.json')
                        if os.path.exists(atoms_path):
                            print(atoms_path)
                            atoms = read(atoms_path)
                            energy = atoms.get_total_energy()
                            # numb_N = len([atom for atom in atoms if atom.symbol == 'N'])
                            # numb_C = len([atom for atom in atoms if atom.symbol == 'C'])
                            # formation_energy = energy - metal_df.at[metal, 'energy'] - numb_C * carbon - numb_N * nitrogen
                            formation_energy = energy - metal_df.at[metal, 'energy'] - 26 * carbon - 4 * nitrogen
                            df.at[dz, spin] = formation_energy
                            try:
                                magmoms = atoms.get_magnetic_moments()
                                for atom in atoms:
                                    if atom.symbol not in ['N', 'C', 'O', 'H']:
                                        df_mag.at[dz, spin] = abs(magmoms[atom.index]) 
                            except:
                                df_mag.at[dz, spin] = 0

                    relaxed_path = os.path.join(path, 'relaxed_', 'moments.json')
                    if os.path.exists(relaxed_path):
                        atoms = read(relaxed_path)
                        zN = mean([atom.z for atom in atoms if atom.symbol == 'N'])
                        zM = mean([atom.z for atom in atoms if atom.symbol not in ['N', 'C', 'O', 'H']])
                        dz_relaxed = abs(zN - zM)
                        energy = atoms.get_total_energy()
                        # numb_N = len([atom for atom in atoms if atom.symbol == 'N'])
                        # numb_C = len([atom for atom in atoms if atom.symbol == 'C'])
                        # formation_energy = energy - metal_df.at[metal, 'energy'] - numb_C * carbon - numb_N * nitrogen
                        formation_energy = energy - metal_df.at[metal, 'energy'] - 26 * carbon - 4 * nitrogen
                        df_relaxed.at[dz_relaxed, spin] = formation_energy
                        try:
                            magmoms = atoms.get_magnetic_moments()[atom.index]
                            for atom in atoms:
                                if atom.symbol not in ['N', 'C', 'O', 'H']:
                                    df_relaxed_mag.at[dz_relaxed, spin] = abs(magmoms[atom.index]) 
                        except:
                            df_relaxed_mag.at[dz_relaxed, spin] = 0

            if 'HS' in df.columns and 'LS' in df.columns:
                df_rel['HS-LS'] = df['HS'] - df['LS']
            else:
                print(f"Warning: 'HS' or 'LS' column not found in df for {row_key}_{metal}")

            if 'HS' in df_relaxed.columns and 'LS' in df_relaxed.columns:
                df_relaxed_rel['HS-LS'] = df_relaxed['HS'] - df_relaxed['LS']
            else:
                print(f"Warning: 'HS' or 'LS' column not found in df_relaxed for {row_key}_{metal}")

            combining(df=df, df_relaxed=df_relaxed, tsv_filename=tsv_filename)
            combining(df=df_rel, df_relaxed=df_relaxed_rel, tsv_filename=tsv_rel_filename)
            combining(df=df_mag, df_relaxed=df_relaxed_mag, tsv_filename=tsv_mag_filename)

            # plotting(df=df, df_relaxed=df_relaxed, dzs=dzs, spins=spins, 
            #          ylabel='Formation energy (eV)', png_filename=png_filename)
            # plotting(df=df_rel, df_relaxed=df_relaxed_rel, dzs=dzs, spins=spins, color='black', 
            #          ylabel='Spin crossover energy (eV)', png_filename=png_rel_filename)
            # plotting(df=df_mag, df_relaxed=df_relaxed_mag, dzs=dzs, spins=spins, 
            #          ylabel='Magnetic Moments', png_filename=png_mag_filename)

def combining(df, df_relaxed, tsv_filename):
    combined_df = pd.concat([df, df_relaxed])
    combined_df.to_csv(tsv_filename, sep='\t', float_format='%.2f')
    print(f"Data saved to {tsv_filename}")

def plot_smooth_line(x, y, color, label):
    x_new = np.linspace(min(x), max(x), 300)
    spl = make_interp_spline(x, y, k=3)  # Smoothing spline
    y_smooth = spl(x_new)
    plt.plot(x_new, y_smooth, color=color, label=label)
    plt.scatter(x, y, color=color)  # Add markers without label

def plotting(df, df_relaxed, dzs, spins, ylabel, png_filename, color=None):
    plt.figure(figsize=(8, 6))
    for column in df.columns:
        filtered_df = df[column].dropna()
        if not filtered_df.empty:
            x = filtered_df.index
            y = filtered_df.values
            if color:
                plot_smooth_line(x, y, color, f'{column} (fixed)')
            else:
                plot_smooth_line(x, y, spins[column], f'{column} (fixed)')
    for column in df_relaxed.columns:
        filtered_df = df_relaxed[column].dropna()
        if not filtered_df.empty:
            x = filtered_df.index
            y = filtered_df.values
            if color:
                plt.scatter(x, y, marker='x', color=color, label=f'{column} (relaxed)')
            else:
                plt.scatter(x, y, marker='x', color=spins[column], label=f'{column} (relaxed)')
    plt.xticks(dzs)
    plt.xlabel('dz')
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.savefig(png_filename, bbox_inches="tight")
    print(f"Figure saved as {png_filename}")
    plt.close()

if __name__ == '__main__':
    main()