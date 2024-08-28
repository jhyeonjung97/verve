#!/bin/bash

for dir in /pscratch/sd/j/jiuy97/6_MNC/0_clean/kisti/*d/*_*/*_*S/*_
do
    cd $dir; pwd
    IFS='/' read -r -a path_components <<< $PWD
    row=$(echo "${path_components[-4]}" | cut -d'_' -f1)
    metal=$(echo "${path_components[-3]}" | cut -d'_' -f2)
    spin=$(echo "${path_components[-2]}" | cut -d'_' -f2)
    dz=$(echo "${path_components[-1]}" | cut -d'_' -f1)
    
    path4=${path_components[-4]}
    path3=${path_components[-3]}
    path2=${path_components[-2]}
    path1=${path_components[-1]}
    
    if [[ ! -s DONE ]]; then
        path="/pscratch/sd/j/jiuy97/6_MNC/0_clean/$path4/$path3/$path2/nupdown"
        ls $path
        cp $path/WAVECAR .
        cp $path/restart.json .
        python ~/bin/tools/mnc/dz.py $dz
        cp /pscratch/sd/j/jiuy97/6_MNC/0_clean/submit.sh .
        sed -i -e "s/jobname/$row$metal$spin$dz/" submit.sh
        if [[ $spin == 'LS' ]]; then
            sed -i -e "s/mnc-sol.py/mnc-sol-ls-nupdown.py/" submit.sh
        elif [[ $spin == 'IS' ]]; then
            sed -i -e "s/mnc-sol.py/mnc-sol-is-nupdown.py/" submit.sh
        elif [[ $spin == 'HS' ]]; then
            sed -i -e "s/mnc-sol.py/mnc-sol-hs-nupdown.py/" submit.sh
        fi
        sbatch submit.sh
    fi
done
