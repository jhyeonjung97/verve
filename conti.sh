#!/bin/bash

python ~/bin/get_restart3

i=1
save="conti$i"
while [[ -d "$save" ]]; do
    i=$((i+1))
    save="conti$i"
done
mkdir "$save"
find . -maxdepth 1 -type f -exec mv {} "$save" \;

cp "$save"/restart.json .
cp "$save"/submit.sh .
if [[ -s "$save"/WAVECAR ]]; then
    cp "$save"/WAVECAR .
fi

sh ~/bin/verve/sub.sh
