#BASIC
alias c='clear'
alias ls='ls --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias grep='grep --color=auto'

alias rm='~/bin/shoulder/rm_mv'
alias remove='/bin/rm'
alias lsport='ls ~/port/'
alias cpport='cp *.vasp ~/port'
alias rmport='~/bin/rm_mv ~/port; mkdir ~/port'
alias temp='sh ~/bin/verve/temp.sh'
alias vitemp='vi ~/bin/temp.sh'
alias rmtemp='~/bin/rm_mv ~/bin/temp.sh'
alias retemp='sed -i -e "/^[^#]/s/^/#/" ~/bin/temp.sh'
alias vbash='vi ~/.bashrc'
alias sbash='source ~/.bashrc'
alias nofile='mkdir _trash
find . -maxdepth 1 -type f -exec mv {} _trash \;
~/bin/rm_mv _trash'
alias rsync='sh ~/bin/verve/archieve.sh'
alias spread='~/bin/verve/spread.sh'
alias conda-hi='conda init; conda activate py3'
alias conda-bye='conda deactivate; conda init --reverse'
alias conti='sh ~/bin/verve/conti.sh'

# Preperation
alias ma='grep MAGMOM */INCAR'
alias PBE='grep TITEL POTCAR'
alias sub='sh ~/bin/verve/sub.sh'
alias resub='sh ~/bin/verve/resub.sh'
alias name='sh ~/bin/verve/jobname.sh'
alias spread='sh ~/bin/verve/spread.sh'
alias cell-size='python ~/bin/verve/cell-size.py'
alias strain='sh ~/bin/verve/strain.sh'
alias debug='sed -i "/#SBATCH -t/c\#SBATCH -t 00:30:00" submit.sh
sed -i "/#SBATCH -q/c\#SBATCH -q debug" submit.sh'
alias regular='sed -i "/#SBATCH -t/c\#SBATCH -t 12:00:00" submit.sh
sed -i "/#SBATCH -q/c\#SBATCH -q regular" submit.sh'
alias cpu='sed -i "s/gpu/cpu/g" submit.sh
sed -i "s/-n 4 -c 32/-n 64 -c 4/g" submit.sh
sed -i "/#SBATCH -G/d" submit.sh'
alias gpu='sed -i "s/cpu/gpu/g" submit.sh
sed -i "s/gpu-bind/cpu-bind/g" submit.sh
sed -i "s/-n 64 -c 4/-n 4 -c 32/g" submit.sh
sed -i "/#SBATCH -G/d" submit.sh
sed -i "3a\#SBATCH -G 4" submit.sh'
alias hour='sh ~/bin/verve/hour.sh'
alias minute='sh ~/bin/verve/minute.sh'
alias static='sh ~/bin/verve/static.sh'
alias phonon='sh ~/bin/verve/phonon.sh'
alias lobin='sh ~/bin/verve/lobin.sh'
alias mpi='python ~/bin/verve/mpi.py'
alias gather='sh ~/bin/verve/gather.sh'
alias rename='sh ~/bin/verve/rename.sh'
alias slab='python ~/bin/verve/slab.py'

# Analysis
alias dp='display'
alias ta='tail */vasp.out'
alias te='grep free_energy */final*json'
alias me='grep MAGMOM */OUTCAR'
alias e='grep E0 OSZICAR'
alias ee='grep TOTEN OUTCAR | tail -n 1'
alias freq='grep THz OUTCAR'
alias fermi='grep E-fermi OUTCAR | tail -n 1'
alias outcar='sh ~/bin/verve/outcar.sh'
alias energy='python ~/bin/verve/energy.py'
alias bader='python ~/bin/verve/bader.py'
alias dos3='python ~/bin/shoulder/dos3.py'
alias dos3lob='python ~/bin/shoulder/dos3lob.py'
alias cohp='python ~/bin/playground/aloha/cohp.py'
alias cobi='python ~/bin/playground/aloha/cobi.py'
alias hopping='python ~/bin/verve/hopping.py'
alias sumo='sh ~/bin/verve/sumo.sh'
alias metals='sh ~/bin/verve/metals.sh'
alias mfa='sh ~/bin/verve/mmff-result.sh'
alias err='sh ~/bin/verve/err.sh'
alias open='sh ~/bin/verve/open.sh'
alias more='sh ~/bin/verve/more.sh'
alias tsv='python ~/bin/verve/tsv.py'
alias atoms='python ~/bin/verve/atoms.py'
alias time='grep sec OUTCAR'
alias formation='python ~/bin/verve/formation.py'
alias png='sh ~/bin/verve/png.sh'

#SSH
alias hi='sh ~/bin/verve/gits.sh orange shoulder verve tools
~/bin/sshproxy.sh -u jiuy97
ssh -X -Y -l jiuy97 -i ~/.ssh/nersc perlmutter.nersc.gov'
alias bye='sh ~/bin/verve/gits.sh orange shoulder verve tools'
alias byebye='sh ~/bin/verve/gits.sh orange shoulder verve tools && sh ~/bin/verve/archieve.sh'
alias burning='ssh -X -Y hyeonjung@burning.postech.ac.kr -p 54329'
alias slac='ssh -X -Y hyeonjung@burning.postech.ac.kr -p 54329'
alias snu='ssh -X -Y jiuy97@s3dflogin.slac.stanford.edu'
alias x2658='ssh -X -Y x2658a09@nurion.ksc.re.kr'
alias x2431='ssh -X -Y x2431a10@nurion.ksc.re.kr'
alias x2421='ssh -X -Y x2421a04@nurion.ksc.re.kr'
alias x2347='ssh -X -Y x2347a10@nurion.ksc.re.kr'
alias x2755='ssh -X -Y x2755a09@nurion.ksc.re.kr'
alias cori='ssh -X -Y jiuy97@cori.nersc.gov'
alias nersc='ssh -X -Y jiuy97@perlmutter.nersc.gov'

alias send='sh ~/bin/orange/send.sh'
alias get='sh ~/bin/orange/get.sh'

alias token='echo jhyeonjung97
echo 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'

#Git
alias gits='sh ~/bin/verve/gits.sh orange shoulder verve tools'
alias orange='sh ~/bin/verve/gits.sh orange'
alias shoulder='sh ~/bin/verve/gits.sh shoulder'
alias verve='sh ~/bin/verve/gits.sh verve'
alias tools='sh ~/bin/verve/gits.sh tools'
alias bye='sh ~/bin/verve/gits.sh orange shoulder verve tools'

#ASE
alias ag='ase gui'
alias aga='ag *.vasp'
alias pos='ag POSCAR'
alias posa='ag */POSCAR'
alias pos3='ag 00/POSCAR 01/POSCAR 02/POSCAR 03/POSCAR 04/POSCAR'
alias pos5='ag 00/POSCAR 01/POSCAR 02/POSCAR 03/POSCAR 04/POSCAR 05/POSCAR 06/POSCAR'
alias con='ag CONTCAR'
alias cona='ag */CONTCAR'
alias con3='ag 00/POSCAR 01/CONTCAR 02/CONTCAR 03/CONTCAR 04/POSCAR'
alias con5='ag 00/POSCAR 01/CONTCAR 02/CONTCAR 03/CONTCAR 04/CONTCAR 05/CONTCAR 06/POSCAR'
alias pickle='python3 -m ase.io.trajectory *.traj'
