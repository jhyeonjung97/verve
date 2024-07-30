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

if [[ ${here} == 'nersc' ]] || [[ ${here} == 's3df' ]] || [[ ${here} == 'kisti' ]]; then
    for i in $@
    do
        gits_nersc $i
        if [[ ${here} == 'nersc' ]] && [[ $i == 'tools' ]]; then
            cp ~/bin/tools/mnc/* /pscratch/sd/j/jiuy97/6_MNC/scripts
            echo "cp ~/bin/tools/mnc/* /pscratch/sd/j/jiuy97/6_MNC/scripts"
            cp ~/bin/tools/heo/* /pscratch/sd/j/jiuy97/5_HEO/scripts
            echo "cp ~/bin/tools/heo/* /pscratch/sd/j/jiuy97/5_HEO/scripts"
        elif [[ ${here} == 'kisti' ]] && [[ $i == 'tools' ]]; then
            cp ~/bin/tools/mnc/* /scratch/x2755a09/3_MNC/scripts
            echo "cp ~/bin/tools/mnc/* /scratch/x2755a09/3_MNC/scripts"
            cp ~/bin/tools/heo/* /scratch/x2755a09/4_HEO/scripts
            echo "cp ~/bin/tools/heo/* /scratch/x2755a09/4_HEO/scripts"
        fi
    done
else
    for i in $@
    do
        gits $i
    done
fi