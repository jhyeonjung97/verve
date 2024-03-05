#!/bin/bash

dir_tag=0
numb_tag=0
while getopts ":rnf:" opt; do
  case $opt in
    r)
      dir_tag=1
    n)
      numb_tag=1
    f)
      filename="$OPTARG"
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

if [[ $dir_tag = 1 ]]; then
    DIR='*/*/'
else
    DIR='*/'
fi

if [[ $numb_tag = 1 ]]; then
    for dir in $DIR
    do
        cp $file $dir
    done
else
    for dir in $DIR
    do
        i=$(echo ${dir%/} | cut -c 1)
        cp $file$i $dir
    done
fi