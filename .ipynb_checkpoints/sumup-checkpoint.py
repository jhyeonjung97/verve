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
        df = pd.read_csv(file, delimiter='\t').iloc[:, 1:]
        if summed_x is None:
            summed_x = df.copy()
        else:
            summed_x += df
    
    for file in yfiles:
        df = pd.read_csv(file, delimiter='\t').iloc[:, 1:]
        if summed_y is None:
            summed_y = df.copy()
        else:
            summed_y += df

    plt.figure(figsize=(8, 6))
    XX_values = np.array([])
    YY_values = np.array([])
    num_rows, num_cols = summed_x.shape
    
    for col_name in summed_x.columns:
        print(col_name)
        X_values = summed_x[col_name].values
        Y_values = summed_y[col_name].values
        XX_values = np.concatenate((XX_values, X_values))
        YY_values = np.concatenate((YY_values, Y_values))
        plt.scatter(X_values, Y_values, label=col_name)
        
    A = np.vstack([XX_values, np.ones(len(XX_values))]).T
    coeffs, residuals, rank, s = np.linalg.lstsq(A, YY_values, rcond=None)
    a, b = coeffs
    xx = np.linspace(np.min(XX_values), np.max(XX_values), 1000)
    yy = a * xx + b
    
    plt.plot(xx, yy, color='black', alpha=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    
    YY_pred = a*XX_values + b
    R2 = r2_score(YY_values, YY_pred)
    MAE = mean_absolute_error(YY_values, YY_pred)
    MSE = mean_squared_error(YY_values, YY_pred)

    x_text_margin = np.min(XX_values) + (np.max(XX_values) - np.min(XX_values)) * 0.25
    y_text_margin = np.max(YY_values) - (np.max(YY_values) - np.min(YY_values)) * 0.95
    plt.text(x_text_margin, y_text_margin, 
             f"Y = {a:.3f}X + {b:.3f}\nR^2: {R2:.3f}, MAE: {MAE:.3f}, MSE: {MSE:.3f}", fontsize=9)
    
    # print(f"Y = {a:.3f}X + {b:.3f}")
    # print(f"R^2: {R2:.3f}, MAE: {MAE:.3f}, MSE: {MSE:.3f}")
    # plt.text(np.min(X), np.max(Y), f"Y = {a:.3f}X + {b:.3f}", fontsize=12)
    # plt.text(np.min(X), np.max(Y) - (np.max(Y) - np.min(Y)) * 0.1, 
    #          f"R^2: {R2:.3f}, MAE: {MAE:.3f}, MSE: {MSE:.3f}", fontsize=12)
    
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
    parser.add_argument('--xdata', type=str, default='X')
    parser.add_argument('--ydata', type=str, default='Y')
    
    args = parser.parse_args()
    xfiles = args.xfiles
    yfiles = args.yfiles
    xlabel = args.xlabel
    ylabel = args.ylabel
    xdata = args.xdata
    ydata = args.ydata
    output = args.output
    if not output:
        png_filename = f"linear_{xdata}_vs_{ydata}.png"
        tsv_filename = f"linear_{xdata}_vs_{ydata}.tsv"
    else:
        png_filename = f"linear_{output}.png"
        tsv_filename = f"linear_{output}.tsv"
    line_fitting(xfiles, yfiles, xlabel, ylabel, png_filename, tsv_filename)
