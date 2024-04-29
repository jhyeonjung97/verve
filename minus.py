import pandas as pd
import sys

def invert_signs_in_tsv(input_filename):
    # Read the TSV file
    df = pd.read_csv(input_filename, delimiter='\t')
    
    # Invert the signs of all numeric data
    for column in df.select_dtypes(include=[int, float]):
        df[column] = -df[column]
    
    # Construct the output filename
    output_filename = "minus_" + input_filename
    
    # Write the modified DataFrame to a new TSV file
    df.to_csv(output_filename, index=False, sep='\t')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py input.tsv")
    else:
        input_filename = sys.argv[1]
        invert_signs_in_tsv(input_filename)
