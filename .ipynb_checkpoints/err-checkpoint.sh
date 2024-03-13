if [[ $1 == '-r' ]]; then
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' */vasp.out
    tail */err.*.log
else
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out
    tail err.*.log

fi