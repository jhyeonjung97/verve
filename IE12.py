import pandas as pd

x = pd.read_csv('energy_IE1.tsv', delimiter='\t', index_col=0)
y = pd.read_csv('energy_IE2.tsv', delimiter='\t', index_col=0)
x.columns = ['IE1+IE2']
y.columns = ['IE1+IE2']
z = x+y
z.to_csv('energy_IE12.tsv', sep='\t', index=True)