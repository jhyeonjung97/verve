import os
import glob
import argparse
import subprocess
from ase.io import read

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--magnetic', action='store_true', default=False, help='Print magnetic moments')
parser.add_argument('-c', '--charge', action='store_true', default=False, help='Print Bader charges')
parser.add_argument('-e', '--energy', action='store_true', default=False, help='Print total energy')
args = parser.parse_args()

class Colors:
    CYAN = '\033[34m'
    GREEN = '\033[38;5;22m'
    ORANGE = '\033[38;5;208m'
    MAGENTA = '\033[35m'
    RED = '\033[91m'
    RESET = '\033[0m'

dirs = [d for d in os.listdir('.') if os.path.isdir(d) and '_' in d]
for dir in dirs:
    dir_path = os.path.join('.', dir)
    patterns = ['final*static*traj', 'final*opt*traj', '*json']
    matching_files = [file for pattern in patterns for file in glob.glob(os.path.join(dir_path, pattern))]
    
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
        if args.charge:
            chg_path = os.path.join(dir_path, 'atoms_bader_charge.json')
            if not os.path.exists(chg_path):
                subprocess.call('python ~/bin/verve/bader.py', shell=True, cwd=dir_path)
            if os.path.exists(chg_path):
                print(f"{Colors.GREEN}{dir}{Colors.RESET}", "Bader charges not implemented")