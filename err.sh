err_count=0
if [[ $1 == '-r' ]]; then
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
    tail err.*.log
else
    dir_now=$PWD
    for dir in */
    do
        cd $dir
        if [[ -s vasp.out ]]; then
            vasp.out temp.out
            if grep -q 'MAGMOM' vasp.out; then
                sed -i '0,/-----------------------------------------------------------------------------/{/-----------------------------------------------------------------------------/d;}' temp.out
            fi
            if grep -q '\-\-\-\-\-\-\-\-\-\-\-\-' temp.out; then
                echo -n -e "\e[35m$dir\e[0m"
                grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
                err_count=1
            fi
        fi
        cd $dir_now
        if [[ -s err.*.long ]]; then
            echo -n -e "\e[35m$dir\e[0m" && tail vasp.out | tail -n 1
            err_count=1
        fi
    done
    if [[ $err_count == 0 ]]; then
        echo -e "\e[35mCongrats! No error founded in vasp.out files\e[0m"
    fi
fi