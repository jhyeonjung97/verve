if [[ $1 == '-r' ]]; then
    dir_now=$PWD
    for dir in */
    do
        cd $dir
        if [[ -s vasp.out ]]; then
            if grep -q '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out; then
                echo -n $dir && grep "\e[32m\-\-\-\-\-\-\-\-\-\-\-\-\e[0m" $dir'vasp.out' | tail -n 1
            fi
        fi
        cd $dir_now
    done
    tail */err.*.log
else
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
    tail err.*.log
fi