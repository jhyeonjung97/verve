import os
import re
import argparse
import subprocess
import numpy as np
from ase.io import read
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir-range', type=str, default=None, help='Range of directories to investigate, e.g., "3,6"')
    parser.add_argument('-p', '--patterns', nargs='+', default=['TOTEN'], help='Patterns to search and plot: \
    PSCENC, TEWEN, DENC, EXHF, XCENC, PAW_double_counting, EENTRO, EBANDS, EATOM, \
    TOTEN, Madelung, Madelung_M, Madelung_L, ICOHP, ICOBI, mag, chg, Bader, GP')
    parser.add_argument('-a', '--all', action='store_true', default=False, help='Show all components')
    parser.add_argument('-r', '--ref', type=str, default='zero', help='Adjust values by subtracting the minimum')
    parser.add_argument('-n', '--norm', type=int, default=1, help='Normalization factor')
    parser.add_argument('--total', action='store_false', default=True, help='No show total energy')
    parser.add_argument('--save', action='store_true', default=False, help="save files")
    parser.add_argument('-s', '--separate', action='store_true', default=False, help="save the plots seperately")
    parser.add_argument('-i', '--input', dest='outcar', type=str, default='OUTCAR', help='input filename')
    parser.add_argument('-o', '--output', dest='filename', type=str, default='energy', help="output filename")
    parser.add_argument('-e', '--element', dest='symbols', nargs='+', default=[], help="elements of mag, chg, Bader")
    parser.add_argument('--line', action='store_true', default=False, help="plot 2d")
    parser.add_argument('--plane', action='store_true', default=False, help="plot 3d")
    parser.add_argument('-x', '--xlabel', type=str, default='Element or Lattice parameter (Å)', help="xlabel")
    parser.add_argument('-y', '--ylabel', type=str, default='Energy (eV) or Charge (e)', help="ylabel")

    return parser

def main():
    args = get_parser().parse_args()
    filename = args.filename.rsplit('.', 1)[0]
    xlabel = args.xlabel
    save = args.save
    if args.all:
        patterns = {'PSCENC', 'TEWEN', 'DENC', 'EXHF', 'XCENC', 'PAW_double_counting', 
                    'EENTRO', 'EBANDS', 'EATOM', 'TOTEN', 'Madelung', 'Madelung_M', 'Madelung_L',
                    'ICOHP', 'ICOBI', 'mag', 'chg', 'Bader', 'GP'}
    else:
        patterns = set(args.patterns)
    if 'Madelung' in patterns:
        patterns.discard('Madelung')
        patterns.update(['Madelung_Mulliken', 'Madelung_Loewdin'])
    if 'Madelung_M' in patterns:
        patterns.discard('Madelung_M')
        patterns.add('Madelung_Mulliken')
    if 'Madelung_L' in patterns:
        patterns.discard('Madelung_L')
        patterns.add('Madelung_Loewdin')
    if not args.total:
        patterns.discard('TOTEN')
    original_patterns = patterns.copy()

    directory='./'
    values_dict, dir_names, atoms = extract_values(directory, patterns, dir_range=args.dir_range, outcar=args.outcar)
    values_dict = selected_values(values_dict, args.symbols, atoms)
        
    values_dict = adjust_values(values_dict, ref=args.ref, norm=args.norm)
    if any(values_dict.values()):
        plot_merged(values_dict, dir_names, xlabel, save, filename, atoms)
        if args.separate:
            plot_separately(values_dict, dir_names, xlabel, save, filename)
    else:
        raise ValueError('No values found for the given patterns.')
    if args.line:
        line_fitting(original_patterns, values_dict, dir_names, xlabel, save, filename, atoms)
    elif args.plane:
        plane_fitting(original_patterns, values_dict, dir_names, xlabel, save, filename, atoms)

def extract_values(directory, patterns, dir_range, outcar):
    """Extract the last values for the given patterns from OUTCAR files in the given directories, sorted numerically."""
    pattern_map = {
        'PSCENC': r'alpha Z        PSCENC =\s+([0-9.-]+)',
        'TEWEN': r'Ewald energy   TEWEN  =\s+([0-9.-]+)',
        'DENC': r'-Hartree energ DENC   =\s+([0-9.-]+)',
        'EXHF': r'-exchange      EXHF   =\s+([0-9.-]+)',
        'XCENC': r'-V\(xc\)\+E\(xc\)   XCENC  =\s+([0-9.-]+)',
        'PAW_double_counting': r'PAW double counting   =\s+([0-9.-]+)\s+([0-9.-]+)',
        'EENTRO': r'entropy T\*S    EENTRO =\s+([0-9.-]+)',
        'EBANDS': r'eigenvalues    EBANDS =\s+([0-9.-]+)',
        'EATOM': r'atomic energy  EATOM  =\s+([0-9.-]+)',
        'Ediel_sol': r'Solvation  Ediel_sol  =\s+([0-9.-]+)',
        'TOTEN': r'free energy    TOTEN  =\s+([0-9.-]+)',
        'mag': r'\s*\d+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)',
        'chg': r'magnetization \(x\)',
    }
            
    values = {key: [] for key in patterns}  # Initialize dict to store values for each pattern
    dir_names = []
    
    specific_patterns = set()
    for pattern in ['Madelung_Mulliken', 'Madelung_Loewdin', 'Bader', 'ICOHP', 'ICOBI', 'GP']:
        if pattern in patterns:
            patterns.discard(pattern)
            specific_patterns.add(pattern)
            
    dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and '_' in d]
    
    if dir_range is not None:
        if ',' in dir_range:
            start_dir, end_dir = map(int, dir_range.split(','))
        else: 
            start_dir, end_dir = 1, int(dir_range)
        dir_nums = range(start_dir, end_dir + 1)
        dirs = [d for d in dirs if any(d.startswith(str(num)) for num in dir_nums)]
    dirs.sort(key=lambda x: [int(c) if c.isdigit() else c for c in re.split('(\d+)', x)])

    for dir_name in dirs:
        dir_path = os.path.join(directory, dir_name)
        trimmed_dir_name = dir_name.split('_')[1]
        dir_names.append(trimmed_dir_name)

        in_charge_section = False
        for poscar in ['POSCAR', 'CONTCAR', 'start.traj', 'restart.json']:
            poscar_path = os.path.join(dir_path, poscar)
            if os.path.exists(poscar_path):
                atoms = read(poscar_path)
                numb = atoms.get_global_number_of_atoms()
                break
        if not atoms:
            print('No atomic structure data..')
            exit()
        zvals =[]
        titels =[]
        potcar_path = os.path.join(dir_path, 'POTCAR')
        if os.path.exists(potcar_path):
            for line in open(potcar_path, 'r'):
                match_zval = re.search(r'POMASS\s*=\s*([0-9.]+);\s*ZVAL\s*=\s*([0-9.]+)', line)
                match_titel = re.search(r'TITEL  = PAW_PBE\s+([A-Za-z0-9_]+)\s+\d{2}[A-Za-z]{3}\d{4}', line)
                if match_zval:
                    zvals.append(float(match_zval.group(2)))
                if match_titel:
                    titels.append(match_titel.group(1).rsplit('_', 1)[0])
            zval_dict = dict(zip(titels, zvals))
            print(zval_dict)
                        
        if 'Madelung_Mulliken' in specific_patterns or 'Madelung_Loewdin' in specific_patterns:
            madelung_path = os.path.join(dir_path, 'MadelungEnergies.lobster')
            if os.path.exists(madelung_path):
                with open(madelung_path, 'r') as file:
                    lines = file.readlines()
                for line in reversed(lines):
                    match = re.search(r'\s*\d+\.\d+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)', line)
                    if match:
                        if 'Madelung_Mulliken' in specific_patterns:
                            values.setdefault('Madelung_Mulliken', []).append(float(match.group(1)))
                        if 'Madelung_Loewdin' in specific_patterns:
                            values.setdefault('Madelung_Loewdin', []).append(float(match.group(2)))
                        break
        if 'GP' in specific_patterns:
            i = numb - 1
            gp_path = os.path.join(dir_path, 'GROSSPOP.lobster')
            if os.path.exists(gp_path):
                for line in open(gp_path, 'r'):
                    match = re.search(r'\s*total\s+([0-9.]+)\s+([0-9.]+)', line)
                    if match:
                        symbol = atoms[i].symbol
                        zval = zval_dict[symbol]
                        values.setdefault('GP_Mulliken_'+symbol+str(i), []).append(zval-float(match.group(1)))
                        values.setdefault('GP_Loewdin_'+symbol+str(i), []).append(zval-float(match.group(2)))
                        if i != 0: i -= 1
                        else: break
        if 'Bader' in specific_patterns:
            i = numb - 1
            Bader_path = os.path.join(dir_path, 'ACF.dat')
            if not os.path.exists(Bader_path):
                subprocess.call('python ~/bin/verve/bader.py', shell=True, cwd=dir_path)
            if os.path.exists(Bader_path):
                with open(Bader_path, 'r') as file:
                    lines = file.readlines()
                for line in lines:
                    match = re.search(r'\s*\d+\s+([-]?\d+\.\d+)\s+([-]?\d+\.\d+)\s+([-]?\d+\.\d+)\s+([-]?\d+\.\d+)', line)
                    if match:
                        symbol = atoms[i].symbol
                        zval = zval_dict[symbol]
                        values.setdefault('Bader_'+symbol+str(i), []).append(zval-float(match.group(4)))
                        if i != 0: i -= 1
                        else: break
        if 'ICOHP' in specific_patterns:
            ICOHP_path = os.path.join(dir_path, 'icohp.txt')
            if not os.path.exists(ICOHP_path):
                subprocess.call('python ~/bin/playground/aloha/cohp.py > icohp.txt', shell=True, cwd=dir_path)
            if os.path.exists(ICOHP_path):
                for line in open(ICOHP_path, 'r'):
                    match = re.search(r'-ICOHP sum:(\s*)([0-9.]+)', line)
                    if match:
                        values.setdefault('ICOHP', []).append(-float(match.group(2)))
                        break
        if 'ICOBI' in specific_patterns:
            ICOBI_path = os.path.join(dir_path, 'icobi.txt')
            if not os.path.exists(ICOBI_path):
                subprocess.call('python ~/bin/playground/aloha/cobi.py > icobi.txt', shell=True, cwd=dir_path)
            if os.path.exists(ICOBI_path):
                for line in open(ICOBI_path, 'r'):
                    match = re.search(r'ICOBI avg:([0-9.]+)', line)
                    if match:
                        values.setdefault('ICOBI', []).append(float(match.group(1)))
                        break

        if patterns:
            outcar_path = os.path.join(dir_path, outcar)
            if os.path.exists(outcar_path) and patterns:
                with open(outcar_path, 'r') as file:
                    lines = file.readlines()
                for key in patterns:
                    i = numb - 1
                    pattern = re.compile(pattern_map[key])
                    for line in reversed(lines):
                        match = pattern.search(line)
                        if match:
                            if key == 'PAW_double_counting':
                                combined_value = sum(map(float, match.groups()))
                                values[key].append(combined_value)
                                break
                            elif key == 'mag':
                                symbol = atoms[i].symbol
                                values.setdefault('mag_'+symbol+str(i), []).append(float(match.group(4)))
                                if i != 0: i -= 1
                                else: break
                            elif key == 'chg' and not in_charge_section:
                                in_charge_section = True                                
                            else:
                                values[key].append(float(match.group(1)))
                                break
                        if key == 'chg' and in_charge_section:
                            symbol = atoms[i].symbol
                            zval = zval_dict[symbol]
                            match = re.compile(pattern_map['mag']).search(line)
                            if match:
                                values.setdefault('chg_'+symbol+str(i), []).append(zval-float(match.group(4)))
                                if i != 0: i -= 1
                                else: break
    
    return values, dir_names, atoms

def adjust_values(values_dict, ref, norm):
    """Subtract the reference value from each pattern's data set."""
    adjusted_values_dict = {}
    qualitative = ['PSCENC', 'TEWEN', 'DENC', 'EXHF', 'XCENC', 'PAW_double_counting',
                   'EENTRO', 'EBANDS', 'EATOM', 'TOTEN', 'Madelung_Mulliken', 'Madelung_Loewdin',
                   'ICOHP', 'ICOBI']
        
    for pattern, values in values_dict.items():
        if ref == 'min':
            ref_value = min(values)
        elif ref == 'max':
            ref_value = max(values)
        elif ref == 'mid':
            ref_value = np.median(values)
        elif ref.isdigit() and 0 <= int(ref) < len(values):
            ref_value = values[int(ref)-1]
        else:
            ref_value = 0
        adjusted_values = [(value - ref_value) / norm for value in values]
        adjusted_values_dict[pattern] = adjusted_values
    return adjusted_values_dict

def selected_values(values_dict, symbols, atoms):
    if not symbols:
        symbols = atoms.get_chemical_symbols()
    keys_to_remove = [
        'mag_' + atom.symbol + str(atom.index) 
        for atom in atoms 
        if atom.symbol not in symbols
    ] + [
        'chg_' + atom.symbol + str(atom.index) 
        for atom in atoms 
        if atom.symbol not in symbols
    ] + [
        'Bader_' + atom.symbol + str(atom.index) 
        for atom in atoms 
        if atom.symbol not in symbols
    ] + ['mag', 'chg', 'Bader', 'Madelung', 'GP']
    
    for key in keys_to_remove:
        if key in values_dict:
            del values_dict[key]
        
    return values_dict
        
def plot_separately(values_dict, dir_names, xlabel, save, filename):
    """Plot each pattern on its own graph."""
    x = np.arange(len(dir_names))
    
    for i, (pattern, values) in enumerate(values_dict.items()):
        if not values:
            print(f"No values found for pattern: {pattern}")
            continue
        plt.figure(figsize=(10, 6))
        plt.plot(x, values, marker='o', linestyle='-', label=pattern)
        
        plt.title(f'{pattern} Energy Contribution')
        plt.xlabel(xlabel)
        plt.ylabel('Energy (eV) or Charge')
        plt.xticks(x, dir_names, rotation='vertical')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        if save:
            png_filename = f"{filename}_{pattern}.png"
            tsv_filename = f"{filename}_{pattern}.tsv"
            
            plt.savefig(png_filename, bbox_inches="tight")
            plt.close()
            print(f"Figure saved as {png_filename}")

            with open(tsv_filename, "w") as f:
                header = "Dir_Name\tValues\n"
                f.write(header)
                for dir_name, value in zip(tsv_filename, values):
                    f.write(f"{dir_name}\t{value}\n")
            print(f"Data saved as {tsv_filename}")
        else:
            plt.show()

def plot_merged(values_dict, dir_names, xlabel, save, filename, atoms):
    plt.figure(figsize=(10, 6))

    patterns_order = ['PSCENC', 'TEWEN', 'DENC', 'EXHF', 'XCENC', 'PAW_double_counting', 
                      'EENTRO', 'EBANDS', 'EATOM', 'TOTEN', 'Madelung_Mulliken', 'Madelung_Loewdin', 
                      'ICOHP', 'ICOBI', 'GP_Mulliken', 'GP_Loewdin']
    patterns_order.extend(['mag_'+atom.symbol+str(atom.index) for atom in atoms])
    patterns_order.extend(['chg_'+atom.symbol+str(atom.index) for atom in atoms])
    patterns_order.extend(['Bader_'+atom.symbol+str(atom.index) for atom in atoms])
    filtered_patterns_order = [pattern for pattern in patterns_order if values_dict.get(pattern)]

    colors = plt.cm.turbo(np.linspace(0, 1, len(filtered_patterns_order))) 
    # viridis, magma, plasma, inferno, cividis, mako, rocket, turbo
    
    for pattern, color in zip(filtered_patterns_order, colors):
        values = values_dict.get(pattern, [])
        if all(isinstance(v, tuple) for v in values):
            values = [v[0] for v in values]
        if not values:
            print(f"No values found for pattern: {pattern}")
            continue
        plt.plot(values, marker='o', linestyle='-', label=pattern, color=color)
    
    plt.title('Energy Contribution')
    plt.xlabel(xlabel)
    plt.ylabel('Energy (eV) or Charge')
    plt.xticks(np.arange(len(dir_names)), dir_names, rotation='vertical')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    if save:
        png_filename = f"{filename}.png"
        tsv_filename = f"{filename}.tsv"
        
        plt.gcf().savefig(filename, bbox_inches="tight")
        print(f"Figure saved as {png_filename}")
        plt.close()
        
        with open(tsv_filename, "w") as f:
            header = "Pattern\t" + "\t".join(dir_names) + "\n"
            f.write(header)
            for pattern in filtered_patterns_order:
                line = pattern + "\t" + "\t".join(map(str, values_dict[pattern])) + "\n"
                f.write(line)
        print(f"Data saved as {tsv_filename}")
    else:
        plt.show()
        
def line_fitting(patterns, values_dict, dir_names, xlabel, save, filename, atoms):
    patterns_order = list(patterns)
    patterns_order.extend(['mag_'+atom.symbol+str(atom.index) for atom in atoms])
    patterns_order.extend(['chg_'+atom.symbol+str(atom.index) for atom in atoms])
    patterns_order.extend(['Bader_'+atom.symbol+str(atom.index) for atom in atoms])
    filtered_patterns_order = [pattern for pattern in patterns_order \
                               if values_dict.get(pattern)]

    if len(filtered_patterns_order) < 2:
        raise ValueError("Not enough valid patterns with data for line fitting.")
    
    X = np.array(values_dict[filtered_patterns_order[0]])
    Y = np.array(values_dict[filtered_patterns_order[1]])

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
    plt.xlabel('X')
    plt.ylabel('Y')
    
    if save:
        png_filename = f"{filename}_2d.png"
        plt.savefig(png_filename, bbox_inches="tight")
        print(f"Figure saved as {png_filename}")
        plt.close()
    else:
        plt.show()
        
def plane_fitting(patterns, values_dict, dir_names, xlabel, save, filename, atoms):
    patterns_order = list(patterns)
    patterns_order.extend(['mag_'+atom.symbol+str(atom.index) for atom in atoms])
    patterns_order.extend(['chg_'+atom.symbol+str(atom.index) for atom in atoms])
    patterns_order.extend(['Bader_'+atom.symbol+str(atom.index) for atom in atoms])
    filtered_patterns_order = [pattern for pattern in patterns_order if values_dict.get(pattern)]

    if len(filtered_patterns_order) < 3:
        raise ValueError("Not enough valid patterns with data for plane fitting.")
    
    X = np.array(values_dict[filtered_patterns_order[0]])
    Y = np.array(values_dict[filtered_patterns_order[1]])
    Z = np.array(values_dict[filtered_patterns_order[2]])
    
    A = np.vstack([X, Y, np.ones(len(X))]).T
    coeffs, residuals, rank, s = np.linalg.lstsq(A, Z, rcond=None)
    a, b, c = coeffs
    Z_pred = a*X + b*Y + c

    R2 = r2_score(Z, Z_pred)
    MAE = mean_absolute_error(Z, Z_pred)
    MSE = mean_squared_error(Z, Z_pred)

    print(f"Z = {a:.3f}X + {b:.3f}Y + {c:.3f}")
    print(f"R^2: {R2:.3f}, MAE: {MAE:.3f}, MSE: {MSE:.3f}")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(X, Y, Z, color='r')
    xx, yy = np.meshgrid(np.linspace(np.min(X), np.max(X), 10), 
                         np.linspace(np.min(Y), np.max(Y), 10))
    zz = a * xx + b * yy + c
    
    ax.plot_surface(xx, yy, zz, color='b', alpha=0.5, edgecolor='none')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    if save:
        png_filename = f"{filename}_2d.png"
        plt.gcf().savefig(png_filename, bbox_inches="tight")
        print(f"Figure saved as {png_filename}")
    else:
        plt.show()
    
if __name__ == '__main__':
    main()

