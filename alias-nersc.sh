#!/bin/bash

alias cdw='cd /pscratch/sd/j/jiuy97'
alias cdp='cd /global/cfs/cdirs/m2997/'

alias vasp5='mv /global/homes/j/jiuy97/bin/vasp_outcar_parsers5.py /global/homes/j/jiuy97/.local/lib/python3.11/site-packages/ase/io/vasp_parsers/vasp_outcar_parsers.py'
alias vasp6='mv /global/homes/j/jiuy97/bin/vasp_outcar_parsers6.py /global/homes/j/jiuy97/.local/lib/python3.11/site-packages/ase/io/vasp_parsers/vasp_outcar_parsers.py'
alias mystat='squeue -o "%.18i %.9P %.18j %.8u %.10T %.8M %.10l %.6D %R" --me --sort=i'

alias sub='sbatch submit.sh'
alias qdel='scancel'

alias time='grep sec OUTCAR'
