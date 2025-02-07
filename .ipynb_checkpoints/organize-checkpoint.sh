#!/bin/bash

source_base="/pscratch/sd/j/jiuy97/6_MNC"
destination_base="/pscratch/sd/j/jiuy97/cathub"

# for dir in ${source_base}/0_clean/*d/*_*/most_stable/relaxed; do
#     if [[ -d "$dir" ]]; then
#         IFS='/' read -r -a path <<< "$dir"
#         metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#         dest_dir="${destination_base}/${metal}N4C26/001"
#         mkdir -p "$dest_dir"
#         cp "$dir/final_with_calculator.json" "$dest_dir/"
#         echo "Copied final_with_calculator.json to $dest_dir"
#     else
#         echo "Directory does not exist: $dir"
#     fi
# done

for dir in ${source_base}/1_O/*_*/most_stable/relaxed; do
    if [[ -d "$dir" ]]; then
        IFS='/' read -r -a path <<< "$dir"
        metal=$(echo "${path[-3]}" | cut -d'_' -f2)
        dest_dir="${destination_base}/${metal}N4C26/001/M-site/O"
        mkdir -p "$dest_dir"
        cp "$dir/final_with_calculator.json" "$dest_dir/"
        echo "Copied final_with_calculator.json to $dest_dir"
    else
        echo "Directory does not exist: $dir"
    fi
done

for dir in ${source_base}/2_OH/*_*/most_stable/relaxed; do
    if [[ -d "$dir" ]]; then
        IFS='/' read -r -a path <<< "$dir"
        metal=$(echo "${path[-3]}" | cut -d'_' -f2)
        dest_dir="${destination_base}/${metal}N4C26/001/M-site/OH"
        mkdir -p "$dest_dir"
        cp "$dir/final_with_calculator.json" "$dest_dir/"
        echo "Copied final_with_calculator.json to $dest_dir"
    else
        echo "Directory does not exist: $dir"
    fi
done

for dir in ${source_base}/3_OOH/*_*/most_stable/relaxed; do
    if [[ -d "$dir" ]]; then
        IFS='/' read -r -a path <<< "$dir"
        metal=$(echo "${path[-3]}" | cut -d'_' -f2)
        dest_dir="${destination_base}/${metal}N4C26/001/M-site/OOH"
        mkdir -p "$dest_dir"
        cp "$dir/final_with_calculator.json" "$dest_dir/"
        echo "Copied final_with_calculator.json to $dest_dir"
    else
        echo "Directory does not exist: $dir"
    fi
done