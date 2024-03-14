if [[ $1 == '-r' ]]; then
    dir_now=$PWD
    for dir in */
    do
        cd $dir
        if [[ -s vasp.out ]]; then
            if grep -q '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out; then
                echo -n -e "\e[35m$dir\e[0m" && grep '\-\-\-\-\-\-\-\-\-\-\-\-' $dir'vasp.out' | tail -n 1
            fi
        fi
        cd $dir_now
        if [[ -s err.*.long ]]; then
            echo -n -e "\e[35m$dir\e[0m" && tail vasp.out | tail -n 1
        fi
    done
    # tail */err.*.log
else
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
    tail err.*.log
fi