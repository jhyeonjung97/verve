#!/bin/bash

function usage_error {
    echo "Usage: $0 [-h] [-r] [-c cut] -n jobname [startDir] [endDir]"
    exit 1
}

cut=1
while getopts ":hrs:d:c:" opt; do
    case ${opt} in
        h )
            usage_error
            ;;
        r)
          dir_tag=1
          ;;
        s)
          select="$OPTARG"
          ;;
        d)
          set="$OPTARG"
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

if [[ -z $1 ]]; then
    echo "Job name is required."
    usage_error
else
    name=$1
fi

if [[ -n $select_dir ]]; then
    DIR="$select_dir"
elif [[ -n $range ]]; then
    IFS=',' read -r -a range_arr <<< "$range"
    DIR=$(seq "${range_arr[0]}" "${range_arr[1]}")
elif [[ $dir_tag = 1 ]]; then
    DIR='*/'
fi

if [[ -n $DIR ]]; then
    for dir in $DIR
    do
        dir=${dir%/}
        i=${dir:0:$cut}
        sed -i "/#SBATCH -J/c\#SBATCH -J ${name}$i" "$dir/submit.sh"
    done
    grep '#SBATCH -J' */submit.sh
else
    sed -i "/#SBATCH -J/c\#SBATCH -J $name" submit.sh
    grep '#SBATCH -J' submit.sh
    exit 0
fi
