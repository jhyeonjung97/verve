if [[ ${here} == 'slac' ]]; then
    cd /Users/jiuy97/Library/CloudStorage/OneDrive-Stanford
    
    /usr/bin/rsync -avzpl ~/bin/orange ./bin
    /usr/bin/rsync -avzpl ~/bin/shoulder ./bin
    /usr/bin/rsync -avzpl ~/bin/verve ./bin
    /usr/bin/rsync -avzpl ~/bin/tools ./bin
    
    /usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/5_HEO .
    /usr/bin/rsync -e ssh --ignore-times --size-only -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/6_MNC .
fi