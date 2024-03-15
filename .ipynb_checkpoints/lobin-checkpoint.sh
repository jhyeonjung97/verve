#!/bin/bash

cp ~/bin/shoulder/lobsterin .
sh ~/bin/verve/spread.sh lobsterin
for dir in *_*/; do
    dir=${dir%/}
    IFS='_' read -r A B <<< "$dir"
    sed -i -e "s/X/$B/g" lobsterin
done
