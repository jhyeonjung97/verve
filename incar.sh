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

sed -i "s/#$pattern/$pattern/g" $filename
sed -i "s/# $pattern/$pattern/g" $filename

if [[ -z $value ]]; then
    sed -i "s/$pattern/# $pattern/g" $filename
else
    sed -i "s/\($pattern\s*=\s*\).*/\1$value,/" $filename

fi

echo "'$pattern' updated to '$pattern=$value' in '$filename'."