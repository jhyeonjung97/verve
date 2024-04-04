#!/bin/bash

function usage_error {
    echo "Usage: $0 [-h] [-r] [-c cut] -n jobname [startDir] [endDir]"
    exit 1
}

cut=1
while getopts ":hrcs:d:" opt; do
    case ${opt} in
        h )
            usage_error
            ;;
        r)
          dir_tag=1
          ;;
        c )
            cut=2
            ;;
        s)
          select="$OPTARG"
          ;;
        d)
          set="$OPTARG"
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

if [ "$opt" = "h" ]; then
    echo "Usage: $0 [-h] [-r] [-c cut] -n jobname [startDir] [endDir]"
    echo "Options:"
    echo "  -h          Display this help message."
    echo "  -r          Use a recursive directory pattern."
    echo "  -c          Set the cut length for the directory name modification."
    echo "  -s select   Select specific directories."
    echo "  -d set      Specify a range of directories."
    exit 0
fi

if [[ -z $1 ]]; then
    echo "Job name is required."
    usage_error
else
    name=$1
fi

DIR=''
if [[ -n $select ]]; then
    DIR=$(find . -type d -path "$select")
elif [[ -n $range ]]; then
    IFS=',' read -r -a range_arr <<< "$range"
    DIR=$(seq "${range_arr[0]}" "${range_arr[1]}")
elif [[ $dir_tag = 1 ]]; then
    DIR='*_*/'
fi

if [[ -n $DIR ]]; then
    for dir in $DIR
    do
        dir=${dir%/}
        i=${dir:0:$cut}
        sed -i "/#SBATCH -J/c\#SBATCH -J ${name}$i" "$dir/submit.sh"
    done
    grep '#SBATCH -J' "$dir/submit.sh"
else
    sed -i "/#SBATCH -J/c\#SBATCH -J $name" submit.sh
    grep '#SBATCH -J' submit.sh
    exit 0
fi
