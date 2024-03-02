#BASIC
alias c='clear'
alias ls='ls --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

alias rm='~/bin/rm_mv'
alias remove='/bin/rm'
alias lsport='ls ~/port/'
alias cpport='cp *.vasp ~/port'
alias rmport='~/bin/rm_mv ~/port; mkdir ~/port'
alias vitemp='vi ~/bin/temp.sh'
alias rmtemp='~/bin/rm_mv ~/bin/temp.sh'
alias vbash='vi ~/.bashrc'
alias sbash='source ~/.bashrc'
alias nofile='mkdir _trash
find . -maxdepth 1 -type f -exec mv {} _trash \;
~/bin/rm_mv _trash'

alias spread='~/bin/verve/spread.sh'

# Preperation
alias ma='grep MAGMOM */INCAR'
alias PBE='grep TITEL POTCAR'
alias sub='sh ~/bin/verve/sub.sh'
alias resub='sh ~/bin/verve/resub.sh'
alias name='sh ~/bin/verve/jobname.sh'
alias incar='sh ~/bin/verve/incar.sh'
alias mmff='sh ~/bin/verve/mmff.sh'

# Analysis
alias ta='tail */std*'
alias e='grep E0 stdout*'
alias ee='grep E0 stdout* | tail -n 3'
alias freq='grep THz OUTCAR'
alias fermi='grep E-fermi OUTCAR | tail -n 1'
alias magnet='awk "/magnetization \(x\)/,/tot /" OUTCAR'
alias bader='python ~/bin/verve/bader.py'
alias dos3='python ~/bin/shoulder/dos3.py'

# Git
alias orange='dir_now=$PWD
cd ~/bin/orange
git stash
git pull
cd $dir_now'
alias shoulder='dir_now=$PWD
cd ~/bin/shoulder
git stash
git pull
cd $dir_now'
alias verve='dir_now=$PWD
cd ~/bin/verve
git stash
git pull
cd $dir_now'

#SSH
alias burning='ssh -X -Y hyeonjung@burning.postech.ac.kr -p 54329'
alias snu='ssh -X -Y hyeonjung@210.117.209.87'
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
