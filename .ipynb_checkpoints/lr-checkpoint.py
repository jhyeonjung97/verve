import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import argparse

def main():
    parser = argparse.ArgumentParser(description='Perform linear regression using aggregated columns from multiple TSV files excluding the first column, calculate MAE, MSE, plot results, and save output.')
    parser.add_argument('--Y', required=True, help='File path for Y.tsv')
    parser.add_argument('--X1', required=True, help='File path for X1.tsv')
    parser.add_argument('--X2', required=True, help='File path for X2.tsv')
    parser.add_argument('--X3', required=True, help='File path for X3.tsv')

    args = parser.parse_args()

    # Load the data excluding the first column
    df_Y = pd.read_csv(args.Y, delimiter='\t').iloc[:, 1:]
    df_X1 = pd.read_csv(args.X1, delimiter='\t').iloc[:, 1:]
    df_X2 = pd.read_csv(args.X2, delimiter='\t').iloc[:, 1:]
    df_X3 = pd.read_csv(args.X3, delimiter='\t').iloc[:, 1:]

    # Ensure all DataFrames have the same shape
    if not (df_Y.shape == df_X1.shape == df_X2.shape == df_X3.shape):
        raise ValueError("All files must have the same number of rows and columns after excluding the first column.")

    # Reshape the data into a long format
    Y = df_Y.values.flatten()
    X1 = df_X1.values.flatten()
    X2 = df_X2.values.flatten()
    X3 = df_X3.values.flatten()
    
    # Combine into a single DataFrame
    df_combined = pd.DataFrame({
        'E_form': Y,
        'ICOHP': X1,
        'MadelungL': X2,
        'CFSE': X3
    })

    # Drop rows with NaN values (if any)
    df_combined.dropna(inplace=True)

    # Set up the predictors and response
    X = df_combined[['ICOHP', 'MadelungL', 'CFSE']]
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
    output_filename = 'regression_output.tsv'
    df_combined.to_csv(output_filename, sep='\t', index=False)

    # Plotting actual vs predicted values
    plt.figure(figsize=(10, 6))
    plt.scatter(Y, Y_pred, alpha=0.3)
    plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--', lw=2)  # Ideal line where actual = predicted
    plt.xlabel('DFT-calculated Formation Energy (eV)')
    plt.ylabel('Predicted Formation Energy (eV)')
    # plt.title('Calculated vs. Predicted Values')
    # plt.show()
    plt.tight_layout()
    plt.gcf().savefig('regression_output.png', bbox_inches="tight")
    
    # Display results
    print(f"Intercept: {model.intercept_}")
    print(f"Coefficients: {model.coef_}")
    print(f"R-squared: {model.score(X, Y)}")
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    main()
