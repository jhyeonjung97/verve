#!/bin/bash

function usage_error {
    echo 'Usage: sub.sh [-r | -s dir]'
    exit 1
}

if [[ $1 == '-h' || $1 == '--help' || -z $1 ]]; then
    usage_error
fi

if [[ -z $1 ]]; then
    sbatch submit.sh
    exit 0
else
    if [[ $1 == '-r' ]]; then
        DIR='*/'
    elif [[ $1 == '-s' && -n $2 ]]; then
        DIR=$2
    else
        DIR=$(seq ${1:-1} ${2:-$1})
    fi
fi

for i in $DIR
do
    i=${i%/}
    cd $i* && sbatch submit.sh && cd ..
done
