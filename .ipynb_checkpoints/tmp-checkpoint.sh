sh ~/bin/verve/gather.sh -r -c 2 traj $1
python ~/bin/verve/slab.py -wcsf -r 2,2,2 -a 20 -t traj $1