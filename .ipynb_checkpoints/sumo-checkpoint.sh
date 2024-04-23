#!/bin/bash

if [[ -n $1 ]]; then
    prefix=$1
else
    prefix='sumo'
fi

sumo-dosplot \
    --legend-frame \
    --config ~/bin/verve/orbital_colours.conf \
    --format png \
    --dpi 100 \
    --column 1 \
    --width 12 \
    --height 6 \
    --elements Zn.d \
    --orbitals Zn.d \
    --atoms Zn.1 \
    --yscale 2 \
    --zero-line \
    --prefix $prefix \
    --xmin -10 \
    --xmax 10
    

