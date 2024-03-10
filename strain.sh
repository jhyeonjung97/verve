#!/bin/bash

if [[ -z $1 ]]; then
    pwd
    read -p 'which structure file?: ' file
else
    file=$1
fi

if [[ $file == '*CONTCAR']] || [[ $file == '*.traj' ]]; then
    name='start'
    ext='.traj'
    ase convert $file start.traj
    python ~/bin/verve/cell-size.py -f -0.3 -o start1.traj
    python ~/bin/verve/cell-size.py -f -0.2 -o start2.traj
    python ~/bin/verve/cell-size.py -f -0.1 -o start3.traj
    python ~/bin/verve/cell-size.py -f 0.0 -o start4.traj
    python ~/bin/verve/cell-size.py -f 0.1 -o start5.traj
    python ~/bin/verve/cell-size.py -f 0.2 -o start6.traj
    python ~/bin/verve/cell-size.py -f 0.3 -o start7.traj
elif [[ $file == '*.json' ]]; then
    name='restart'
    ext='.json'
    ase convert $file restart.json
    python ~/bin/verve/cell-size.py -f -0.3 -o restart1.json
    python ~/bin/verve/cell-size.py -f -0.2 -o restart2.json
    python ~/bin/verve/cell-size.py -f -0.1 -o restart3.json
    python ~/bin/verve/cell-size.py -f 0.0 -o restart4.json
    python ~/bin/verve/cell-size.py -f 0.1 -o restart5.json
    python ~/bin/verve/cell-size.py -f 0.2 -o restart6.json
    python ~/bin/verve/cell-size.py -f 0.3 -o restart7.json
fi

mkdir 1_-0.3  2_-0.2  3_-0.1  4_0.0  5_+0.1  6_+0.2  7_+0.3

for dir in */
do
    i=$(echo ${dir%/} | cut -c 1)
    if [[ -s $name$i$ext ]]; then
        mv $name$i$ext $dir$name$ext
        echo "mv $name$i$ext $dir$name$ext"
        cp ~/bin/shoulder/lobsterin $dir
    fi
done

~/bin/rm_mv $name$ext original.traj
echo "\033[0;31mPrepare submit script and spread into the directories\033[0m"
