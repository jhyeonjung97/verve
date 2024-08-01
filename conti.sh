#!/bin/bash

i=1
save="conti_$i"
while [[ -d "conti_$i" ]]
do
    i=$(($i+1))
    save="conti_$i"
done
mkdir $save
echo "mkdir $save"
cp * $save
echo "cp * $save"

# if [[ ! -d opt ]]; then
#     ase convert -f CONTCAR start.traj
# fi
# ase convert -f CONTCAR restart.json
find . -name 'DOS*' ! -name 'DOSCAR' -delete
sh ~/bin/verve/resub.sh