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
    #         python ~/bin/verve/energy.py --save -p Madelung_L -x "Metal (MO)" -y "Madelugn energy (Loewdin, eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p energy -x "Metal (MO)" -y "Total energy (eV/MO)" -n m
    #         python ~/bin/verve/energy.py --save -p volume -x "Metal (MO)" -y "Volume (A^3/MO)" -n m
            python ~/bin/verve/energy.py --save -p mag -e M -x "Metal (MO)" -y "Magnetization"
    #         python ~/bin/verve/energy.py --save -p GP_L -e M  -x "Metal (MO)" -y "Gross population (Loewdin)"
    #         python ~/bin/verve/formation.py
    #         if [[ $dir == *'Tetrahedral'* ]]; then
    #             n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Hexagonal ratio [c/a]"
    #         elif [[ $dir == *'Square_Planar'* ]]; then
    #             n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Square prism ratio [c/a]"
    #         elif [[ $dir == *'Octahedral'* ]]; then
    #             n=6
    #         fi
    #         python ~/bin/verve/energy.py --save -p bond -x "Metal (MO)" -y "Bond length (A/M-O)" -n "$n"
    #         python ~/bin/verve/energy.py --save -p ICOHP -x "Metal (MO)" -y "ICOHP (eV/M-O)" -n "$n"
    #         sed -i 's/\x0//g' *.tsv
            cd $dir_now
        fi
    done
    for dir in *_*/; do
        cd $dir
        python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_Madelung_L */energy_norm_Madelung_Loewdin.tsv
        python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Total energy (eV/MO)" -o norm_energy */energy_norm_energy.tsv
        python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Volume (A^3/MO)" -o norm_volume */energy_norm_volume.tsv
        python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Magnetization" -o mag_M */energy_mag_M.tsv
        python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Gross population (Loewdin)" -o magnetization */energy_GP_Loewdin_M.tsv
        python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Formation energy (eV/MO)" -o norm_formation */energy_norm_formation.tsv
        if [[ $PWD == *'Tetraheral'* ]]; then
            python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Hexagonal ratio [c/a]" -o hexa_ratio */energy_hexa_ratio.tsv
        elif [[ $PWD == *'Square_Planar'* ]]; then
            python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Square prism ratio [c/a]" -o hexa_ratio */energy_hexa_ratio.tsv
        fi
        python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Bond lentgh (A/M-O)" -o norm_bond */energy_norm_bond.tsv
        python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP */energy_norm_ICOHP.tsv
        python ~/bin/verve/sumup.py -x merged_norm_ICOHP.tsv -y merged_norm_formation.tsv --xlabel "ICOHP (eV)" --ylabel "Formation energy (eV)" --xdata ICOHP --ydata formation
        python ~/bin/verve/sumup.py -x merged_norm_Madelung_L.tsv -y merged_norm_formation.tsv --xlabel "Madelung_Loewdin (eV)" --ylabel "Formation energy (eV)" --xdata MadelungL --ydata formation
        python ~/bin/verve/sumup.py -x merged_norm_ICOHP.tsv merged_norm_Madelung_L.tsv -y merged_norm_formation.tsv --xlabel "ICOHP + Madelung Loewdin (eV)" --ylabel "Formation energy (eV)" --xdata ICOHP+MadelungL --ydata formation            
        cd $dir_now
    done
    python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_3d_afm */1_afm/energy_norm_ICOHP.tsv
    python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_3d_fm */2_fm/energy_norm_ICOHP.tsv
    python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_3d */3d/energy_norm_ICOHP.tsv
    python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_4d */4d/energy_norm_ICOHP.tsv
    python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP_5d */5d/energy_norm_ICOHP.tsv
    python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Formation energy (Loewdin, eV/MO)" -o norm_formation_3d_afm */1_afm/energy_norm_formation.tsv
    python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Formation energy (Loewdin, eV/MO)" -o norm_formation_3d_fm */2_fm/energy_norm_formation.tsv
    python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Formation energy (Loewdin, eV/MO)" -o norm_formation_3d */3d/energy_norm_formation.tsv
    python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "Formation energy (Loewdin, eV/MO)" -o norm_formation_4d */4d/energy_norm_formation.tsv
    python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "Formation energy (Loewdin, eV/MO)" -o norm_formation_5d */5d/energy_norm_formation.tsv
    python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL_3d_afm */1_afm/energy_norm_Madelung_Loewdin.tsv
    python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL_3d_fm */2_fm/energy_norm_Madelung_Loewdin.tsv
    python ~/bin/verve/tsv.py -r 3d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL_3d */3d/energy_norm_Madelung_Loewdin.tsv
    python ~/bin/verve/tsv.py -r 4d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL_4d */4d/energy_norm_Madelung_Loewdin.tsv
    python ~/bin/verve/tsv.py -r 5d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_MadelungL_5d */5d/energy_norm_Madelung_Loewdin.tsv
fi