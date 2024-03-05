import argparse
import os
import re
import matplotlib.pyplot as plt

def extract_values(directory, pattern_key):
    """Extract the last value for the given pattern key from OUTCAR files in the given directory."""
    pattern_map = {
        'PSCENC': r'alpha Z        PSCENC =\s+([0-9.]+)',
        'TEWEN': r'Ewald energy   TEWEN  =\s+([0-9.]+)',
        'DENC': r'-Hartree energ DENC   =\s+([0-9.]+)',
        'EXHF': r'-exchange      EXHF   =\s+([0-9.]+)',
        'XCENC': r'-V(xc)+E(xc)   XCENC  =\s+([0-9.]+)',
        'EENTRO': r'entropy T*S    EENTRO =\s+([0-9.]+)',
        'EBANDS': r'eigenvalues    EBANDS =\s+([0-9.]+)',
        'EATOM': r'atomic energy  EATOM  =\s+([0-9.]+)',
        'Ediel_sol': r'Solvation  Ediel_sol  =\s+([0-9.]+)'
    }
    pattern = re.compile(pattern_map[pattern_key])
    values = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file == 'OUTCAR':
                last_value = None
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        match = pattern.search(line)
                        if match:
                            last_value = float(match.group(1))
                if last_value is not None:
                    values.append(last_value)
    return values

def plot_values(values, pattern_key):
    """Plot the extracted last values for the selected pattern."""
    plt.figure(figsize=(10, 6))
    plt.plot(values, marker='o', linestyle='-', color='blue')
    plt.title(f'Last {pattern_key} Values Across OUTCAR Files')
    plt.xlabel('File Index')
    plt.ylabel(f'Last {pattern_key} Value')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--dir', action='store_true', help='Directory flag')
    parser.add_argument('-p', '--pattern', choices=['PSCENC', 'TEWEN', 'DENC', 'EXHF', 'XCENC', 'EENTRO', 'EBANDS', 'EATOM', 'Ediel_sol'], required=True, help='Pattern to search and plot')
    parser.add_argument('file', nargs='?', default='OUTCAR', help='File to process (default: OUTCAR)')
    args = parser.parse_args()

    directory = './' if args.dir else os.getcwd()  # Adjusted to use current directory if -r is not specified
    values = extract_values(directory, args.pattern)
    if values:
        plot_values(values, args.pattern)
    else:
        print(f'No {args.pattern} values found.')