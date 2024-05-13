import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import argparse

def main():
    parser = argparse.ArgumentParser(description='Perform linear regression using aggregated columns from multiple TSV files excluding the first column, calculate MAE, MSE, plot results, and save output.')
    parser.add_argument('--Y', required=True, help='File path for Y.tsv')
    parser.add_argument('--X', required=True, nargs='+', help='File paths for one or more X.tsv files')
    parser.add_argument('-c', '--columns', nargs='+', help='Column names to be used from the X.tsv files')
    parser.add_argument('-o', '--output', dest='filename', type=str, default='', help="output filename")
    args = parser.parse_args()

    filename = f'regression{args.filename}'
    
    # Load the data excluding the first column
    df_Y = pd.read_csv(args.Y, delimiter='\t').iloc[:, 1:]
    labels = pd.read_csv('/pscratch/sd/j/jiuy97/3_V_shape/merged_element.tsv', delimiter='\t').iloc[:, 1:].values.flatten()
    X_dataframes = []
    data_counts = []
    
    for x_file in args.X:
        df_X = pd.read_csv(x_file, delimiter='\t').iloc[:, 1:]
        melted_df = pd.melt(df_X)
        single_column_df = melted_df['value'].reset_index(drop=True)
        # valid_df = single_column_df.dropna()
        # row_count = df_X.shape[0]
        # nan_count = df_X.isna().any(axis=1).sum()
        X_dataframes.append(melted_df)
        # data_counts.append(row_count - nan_count)
    
    df_combined = pd.concat(X_dataframes, axis=1)
    df_combined = df_combined.dropna()
    print(df_combined)

    X = df_combined
    Y = df_Y.iloc[:df_combined.shape[0]]

    print(X)
    print(Y)

    model = LinearRegression()
    model.fit(X, Y)

    Y_pred = model.predict(X)

    mae = mean_absolute_error(Y, Y_pred)
    mse = mean_squared_error(Y, Y_pred)

    df_combined['Predicted E_form'] = Y_pred
    df_combined['Residuals'] = Y - Y_pred

    tsv_filename = f'{filename}.tsv'
    png_filename = f'{filename}.png'
    df_combined.to_csv(tsv_filename, sep='\t', index=False)
    
    plt.figure(figsize=(10, 8))
    colors = ['red', 'green', 'blue']  # Ensure enough colors are defined
    start_index = 0
    for i, data_count in enumerate(data_counts):
        end_index = start_index + data_count
        plt.scatter(Y[start_index:end_index], Y_pred[start_index:end_index], alpha=0.3, c=colors[i % len(colors)])
        for j in range(start_index, end_index):
            plt.annotate(labels[j], (Y[j], Y_pred[j]))
        start_index = end_index
    
    plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--', lw=2)
    plt.xlabel('DFT-calculated Formation Energy (eV)')
    plt.ylabel('Predicted Formation Energy (eV)')
    plt.tight_layout()
    plt.gcf().savefig(png_filename, bbox_inches="tight")
    
    print(f"Results saved to {tsv_filename}")
    print(f"Intercept: {model.intercept_}")
    print(f"Coefficients: {model.coef_}")
    print(f"R-squared: {model.score(X, Y)}")
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"Figure saved as {png_filename}")

if __name__ == "__main__":
    main()
