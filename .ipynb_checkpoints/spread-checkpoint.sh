#!/bin/bash

dir_tag=0
atom_tag=0
forced_tag=0
while getopts ":rfas:d:" opt; do
  case $opt in
    r)
      dir_tag=1
      ;;
    f)
      forced_tag=1
      ;;
    a)
      atom_tag=1
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


if [[ $atom_tag == 1 ]]; then
    name=$1
    for i in {0..9}
    do
        dir=$i_*/
        file=$name*$i.vasp
        cp $file $dir
        echo "cp $file $dir"
    done
    exit
else
    files=$@
fi

if [[ -n $select_dir ]]; then
    DIR=$select_dir
elif [[ -n $range ]]; then
    IFS=',' read -r -a range_arr <<< "$range"
    DIR=$(seq "${range_arr[0]}" "${range_arr[1]}")
elif [[ $dir_tag == 1 ]]; then
    DIR='*/*/'
elif [[ $forced_tag == 1 ]]; then
    DIR='*/'
else
    DIR='*_*/'
fi

for dir in $DIR
do
    if [[ -d $dir ]]; then
        for file in $files; do
            cp $file $dir
            echo "cp $file $dir"
        done
    else
        echo "$dir is not a valid directory."
    fi
done