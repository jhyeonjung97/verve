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
for dir in FeN4C26.organized/${vasp_pbe}/FeC26N4; do
    # mv "${dir}/001" "${dir}/001@M"
    for sub_dir in ${dir}/001@M/*; do
        if [[ ${sub_dir} == *'@site1' ]]; then
            new_name="${sub_dir%@site1}"
            echo $new_name
            # mv "$sub_dir" "${dir}/001@M/${new_name##*/}"
        elif [[ ${sub_dir} == *'@site2' ]]; then
            mkdir -p "${dir}/001@N"
            mv ${sub_dir} ${dir}/001@N
        fi
    done
done











# for dir in ${source_base}/pourbaix/*_*/*/most_stable; do
#     IFS='/' read -r -a path <<< "$dir"
#     metal=$(echo "${path[-3]}" | cut -d'_' -f2)
#     ads=${path[-2]}
#     ads_upper=$(echo "$ads" | tr '[:lower:]' '[:upper:]')
#     if [[ "$ads_upper" == "CLEAN" ]] || [[ "$ads_upper" == "TEMP" ]]; then
#         continue
#     elif [[ "$ads_upper" == "MH" ]] || [[ "$ads_upper" == "NH" ]]; then
#         continue
#     elif [[ "$ads_upper" == "O" ]] || [[ "$ads_upper" == "OH" ]] || [[ "$ads_upper" == "OOH" ]]; then
#         continue
#     elif [[ "$ads_upper" == "OHO" ]] || [[ "$ads_upper" == "OH-O" ]]; then
#         dest_dir="2.0H2Ogas_-1.5H2gas_star__OHstarOstar"
#     elif [[ "$ads_upper" == "OHOH" ]] || [[ "$ads_upper" == "OH-OH" ]]; then
#         dest_dir="2.0H2Ogas_-1.0H2gas_star__OHstarOHstar"
#     elif [[ "$ads_upper" == "OHOH" ]] || [[ "$ads_upper" == "OH-OH" ]]; then
#         dest_dir="2.0H2Ogas_-1.0H2gas_star__OHstarOHstar"









    
#     if [[ -f "$dir/final_with_calculator.json" ]]; then
#         mkdir -p "$dest_dir"
#         cp "$dir/final_with_calculator.json" "$dest_dir/"
#         echo "Copied final_with_calculator.json to $dest_dir"
#     fi
# done















# mv "${destination_base}/FeN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/FeC26N4/001/0.5H2gas_star__H@site1" "${destination_base}/FeN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/FeC26N4/001/0.5H2gas_star__H@site3"
# mv "${destination_base}/FeN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/FeC26N4/001/0.5H2gas_star__H@site2" "${destination_base}/FeN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/FeC26N4/001/0.5H2gas_star__H@site1"

# rm -r "${destination_base}/FeN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/FeC26N4/001/2.0H2Ogas_-1.5H2gas_star__OOH@site1"
# mv "${destination_base}/FeN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/FeC26N4/001/2.0H2Ogas_-1.5H2gas_star__OOH@site2" "${destination_base}/FeN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/FeC26N4/001/2.0H2Ogas_-1.5H2gas_star__OOH@site1"

# rm -r "${destination_base}/CoN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/CoC26N4/001/2.0H2Ogas_-1.5H2gas_star__OOH@site1"
# mv "${destination_base}/CoN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/CoC26N4/001/2.0H2Ogas_-1.5H2gas_star__OOH@site2" "${destination_base}/CoN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/CoC26N4/001/2.0H2Ogas_-1.5H2gas_star__OOH@site1"


# dual_path="/pscratch/sd/j/jiuy97/cathub/SampleFe2025/VASP-6.3.2/PBE+U+D3+VASPsol/FeC26N4_fcc/001"
# dual_metals=("Co" "Fe" "Mo")
# for metal in "${dual_metals[@]}"; do
#     json_dir="${destination_base}/${metal}N4C26/001/site2"
#     dest_dir="${destination_base}/${metal}N4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/${metal}C26N4/001"
#     mkdir -p "$dest_dir"
#     for dual_dir in "${dual_path}"/*/; do
#         dual_dir_name=$(basename "$dual_dir")       
#         pattern="${dual_dir_name##*__}"
#         ads1=$(echo "$pattern" | cut -d'_' -f1 | cut -d'@' -f1 | sed 's/star//g')
#         ads2=$(echo "$pattern" | cut -d'_' -f2 | cut -d'@' -f1 | sed 's/star//g')
#         dir_name="${ads1}-${ads2}"
#         if [[ -f "${json_dir}/${dir_name}/final_with_calculator.json" ]]; then
#             mkdir -p "${dest_dir}/${dual_dir_name}"
#             cp "${json_dir}/${dir_name}/final_with_calculator.json" "${dest_dir}/${dual_dir_name}"
#         fi
#     done
# done



# mv "${destination_base}/MoN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/MoC26N4/001/2.0H2Ogas_-1.0H2gas_star__OHstar@site1_OHstar@site2" "${destination_base}/MoN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/MoC26N4/001/2.0H2Ogas_-1.0H2gas_star__OHstar@site1_OHstar@site1"
# mv "${destination_base}/MoN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/MoC26N4/001/2.0H2Ogas_-1.5H2gas_star__OHstar@site1_Ostar@site2" "${destination_base}/MoN4C26.organized/VASP-6.3.2/PBE+U+D3+VASPsol/MoC26N4/001/2.0H2Ogas_-1.5H2gas_star__OHstar@site1_Ostar@site1"

# dest_dir="${destination_base}/JungTuning2025/VASP-6.3.2/PBE+U+D3+VASPsol"
# mkdir -p "${dest_dir}"
# for dir in "${destination_base}/*.organized/VASP-6.3.2/PBE+U+D3+VASPsol/*"; do
#     if [[ ! ${dir} =~ '*gas' ]]; then
#         echo ${dir}
#         cp -r ${dir} ${dest_dir}
#     fi 
# done

# cp "${destination_base}/SampleFe2025/publication.txt" "${destination_base}/JungTuning2025"
# mv "${destination_base}/JungTuning2025" "${destination_base}/JungTuning2025.organized"
# tree "${destination_base}/JungTuning2025.organized"