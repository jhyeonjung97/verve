from mendeleev import element
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='~~')
parser.add_argument('-p', '--patterns', required=True, nargs='+', default=['en_pauling'], help='~~')

# Define the d-block elements for 3d, 4d, and 5d series
elements_3d = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As']
elements_4d = ['Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb']
elements_5d = ['La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi']

# Function to get electronegativity
def get_data(element_symbol, atomic_property):
    try:
        return element(element_symbol).atomic_property
    except:
        return None

for pattern in args.patterns:
    # Create the DataFrame
    data = {
        '3d': [get_data(e, p) for e in elements_3d] * 5,
        '4d': [get_data(e, p) for e in elements_4d] * 5,
        '5d': [get_data(e, p) for e in elements_5d] * 5
    }

    # Since we need exactly 65 rows, let's slice the data
    df = pd.DataFrame(data).iloc[:65]

    # Save the DataFrame as a TSV file
    df.to_csv(f'concat_{p}.tsv', sep='\t', index=False)

    print(f"DataFrame saved as concat_{p}.tsv")

