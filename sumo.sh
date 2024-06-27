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
    --width 8 \
    --height 6 \
    --yscale 1 \
    --zero-line \
    --prefix $prefix \
    --xmin -8 \
    --xmax 6 \
    --gaussian 0.05
    

