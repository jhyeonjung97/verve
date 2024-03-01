#!/bin/bash

function usage_error {
    echo 'Usage: name_slurm.sh (-r) [jobname] [dir#1] [dir#2]'
    exit 1
}

if [[ $1 == '-h' ]] || [[ -z $1 ]]; then
    usage_error
fi

name=$2
if [[ -z $name ]]; then
    sed -i "/#SBATCH -J/c\#SBATCH -J $name" submit.sh
    if [[ -f lobster.sh ]]; then
        sed -i "/#SBATCH -J/c\#SBATCH -J $name" lobster.sh
    fi
    exit 0
elif [[ $1 == '-r' ]]; then
    if [[ -z $4 ]]; then
        SET=$(seq 1 $3)
    elif [[ -z $5 ]]; then
        SET=$(seq $3 $4)
    else
        usage_error
    fi
else
    name=$1
    SET=$(seq 1 $2)
fi

# loop
for i in $SET
do
    i=${i%/}
    j=$(echo $i | cut -c 1)
    sed -i "/#SBATCH -J/c\#SBATCH -J $name$j" $i/submit.sh
done
grep '#SBATCH -J' */submit.sh
