import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse

def line_fitting(xfiles, yfiles, xlabel, ylabel, output):
    summed_x = None
    summed_y = None
    
    for i, file in enumerate(xfiles):
        df = pd.read_csv(file, delimiter='\t', index_col=0)
        if summed_x is None:
            summed_x = df.copy()
        else:
            summed_values = summed_x.values + df.values
            summed_x = pd.DataFrame(summed_values, columns=df.columns, index=['Sum'])
            
    for i, file in enumerate(yfiles):
        df = pd.read_csv(file, delimiter='\t', index_col=0)
        if summed_y is None:
            summed_y = df.copy()
        else:
            summed_values = summed_y.values + df.values
            summed_y = pd.DataFrame(summed_values, columns=df.columns, index=['Sum'])
    
    X = np.array(summed_x)
    Y = np.array(summed_y)
    A = np.vstack([X, np.ones(len(X))]).T
    coeffs, residuals, rank, s = np.linalg.lstsq(A, Y, rcond=None)
    a, b = coeffs
    
    Y_pred = a*X + b
    R2 = r2_score(Y, Y_pred)
    MAE = mean_absolute_error(Y, Y_pred)
    MSE = mean_squared_error(Y, Y_pred)

    print(f"Y = {a:.3f}X + {b:.3f}")
    print(f"R^2: {R2:.3f}, MAE: {MAE:.3f}, MSE: {MSE:.3f}")

    plt.figure()
    plt.scatter(X, Y, color='r')
    xx = np.linspace(np.min(X), np.max(X), 1000)
    yy = a * xx + b
    
    plt.plot(xx, yy, color='b', alpha=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    if save:
        png_filename = f"{filename}_2d.png"
        plt.savefig(png_filename, bbox_inches="tight")
        print(f"Figure saved as {png_filename}")
        plt.close()
    else:
        plt.show()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot 2d fitting with sumup data.')
    parser.add_argument('-x', '--xfiles', nargs='+')
    parser.add_argument('-y', '--yfiles', nargs='+')
    parser.add_argument('-o', '--output', type=str, default='summed')
    parser.add_argument('--xlabel', type=str, default='Element or Lattice parameter (Å)')
    parser.add_argument('--ylabel', type=str, default='Energy (eV) or Charge (e)')    
    parser = argparse.ArgumentParser()
    
    line_fitting(args.xfiles, args.yfiles, args.xlabel, args.ylabel, args.output)