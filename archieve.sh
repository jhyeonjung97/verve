stanford=""
personal=""
google=""
tetra=""

if [[ ${here} == 'slac' ]]; then
    toshiba='/Volumes/TOSHIBA'
    jeung2hailey='/Volumes/jeung2hailey'
    stanford='/Users/jiuy97/Library/CloudStorage/OneDrive-Stanford'
    personal='/Users/jiuy97/Library/CloudStorage/OneDrive-Personal'
    google='/Users/jiuy97/Library/CloudStorage/GoogleDrive-jiuy97@stanford.edu/My Drive/'
    tetra='/Users/jiuy97/Library/CloudStorage/GoogleDrive-jiuy97@stanford.edu/My Drive/Tetrahedral_oxides_ML/Figures'
elif [[ ${here} == 'mac' ]]; then
    toshiba='/Volumes/TOSHIBA'
    jeung2hailey='/Volumes/jeung2hailey'
    stanford='/Users/hailey/Library/CloudStorage/OneDrive-Stanford'
    personal='/Users/hailey/Library/CloudStorage/OneDrive-Personal'
    google='/Users/hailey/Library/CloudStorage/GoogleDrive-jiuy97@stanford.edu/My Drive/'
elif [[ ${here} == 'mini' ]]; then
    toshiba='/Volumes/TOSHIBA'
    jeung2hailey='/Volumes/jeung2hailey'
    stanford='/Users/hailey/Library/CloudStorage/OneDrive-Stanford'
    personal='/Users/hailey/Library/CloudStorage/OneDrive-Personal'
    google='/Users/hailey/Library/CloudStorage/GoogleDrive-jiuy97@stanford.edu/My Drive/'
fi

if [[ -d $toshiba ]]; then
    cd "$toshiba" || { echo "Failed to change directory to $toshiba"; exit 1; }
    /opt/homebrew/bin/rsync -e ssh -av --min-size=1 jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/3_V_bulk .
    /opt/homebrew/bin/rsync -e ssh -av --min-size=1 jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/4_V_slab .
    /opt/homebrew/bin/rsync -e ssh -av --min-size=1 jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/7_V_bulk .
    /opt/homebrew/bin/rsync -e ssh -av --min-size=1 jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/8_V_slab .
fi

if [[ -d $jeung2hailey ]]; then
    cd "$jeung2hailey" || { echo "Failed to change directory to $jeung2hailey"; exit 1; }
    /opt/homebrew/bin/rsync -e ssh -av --min-size=1 jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/1_cation .
    /opt/homebrew/bin/rsync -e ssh -av --min-size=1 jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/5_HEO .
fi

if [[ -d $stanford ]]; then
    cd "$stanford" || { echo "Failed to change directory to $stanford"; exit 1; }
    /opt/homebrew/bin/rsync -e ssh -av --min-size=1 jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/6_MNC .
    /opt/homebrew/bin/rsync -e ssh -av --min-size=1 jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/9_pourbaixGC .
fi

if [[ -d $personal ]] && [[ -d $google ]]; then
    cd "$personal" || { echo "Failed to change directory to $personal"; exit 1; }
    /opt/homebrew/bin/rsync -av --min-size=1 $google ./GoogleDrive
fi

if [[ -d $tetra ]]; then
    cd "$tetra" || { echo "Failed to change directory to $tetra"; exit 1; }
    rsync -avz --min-size=1 /Users/jiuy97/Desktop/7_V_bulk/figures .
fi