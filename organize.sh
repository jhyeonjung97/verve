#!/bin/bash

source_base="/pscratch/sd/j/jiuy97/6_MNC"
destination_base="/pscratch/sd/j/jiuy97/cathub"
gas_path="/global/cfs/cdirs/m2997/Delowar/OER/MOF/data_storage_MOF/gas"
vasp_pbe="VASP-6.3.2/PBE+U+D3+VASPsol"
cd "${destination_base}" || exit 1

site1='M'
site2='N'
site3='D'

# dest_dir="${destination_base}/N4C26/001"
# mkdir -p "${dest_dir}/N"
# cp "${source_base}/empty/0_/final_with_calculator.json" "${dest_dir}/"
# cp "${source_base}/empty/2_/final_with_calculator.json" "${dest_dir}/N/"

# for dir in ${source_base}/0_clean/*d/*_*/most_stable; do
#     IFS='/' read -r -a path <<< "$dir"
#     metal=$(echo "${path[-2]}" | cut -d'_' -f2)
#     dest_dir="${destination_base}/${metal}N4C26/001"
#     mkdir -p "$dest_dir"
#     cp "$dir/relaxed/final_with_calculator.json" "$dest_dir/"
#     echo "Copied final_with_calculator.json to $dest_dir"
#     if [[ -f "${dir}/o/final_with_calculator.json" ]]; then
#         mkdir -p "${dest_dir}/${site1}/O"
#         cp "$dir/o/final_with_calculator.json" "$dest_dir/${site1}/O"
#         echo "Copied final_with_calculator.json to $dest_dir/${site1}/O"
#     fi
#     if [[ -f "${dir}/oh/final_with_calculator.json" ]]; then
#         mkdir -p "${dest_dir}/${site1}/OH"
#         cp "$dir/oh/final_with_calculator.json" "$dest_dir/${site1}/OH"
#         echo "Copied final_with_calculator.json to $dest_dir/${site1}/OH"
#     fi
#     if [[ -f "${dir}/ooh/final_with_calculator.json" ]]; then
#         mkdir -p "${dest_dir}/${site1}/OOH"
#         cp "$dir/ooh/final_with_calculator.json" "$dest_dir/${site1}/OOH"
#         echo "Copied final_with_calculator.json to $dest_dir/${site1}/OOH"
#     fi
# done

# for dir in ${source_base}/0_clean/*d/*_*/most_stable/relaxed; do
#     IFS='/' read -r -a path <<< "$dir"
#     metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#     dest_dir="${destination_base}/${metal}N4C26/001"
#     mkdir -p "$dest_dir"
#     cp "$dir/final_with_calculator.json" "$dest_dir/"
#     echo "Copied final_with_calculator.json to $dest_dir"
# done

# for dir in ${source_base}/1_O/*_*/most_stable/relaxed; do
#     IFS='/' read -r -a path <<< "$dir"
#     metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#     dest_dir="${destination_base}/${metal}N4C26/001/${site1}/O"
#     mkdir -p "$dest_dir"
#     cp "$dir/final_with_calculator.json" "$dest_dir/"
#     echo "Copied final_with_calculator.json to $dest_dir"
# done

# for dir in ${source_base}/2_OH/*_*/most_stable/relaxed; do
#     IFS='/' read -r -a path <<< "$dir"
#     metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#     dest_dir="${destination_base}/${metal}N4C26/001/${site1}/OH"
#     mkdir -p "$dest_dir"
#     cp "$dir/final_with_calculator.json" "$dest_dir/"
#     echo "Copied final_with_calculator.json to $dest_dir"
# done

# for dir in ${source_base}/3_OOH/*_*/most_stable/relaxed; do
#     IFS='/' read -r -a path <<< "$dir"
#     metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#     dest_dir="${destination_base}/${metal}N4C26/001/${site1}/OOH"
#     mkdir -p "$dest_dir"
#     cp "$dir/final_with_calculator.json" "$dest_dir/"
#     echo "Copied final_with_calculator.json to $dest_dir"
# done

# for dir in ${source_base}/pourbaix/*_*/*/most_stable; do
#     IFS='/' read -r -a path <<< "$dir"
#     metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#     ads=${path[-2]}
#     ads_upper=$(echo "$ads" | tr '[:lower:]' '[:upper:]')
#     if [[ "$ads_upper" == "MH" ]]; then
#         dest_dir="${destination_base}/${metal}N4C26/001/${site1}/H"
#     elif [[ "$ads_upper" == "NH" ]]; then
#         dest_dir="${destination_base}/${metal}N4C26/001/${site2}/H"
#     elif [[ "$ads_upper" == "O" ]] || [[ "$ads_upper" == "OH" ]] || [[ "$ads_upper" == "OOH" ]]; then
#         dest_dir="${destination_base}/${metal}N4C26/001/${site1}/${ads_upper}"
#     else
#         dest_dir=''
#     fi
#     if [[ -n "${dest_dir}" ]] && [[ -f "${dir}/final_with_calculator.json" ]]; then
#         mkdir -p "$dest_dir"
#         cp "${dir}/final_with_calculator.json" "${dest_dir}/"
#         echo "Copied final_with_calculator.json to ${dest_dir}"
#     fi
# done

# cp /global/homes/j/jiuy97/bin/verve/template* .
# cathub make-folders template
# # for dir in ${source_base}/0_clean/*d/*_*/most_stable/relaxed; do
# #     if [[ -d "$dir" ]]; then
# #         IFS='/' read -r -a path <<< "$dir"
# #         metal=$(echo "${path[-3]}" | cut -d'_' -f2)
# #         echo $metal
# #         sed "s/METAL/$metal/g" template-metal > template
# #         cathub make-folders template
# #         sed "s/METAL/$metal/g" template-metal-h2 > template
# #         cathub make-folders template
# #     fi
# # done
# # find ${destination_base} -path "*/MISSING:*" -delete

# for dir in *N4C26/; do
#     cathub organize "${dir%/}" -c VASP-6.3.2 -x PBE+U+D3+VASPsol -d "${gas_path}"
#     echo "Directory organized: ${dir_name}.organized"
# done

# dest_dir="${destination_base}/N4C26.organized/${vasp_pbe}/C26N4/001"
# mkdir -p "${dest_dir}/H2gas_star__2H@site2"
# cp "${destination_base}/N4C26/001/final_with_calculator.json" "${dest_dir}/empty_slab.json"
# cp "${destination_base}/N4C26/001/N/H2/final_with_calculator.json" "${dest_dir}/H2gas_star__2H@site2/H2.json"

# for dir in *N4C26.organized/${vasp_pbe}/*C26N4; do
#     if [[ -d "${dir}/001" ]] && [[ ! -d "${dir}/001@M" ]]; then
#         mv "${dir}/001" "${dir}/001@M"
#     fi
#     for sub_dir in ${dir}/001@M/*; do
#         if [[ ${sub_dir} == *'@site1' ]]; then
#             new_name="${sub_dir%@site1}"
#             mv "$sub_dir" "${dir}/001@M/${new_name##*/}"
#         elif [[ ${sub_dir} == *'@site2' ]]; then
#             mkdir -p "${dir}/001@N"
#             cp "${dir}/001@M/empty_slab.json" "${dir}/001@N"
#             new_name="${sub_dir%@site2}"
#             mv "$sub_dir" "${dir}/001@N/${new_name##*/}"
#         fi
#     done
# done
# rm -r "${destination_base}/N4C26.organized/${vasp_pbe}/C26N4/001@M"

# for dir in ${source_base}/pourbaix/*_*/*/most_stable; do
#     IFS='/' read -r -a path <<< "$dir"
#     metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#     ads=${path[-2]}
#     ads_upper=$(echo "$ads" | tr '[:lower:]' '[:upper:]')
#     if [[ "$ads_upper" == "OO" ]] || [[ "$ads_upper" == "O-O" ]]; then
#         rxn="2.0H2Ogas_-2.0H2gas_star__OstarOstar"
#     elif [[ "$ads_upper" == "OHO" ]] || [[ "$ads_upper" == "OH-O" ]]; then
#         rxn="2.0H2Ogas_-1.5H2gas_star__OHstarOstar"
#     elif [[ "$ads_upper" == "OHOH" ]] || [[ "$ads_upper" == "OH-OH" ]]; then
#         rxn="2.0H2Ogas_-1.0H2gas_star__OHstarOHstar"
#     elif [[ "$ads_upper" == "OOH-O" ]] ; then
#         rxn="3.0H2Ogas_-2.5H2gas_star__OOHstarOstar"
#     elif [[ "$ads_upper" == "OOH-OH" ]]; then
#         rxn="3.0H2Ogas_-2.0H2gas_star__OOHstarOHstar"
#     elif [[ "$ads_upper" == "OOH-OOH" ]]; then
#         rxn="4.0H2Ogas_-3.0H2gas_star__OOHstarOOHstar"
#     else
#         rxn=''
#     fi
#     if [[ -n ${rxn} ]] && [[ -f "${dir}/final_with_calculator.json" ]]; then
#         dest_dir="${destination_base}/${metal}N4C26.organized/${vasp_pbe}/${metal}C26N4/001@M"
#         mkdir -p ${dest_dir}/${rxn}
#         cp ${dir}/final_with_calculator.json ${dest_dir}/${rxn}
#     fi
# done

dest_dir="${destination_base}/JungTuning2025/VASP-6.3.2/PBE+U+D3+VASPsol"
mkdir -p "${dest_dir}"
for dir in "${destination_base}/*.organized/VASP-6.3.2/PBE+U+D3+VASPsol/*"; do
    if [[ ! ${dir} =~ '*gas' ]]; then
        cp -r ${dir} ${dest_dir}
    fi 
done

tree "${destination_base}/JungTuning2025.organized"
cp ~/bin/tools/mnc/publication.txt "${destination_base}/JungTuning2025/"
cathub folder2db JungTuning2025