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
        'PAW_double_counting': r'PAW double counting   =\s+([0-9.-]+)\s+([0-9.-]+)'
    }
    values = {key: [] for key in patterns}  # Initialize dict to store values for each pattern
    
    # Split dir_range into start and end, then generate the range of directories to process
    start_dir, end_dir = map(int, dir_range.split(','))
    dir_nums = range(start_dir, end_dir + 1)

    # List directories and filter based on the input range
    dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    dirs = [d for d in dirs if any(d.startswith(str(num)) for num in dir_nums)]
    dirs.sort(key=lambda x: [int(c) if c.isdigit() else c for c in re.split('(\d+)', x)])

    for dir_name in dirs:
        dir_path = os.path.join(directory, dir_name)
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
                            # Assuming single value patterns for simplicity; adjust if handling tuples
                            values[key].append(float(match.group(1)))
                            break
    return values

def plot_values_combined(values_dict):
    """Plot the extracted last values for all selected patterns on a single graph."""
    plt.figure(figsize=(10, 6))
    
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
    
    plt.title('Pattern Values Across OUTCAR Files')
    plt.xlabel('File Index')
    plt.ylabel('Value')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--dir', action='store_true', help='Directory flag')
    parser.add_argument('-p', '--patterns', nargs='+', required=True, help='Patterns to search and plot')
    parser.add_argument('file', nargs='?', default='OUTCAR', help='File to process (default: OUTCAR)')
    args = parser.parse_args()

    directory = './' if args.dir else os.getcwd()
    values_dict = extract_values(directory, args.patterns)
    if any(values_dict.values()):
        plot_values_combined(values_dict)
    else:
        print(f'No values found for the given patterns.')