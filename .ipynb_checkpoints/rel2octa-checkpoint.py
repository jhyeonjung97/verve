import pandas as pd
import sys

# Example read and write functions (replace these with your actual implementation)
def read(data):
    return pd.read_csv(data, delimiter='\t', index_col=0)

def write(df, filename):
    df.to_csv(filename, sep='\t')

# Assume data is the first argument
data = sys.argv[1]

# Read the data, keeping the first column as the index
df = read(data)

# Split filename and extension correctly
filename, ext = data.rsplit('.', 1)

# Iterate over the specified rows and modify the DataFrame
for metal_row in ['3d', '4d', '5d']:
    for i in range(5):
        for j in range(13):
            index1 = i * j
            index2 = 6 * j
            if index1 < len(df) and index2 < len(df):
                if not pd.isna(df.loc[df.index[index1], metal_row]) and not pd.isna(df.loc[df.index[index2], metal_row]):
                    df.loc[df.index[index1], metal_row] = df.loc[df.index[index1], metal_row] - df.loc[df.index[index2], metal_row]

# Print the DataFrame (optional)
print(df)

# Write the modified DataFrame to a new file, keeping the index
write(df, filename=f'{filename}_rel.{ext}')
