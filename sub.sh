#!/bin/bash

dir_tag=0
forced_tag=0
while getopts ":rfs:d:" opt; do
  case $opt in
    r)
      let r_count+=1
      ;;
    f)
      forced_tag=1
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
files=$@

if [[ -n $select_dir ]]; then
    DIR=$select_dir
elif [[ -n $range ]]; then
    IFS=',' read -r -a range_arr <<< "$range"
    DIR=$(seq "${range_arr[0]}" "${range_arr[1]}")
elif [[ $r_count -eq 1 ]]; then
    DIR='*_*/'
elif [[ $r_count -gt 1 ]]; then
    DIR=''
    for ((i=0; i<r_count; i++)); do
        DIR+='*/'
    done
elif [[ $forced_tag == 1 ]]; then
    DIR='*/'
fi

dir_now=$PWD
if [[ ${here} == 'kisti' ]]; then
    if [[ -n $DIR ]]; then
        for dir in $DIR
        do
            cd $dir
            if [[ -s submit.sh ]]; then
                qsub submit.sh
            fi
            cd $dir_now
        done
    else
        qsub submit.sh
    fi
else
    if [[ -n $DIR ]]; then
        for dir in $DIR
        do
            cd $dir
            if [[ -s submit.sh ]]; then
                sbatch submit.sh
            fi
            cd $dir_now
        done
    else
        sbatch submit.sh
    fi