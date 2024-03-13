#!/bin/bash

function usage_error {
    echo "Usage: $0 [-h] [-r] [-n jobname] [startDir] [endDir]"
    exit 1
}

# Initialize variables
cut=1
rename=false
startDir=""
endDir=""
DIR=""

# Process options
while getopts ":hr:c:" opt; do
    case ${opt} in
        h )
            usage_error
            ;;
        r )
            rename=true
            ;;
        c )
            cut="$OPTARG"
            ;;
        \? )
            echo "Invalid Option: -$OPTARG" 1>&2
            usage_error
            ;;
        : )
            echo "Invalid option: $OPTARG requires an argument" 1>&2
            usage_error
            ;;
    esac
done
shift $((OPTIND -1))
name=$1

# Additional argument handling
if [[ -z $name ]]; then
    echo "Job name is required."
    usage_error
fi

if $rename; then
    if [[ $# -eq 0 ]]; then
        DIR='*/'
    elif [[ $# -eq 2 ]]; then
        startDir=$1
        endDir=$2
        DIR=$(seq $startDir $endDir)
    else
        echo "Incorrect number of directories specified."
        usage_error
    fi
else
    sed -i "/#SBATCH -J/c\#SBATCH -J $name" submit.sh
    grep '#SBATCH -J' submit.sh
    exit 0
fi

# Loop through directories and rename
for i in $DIR
do
    i=${i%/} # Remove trailing slash if present
    j=$(echo $i | cut -c $cut)
    sed -i "/#SBATCH -J/c\#SBATCH -J ${name}$j" "$i/submit.sh"
done

grep '#SBATCH -J' */submit.sh
