def remove_lines(filename, num_lines=2, pattern='-'*80):
    with open(filename, 'r') as file:
        lines = file.readlines()

    count = 0
    new_lines = []
    for line in lines:
        if line.strip() == pattern and count < num_lines:
            count += 1
        else:
            new_lines.append(line)

    with open(filename, 'w') as file:
        file.writelines(new_lines)

# Replace 'filename.txt' with the path to your file
remove_lines('vasp.out')