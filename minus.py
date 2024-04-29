import pandas as pd
import sys

def process_files(add_files, subtract_files, output_filename):
    # Start with the first file in the addition list
    df_result = pd.read_csv(add_files[0], delimiter='\t')

    # Add all subsequent files in the addition list
    for filename in add_files[1:]:
        df = pd.read_csv(filename, delimiter='\t')
        df_result += df

    # Subtract all files in the subtraction list
    for filename in subtract_files:
        df = pd.read_csv(filename, delimiter='\t')
        df_result -= df

    # Save the result to a specified output TSV file
    df_result.to_csv(output_filename, index=False, sep='\t')

def main():
    if len(sys.argv) < 2:
        print("Usage: python code.py -plus a.tsv b.tsv -minus c.tsv d.tsv [-o output.tsv]")
        sys.exit()

    args = sys.argv[1:]
    plus_files = []
    minus_files = []
    output_filename = "output.tsv"  # default output filename

    # Initialize flags for parsing
    in_plus_section = False
    in_minus_section = False

    # Iterate over command-line arguments to sort files and options
    for arg in args:
        if arg == "-plus":
            in_plus_section = True
            in_minus_section = False
        elif arg == "-minus":
            in_plus_section = False
            in_minus_section = True
        elif arg in ("-o", "--output"):
            output_index = args.index(arg) + 1
            output_filename = args[output_index]
        elif in_plus_section:
            plus_files.append(arg)
        elif in_minus_section:
            minus_files.append(arg)

    # Process the files
    process_files(plus_files, minus_files, output_filename)

if __name__ == "__main__":
    main()
