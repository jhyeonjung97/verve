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
    parser.add_argument('-o', '--output', dest='filename', type=str, default='regression', help="output filename")
    args = parser.parse_args()

    filename = '_' + args.filename
    filename = f'regression_{filename}' if filename else 'regression'
    
    # Load the data excluding the first column
    df_Y = pd.read_csv(args.Y, delimiter='\t').iloc[:, 1:]
    X_dataframes = [pd.read_csv(x_file, delimiter='\t').iloc[:, 1:] for x_file in args.X]

    # Ensure all DataFrames have the same shape
    all_shapes = [df_Y.shape] + [df.shape for df in X_dataframes]
    if not all(shape == all_shapes[0] for shape in all_shapes):
        raise ValueError("All files must have the same number of rows and columns after excluding the first column.")

    # Flatten and combine the X data into a single DataFrame
    Y = df_Y.values.flatten()
    X_combined = np.column_stack([df.values.flatten() for df in X_dataframes])
    
    # Create column names for X
    column_names = args.columns if args.columns else [f'X{i+1}' for i in range(len(X_dataframes))]

    # Combine into a single DataFrame
    df_combined = pd.DataFrame(X_combined, columns=column_names)
    df_combined['E_form'] = Y

    # Drop rows with NaN values (if any)
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
    print(df_combined)
    df_combined.to_csv(tsv_filename, sep='\t', index=False)
    print(f"Results saved to {tsv_filename}")

    # Plotting actual vs predicted values
    plt.figure(figsize=(6, 4))
    plt.scatter(Y, Y_pred, alpha=0.3)
    plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--', lw=2)  # Ideal line where actual = predicted
    plt.xlabel('DFT-calculated Formation Energy (eV)')
    plt.ylabel('Predicted Formation Energy (eV)')
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
