import pandas as pd
from sklearn.linear_model import LinearRegression
import argparse

def main():
    # Set up argument parsing
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

    # Check that all DataFrames have the same shape
    if not (df_Y.shape == df_X1.shape == df_X2.shape == df_X3.shape):
        raise ValueError("All files must have the same number of rows and columns.")

    # Perform regression for each column set
    results = []
    for i in range(df_Y.shape[1]):  # Iterate over the number of columns
        Y = df_Y.iloc[:, i]
        X = pd.concat([df_X1.iloc[:, i], df_X2.iloc[:, i], df_X3.iloc[:, i]], axis=1)
        
        model = LinearRegression()
        model.fit(X, Y)
        
        results.append({
            'Column': df_Y.columns[i],
            'Intercept': model.intercept_,
            'Coefficients': model.coef_,
            'R_squared': model.score(X, Y)
        })

    # Print results for each regression
    for result in results:
        print(f"Results for {result['Column']}:")
        print(f"  Intercept: {result['Intercept']}")
        print(f"  Coefficients: {result['Coefficients']}")
        print(f"  R-squared: {result['R_squared']}\n")

if __name__ == "__main__":
    main()
