#!/bin/bash

grep -B 1 "CONVERGED" err.*.log | grep -v "CONVERGED" | grep -vE "^--$" > temp.out
awk '$1 <= 29' temp.out > filtered_temp.out
awk '{printf "%s %s\n", (NR<10 ? "0" NR : NR), $2}' filtered_temp.out | sort -k2,2n > mmff.out

# rm temp.out
more mmff.out