parser = argparse.ArgumentParser()
parser.add_argument('-m', action='store_true', default=False)
parser.add_argument('-c', action='store_true', default=False)
parser.add_argument('-e', action='store_true', default=False)
args = parser.parse_args()
    
dirs = [d for d in os.listdir('./') if os.path.isdir(os.path.join('./', d)) and '_' in d]
for dir in dirs:
    dir_path = os.path.join('./', dir)
    pattern_A = os.path.join(dir_path, 'final*static*traj')
    pattern_B = os.path.join(dir_path, 'final*opt*traj')
    pattern_C = os.path.join(dir_path, '*json')
    matching_files_A = glob.glob(pattern_A)
    matching_files_B = glob.glob(pattern_B)
    matching_files_C = glob.glob(pattern_C)
    matching_files = matching_files_A + matching_files_B + matching_files_C
    for traj_file in matching_files:
        if os.path.exists(traj_file):
            atoms = read(traj_file)
            break
    if m:
        print(dir, atoms.get_magnetic_moments())
    if e:
        print(dir, atoms.get_total_energy())
    if c:
        chg_path = os.path.join(dir_path, 'atoms_bader_charge.json')
        if not os.path.exists(Bader_path):
            subprocess.call('python ~/bin/verve/bader.py', shell=True, cwd=dir_path)
        if os.path.exists(chg_path):
            print(dir, atoms_bader.get_initial_charges())