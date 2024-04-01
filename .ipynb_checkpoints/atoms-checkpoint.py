import os
import glob
import argparse
import subprocess
from ase.io import read

# Setup argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--magnetic', action='store_true', default=False, help='Print magnetic moments')
parser.add_argument('-c', '--charge', action='store_true', default=False, help='Print Bader charges')
parser.add_argument('-e', '--energy', action='store_true', default=False, help='Print total energy')
args = parser.parse_args()

# Process directories
dirs = [d for d in os.listdir('.') if os.path.isdir(d) and '_' in d]
for dir in dirs:
    dir_path = os.path.join('.', dir)
    patterns = ['final*static*traj', 'final*opt*traj', '*json']
    matching_files = [file for pattern in patterns for file in glob.glob(os.path.join(dir_path, pattern))]
    
    atoms = None
    for traj_file in matching_files:
        if os.path.exists(traj_file):
            atoms = read(traj_file)
            break  # Remove break if you want to process all files
    
    if atoms:
        if args.magnetic:
            print(dir, atoms.get_magnetic_moments())
        if args.energy:
            print(dir, atoms.get_total_energy())
        if args.charge:
            chg_path = os.path.join(dir_path, 'atoms_bader_charge.json')
            if not os.path.exists(chg_path):
                subprocess.call('python ~/bin/verve/bader.py', shell=True, cwd=dir_path)
            if os.path.exists(chg_path):
                # Assuming `atoms_bader` is supposed to be loaded from `chg_path`
                # You need to implement loading logic for `atoms_bader` here
                print(dir, "Bader charges not implemented")