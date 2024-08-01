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

find . -name 'DOS*' ! -name 'DOSCAR' -delete
rm DONE vasprun.xml atoms_bader_charge.json OUTCAR* moments* final* *tsv *txt

sh ~/bin/verve/resub.sh