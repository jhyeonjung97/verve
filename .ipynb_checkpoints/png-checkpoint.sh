#!/bin/bash
if ${here} == 'slac'; then
    /usr/bin/rsync -e 'ssh' --ignore-times --size-only -avlzp -K --max-size=50000m \
    	--include="*/" \
    	--include="*.png" \
    	--exclude="*" \
     jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/3_V_shape .
elif ${here} == 'nersc'; then
    dir_now='/pscratch/sd/j/jiuy97/3_V_shape'
    cd $dir_now
    for dir in */*/; do
            cd $dir
            sh png1.sh
            cd $dir_now
    done
    for dir in */; do
            cd $dir
            sh png2.sh
            cd $dir_now
    done
    sh png3.sh
fi