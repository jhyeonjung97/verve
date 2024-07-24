#!/bin/bash
if [[ ${here} == 'slac' ]]; then
    /usr/bin/rsync -e 'ssh' --ignore-times --size-only -avlzp -K --max-size=50000m \
    	--include="*/" \
    	--include="*.png" \
    	--exclude="*" \
     jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/3_V_shape .
elif [[ ${here} == 'nersc' ]]; then   
    # for dir in /pscratch/sd/j/jiuy97/3_V_shape/metal/*/; do
    #     cd $dir
    #     python ~/bin/verve/energy.py --save -x "Metal (M)" -y "Total energy (eV/M)" -n m
    # done
    # cd /pscratch/sd/j/jiuy97/3_V_shape/metal
    # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Total energy (eV)" -o norm_energy *fm/energy_norm_energy.tsv *d/energy_norm_energy.tsv
    # cd /pscratch/sd/j/jiuy97/3_V_shape/oxide/0_min
    # python ~/bin/verve/energy.py --save -x "Metal (MxOy)" -y "Total energy (eV/M)" -n m
    # for dir in /pscratch/sd/j/jiuy97/3_V_shape/*_*_*/*/; do
    #     if [[ $dir != *'save'* ]] && [[ $dir != *'rhom'* ]] && [[ $dir != *'bin'* ]] && [[ $dir != *'cubic'* ]]; then
    #         cd $dir
    #         if [[ $dir == *'Tetrahedral'* ]]; then
    #             n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Hexagonal ratio [c/a]"
    #         elif [[ $dir == *'Pyramidal'* ]] || [[ $dir == *'Tetragonal'* ]] || [[ $dir == *'Square_Planar'* ]]; then
    #             n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Square prism ratio [c/a]"
    #         elif [[ $dir == *'Octahedral'* ]]; then
    #             n=6
    #         fi
    #         python ~/bin/verve/energy.py --save -p energy -x "Metal (MO)" -y "Total energy (eV)"
    #         python ~/bin/verve/energy.py --save -p energy -x "Metal (MO)" -y "Total energy (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p bond  -x "Metal (MO)" -y "Bond length (A)"
    #         python ~/bin/verve/energy.py --save -p bond -x "Metal (MO)" -y "Bond length (A/M-O)" -n $n
    #         python ~/bin/verve/energy.py --save -p volume -x "Metal (MO)" -y "Volume (A^3/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p chg -e M  -x "Metal (MO)" -y "Bader charge (e-)"
    #         python ~/bin/verve/energy.py --save -p mag -e M -x "Metal (MO)" -y "|Magnetization|"
    #         python ~/bin/verve/energy.py --save -p ICOHP -x "Metal (MO)" -y "ICOHP (eV/MO)"
    #         python ~/bin/verve/energy.py --save -p ICOHP -x "Metal (MO)" -y "ICOHP (eV/M-O)" -n $n
    #         python ~/bin/verve/energy.py --save -p ICOBI -x "Metal (MO)" -y "ICOBI (/MO)"
    #         python ~/bin/verve/energy.py --save -p ICOBI -x "Metal (MO)" -y "ICOBI (eV/M-O)" -n $n
    #         python ~/bin/verve/energy.py --save -p GP_L -e M  -x "Metal (MO)" -y "Gross population (Loewdin)"
    #         python ~/bin/verve/energy.py --save -p Madelung_L -x "Metal (MO)" -y "Madelugn energy (Loewdin, eV/MO)" -n m
    #         python ~/bin/verve/formation_energy.py
    #         # python ~/bin/verve/energy.py --save -p area -x "Metal (MO)" -y "Area (A^2)"
    #         # python ~/bin/verve/energy.py --save -p PSCENC -x "Metal (MO)" -y "PSCENC (eV/MO)" -n m
    #         # python ~/bin/verve/energy.py --save -p TEWEN -x "Metal (MO)" -y "TEWEN (eV/MO)" -n m
    #         # python ~/bin/verve/energy.py --save -p DENC -x "Metal (MO)" -y "DENC (eV/MO)" -n m
    #         # python ~/bin/verve/energy.py --save -p EXHF -x "Metal (MO)" -y "EXHF (eV/MO)" -n m
    #         # python ~/bin/verve/energy.py --save -p XCENC -x "Metal (MO)" -y "XCENC (eV/MO)" -n m
    #         # python ~/bin/verve/energy.py --save -p PAW_double_counting -x "Metal (MO)" -y "PAW_double_counting (eV/MO)" -n m
    #         # python ~/bin/verve/energy.py --save -p EENTRO -x "Metal (MO)" -y "EENTRO (eV/MO)" -n m
    #         # python ~/bin/verve/energy.py --save -p EBANDS -x "Metal (MO)" -y "EBANDS (eV/MO)" -n m
    #         # python ~/bin/verve/energy.py --save -p EATOM -x "Metal (MO)" -y "EATOM (eV/MO)" -n m
    #         sed -i 's/\x0//g' *.tsv
    #         cd $dir_now
    #     fi
    # done
    for dir in /pscratch/sd/j/jiuy97/3_V_shape/*_*_*/; do
        cd $dir
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Total energy (eV)" \
        -o energy 1_afm/energy_energy.tsv 4d/energy_energy.tsv 5d/energy_energy.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Total energy (eV/MO)" \
        -o norm_energy 1_afm/energy_norm_energy.tsv 4d/energy_norm_energy.tsv 5d/energy_norm_energy.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Bond length (A/M-O)" \
    #     -o bond 1_afm/energy_bond.tsv 4d/energy_bond.tsv 5d/energy_bond.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Bond length (A/M-O)" \
    #     -o norm_bond 1_afm/energy_norm_bond.tsv 4d/energy_norm_bond.tsv 5d/energy_norm_bond.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Volume (A^3/MO)" \
    #     -o norm_volume 1_afm/energy_norm_volume.tsv 4d/energy_norm_volume.tsv 5d/energy_norm_volume.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Bader charge (e-)" \
    #     -o chg 1_afm/energy_chg_M.tsv 4d/energy_chg_M.tsv 5d/energy_chg_M.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "|Magnetization|" \
    #     -o mag_M 1_afm/energy_mag_M.tsv 4d/energy_mag_M.tsv 5d/energy_mag_M.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/MO)" \
    #     -o ICOHP 1_afm/energy_ICOHP.tsv 4d/energy_ICOHP.tsv 5d/energy_ICOHP.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/M-O)" \
    #     -o norm_ICOHP 1_afm/energy_norm_ICOHP.tsv 4d/energy_norm_ICOHP.tsv 5d/energy_norm_ICOHP.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "ICOBI (/MO)" \
    #     -o ICOBI 1_afm/energy_ICOBI.tsv 4d/energy_ICOBI.tsv 5d/energy_ICOBI.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "ICOBI (/M-O)" \
    #     -o norm_ICOBI 1_afm/energy_ICOBI.tsv 4d/energy_norm_ICOBI.tsv 5d/energy_norm_ICOBI.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Gross population (Loewdin)" \
    #     -o GP_L_M 1_afm/energy_GP_Loewdin_M.tsv 4d/energy_GP_Loewdin_M.tsv 5d/energy_GP_Loewdin_M.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" \
    #     -o norm_Madelung_L 1_afm/energy_norm_Madelung_Loewdin.tsv 4d/energy_norm_Madelung_Loewdin.tsv 5d/energy_norm_Madelung_Loewdin.tsv
        
    #     python ~/bin/verve/tsv.py -l 3d_AFM 3d_FM -x "Metal (MO)" -y "Formation energy (eV/MO)" -o AFMvsFM *_*fm/energy_norm_formation.tsv
    #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Formation energy (eV/MO)" \
    #     -o norm_formation 1_afm/energy_norm_formation.tsv 4d/energy_norm_formation.tsv 5d/energy_norm_formation.tsv
        
    #     if [[ $dir == *'Octahedral'* ]]; then
    #         python ~/bin/verve/mendeleev2tsv.py -p atomic_number atomic_volume boiling_point covalent_radius density dipole_polarizability en_pauling evaporation_heat fusion_heat group_id heat_of_formation ionenergies[1] ionenergies[2] ionenergies[3] mass melting_point metallic_radius vdw_radius
    #     fi
        
    #     # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "PSCENC (eV/MO)" \
    #     # -o norm_PSCENC 1_afm/energy_norm_PSCENC.tsv 4d/energy_norm_PSCENC.tsv 5d/energy_norm_PSCENC.tsv
    #     # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "TEWEN (eV/MO)" \
    #     # -o norm_TEWEN 1_afm/energy_norm_TEWEN.tsv 4d/energy_norm_TEWEN.tsv 5d/energy_norm_TEWEN.tsv
    #     # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "DENC (eV/MO)" \
    #     # -o norm_DENC 1_afm/energy_norm_DENC.tsv 4d/energy_norm_DENC.tsv 5d/energy_norm_DENC.tsv
    #     # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "EXHF (eV/MO)" \
    #     # -o norm_EXHF 1_afm/energy_norm_EXHF.tsv 4d/energy_norm_EXHF.tsv 5d/energy_norm_EXHF.tsv
    #     # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "XCENC (eV/MO)" \
    #     # -o norm_XCENC 1_afm/energy_norm_XCENC.tsv 4d/energy_norm_XCENC.tsv 5d/energy_norm_XCENC.tsv
    #     # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "PAW_double_counting (eV/MO)" \
    #     # -o norm_PAW_double_counting 1_afm/energy_norm_PAW_double_counting.tsv 4d/energy_norm_PAW_double_counting.tsv 5d/energy_norm_PAW_double_counting.tsv
    #     # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "EENTRO (eV/MO)" \
    #     # -o norm_EENTRO 1_afm/energy_norm_EENTRO.tsv 4d/energy_norm_EENTRO.tsv 5d/energy_norm_EENTRO.tsv
    #     # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "EBANDS (eV/MO)" \
    #     # -o norm_EBANDS 1_afm/energy_norm_EBANDS.tsv 4d/energy_norm_EBANDS.tsv 5d/energy_norm_EBANDS.tsv
    #     # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "EATOM (eV/MO)" \
    #     # -o norm_EATOM 1_afm/energy_norm_EATOM.tsv 4d/energy_norm_EATOM.tsv 5d/energy_norm_EATOM.tsv
    done
    
    cd /pscratch/sd/j/jiuy97/3_V_shape
    # rows=('3d' '4d' '5d')
    # dirs=('1_afm' '4d' '5d')
    # for i in {0..2}; do
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "Total energy (eV)" -o energy_${rows[$i]} *_*_*/${dirs[$i]}/energy_energy.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "Total energy (eV/MO)" -o norm_energy_${rows[$i]} *_*_*/${dirs[$i]}/energy_norm_energy.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "Bond length (A/M-O)" -o bond_${rows[$i]} *_*_*/${dirs[$i]}/energy_bond.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "Volume (A^3/MO)" -o norm_volume_${rows[$i]} *_*_*/${dirs[$i]}/energy_norm_volume.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "Bader charge (e-)" -o chg_M_${rows[$i]} *_*_*/${dirs[$i]}/energy_chg_M.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "|Magnetization|" -o mag_M_${rows[$i]} *_*_*/${dirs[$i]}/energy_mag_M.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "ICOHP (eV/MO)" -o ICOHP_${rows[$i]} *_*_*/${dirs[$i]}/energy_ICOHP.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_${rows[$i]} *_*_*/${dirs[$i]}/energy_norm_ICOHP.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "ICOBI (/MO)" -o ICOBI_${rows[$i]} *_*_*/${dirs[$i]}/energy_ICOBI.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "ICOBI (/M-O)" -o norm_ICOBI_${rows[$i]} *_*_*/${dirs[$i]}/energy_norm_ICOBI.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "Gross population (Loewdin)" -o GP_L_${rows[$i]} *_*_*/${dirs[$i]}/energy_GP_Loewdin_M.tsv
    #     python ~/bin/verve/tsv.py -r ${rows[$i]} -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_Madelung_L_${rows[$i]} *_*_*/${dirs[$i]}/energy_norm_Madelung_Loewdin.tsv
    # done
    
    python ~/bin/verve/concat.py -o energy --X *_*_*/merged_energy.tsv
    python ~/bin/verve/concat.py -o norm_energy --X *_*_*/merged_norm_energy.tsv
    python ~/bin/verve/concat.py -o norm_formation --X *_*_*/merged_norm_formation.tsv
    python ~/bin/verve/concat.py -o ICOHP --X *_*_*/merged_ICOHP.tsv
    python ~/bin/verve/concat.py -o norm_ICOHP --X *_*_*/merged_norm_ICOHP.tsv
    python ~/bin/verve/concat.py -o ICOBI --X *_*_*/merged_ICOBI.tsv
    python ~/bin/verve/concat.py -o norm_ICOHP --X *_*_*/merged_norm_ICOHP.tsv
    python ~/bin/verve/concat.py -o bond --X *_*_*/merged_bond.tsv
    python ~/bin/verve/concat.py -o norm_bond --X *_*_*/merged_norm_bond.tsv
    python ~/bin/verve/concat.py -o norm_volume --X *_*_*/merged_norm_volume.tsv
    python ~/bin/verve/concat.py -o chg --X *_*_*/merged_chg.tsv
    python ~/bin/verve/concat.py -o mag --X *_*_*/merged_mag_M.tsv
    python ~/bin/verve/concat.py -o norm_MadelungL --X *_*_*/merged_norm_Madelung_L.tsv
    python ~/bin/verve/concat.py -o GrossPopulationL --X *_*_*/merged_GP_L_M.tsv
    
    # python ~/bin/verve/rel2octa.py concat_norm_formation.tsv
    # python ~/bin/verve/rel2octa.py concat_ICOHP_per_MO.tsv
    # python ~/bin/verve/rel2octa.py concat_ICOHP_per_bond.tsv
    # python ~/bin/verve/rel2octa.py concat_ICOBI.tsv
    # python ~/bin/verve/rel2octa.py concat_norm_MadelungL.tsv
    # python ~/bin/verve/rel2octa.py concat_GrossPopulationL.tsv
    # python ~/bin/verve/rel2octa.py concat_norm_volume.tsv
    # python ~/bin/verve/rel2octa.py concat_bond.tsv
    # python ~/bin/verve/rel2octa.py concat_chg.tsv
    # python ~/bin/verve/rel2octa.py concat_redoxP.tsv
    # python ~/bin/verve/rel2octa.py concat_redoxP_clean.tsv
    # python ~/bin/verve/rel2octa.py concat_norm_cohesive.tsv
    

    
    # python ~/bin/verve/lr.py -i \
    # ICOHP_per_bond \
    # ICOHP_per_MO \
    # ICOBI \
    # MadelungL \
    # GrossPopulationL \
    # volume \
    # bond \
    # chg \
    # atomic_number \
    # group_id \
    # row \
    # mass \
    # atomic_volume \
    # redoxP \
    # ionenergies1 \
    # ionenergies2 \
    # ionenergies12 \
    # ionenergies3 \
    # dipole_polarizability \
    # en_pauling \
    # density \
    # covalent_radius \
    # metallic_radius \
    # vdw_radius \
    # melting_point \
    # boiling_point \
    # sublimation_heat \
    # fusion_heat \
    # --Y concat_norm_formation.tsv \
    # --X \
    # concat_ICOHP_per_bond.tsv \
    # concat_ICOHP_per_MO.tsv \
    # concat_ICOBI.tsv \
    # concat_norm_MadelungL.tsv \
    # concat_GrossPopulationL.tsv \
    # concat_norm_volume.tsv \
    # concat_bond.tsv \
    # concat_chg.tsv \
    # concat_atomic_number.tsv \
    # concat_group_id.tsv \
    # concat_row.tsv \
    # concat_mass.tsv \
    # concat_atomic_volume.tsv \
    # concat_redoxP.tsv \
    # concat_ionenergies_1.tsv \
    # concat_ionenergies_2.tsv \
    # concat_ionenergies_12.tsv \
    # concat_ionenergies_3.tsv \
    # concat_dipole_polarizability.tsv \
    # concat_en_pauling.tsv \
    # concat_density.tsv \
    # concat_covalent_radius.tsv \
    # concat_metallic_radius.tsv \
    # concat_vdw_radius.tsv \
    # concat_melting_point.tsv \
    # concat_boiling_point.tsv \
    # concat_sublimation.tsv \
    # concat_fusion_heat.tsv
    
    # python ~/bin/verve/lr.py -o Ec -i \
    # ICOHP_per_bond \
    # ICOHP_per_MO \
    # ICOBI \
    # MadelungL \
    # GrossPopulationL \
    # volume \
    # bond \
    # chg \
    # atomic_number \
    # group_id \
    # row \
    # mass \
    # atomic_volume \
    # ionenergies1 \
    # ionenergies2 \
    # ionenergies12 \
    # ionenergies3 \
    # dipole_polarizability \
    # en_pauling \
    # density \
    # covalent_radius \
    # metallic_radius \
    # vdw_radius \
    # melting_point \
    # boiling_point \
    # sublimation_heat \
    # fusion_heat \
    # --Y concat_norm_cohesive.tsv \
    # --X \
    # concat_ICOHP_per_bond.tsv \
    # concat_ICOHP_per_MO.tsv \
    # concat_ICOBI.tsv \
    # concat_norm_MadelungL.tsv \
    # concat_GrossPopulationL.tsv \
    # concat_norm_volume.tsv \
    # concat_bond.tsv \
    # concat_chg.tsv \
    # concat_atomic_number.tsv \
    # concat_group_id.tsv \
    # concat_row.tsv \
    # concat_mass.tsv \
    # concat_atomic_volume.tsv \
    # concat_ionenergies_1.tsv \
    # concat_ionenergies_2.tsv \
    # concat_ionenergies_12.tsv \
    # concat_ionenergies_3.tsv \
    # concat_dipole_polarizability.tsv \
    # concat_en_pauling.tsv \
    # concat_density.tsv \
    # concat_covalent_radius.tsv \
    # concat_metallic_radius.tsv \
    # concat_vdw_radius.tsv \
    # concat_melting_point.tsv \
    # concat_boiling_point.tsv \
    # concat_sublimation.tsv \
    # concat_fusion_heat.tsv
    
    # python ~/bin/verve/lr.py -o Ec -i \
    # ICOHP_per_bond \
    # ICOHP_per_MO \
    # ICOBI \
    # MadelungL \
    # GrossPopulationL \
    # volume \
    # bond \
    # chg \
    # atomic_number \
    # group_id \
    # row \
    # mass \
    # atomic_volume \
    # ionenergies1 \
    # ionenergies2 \
    # ionenergies12 \
    # ionenergies3 \
    # dipole_polarizability \
    # en_pauling \
    # density \
    # covalent_radius \
    # metallic_radius \
    # vdw_radius \
    # melting_point \
    # boiling_point \
    # sublimation_heat \
    # fusion_heat \
    # --Y concat_norm_cohesive.tsv \
    # --X \
    # concat_ICOHP_per_bond.tsv \
    # concat_ICOHP_per_MO.tsv \
    # concat_ICOBI.tsv \
    # concat_norm_MadelungL.tsv \
    # concat_GrossPopulationL.tsv \
    # concat_norm_volume.tsv \
    # concat_bond.tsv \
    # concat_chg.tsv \
    # concat_atomic_number.tsv \
    # concat_group_id.tsv \
    # concat_row.tsv \
    # concat_mass.tsv \
    # concat_atomic_volume.tsv \
    # concat_ionenergies_1.tsv \
    # concat_ionenergies_2.tsv \
    # concat_ionenergies_12.tsv \
    # concat_ionenergies_3.tsv \
    # concat_dipole_polarizability.tsv \
    # concat_en_pauling.tsv \
    # concat_density.tsv \
    # concat_covalent_radius.tsv \
    # concat_metallic_radius.tsv \
    # concat_vdw_radius.tsv \
    # concat_melting_point.tsv \
    # concat_boiling_point.tsv \
    # concat_sublimation.tsv \
    # concat_fusion_heat.tsv
    
    # python ~/bin/verve/lr.py -o Ec_rel -i \
    # ICOHP_per_bond_rel \
    # ICOHP_per_MO_rel \
    # ICOBI_rel \
    # MadelungL_rel \
    # GrossPopulationL_rel \
    # volume_rel \
    # bond_rel \
    # chg_rel \
    # atomic_number \
    # group_id \
    # row \
    # mass \
    # atomic_volume \
    # ionenergies1 \
    # ionenergies2 \
    # ionenergies12 \
    # ionenergies3 \
    # dipole_polarizability \
    # en_pauling \
    # density \
    # covalent_radius \
    # metallic_radius \
    # vdw_radius \
    # melting_point \
    # boiling_point \
    # sublimation_heat \
    # fusion_heat \
    # --Y concat_norm_cohesive_rel.tsv \
    # --X \
    # concat_ICOHP_per_bond_rel.tsv \
    # concat_ICOHP_per_MO_rel.tsv \
    # concat_ICOBI_rel.tsv \
    # concat_norm_MadelungL_rel.tsv \
    # concat_GrossPopulationL_rel.tsv \
    # concat_norm_volume_rel.tsv \
    # concat_bond_rel.tsv \
    # concat_chg_rel.tsv \
    # concat_atomic_number.tsv \
    # concat_group_id.tsv \
    # concat_row.tsv \
    # concat_mass.tsv \
    # concat_atomic_volume.tsv \
    # concat_ionenergies_1.tsv \
    # concat_ionenergies_2.tsv \
    # concat_ionenergies_12.tsv \
    # concat_ionenergies_3.tsv \
    # concat_dipole_polarizability.tsv \
    # concat_en_pauling.tsv \
    # concat_density.tsv \
    # concat_covalent_radius.tsv \
    # concat_metallic_radius.tsv \
    # concat_vdw_radius.tsv \
    # concat_melting_point.tsv \
    # concat_boiling_point.tsv \
    # concat_sublimation.tsv \
    # concat_fusion_heat.tsv

    # python ~/bin/verve/gpr.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv
    # python ~/bin/verve/gpr-optuna.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv
    
    # python ~/bin/verve/gpr.py -o gpu -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv
    # python ~/bin/verve/gpr-optuna.py -o gpu -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv
    
    # python ~/bin/verve/gbr.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv
    # python ~/bin/verve/gbr-optuna.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv 
    
    # python ~/bin/verve/gbr.py -o gpu -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv 
    # python ~/bin/verve/gbr-optuna.py -o gpu -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv  
    
    # python ~/bin/verve/nn-hyperopt.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv 
    
    # python ~/bin/verve/nn-hyperopt.py -o gpu -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv 

    # python ~/bin/verve/gbr-optuna.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv  

    # python ~/bin/verve/nn-hyperopt.py -i ICOHP wICOHP ICOBI MadelungL volume bond chg GP_L CFSE IE1 IE2 IE12 redoxP IE3 E_sub row group number negativity melting boiling density mass --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_wICOHP.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_GP_L.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE12.tsv concat_redoxP.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv concat_number.tsv concat_neg.tsv concat_melting.tsv concat_boiling.tsv concat_density.tsv concat_mass.tsv 


    # python ~/bin/verve/gbr-optuna.py -i ICOHP_per_bond ICOHP_per_MO ICOBI MadelungL GrossPopulationL volume bond chg atomic_number group_id row mass atomic_volume ionenergies1 ionenergies2 ionenergies12 ionenergies3 dipole_polarizability en_pauling density covalent_radius metallic_radius vdw_radius melting_point boiling_point heat_of_formation sublimation_heat evaporation_heat fusion_heat --Y concat_norm_formation_rel.tsv --X concat_ICOHP_per_bond.tsv concat_ICOHP_per_MO.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_GrossPoluationL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_atomic_number.tsv concat_group_id.tsv concat_row.tsv concat_mass.tsv concat_atomic_volume.tsv concat_ionenergies_1.tsv concat_ionenergies_2.tsv concat_ionenergies_12.tsv concat_ionenergies_3.tsv concat_dipole_polarizability.tsv concat_en_pauling.tsv concat_density.tsv concat_covalent_radius.tsv concat_metallic_radius.tsv concat_vdw_radius.tsv concat_melting_point.tsv concat_boiling_point.tsv concat_heat_of_formation.tsv concat_sublimation.tsv concat_evaporation_heat.tsv concat_fusion_heat.tsv
        
    # python ~/bin/verve/nn-hyperopt.py -i ICOHP_per_bond ICOHP_per_MO ICOBI MadelungL GrossPopulationL volume bond chg atomic_number group_id row mass atomic_volume ionenergies1 ionenergies2 ionenergies12 ionenergies3 dipole_polarizability en_pauling density covalent_radius metallic_radius vdw_radius melting_point boiling_point heat_of_formation sublimation_heat evaporation_heat fusion_heat --Y concat_norm_formation_rel.tsv --X concat_ICOHP_per_bond.tsv concat_ICOHP_per_MO.tsv concat_ICOBI.tsv concat_norm_MadelungL.tsv concat_GrossPoluationL.tsv concat_norm_volume.tsv concat_bond.tsv concat_chg.tsv concat_atomic_number.tsv concat_group_id.tsv concat_row.tsv concat_mass.tsv concat_atomic_volume.tsv concat_ionenergies_1.tsv concat_ionenergies_2.tsv concat_ionenergies_12.tsv concat_ionenergies_3.tsv concat_dipole_polarizability.tsv concat_en_pauling.tsv concat_density.tsv concat_covalent_radius.tsv concat_metallic_radius.tsv concat_vdw_radius.tsv concat_melting_point.tsv concat_boiling_point.tsv concat_heat_of_formation.tsv concat_sublimation.tsv concat_evaporation_heat.tsv concat_fusion_heat.tsv
fi