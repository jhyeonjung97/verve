import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

def main():
    parser = argparse.ArgumentParser(description='Perform linear regression using aggregated columns from multiple TSV files excluding the first column, calculate MAE, MSE, plot results, and save output.')
    parser.add_argument('--Y', required=True, help='File path for Y.tsv')
    parser.add_argument('--X', required=True, nargs='+', help='File paths for one or more X.tsv files')
    parser.add_argument('-c', '--columns', required=True, nargs='+', help='Column names to be used from the X.tsv files')
    parser.add_argument('-o', '--output', dest='filename', type=str, default='', help="output filename")
    args = parser.parse_args()
    numb = int(args.filename)
    filename = f'regression{args.filename}'
    
    # Load the data excluding the first column
    df_Y = pd.read_csv(args.Y, delimiter='\t').iloc[:, 1:]
    df_L = pd.melt(pd.read_csv('/pscratch/sd/j/jiuy97/3_V_shape/merged_element.tsv', delimiter='\t').iloc[:, 1:])
    X_dataframes = []
    data_counts = []
    
    for x_file in args.X:
        df_X = pd.read_csv(x_file, delimiter='\t').iloc[:, 1:]
        melted_df = pd.melt(df_X)
        single_column_df = melted_df['value'].reset_index(drop=True)
        X_dataframes.append(single_column_df)
    
    df_X_combined = pd.concat(X_dataframes, axis=1)
    df_X_combined.columns = args.columns
    df_Y_combined = pd.melt(df_Y.iloc[:df_X_combined.shape[0]])
    
    X = df_X_combined
    Y = pd.DataFrame(df_Y_combined['value'])
    labels = pd.DataFrame(df_L['value'])
    rows = pd.DataFrame(df_Y_combined['variable'])
    
    Y.columns = ['E_form']
    rows.columns = ['Row']
    labels.columns = ['Metal']
    
    df_combined = pd.concat([rows, labels, X, Y], axis=1)
    df_combined = df_combined.dropna()
    
    X = df_combined.iloc[:, -(numb+1):-1]
    Y = df_combined['E_form']
    rows = df_combined['Row']
    labels = df_combined['Metal']
    
    model = LinearRegression()
    model.fit(X, Y)

    Y_pred = model.predict(X)
    
    mae = mean_absolute_error(Y, Y_pred)
    mse = mean_squared_error(Y, Y_pred)
    
    print(f"Intercept: {model.intercept_}")
    print(f"Coefficients: {model.coef_}")
    print(f"R-squared: {model.score(X, Y)}")
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    
    tsv_filename = f'{filename}.tsv'
    png_filename = f'{filename}.png'
    matrix_filename = f'covariance_matrix{str(numb)}.png'
    df_combined.to_csv(tsv_filename, sep='\t', index=False)
    print(f"Results saved to {tsv_filename}")
    
    df_combined['Predicted E_form'] = Y_pred
    df_combined['Residuals'] = Y - Y_pred

    plt.figure(figsize=(10, 8))
    colors = ['red', 'green', 'blue']
    for i, row in enumerate(['3d', '4d', '5d']):
        subset = df_combined[df_combined['Row'] == row]
        LL = subset['Metal']
        YY = subset['E_form']
        YY_pred = subset['Predicted E_form']
        plt.scatter(YY, YY_pred, alpha=0.3, c=colors[i], label=row)
        for (x, y, label) in zip(YY, YY_pred, LL):
            plt.annotate(label, (x, y))
            
    plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--', lw=2)
    plt.xlabel('DFT-calculated Formation Energy (eV)')
    plt.ylabel('Predicted Formation Energy (eV)')
    plt.legend()
    plt.tight_layout()
    plt.gcf().savefig(png_filename, bbox_inches="tight")
    print(f"Figure saved as {png_filename}")
    plt.close()

    rss = np.sum(df_combined['Residuals']**2)
    degrees_of_freedom = X.shape[0] - X.shape[1] - 1  # Adjust for intercept
    estimated_variance = rss / degrees_of_freedom

    print(estimated_variance)
    M = X+Y
    
    XTX_inv = np.linalg.inv(M.T.dot(M))
    covariance_matrix = XTX_inv # * estimated_variance
    print(covariance_matrix)
    
    plt.figure(figsize=(7, 6)) # Set the figure size as needed
    sns.heatmap(covariance_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    plt.xticks(np.arange(len(M.columns)) + 0.5, M.columns, rotation=90, ha='right')
    plt.yticks(np.arange(len(M.columns)) + 0.5, M.columns, rotation=0, va='center')
    plt.title('Covariance matrix showing correlation coefficients')
    plt.tight_layout()
    plt.gcf().savefig(matrix_filename, bbox_inches="tight")
    print(f"Figure saved as {matrix_filename}")
    plt.close()

if __name__ == "__main__":
    main()
