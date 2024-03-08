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

mv start1.traj 1*/start.traj
mv start2.traj 2*/start.traj
mv start3.traj 3*/start.traj
mv start4.traj 4*/start.traj
mv start5.traj 5*/start.traj
mv start6.traj 6*/start.traj
mv start7.traj 7*/start.traj


rm 'restart.json'
ls */