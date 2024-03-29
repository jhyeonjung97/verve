#!/bin/bash

function usage_error {
    echo 'Usage: sub.sh [-r | -s dir]'
    exit 1
}

if [[ -z $1 ]]; then
    if [[ -s submit.sh ]]; then
        sbatch submit.sh
    fi
    exit 0
elif [[ $1 == '-r' ]]; then
    DIR='*_*/'
elif [[ $1 == '-s' ]]; then
    DIR=${2:@}
elif [[ -z $2 ]]; then
    DIR=$(seq 1 $1)
else
    DIR=$(seq $1 $2)
fi

for i in $DIR
do
    i=${i%/}
    cd $i*
    if [[ -s submit.sh ]]; then
        sbatch submit.sh
    fi
    cd ..
done
