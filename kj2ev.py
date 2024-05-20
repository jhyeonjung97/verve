import numpy as np
import pandas as pd

df = pd.read_csv('energy_sub.tsv', delimiter='\t').iloc[:, 1:]
df = df / 96.48
df.to_csv('energy_sub_eV.tsv', sep='\t', index=False)