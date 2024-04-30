import argparse
import pandas as pd
from sklearn.linear_model import LinearRegression

parser = argparse.ArgumentParser(description='Perform linear regression.')
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

# Combine the data into a single DataFrame
df = pd.concat([df_Y, df_X1, df_X2, df_X3], axis=1)
df.columns = ['Y', 'X1', 'X2', 'X3']

# Set up the X and Y
X = df[['X1', 'X2', 'X3']]
Y = df['Y']

# Initialize and fit the Linear Regression Model
model = LinearRegression()
model.fit(X, Y)

# Print the coefficients
print('Intercept:', model.intercept_)
print('Coefficients:', model.coef_)
