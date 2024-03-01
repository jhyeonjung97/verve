#!/bin/bash

function usage_error {
    echo 'Usage: name_slurm.sh (-r) [jobname] [dir#1] [dir#2]'
    exit 1
}

if [[ $1 == '-h' ]] || [[ -z $1 ]]; then
    usage_error
fi

if [[ -z $2 ]]; then
    name=$1
    sed -i "/#SBATCH -J/c\#SBATCH -J $name" submit.sh
    if [[ -f lobster.sh ]]; then
        sed -i "/#SBATCH -J/c\#SBATCH -J $name" lobster.sh
    fi
    exit 0
elif [[ $1 == '-r' ]]; then
    name=$2
    DIR='*/'
elif [[ -z $3 ]]; then
    name=$2
    DIR=$(seq 1 $1)
else
    name=$3
    DIR=$(seq $1 $2)
fi
exit 1
# loop
for i in $DIR
do
    i=${i%/}
    j=$(echo $i | cut -c 1)
    sed -i "/#SBATCH -J/c\#SBATCH -J $name$j" $i/submit.sh
done
grep '#SBATCH -J' */submit.sh
