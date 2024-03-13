#!/bin/bash
    
if [[ -z $1 ]]; then # simple submit
    sh ~/bin/temp.sh
else
    dir_now=$PWD
    if [[ $1 == '-r' ]]; then
        DIR='*/'
    elif [[ $1 == '-rr' ]]; then
        DIR='*/*/'
    elif [[ $1 == '-rrr' ]]; then
        DIR='*/*/*/'
    elif [[ $1 == '-s' ]]; then
        DIR=${@:2}
    elif [[ -z $2 ]]; then
        DIR=$(seq 1 $1)
    else
        DIR=$(seq $1 $2)
    fi
    for i in $DIR
    do
        cd $i
        sh ~/bin/temp.sh
        cd $dir_now
    done
fi