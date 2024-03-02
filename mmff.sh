#!/bin/bash

if [[ $1 =~ '-h' ]]; then
    echo 'usage: pack [NAME.inp] (lattice A, B, C)'
    exit 1
fi

name="${1%.*}"
seed=$2

a=$3
b=$4
c=$5
if [[ -z $a ]]; then
    echo 'use default lattice parameter 30 A, 30 A, 40 A...'
    a=30.
    b=30.
    c=40.
else
    if [[ $a != '*.*' ]]; then
        a=$a.0
    fi
    if [[ $b != '*.*' ]]; then
        b=$b.0
    fi
    if [[ $c != '*.*' ]]; then
        c=$c.0
    fi
fi

for i in {0..99}
do
    j=$(printf "%02d" $i)
    sed -i "/output/c\output $name$j.xyz" $name.inp
    sed -i "/seed/c\seed $i" $name.inp
    ~/bin/packmol/packmol < $name.inp
    echo "obabel $name$j.xyz -O $name$j.mol2"
    obabel $name$j.xyz -O $name$j.mol2
done

for i in {0..99}
do
    j=$(printf "%02d" $i)    
    echo "obminimize -n 100000000 -sd -c 1e-8 -ff MMFF94s $name$j.mol2 > $name$j.pdb"
    obminimize -n 100000000 -sd -c 1e-8 -ff MMFF94s $name$j.mol2 > $name$j.pdb
done

python3 ~/bin/orange/convert.py pdb json $a $b $c