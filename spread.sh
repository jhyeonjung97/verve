#!/bin/bash

if [[ $1 = '-r' ]]; then
    shift
    DIR='*/*/'
    file=$@
else
    DIR='*/'
    file=$@
fi

for dir in $DIR
do
    cp $file $dir
done