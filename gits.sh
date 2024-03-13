gits() {
    local repository="$1"
    if [[ -d ~/bin/"$repository" ]]; then
        local dir_now=$PWD
        cd ~/bin/"$repository" || return
        git pull && git add . && git commit -m "." && git push
        cd "$dir_now" || return
    else
        echo "There is no ~/bin/$repository"
    fi
}

gits_nersc() {
    local repository="$1"
    if [[ -d ~/bin/"$repository" ]]; then
        local dir_now=$PWD
        cd ~/bin/"$repository" || return
        git stash && git pull && chmod 755 .
        cd "$dir_now" || return
    else
        echo "There is no ~/bin/$repository"
    fi
}

if [[ ${here} == 'nersc' ]]; then
    for i in "$@"
    do
        gits_nersc "$i"
    done
else
    for i in "$@"
    do
        gits "$i"
    done
fi