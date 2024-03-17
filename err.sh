err_count=0
if [[ $1 == '-r' ]]; then
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
    tail err.*.log
elif [[ $1 == '-f' ]]; then
    tail err.*.log; tail vasp.out
else
    dir_now=$PWD
    for dir in *_*/
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
            if ! grep -q "PROFILE" vasp.out; then
                echo -e "\e[35m$dir\e[0m Calculation is not done.."
                err_count=1
            fi
        else
            echo -e "\e[35m$dir\e[0m Calculation is not done.."
            err_count=1
        fi
        files=$(find . -maxdepth 1 -type f -name 'err*')
        if [[ -z $files ]]; then
            echo -n -e "\e[35m$dir \e[0m"
            echo "No 'err' files found."
            err_count=1
        else
            for file in err.*.log
            do
                if [[ -s $file ]]; then
                    echo -n -e "\e[35m$dir\e[0m"
                    tail $file | tail -n 2
                    err_count=1
                fi
            done
        fi
        if [[ -d opt ]]; then
            files=$(find opt -maxdepth 1 -type f -name 'err*')
            if [[ -z $files ]]; then
                echo -n -e "\e[35m$dir \e[0m"
                echo "No 'opt\/err' files found."
                err_count=1
            else
                for file in opt/err.*.log
                do
                    if [[ -s $file ]]; then
                        echo -n -e "\e[35m$dir\e[0m"
                        tail $file | tail -n 2
                        err_count=1
                    fi
                done
            fi
            if ! grep -q "PROFILE" opt/vasp.out; then
                echo -e "\e[35m$dir\e[0m Opt calculation is not done.."
                err_count=1
            fi
            if [[ -z opt/vasp.out ]]; then
                echo -e "\e[35m$dir\e[0m Calculation is not done.."
                err_count=1
            fi
        fi
        cd $dir_now
    done
    if [[ $err_count == 0 ]]; then
        echo -e "\e[35mCongrats! No error founded in vasp.out files\e[0m"
    fi
fi