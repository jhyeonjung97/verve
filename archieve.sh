dir_now=$PWD

if [[ ${here} == 'slac' ]]; then
    cd /Users/jiuy97/OneDrive\ -\ Stanford
else
    exit
fi

cp -r /Users/jiuy97/bin/orange/* ./bin/orange
cp -r /Users/jiuy97/bin/shoulder/* ./bin/shoulder
cp -r /Users/jiuy97/bin/verve/* ./bin/verve

/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/1_cation .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/2_icohp .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/3_V_shape .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/4_V_slab .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/5_HEO .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/6_MNC .
  
cd $dir_now