#!/bin/bash

set_tag=0
dir_tag=0
numb_tag=0
while getopts ":rnd:" opt; do
  case $opt in
    r)
      dir_tag=1
      ;;
    n)
      numb_tag=1
      ;;
    d)
      set="$OPTARG"
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

# Shift the options out, so $1, $2, etc. are the non-option arguments
shift "$((OPTIND-1))"   

file=$1
echo $file

if [[ -n $set ]]; then
    a=${set%,*}
    b=${set##*,}
fi
echo $a $b

if [[ $dir_tag = 1 ]]; then
    DIR='*/*/'
else
    DIR='*/'
fi
        
if [[ $numb_tag = 0 ]]; then
    for dir in $DIR
    do
        cp $file $dir
    done
elif [[ -z $set ]]; then
    name=${file%.*}
    ext=${file##*.}
    for dir in $DIR
    do
        i=$(echo ${dir%/} | cut -c 1)
        if [[ -s $name$i.$ext ]]; then
            cp $name$i.$ext $dir$file
            echo "cp $name$i.$ext $dir$file"
        fi
    done
else
    for i in $(seq $a $b)
    do
        cp $name$i.$ext $i'*'/$file
        echo "cp $name$i.$ext $i'*'/$file"
    done
fi