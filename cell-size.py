import argparse
from ase.io import read, write
from os import path

def main():
    parser = argparse.ArgumentParser(description='Command-line options example')

    parser.add_argument('-i', '--input', type=str, required=True, help='input file name (json or traj)')
    parser.add_argument('-r', '--ratio', action='store_true', default=False, help='use ratio for scaling')
    parser.add_argument('-f', '--factor', type=float, default=1.0, help='scaling factor or fixed size')
    parser.add_argument('-o', '--output', type=str, default=None, help='the name of output file')

    args = parser.parse_args()

    input_file = args.input

    if not path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    file_ext = path.splitext(input_file)[1]

    if file_ext == '.json' or file_ext == '.traj':
        atoms = read(input_file)
    else:
        print("Error: Unsupported file format. Please provide a JSON or Trajectory file.")
        return

    magmoms = None
    if 'magmom' in atoms.arrays:
        magmoms = atoms.get_initial_magnetic_moments().copy()

    factor = args.factor
    if not args.ratio:
        factor = (atoms.cell[0][0] + factor) / atoms.cell[0][0]

    atoms.set_cell(atoms.get_cell() * factor, scale_atoms=True)

    # Overwrite the original file with the modified atoms object
    if args.output:
        output_file = args.output
    elif file_ext == '.json':
        output_file = 'restart.json'
    else:
        output_file = 'start.traj'
    write(output_file, atoms)

if __name__ == "__main__":
    main()