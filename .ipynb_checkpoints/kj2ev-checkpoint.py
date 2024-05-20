import numpy as np
import pandas as pd

# Read the data
X = pd.read_csv('energy_sub.tsv', delimiter='\t')
Y = pd.read_csv('energy_norm_formation.tsv', delimiter='\t', header=None, index_col=0)


print(X)

print(Y)

# Set the index of X to match the index of Y
X.index = Y.index

# Save the modified X to a new file
X.to_csv('energy_sub_eV.tsv', sep='\t', index=True)
