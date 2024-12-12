<<<<<<< HEAD
for file in *.vasp
do
    python ~/bin/verve/vasp2png.py $file
=======
for dir in /pscratch/sd/j/jiuy97/6_MNC/0_clean/*/*/*/*;
do
    cd $dir; pwd
    if [[ -s CONTCAR ]] && [[ ! -f side-view.png ]]; then
        python ~/bin/verve/vasp2png.py
    fi
done

for dir in /pscratch/sd/j/jiuy97/6_MNC/*_O*/*/*/*;
do
    cd $dir; pwd
    if [[ -s CONTCAR ]] && [[ ! -f side-view.png ]]; then
        python ~/bin/verve/vasp2png.py
    fi
>>>>>>> 392149b737b6b94a0bcd9cb166c6d06a476b27d9
done