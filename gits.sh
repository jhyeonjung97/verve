gits() {
    local repository=$1
    if [[ -d ~/bin/$repository ]]; then
        local dir_now=$PWD
        cd ~/bin/$repository
        git pull
        git add .
        git commit -m "."
        git push
        cd $dir_now
    else
        echo "There is no ~/bin/$repository"
    fi
}

gits_nersc() {
    local repository=$1
    if [[ -d ~/bin/$repository ]]; then
        local dir_now=$PWD
        cd ~/bin/$repository
        git stash
        git pull
        chmod 755 ./*
        cd $dir_now
    else
        echo "There is no ~/bin/$repository"
    fi
}

if [[ ${here} == 'nersc' ]] || [[ ${here} == 's3df' ]] || [[ ${here} == 'kisti' ]] || [[ ${here} == 'burning2' ]]; then
    for i in $@
    do
        gits_nersc $i
        if [[ ${here} == 'nersc' ]] && [[ $i == 'tools' ]]; then
            cp -r ~/bin/tools/mnc/* /pscratch/sd/j/jiuy97/6_MNC/scripts
            cp -r ~/bin/tools/heo/* /pscratch/sd/j/jiuy97/5_HEO/scripts
            cp -r ~/bin/tools/tetra/* /pscratch/sd/j/jiuy97/3_V_bulk/scripts
        elif [[ ${here} == 'kisti' ]] && [[ $i == 'tools' ]]; then
            cp -r ~/bin/tools/mnc/* /scratch/x2755a09/3_MNC/scripts
            sed -i -e 's/kpar=8/kpar=1/' /scratch/x2755a09/3_MNC/scripts/*.py
            sed -i -e 's/npar=1/npar=8/' /scratch/x2755a09/3_MNC/scripts/*.py
            cp -r ~/bin/tools/heo/* /scratch/x2755a09/4_HEO/scripts
            sed -i -e 's/kpar=8/kpar=8/' /scratch/x2755a09/4_HEO/scripts/*.py
            sed -i -e 's/npar=1/npar=8/' /scratch/x2755a09/4_HEO/scripts/*.py
            cp -r ~/bin/tools/tetra/* /scratch/x2755a09/5_V_bulk/scripts
            sed -i -e 's/kpar=8/kpar=4/' /scratch/x2755a09/5_V_bulk/scripts/opt*.py
            sed -i -e 's/npar=1/npar=16/' /scratch/x2755a09/5_V_bulk/scripts/opt*.py 
        fi
    done
else
    for i in $@
    do
        gits $i
    done
fi