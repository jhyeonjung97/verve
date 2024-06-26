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

if [[ ${here} == 'nersc' ]] || [[ ${here} == 's3df' ]]; then
    for i in $@
    do
        gits_nersc $i
    done
else
    for i in $@
    do
        gits $i
    done
fi