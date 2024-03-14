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

if [[ -z $2 ]]; then
    pattern='X'
else
    pattern=$2
fi

metals_3d=(Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge)
metals_4d=(Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn)
metals_5d=(La Hf Ta W Re Os Ir Pt Au Hg Tl Pb)

mkdir -p 3d 4d 5d

process_metals() {
    local -n metals=$1
    local subdir=$2
    cd $subdir
    for i in ${!metals[@]}; do
        local formatted_index=$(printf "%02d" $i)
        local dir="${formatted_index}_${metals[i]}"
        mkdir $dir
        sed "s/$pattern/${metals[i]}/" ../$file > $dir/$file
        echo "sed \"s/$pattern/${metals[i]}/\" ../$file > $dir/$file"
    done
    cd ..
}

process_metals metals_3d 3d
process_metals metals_4d 4d
process_metals metals_5d 5d
rm $file

sed -i -e "/^[^#]/s/^/#/" ~/bin/temp.sh
echo "ase convert -f $file start.traj" >> ~/bin/temp.sh
echo "rm $file" >> ~/bin/temp.sh
sh ~/bin/verve/temp.sh -rr
sed -i -e '/^[^#]/d' ~/bin/temp.sh
