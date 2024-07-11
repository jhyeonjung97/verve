#!/bin/bash

# Get the current working directory
current_dir=$(pwd)

# Split the path into components
IFS='/' read -r -a path_components <<< "$current_dir"

# Extract the required parts and split by '_'
metal=$(echo "${path_components[-3]}" | cut -d'_' -f2)
spin=$(echo "${path_components[-2]}" | cut -d'_' -f2)
dz=$(echo "${path_components[-1]}" | cut -d'_' -f1)

# Print the results
echo "Metal part: $metal"
echo "Spin part: $spin"
echo "DZ part: $dz"
