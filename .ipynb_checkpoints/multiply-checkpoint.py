import numpy as np
import pandas as pd

# Load the data from CSV files
X = pd.read_csv('energy_norm_formation.tsv', delimiter='\t', index_col=0)
Y = pd.read_csv('energy_norm_formation_octa.tsv', delimiter='\t', index_col=0)

# Perform element-wise division
Z = X - Y

# Ensure the index of Z matches the index of X
Z.index = X.index

# Save the result to a new TSV file
Z.to_csv('energy_norm_formation_rel.tsv', sep='\t', index=True)