#!/bin/bash

# Define source and destination base directories
source_base="/pscratch/sd/j/jiuy97/6_MNC/0_clean"
destination_base="/pscratch/sd/j/jiuy97/cathub"

for dir in ${source_base}/*d/*_*/most_stable/relaxed; do
    if [[ -d "$dir" ]]; then
        IFS='/' read -r -a path <<< "$dir"
        metal=$(echo "${path[-3]}" | cut -d'_' -f3)
        dest_dir="${destination_base}/${metal}N4C26/001"
        mkdir -p "$dest_dir"
        cp "$dir/final_with_calculator.json" "$dest_dir/"
        echo "Copied final_with_calculator.json to $dest_dir"
    else
        echo "Directory does not exist: $dir"
    fi
done

echo "All files copied successfully."
