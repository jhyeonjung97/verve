#!/bin/bash

i=1
save="conti_$i"
while [[ -d "conti_$i" ]]
do
    i=$(($i+1))
    save="conti_$i"
done
mkdir $save
echo "mkdir $save"
mv * $save
echo "mv * $save"

cp "$save"/restart.json .
cp "$save"/WAVECAR .
cp "$save"/submit.sh .

sh ~/bin/verve/sub.sh