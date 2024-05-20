import numpy as np
import pandas as pd

X = pd.read_csv('energy_sub.tsv', delimiter='\t')
Y = pd.read_csv('energy_sub.tsv', delimiter='\t').iloc[:, :1]
print(Y)
# df = df / 96.48
X.to_csv('energy_sub_eV.tsv', sep='\t', index=False)