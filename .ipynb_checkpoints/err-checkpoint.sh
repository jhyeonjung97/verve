if [[ $1 == '-r' ]]; then
    dir_now=$PWD
    for dir in */
    do
        cd $dir
        grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
        tail err.*.log
        cd $dir_now
    done
else
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
    tail err.*.log
fi