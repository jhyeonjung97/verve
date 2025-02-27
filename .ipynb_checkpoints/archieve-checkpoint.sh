stanford=""
personal=""
google=""

if [[ ${here} == 'slac' ]]; then
    stanford='/Users/jiuy97/Library/CloudStorage/OneDrive-Stanford'
    personal='/Users/jiuy97/Library/CloudStorage/OneDrive-Personal'
    google='/Users/jiuy97/Library/CloudStorage/GoogleDrive-jiuy97@stanford.edu/My\ Drive'
elif [[ ${here} == 'mac' ]]; then
    stanford='/Users/hailey/Library/CloudStorage/OneDrive-Stanford'
fi

if [[ -n $stanford ]]; then
    cd "$stanford" || { echo "Failed to change directory to $stanford"; exit 1; }
    
    /usr/bin/rsync -avzpl ~/bin/orange ./bin
    /usr/bin/rsync -avzpl ~/bin/shoulder ./bin
    /usr/bin/rsync -avzpl ~/bin/verve ./bin
    /usr/bin/rsync -avzpl ~/bin/tools ./bin
    
    /usr/bin/rsync -e ssh -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/5_HEO .
    /usr/bin/rsync -e ssh -avlzp jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/6_MNC .

    if [[ -n $google ]]; then
        /usr/bin/rsync -avzpl $google google
fi