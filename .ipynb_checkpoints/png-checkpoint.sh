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
    for dir in */*/; do
            cd $dir
            python ~/bin/verve/energy.py --save -p Madelung_L -x "Metal (MO)" -y "Madelugn energy (Loewdin, eV/MO)" -n m
            python ~/bin/verve/energy.py --save -p Madelung_M -x "Metal (MO)" -y "Madelung energy (Mulliken, eV/MO)" -n m
            python ~/bin/verve/energy.py --save -p energy -x "Metal (MO)" -y "Total energy (eV/MO)" -n m
            python ~/bin/verve/energy.py --save -p volume -x "Metal (MO)" -y "Volume (A^3/MO)" -n m
            python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Hexagonal ratio [c/a]"
            python ~/bin/verve/energy.py --save -p mag -e M -x "Metal (MO)" -y "Magnetization"
            python ~/bin/verve/formation.py
            if [[ 'Tetraheral' in $dir ]]; then
                n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Hexagonal ratio [c/a]"
            elif [[ 'Square_Planar' in $dir ]]; then
                n=4; python ~/bin/verve/energy.py --save -p hexa -x "Metal (MO)" -y "Square prism ratio [c/a]"
            elif [[ 'Octahedral' in $dir ]]; then
                n=6
            fi
            python ~/bin/verve/energy.py --save -p bond -x "Metal (MO)" -y "Bond length (A/M-O)" -n $n
            python ~/bin/verve/energy.py --save -p ICOHP -x "Metal (MO)" -y "ICOHP (eV/M-O)" -n $n
            sed -i 's/\x0//g' *.tsv
            cd $dir_now
    done
    for dir in */; do
            cd $dir
            sed -i 's/\x0//g' */*.tsv
            python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Madelung energy (Loewdin, eV/MO)" -o norm_Madelung_L */energy_norm_Madelung_Loewdin.tsv
            python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Madelung energy (Mulliken, eV/MO)" -o norm_Madelung_M */energy_norm_Madelung_Mulliken.tsv
            python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "ICOHP (eV/M-O)" -o norm_ICOHP */energy_norm_ICOHP.tsv
            python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Volume (A^3/MO)" -o norm_volume */energy_norm_volume.tsv
            python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Bond lentgh (A/M-O)" -o norm_bond */energy_norm_bond.tsv
            python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Total energy (eV/MO)" -o norm_energy */energy_norm_energy.tsv
            python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Formation energy (eV/MO)" -o norm_formation */energy_norm_formation.tsv
            python ~/bin/verve/tsv.py -l 3d_afm 3d_fm 3d 4d 5d -x "Metal (MO)" -y "Hexagonal ratio [c/a]" -o hexa_ratio */energy_hexa_ratio.tsv
            python ~/bin/verve/sumup.py -x merged_norm_ICOHP.tsv -y merged_norm_formation.tsv --xlabel "ICOHP (eV)" --ylabel "Formation energy (eV)" --xdata ICOHP --ydata formation
            python ~/bin/verve/sumup.py -x merged_norm_Madelung_L.tsv -y merged_norm_formation.tsv --xlabel "Madelung_Loewdin (eV)" --ylabel "Formation energy (eV)" --xdata MadelungL --ydata formation
            python ~/bin/verve/sumup.py -x merged_norm_ICOHP.tsv merged_norm_Madelung_L.tsv -y merged_norm_formation.tsv --xlabel "ICOHP + Madelung Loewdin (eV)" --ylabel "Formation energy (eV)" --xdata ICOHP+MadelungL --ydata formation            
            cd $dir_now
    done
    sh png3.sh
fi