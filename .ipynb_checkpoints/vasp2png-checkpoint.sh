for dir in /pscratch/sd/j/jiuy97/6_MNC/0_clean/*/*/*/*;
do
    cd $dir
    if [[ -s CONTCAR ]] && [[ ! -f side-view.png ]]; then
        python ~/bin/verve/vasp2png.py
    fi
done