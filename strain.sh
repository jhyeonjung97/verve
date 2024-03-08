#!/bin/bash

cp relaxed/restart.json .
mkdir 1_-0.3  2_-0.2  3_-0.1  4_0.0  5_+0.1  6_+0.2  7_+0.3

python ~/bin/verve/cell-size.py -f -0.3 -o start1.traj
python ~/bin/verve/cell-size.py -f -0.2 -o start2.traj
python ~/bin/verve/cell-size.py -f -0.1 -o start3.traj
python ~/bin/verve/cell-size.py -f 0.0 -o start4.traj
python ~/bin/verve/cell-size.py -f 0.1 -o start5.traj
python ~/bin/verve/cell-size.py -f 0.2 -o start6.traj
python ~/bin/verve/cell-size.py -f 0.3 -o start7.traj

# for i in {1..7}
#     dir="$i*/"
#     file='start.traj'
#     mv start$i.traj $dir$file
    
name='start'
ext='.traj'

for dir in */
do
    i=$(echo ${dir%/} | cut -c 1)
    echo $name$i$ext
    if [[ -s $name$i$ext ]]; then
        mv $name$i$ext $dir$name$ext
        echo "mv $name$i$ext $dir$name$ext"
    fi
done

~/bin/rm_mv 'restart.json' 'original.json'
ls */