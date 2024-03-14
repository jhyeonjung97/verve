if [[ $1 == '-r' ]]; then
    dir_now=$PWD
    for dir in */
    do
        cd $dir
        if grep -q '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out; then
            echo -n $dir && grep '\-\-\-\-\-\-\-\-\-\-\-\-' $dir'vasp.out' | tail -n 1
        fi
        cd $dir_now
    done
    tail */err.*.log
else
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
    tail err.*.log
fi