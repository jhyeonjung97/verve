#!/bin/bash

if [[ -n $1 ]]; then
    prefix=$1
else
    prefix='sumo'
fi

sumo-dosplot \
    --no-legend \
    --elements N.p.s \
    --orbitals N.p.s \
    --config ~/bin/verve/orbital_colours.conf \
    --format png \
    --dpi 100 \
    --column 1 \
    --width 6 \
    --height 4 \
    --yscale 1 \
    --zero-line \
    --prefix $prefix \
    --xmin -8 \
    --xmax 6 \
    --gaussian 0.05
    

