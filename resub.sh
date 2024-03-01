#!/bin/bash

function usage_error {
    echo 'Usage: resub.sh [-r | -s dir]'
    exit 1
}

if [[ -z $1 ]]; then
    rm STD*
    sbatch submit.sh
    exit 0
else
    if [[ $1 == '-r' ]]; then
        DIR='*/'
    elif [[ $1 == '-s' && -n $2 ]]; then
        DIR=$2
    elif [[ -n $2 ]]; then
        DIR=$(seq $1 $2)
    else
        DIR=$(seq 1 $1)
    fi
fi

for i in $DIR
do
    i=${i%/}
    cd $i*
    rm STD*
    sbatch submit.sh
    cd ..
done
