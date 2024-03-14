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
            python ~/bin/verve/err-mag.py
            if grep -q '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out; then
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
        echo "\e[34mCongrats! There is no error founded in vasp.out files\e[0m"
    fi
fi