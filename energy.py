import os
import re
import matplotlib.pyplot as plt

def extract_pscenc_values(directory):
    """Extract the last PSCENC value from OUTCAR files in the given directory."""
    pscenc_values = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file == 'OUTCAR':
                last_value = None  # Initialize to None for each OUTCAR file
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        if 'PSCENC' in line:
                            # Regex to extract the PSCENC value
                            match = re.search(r'PSCENC =\s+([0-9.]+)', line)
                            if match:
                                last_value = float(match.group(1))  # Update last_value on each match
                if last_value is not None:  # Ensure at least one match was found
                    pscenc_values.append(last_value)
    return pscenc_values

def plot_values(values):
    """Plot the extracted last PSCENC values."""
    plt.figure(figsize=(10, 6))
    plt.plot(values, marker='o', linestyle='-', color='blue')
    plt.title('Last PSCENC Values Across OUTCAR Files')
    plt.xlabel('File Index')
    plt.ylabel('Last PSCENC Value')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    directory = './'  # Starting directory
    pscenc_values = extract_pscenc_values(directory)
    if pscenc_values:
        plot_values(pscenc_values)
    else:
        print('No PSCENC values found.')
