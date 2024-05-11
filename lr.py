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
    
    if args.columns:
        X_dataframes = [pd.read_csv(x_file, delimiter='\t')[args.columns] for x_file in args.X]
    else:
        X_dataframes = [pd.read_csv(x_file, delimiter='\t').iloc[:, 1:] for x_file in args.X]
        
    # Ensure all DataFrames have the same shape
    all_shapes = [df_Y.shape] + [df.shape for df in X_dataframes]
    if not all(shape == all_shapes[0] for shape in all_shapes):
        raise ValueError("All files must have the same number of rows and columns after excluding the first column.")

    # Combining all X dataframes (ensure they are compatible)
    X_combined = np.column_stack([df.values.flatten() for df in X_dataframes])
    
    # Create column names for X
    column_names = args.columns if args.columns else [f'X{i+1}' for i in range(len(X_dataframes))]

    # Combine the X data into a single DataFrame and add Y
    df_combined = pd.DataFrame(X_combined, columns=column_names)
    df_combined['E_form'] = df_Y.values.flatten()
    
    # Handle NaNs carefully
    valid_indices = df_combined.index[df_combined.notna().all(1)]  # Get indices before dropping NaNs
    filtered_labels = labels[valid_indices]  # Filter labels to match valid indices
    df_combined.dropna(inplace=True)

    # Set up the predictors and response
    X = df_combined[column_names]
    Y = df_combined['E_form']

    # Initialize and fit the Linear Regression Model
    model = LinearRegression()
    model.fit(X, Y)

    # Make predictions
    Y_pred = model.predict(X)

    # Calculate MAE and MSE
    mae = mean_absolute_error(Y, Y_pred)
    mse = mean_squared_error(Y, Y_pred)

    # Append predictions and error metrics to the DataFrame
    df_combined['Predicted E_form'] = Y_pred
    df_combined['Residuals'] = Y - Y_pred

    # Save the extended DataFrame to a new TSV file
    tsv_filename = f'{filename}.tsv'
    png_filename = f'{filename}.png'
    df_combined.to_csv(tsv_filename, sep='\t', index=False)
    print(f"Results saved to {tsv_filename}")
    
    # Plotting actual vs predicted values
    plt.figure(figsize=(10, 8))
    colors = ['red', 'green', 'blue']  # Extend this list if more files
    file_row_count = df_combined.shape[0] // len(args.X)  # Adjust row count post NaN removal
    
    for i, color in enumerate(colors):
        start_index = i * file_row_count
        end_index = start_index + file_row_count
        plt.scatter(Y[start_index:end_index], Y_pred[start_index:end_index], alpha=0.3, c=color)
        
        # Annotate each point with its label
        for j in range(start_index, end_index):
            if j < len(filtered_labels):  # Ensure within bounds of filtered_labels
                plt.annotate(filtered_labels[j], (Y[j], Y_pred[j]))
        
    plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--', lw=2) 
    plt.xlabel('DFT-calculated Formation Energy (eV)')
    plt.ylabel('Predicted Formation Energy (eV)')
    plt.legend()  # Use a slice of labels list to create a legend
    # plt.title('Calculated vs. Predicted Values')
    # plt.show()
    plt.tight_layout()
    plt.gcf().savefig(png_filename, bbox_inches="tight")
    
    # Display results
    print(f"Intercept: {model.intercept_}")
    print(f"Coefficients: {model.coef_}")
    print(f"R-squared: {model.score(X, Y)}")
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"Figure saved as {png_filename}")

if __name__ == "__main__":
    main()
