#!/bin/bash

dir_tag=0
forced_tag=0
dir_now=$PWD

while getopts ":rfs:d:" opt; do
  case $opt in
    r)
      dir_tag=1
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
elif [[ $dir_tag == 1 ]]; then
    DIR='*_*/'
elif [[ $forced_tag == 1 ]]; then
    DIR='*/'
fi

if [[ -n $DIR ]]; then
    for dir in $DIR
    do
        cd $dir
        sh ~/bin/temp.sh
        cd $dir_now
    done
else
    sh ~/bin/temp.sh
fi