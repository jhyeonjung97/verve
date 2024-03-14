def remove_lines_before_pattern(file_path, pattern):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    pattern_found = False
    new_lines = []
    for line in lines:
        if pattern_found:
            new_lines.append(line)
        elif pattern in line:
            pattern_found = True

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

# Example usage:
file_path = 'vasp.out'
pattern = 'MAGMOM'
remove_lines_before_pattern(file_path, pattern)
