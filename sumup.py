import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def line_fitting(xfiles, yfiles, xlabel, ylabel, png_filename, tsv_filename):
    summed_x = None
    summed_y = None
    
    for file in xfiles:
        df = pd.read_csv(file, delimiter='\t', index_col=0)
        if summed_x is None:
            summed_x = df.copy()
        else:
            summed_xvalues = summed_x.values + df.values
            print(summed_xvalues)
            summed_x = pd.DataFrame(summed_xvalues, columns=df.columns, index=['Sum'])
            
    for file in yfiles:
        df = pd.read_csv(file, delimiter='\t', index_col=0)
        if summed_y is None:
            summed_y = df.copy()
        else:
            summed_yvalues = summed_y.values + df.values
            summed_y = pd.DataFrame(summed_yvalues, columns=df.columns, index=['Sum'])
    print(summed_x)
    with open(tsv_filename, 'w') as f:
        summed_x.to_csv(f, sep='\t')
        f.write('\n')
        summed_y.to_csv(f, sep='\t')    
    print(f"Figure saved as {tsv_filename}")
        
    X = summed_x.iloc[0].values
    Y = summed_y.iloc[0].values
    A = np.vstack([X, np.ones(len(X))]).T
    coeffs, residuals, rank, s = np.linalg.lstsq(A, Y, rcond=None)
    a, b = coeffs
    
    Y_pred = a*X + b
    R2 = r2_score(Y, Y_pred)
    MAE = mean_absolute_error(Y, Y_pred)
    MSE = mean_squared_error(Y, Y_pred)

    # print(f"Y = {a:.3f}X + {b:.3f}")
    # print(f"R^2: {R2:.3f}, MAE: {MAE:.3f}, MSE: {MSE:.3f}")
    # plt.text(np.min(X), np.max(Y), f"Y = {a:.3f}X + {b:.3f}", fontsize=12)
    # plt.text(np.min(X), np.max(Y) - (np.max(Y) - np.min(Y)) * 0.1, 
    #          f"R^2: {R2:.3f}, MAE: {MAE:.3f}, MSE: {MSE:.3f}", fontsize=12)
    
    x_text_margin = np.min(X) + (np.max(X) - np.min(X)) * 0.02
    y_text_margin = np.max(Y) - (np.max(Y) - np.min(Y)) * 0.05

    plt.figure()
    plt.scatter(X, Y, color='r')
    xx = np.linspace(np.min(X), np.max(X), 1000)
    yy = a * xx + b
    
    plt.plot(xx, yy, color='b', alpha=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.text(x_text_margin, y_text_margin, 
             f"Y = {a:.3f}X + {b:.3f}\nR^2: {R2:.3f}, MAE: {MAE:.3f}, MSE: {MSE:.3f}", fontsize=9)
    
    plt.savefig(png_filename, bbox_inches="tight")
    print(f"Figure saved as {png_filename}")
    plt.close()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot 2d fitting with sumup data.')
    parser.add_argument('-x', '--xfiles', nargs='+', required=True)
    parser.add_argument('-y', '--yfiles', nargs='+', required=True)
    parser.add_argument('-o', '--output', type=str, default=None)
    parser.add_argument('--xlabel', type=str, default='X')
    parser.add_argument('--ylabel', type=str, default='Y')
    
    args = parser.parse_args()
    xfiles = args.xfiles
    yfiles = args.yfiles
    xlabel = args.xlabel
    ylabel = args.ylabel
    output = args.output
    if not output:
        png_filename = f"linear_{xlabel}_vs_{ylabel}.png"
        tsv_filename = f"linear_{xlabel}_vs_{ylabel}.tsv"
    else:
        png_filename = f"linear_{output}.png"
        tsv_filename = f"linear_{output}.tsv"
    line_fitting(xfiles, yfiles, xlabel, ylabel, png_filename, tsv_filename)
