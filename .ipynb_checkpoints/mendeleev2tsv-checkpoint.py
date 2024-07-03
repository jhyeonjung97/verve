from mendeleev import element
import pandas as pd
import argparse

# Define the argument parser
parser = argparse.ArgumentParser(description='Generate TSV files with specified atomic properties.')
parser.add_argument('-p', '--patterns', required=True, nargs='+', help='List of atomic properties to retrieve.')
parser.add_argument('-n', '--number', default=6, type=int, help='Number of repeat')

# Parse the arguments
args = parser.parse_args()
n = args.number
m = n*13

# Define the d-block elements for 3d, 4d, and 5d series
elements_3d = ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge']
elements_4d = ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn']
elements_5d = ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']

# Function to get the specified atomic property
def get_data(element_symbol, atomic_property):
    try:
        elem = element(element_symbol)
        if 'ionenergies' in atomic_property:
            # Handle ionenergies property
            ion_index = int(atomic_property.split('[')[1].strip(']'))
            return elem.ionenergies[ion_index]
        else:
            return getattr(elem, atomic_property)
    except AttributeError:
        return None
    except (KeyError, IndexError):
        return None
    
# Generate the repeating index pattern
index_pattern = list(range(13)) * n
index_pattern = index_pattern[:m]

# Process each specified pattern
for pattern in args.patterns:
    # Handle file naming for ionenergies
    if 'ionenergies' in pattern:
        ion_index = int(pattern.split('[')[1].strip(']'))
        filname = f'ionenergies_{ion_index}'
    else:
        filname = pattern
    
    # Create the DataFrame
    data = {
        '3d': [get_data(e, pattern) for e in elements_3d] * n,
        '4d': [get_data(e, pattern) for e in elements_4d] * n,
        '5d': [get_data(e, pattern) for e in elements_5d] * n
    }

    # Since we need exactly m rows, let's slice the data
    df = pd.DataFrame(data).iloc[:m]
    
    if pattern == 'boiling_point' or pattern == 'melting_point':
        for i in range(n):
            df[i][2]=df[i][2]['gray']
        
    # Set the index
    df.index = index_pattern

    # Save the DataFrame as a TSV file
    df.to_csv(f'concat_{filname}.tsv', sep='\t', index=True)

    print(f"DataFrame saved as concat_{filname}.tsv")
