#!/bin/bash

grep -B 1 "CONVERGED" err.*.log | grep -v "CONVERGED" | grep -vE "^--$" > temp.out
awk '{printf "%s %s\n", (NR<10 ? "0" NR : NR), $2}' temp.out | sort -k2,2n > mmff.out
awk '$1 <= 29' mmff.out > filtered_mmff.out
mv filtered_mmff.out mmff.out

rm temp.out
more mmff.out