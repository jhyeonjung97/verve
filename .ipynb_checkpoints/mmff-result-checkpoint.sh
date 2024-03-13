#!/bin/bash

grep -B 1 "CONVERGED" err.*.log | grep -v "CONVERGED" | grep -vE "^--$" > temp.out
awk '{printf "%s %s\n", (NR<10 ? "0" NR : NR), $2}' temp.out | sort -k2,2n > mmff.out