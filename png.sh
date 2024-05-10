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
    for dir in *_*/*/; do
        if [[ $dir != *'save'* ]] && [[ $dir != *'rhom'* ]] && [[ $dir != *'bin'* ]] && [[ $dir != *'cubic'* ]]; then
            cd $dir
            # python ~/bin/verve/energy.py --save -p Madelung_L -x "Metal (MO)" -y "Madelugn energy (Loewdin, eV/MO)" -n m
            # python ~/bin/verve/energy.py --save -p energy -x "Metal (MO)" -y "Total energy (eV/MO)" -n m
            # python ~/bin/verve/energy.py --save -p volume -x "Metal (MO)" -y "Volume (A^3/MO)" -n m
            # python ~/bin/verve/energy.py --save -p mag -e M -x "Metal (MO)" -y "|Magnetization|"
            # python ~/bin/verve/energy.py --save -p GP_L -e M  -x "Metal (MO)" -y "Gross population (Loewdin)"
            # python ~/bin/verve/energy.py --save -p chg -e M  -x "Metal (MO)" -y "Bader charge (e-)"
            # python ~/bin/verve/energy.py --save -p bond  -x "Metal (M-O)" -y "Bond length (A)"
            # python ~/bin/verve/energy.py --save -p ICOHP -x "Metal (MO)" -y "ICOHP (eV/M-O)"
            python ~/bin/verve/energy.py --save -p PSCENC -x "Metal (MO)" -y "PSCENC (eV/MO)" -n m
            # python ~/bin/verve/energy.py --save -p TEWEN -x "Metal (MO)" -y "TEWEN (eV/MO)" -n m
            # python ~/bin/verve/energy.py --save -p DENC -x "Metal (MO)" -y "DENC (eV/MO)" -n m
            # python ~/bin/verve/energy.py --save -p EXHF -x "Metal (MO)" -y "EXHF (eV/MO)" -n m
            # python ~/bin/verve/energy.py --save -p XCENC -x "Metal (MO)" -y "XCENC (eV/MO)" -n m
            # python ~/bin/verve/energy.py --save -p PAW_double_counting -x "Metal (MO)" -y "PAW_double_counting (eV/MO)" -n m
            # python ~/bin/verve/energy.py --save -p EENTRO -x "Metal (MO)" -y "EENTRO (eV/MO)" -n m
            # python ~/bin/verve/energy.py --save -p EBANDS -x "Metal (MO)" -y "EBANDS (eV/MO)" -n m
            python ~/bin/verve/energy.py --save -p EATOM -x "Metal (MO)" -y "EATOM (eV/MO)" -n m
            # python ~/bin/verve/formation.py
            
            # if [[ $dir == *'Tetrahedral'* ]]; then
            #     n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Hexagonal ratio [c/a]"
            # elif [[ $dir == *'Tetragonal'* ]] || [[ $dir == *'Square_Planar'* ]]; then
            #     n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Square prism ratio [c/a]"
            # elif [[ $dir == *'Octahedral'* ]]; then
            #     n=6
            # fi
            
            # python ~/bin/verve/energy.py --save -p bond -x "Metal (MO)" -y "Bond length (A/M-O)" -n $n
            # python ~/bin/verve/energy.py --save -p ICOHP -x "Metal (MO)" -y "ICOHP (eV/M-O)" -n $n
            # sed -i 's/\x0//g' *.tsv
            cd $dir_now
        fi
    done
    for dir in *_*/; do
        cd $dir
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_Madelung_L */energy_norm_Madelung_Loewdin.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Total energy (eV/MO)" -o norm_energy */energy_norm_energy.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Volume (A^3/MO)" -o norm_volume */energy_norm_volume.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "|Magnetization|" -o mag_M */energy_mag_M.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Gross population (Loewdin)" -o GP_Loewdin_M */energy_GP_Loewdin_M.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Bader charge (e-)" -o chg */energy_chg_M.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (M-O)" -y "Bond length (A)" -o bond */energy_bond.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (M-O)" -y "Ionization energy (eV)" -o IE1 */energy_IE1.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (M-O)" -y "Ionization energy (eV)" -o IE2 */energy_IE2.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (M-O)" -y "Ionization energy (eV)" -o IE3 */energy_IE3.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (M-O)" -y "Sublimation energy (eV)" -o sub */energy_sub.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Formation energy (eV/MO)" -o norm_formation */energy_norm_formation.tsv
        python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "PSCENC (eV/MO)" -o norm_PSCENC */energy_norm_PSCENC.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "TEWEN (eV/MO)" -o norm_TEWEN */energy_norm_TEWEN.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "DENC (eV/MO)" -o norm_DENC */energy_norm_DENC.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "EXHF (eV/MO)" -o norm_EXHF */energy_norm_EXHF.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "XCENC (eV/MO)" -o norm_XCENC */energy_norm_XCENC.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "PAW_double_counting (eV/MO)" -o norm_PAW_double_counting */energy_norm_PAW_double_counting.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "EENTRO (eV/MO)" -o norm_EENTRO */energy_norm_EENTRO.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "EBANDS (eV/MO)" -o norm_EBANDS */energy_norm_EBANDS.tsv
        python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "EATOM (eV/MO)" -o norm_EATOM */energy_norm_EATOM.tsv
        
        # if [[ $PWD == *'Tetraheral'* ]]; then
        #     python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Hexagonal ratio [c/a]" -o hexa_ratio */energy_hexa_ratio.tsv
        #     python ~/bin/verve/lr3.py --Y merged_norm_formation.tsv --X1 merged_ICOHP.tsv --X2 merged_norm_Madelung_L.tsv --X3 merged_cfse.tsv > regression_output3.log
        #     python ~/bin/verve/lr7.py --Y merged_norm_formation.tsv --X1 merged_ICOHP.tsv --X2 merged_norm_Madelung_L.tsv --X3 merged_cfse.tsv --X4 merged_IE1.tsv --X5 merged_IE2.tsv --X6 merged_IE3.tsv --X7 merged_sub.tsv > regression_output7.log
        #     python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Crystal Field Stabilization Energy" -o cfse */energy_cfse.tsv
        # elif [[ $dir == *'Tetragonal'* ]] || [[ $PWD == *'Square_Planar'* ]]; then
        #     echo 'pass'
        #     python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Square prism ratio [c/a]" -o hexa_ratio */energy_hexa_ratio.tsv
        # else
        #     python ~/bin/verve/lr.py --Y merged_norm_formation.tsv --X1 merged_ICOHP.tsv --X2 merged_norm_Madelung_L.tsv --X3 merged_cfse.tsv > regression_output.log
        #     python ~/bin/verve/lr3.py --Y merged_norm_formation.tsv --X1 merged_ICOHP.tsv --X2 merged_norm_Madelung_L.tsv --X3 merged_cfse.tsv > regression_output3.log
        #     python ~/bin/verve/lr7.py --Y merged_norm_formation.tsv --X1 merged_ICOHP.tsv --X2 merged_norm_Madelung_L.tsv --X3 merged_cfse.tsv --X4 merged_IE1.tsv --X5 merged_IE2.tsv --X6 merged_IE3.tsv --X7 merged_sub.tsv > regression_output7.log
        #     python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Crystal Field Stabilization Energy" -o cfse */energy_cfse.tsv
        # fi
        
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Bond lentgh (A/M-O)" -o norm_bond */energy_norm_bond.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP */energy_norm_ICOHP.tsv
        # python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o ICOHP */energy_ICOHP.tsv
        # python ~/bin/verve/sumup.py -x merged_ICOHP.tsv -y merged_norm_formation.tsv --xlabel "ICOHP (eV)" --ylabel "Formation energy (eV)" --xdata ICOHP --ydata formation
        # python ~/bin/verve/sumup.py -x merged_norm_Madelung_L.tsv -y merged_norm_formation.tsv --xlabel "Madelung_Loewdin (eV)" --ylabel "Formation energy (eV)" --xdata MadelungL --ydata formation
        # python ~/bin/verve/sumup.py -x merged_ICOHP.tsv merged_norm_Madelung_L.tsv -y merged_norm_formation.tsv --xlabel "ICOHP + Madelung Loewdin (eV)" --ylabel "Formation energy (eV)" --xdata ICOHP+MadelungL --ydata formation
        # python ~/bin/verve/sum.py -p merged_norm_formation.tsv -m merged_ICOHP.tsv merged_norm_Madelung_L.tsv -o cfse
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
fi