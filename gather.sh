#!/bin/bash

r_count=0
c_count=1
neb_tag=false
port_tag=false
force_tag=false

while getopts ":rcnf:" opt; do
  case $opt in
    r)
      let r_count+=1
      ;;
    c)
      let c_count+=1
      ;;
    n)
      neb_tag=true
      ;;
    f)
      force_tag=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done
shift "$((OPTIND-1))"

if [[ $neb_tag == true ]]; then
    # usage: sh gather.sh -n #IMAGES
    read -p "files start with: " name
    for i in $(seq 1 $2)
    do
        cp 0$i/POSCAR ${name}_p$i.vasp
        cp 0$i/CONTCAR ${name}_c$i.vasp
    done
    cp 00/POSCAR ${name}_p0.vasp
    cp 0$(($2+1))/POSCAR ${name}_p$(($2+1)).vasp
    cp 00/POSCAR ${name}_c0.vasp
    cp 0$(($2+1))/POSCAR ${name}_c$(($2+1)).vasp
    exit 1
fi

if [[ $r_count -eq 0 ]]; then
    dirs='*_*/'
elif [[ $r_count -gt 0 ]]; then
    dirs='*/'
    for ((i=0; i<r_count; i++)); do
        dirs+='*/'
    done
elif [[ $force_tag == true ]]; then
    dirs='*/'
fi

if [[ -z $1 ]]; then
    read -p 'Which file? ' f
else
    f=$1
fi

if [[ $f == 'p' ]] || [[ $f == 'pos' ]] || [[ $f == 'POSCAR' ]]; then
    file='POSCAR'
elif [[ $f == 'c' ]] || [[ $f == 'con' ]] || [[ $f == 'CONTCAR' ]]; then
    file='CONTCAR'
elif [[ $f == 'f' ]] || [[ $f == 'final' ]] || [[ $f == 'final_with_calculator.json' ]]; then
    file='final_with_calculator.json'
else
    file=$f
fi

if [[ -z $2 ]]; then
    name=${file%%.*}
else
    name=$2
fi

for dir in $dirs
do
    dir=${dir%/}
    i=${dir:0:$c_count}
    if [[ $file == *.* ]]; then
        ext=".${file##*.}"
    else
        ext=''
    fi
    cp ${dir}/${file} ${name}${i}${ext}
    echo "cp ${dir}/${file} ${name}${i}${ext}"
done
