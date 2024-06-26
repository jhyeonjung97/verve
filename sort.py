import os

def read_poscar(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    header = lines[:7]
    atomic_symbols = header[5].split()
    atomic_counts = list(map(int, header[6].split()))
    
    atom_positions = lines[8:8 + sum(atomic_counts)]
    
    return header, atomic_symbols, atomic_counts, atom_positions

def write_poscar(file_path, header, atomic_symbols, atomic_counts, atom_positions):
    with open(file_path, 'w') as file:
        file.writelines(header[:5])
        file.write(' '.join(atomic_symbols) + '\n')
        file.write(' '.join(map(str, atomic_counts)) + '\n')
        file.writelines(header[7])
        file.writelines(atom_positions)

def sort_atoms(atomic_symbols, atomic_counts, atom_positions):
    metal_positions = []
    oxygen_positions = []
    
    index = 0
    for symbol, count in zip(atomic_symbols, atomic_counts):
        positions = atom_positions[index:index + count]
        if symbol == 'O':
            oxygen_positions.extend(positions)
        else:
            metal_positions.extend(positions)
        index += count
    
    sorted_positions = metal_positions + oxygen_positions
    
    sorted_symbols = [symbol for symbol in atomic_symbols if symbol != 'O'] + ['O']
    sorted_counts = [count for symbol, count in zip(atomic_symbols, atomic_counts) if symbol != 'O'] + [atomic_counts[atomic_symbols.index('O')]]
    
    return sorted_symbols, sorted_counts, sorted_positions

def main(input_file, output_file):
    header, atomic_symbols, atomic_counts, atom_positions = read_poscar(input_file)
    
    sorted_symbols, sorted_counts, sorted_positions = sort_atoms(atomic_symbols, atomic_counts, atom_positions)
    
    write_poscar(output_file, header, sorted_symbols, sorted_counts, sorted_positions)
    print(f"Sorted POSCAR file has been saved as {output_file}")

if __name__ == "__main__":
    input_file = 'POSCAR'  # Replace with your input file name
    output_file = 'POSCAR_sorted'  # Replace with your desired output file name
    main(input_file, output_file)