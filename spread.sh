#!/bin/bash

dir_tag=0
select_dir=""
range=""
while getopts ":rs:d:" opt; do
  case $opt in
    r)
      dir_tag=1
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

# Shift off the options and optional --
shift "$((OPTIND-1))"

file=$1
files="$@"
name=${file%.*}
ext=${file##*.}
ext="${ext:+.$ext}"

if [[ -n $select_dir ]]; then
    DIR=("${select_dir}/")
elif [[ -n $range ]]; then
    IFS=',' read -r -a range_arr <<< "$range"
    DIR=($(seq "${range_arr[0]}" "${range_arr[1]}"))
elif [[ $dir_tag = 1 ]]; then
    DIR=('*/*/')
else
    DIR=('*/')
fi

for dir in "${DIR[@]}"
do
    if [[ -d $dir ]]; then
        for f in $files; do
            cp "$f" "$dir"
            echo "cp $f $dir"
        done
    else
        echo "$dir is not a valid directory."
    fi
done