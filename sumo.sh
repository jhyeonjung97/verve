#!/bin/bash

# Generate DOS plot with specified options
sumo-dosplot \
    --legend-frame \
    --config ~/bin/verve/orbital_colours.conf \
    --format png \
    --dpi 100 \
    --column 1 \
    --width 12 \
    --height 8 \
    --elements Co.d \
    --orbitals Co.d \
    --atoms Co.1 \
    --no-total \
    --yscale 2 \
    --zero-line

# Check if a command-line argument is provided
if [[ -n $1 ]]; then
    # Rename and display the generated plot
    mv dos.png "$1.png"
    display "$1.png"
else
    # Display the plot with the default name
    display dos.png
fi