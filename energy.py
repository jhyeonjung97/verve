import argparse
import os
import re
import matplotlib.pyplot as plt
import numpy as np

def extract_values(directory, patterns):
    """Extract the last values for the given patterns from OUTCAR files in the given directory."""
    pattern_map = {
        'PSCENC': r'PSCENC =\s+([0-9.-]+)',
        'TEWEN': r'TEWEN =\s+([0-9.-]+)',
        'DENC': r'DENC =\s+([0-9.-]+)',
        'EXHF': r'EXHF =\s+([0-9.-]+)',
        'XCENC': r'XCENC =\s+([0-9.-]+)',
        'EENTRO': r'EENTRO =\s+([0-9.-]+)',
        'EBANDS': r'EBANDS =\s+([0-9.-]+)',
        'EATOM': r'EATOM =\s+([0-9.-]+)',
        'Ediel_sol': r'Ediel_sol =\s+([0-9.-]+)',
        'PAW_double_counting': r'PAW double counting\s+=\s+([0-9.-]+)\s+([0-9.-]+)'
    }
    values = {key: [] for key in patterns}  # Initialize dict to store values for each pattern
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file == 'OUTCAR':
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                for key in patterns:
                    pattern = re.compile(pattern_map[key])
                    for line in reversed(lines):  # Search from the end of the file
                        match = pattern.search(line)
                        if match:
                            # For patterns with two values, store them as a tuple
                            if key == 'PAW_double_counting':
                                values[key].append((float(match.group(1)), float(match.group(2))))
                            else:
                                values[key].append(float(match.group(1)))
                            break
    return values

def plot_values(values_dict):
    """Plot the extracted last values for all selected patterns."""
    plt.figure(figsize=(14, 7))
    patterns = list(values_dict.keys())
    for i, key in enumerate(patterns, 1):
        plt.subplot(1, len(patterns), i)
        values = values_dict[key]
        if isinstance(values[0], tuple):  # Handle patterns with two values
            values1, values2 = zip(*values)
            plt.plot(values1, marker='o', linestyle='-', label=f'{key} 1')
            plt.plot(values2, marker='o', linestyle='-', label=f'{key} 2')
            plt.legend()
        else:
            plt.plot(values, marker='o', linestyle='-')
        plt.title(f'{key} Values Across OUTCAR Files')
        plt.xlabel('File Index')
        plt.ylabel(f'{key} Value')
        plt.grid(True)
    plt.tight_layout()
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
        plot_values(values_dict)
    else:
        print(f'No values found for the given patterns.')