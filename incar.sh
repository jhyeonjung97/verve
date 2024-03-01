#!/bin/bash

function usage_error {
    echo 'Usage: incar.sh [filename] [pattern] [value]'
    exit 1
}

if [[ -z $1 || -z $2 || -z $3 ]]; then
    usage_error
fi

filename=$1
pattern=$2
value=$3

# Check if the file exists
if [[ ! -f $filename ]]; then
    echo "Error: File '$filename' not found."
    exit 1
fi

# Update the file with the specified pattern=value

if [[ -n $(grep $pattern $filename) ]]; then
    sed -i "/calc = vasp_calculator.Vasp(/a\    $pattern=" "$filename"
fi

sed -i "s/$pattern=.*/$pattern=$value/" $filename
sed -i "/calc = vasp_calculator.Vasp(/a\    $text_to_add" "$file"
echo "Pattern '$pattern' updated to '$pattern=$value' in '$filename'."