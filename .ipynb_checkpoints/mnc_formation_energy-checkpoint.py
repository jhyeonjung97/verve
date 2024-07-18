import matplotlib.pyplot as plt
from ase.io import read
from statistics import mean
import glob
import os
import pandas as pd

rows = {
    '3d': ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu'],
    '4d': ['Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag'],
    '5d': ['La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au']
}
spins = {'LS': '#ff7f0e', 'IS': '#279ff2', 'HS': '#9467bd'}
dzs = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]

for row_key, metals in rows.items():
    for metal in metals:
        df = pd.DataFrame(index=dzs, columns=spins.keys())
        df_relaxed = pd.DataFrame(index=dzs, columns=spins.keys())
        tsv_filename = f'{row_key}_{metal}.tsv'
        png_filename = f'{row_key}_{metal}.png'
        
        for spin in spins.keys():
            path_pattern = f'/scratch/x2755a09/3_MNC/{row_key}/*_{metal}/*_{spin}'
            matching_paths = glob.glob(path_pattern)
            
            for path in matching_paths:
                print(path)
                for i, dz in enumerate(dzs):
                    atoms_path = os.path.join(path, f'{i}_', 'restart.json')
                    if os.path.exists(atoms_path):
                        atoms = read(atoms_path)
                        energy = atoms.get_total_energy()
                        df.at[dz, spin] = energy
                    
                relaxed_path = os.path.join(path, 'relaxed_', 'restart.json')
                if os.path.exists(relaxed_path):
                    atoms = read(relaxed_path)
                    zN = mean([atom.z for atom in atoms if atom.symbol == 'N'])
                    zM = mean([atom.z for atom in atoms if atom.symbol not in ['N', 'C', 'O', 'H']])
                    dz = abs(zN - zM)
                    energy = atoms.get_total_energy()
                    df_relaxed.at[dz, spin] = energy
        
        plt.figure(figsize=(8, 6))
        
        for column in df.columns:
            filtered_df = df[column].dropna()
            if not filtered_df.empty:
                x = filtered_df.index
                y = filtered_df.values
                plt.plot(x, y, marker='o', color=spins[column], label=f'{column} (unrelaxed)')
            
        for column in df_relaxed.columns:
            filtered_df_relaxed = df_relaxed[column].dropna()
            if not filtered_df_relaxed.empty:
                x = filtered_df_relaxed.index
                y = filtered_df_relaxed.values
                plt.plot(x, y, marker='x', color=spins[column], label=f'{column} (relaxed)')
        
        plt.xticks(dzs)
        plt.xlabel('dz')
        plt.ylabel('Energy (eV)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(png_filename, bbox_inches="tight")
        print(f"Figure saved as {png_filename}")
        plt.close()

        combined_df = pd.concat([df, df_relaxed], keys=['unrelaxed', 'relaxed'])
        combined_df.to_csv(tsv_filename, sep='\t')
        print(f"Data saved to {tsv_filename}")
