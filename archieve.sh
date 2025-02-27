if [[ ${here} == 'slac' ]]; then
    stanford='/Users/jiuy97/Library/CloudStorage/OneDrive-Stanford'
elif [[ ${here} == 'mac' ]]; then
    stanford='/Users/jiuy97/Library/CloudStorage/OneDrive-Stanford'
fi

cd $stanford

/usr/bin/rsync -avzpl ~/bin/orange ./bin
/usr/bin/rsync -avzpl ~/bin/shoulder ./bin
/usr/bin/rsync -avzpl ~/bin/verve ./bin
/usr/bin/rsync -avzpl ~/bin/tools ./bin

/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/5_HEO .
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/6_MNC .