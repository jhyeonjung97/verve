#!/bin/bash

file=$1
case "$file" in
    POSCAR|CONTCAR|*.vasp)
        ;;
    *)
        echo 'Are you sure..? Give me POSCAR or CONTCAR or *.vasp'
        exit 1
        ;;
esac

if [[ ! -f $file ]]; then
    echo "File $file does not exist."
    exit 1
fi

if [[ -z $2 ]]; then
    pattern='X'
else
    pattern=$2
fi

metals_3d=(Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge)
metals_4d=(Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn)
metals_5d=(Ba La Hf Ta W Re Os Ir Pt Au Hg Tl Pb)

mkdir -p 3d 4d 5d

process_metals() {
    local metals=("$@")
    local subdir=${metals[-1]}
    unset metals[-1]
    cd $subdir
    for metal in "${metals[@]}"; do
        local dir="${metal}"
        mkdir -p $dir || { echo "Failed to create directory $dir"; exit 1; }
        sed "s/$pattern/$metal/" ../$file > $dir/$file || { echo "Failed to process $file with $metal"; exit 1; }
        echo "sed \"s/$pattern/$metal/\" ../$file > $dir/$file"
    done
    cd ..
}

process_metals "${metals_3d[@]}" 3d
process_metals "${metals_4d[@]}" 4d
process_metals "${metals_5d[@]}" 5d
rm $file

trap 'sed -i -e "/^[^#]/d" ~/bin/temp.sh' EXIT
sed -i -e "/^[^#]/s/^/#/" ~/bin/temp.sh
echo "ase convert -f $file start.traj" >> ~/bin/temp.sh
echo "rm $file" >> ~/bin/temp.sh
sh ~/bin/verve/temp.sh -rr
