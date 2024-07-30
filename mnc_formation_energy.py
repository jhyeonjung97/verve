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

# Reference energies and corrections
E_H2O = -14.23919983
E_H2 = -6.77409008
ZPE_H2O = 0.558
ZPE_H2 = 0.273
Cp_H2O = 0.10
Cp_H2 = 0.09
Ref_H2 = E_H2 + ZPE_H2 + Cp_H2
Ref_H2O = E_H2O + ZPE_H2O + Cp_H2O
Ref_O = Ref_H2O - Ref_H2 + 2.506

# DFT energies and corrections
nitrogen_E = -16.64503942  # eV
nitrogen_TS = 0.635139     # eV
nitrogen_ZPE = 0.096279    # eV
nitrogen = (nitrogen_E - nitrogen_TS + nitrogen_ZPE) / 2
carbon = -9.357363435      # eV

metal_path = '/scratch/x2755a09/3_MNC/gas/metals.tsv'
metal_df = pd.read_csv(metal_path, delimiter='\t', index_col=0)

def main():
    for row_key, metals in rows.items():
        for metal in metals:
            process_metal(row_key, metal)

def process_metal(row_key, metal):
    # Initialize DataFrames for each state
    df, df_rel, df_mag = [pd.DataFrame() for _ in range(3)]
    df_relaxed, df_relaxed_rel, df_relaxed_mag = [pd.DataFrame() for _ in range(3)]
    df_O, df_O_rel, df_O_mag = [pd.DataFrame() for _ in range(3)]
    df_O_relaxed, df_O_relaxed_rel, df_O_relaxed_mag = [pd.DataFrame() for _ in range(3)]
    df_OH, df_OH_rel, df_OH_mag = [pd.DataFrame() for _ in range(3)]
    df_OH_relaxed, df_OH_relaxed_rel, df_OH_relaxed_mag = [pd.DataFrame() for _ in range(3)]

    filenames = generate_filenames(row_key, metal)

    for spin in spins.keys():
        matching_paths = glob.glob(f'/scratch/x2755a09/3_MNC/{row_key}/*_{metal}/*_{spin}')
        for path in matching_paths:
            process_path(path, dzs, spin, metal_df.at[metal, 'energy'],
                         df, df_rel, df_mag, df_relaxed, df_relaxed_rel, df_relaxed_mag,
                         df_O, df_O_rel, df_O_mag, df_O_relaxed, df_O_relaxed_rel, df_O_relaxed_mag,
                         df_OH, df_OH_rel, df_OH_mag, df_OH_relaxed, df_OH_relaxed_rel, df_OH_relaxed_mag)
    
    # Calculate relative values
    calculate_relative(df, df_rel)
    calculate_relative(df_O, df_O_rel)
    calculate_relative(df_OH, df_OH_rel)
    calculate_relative(df_relaxed, df_relaxed_rel)
    calculate_relative(df_O_relaxed, df_O_relaxed_rel)
    calculate_relative(df_OH_relaxed, df_OH_relaxed_rel)

    # Combine and save data
    combine_and_save(df, df_relaxed, filenames['tsv_filename'])
    combine_and_save(df_rel, df_relaxed_rel, filenames['tsv_rel_filename'])
    combine_and_save(df_mag, df_relaxed_mag, filenames['tsv_mag_filename'])
    combine_and_save(df_O, df_O_relaxed, filenames['tsv_O_filename'])
    combine_and_save(df_O_rel, df_O_relaxed_rel, filenames['tsv_O_rel_filename'])
    combine_and_save(df_O_mag, df_O_relaxed_mag, filenames['tsv_O_mag_filename'])
    combine_and_save(df_OH, df_OH_relaxed, filenames['tsv_OH_filename'])
    combine_and_save(df_OH_rel, df_OH_relaxed_rel, filenames['tsv_OH_rel_filename'])
    combine_and_save(df_OH_mag, df_OH_relaxed_mag, filenames['tsv_OH_mag_filename'])

    # Plot and save figures
    plot_and_save(df, df_relaxed, dzs, spins, 'Formation energy (eV)', filenames['png_filename'])
    plot_and_save(df_rel, df_relaxed_rel, dzs, spins, 'Spin crossover energy (eV)', filenames['png_rel_filename'], color='black')
    plot_and_save(df_mag, df_relaxed_mag, dzs, spins, 'Magnetic Moments', filenames['png_mag_filename'], ymin=-0.5, ymax=5.5, yticks=np.arange(6))
    plot_and_save(df_O, df_O_relaxed, dzs, spins, 'Formation energy (eV)', filenames['png_O_filename'])
    plot_and_save(df_O_rel, df_O_relaxed_rel, dzs, spins, 'Spin crossover energy (eV)', filenames['png_O_rel_filename'], color='black')
    plot_and_save(df_O_mag, df_O_relaxed_mag, dzs, spins, 'Magnetic Moments', filenames['png_O_mag_filename'], ymin=-0.5, ymax=5.5, yticks=np.arange(6))
    plot_and_save(df_OH, df_OH_relaxed, dzs, spins, 'Formation energy (eV)', filenames['png_OH_filename'])
    plot_and_save(df_OH_rel, df_OH_relaxed_rel, dzs, spins, 'Spin crossover energy (eV)', filenames['png_OH_rel_filename'], color='black')
    plot_and_save(df_OH_mag, df_OH_relaxed_mag, dzs, spins, 'Magnetic Moments', filenames['png_OH_mag_filename'], ymin=-0.5, ymax=5.5, yticks=np.arange(6))

def generate_filenames(row_key, metal):
    return {
        'tsv_filename': f'{row_key}_{metal}_Ef.tsv',
        'png_filename': f'{row_key}_{metal}_Ef.png',
        'tsv_rel_filename': f'{row_key}_{metal}_rel.tsv',
        'png_rel_filename': f'{row_key}_{metal}_rel.png',
        'tsv_mag_filename': f'{row_key}_{metal}_mag.tsv',
        'png_mag_filename': f'{row_key}_{metal}_mag.png',
        'tsv_O_filename': f'{row_key}_{metal}_Oads.tsv',
        'png_O_filename': f'{row_key}_{metal}_Oads.png',
        'tsv_O_rel_filename': f'{row_key}_{metal}_rel_O.tsv',
        'png_O_rel_filename': f'{row_key}_{metal}_rel_O.png',
        'tsv_O_mag_filename': f'{row_key}_{metal}_mag_O.tsv',
        'png_O_mag_filename': f'{row_key}_{metal}_mag_O.png',
        'tsv_OH_filename': f'{row_key}_{metal}_OHads.tsv',
        'png_OH_filename': f'{row_key}_{metal}_OHads.png',
        'tsv_OH_rel_filename': f'{row_key}_{metal}_rel_OH.tsv',
        'png_OH_rel_filename': f'{row_key}_{metal}_rel_OH.png',
        'tsv_OH_mag_filename': f'{row_key}_{metal}_mag_OH.tsv',
        'png_OH_mag_filename': f'{row_key}_{metal}_mag_OH.png',
    }

def process_path(path, dzs, spin, metal_energy, *dfs):
    for i, dz in enumerate(dzs):
        atoms_path = os.path.join(path, f'{i}_', 'moments.json')
        atoms_O_path = os.path.join(atoms_path, '1_O', 'moments.json')
        atoms_OH_path = os.path.join(atoms_path, '2_OH', 'moments.json')

        process_atoms(atoms_path, dz, spin, metal_energy, dfs[0], dfs[1], dfs[2])
        process_atoms(atoms_O_path, dz, spin, metal_energy, dfs[3], dfs[4], dfs[5], ref_energy=Ref_O)
        process_atoms(atoms_OH_path, dz, spin, metal_energy, dfs[6], dfs[7], dfs[8], ref_energy=Ref_OH)

    relaxed_path = os.path.join(path, 'relaxed_', 'moments.json')
    relaxed_O_path = os.path.join(relaxed_path, '1_O', 'moments.json')
    relaxed_OH_path = os.path.join(relaxed_path, '2_OH', 'moments.json')

    process_atoms(relaxed_path, None, spin, metal_energy, dfs[0], dfs[1], dfs[2], relaxed=True)
    process_atoms(relaxed_O_path, None, spin, metal_energy, dfs[3], dfs[4], dfs[5], ref_energy=Ref_O, relaxed=True)
    process_atoms(relaxed_OH_path, None, spin, metal_energy, dfs[6], dfs[7], dfs[8], ref_energy=Ref_OH, relaxed=True)

def process_atoms(path, dz, spin, metal_energy, df, df_rel, df_mag, relaxed=False, ref_energy=None):
    if not os.path.exists(path):
        if dz is not None:
            df.at[dz, spin] = np.nan
            df_mag.at[dz, spin] = np.nan
        return

    atoms = read(path)
    energy = atoms.get_total_energy()
    formation_energy = energy - metal_energy - 26 * carbon - 4 * nitrogen
    adsorption_energy = None if ref_energy is None else energy - ref_energy

    if relaxed:
        zN = mean([atom.z for atom in atoms if atom.symbol == 'N'])
        zM = mean([atom.z for atom in atoms if atom.symbol not in ['N', 'C', 'O', 'H']])
        dz_relaxed = abs(zN - zM)
        df.at[dz_relaxed, spin] = adsorption_energy if ref_energy else formation_energy
    else:
        df.at[dz, spin] = adsorption_energy if ref_energy else formation_energy

    try:
        magmoms = atoms.get_magnetic_moments()
        for atom in atoms:
            if atom.symbol not in ['N', 'C', 'O', 'H']:
                df_mag.at[dz if not relaxed else dz_relaxed, spin] = magmoms[atom.index]
    except Exception:
        df_mag.at[dz if not relaxed else dz_relaxed, spin] = 0

def calculate_relative(df, df_rel):
    df_rel['HS-LS'] = df['HS'] - df['LS']

def combine_and_save(df, df_relaxed, tsv_filename):
    combined_df = pd.concat([df, df_relaxed])
    combined_df.to_csv(tsv_filename, sep='\t', float_format='%.2f')
    print(f"Data saved to {tsv_filename}")

def plot_smooth_line(x, y, color, label):
    x_new = np.linspace(min(x), max(x), 300)
    spl = make_interp_spline(x, y, k=3)  # Smoothing spline
    y_smooth = spl(x_new)
    plt.plot(x_new, y_smooth, color=color, label=label)
    plt.scatter(x, y, color=color)  # Add markers without label

def plot_and_save(df, df_relaxed, dzs, spins, ylabel, png_filename, ymin=None, ymax=None, yticks=None, color=None):
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
            plt.scatter(x, y, marker='x', color=color if color else spins[column], label=f'{column} (relaxed)')

    plt.xticks(dzs)
    plt.xlabel('dz')
    plt.ylabel(ylabel)
    if ymin and ymax:
        plt.ylim(ymin, ymax)
    if yticks is not None:
        plt.yticks(yticks)
    plt.legend()
    plt.tight_layout()
    plt.savefig(png_filename, bbox_inches="tight")
    print(f"Figure saved as {png_filename}")
    plt.close()

if __name__ == '__main__':
    main()
