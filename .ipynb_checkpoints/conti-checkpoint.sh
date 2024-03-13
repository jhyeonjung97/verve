#!/bin/bash

i=1
save="conti_$i"
while [[ -d "conti_$i" ]]
do
    i=$(($i+1))
    save="conti_$i"
done
mkdir $save
cp * $save
ase convert CONTCAR start.traj
sh ~/bin/verve/sub.sh