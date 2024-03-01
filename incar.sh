#!/bin/bash

function usage_error {
    echo 'Usage: incar.sh [filename] [pattern] [value]'
    exit 1
}

if [[ -z $1 || -z $2 ]]; then
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

# Delete the pattern if value is empty
if [[ -z $value ]]; then
    sed -i "/$pattern=.*/d" $filename
    echo "'$pattern' is deleted from '$filename'."
    exit 0
fi

# Update the file with the specified pattern=value
sed -i "s/\($pattern\s*=\s*\).*/\1$value/" $filename
echo "'$pattern' updated to '$pattern=$value' in '$filename'."