#!/bin/bash

if [[ -n $1 ]]; then
    prefix=$1
else
    prefix='sumo'
fi

sumo-dosplot \
    --legend-frame \
    --legend-cutoff 0 \
    --config ~/bin/verve/orbital_colours.conf \
    --format png \
    --dpi 100 \
    --column 1 \
    --width 12 \
    --height 6 \
    --yscale 1 \
    --zero-line \
    --prefix $prefix \
    --xmin -10 \
    --xmax 6 \
    --gaussian 0.05
    

