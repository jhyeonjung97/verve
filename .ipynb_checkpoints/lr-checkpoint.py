import pandas as pd
from sklearn.linear_model import LinearRegression
import argparse

def main():
    parser = argparse.ArgumentParser(description='Perform multiple linear regressions on corresponding columns across TSV files.')
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

    # Concatenate all X dataframes to handle NaNs collectively
    df_X = pd.concat([df_X1, df_X2, df_X3], axis=1)
    df_combined = pd.concat([df_Y, df_X], axis=1)

    # Drop rows with any NaN values
    df_combined.dropna(inplace=True)

    # Perform regression for each column in Y
    results = []
    for i in range(df_Y.shape[1]):
        Y = df_combined.iloc[:, i]
        X = df_combined.iloc[:, df_Y.shape[1]:]  # X starts right after Y columns

        model = LinearRegression()
        model.fit(X, Y)
        
        results.append({
            'Column': df_Y.columns[i],
            'Intercept': model.intercept_,
            'Coefficients': model.coef_,
            'R_squared': model.score(X, Y)
        })

    # Display results for each regression
    for result in results:
        print(f"Results for {result['Column']}:")
        print(f"  Intercept: {result['Intercept']}")
        print(f"  Coefficients: {result['Coefficients']}")
        print(f"  R-squared: {result['R_squared']}\n")

if __name__ == "__main__":
    main()
