import os
import re
import matplotlib.pyplot as plt

def extract_pscenc_values(directory):
    """Extract PSCENC values from OUTCAR files in the given directory."""
    pscenc_values = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file == 'OUTCAR':
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        if 'PSCENC' in line:
                            # Regex to extract the PSCENC value
                            match = re.search(r'PSCENC =\s+([0-9.]+)', line)
                            if match:
                                pscenc_values.append(float(match.group(1)))
    return pscenc_values

def plot_values(values):
    """Plot the extracted PSCENC values."""
    plt.figure(figsize=(10, 6))
    plt.plot(values, marker='o', linestyle='-')
    plt.title('PSCENC Values Across OUTCAR Files')
    plt.xlabel('File Index')
    plt.ylabel('PSCENC Value')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    directory = './'  # Starting directory
    pscenc_values = extract_pscenc_values(directory)
    if pscenc_values:
        plot_values(pscenc_values)
    else:
        print('No PSCENC values found.')