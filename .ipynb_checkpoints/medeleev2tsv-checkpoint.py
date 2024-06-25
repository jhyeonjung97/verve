from mendeleev import element
import pandas as pd
import argparse

# Define the argument parser
parser = argparse.ArgumentParser(description='Generate TSV files with specified atomic properties.')
parser.add_argument('-p', '--patterns', required=True, nargs='+', default=['en_pauling'], help='List of atomic properties to retrieve.')

# Parse the arguments
args = parser.parse_args()

# Define the d-block elements for 3d, 4d, and 5d series
elements_3d = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As']
elements_4d = ['Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb']
elements_5d = ['La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi']

# Function to get the specified atomic property
def get_data(element_symbol, atomic_property):
    try:
        return getattr(element(element_symbol), atomic_property)
    except AttributeError:
        return None

# Process each specified pattern
for pattern in args.patterns:
    # Create the DataFrame
    data = {
        '3d': [get_data(e, pattern) for e in elements_3d] * 5,
        '4d': [get_data(e, pattern) for e in elements_4d] * 5,
        '5d': [get_data(e, pattern) for e in elements_5d] * 5
    }

    # Since we need exactly 65 rows, let's slice the data
    df = pd.DataFrame(data).iloc[:65]

    # Save the DataFrame as a TSV file
    df.to_csv(f'concat_{pattern}.tsv', sep='\t', index=False)

    print(f"DataFrame saved as concat_{pattern}.tsv")
