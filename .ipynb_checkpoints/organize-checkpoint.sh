#!/bin/bash

source_base="/pscratch/sd/j/jiuy97/6_MNC"
destination_base="/pscratch/sd/j/jiuy97/cathub"

site1='site1'
site2='site2'
site3='site3'

dest_dir="${destination_base}/N4C26/001"
mkdir -p "$dest_dir"
cp "${source_base}/empty/0_/final_with_calculator.json" "$dest_dir/"

dest_dir="${destination_base}/H2N4C26/001"
mkdir -p "$dest_dir"
cp "${source_base}/empty/2_/final_with_calculator.json" "$dest_dir/"

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

gas_path="/global/cfs/cdirs/m2997/Delowar/OER/MOF/data_storage_MOF/gas"
cd "${destination_base}" || exit 1
for dir in */; do
    dir_name=$(basename "$dir")
    if [[ -d "${dir_name}/001/site1" ]]; then
        if [[ ! -d "${dir_name}.organized" ]]; then
            cathub organize "${dir%/}" -c VASP-6.3.2 -x PBE+U+D3+VASPsol -d "${gas_path}"
            echo "Directory organized: ${dir_name}.organized"
        fi
    # else  
    fi
done

cp /global/homes/j/jiuy97/bin/verve/template .
cathub make-folders template
cp /global/homes/j/jiuy97/bin/verve/template-metal .
for dir in ${source_base}/0_clean/*d/*_*/most_stable/relaxed; do
    if [[ -d "$dir" ]]; then
        IFS='/' read -r -a path <<< "$dir"
        metal=$(echo "${path[-3]}" | cut -d'_' -f2)
        echo $metal
        sed "s/METAL/$metal/g" template-metal > template
        cathub make-folders template
        sed "s/METAL/$metal/g" template-metal-h2 > template
        cathub make-folders template
    fi
done
find ${destination_base} -path "*/MISSING:*" -delete


# for dir in ${source_base}/0_clean/*d/*_*/most_stable/relaxed; do
#     if [[ -d "$dir" ]]; then
#         IFS='/' read -r -a path <<< "$dir"
#         metal=$(echo "${path[-3]}" | cut -d'_' -f2)
        
#         dest_dir="${destination_base}/${metal}N4C26/001/${site1}/H"

        
#         dest_dir="${destination_base}/${metal}N4C26/001"
#         mkdir -p "$dest_dir"
#         cp "$dir/final_with_calculator.json" "$dest_dir/"
#         echo "Copied final_with_calculator.json to $dest_dir"
#     else
#         echo "Directory does not exist: $dir"
#     fi
# done

# # dual_path="/pscratch/sd/j/jiuy97/cathub/JungTuning2025/VASP-6.3.2/PBE+U+D3+VASPsol/FeC26N4_fcc/001"
# # dual_metals=("Co" "Fe" "Mo")
# # for metal in "${dual_metals[@]}"; do
# #     json_dir="${destination_base}/${metal}N4C26/001/site2"
# #     dest_dir="${destination_base}/${metal}N4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/${metal}C26N4/001"
# #     mkdir -p "$dest_dir"
# #     for dual_dir in "${dual_path}"/*; do
# #         dual_dir_name=$(basename "$dual_dir")       
# #         pattern="${dual_dir_name##*__}"
# #         ads1=$(echo "$pattern" | cut -d'_' -f1 | cut -d'@' -f1 | sed 's/star//g')
# #         ads2=$(echo "$pattern" | cut -d'_' -f2 | cut -d'@' -f1 | sed 's/star//g')
# #         dir_name="${ads1}-${ads2}"
# #         if [[ -f "${json_dir}/${dir_name}/final_with_calculator.json" ]]; then
# #             mkdir -p "${dest_dir}/${dual_dir_name}"
# #             cp "${json_dir}/${dir_name}/final_with_calculator.json" "${dest_dir}/${dual_dir_name}"
# #         fi
# #     done
# # done

# tree *.organized
