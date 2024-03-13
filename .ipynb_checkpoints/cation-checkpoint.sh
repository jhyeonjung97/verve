#!/bin/bash

dir_now=$PWD
for dir in */
do
    cd $dir
    for i in $(seq 0 $1)
    do
        mkdir $i
        cp cation*_$i.traj $i/start.traj
    done
    cd $dir_now
done