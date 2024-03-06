import argparse
import os
import re
import matplotlib.pyplot as plt
import numpy as np
from aloha.cohp_analysis import *
from aloha.cohp_analysis import *

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir-range', type=str, default=None, help='Range of directories to investigate, e.g., "3,6"')
    parser.add_argument('-p', '--patterns', nargs='+', default=['TOTEN'], help='Patterns to search and plot')
    parser.add_argument('-a', '--all', action='store_true', default=False, help='Show all components')
    parser.add_argument('-r', '--ref', type=str, default=None, help='Adjust values by subtracting the minimum')
    parser.add_argument('-x', '--xlabel', default='Lattice parameter (Å)', type=str, help="x-axis title of the figure")
    parser.add_argument('--total', action='store_false', default=True, help='No show total energy')
    parser.add_argument('--save', action='store_false', default=True, help="save files")
    parser.add_argument('-s', '--seperate', action='store_true', default=False, help="save the plots seperately")
    parser.add_argument('-i', '--input', dest='outcar', type=str, default='OUTCAR', help='input filename')
    parser.add_argument('-o', '--output', dest='filename', type=str, default='energy.png', help="output filename")
    return parser

def main():
    args = get_parser().parse_args()
    if args.all:
        patterns = {'PSCENC', 'TEWEN', 'DENC', 'EXHF', 'XCENC', 'PAW_double_counting', 
                    'EENTRO', 'EBANDS', 'EATOM', 'TOTEN', 'Madelung', 'ICOHP'}
    else:
        patterns = set(args.patterns)
    if not args.total:
        patterns.discard('TOTEN')
        
    directory='./'
    values_dict, dir_names = extract_values(directory, patterns, dir_range=args.dir_range, outcar=args.outcar)
    if args.ref is not None:
        values_dict = adjust_values(values_dict, ref=args.ref)
    if any(values_dict.values()):
        plot_merged(values_dict, dir_names, xlabel=args.xlabel, save=args.save, filename=args.filename)
        if args.seperate:
            plot_separately(values_dict, dir_names, xlabel=args.xlabel, save=args.save, filename=args.filename)
    else:
        print('No values found for the given patterns.')

def extract_values(directory, patterns, dir_range, outcar):
    """Extract the last values for the given patterns from OUTCAR files in the given directories, sorted numerically."""
    pattern_map = {
        'PSCENC': r'alpha Z        PSCENC =\s+([0-9.-]+)',
        'TEWEN': r'Ewald energy   TEWEN  =\s+([0-9.-]+)',
        'DENC': r'-Hartree energ DENC   =\s+([0-9.-]+)',
        'EXHF': r'-exchange      EXHF   =\s+([0-9.-]+)',
        'XCENC': r'-V\(xc\)\+E\(xc\)   XCENC  =\s+([0-9.-]+)',
        'PAW_double_counting': r'PAW double counting   =\s+([0-9.-]+)\s+([0-9.-]+)',
        'EENTRO': r'entropy T\*S    EENTRO =\s+([0-9.-]+)',
        'EBANDS': r'eigenvalues    EBANDS =\s+([0-9.-]+)',
        'EATOM': r'atomic energy  EATOM  =\s+([0-9.-]+)',
        'Ediel_sol': r'Solvation  Ediel_sol  =\s+([0-9.-]+)',
        'TOTEN': r'free energy    TOTEN  =\s+([0-9.-]+)',
    }
    Madelung = 'Madelung' in patterns
    ICOHP = 'ICOHP' in patterns
    if Madelung:
        patterns.discard('Madelung')
    if ICOHP:
        patterns.discard('ICOHP')
    values = {key: [] for key in patterns}  # Initialize dict to store values for each pattern
    dir_names = []

    dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    if dir_range is not None:
        if ',' in dir_range:
            start_dir, end_dir = map(int, dir_range.split(','))
        else: 
            start_dir, end_dir = 1, int(dir_range)
        dir_nums = range(start_dir, end_dir + 1)
        dirs = [d for d in dirs if any(d.startswith(str(num)) for num in dir_nums)]
    dirs.sort(key=lambda x: [int(c) if c.isdigit() else c for c in re.split('(\d+)', x)])
        
    for dir_name in dirs:
        dir_path = os.path.join(directory, dir_name)
        trimmed_dir_name = dir_name[2:]  # Remove the first two characters
        dir_names.append(trimmed_dir_name)

        outcar_path = os.path.join(dir_path, outcar)
        if os.path.exists(outcar_path) and patterns:  # Check if OUTCAR file exists
            with open(outcar_path, 'r') as file:
                lines = file.readlines()
            for key in patterns:
                pattern = re.compile(pattern_map[key])
                for line in reversed(lines):  # Search from the end of the file
                    match = pattern.search(line)
                    if match:
                        if key == 'PAW_double_counting':
                            combined_value = sum(map(float, match.groups()))
                            values[key].append(combined_value)
                        else:
                            values[key].append(float(match.group(1)))
                        break
        if Madelung:
            madelung_path = os.path.join(dir_path, 'MadelungEnergies.lobster')
            if os.path.exists(madelung_path):
                with open(madelung_path, 'r') as file:
                    lines = file.readlines()
                for line in reversed(lines):
                    match = re.search(r'\s*\d+\.\d+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)', line)
                    if match:
                        values.setdefault('Mulliken', []).append(float(match.group(1)))
                        values.setdefault('Loewdin', []).append(float(match.group(2)))
                        break
        if ICOHP:
            ICOHP_path = os.path.join(dir_path, 'icohp.txt')
            if os.path.exists(ICOHP_path):
                with open(ICOHP_path, 'r') as file:
                    lines = file.readlines()
                for line in reversed(lines):
                    match = re.search(r'-ICOHP sum:(\s*)([0-9.]+)', line)
                    if match:
                        values.setdefault('ICOHP', []).append(-float(match.group(1)))
                        break

    return values, dir_names

def adjust_values(values_dict, ref):
    """Subtract the reference value from each pattern's data set."""
    adjusted_values_dict = {}
    for pattern, values in values_dict.items():
        if values:
            if ref == 'min':
                ref_value = min(values)
            elif ref == 'max':
                ref_value = max(values)
            elif ref == 'mid':
                ref_value = np.median(values)
            else:
                raise ValueError(f"Unknown reference type: {ref}")
            adjusted_values = [value - ref_value for value in values]
            adjusted_values_dict[pattern] = adjusted_values
        else:
            adjusted_values_dict[pattern] = values  # No adjustment needed
    return adjusted_values_dict

def plot_separately(values_dict, dir_names, xlabel, save, filename):
    """Plot each pattern on its own graph."""
    x = np.arange(len(dir_names))
    for i, (pattern, values) in enumerate(values_dict.items()):
        if not values:
            print(f"No values found for pattern: {pattern}")
            continue
        plt.figure(figsize=(10, 6))
        plt.plot(x, values, marker='o', linestyle='-', label=pattern)
        
        plt.title(f'{pattern} Energy Contribution')
        plt.xlabel(xlabel)
        plt.ylabel('Energy (eV)')
        plt.xticks(x, dir_names, rotation='vertical')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        
        if save:
            filename = filename.split(".")[0]
            plt.savefig(f"{filename}_{pattern}.png", bbox_inches="tight")
            print(f"Figure saved as {filename}_{pattern}.png")
        
        # plt.show()

def plot_merged(values_dict, dir_names, xlabel, save, filename):
    plt.figure(figsize=(10, 6))

    patterns_order = ['PSCENC', 'TEWEN', 'DENC', 'EXHF', 'XCENC', 'PAW_double_counting', 
                      'EENTRO', 'EBANDS', 'EATOM', 'TOTEN', 'Mulliken', 'Loewdin']
    filtered_patterns_order = [pattern for pattern in patterns_order if values_dict.get(pattern)]

    colors = plt.cm.turbo(np.linspace(0, 1, len(filtered_patterns_order))) 
    # viridis, magma, plasma, inferno, cividis, mako, rocket, turbo
    
    for pattern, color in zip(filtered_patterns_order, colors):
        values = values_dict.get(pattern, [])
        if all(isinstance(v, tuple) for v in values):
            values = [v[0] for v in values]
        if not values:
            print(f"No values found for pattern: {pattern}")
            continue
        plt.plot(values, marker='o', linestyle='-', label=pattern, color=color)
    
    plt.title('Energy Contribution')
    plt.xlabel(xlabel)
    plt.ylabel('Energy (eV)')
    plt.xticks(np.arange(len(dir_names)), dir_names, rotation='vertical')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    if save:
        plt.gcf().savefig(filename, bbox_inches="tight")
        print(f"Figure saved as {filename}")
        
    plt.show()

if __name__ == '__main__':
    main()

