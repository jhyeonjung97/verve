import argparse
import os
import re
import matplotlib.pyplot as plt
import numpy as np

def extract_values(directory, patterns, dir_range):
    """Extract the last values for the given patterns from OUTCAR files in the given directories, sorted numerically."""
    pattern_map = {
        'PSCENC': r'alpha Z        PSCENC =\s+([0-9.-]+)',
        'TEWEN': r'Ewald energy   TEWEN  =\s+([0-9.-]+)',
        'DENC': r'-Hartree energ DENC   =\s+([0-9.-]+)',
        'EXHF': r'-exchange      EXHF   =\s+([0-9.-]+)',
        'XCENC': r'-V(xc)+E(xc)   XCENC  =\s+([0-9.-]+)',
        'EENTRO': r'entropy T*S    EENTRO =\s+([0-9.-]+)',
        'EBANDS': r'eigenvalues    EBANDS =\s+([0-9.-]+)',
        'EATOM': r'EATOM =\s+([0-9.-]+)',
        'Ediel_sol': r'atomic energy  EATOM  =\s+([0-9.-]+)',
        'PAW_double_counting': r'PAW double counting   =\s+([0-9.-]+)\s+([0-9.-]+)',
        'TOTEN': r'free energy    TOTEN  =\s+([0-9.-]+)\s+([0-9.-]+)'
    }
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
        for file_name in os.listdir(dir_path):
            if file_name == 'OUTCAR':
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                for key in patterns:
                    pattern = re.compile(pattern_map[key])
                    for line in reversed(lines):  # Search from the end of the file
                        match = pattern.search(line)
                        if match:
                            if key == 'PAW_double_counting':
                                # Add the two values together
                                combined_value = sum(map(float, match.groups()))
                                values[key].append(combined_value)
                            else:
                                # For all other patterns, assuming single value patterns for simplicity
                                values[key].append(float(match.group(1)))
                            break
    return values, dir_names

def plot_values(values_dict, dir_names, xlabel, save, filename):
    """Plot the extracted last values for all selected patterns on a single graph."""
    plt.figure(figsize=(10, 6))

    num_dirs = len(dir_names)
    x = np.arange(num_dirs) # Generate x locations for each directory
    
    # Generating a color map for different patterns
    colors = plt.cm.viridis(np.linspace(0, 1, len(values_dict)))
    
    for (pattern, values), color in zip(values_dict.items(), colors):
        # Check if we're dealing with single values or tuples (for patterns like PAW_double_counting)
        if all(isinstance(v, tuple) for v in values):
            # If tuples, assuming we want to plot the first value
            values = [v[0] for v in values]
        
        if not values:  # Skip patterns with no values found
            print(f"No values found for pattern: {pattern}")
            continue
        
        plt.plot(values, marker='o', linestyle='-', label=pattern, color=color)
    
    plt.title('Energy Contribution')
    plt.xlabel(xlabel)
    plt.ylabel('Energy (eV)')
    plt.xticks(x, dir_names, rotation='vertical')  # Set directory names as x-axis labels
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    if save:
        plt.gcf().savefig(filename, bbox_inches="tight")
        print(f"Figure saved as {filename}")
        
    plt.show()
            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir-range', type=str, default=None, help='Range of directories to investigate, e.g., "3,6"')
    parser.add_argument('-p', '--patterns', nargs='+', default='TOTEN', help='Patterns to search and plot')
    parser.add_argument('-a', '--all', action='store_true', default=False, help='Show all components')
    parser.add_argument('--total', action='store_true', default=False, help='Show total energy')
    parser.add_argument('--xlabel', default='Lattice parameter (Å)', type=str, help="x-axis title of the figure")
    parser.add_argument('-s', '--save', default=True, action='store_true', help="save files")
    parser.add_argument('-o', '--filename', default='energy.png', type=str, help="output filename")
    args = parser.parse_args()

    if args.all:
        patterns = {'PSCENC', 'TEWEN', 'DENC', 'EXHF', 'XCENC', 'EENTRO', 'EBANDS', 'EATOM', 'PAW_double_counting', 'TOTEN'}
    else:
        patterns = set(args.patterns)

    if args.total and 'TOTEN' not in patterns:
        patterns.append('TOTEN')

    directory = './'  # Adjust based on your directory structure
    values_dict, dir_names = extract_values(directory, patterns, args.dir_range)
    # dir_names = [name[2:] for name in dir_names]  # Slice names here if not already done

    if any(values_dict.values()):
        plot_values(values_dict, dir_names, xlabel=args.xlabel, save=args.save, filename=args.filename)
    else:
        print('No values found for the given patterns.')

if __name__ == '__main__':
    main()
