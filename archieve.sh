dir_now=$PWD

if [[ ! ${here} == 'slac' ]]; then
    exit
fi

cd /Users/jiuy97/Library/CloudStorage/OneDrive-Stanford

cp -r /Users/jiuy97/bin/orange/* ./bin/orange
cp -r /Users/jiuy97/bin/shoulder/* ./bin/shoulder
cp -r /Users/jiuy97/bin/verve/* ./bin/verve
cp -r /Users/jiuy97/bin/tools/* ./bin/tools

/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/3_V_bulk .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/4_V_slab .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/6_MNC .

cd /Users/jiuy97/Library/CloudStorage/OneDrive-Personal

/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/1_cation .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/2_icohp .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/5_HEO .
  
cd $dir_now