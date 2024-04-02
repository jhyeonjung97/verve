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
ase convert -f CONTCAR start.traj
ase convert -f CONTCAR restart.json
sh ~/bin/verve/resub.sh