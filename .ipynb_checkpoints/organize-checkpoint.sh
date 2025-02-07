#!/bin/bash

source_base="/pscratch/sd/j/jiuy97/6_MNC"
destination_base="/pscratch/sd/j/jiuy97/cathub"

dest_dir="${destination_base}/N4C26/001"
mkdir -p "$dest_dir"
cp "${source_base}/empty/0_/final_with_calculator.json" "$dest_dir/"

dest_dir="${destination_base}/H2N4C26/001"
mkdir -p "$dest_dir"
cp "${source_base}/empty/2_/final_with_calculator.json" "$dest_dir/"

site1='site1'
site2='site2'
site3='site3'

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

# for dir in ${source_base}/1_O/*_*/most_stable/relaxed; do
#     if [[ -d "$dir" ]]; then
#         IFS='/' read -r -a path <<< "$dir"
#         metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#         dest_dir="${destination_base}/${metal}N4C26/001/${site1}/O"
#         mkdir -p "$dest_dir"
#         cp "$dir/final_with_calculator.json" "$dest_dir/"
#         echo "Copied final_with_calculator.json to $dest_dir"
#     else
#         echo "Directory does not exist: $dir"
#     fi
# done

# for dir in ${source_base}/2_OH/*_*/most_stable/relaxed; do
#     if [[ -d "$dir" ]]; then
#         IFS='/' read -r -a path <<< "$dir"
#         metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#         dest_dir="${destination_base}/${metal}N4C26/001/${site1}/OH"
#         mkdir -p "$dest_dir"
#         cp "$dir/final_with_calculator.json" "$dest_dir/"
#         echo "Copied final_with_calculator.json to $dest_dir"
#     else
#         echo "Directory does not exist: $dir"
#     fi
# done

# for dir in ${source_base}/3_OOH/*_*/most_stable/relaxed; do
#     if [[ -d "$dir" ]]; then
#         IFS='/' read -r -a path <<< "$dir"
#         metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#         dest_dir="${destination_base}/${metal}N4C26/001/${site1}/OOH"
#         mkdir -p "$dest_dir"
#         cp "$dir/final_with_calculator.json" "$dest_dir/"
#         echo "Copied final_with_calculator.json to $dest_dir"
#     else
#         echo "Directory does not exist: $dir"
#     fi
# done

# for dir in ${source_base}/pourbaix/*_*/*/most_stable; do
#     if [[ -d "$dir" ]]; then
#         IFS='/' read -r -a path <<< "$dir"
#         metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#         ads=${path[-2]}
#         ads_upper=$(echo "$ads" | tr '[:lower:]' '[:upper:]')
#         if [[ "$ads_upper" == "CLEAN" ]] || [[ "$ads_upper" == "TEMP" ]] || [[ "$ads_upper" == "O-OH" ]]; then
#             continue
#         elif [[ "$ads_upper" == "MH" ]]; then
#             dest_dir="${destination_base}/${metal}N4C26/001/${site1}/H"
#         elif [[ "$ads_upper" == "NH" ]]; then
#             dest_dir="${destination_base}/${metal}N4C26/001/${site3}/H"
#         elif [[ "$ads" =~ .*-.+ ]]; then
#             dest_dir="${destination_base}/${metal}N4C26/001/${site2}/${ads_upper}"
#         else
#             dest_dir="${destination_base}/${metal}N4C26/001/${site1}/${ads_upper}"
#         fi
#         if [[ -f "$dir/final_with_calculator.json" ]]; then
#             mkdir -p "$dest_dir"
#             cp "$dir/final_with_calculator.json" "$dest_dir/"
#             echo "Copied final_with_calculator.json to $dest_dir"
#         fi
#     else
#         echo "Directory does not exist: $dir"
#     fi
# done

# gas_path="/global/cfs/cdirs/m2997/Delowar/OER/MOF/data_storage_MOF/gas"
# cd "${destination_base}" || exit 1
# for dir in */; do
#     cathub organize "${dir%/}" -c VASP-6.3.2 -x PBE+U+D3+VASPsol -d "${gas_path}"
# done
# cp /global/homes/j/jiuy97/bin/verve/template .
# cathub make-folders template
# find ${destination_base} -path "*/MISSING:*" -delete

dual_path="/pscratch/sd/j/jiuy97/cathub/JungTuning2025/VASP-6.3.2/PBE+U+D3+VASPsol/FeC26N4_fcc/001"
dual_metals=("Co" "Fe" "Mo")
for metal in "${dual_metals[@]}"; do
    dest_dir="${destination_base}/${metal}N4C26/001/site2"
    mkdir -p "$dest_dir"
    for sub_dir in "${dual_path}"/*: do
        echo $dir_name
        dir_name=$(basename "$sub_dir")       
        pattern="${dir_name##*__}"
        ads1=$(echo "$pattern" | cut -d'_' -f1 | sed 's/star//g')
        ads2=$(echo "$pattern" | cut -d'_' -f2 | sed 's/star//g')
        result="${ads1}-${ads2}"
        echo "$result"
    done
    # cp -r "${dual_path}/"* "$dest_dir/"
    # echo "Copied files to $dest_dir"
done