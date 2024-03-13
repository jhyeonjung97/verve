#!/bin/bash

i=0
if grep -q 'Error EDDDAV: Call to ZHEGV failed. Returncode' vasp.out; then
    while (( i < 3 )); do
        sh ~/bin/verve/conti.sh
        ((i++))
    done
fi