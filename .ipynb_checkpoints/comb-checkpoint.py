import itertools
from ase.io import read, write

# Path to your POSCAR file
poscar_path = 'POSCAR'

# Define the metals
metals = ['Cr', 'Mn', 'Fe', 'Co', 'Ni']

# Generate all possible 2x2x2 combinations
combinations = list(itertools.product(metals, repeat=8))

# Function to generate all possible rotations and reflections of a combination
def generate_symmetries(comb):
    symmetries = set()
    comb = list(comb)
    
    # Original combination
    symmetries.add(tuple(comb))
    
    # Define the indices for each rotation
    rotation_indices = [
        [0, 1, 5, 4, 3, 2, 6, 7], [0, 1, 6, 7, 4, 5, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7],
        [4, 0, 3, 7, 5, 1, 2, 6], [1, 5, 6, 2, 0, 4, 7, 3], [4, 5, 6, 7, 0, 1, 2, 3],
        [1, 2, 6, 5, 0, 3, 7, 4], [3, 2, 6, 7, 0, 1, 5, 4], [0, 3, 7, 4, 1, 2, 6, 5]
    ]
    
    # Define the indices for each reflection
    reflection_indices = [
        [4, 5, 6, 7, 0, 1, 2, 3],
        [1, 0, 3, 2, 5, 4, 7, 6],
        [2, 3, 0, 1, 6, 7, 4, 5]
    ]
    
    for indices in rotation_indices:
        rotated_comb = [comb[i] for i in indices]
        symmetries.add(tuple(rotated_comb))
        for ref_indices in reflection_indices:
            reflected_comb = [rotated_comb[i] for i in ref_indices]
            symmetries.add(tuple(reflected_comb))
    
    return symmetries

# Function to check if any two neighboring elements are the same
def has_no_neighbor_duplicates(comb):
    neighbors = [
        (0, 1), (0, 2), (0, 4),
        (1, 3), (1, 5),
        (2, 3), (2, 6),
        (3, 7),
        (4, 5), (4, 6),
        (5, 7),
        (6, 7)
    ]
    return all(comb[i] != comb[j] for i, j in neighbors)

# Function to check if any facet consists of only two unique elements
def has_valid_facets(comb):
    facets = [
        [comb[0], comb[1], comb[2], comb[3]], # Front face
        [comb[4], comb[5], comb[6], comb[7]], # Back face
        [comb[0], comb[1], comb[4], comb[5]], # Top face
        [comb[2], comb[3], comb[6], comb[7]], # Bottom face
        [comb[0], comb[2], comb[4], comb[6]], # Left face
        [comb[1], comb[3], comb[5], comb[7]]  # Right face
    ]
    return all(len(set(facet)) >= 3 for facet in facets)

# Function to check if any facet has the same element located diagonally
def has_no_diagonal_duplicates(comb):
    diagonals = [
        (0, 3), (1, 2), (4, 7), (5, 6), # Front and Back faces
        (0, 5), (1, 4), (2, 7), (3, 6), # Top and Bottom faces
        (0, 6), (1, 7), (2, 4), (3, 5)  # Left and Right faces
    ]
    return all(comb[i] != comb[j] for i, j in diagonals)

# Filter combinations to ensure minimal duplicates and no neighboring duplicates
def has_minimal_duplicates(combination):
    counts = {metal: combination.count(metal) for metal in metals}
    return all(count <= 2 for count in counts.values())

# Check if a combination contains the specific subset
def contains_specific_subset(comb, subset):
    comb_counts = {metal: comb.count(metal) for metal in metals}
    subset_counts = {metal: subset.count(metal) for metal in subset}
    return all(comb_counts[metal] >= subset_counts[metal] for metal in subset_counts)

filtered_combinations = []
seen_combinations = set()
specific_combinations = []

subset = ['Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cr', 'Mn', 'Fe']

for comb in combinations:
    if (has_minimal_duplicates(comb) and has_no_neighbor_duplicates(comb) and 
        has_valid_facets(comb) and has_no_diagonal_duplicates(comb)):
        symmetries = generate_symmetries(comb)
        valid = not any(sym in seen_combinations for sym in symmetries)
        if valid:
            filtered_combinations.append(comb)
            seen_combinations.update(symmetries)
            if contains_specific_subset(comb, subset):
                specific_combinations.append(comb)

for numb, comb in enumerate(filtered_combinations):
    # Format filename with leading zero for single-digit numbers
    filename = f"{numb:02d}.vasp"
    
    # Read atomic structure from POSCAR file
    try:
        atoms = read(poscar_path)
    except Exception as e:
        print(f"Error reading POSCAR file: {e}")
        continue
    
    # Modify atomic symbols based on the combination
    try:
        for i in range(8,16):
            atoms[i].symbol = comb[i]
    except IndexError as e:
        print(f"Error updating atomic symbols: {e}")
        continue
    
    # Write the modified structure to a new file
    try:
        write(filename, atoms)
        print(f"Written: {filename}")
    except Exception as e:
        print(f"Error writing {filename}: {e}")

print("Finished processing all combinations.")
    
# # Print the filtered combinations
# print("Filtered combinations:")
#     print(comb)

# # Print the specific combinations
# print("\nCombinations that include ['Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cr', 'Mn', 'Fe']:")
# for comb in specific_combinations:
#     print(comb)

# # Print the number of specific combinations
# print(f"\nTotal number of specific combinations: {len(specific_combinations)}")

# You can also check the total number of filtered combinations
print(f"Total number of valid combinations: {len(filtered_combinations)}")
