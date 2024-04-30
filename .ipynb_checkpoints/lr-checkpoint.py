import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import argparse

def main():
    parser = argparse.ArgumentParser(description='Perform linear regression using aggregated columns from multiple TSV files and calculate MAE, MSE.')
    parser.add_argument('--Y', required=True, help='File path for Y.tsv')
    parser.add_argument('--X1', required=True, help='File path for X1.tsv')
    parser.add_argument('--X2', required=True, help='File path for X2.tsv')
    parser.add_argument('--X3', required=True, help='File path for X3.tsv')

    args = parser.parse_args()

    # Load the data
    df_Y = pd.read_csv(args.Y, delimiter='\t')
    df_X1 = pd.read_csv(args.X1, delimiter='\t')
    df_X2 = pd.read_csv(args.X2, delimiter='\t')
    df_X3 = pd.read_csv(args.X3, delimiter='\t')

    # Ensure all DataFrames have the same shape
    if not (df_Y.shape == df_X1.shape == df_X2.shape == df_X3.shape):
        raise ValueError("All files must have the same number of rows and columns.")

    # Reshape the data into a long format
    Y = df_Y.values.flatten()
    X1 = df_X1.values.flatten()
    X2 = df_X2.values.flatten()
    X3 = df_X3.values.flatten()
    
    # Combine into a single DataFrame
    df_combined = pd.DataFrame({
        'Y': Y,
        'X1': X1,
        'X2': X2,
        'X3': X3
    })

    # Drop rows with NaN values (if any)
    df_combined.dropna(inplace=True)

    # Set up the predictors and response
    X = df_combined[['X1', 'X2', 'X3']]
    Y = df_combined['Y']

    # Initialize and fit the Linear Regression Model
    model = LinearRegression()
    model.fit(X, Y)

    # Make predictions
    Y_pred = model.predict(X)

    # Calculate MAE and MSE
    mae = mean_absolute_error(Y, Y_pred)
    mse = mean_squared_error(Y, Y_pred)

    # Display results
    print(f"Intercept: {model.intercept_}")
    print(f"Coefficients: {model.coef_}")
    print(f"R-squared: {model.score(X, Y)}")
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")

if __name__ == "__main__":
    main()
