import pandas as pd
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
    for i in range(5):
        for j in range(13):
            index1 = i * j
            index2 = 6 * j
            if not pd.isna(df.at[index1, metal_row]) and not pd.isna(df.at[index2, metal_row]):
                print(df[metal_row, index1])
                print(df[metal_row, index2])
                df.at[index1, metal_row] = df.at[index1, metal_row] - df.at[index2, metal_row]
                print(df[metal_row, index1])

index_pattern = list(range(13)) * 6
index_pattern = index_pattern[:78]
df.index = index_pattern

# Print the DataFrame (optional)
print(df)

# Write the modified DataFrame to a new file
write(df, filename=f'{filename}_rel.{ext}')
