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
        echo $err_tag
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
        files=$(find . -maxdepth 1 -type f -name 'err*')
        if [ -z $files ]; then
            echo -n -e "\e[35m$dir\e[0m"
            echo "No 'err' files found."
            err_count=1
        elif [[ -s $file ]]; then
            echo -n -e "\e[35m$dir\e[0m"
            tail $file | tail -n 2
            err_count=1
        fi
        cd $dir_now
    done
    if [[ $err_count == 0 ]]; then
        echo -e "\e[35mCongrats! No error founded in vasp.out files\e[0m"
    fi
fi