import itertools

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
        # 90-degree rotations around x-axis
        [0, 1, 5, 4, 3, 2, 6, 7], [0, 1, 6, 7, 4, 5, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7],
        # 90-degree rotations around y-axis
        [4, 0, 3, 7, 5, 1, 2, 6], [1, 5, 6, 2, 0, 4, 7, 3], [4, 5, 6, 7, 0, 1, 2, 3],
        # 90-degree rotations around z-axis
        [1, 2, 6, 5, 0, 3, 7, 4], [3, 2, 6, 7, 0, 1, 5, 4], [0, 3, 7, 4, 1, 2, 6, 5]
    ]
    
    # Define the indices for each reflection
    reflection_indices = [
        # Reflections across the xy-plane
        [4, 5, 6, 7, 0, 1, 2, 3],
        # Reflections across the yz-plane
        [1, 0, 3, 2, 5, 4, 7, 6],
        # Reflections across the xz-plane
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

# Filter combinations to ensure minimal duplicates and no neighboring duplicates
def has_minimal_duplicates(combination):
    counts = {metal: combination.count(metal) for metal in metals}
    return all(count <= 2 for count in counts.values())

filtered_combinations = []
seen_combinations = set()

for comb in combinations:
    if (has_minimal_duplicates(comb) and has_no_neighbor_duplicates(comb) and 
        has_valid_facets(comb)):
        symmetries = generate_symmetries(comb)
        valid = True
        if any(sym in seen_combinations for sym in symmetries):
            valid = False
        if valid:
            filtered_combinations.append(comb)
            seen_combinations.update(symmetries)

# Print the filtered combinations
print("Filtered combinations:")
for comb in filtered_combinations:
    print(comb)
    
# You can also check the total number of filtered combinations
print(f"Total number of valid combinations: {len(filtered_combinations)}")