#!/bin/bash

mnc="/pscratch/sd/j/jiuy97/6_MNC"
vasp_pbe="VASP-6.3.2/PBE+U+D3+VASPsol"
cathub="${mnc}/JungTuning2025/${vasp_pbe}"
gas="/global/cfs/cdirs/m2997/Delowar/OER/MOF/data_storage_MOF/gas"
cd "${cathub_path}" || exit 1

site1='M'
site2='N'
site3='D'

for dir in ${mnc}/0_clean/*d/*_*/most_stable; do
    IFS='/' read -r -a path <<< "$dir"
    metal=$(echo "${path[-2]}" | cut -d'_' -f2)
    
    dest_dir="${cathub}/${metal}N4C26_relaxed/001-${site1}"
    mkdir -p "${dest_dir}"
    cp "${dir}/relaxed/final_with_calculator.json" "${dest_dir}/empty_slab.json"
    # echo "Copied relaxed/final_with_calculator.json to ${dest_dir}"
    
    dest_dir="${cathub}/${metal}N4C26_relaxed/001-${site1}/H2Ogas_-1.0H2gas_star__Ostar"
    mkdir -p "${dest_dir}"
    cp "${dir}/o/final_with_calculator.json" "${dest_dir}/O.json"
    # echo "Copied o/final_with_calculator.json to ${dest_dir}"
    
    dest_dir="${cathub}/${metal}N4C26_relaxed/001-${site1}/H2Ogas_-0.5H2gas_star__OHstar"
    mkdir -p "${dest_dir}"
    cp "${dir}/oh/final_with_calculator.json" "${dest_dir}/OH.json"
    # echo "Copied oh/final_with_calculator.json to ${dest_dir}"
    
    dest_dir="${cathub}/${metal}N4C26_relaxed/001-${site1}/2.0H2Ogas_-1.5H2gas_star__OOHstar"
    mkdir -p "${dest_dir}"
    cp "${dir}/ooh/final_with_calculator.json" "${dest_dir}/OOH.json"
    # echo "Copied ooh/final_with_calculator.json to ${dest_dir}"
    
    dzs=(0.0 0.2 0.4 0.6 0.8 1.0 1.2)
    for i in {0..6}; do
        dz=${dzs[$i]}
        dest_dir="${cathub}/${metal}N4C26_${dz}/001-${site1}"
        mkdir -p "${dest_dir}"
        cp "${dir}/${i}_/final_with_calculator.json" "${dest_dir}/empty_slab.json"
        # echo "Copied ${i}_/final_with_calculator.json to ${dest_dir}"
    done
done

for dir in ${mnc}/1_O/*_*/most_stable; do
    IFS='/' read -r -a path <<< "$dir"
    metal=$(echo "${path[-2]}" | cut -d'_' -f2)
    
    dest_dir="${cathub}/${metal}N4C26_relaxed/001-${site1}/H2Ogas_-1.0H2gas_star__Ostar"
    mkdir -p "${dest_dir}"
    cp "${dir}/relaxed/final_with_calculator.json" "${dest_dir}/O.json"
    # echo "Copied relaxed/final_with_calculator.json to ${dest_dir}"
    
    dzs=(0.0 0.2 0.4 0.6 0.8 1.0 1.2)
    for i in {0..6}; do
        dz=${dzs[$i]}
        dest_dir="${cathub}/${metal}N4C26_${dz}/001-${site1}/H2Ogas_-1.0H2gas_star__Ostar"
        mkdir -p "${dest_dir}"
        cp "${dir}/${i}_/final_with_calculator.json" "${dest_dir}/O.json"
        # echo "Copied ${i}_/final_with_calculator.json to ${dest_dir}"
    done
done

for dir in ${mnc}/2_OH/*_*/most_stable; do
    IFS='/' read -r -a path <<< "$dir"
    metal=$(echo "${path[-2]}" | cut -d'_' -f2)
    
    dest_dir="${cathub}/${metal}N4C26_relaxed/001-${site1}/H2Ogas_-0.5H2gas_star__OHstar"
    mkdir -p "${dest_dir}"
    cp "${dir}/relaxed/final_with_calculator.json" "${dest_dir}/OH.json"
    # echo "Copied relaxed/final_with_calculator.json to ${dest_dir}"
    
    dzs=(0.0 0.2 0.4 0.6 0.8 1.0 1.2)
    for i in {0..6}; do
        dz=${dzs[$i]}
        dest_dir="${cathub}/${metal}N4C26_${dz}/001-${site1}/H2Ogas_-0.5H2gas_star__OHstar"
        mkdir -p "${dest_dir}"
        cp "${dir}/${i}_/final_with_calculator.json" "${dest_dir}/OH.json"
        # echo "Copied ${i}_/final_with_calculator.json to ${dest_dir}"
    done
done

for dir in ${mnc}/3_OOH/*_*/most_stable; do
    IFS='/' read -r -a path <<< "$dir"
    metal=$(echo "${path[-2]}" | cut -d'_' -f2)
    
    dest_dir="${cathub}/${metal}N4C26_relaxed/001-${site1}/2.0H2Ogas_-1.5H2gas_star__OOHstar"
    mkdir -p "${dest_dir}"
    cp "${dir}/relaxed/final_with_calculator.json" "${dest_dir}/OOH.json"
    # echo "Copied relaxed/final_with_calculator.json to ${dest_dir}"
    
    dzs=(0.0 0.2 0.4 0.6 0.8 1.0 1.2)
    for i in {0..6}; do
        dz=${dzs[$i]}
        dest_dir="${cathub}/${metal}N4C26_${dz}/001-${site1}/2.0H2Ogas_-1.5H2gas_star__OOHstar"
        mkdir -p "${dest_dir}"
        cp "${dir}/${i}_/final_with_calculator.json" "${dest_dir}/OOH.json"
        # echo "Copied ${i}_/final_with_calculator.json to ${dest_dir}"
    done
done

for dir in ${mnc}/pourbaix/*_*/*/most_stable; do
    IFS='/' read -r -a path <<< "$dir"
    metal=$(echo "${path[-3]}" | cut -d'_' -f2)
    ads=${path[-2]}
    ads_upper=$(echo "$ads" | tr '[:lower:]' '[:upper:]')
    if [[ "$ads_upper" == "MH" ]]; then
        site_rxn="001-${site1}/0.5H2gas_star__Hstar"
    elif [[ "$ads_upper" == "NH" ]]; then
        site_rxn="001-${site2}/0.5H2gas_star__Hstar"
    elif [[ "$ads_upper" == "O" ]]; then
        site_rxn="001-${site1}/H2Ogas_-1.0H2gas_star__Ostar"
    elif [[ "$ads_upper" == "OH" ]]; then
        site_rxn="001-${site1}/H2Ogas_-0.5H2gas_star__OHstar"
    elif [[ "$ads_upper" == "OOH" ]]; then
        site_rxn="001-${site1}/2.0H2Ogas_-1.5H2gas_star__OOHstar"
    elif [[ "$ads_upper" == "OO" ]]; then
        site_rxn="001-${site1}/2.0H2Ogas_-2.0H2gas_star__OstarOstar"
    elif [[ "$ads_upper" == "OHO" ]]; then
        site_rxn="001-${site1}/2.0H2Ogas_-1.5H2gas_star__OHstarOstar"
    elif [[ "$ads_upper" == "OHOH" ]]; then
        site_rxn="001-${site1}/2.0H2Ogas_-1.0H2gas_star__OHstarOHstar"
    elif [[ "$ads_upper" == "OOHO" ]] || [[ "$ads_upper" == "OOOH" ]]; then
        site_rxn="001-${site1}/3.0H2Ogas_-2.5H2gas_star__OOHstarOstar"
    elif [[ "$ads_upper" == "OOHOH" ]] || [[ "$ads_upper" == "OHOOH" ]]; then
        site_rxn="001-${site1}/3.0H2Ogas_-2.0H2gas_star__OOHstarOHstar"
    elif [[ "$ads_upper" == "OOHOOH" ]]; then
        site_rxn="001-${site1}/4.0H2Ogas_-3.0H2gas_star__OOHstarOOHstar"
    elif [[ "$ads_upper" == "O-O" ]]; then
        site_rxn="001-${site3}/2.0H2Ogas_-2.0H2gas_star__OstarOstar"
    elif [[ "$ads_upper" == "OH-O" ]]; then
        site_rxn="001-${site3}/2.0H2Ogas_-1.5H2gas_star__OHstarOstar"
    elif [[ "$ads_upper" == "OH-OH" ]]; then
        site_rxn="001-${site3}/2.0H2Ogas_-1.0H2gas_star__OHstarOHstar"
    elif [[ "$ads_upper" == "OOH-O" ]]; then
        site_rxn="001-${site3}/3.0H2Ogas_-2.5H2gas_star__OOHstarOstar"
    elif [[ "$ads_upper" == "OOH-OH" ]]; then
        site_rxn="001-${site3}/3.0H2Ogas_-2.0H2gas_star__OOHstarOHstar"
    elif [[ "$ads_upper" == "OOH-OOH" ]]; then
        site_rxn="001-${site3}/4.0H2Ogas_-3.0H2gas_star__OOHstarOOHstar"
    else
        site_rxn=''
    fi
    if [[ -n "${site_rxn}" ]] && [[ -f "${dir}/final_with_calculator.json" ]]; then
        dest_dir="${cathub}/${metal}N4C26_relaxed/${site_rxn}"
        mkdir -p "${dest_dir}"
        cp "${dir}/final_with_calculator.json" "${dest_dir}"
        # echo "Copied final_with_calculator.json to ${dest_dir}"
    fi
done

find ${cathub} -type d -empty -delete