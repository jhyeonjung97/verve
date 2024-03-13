#!/bin/bash

file=$1
metals_3d=(Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge)
metals_4d=(Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn)
metals_5d=(La Hf Ta W Re Os Ir Pt Au Hg Tl Pb)

mkdir -p 3d 4d 5d
sh ~/bin/verve/spread.sh -d 3,5 "$file"

process_metals() {
    local -n metals=$1
    local subdir=$2
    cd "$subdir"
    for i in "${!metals[@]}"; do
        local formatted_index=$(printf "%02d" $i)
        local dir="${formatted_index}_${metals[i]}"
        mkdir "$dir"
        sed "s/X/${metals[i]}/" "../$file" > "$dir/$file"
        echo "Changed XX in $file to ${metals[i]}"
    done
    cd ..
}

process_metals metals_3d 3d
process_metals metals_4d 4d
process_metals metals_5d 5d