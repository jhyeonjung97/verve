import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as K
from sklearn.metrics import mean_absolute_error, mean_squared_error

def main():
    parser = argparse.ArgumentParser(description='Perform linear regression using aggregated columns from multiple TSV files excluding the first column, calculate MAE, MSE, plot results, and save output.')
    parser.add_argument('--Y', required=True, help='File path for Y.tsv')
    parser.add_argument('--X', required=True, nargs='+', help='File paths for one or more X.tsv files')
    parser.add_argument('--C', default='concat_coord.tsv', help='File paths for one or more C.tsv files')
    parser.add_argument('--R', default='concat_row.tsv', help='File paths for one or more R.tsv files')
    parser.add_argument('--L', default='concat_element.tsv', help='File paths for one or more L.tsv files')
    parser.add_argument('-i', '--index', required=True, nargs='+', help='Column names to be used from the X.tsv files')
    parser.add_argument('-o', '--output', dest='filename', type=str, default='', help="output filename")
    args = parser.parse_args()
    index = args.index
    numb = len(index)
    
    if args.filename:
        filename = str(numb) + '_' + args.filename
    else:
        filename = str(numb)
        
    # Load the data excluding the first column
    df_Y = pd.read_csv(args.Y, delimiter='\t').iloc[:, 1:]
    df_C = pd.read_csv(args.C, delimiter='\t', dtype=str).iloc[:, 1:]
    df_R = pd.read_csv(args.R, delimiter='\t', dtype=str).iloc[:, 1:]
    df_L = pd.read_csv(args.L, delimiter='\t', dtype=str).iloc[:, 1:]
    X_dataframes = []
    data_counts = []
    
    for x_file in args.X:
        df_X = pd.read_csv(x_file, delimiter='\t').iloc[:, 1:]
        melted_df = pd.melt(df_X)
        single_column_df = melted_df['value'].reset_index(drop=True)
        X_dataframes.append(single_column_df)
    
    df_X_combined = pd.concat(X_dataframes, axis=1)
    df_X_combined.columns = index
    df_Y_combined = pd.melt(df_Y.iloc[:df_X_combined.shape[0]])
    df_C_combined = pd.melt(df_C.iloc[:df_X_combined.shape[0]])
    df_R_combined = pd.melt(df_R.iloc[:df_X_combined.shape[0]])
    df_L_combined = pd.melt(df_L.iloc[:df_X_combined.shape[0]])
    
    X = df_X_combined
    Y = pd.DataFrame(df_Y_combined['value'])
    R = pd.DataFrame(df_R_combined['value'])
    L = pd.DataFrame(df_L_combined['value'])
    C = pd.DataFrame(df_C_combined['value'])
    
    Y.columns = ['E_form']
    R.columns = ['Row']
    L.columns = ['Metal']
    C.columns = ['Coordination']
    
    df_combined = pd.concat([R, L, C, X, Y], axis=1)
    df_combined = df_combined.dropna()
    df_combined = df_combined[df_combined['Metal'] != 'Ba']
    
    X = df_combined.iloc[:, -(numb+1):-1]
    Y = df_combined['E_form']
    R = df_combined['Row']
    L = df_combined['Metal']
    C = df_combined['Coordination']

    kernel = K(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2))
    model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
    model.fit(X, Y)

    Y_pred = model.predict(X)
    
    mae = mean_absolute_error(Y, Y_pred)
    mse = mean_squared_error(Y, Y_pred)
    
    print(f"\nKernel: {model.kernel_}\n")
    print(f"\nLog-Marginal-Likelihood: {model.log_marginal_likelihood(model.kernel_.theta)}\n")
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}\n")

    tsv_filename = f'regression{filename}.tsv'
    png_filename = f'regression{filename}.png'
    df_combined.to_csv(tsv_filename, sep='\t', index=False)
    # print(f"Results saved to {tsv_filename}")
    
    df_combined['Predicted E_form'] = Y_pred
    df_combined['Residuals'] = Y - Y_pred

    plt.figure(figsize=(10, 8))
    colors = ['red', 'green', 'blue']
    markers = ['v', '^', 's', 'D', 'o']
    # markers = ['v', 'v', '^', 's', 's', 'o']
    for i, row in enumerate(['3d', '4d', '5d']):
        sub = df_combined[df_combined['Row'] == row]
        for j, coordination in enumerate(['WZ', 'ZB', 'TN', '33', 'RS']):
        # for j, coordination in enumerate(['WZ', 'ZB', 'LT', 'TN', '33', 'RS']):
            subset = sub[sub['Coordination'] == coordination]
            LL = subset['Metal']
            YY = subset['E_form']
            YY_pred = subset['Predicted E_form']
            plt.scatter(YY, YY_pred, alpha=0.3, color=colors[i], marker=markers[j], label=f'{row}_{coordination}')
            for (x, y, label) in zip(YY, YY_pred, LL):
                plt.annotate(label, (x, y))
            
    plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--', lw=1)
    plt.xlabel('DFT-calculated Formation Energy (eV)')
    plt.ylabel('Predicted Formation Energy (eV)')
    plt.legend()
    plt.tight_layout()
    plt.gcf().savefig(png_filename, bbox_inches="tight")
    # print(f"Figure saved as {png_filename}")
    plt.close()

    M = pd.concat([Y, X], axis=1)
    # covariance_matrix = np.cov(M, rowvar=False)
    correlation_matrix = M.corr()
    abs_correlation_matrix = correlation_matrix.abs()
    
    plt.figure(figsize=(7, 6)) # Set the figure size as needed
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    plt.xticks(np.arange(M.shape[1]) + 0.5, M.columns, rotation=90, ha='right')
    plt.yticks(np.arange(M.shape[1]) + 0.5, M.columns, rotation=0, va='center')
    plt.tight_layout()
    plt.gcf().savefig(f'covariance_matrix{str(filename)}.png', bbox_inches="tight")
    plt.close()
    
    plt.figure(figsize=(7, 6)) # Set the figure size as needed
    sns.heatmap(abs_correlation_matrix, annot=True, fmt=".2f", 
                cmap='coolwarm', center=0, vmin=0, vmax=1)
    plt.xticks(np.arange(M.shape[1]) + 0.5, M.columns, rotation=90, ha='right')
    plt.yticks(np.arange(M.shape[1]) + 0.5, M.columns, rotation=0, va='center')
    plt.tight_layout()
    plt.gcf().savefig(f'abs_covariance_matrix{str(filename)}.png', bbox_inches="tight")
    plt.close()
    
if __name__ == "__main__":
    main()
