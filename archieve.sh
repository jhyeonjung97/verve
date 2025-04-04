stanford=""
personal=""
google=""

if [[ ${here} == 'slac' ]]; then
    toshiba='/Volumes/TOSHIBA'
    jeung2hailey='/Volumes/jeung2hailey'
    stanford='/Users/jiuy97/Library/CloudStorage/OneDrive-Stanford'
    personal='/Users/jiuy97/Library/CloudStorage/OneDrive-Personal'
    google='/Users/jiuy97/Library/CloudStorage/GoogleDrive-jiuy97@stanford.edu/My\ Drive'
elif [[ ${here} == 'mac' ]]; then
    toshiba='/Volumes/TOSHIBA'
    jeung2hailey='/Volumes/jeung2hailey'
    stanford='/Users/hailey/Library/CloudStorage/OneDrive-Stanford'
    personal='/Users/hailey/Library/CloudStorage/OneDrive-Personal'
    google='/Users/hailey/Library/CloudStorage/GoogleDrive-hailey@stanford.edu/My\ Drive'
fi

if [[ -d $toshiba ]]; then
    cd "$toshiba" || { echo "Failed to change directory to $toshiba"; exit 1; }
    /usr/bin/rsync -e ssh -avzpl jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/3_V_bulk .
    /usr/bin/rsync -e ssh -avzpl jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/4_V_slab .
    /usr/bin/rsync -e ssh -avzpl jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/7_V_bulk .
    /usr/bin/rsync -e ssh -avzpl jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/8_V_slab .
fi

if [[ -d $jeung2hailey ]]; then
    cd "$jeung2hailey" || { echo "Failed to change directory to $jeung2hailey"; exit 1; }
    /usr/bin/rsync -e ssh -avzpl jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/1_cation .
    /usr/bin/rsync -e ssh -avzpl jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/5_HEO .
fi

if [[ -d $stanford ]]; then
    cd "$stanford" || { echo "Failed to change directory to $stanford"; exit 1; }
    /usr/bin/rsync -e ssh -avzpl jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/6_MNC .
    /usr/bin/rsync -e ssh -avzpl jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/9_pourbaixGC .
fi

if [[ -d $stanford ]] && [[ -d $google ]]; then
    cd "$stanford" || { echo "Failed to change directory to $stanford"; exit 1; }
    /usr/bin/rsync -avzpl $google .
fi