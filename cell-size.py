import argparse
from ase.io import read, write
from os import path

def main():
    parser = argparse.ArgumentParser(description='Command-line options example')

    parser.add_argument('-r', '--ratio', action='store_true', default=True, help='use ratio for scaling')
    parser.add_argument('factor', type=float, default=1.0, help='scaling factor or fixed size')

    args = parser.parse_args()

    ratio = args.ratio
    factor = args.factor

    if path.exists('restart.json'):
        atoms = read('restart.json')
        write('original.json', atoms)
    else:
        atoms = read('start.traj')
        write('original.traj', atoms)

    if not ratio:
        factor = (atoms.cell[0][0] + factor) / atoms.cell[0][0]

    atoms.set_cell(atoms.get_cell() * factor, scale_atoms=True)

    # Overwrite the original file with the modified atoms object
    write('start.traj', atoms)

if __name__ == "__main__":
    main()