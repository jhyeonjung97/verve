import argparse
import numpy as np
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--X', required=True, help='Path to the input CSV file')
    args = parser.parse_args()

    df = pd.read_csv(args.X, delimiter='\t').iloc[:, 1:]
    df = df / 96.48
    df.to_csv('test.tsv', sep='\t', index=False)

if __name__ == "__main__":
    main()
