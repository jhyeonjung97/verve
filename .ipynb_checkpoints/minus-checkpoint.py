import pandas as pd
import sys

def process_files(add_files, subtract_files):
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

    # Save the result to a new TSV file
    df_result.to_csv("output.tsv", index=False, sep='\t')

def main():
    if len(sys.argv) < 2:
        print("Usage: python code.py -plus a.tsv b.tsv -minus c.tsv d.tsv")
        sys.exit()

    # Split the argument list at "-plus" and "-minus"
    args = sys.argv[1:]
    if "-plus" in args:
        plus_index = args.index("-plus") + 1
    else:
        plus_index = None

    if "-minus" in args:
        minus_index = args.index("-minus") + 1
    else:
        minus_index = None

    # Get the lists of filenames for addition and subtraction
    if plus_index and minus_index:
        if plus_index < minus_index:
            add_files = args[plus_index:minus_index-1]
            subtract_files = args[minus_index:]
        else:
            subtract_files = args[minus_index:plus_index-1]
            add_files = args[plus_index:]
    elif plus_index:
        add_files = args[plus_index:]
        subtract_files = []
    elif minus_index:
        subtract_files = args[minus_index:]
        add_files = []
    else:
        print("Invalid command line arguments")
        sys.exit()

    # Process the files
    process_files(add_files, subtract_files)

if __name__ == "__main__":
    main()