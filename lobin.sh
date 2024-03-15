#!/bin/bash

dir_now=$PWD
cp ~/bin/shoulder/lobsterin .
sh ~/bin/verve/spread.sh lobsterin
for dir in *_*/; do
    cd $dir
    dir=${dir%/}
    IFS='_' read -r A B <<< "$dir"
    sed -i -e "s/X/$B/g" lobsterin
    cd $dir_now
done
