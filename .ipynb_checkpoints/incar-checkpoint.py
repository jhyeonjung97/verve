import argparse

# Your existing import statements and code here...

def modify_parameters(tag_to_modify, new_value):
    if tag_to_modify in locals():
        locals()[tag_to_modify] = new_value
    else:
        with open('opt_bulk.py', 'a') as f:
            f.write(f"{tag_to_modify} = {new_value}\n")

def main():
    parser = argparse.ArgumentParser(description='Modify or add VASP calculation parameters in opt_bulk.py')
    parser.add_argument('tag', type=str, help='Parameter tag to modify or add')
    parser.add_argument('value', type=str, help='Value to set for the parameter')

    args = parser.parse_args()

    tag_to_modify = args.tag
    new_value = args.value

    modify_parameters(tag_to_modify, new_value)

    # Your existing code to create 'calc' instance...

if __name__ == "__main__":
    main()
