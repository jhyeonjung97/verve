import argparse
from ase.io import read, write
from os import path
import json
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='Scale the cell size of JSON or Trajectory files')

    parser.add_argument('-i', '--input', type=str, required=True, help='input file name (JSON or Trajectory)')
    parser.add_argument('-r', '--is-ratio', action='store_true', default=False, help='use ratio for scaling')
    parser.add_argument('-f', '--factor', type=float, default=1.0, help='scaling factor or fixed size')
    parser.add_argument('-o', '--output', type=str, default=None, help='the name of output file')

    args = parser.parse_args()

    input_file = args.input
    if not path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    file_ext = path.splitext(input_file)[1]
    
    output_file = args.output or default_output_file(input_file, file_ext)

    if file_ext == '.json':
        json_cell_size(input_file, output_file, args.factor, args.is_ratio)
    elif file_ext == '.traj':
        traj_cell_size(input_file, output_file, args.factor, args.is_ratio)
    else:
        print("Error: Unsupported file format. Please provide a JSON or Trajectory file.")
        return

def default_output_file(input_file, file_ext):
    base_name = path.splitext(path.basename(input_file))[0]
    if file_ext == '.json':
        return f'{base_name}_scaled.json'
    else:
        return f'{base_name}_scaled.traj'

def traj_cell_size(input_file, output_file, scaling_factor, is_ratio):
    atoms = read(input_file)
    if not is_ratio:
        scaling_factor = (atoms.cell[0][0] + scaling_factor) / atoms.cell[0][0]
    atoms.set_cell(atoms.get_cell() * scaling_factor, scale_atoms=True)
    write(output_file, atoms)
    print(f"Cell size scaled by a factor of {scaling_factor} and saved to {output_file}")

def json_cell_size(input_file, output_file, scaling_factor, is_ratio):
    with open(input_file, 'r') as f:
        atoms = json.load(f)

    cell_array = atoms['1']['cell']['array']['__ndarray__'][2]
    cell_matrix = np.reshape(cell_array, (3, 3))

    if not is_ratio:
        scaling_factor = (cell_matrix[0][0] + scaling_factor) / cell_matrix[0][0]
    scaled_cell_matrix = cell_matrix * scaling_factor

    scaled_cell_array = scaled_cell_matrix.flatten().tolist()
    atoms['1']['cell']['array']['__ndarray__'][2] = scaled_cell_array

    with open(output_file, 'w') as f:
        json.dump(atoms, f, indent=4)

    print(f"Cell size scaled by a factor of {scaling_factor} and saved to {output_file}")

if __name__ == "__main__":
    main()