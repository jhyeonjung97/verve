import pandas as pd
import numpy as np
import sys

# Example read and write functions (replace these with your actual implementation)
def read(data):
    return pd.read_csv(data, delimiter='\t')

def write(df, filename):
    df.to_csv(filename, sep='\t', index=False)

# Assume data is the first argument
data = sys.argv[1]

# Read the data
df = read(data).iloc[:, 1:]

# Split filename and extension correctly
filename, ext = data.rsplit('.', 1)

# Iterate over the specified rows and modify the DataFrame
for metal_row in ['3d', '4d', '5d']:
    for i in range(6):
        for j in range(13):
            index1 = 13 * i + j
            index2 = 13 * 5 + j
            if index1 < len(df) and index2 < len(df):
                if not pd.isna(df.at[index1, metal_row]) and not pd.isna(df.at[index2, metal_row]):
                    df.at[index1, metal_row] = df.at[index1, metal_row] - df.at[index2, metal_row]

# Remove the last 13 lines
df = df[:-13]

# Generate the new index pattern
index_pattern = np.tile(np.arange(13), len(df) // 13 + 1)[:len(df)]

# Set the new index
df.index = index_pattern

# Write the modified DataFrame to a new file
df.to_csv(f'{filename}_rel.{ext}', sep='\t', index=True)
print(f"DataFrame saved as {filename}_rel.{ext}")