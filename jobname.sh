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
else
    if [[ $1 == '-r' && -z $2 ]]; then
        usage_error
    elif [[ $1 == '-r' ]]; then
        job_name=$2
        DIR='*/'
    elif [[ $1 == '-s' && -n $2 ]]; then
        DIR=$@
    else
        DIR=$(seq ${1:-1} ${2:-$1})
    fi
fi

# Loop through directories and update job names
for i in $DIR
do
    i=${i%/}
    j=$(echo $i | cut -c 1)
    sed -i "/#SBATCH -J/c\#SBATCH -J $job_name$j" $i*/submit.sh
done

# Display updated job names
grep '#SBATCH -J' */submit.sh