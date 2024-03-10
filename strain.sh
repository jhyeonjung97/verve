#!/bin/bash

cp relaxed/submit.sh .
ase convert relaxed/CONTCAR start.traj

mkdir 1_-0.3  2_-0.2  3_-0.1  4_0.0  5_+0.1  6_+0.2  7_+0.3

python ~/bin/verve/cell-size.py -f -0.3 -o start1.traj
python ~/bin/verve/cell-size.py -f -0.2 -o start2.traj
python ~/bin/verve/cell-size.py -f -0.1 -o start3.traj
python ~/bin/verve/cell-size.py -f 0.0 -o start4.traj
python ~/bin/verve/cell-size.py -f 0.1 -o start5.traj
python ~/bin/verve/cell-size.py -f 0.2 -o start6.traj
python ~/bin/verve/cell-size.py -f 0.3 -o start7.traj
    
name='start'
ext='.traj'

for dir in */
do
    i=$(echo ${dir%/} | cut -c 1)
    if [[ -s $name$i$ext ]]; then
        mv $name$i$ext $dir$name$ext
        echo "mv $name$i$ext $dir$name$ext"
        cp ~/bin/shoulder/lobsterin $dir
    fi
done

~/bin/rm_mv start.traj submit.sh original.traj
echo '\033[0;31mPlease modify a submit script and spread into the directories\033[0m'
