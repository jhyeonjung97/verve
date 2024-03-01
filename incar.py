import argparse

def main():
    parser = argparse.ArgumentParser(description='Modify VASP calculation parameters in opt_bulk.py')
    parser.add_argument('tag', type=str, help='Parameter tag to modify')
    parser.add_argument('value', type=str, help='Value to set for the parameter')

    args = parser.parse_args()

    tag_to_modify = args.tag
    new_value = args.value

    if tag_to_modify not in locals():
        print(f"Error: Tag '{tag_to_modify}' not found in opt_bulk.py.")
        return

    locals()[tag_to_modify] = new_value

    # Your existing code to create 'calc' instance...

if __name__ == "__main__":
    main()