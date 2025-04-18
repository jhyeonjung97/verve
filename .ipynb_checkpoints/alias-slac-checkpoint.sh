#!/bin/bash

# alias cdw='cd /sdf/scratch/users/j/jiuy97/'
# alias cdp='cd /fs/ddn/sdf/group/suncat/hailey/'
alias cdw='cd /fs/ddn/sdf/group/suncat/hailey/'
alias cdp='cd /fs/ddn/sdf/group/suncat/'

alias vasp5='mv /global/homes/j/jiuy97/bin/vasp_outcar_parsers5.py /global/homes/j/jiuy97/.local/lib/python3.11/site-packages/ase/io/vasp_parsers/vasp_outcar_parsers.py'
alias vasp6='mv /global/homes/j/jiuy97/bin/vasp_outcar_parsers6.py /global/homes/j/jiuy97/.local/lib/python3.11/site-packages/ase/io/vasp_parsers/vasp_outcar_parsers.py'
alias mystat='squeue -o "%.10i %.9P %.16j %.8u %.8T %.8M %.10l %.6D %.15R" --me --sort=i'
alias idle='squeue -o "%.10i %.9P %.16j %.8u %.8T %.8M %.10l %.6D %.15R" --me --sort=i | grep "30:00" | grep gpu
squeue -o "%.10i %.9P %.16j %.8u %.8T %.8M %.10l %.6D %.15R" --me --sort=i | grep "30:00" | grep regular'

alias qdel='scancel'

alias k='python ~/bin/verve/show_kpoints.py POSCAR
python ~/bin/verve/show_kpoints.py CONTCAR'