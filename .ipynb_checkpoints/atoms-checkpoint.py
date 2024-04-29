import os
import glob
import argparse
import subprocess
from ase.io import read

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--magnetic', action='store_true', default=False, help='Print magnetic moments')
parser.add_argument('-c', '--charge', action='store_true', default=False, help='Print Bader charges')
parser.add_argument('-e', '--energy', action='store_true', default=False, help='Print total energy')
parser.add_argument('-a', '--atoms', action='store_true', default=False, help='Print chemical formula')
parser.add_argument('-f', '--force', action='store_true', default=False, help='Force to select all directories')
args = parser.parse_args()

class Colors:
    CYAN = '\033[34m'
    GREEN = '\033[38;5;22m'
    ORANGE = '\033[38;5;208m'
    MAGENTA = '\033[35m'
    RED = '\033[91m'
    RESET = '\033[0m'

if args.force:
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
else:
    dirs = [d for d in os.listdir('.') if os.path.isdir(d) and '_' in d]
    
sorted_dirs = sorted(dirs)
for dir in sorted_dirs:
    dir_path = os.path.join('.', dir)

    pattern = os.path.join(dir_path, 'OUTCAR')
    pattern_A = os.path.join(dir_path, 'final*mnc*traj')
    pattern_B = os.path.join(dir_path, 'final*static*traj')
    pattern_C = os.path.join(dir_path, 'final*opt*traj')
    pattern_D = os.path.join(dir_path, '*json')

    matching_files = []
    for pattern in [pattern_A, pattern_B, pattern_C, pattern_D]:
        matching_files.extend(glob.glob(pattern))
        if matching_files:
            break
    
    atoms = None
    for traj_file in matching_files:
        if os.path.exists(traj_file):
            atoms = read(traj_file)
            break
    
    if atoms:
        if args.magnetic:
            print(f"{Colors.CYAN}{dir}{Colors.RESET}", atoms.get_magnetic_moments())
        if args.energy:
            print(f"{Colors.ORANGE}{dir}{Colors.RESET}", atoms.get_total_energy())
        if args.atoms:
            print(f"{Colors.MAGENTA}{dir}{Colors.RESET}", atoms.get_chemical_formula())
        if args.charge:
            chg_path = os.path.join(dir_path, 'atoms_bader_charge.json')
            if not os.path.exists(chg_path):
                subprocess.call('python ~/bin/verve/bader.py', shell=True, cwd=dir_path)
            if os.path.exists(chg_path):
                print(f"{Colors.GREEN}{dir}{Colors.RESET}", "Bader charges not implemented")