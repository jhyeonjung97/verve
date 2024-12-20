#!/bin/bash

cut=1
dir_tag=0
forced_tag=0
while getopts ":rfcs:d:" opt; do
  case $opt in
    r)
      dir_tag=1
      ;;
    f)
      forced_tag=1
      ;;
    c)
      cut=2
      ;;
    s)
      select_dir="$OPTARG"
      ;;
    d)
      range="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done
shift "$((OPTIND-1))"
name=$1

if [[ -n $select_dir ]]; then
    DIR=$select_dir
elif [[ -n $range ]]; then
    IFS=',' read -r -a range_arr <<< "$range"
    DIR=$(seq "${range_arr[0]}" "${range_arr[1]}")
elif [[ $dir_tag == 1 ]]; then
    DIR='*_*/'
elif [[ $forced_tag == 1 ]]; then
    DIR='*/'
fi

if [[ -n $DIR ]]; then
    for dir in $DIR
    do
        dir=${dir%/}
        i=${dir:0:$cut}
        echo -n -e "$dir\t"
        if [[ -s "$dir/submit.sh"]]; then
            sed -i "/#SBATCH -J/c\#SBATCH -J ${name}$i" "$dir/submit.sh"
            sed -i "/#PBS -N/c\#PBS -N ${name}$i" "$dir/submit.sh"
            grep '#SBATCH -J' "$dir/submit.sh"
            grep '#PBS -N' "$dir/submit.sh"
        elif [[ -s "$dir/run_slurm.sh"]]; then
            sed -i "/#SBATCH --job-name/c\#SBATCH -J ${name}$i" "$dir/run_slurm.sh"
            sed -i "/#SBATCH -J/c\#SBATCH -J ${name}$i" "$dir/run_slurm.sh"
            grep '#SBATCH -J' "$dir/run_slurm.sh"
            grep '#PBS -N' "$dir/run_slurm.sh"
        fi
    done
elif [[ -s 'submit.sh' ]]; then
    sed -i "/#SBATCH -J/c\#SBATCH -J $name" submit.sh
    sed -i "/#PBS -N/c\#PBS -N $name" submit.sh
    grep '#SBATCH -J' submit.sh
    grep '#PBS -N' submit.sh
    exit 0
elif [[ -s 'run_slurm.sh' ]]; then
    sed -i "/#SBATCH --job-name/c\#SBATCH -J $name" run_slurm.sh
    sed -i "/#SBATCH -J/c\#SBATCH -J $name" run_slurm.sh
    grep '#SBATCH -J' run_slurm.sh
fi