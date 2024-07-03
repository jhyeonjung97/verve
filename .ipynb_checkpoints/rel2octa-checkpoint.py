import pandas as pd
import sys

# Example read and write functions (replace these with your actual implementation)
def read(data):
    return pd.read_csv(data)

def write(df, filename):
    df.to_csv(filename, index=False)

# Assume data is the first argument
data = sys.argv[1]

# Read the data
df = read(data)

# Split filename and extension correctly
filename, ext = data.rsplit('.', 1)

# Iterate over the specified rows and modify the DataFrame
for metal_row in ['3d', '4d', '5d']:
    for i in range(5):
        for j in range(13):
            if i * j < len(df) and 6 * j < len(df):
                df.loc[i * j, metal_row] = df.loc[i * j, metal_row] - df.loc[6 * j, metal_row]

# Print the DataFrame (optional)
print(df)

# Write the modified DataFrame to a new file
write(df, filename=f'{filename}_rel.{ext}')
