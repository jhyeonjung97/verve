#!/bin/bash

function usage_error {
    echo 'Usage: name (-r) [jobname] [dir#1] [dir#2]'
    exit 1
}

if [[ $1 == '-h' || $1 == '--help' || -z $1 ]]; then
    usage_error
fi

if [[ -z $2 ]]; then
    job_name=$1
    sed -i "/#SBATCH -J/c\#SBATCH -J $job_name" submit.sh
    if [[ -f lobster.sh ]]; then
        sed -i "/#SBATCH -J/c\#SBATCH -J $job_name" lobster.sh
    fi
    exit 0

elif [[ $1 == '-r' && ! -z $2 ]]; then
    if [[ -z $3 ]]; then
        usage_error
    fi
    job_name=$2
    SET=$(seq ${3:-1} ${4:-$3})
else
    numb $2
    job_name=$1
    SET=$(seq ${3:-1} ${4:-$3})
fi

# Loop through directories and update job names
for i in $SET
do
    i=${i%/}
    j=$(echo $i | cut -c 1)
    sed -i "/#SBATCH -J/c\#SBATCH -J $job_name$j" $i*/submit.sh
done

# Display updated job names
grep '#SBATCH -J' */submit.sh