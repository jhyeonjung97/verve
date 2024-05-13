import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

def main():
    parser = argparse.ArgumentParser(description='Perform linear regression using aggregated columns from multiple TSV files excluding the first column, calculate MAE, MSE, plot results, and save output.')
    parser.add_argument('--X', required=True, nargs='+', help='File paths for one or more X.tsv files')
    parser.add_argument('-o', '--output', dest='filename', type=str, default='', help="output filename")
    args = parser.parse_args()
    filename = args.filename
    
    df_X_combined = pd.concat(args.X, axis=0)
    print(df_X_combined)

if __name__ == "__main__":
    main()
