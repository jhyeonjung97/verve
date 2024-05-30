import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV, cross_validate, train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.gaussian_process.kernels import RBF, Matern, RationalQuadratic
from sklearn.ensemble import GradientBoostingRegressor as GBR
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle

def main():
    parser = argparse.ArgumentParser(description='Perform linear regression using aggregated columns from multiple TSV files excluding the first column, calculate MAE, MSE, plot results, and save output.')
    parser.add_argument('--Y', required=True, help='File path for Y.tsv')
    parser.add_argument('--X', required=True, nargs='+', help='File paths for one or more X.tsv files')
    parser.add_argument('--C', default='concat_coord.tsv', help='File paths for one or more C.tsv files')
    parser.add_argument('--R', default='concat_row.tsv', help='File paths for one or more R.tsv files')
    parser.add_argument('--L', default='concat_element.tsv', help='File paths for one or more L.tsv files')
    parser.add_argument('-i', '--index', required=True, nargs='+', help='Column names to be used from the X.tsv files')
    parser.add_argument('-r', '--row', default=None, type=int)
    parser.add_argument('-c', '--coord', default=None, type=str)
    parser.add_argument('-z', '--zero', action='store_true', default=False)
    parser.add_argument('-o', '--output', dest='filename', type=str, default='', help="output filename")
    args = parser.parse_args()
    index = args.index
    row = args.row
    coord = args.coord
    zero = args.zero
    numb = len(index)
    
    filename = str(numb)
    if args.filename:
        filename = filename + '_' + args.filename
    if row:
        filename = filename + '_' + str(row) + 'd'
    if coord:
        filename = filename + '_' + coord
    if zero:
        filename = filename + '_zero'

    # Save results
    tsv_filename = f'gpr{filename}.tsv'
    png_filename = f'gpr{filename}.png'
    log_filename = f'gpr{filename}.log'
    
    # Load the data excluding the first column
    df_Y = pd.read_csv(args.Y, delimiter='\t').iloc[:, 1:]
    df_C = pd.read_csv(args.C, delimiter='\t', dtype=str).iloc[:, 1:]
    df_R = pd.read_csv(args.R, delimiter='\t', dtype=int).iloc[:, 1:]
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
    # df_combined = df_combined[df_combined['Metal'] != 'Ba']
    if row:
        df_combined = df_combined[df_combined['Row'] == row]
    if coord:
        df_combined = df_combined[df_combined['Coordination'] == coord]
    if zero:
        df_combined = df_combined[df_combined['E_form'] < 0]
        
    X = df_combined.iloc[:, -(numb+1):-1]
    Y = df_combined['E_form']
    R = df_combined['Row']
    L = df_combined['Metal']
    C = df_combined['Coordination']

    # Split the data into training and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Define separate parameter grids for each kernel with a lower bound for length_scale
    gpr_params = {
        'poly__degree': [1, 2, 3],
        'model__alpha': np.logspace(-10, 1, 100)
    }

    # Create the pipeline with PolynomialFeatures and StandardScaler for GPR
    gpr_pipe = Pipeline([
        ('poly', PolynomialFeatures()),
        ('scaler', StandardScaler()),
        ('model', GPR(normalize_y=True)),
    ])

    # Initialize GridSearchCV with GaussianProcessRegressor
    gpr_search = GridSearchCV(gpr_pipe, gpr_params, cv=5, scoring='neg_mean_absolute_error')

    # Cross-validate the pipeline and print CV scores for GPR
    gpr_score = cross_validate(gpr_search, X_train, Y_train, 
                               scoring=['r2', 'neg_mean_absolute_error', 'neg_mean_squared_error'], cv=5)
    # print(f"GPR CV Test R^2: {np.mean(gpr_score['test_r2']):.4f}")
    # print(f"GPR CV Test MAE: {-np.mean(gpr_score['test_neg_mean_absolute_error']):.4f}")  # Take negative to get positive MAE
    # print(f"GPR CV Test MSE: {-np.mean(gpr_score['test_neg_mean_squared_error']):.4f}\n")  # Take negative to get positive MSE
    with open(log_filename, 'w') as file:
        file.write(f"GPR CV Test R^2: {np.mean(gpr_score['test_r2']):.4f}")
        file.write(f"GPR CV Test MAE: {-np.mean(gpr_score['test_neg_mean_absolute_error']):.4f}")  # Take negative to get positive MAE
        file.write(f"GPR CV Test MSE: {-np.mean(gpr_score['test_neg_mean_squared_error']):.4f}\n")  # Take negative to get positive MSE
        
    # Fit the GridSearchCV to the training data
    gpr_search.fit(X_train, Y_train)

    # Extract the best pipeline from GridSearchCV
    best_gpr_pipe = gpr_search.best_estimator_
    # print(f"Optimized poly: {gpr_search.best_params_['poly__degree']}")
    # print(f"Optimized alpha: {gpr_search.best_params_['model__alpha']:.4f}\n")
    with open(log_filename, 'w') as file:
        file.write(f"Optimized poly: {gpr_search.best_params_['poly__degree']}")
        file.write(f"Optimized alpha: {gpr_search.best_params_['model__alpha']:.4f}\n")
        
    # Predict on the entire set using the final GPR model
    Y_pred_gpr = best_gpr_pipe.predict(X)

    # Compute and print MAE and MSE for the entire set for GPR
    mae_gpr = mean_absolute_error(Y, Y_pred_gpr)
    mse_gpr = mean_squared_error(Y, Y_pred_gpr)
    # print(f"GPR R^2: {best_gpr_pipe.score(X, Y):.4f}")
    # print(f"GPR MAE: {mae_gpr:.4f}")
    # print(f"GPR MSE: {mse_gpr:.4f}\n")
    with open(log_filename, 'w') as file:
        file.write(f"GPR R^2: {best_gpr_pipe.score(X, Y):.4f}")
        file.write(f"GPR MAE: {mae_gpr:.4f}")
        file.write(f"GPR MSE: {mse_gpr:.4f}\n")
        
    # Predict on the test set using the final GPR model
    Y_pred_gpr_test = best_gpr_pipe.predict(X_test)

    # Compute and print MAE and MSE for the test set for GPR
    mae_gpr_test = mean_absolute_error(Y_test, Y_pred_gpr_test)
    mse_gpr_test = mean_squared_error(Y_test, Y_pred_gpr_test)
    # print(f"GPR Test R^2: {best_gpr_pipe.score(X_test, Y_test):.4f}")
    # print(f"GPR Test MAE: {mae_gpr_test:.4f}")
    # print(f"GPR Test MSE: {mse_gpr_test:.4f}\n")
    with open(log_filename, 'w') as file:
        file.write(f"GPR Test R^2: {best_gpr_pipe.score(X_test, Y_test):.4f}")
        file.write(f"GPR Test MAE: {mae_gpr_test:.4f}")
        file.write(f"GPR Test MSE: {mse_gpr_test:.4f}\n")

    df_combined['Predicted E_form'] = Y_pred_gbr
    df_combined['Residuals'] = Y - Y_pred_gbr
    
    df_combined.to_csv(tsv_filename, sep='\t', index=False)

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
