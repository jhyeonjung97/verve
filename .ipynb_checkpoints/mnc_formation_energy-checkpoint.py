import matplotlib.pyplot as plt
from ase.io import read
from statistics import mean
import glob
import os
import pandas as pd

# Define the rows and spins
rows = {
    '3d': ['Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu'],
    '4d': ['Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd'],
    '5d': ['Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt']
}
spins = {'LS': '#ff7f0e', 'IS': '#279ff2', 'HS': '#9467bd'}
dzs = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]

for row_key, metals in rows.items():
    for metal in metals:
        df = pd.DataFrame()
        df_rel = pd.DataFrame()
        df_mag = pd.DataFrame()
        df_relaxed = pd.DataFrame()
        df_relaxed_rel = pd.DataFrame()
        df_relaxed_mag = pd.DataFrame()

        tsv_filename = f'{row_key}_{metal}.tsv'
        png_filename = f'{row_key}_{metal}.png'
        tsv_rel_filename = f'{row_key}_{metal}_rel.tsv'
        png_rel_filename = f'{row_key}_{metal}_rel.png'
        tsv_mag_filename = f'{row_key}_{metal}_mag.tsv'
        png_mag_filename = f'{row_key}_{metal}_mag.png'

        for spin in spins.keys():
            path_pattern = f'/scratch/x2755a09/3_MNC/{row_key}/*_{metal}/*_{spin}'
            matching_paths = glob.glob(path_pattern)

            for path in matching_paths:
                print(path)
                for i, dz in enumerate(dzs):
                    atoms_path = os.path.join(path, f'{i}_', 'moments.json')
                    if os.path.exists(atoms_path):
                        atoms = read(atoms_path)
                        energy = atoms.get_total_energy()
                        df.at[dz, spin] = energy

                        magnetic_moments = atoms.get_magnetic_moments()
                        if magnetic_moments:
                            for atom in atoms:
                                if atom.symbol not in ['N', 'C', 'O', 'H']:
                                    df_mag.at[dz, spin] = abs(magnetic_moments[atom.index])
                        else:
                            df_mag.at[dz, spin] = 0

                relaxed_path = os.path.join(path, 'relaxed_', 'moments.json')
                if os.path.exists(relaxed_path):
                    atoms = read(relaxed_path)
                    zN = mean([atom.z for atom in atoms if atom.symbol == 'N'])
                    zM = mean([atom.z for atom in atoms if atom.symbol not in ['N', 'C', 'O', 'H']])
                    dz_relaxed = abs(zN - zM)
                    energy = atoms.get_total_energy()
                    df_relaxed.at[dz_relaxed, spin] = energy
                    magnetic_moments = atoms.get_magnetic_moments()
                    if magnetic_moments:
                        for atom in atoms:
                            if atom.symbol not in ['N', 'C', 'O', 'H']:
                                df_relaxed_mag.at[dz, spin] = abs(magnetic_moments[atom.index])
                    else:
                        df_relaxed_mag.at[dz, spin] = 0

        df_rel['HS-LS'] = df['HS'] - df['LS']
        df_relaxed_rel['HS-LS'] = df_relaxed['HS'] - df_relaxed['LS']

        combined_df = pd.concat([df, df_relaxed])
        combined_df.to_csv(tsv_filename, sep='\t', float_format='%.2f')
        print(f"Data saved to {tsv_filename}")

        combined_df_rel = pd.concat([df_rel, df_relaxed_rel])
        combined_df_rel.to_csv(tsv_rel_filename, sep='\t', float_format='%.2f')
        print(f"Data saved to {tsv_rel_filename}")

        combined_df_mag = pd.concat([df_mag, df_relaxed_mag])
        combined_df_mag.to_csv(tsv_mag_filename, sep='\t', float_format='%.2f')
        print(f"Data saved to {tsv_mag_filename}")

        # Formation energy
        plt.figure(figsize=(8, 6))

        for column in df.columns:
            filtered_df = df[column].dropna()
            if not filtered_df.empty:
                x = filtered_df.index
                y = filtered_df.values
                plt.plot(x, y, marker='o', color=spins[column], label=f'{column} (fixed)')

        for column in df_relaxed.columns:
            filtered_df_relaxed = df_relaxed[column].dropna()
            if not filtered_df_relaxed.empty:
                x = filtered_df_relaxed.index
                y = filtered_df_relaxed.values
                plt.plot(x, y, marker='x', color=spins[column], label=f'{column} (relaxed)')

        plt.xticks(dzs)
        plt.xlabel('dz')
        plt.ylabel('Formation energy (eV)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(png_filename, bbox_inches="tight")
        print(f"Figure saved as {png_filename}")
        plt.close()

        # HS vs. LS
        plt.figure(figsize=(8, 6))

        filtered_df = df_rel['HS-LS'].dropna()
        if not filtered_df.empty:
            x = filtered_df.index
            y = filtered_df.values
            plt.plot(x, y, marker='o', color='black', label='HS-LS (fixed)')

        filtered_df_relaxed = df_relaxed_rel['HS-LS'].dropna()
        if not filtered_df_relaxed.empty:
            x = filtered_df_relaxed.index
            y = filtered_df_relaxed.values
            plt.plot(x, y, marker='x', color='black', label='HS-LS (relaxed)')

        plt.xticks(dzs)
        plt.xlabel('dz')
        plt.ylabel('Formation energy (eV)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(png_rel_filename, bbox_inches="tight")
        print(f"Figure saved as {png_rel_filename}")
        plt.close()

        # Magnetic Moments
        plt.figure(figsize=(8, 6))

        for column in df_mag.columns:
            filtered_df = df_mag[column].dropna()
            if not filtered_df.empty:
                x = filtered_df.index
                y = filtered_df.values
                plt.plot(x, y, marker='o', color=spins[column], label=f'{column} (fixed)')

        for column in df_relaxed_mag.columns:
            filtered_df_relaxed_mag = df_relaxed_mag[column].dropna()
            if not filtered_df_relaxed_mag.empty:
                x = filtered_df_relaxed_mag.index
                y = filtered_df_relaxed_mag.values
                plt.plot(x, y, marker='x', color=spins[column], label=f'{column} (relaxed)')

        plt.xticks(dzs)
        plt.xlabel('dz')
        plt.ylabel('Magnetic Moments')
        plt.legend()
        plt.tight_layout()
        plt.savefig(png_mag_filename, bbox_inches="tight")
        print(f"Figure saved as {png_mag_filename}")
        plt.close()