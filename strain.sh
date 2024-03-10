#!/bin/bash

if [[ -z $1 ]]; then
    pwd
    read -p 'Enter the name of the structure file (traj or json): ' file
else
    file=$1
fi

if [[ $file == *.traj ]]; then
    name='start'
    ext='.traj'
    ase convert "$file" start.traj
elif [[ $file == *.json ]]; then
    name='restart'
    ext='.json'
    ase convert "$file" restart.json
else
    echo "Unsupported file type. Please provide a CONTCAR, .traj, or .json file."
    exit 1
fi

python ~/bin/verve/cell-size.py -i $file -f -0.3 -o "${name}1$ext"
python ~/bin/verve/cell-size.py -i $file -f -0.2 -o "${name}2$ext"
python ~/bin/verve/cell-size.py -i $file -f -0.1 -o "${name}3$ext"
python ~/bin/verve/cell-size.py -i $file -f 0.0 -o "${name}4$ext"
python ~/bin/verve/cell-size.py -i $file -f 0.1 -o "${name}5$ext"
python ~/bin/verve/cell-size.py -i $file -f 0.2 -o "${name}6$ext"
python ~/bin/verve/cell-size.py -i $file -f 0.3 -o "${name}7$ext"

mkdir 1_-0.3  2_-0.2  3_-0.1  4_0.0  5_+0.1  6_+0.2  7_+0.3

for dir in */; do
    i=$(echo "${dir%/}" | cut -c 1)
    if [[ -s "$name$i$ext" ]]; then
        mv "$name$i$ext" "$dir${name}$ext"
        cp ~/bin/shoulder/lobsterin "$dir"
        echo "Moved $name$i$ext to $dir${name}$ext"
    fi
done

~/bin/rm_mv "${name}$ext" original.traj
echo -e "\033[0;31mPrepare submit script and spread into the directories\033[0m"