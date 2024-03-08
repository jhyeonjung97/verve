import argparse
from ase.io import read, write
from os import path

def main():
    parser = argparse.ArgumentParser(description='Command-line options example')

    parser.add_argument('-r', '--ratio', action='store_true', default=False, help='use ratio for scaling')
    parser.add_argument('-f', '--factor', type=float, default=1.0, help='scaling factor or fixed size')
    parser.add_argument('-o', '--output', type=str, default=None, help='the name of output file')

    args = parser.parse_args()

    if path.exists('restart.json'):
        atoms = read('restart.json')
        write('original.traj', atoms)
    elif path.exists('CONTCAR'):
        atoms = read('CONTCAR')
        write('original.traj', atoms)
    elif path.exists('start.traj'):
        atoms = read('start.traj')
        write('original.traj', atoms)
        
    factor = args.factor
    if not args.ratio:
        factor = (atoms.cell[0][0] + factor) / atoms.cell[0][0]

    atoms.set_cell(atoms.get_cell() * factor, scale_atoms=True)

    # Overwrite the original file with the modified atoms object
    if args.output is None:
        write('start.traj', atoms)
    else:
        write(args.output, atoms)

if __name__ == "__main__":
    main()