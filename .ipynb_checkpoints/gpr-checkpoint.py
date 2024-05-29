import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split, GridSearchCV, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Perform regression using aggregated columns from multiple TSV files excluding the first column, calculate MAE, MSE, plot results, and save output.')
    parser.add_argument('--Y', required=True, help='File path for Y.tsv')
    parser.add_argument('--X', required=True, nargs='+', help='File paths for one or more X.tsv files')
    parser.add_argument('--C', default='concat_coord.tsv', help='File path for C.tsv')
    parser.add_argument('--R', default='concat_row.tsv', help='File path for R.tsv')
    parser.add_argument('--L', default='concat_element.tsv', help='File path for L.tsv')
    parser.add_argument('-i', '--index', required=True, nargs='+', help='Column names to be used from the X.tsv files')
    parser.add_argument('-r', '--row', default=None, type=int, help='Filter by specific row')
    parser.add_argument('-c', '--coord', default=None, type=str, help='Filter by specific coordination')
    parser.add_argument('-z', '--zero', action='store_true', default=False, help='Filter E_form values less than zero')
    parser.add_argument('-o', '--output', dest='filename', type=str, default='', help="Output filename")
    args = parser.parse_args()

    # Generate the output filename based on provided arguments
    filename = str(len(args.index))
    if args.filename:
        filename += '_' + args.filename
    if args.row:
        filename += f'_{args.row}d'
    if args.coord:
        filename += f'_{args.coord}'
    if args.zero:
        filename += '_zero'

    # Load the data excluding the first column
    df_Y = pd.read_csv(args.Y, delimiter='\t').iloc[:, 1:]
    df_C = pd.read_csv(args.C, delimiter='\t', dtype=str).iloc[:, 1:]
    df_R = pd.read_csv(args.R, delimiter='\t', dtype=int).iloc[:, 1:]
    df_L = pd.read_csv(args.L, delimiter='\t', dtype=str).iloc[:, 1:]
    
    X_dataframes = []
    for x_file in args.X:
        df_X = pd.read_csv(x_file, delimiter='\t').iloc[:, 1:]
        single_column_df = pd.melt(df_X)['value'].reset_index(drop=True)
        X_dataframes.append(single_column_df)

    # Combine dataframes
    df_X_combined = pd.concat(X_dataframes, axis=1)
    df_X_combined.columns = args.index
    df_Y_combined = pd.melt(df_Y.iloc[:df_X_combined.shape[0]])
    df_C_combined = pd.melt(df_C.iloc[:df_X_combined.shape[0]])
    df_R_combined = pd.melt(df_R.iloc[:df_X_combined.shape[0]])
    df_L_combined = pd.melt(df_L.iloc[:df_X_combined.shape[0]])
    
    # Create combined dataframe
    X = df_X_combined
    Y = pd.DataFrame(df_Y_combined['value'], columns=['E_form'])
    R = pd.DataFrame(df_R_combined['value'], columns=['Row'])
    L = pd.DataFrame(df_L_combined['value'], columns=['Metal'])
    C = pd.DataFrame(df_C_combined['value'], columns=['Coordination'])

    df_combined = pd.concat([R, L, C, X, Y], axis=1).dropna()
    
    # Apply filters
    if args.row:
        df_combined = df_combined[df_combined['Row'] == args.row]
    if args.coord:
        df_combined = df_combined[df_combined['Coordination'] == args.coord]
    if args.zero:
        df_combined = df_combined[df_combined['E_form'] < 0]

    X = df_combined.iloc[:, -(len(args.index) + 1):-1]
    Y = df_combined['E_form']

    print(X)
    print(Y)
    
#     X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

#     params = [{'alpha': np.logspace(-3, 2, 200)}]
#     model = GridSearchCV(GPR(normalize_y=True), params, cv=5)
    
#     poly = PolynomialFeatures(degree=2)
#     pipe = Pipeline([
#         ('scaler', StandardScaler()),
#         ('model', model),
#     ])
    
#     score = cross_validate(pipe, X_train, y_train, scoring=['r2', 'neg_mean_absolute_error'], cv=5)
#     print(score)
#     print('CV scores:')
#     print(np.mean(score['test_neg_mean_absolute_error']))
#     print(np.mean(score['test_r2']))
    
#     pipe.fit(X_train, y_train)
#     opt_alpha = float(pipe['model'].best_estimator_.get_params()['alpha'])

#     model = GPR(normalize_y=True, alpha=opt_alpha)
#     model.fit(X, Y)
    
#     Y_pred = model.predict(X)
#     mae = mean_absolute_error(Y, Y_pred)
#     mse = mean_squared_error(Y, Y_pred)

#     # Save results
#     tsv_filename = f'regression{filename}.tsv'
#     png_filename = f'regression{filename}.png'
#     log_filename = f'regression{filename}.log'
    
#     df_combined.to_csv(tsv_filename, sep='\t', index=False)

#     with open(log_filename, 'w') as file:
#         file.write(f"\nR-squared: {model.score(X, Y)}\n")
#         file.write(f"Mean Absolute Error: {mae}\n")
#         file.write(f"Mean Squared Error: {mse}\n\n")
    
#     df_combined['Predicted E_form'] = Y_pred
#     df_combined['Residuals'] = Y - Y_pred

#     # Plot results
#     plt.figure(figsize=(10, 8))
#     colors = ['red', 'green', 'blue']
#     markers = ['v', '^', 's', 'D', 'o']
#     for i, row in enumerate([3, 4, 5]):
#         sub = df_combined[df_combined['Row'] == row]
#         for j, coordination in enumerate(['WZ', 'ZB', 'TN', '33', 'RS']):
#             subset = sub[sub['Coordination'] == coordination]
#             plt.scatter(subset['E_form'], subset['Predicted E_form'], alpha=0.3, color=colors[i], marker=markers[j], label=f'{row}_{coordination}')
#             for (x, y, label) in zip(subset['E_form'], subset['Predicted E_form'], subset['Metal']):
#                 plt.annotate(label, (x, y))
    
#     plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--', lw=1)
#     plt.xlabel('DFT-calculated Formation Energy (eV)')
#     plt.ylabel('Predicted Formation Energy (eV)')
#     plt.legend()
#     plt.tight_layout()
#     plt.gcf().savefig(png_filename, bbox_inches="tight")
#     plt.close()

#     # Plot correlation matrix
#     M = pd.concat([Y, X], axis=1)
#     correlation_matrix = M.corr()
#     abs_correlation_matrix = correlation_matrix.abs()
    
#     plt.figure(figsize=(7, 6))
#     sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
#     plt.xticks(np.arange(M.shape[1]) + 0.5, M.columns, rotation=90, ha='right')
#     plt.yticks(np.arange(M.shape[1]) + 0.5, M.columns, rotation=0, va='center')
#     plt.tight_layout()
#     plt.gcf().savefig(f'covariance_matrix{filename}.png', bbox_inches="tight")
#     plt.close()
    
#     plt.figure(figsize=(7, 6))
#     sns.heatmap(abs_correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', center=0, vmin=0, vmax=1)
#     plt.xticks(np.arange(M.shape[1]) + 0.5, M.columns, rotation=90, ha='right')
#     plt.yticks(np.arange(M.shape[1]) + 0.5, M.columns, rotation=0, va='center')
#     plt.tight_layout()
#     plt.gcf().savefig(f'abs_covariance_matrix{filename}.png', bbox_inches="tight")
#     plt.close()

if __name__ == "__main__":
    main()