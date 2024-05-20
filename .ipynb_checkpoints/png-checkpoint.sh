#!/bin/bash
if [[ ${here} == 'slac' ]]; then
    /usr/bin/rsync -e 'ssh' --ignore-times --size-only -avlzp -K --max-size=50000m \
    	--include="*/" \
    	--include="*.png" \
    	--exclude="*" \
     jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/3_V_shape .
elif [[ ${here} == 'nersc' ]]; then
    dir_now='/pscratch/sd/j/jiuy97/3_V_shape'
    cd $dir_now
    # for dir in metal/*/; do
    #     cd $dir
    #     python ~/bin/verve/energy.py --save -x "Metal (M)" -y "Total energy (eV/M)" -n m
    #     cd $dir_now
    # done
    # cd /pscratch/sd/j/jiuy97/3_V_shape/metal
    # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Volume (A^3/MO)" -o norm_energy *fm/energy_norm_energy.tsv *d/energy_norm_energy.tsv
    # cd /pscratch/sd/j/jiuy97/3_V_shape/oxide/0_min
    # python ~/bin/verve/energy.py --save -x "Metal (MxOy)" -y "Total energy (eV/M)" -n m
    # cd $dir_now
    # for dir in *_*/*/; do
    #     if [[ $dir != *'save'* ]] && [[ $dir != *'rhom'* ]] && [[ $dir != *'bin'* ]] && [[ $dir != *'cubic'* ]]; then
    #         cd $dir
    #         python ~/bin/verve/energy.py --save -p Madelung_L -x "Metal (MO)" -y "Madelugn energy (Loewdin, eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p energy -x "Metal (MO)" -y "Total energy (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p volume -x "Metal (MO)" -y "Volume (A^3/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p mag -e M -x "Metal (MO)" -y "|Magnetization|"
    #         python ~/bin/verve/energy.py --save -p GP_L -e M  -x "Metal (MO)" -y "Gross population (Loewdin)"
    #         python ~/bin/verve/energy.py --save -p chg -e M  -x "Metal (MO)" -y "Bader charge (e-)"
    #         python ~/bin/verve/energy.py --save -p bond  -x "Metal (M-O)" -y "Bond length (A)"
    #         python ~/bin/verve/energy.py --save -p ICOHP -x "Metal (MO)" -y "ICOHP (eV/MO)"
    #         python ~/bin/verve/energy.py --save -p ICOBI -x "Metal (MO)" -y "ICOBI (/M-O)"
    #         python ~/bin/verve/energy.py --save -p PSCENC -x "Metal (MO)" -y "PSCENC (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p TEWEN -x "Metal (MO)" -y "TEWEN (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p DENC -x "Metal (MO)" -y "DENC (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p EXHF -x "Metal (MO)" -y "EXHF (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p XCENC -x "Metal (MO)" -y "XCENC (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p PAW_double_counting -x "Metal (MO)" -y "PAW_double_counting (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p EENTRO -x "Metal (MO)" -y "EENTRO (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p EBANDS -x "Metal (MO)" -y "EBANDS (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p EATOM -x "Metal (MO)" -y "EATOM (eV/MO)" -n m
    #         python ~/bin/verve/formation.py
            
    #         if [[ $dir == *'Tetrahedral'* ]]; then
    #             n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Hexagonal ratio [c/a]"
    #         elif [[ $dir == *'Tetragonal'* ]] || [[ $dir == *'Square_Planar'* ]]; then
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
    for dir in *_*/; do
        cd $dir
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL */energy_norm_Madelung_Loewdin.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Total energy (eV/MO)" -o norm_energy */energy_norm_energy.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Volume (A^3/MO)" -o norm_volume */energy_norm_volume.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "|Magnetization|" -o mag_M */energy_mag_M.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Gross population (Loewdin)" -o GP_Loewdin_M */energy_GP_Loewdin_M.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Bader charge (e-)" -o chg */energy_chg_M.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Bond length (A/M-O)" -o bond */energy_bond.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Ionization energy (eV)" -o IE1 */energy_IE1.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Ionization energy (eV)" -o IE2 */energy_IE2.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Ionization energy (eV)" -o IE3 */energy_IE3.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Sublimation energy (eV)" -o sub */energy_sub.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Formation energy (eV/MO)" -o norm_formation */energy_norm_formation.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "PSCENC (eV/MO)" -o norm_PSCENC */energy_norm_PSCENC.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "TEWEN (eV/MO)" -o norm_TEWEN */energy_norm_TEWEN.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "DENC (eV/MO)" -o norm_DENC */energy_norm_DENC.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "EXHF (eV/MO)" -o norm_EXHF */energy_norm_EXHF.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "XCENC (eV/MO)" -o norm_XCENC */energy_norm_XCENC.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "PAW_double_counting (eV/MO)" -o norm_PAW_double_counting */energy_norm_PAW_double_counting.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "EENTRO (eV/MO)" -o norm_EENTRO */energy_norm_EENTRO.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "EBANDS (eV/MO)" -o norm_EBANDS */energy_norm_EBANDS.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "EATOM (eV/MO)" -o norm_EATOM */energy_norm_EATOM.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/MO)" -o ICOHP */energy_ICOHP.tsv

        # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Formation energy (eV/MO)" -o norm_formation 1_afm/energy_norm_formation.tsv 4d/energy_norm_formation.tsv 5d/energy_norm_formation.tsv
        # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/MO)" -o ICOHP 1_afm/energy_ICOHP.tsv 4d/energy_ICOHP.tsv 5d/energy_ICOHP.tsv
        # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "ICOBI (eV/MO)" -o ICOBI 1_afm/energy_ICOBI.tsv 4d/energy_ICOBI.tsv 5d/energy_ICOBI.tsv
        # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL 1_afm/energy_norm_Madelung_Loewdin.tsv 4d/energy_norm_Madelung_Loewdin.tsv 5d/energy_norm_Madelung_Loewdin.tsv
        # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Crystal field stabilization energy" -o cfse 1_afm/energy_cfse.tsv 4d/energy_cfse.tsv 5d/energy_cfse.tsv
        # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Ionization energy (eV)" -o IE1 1_afm/energy_IE1.tsv 4d/energy_IE1.tsv 5d/energy_IE1.tsv
        # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Ionization energy (eV)" -o IE2 1_afm/energy_IE2.tsv 4d/energy_IE2.tsv 5d/energy_IE2.tsv
        # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Ionization energy (eV)" -o IE3 1_afm/energy_IE3.tsv 4d/energy_IE3.tsv 5d/energy_IE3.tsv
        # python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "Sublimation energy (eV)" -o sub 1_afm/energy_sub.tsv 4d/energy_sub.tsv 5d/energy_sub.tsv
        
        # python ~/bin/verve/lr.py -o 3 -i ICOHP MadelungL CFSE --Y merged_norm_formation.tsv --X merged_ICOHP.tsv merged_norm_MadelungL.tsv merged_cfse.tsv > regression3.log
        # python ~/bin/verve/lr.py -o 4 -i MadelungL CFSE IE1 IE2 --Y merged_norm_formation.tsv --X merged_norm_MadelungL.tsv merged_cfse.tsv merged_IE1.tsv merged_IE2.tsv > regression4.log
        # python ~/bin/verve/lr.py -o 7 -i ICOHP MadelungL CFSE IE1 IE2 IE3 E_sub --Y merged_norm_formation.tsv --X merged_ICOHP.tsv merged_norm_MadelungL.tsv merged_cfse.tsv merged_IE1.tsv merged_IE2.tsv merged_IE3.tsv merged_sub.tsv > regression7.log    
        
        # if [[ $PWD == *'Tetraheral'* ]]; then
        #     :
        # elif [[ $dir == *'Tetragonal'* ]]; then
        #     :
        # elif [[ $PWD == *'Square_Planar'* ]]; then
        #     :
        # else
        #     python ~/bin/verve/tsv.py -l 3d 4d 5d -x "Metal (MO)" -y "IE1 + IE2 (eV)" -o IE12 1_afm/energy_IE12.tsv 4d/energy_IE12.tsv 5d/energy_IE12.tsv
        # fi
        
        # python ~/bin/verve/sumup.py -x merged_ICOHP.tsv -y merged_norm_formation.tsv --xlabel "ICOHP (eV)" --ylabel "Formation energy (eV)" --xdata ICOHP --ydata formation
        # python ~/bin/verve/sumup.py -x merged_norm_Madelung_L.tsv -y merged_norm_formation.tsv --xlabel "Madelung_Loewdin (eV)" --ylabel "Formation energy (eV)" --xdata MadelungL --ydata formation
        # python ~/bin/verve/sumup.py -x merged_ICOHP.tsv merged_norm_Madelung_L.tsv -y merged_norm_formation.tsv --xlabel "ICOHP + Madelung Loewdin (eV)" --ylabel "Formation energy (eV)" --xdata ICOHP+MadelungL --ydata formation
        cd $dir_now
    done
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
    
    # python ~/bin/verve/concat.py -o norm_formation --X *_*/merged_norm_formation.tsv
    # python ~/bin/verve/concat.py -o ICOHP --X *_*/merged_ICOHP.tsv
    # python ~/bin/verve/concat.py -o wICOHP --X *_*/merged_weighted_ICOHP.tsv
    # python ~/bin/verve/concat.py -o norm_MadelungL --X *_*/merged_norm_MadelungL.tsv
    # python ~/bin/verve/concat.py -o cfse --X *_*/merged_cfse.tsv
    # python ~/bin/verve/concat.py -o IE1 --X *_*/merged_IE1.tsv
    # python ~/bin/verve/concat.py -o IE2 --X *_*/merged_IE2.tsv
    # python ~/bin/verve/concat.py -o IE3 --X *_*/merged_IE3.tsv
    # python ~/bin/verve/concat.py -o IE12 --X *_*/merged_IE12.tsv
    # python ~/bin/verve/concat.py -o sub --X *_*/merged_sub.tsv
    # python ~/bin/verve/concat.py -o coord --X *_*/merged_coord.tsv
    # python ~/bin/verve/concat.py -o row --X *_*/merged_row.tsv
    # python ~/bin/verve/concat.py -o group --X *_*/merged_group.tsv
    # python ~/bin/verve/concat.py -o element --X *_*/merged_element.tsv

    python ~/bin/verve/lr.py -i wICOHP MadelungL CFSE IE12 --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv 

    python ~/bin/verve/lr.py -i ICOHP MadelungL CFSE IE1 IE2 IE3 E_sub --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv 
    python ~/bin/verve/lr.py -o w -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv

    python ~/bin/verve/lr.py -o wICOHP -i MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv   
    python ~/bin/verve/lr.py -o MadelungL -i wICOHP CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -o CFSE -i wICOHP MadelungL IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -o IE1 -i wICOHP MadelungL CFSE IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -o IE2 -i wICOHP MadelungL CFSE IE1 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -o IE3 -i wICOHP MadelungL CFSE IE1 IE2 E_sub row group --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -o E_sub -i wICOHP MadelungL CFSE IE1 IE2 IE3 row group --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -o row -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub group --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_group.tsv
    python ~/bin/verve/lr.py -o group -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv
    python ~/bin/verve/lr.py -i wICOHP MadelungL CFSE IE12 IE3 E_sub row --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE12.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv
    
    python ~/bin/verve/lr.py -i ICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -o w -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -r 3 -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -r 4 -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -r 5 -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -c WZ -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -c ZB -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -c TN -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -c 33 -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -c RS -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -z -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -z -r 3 -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -z -r 4 -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    python ~/bin/verve/lr.py -z -r 5 -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub row group --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv concat_row.tsv concat_group.tsv
    
    # python ~/bin/verve/gaussian.py -i ICOHP MadelungL CFSE IE1 IE2 IE3 E_sub --Y concat_norm_formation.tsv --X concat_ICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv > gaussian7.log   
    # python ~/bin/verve/gaussian.py -o w -i wICOHP MadelungL CFSE IE1 IE2 IE3 E_sub --Y concat_norm_formation.tsv --X concat_wICOHP.tsv concat_norm_MadelungL.tsv concat_cfse.tsv concat_IE1.tsv concat_IE2.tsv concat_IE3.tsv concat_sub.tsv > gaussian7w.log   
fi