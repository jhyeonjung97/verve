#!/bin/bash

metals_3d=('Ca' 'Sc' 'Ti' 'V' 'Cr' 'Mn' 'Fe' 'Co' 'Ni' 'Cu' 'Zn' 'Ga' 'Ge')
metals_4d=('Sr' 'Y' 'Zr' 'Nb' 'Mo' 'Tc' 'Ru' 'Rh' 'Pd' 'Ag' 'Cd' 'In' 'Sn')
metals_5d=('Ba' 'La' 'Hf' 'Ta' 'W' 'Re' 'Os' 'Ir' 'Pt' 'Au' 'Hg' 'Tl' 'Pb')

dir_now=$PWD

mkdir -p 3d 4d 5d
for dir in 3d 4d 5d; do
    cd $dir
    for i in "${!metals_${dir:0:1}d[@]}"; do
        if [ $i -lt 10 ]; then
            mkdir -p 0"$i"_"${metals_${dir:0:1}d[$i]}"
        else
            mkdir -p "$i"_"${metals_${dir:0:1}d[$i]}"
        fi
    done
    cd $dir_now
done

cp $1 POSCAR
sed -i -e "s/$2/XX/" POSCAR
sh ~/bin/verve/spread.sh -rr POSCAR
for dir in *d/*_*/; do
    cd $dir
    metal=$(basename $PWD | cut -d'_' -f2)
    sed -i -e "s/XX/$metal/" POSCAR
    # ase convert POSCAR start.traj
    cd $dir_now
done
for dir in *d/; do
    cd $dir
    coord=$(basename $PWD | cut -d'_' -f3)
    clean_dir=$(basename $dir)
    sh ~/bin/verve/jobname.sh -rc "$coord$clean_dir"
    cd $dir_now
done