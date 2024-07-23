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
    #         python ~/bin/verve/energy.py --save -p energy -x "Metal (MO)" -y "Total energy (eV)"
    #         python ~/bin/verve/energy.py --save -p energy -x "Metal (MO)" -y "Total energy (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p bond  -x "Metal (M-O)" -y "Bond length (A)"
    #         python ~/bin/verve/energy.py --save -p volume -x "Metal (MO)" -y "Volume (A^3/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p chg -e M  -x "Metal (MO)" -y "Bader charge (e-)"
    #         python ~/bin/verve/energy.py --save -p mag -e M -x "Metal (MO)" -y "|Magnetization|"
    #         python ~/bin/verve/energy.py --save -p ICOHP -x "Metal (MO)" -y "ICOHP (eV/MO)"
    #         python ~/bin/verve/energy.py --save -p ICOBI -x "Metal (MO)" -y "ICOBI (/M-O)"
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
            
    #         if [[ $dir == *'Tetrahedral'* ]]; then
    #             n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Hexagonal ratio [c/a]"
    #         elif [[ $dir == *'Pyramidal'* ]] || [[ $dir == *'Tetragonal'* ]] || [[ $dir == *'Square_Planar'* ]]; then
    #             n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Square prism ratio [c/a]"
    #         elif [[ $dir == *'Octahedral'* ]]; then
    #             n=6
    #         fi
            
    #         python ~/bin/verve/energy.py --save -p bond -x "Metal (MO)" -y "Bond length (A/M-O)" -n $n
    #         python ~/bin/verve/energy.py --save -p ICOHP -x "Metal (MO)" -y "ICOHP (eV/M-O)" -n $n
    #         python ~/bin/verve/energy.py --save -p ICOBI -x "Metal (MO)" -y "ICOBI (eV/M-O)" -n $n
    #         sed -i 's/\x0//g' *.tsv
    #         cd $dir_now
    #     fi
    # done
    
    for dir in /pscratch/sd/j/jiuy97/3_V_shape/*_*_*/; do
        cd $dir
        python ~/bin/verve/tsv.py -l 3d_AFM 3d_FM -x "Metal (MO)" -y "Formation energy (eV/MO)" -o AFMvsFM *_*fm/energy_norm_formation.tsv 2_fm/energy_norm_formation.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Formation energy (eV/MO)" -o norm_formation 1_afm/energy_norm_formation.tsv 4d/energy_norm_formation.tsv 5d/energy_norm_formation.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Cohesive energy (eV/MO)" -o norm_cohesive 1_afm/energy_norm_cohesive.tsv 4d/energy_norm_cohesive.tsv 5d/energy_norm_cohesive.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/MO)" -o ICOHP_per_MO 1_afm/energy_ICOHP.tsv 4d/energy_ICOHP.tsv 5d/energy_ICOHP.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/MO)" -o ICOHP_per_bond 1_afm/energy_norm_ICOHP.tsv 4d/energy_norm_ICOHP.tsv 5d/energy_norm_ICOHP.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "ICOBI (eV/MO)" -o ICOBI 1_afm/energy_ICOBI.tsv 4d/energy_ICOBI.tsv 5d/energy_ICOBI.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL 1_afm/energy_norm_Madelung_Loewdin.tsv 4d/energy_norm_Madelung_Loewdin.tsv 5d/energy_norm_Madelung_Loewdin.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Total energy (eV/MO)" -o norm_energy 1_afm/energy_norm_energy.tsv 4d/energy_norm_energy.tsv 5d/energy_norm_energy.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Volume (A^3/MO)" -o norm_volume 1_afm/energy_norm_volume.tsv 4d/energy_norm_volume.tsv 5d/energy_norm_volume.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "|Magnetization|" -o mag_M 1_afm/energy_mag_M.tsv 4d/energy_mag_M.tsv 5d/energy_mag_M.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Gross population (Loewdin)" -o GP_Loewdin_M 1_afm/energy_GP_Loewdin_M.tsv 4d/energy_GP_Loewdin_M.tsv 5d/energy_GP_Loewdin_M.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Bader charge (e-)" -o chg 1_afm/energy_chg_M.tsv 4d/energy_chg_M.tsv 5d/energy_chg_M.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Bond length (A/M-O)" -o bond 1_afm/energy_bond.tsv 4d/energy_bond.tsv 5d/energy_bond.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Ionization energy (eV)" -o IE1 1_afm/energy_IE1.tsv 4d/energy_IE1.tsv 5d/energy_IE1.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Ionization energy (eV)" -o IE2 1_afm/energy_IE2.tsv 4d/energy_IE2.tsv 5d/energy_IE2.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Ionization energy (eV)" -o IE3 1_afm/energy_IE3.tsv 4d/energy_IE3.tsv 5d/energy_IE3.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "IE1 + IE2 (eV)" -o IE12 1_afm/energy_IE12.tsv 4d/energy_IE12.tsv 5d/energy_IE12.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Sublimation energy (eV)" -o sub 1_afm/energy_sub.tsv 4d/energy_sub.tsv 5d/energy_sub.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "PSCENC (eV/MO)" -o norm_PSCENC 1_afm/energy_norm_PSCENC.tsv 4d/energy_norm_PSCENC.tsv 5d/energy_norm_PSCENC.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "TEWEN (eV/MO)" -o norm_TEWEN 1_afm/energy_norm_TEWEN.tsv 4d/energy_norm_TEWEN.tsv 5d/energy_norm_TEWEN.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "DENC (eV/MO)" -o norm_DENC 1_afm/energy_norm_DENC.tsv 4d/energy_norm_DENC.tsv 5d/energy_norm_DENC.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "EXHF (eV/MO)" -o norm_EXHF 1_afm/energy_norm_EXHF.tsv 4d/energy_norm_EXHF.tsv 5d/energy_norm_EXHF.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "XCENC (eV/MO)" -o norm_XCENC 1_afm/energy_norm_XCENC.tsv 4d/energy_norm_XCENC.tsv 5d/energy_norm_XCENC.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "PAW_double_counting (eV/MO)" -o norm_PAW_double_counting 1_afm/energy_norm_PAW_double_counting.tsv 4d/energy_norm_PAW_double_counting.tsv 5d/energy_norm_PAW_double_counting.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "EENTRO (eV/MO)" -o norm_EENTRO 1_afm/energy_norm_EENTRO.tsv 4d/energy_norm_EENTRO.tsv 5d/energy_norm_EENTRO.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "EBANDS (eV/MO)" -o norm_EBANDS 1_afm/energy_norm_EBANDS.tsv 4d/energy_norm_EBANDS.tsv 5d/energy_norm_EBANDS.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "EATOM (eV/MO)" -o norm_EATOM 1_afm/energy_norm_EATOM.tsv 4d/energy_norm_EATOM.tsv 5d/energy_norm_EATOM.tsv
        python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/MO)" -o ICOHP 1_afm/energy_ICOHP.tsv 4d/energy_ICOHP.tsv 5d/energy_ICOHP.tsv        
        python ~/bin/verve/sumup.py -x merged_ICOHP.tsv -y merged_norm_formation.tsv --xlabel "ICOHP (eV)" --ylabel "Formation energy (eV)" --xdata ICOHP --ydata formation
        python ~/bin/verve/sumup.py -x merged_norm_Madelung_L.tsv -y merged_norm_formation.tsv --xlabel "Madelung_Loewdin (eV)" --ylabel "Formation energy (eV)" --xdata MadelungL --ydata formation
        python ~/bin/verve/sumup.py -x merged_ICOHP.tsv merged_norm_Madelung_L.tsv -y merged_norm_formation.tsv --xlabel "ICOHP + Madelung Loewdin (eV)" --ylabel "Formation energy (eV)" --xdata ICOHP+MadelungL --ydata formation
    done
    
    cd /pscratch/sd/j/jiuy97/3_V_shape
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o ICOHP_3d_afm */1_afm/energy_ICOHP.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o ICOHP_3d_fm */2_fm/energy_ICOHP.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o ICOHP_3d */3d/energy_ICOHP.tsv
    # python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o ICOHP_4d */4d/energy_ICOHP.tsv
    # python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o ICOHP_5d */5d/energy_ICOHP.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_3d_afm */1_afm/energy_norm_ICOHP.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_3d_fm */2_fm/energy_norm_ICOHP.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_3d */3d/energy_norm_ICOHP.tsv
    # python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_4d */4d/energy_norm_ICOHP.tsv
    # python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_5d */5d/energy_norm_ICOHP.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Formation energy (Loewdin, eV/MO)" -o norm_formation_3d_afm */1_afm/energy_norm_formation.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Formation energy (Loewdin, eV/MO)" -o norm_formation_3d_fm */2_fm/energy_norm_formation.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Formation energy (Loewdin, eV/MO)" -o norm_formation_3d */3d/energy_norm_formation.tsv
    # python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "Formation energy (Loewdin, eV/MO)" -o norm_formation_4d */4d/energy_norm_formation.tsv
    # python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "Formation energy (Loewdin, eV/MO)" -o norm_formation_5d */5d/energy_norm_formation.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL_3d_afm */1_afm/energy_norm_Madelung_Loewdin.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL_3d_fm */2_fm/energy_norm_Madelung_Loewdin.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL_3d */3d/energy_norm_Madelung_Loewdin.tsv
    # python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL_4d */4d/energy_norm_Madelung_Loewdin.tsv
    # python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL_5d */5d/energy_norm_Madelung_Loewdin.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "|Magnetization|" -o norm_mag_M_3d_afm */1_afm/energy_mag_M.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "|Magnetization|" -o norm_mag_M_3d_fm */2_fm/energy_mag_M.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "|Magnetization|" -o norm_mag_M_3d */3d/energy_mag_M.tsv
    # python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "|Magnetization|" -o norm_mag_M_4d */4d/energy_mag_M.tsv
    # python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "|Magnetization|" -o norm_mag_M_5d */5d/energy_mag_M.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Bond lentgh (A/M-O)" -o norm_bond_3d_afm */1_afm/energy_norm_bond.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Bond lentgh (A/M-O)" -o norm_bond_3d_fm */2_fm/energy_norm_bond.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Bond lentgh (A/M-O)" -o norm_bond_3d */3d/energy_norm_bond.tsv
    # python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "Bond lentgh (A/M-O)" -o norm_bond_4d */4d/energy_norm_bond.tsv
    # python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "Bond lentgh (A/M-O)" -o norm_bond_5d */5d/energy_norm_bond.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Gross population (Loewdin)" -o norm_GP_M_3d_afm */1_afm/energy_GP_Loewdin_M.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Gross population (Loewdin)" -o norm_GP_M_3d_fm */2_fm/energy_GP_Loewdin_M.tsv
    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Gross population (Loewdin)" -o norm_GP_M_3d */3d/energy_GP_Loewdin_M.tsv
    # python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "Gross population (Loewdin)" -o norm_GP_M_4d */4d/energy_GP_Loewdin_M.tsv
    # python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "Gross population (Loewdin)" -o norm_GP_M_5d */5d/energy_GP_Loewdin_M.tsv
    # python ~/bin/verve/sum.py -r 3d -x "Metal (MO)" -y "E_form - ICOHP - E_Madelung (eV/M-O)" -p merged_norm_formation_3d_afm.tsv -m merged_ICOHP_3d_afm.tsv merged_norm_MadelungL_3d_afm.tsv -o cfse_3d_afm
    # python ~/bin/verve/sum.py -r 3d -x "Metal (MO)" -y "E_form - ICOHP - E_Madelung (eV/M-O)" -p merged_norm_formation_3d_fm.tsv -m merged_ICOHP_3d_fm.tsv merged_norm_MadelungL_3d_fm.tsv -o cfse_3d_fm
    # python ~/bin/verve/sum.py -r 3d -x "Metal (MO)" -y "E_form - ICOHP - E_Madelung (eV/M-O)" -p merged_norm_formation_3d.tsv -m merged_ICOHP_3d.tsv merged_norm_MadelungL_3d.tsv -o cfse_3d
    # python ~/bin/verve/sum.py -r 4d -x "Metal (MO)" -y "E_form - ICOHP - E_Madelung (eV/M-O)" -p merged_norm_formation_4d.tsv -m merged_ICOHP_4d.tsv merged_norm_MadelungL_4d.tsv -o cfse_4d
    # python ~/bin/verve/sum.py -r 5d -x "Metal (MO)" -y "E_form - ICOHP - E_Madelung (eV/M-O)" -p merged_norm_formation_5d.tsv -m merged_ICOHP_5d.tsv merged_norm_MadelungL_5d.tsv -o cfse_5d


    # python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Cohesive energy (eV/MO)" -o norm_cohesive_3d */1_afm/energy_norm_cohesive.tsv
    # python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "Cohesive energy (eV/MO)" -o norm_cohesive_4d */4d/energy_norm_cohesive.tsv
    # python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "Cohesive energy (eV/MO)" -o norm_cohesive_5d */5d/energy_norm_cohesive.tsv
        
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
    
    # python ~/bin/verve/concat.py -o ICOHP --X *_*_*/merged_ICOHP.tsv
    # python ~/bin/verve/concat.py -o ICOHP_per_MO --X *_*_*/merged_ICOHP_per_MO.tsv
    # python ~/bin/verve/concat.py -o ICOHP_per_bond --X *_*_*/merged_ICOHP_per_bond.tsv
    # python ~/bin/verve/concat.py -o ICOBI --X *_*_*/merged_ICOBI.tsv
    # python ~/bin/verve/concat.py -o wICOHP --X *_*_*/merged_weighted_ICOHP.tsv
    # python ~/bin/verve/concat.py -o norm_MadelungL --X *_*_*/merged_norm_MadelungL.tsv
    # python ~/bin/verve/concat.py -o norm_wMadelungL --X *_*_*/merged_weighted_norm_MadelungL.tsv
    # python ~/bin/verve/concat.py -o GrossPopulationL --X *_*_*/merged_GP_Loewdin_M.tsv
    # python ~/bin/verve/concat.py -o norm_volume --X *_*_*/merged_norm_volume.tsv
    # python ~/bin/verve/concat.py -o bond --X *_*_*/merged_bond.tsv
    # python ~/bin/verve/concat.py -o chg --X *_*_*/merged_chg.tsv
    # python ~/bin/verve/concat.py -o redoxP --X *_*_*/merged_redoxP.tsv
    # python ~/bin/verve/concat.py -o redoxP_clean --X *_*_*/merged_redoxP_clean.tsv
    # python ~/bin/verve/concat.py -o norm_cohesive --X *_*_*/merged_norm_cohesive.tsv
    
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