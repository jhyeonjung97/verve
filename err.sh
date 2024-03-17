err_count=0
if [[ $1 == '-r' ]]; then
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
    tail err.*.log
elif [[ $1 == '-f' ]]; then
    tail err.*.log; tail vasp.out
else
    dir_now=$PWD
    for dir in */
    do
        cd $dir
        if [[ -s vasp.out ]]; then
            cp vasp.out temp.out
            if grep -q 'MAGMOM' vasp.out; then
                sed -i '0,/-----------------------------------------------------------------------------/{/-----------------------------------------------------------------------------/d;}' temp.out
                sed -i '0,/-----------------------------------------------------------------------------/{/-----------------------------------------------------------------------------/d;}' temp.out
            fi
            if grep -q '\-\-\-\-\-\-\-\-\-\-\-\-' temp.out; then
                echo -n -e "\e[35m$dir\e[0m"
                grep '\-\-\-\-\-\-\-\-\-\-\-\-' temp.out | tail -n 1
                err_count=1
            fi
            rm temp.out
        fi
        for file in err*log
        do
            if [[ -s $file ]]; then
                echo -n -e "\e[35m$dir\e[0m"
                tail $file | tail -n 2
                err_count=1
            fi
        done
        cd $dir_now
    done
    if [[ $err_count == 0 ]]; then
        echo -e "\e[35mCongrats! No error founded in vasp.out files\e[0m"
    fi
fi