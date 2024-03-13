gits(repository) {
    if [[ -d ~/bin/$repository ]]; then
        dir_now=$PWD
        cd ~/bin/$repository
        git pull
        git add *
        git commit -m "."
        git push
        cd $dir_now
    else
        echo "There is no ~/bin/$repository"
    fi
}

gits_nersc(repository) {
    if [[ -d ~/bin/$repository ]]; then
        dir_now=$PWD
        cd ~/bin/$repository
        git stash
        git pull
        chmod 755 *
        cd $dir_now
    else
        echo "There is no ~/bin/$repository"
    fi
}

if [[ ${here} == 'nersc' ]]; then
    for i in $@
    do
        gits_nersc($i)
    done
else
    for i in $@
    do
        gits($i)
    done
fi