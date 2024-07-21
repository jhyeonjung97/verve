#!/bin/bash

dir_tag=0
deep_tag=0
forced_tag=0
r_count=0

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

if [[ -n $select_dir ]]; then
    DIR=$select_dir
elif [[ -n $range ]]; then
    IFS=',' read -r -a range_arr <<< "$range"
    DIR=$(seq "${range_arr[0]}" "${range_arr[1]}")
    # DIR=$(seq -f "%g/" "${range_arr[0]}" "${range_arr[1]}")
elif [[ $r_count -eq 1 ]]; then
    # DIR='*_*/'
    DIR='*_*/*_*S/relaxed_'
elif [[ $r_count -gt 1 ]]; then
    DIR=''
    for ((i=0; i<r_count; i++)); do
        DIR+='*/'
    done
elif [[ $forced_tag == 1 ]]; then
    DIR='*/'
fi

dir_now=$PWD
if [[ -n $DIR ]]; then
    for dir in $DIR
    do
        cd $dir
        pwd
        sh ~/bin/temp.sh
        cd $dir_now
    done
else
    sh ~/bin/temp.sh
fi