#!/bin/bash

dir_tag=0
numb_tag=0
while getopts ":rnd:f:" opt; do
  case $opt in
    r)
      dir_tag=1
      ;;
    n)
      numb_tag=1
      ;;
    d)
      SET="$OPTARG"
      ;;
    f)
      file="$OPTARG"
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

if [[ -n $SET ]]; then
    a=${SET%,*}
    b=${SET##*,}
    DIR=$(seq $a $b)
elif [[ $dir_tag = 1 ]]; then
    DIR='*/*/'
else
    DIR='*/'
fi
        
if [[ $numb_tag = 0 ]]; then
    for dir in $DIR
    do
        cp $file $dir
    done
else
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
fi