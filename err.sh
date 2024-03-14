if [[ $1 == '-r' ]]; then
    dir_now=$PWD
    for dir in */
    do
        cd $dir
        echo $dir && grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
        cd $dir_now
    done
    tail */err.*.log
else
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
    tail err.*.log
fi