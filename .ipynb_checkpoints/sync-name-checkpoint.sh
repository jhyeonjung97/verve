#!/bin/bash

for dir in /scratch/x2755a09/slab_name/6_V_slab/*_*_*/*
do
    cd $dir; pwd
    IFS='/' read -r -a path_components <<< "$PWD"
    f=($(ls -d */))
    
    # row=$(echo "${path_components[-4]}" | cut -d'_' -f1)
    # metal=$(echo "${path_components[-3]}" | cut -d'_' -f2)
    # spin=$(echo "${path_components[-2]}" | cut -d'_' -f2)
    # dz=$(echo "${path_components[-1]}" | cut -d'_' -f1)
    
    length=${#path_components[@]}
    path2=${path_components[$((length-2))]}
    path1=${path_components[$((length-1))]}

    # path4=${path_components[-4]}
    # path3=${path_components[-3]}
    # path2=${path_components[-2]}
    # path1=${path_components[-1]}
    
    match="/scratch/x2755a09/6_V_slab/$path2/$path1"

    if [[ -d $match ]]; then
        cd $match; pwd
        i=($(ls -d */))
        # echo $i
        # echo $f
    
        n=${#i[@]}
        n=$(($n-1))
        for j in $(seq 0 $n)
        do
            if [[ ${i[$j]} != ${f[$j]} ]]; then
                echo "mv ${i[$j]} ${f[$j]}"
                mv ${i[$j]} ${f[$j]}
            fi
        done
    fi
done
