import time
import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from scikeras.wrappers import KerasRegressor
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
from hyperopt.pyll.base import scope

# Define the model-building function
@tf.function(reduce_retracing=True)
def build_model(units1, dropout1, units2, dropout2, learning_rate, input_dim):
    model = Sequential()
    model.add(Input(shape=(input_dim,)))
    model.add(Dense(units1, activation='relu'))
    model.add(Dropout(dropout1))
    model.add(Dense(units2, activation='relu'))
    model.add(Dropout(dropout2))
    model.add(Dense(1, activation='linear'))
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(loss='mean_squared_error', optimizer=optimizer)
    return model

def main():
    parser = argparse.ArgumentParser(description='Perform neural network regression using aggregated columns from multiple TSV files excluding the first column, calculate MAE, MSE, plot results, and save output.')
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
    tsv_filename = f'nn_hyperopt{filename}.tsv'
    png_filename = f'nn_hyperopt{filename}.png'
    log_filename = f'nn_hyperopt{filename}.log'
    
    # Load the data excluding the first column
    df_Y = pd.read_csv(args.Y, delimiter='\t').iloc[:, 1:]
    df_C = pd.read_csv(args.C, delimiter='\t', dtype=str).iloc[:, 1:]
    df_R = pd.read_csv(args.R, delimiter='\t', dtype=int).iloc[:, 1:]
    df_L = pd.read_csv(args.L, delimiter='\t', dtype=str).iloc[:, 1:]
    X_dataframes = []
    
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

    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split the data into training and test sets
    overall_start_time = time.time()
    X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

    # Define the search space for HyperOpt
    search_space = {
        'units1': scope.int(hp.quniform('units1', 32, 128, 1)),
        'dropout1': hp.uniform('dropout1', 0.0, 0.5),
        'units2': scope.int(hp.quniform('units2', 32, 128, 1)),
        'dropout2': hp.uniform('dropout2', 0.0, 0.5),
        'learning_rate': hp.loguniform('learning_rate', -5, -2),
        'batch_size': scope.int(hp.quniform('batch_size', 16, 128, 1)),
        'epochs': scope.int(hp.quniform('epochs', 10, 100, 1))
    }

    # Define the objective function for HyperOpt
    def objective(params):
        model = KerasRegressor(model=build_model, 
                               input_dim=X_train.shape[1],
                               units1=params['units1'], 
                               dropout1=params['dropout1'], 
                               units2=params['units2'], 
                               dropout2=params['dropout2'], 
                               learning_rate=params['learning_rate'],
                               epochs=params['epochs'],
                               batch_size=params['batch_size'],
                               verbose=0)
        scores = cross_val_score(model, X_train, Y_train, cv=5, scoring='neg_mean_absolute_error')
        mae = -np.mean(scores)
        return {'loss': mae, 'status': STATUS_OK}

    # Create a Trials object to store the results of the optimization
    trials = Trials()
    
    # Run the optimization with HyperOpt
    start_time = time.time()
    max_evals = 10  # Number of evaluations
    best_params = fmin(fn=objective,
                       space=search_space,
                       algo=tpe.suggest,
                       max_evals=max_evals,
                       trials=trials)
    end_time = time.time()
    optimization_time = end_time - start_time

    # Extract the best parameters
    best_params['units1'] = int(best_params['units1'])
    best_params['units2'] = int(best_params['units2'])
    best_params['batch_size'] = int(best_params['batch_size'])
    best_params['epochs'] = int(best_params['epochs'])

    # Create and train the best model
    best_model = KerasRegressor(model=build_model, 
                                input_dim=X_train.shape[1],
                                units1=best_params['units1'], 
                                dropout1=best_params['dropout1'], 
                                units2=best_params['units2'], 
                                dropout2=best_params['dropout2'], 
                                learning_rate=best_params['learning_rate'],
                                epochs=best_params['epochs'],
                                batch_size=best_params['batch_size'],
                                verbose=1)
    start_time = time.time()
    best_model.fit(X_train, Y_train)
    end_time = time.time()
    fitting_time = end_time - start_time

    # Log the best parameters and times
    with open(log_filename, 'w') as file:
        for param_name in sorted(best_params):
            file.write(f"{param_name}: {best_params[param_name]}\n")

    # Predict on the entire set using the final model
    Y_pred = best_model.predict(X_scaled)

    # Compute and print MAE and MSE for the entire set
    mae = mean_absolute_error(Y, Y_pred)
    mse = mean_squared_error(Y, Y_pred)
    with open(log_filename, 'a') as file:
        file.write("\tMAE\tMSE\n")
        file.write(f"\nEntire\t{mae:.4f}\t{mse:.4f}\n")

    # Predict on the test set using the final model
    Y_pred_test = best_model.predict(X_test)
    mae_test = mean_absolute_error(Y_test, Y_pred_test)
    mse_test = mean_squared_error(Y_test, Y_pred_test)
    with open(log_filename, 'a') as file:
        file.write(f"Test\t{mae_test:.4f}\t{mse_test:.4f}\n\n")

    overall_end_time = time.time()
    overall_time = overall_end_time - overall_start_time
    with open(log_filename, 'a') as file:
        file.write(f"Optimization time: {optimization_time:.2f} sec\n")
        file.write(f"Model fitting time: {fitting_time:.2f} sec\n")
        file.write(f"Overall time: {overall_time:.2f} sec\n")

    # Save predictions and residuals to a TSV file
    df_combined['Predicted E_form'] = Y_pred
    df_combined['Residuals'] = Y - Y_pred
    df_combined.to_csv(tsv_filename, sep='\t', index=False)

    # Plotting (if needed)
    # plt.figure(figsize=(10, 8))
    # colors = ['red', 'green', 'blue']
    # markers = ['v', '^', 's', 'D', 'o']
    # for i, row in enumerate([3, 4, 5]):
    #     sub = df_combined[df_combined['Row'] == row]
    #     for j, coordination in enumerate(['WZ', 'ZB', 'TN', '33', 'RS']):
    #         subset = sub[sub['Coordination'] == coordination]
    #         plt.scatter(subset['E_form'], subset['Predicted E_form'], alpha=0.3, color=colors[i], marker=markers[j], label=f'{row}_{coordination}')
    #         for (x, y, label) in zip(subset['E_form'], subset['Predicted E_form'], subset['Metal']):
    #             plt.annotate(label, (x, y))
    # plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--', lw=1)
    # plt.xlabel('DFT-calculated Formation Energy (eV)')
    # plt.ylabel('Predicted Formation Energy (eV)')
    # plt.legend()
    # plt.tight_layout()
    # plt.gcf().savefig(png_filename, bbox_inches="tight")
    # plt.close()

    # plt.figure(figsize=(7, 6))
    # sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    # plt.xticks(np.arange(M.shape[1]) + 0.5, M.columns, rotation=90, ha='right')
    # plt.yticks(np.arange(M.shape[1]) + 0.5, M.columns, rotation=0, va='center')
    # plt.tight_layout()
    # plt.gcf().savefig(f'covariance_matrix{filename}.png', bbox_inches="tight")
    # plt.close()

if __name__ == "__main__":
    main()
