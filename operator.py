import numpy as np
import pandas as pd
import argparse

# Define the argument parser
parser = argparse.ArgumentParser(description='Perform arithmetic operations on two TSV files.')
parser.add_argument('-x', '--file_x', required=True, help='Path to the first TSV file')
parser.add_argument('-y', '--file_y', required=True, help='Path to the second TSV file')
parser.add_argument('-z', '--file_z', required=True, help='Path to the output TSV file')
parser.add_argument('-o', '--operator', required=True, choices=['+', '-', '*', '/'], help='Arithmetic operator to apply')

# Parse the arguments
args = parser.parse_args()

# Load the data from TSV files
X = pd.read_csv(args.file_x, delimiter='\t', index_col=0)
Y = pd.read_csv(args.file_y, delimiter='\t', index_col=0)

# Perform the specified operation
if args.operator == '+':
    Z = X.add(Y, fill_value=0)
elif args.operator == '-':
    Z = X.subtract(Y, fill_value=0)
elif args.operator == '*':
    Z = X.multiply(Y, fill_value=1)
elif args.operator == '/':
    Z = X.divide(Y, fill_value=1)

# Save the result to a new TSV file
Z.to_csv(args.file_z, sep='\t', index=True)

print(f"Result saved to {args.file_z}")
