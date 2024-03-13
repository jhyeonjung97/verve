if [[ $1 == '-r' ]]; then
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' */vasp.out | tail -n 1
    tail */err.*.log
else
    grep '\-\-\-\-\-\-\-\-\-\-\-\-' vasp.out | tail -n 1
    tail err.*.log
fi