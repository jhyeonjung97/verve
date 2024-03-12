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
    --elements Co.d \
    --orbitals Co.d \
    --atoms Co.1 \
    --no-total \
    --yscale 2 \
    --zero-line \
    --prefix $prefix

