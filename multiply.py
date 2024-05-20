import numpy as np
import pandas as pd

# Read the data
X = pd.read_csv('merged_ICOHP.tsv', delimiter='\t', index_col=0)
Y = pd.read_csv('merged_ICOBI.tsv', delimiter='\t', index_col=0)

# Perform element-wise multiplication
Z = X * Y

# Set the index of Z to match the index of X (this is already done by default)
Z.index = X.index

# Save the result to a new file
Z.to_csv('merged_weighted_ICOHP.tsv', sep='\t', index=True)