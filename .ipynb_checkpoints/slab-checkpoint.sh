dir_now=$PWD
mkdir 3d 4d 5d

cd 3d; mkdir 00_Ca 01_Sc 02_Ti 03_V 04_Cr 05_Mn 06_Fe 07_Co 08_Ni 09_Cu 10_Zn 11_Ga 12_Ge; cd $dir_now
cd 4d; mkdir 00_Sr 01_Y 02_Zr 03_Nb 04_Mo 05_Tc 06_Ru 07_Rh 08_Pd 09_Ag 10_Cd 11_In 12_Sn; cd $dir_now
cd 5d; mkdir 00_Ba 01_La 02_Hf 03_Ta 04_W 05_Re 06_Os 07_Ir 08_Pt 09_Au 10_Hg 11_Tl 12_Pb; cd $dir_now

cp -r 3d 1_afm
cp -r 3d 2_fm

mv a*.json 1_afm 
mv b*.json 2_fm
mv c*.json 3d
mv d*.json 4d
mv e*.json 5d

numbs=('00' '01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12')

for dir in */
do
    cd $dir
    echo $dir
    for numb in ${numbs[@]}
    do
        for sub_dir in $numb*/
        do
            mv *$numb.json "$sub_dir"restart.json
        done
    done
    cd $dir_now
done