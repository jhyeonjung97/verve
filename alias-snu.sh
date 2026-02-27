#!/bin/bash

alias cdw='cd /home/hyeonjung/scratch'
alias cdp='cd /global/cfs/cdirs/m2997/'

alias vasp5='mv /global/homes/j/jiuy97/bin/vasp_outcar_parsers5.py /global/homes/j/jiuy97/.local/lib/python3.11/site-packages/ase/io/vasp_parsers/vasp_outcar_parsers.py'
alias vasp6='mv /global/homes/j/jiuy97/bin/vasp_outcar_parsers6.py /global/homes/j/jiuy97/.local/lib/python3.11/site-packages/ase/io/vasp_parsers/vasp_outcar_parsers.py'
alias mystat='squeue -o "%.10i %.9P %.16j %.8u %.8T %.8M %.10l %.6D %.15R" --me --sort=i'
alias idle='squeue -o "%.10i %.9P %.16j %.8u %.8T %.8M %.10l %.6D %.15R" --me --sort=i | grep "30:00" | grep gpu
squeue -o "%.10i %.9P %.16j %.8u %.8T %.8M %.10l %.6D %.15R" --me --sort=i | grep "30:00" | grep regular'

alias qdel='scancel'
alias qdel-all="squeue | grep jiuy97 | awk '{print \$1}' | xargs -I {} scancel {}"

alias k='python ~/bin/verve/show_kpoints.py POSCAR
python ~/bin/verve/show_kpoints.py CONTCAR'

alias va='tail */vib/stdout.*.out'
alias ta='tail */vasp.out'
alias restart='sh ~/bin/verve/correct-contcar.sh; python ~/bin/get_restart.py'

alias idle='pestat -s idle'
alias mystat='qstat -u hyeonjung'
alias mystat-g='
echo "g1"
qstat -u hyeonjung | grep --colour g1
echo "g2"
qstat -u hyeonjung | grep --colour g2
echo "g3"
qstat -u hyeonjung | grep --colour g3
echo "g4"
qstat -u hyeonjung | grep --colour g4'
alias g1='qstat | grep -i "Q g1" '
alias g2='qstat | grep -i "Q g2" '
alias g3='qstat | grep -i "Q g3" '
alias g4='qstat | grep -i "Q g4" '
alias g='
echo -e "\033[1mg1:\033[0m"
g1
echo -e "\033[1mg2:\033[0m"
g2
echo -e "\033[1mg3:\033[0m"
g3
echo -e "\033[1mg4:\033[0m"
g4
idle'

alias p='echo "<g1>"
squeue -o "%.10F %.10u %.20j %.2P %.5Q %.2t %.2Y" -S "t,-Q" | grep g1
echo "<g2>"
squeue -o "%.10F %.10u %.20j %.2P %.5Q %.2t %.2Y" -S "t,-Q" | grep g2
echo "<g3>"
squeue -o "%.10F %.10u %.20j %.2P %.5Q %.2t %.2Y" -S "t,-Q" | grep g3
echo "<g4>"
squeue -o "%.10F %.10u %.20j %.2P %.5Q %.2t %.2Y" -S "t,-Q" | grep g4'
alias p1='squeue -o "%.10F %.10u %.20j %.2P %.5Q %.2t %.2Y" -S "t,-Q" | grep g1'
alias p2='squeue -o "%.10F %.10u %.20j %.2P %.5Q %.2t %.2Y" -S "t,-Q" | grep g2'
alias p3='squeue -o "%.10F %.10u %.20j %.2P %.5Q %.2t %.2Y" -S "t,-Q" | grep g3'
alias p4='squeue -o "%.10F %.10u %.20j %.2P %.5Q %.2t %.2Y" -S "t,-Q" | grep g4'
alias pestat1='pestat -N | grep g1'
alias pestat2='pestat -N | grep g2'
alias pestat3='pestat -N | grep g3'
alias pestat4='pestat -N | grep g4'