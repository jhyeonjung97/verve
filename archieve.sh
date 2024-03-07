dir_now=$PWD

if ${here} == 'slac'; then
    usr='jiuy97'
elif ${here} == 'mac'; then
    usr='hailey'
fi

cd /Users/$usr/jiuy97@stanford.edu\ -\ Google\ Drive/My\ Drive

cp -r /Users/jiuy97/bin/orange/* ./bin/orange
cp -r /Users/jiuy97/bin/shoulder/* ./bin/shoulder
cp -r /Users/jiuy97/bin/verve/* ./bin/verve

/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/1_cation .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/2_icohp .

cd $dir_now