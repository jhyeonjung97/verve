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
files=$1
name=${file%.*}
ext=${file##*.}
if [[ $name == $ext ]]; then
    ext=''
else
    ext='.'$ext
fi

if [[ -n $set ]]; then
    a=${set%,*}
    b=${set##*,}
elif [[ $dir_tag = 1 ]]; then
    DIR='*/*/'
else
    DIR='*/'
fi

if [[ -n $set ]]; then
    for i in $(seq $a $b)
    do
        cp $files $i*
        echo "cp $files $i*"
    done
elif [[ $numb_tag = 0 ]]; then
    for dir in $DIR
    do
        cp $files $dir
        echo "cp $files $dir"
    done
else
    for dir in $DIR
    do
        i=$(echo ${dir%/} | cut -c 1)
        if [[ -s $name$i$ext ]]; then
            cp $name$i$ext $dir$file
            echo "cp $name$i$ext $dir$file"
        fi
    done
fi
