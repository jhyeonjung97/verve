mag_tag=0
chg_tag=0
ene_tag=0
dir_tag=0
while getopts ":mcer:" opt; do
  case $opt in
    m)
      mag_tag=1
      ;;
    c)
      chg_tag=1
      ;;
    e)
      ene_tag=1
      ;;
    r)
      dir_tag=1
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

# Shift the options out, so $1, $2, etc. are the non-option arguments
shift "$((OPTIND-1))"

if [[ -n $1 ]]; then
    file=$1
else
    file='OUTCAR'
fi

if [[ $mag_tag == 1 ]]; then
    pattern_s='magnetization \(x\)'
    pattern_e='tot '
    clr_tag='\e[35m'
elif [[ $chg_tag == 1 ]]; then
    pattern_s='total charge '
    pattern_e='tot '
    clr_tag='\e[34m'
elif [[ $ene_tag == 1 ]]; then
    pattern_s='Free energy of the ion-electron system \(eV\)'
    pattern_e='free energy '
    clr_tag='\e[32m'
fi

if [[ $dir_tag == 1 ]]; then
    DIR='*/'
else
    DIR='./'
fi

dir_now=$PWD
for dir in $DIR
do
    cd $dir
    dir_pwd=$(pwd)
    echo $mag_tag $pattern_s $pattern_e $file $m
    echo -e "$clr_tag$dir_pwd/$file\e[0m"
    n=$(awk "/$pattern_s/{flag=1;next}/$pattern_e/{if(flag){count++;flag=0}}END{print count}" $file)
    m=$(awk "/$pattern_s/{count=0;flag=1;next}/$pattern_e/{if(flag){print count;flag=0}}flag{count++}" $file | tail -n 1)
    awk "/$pattern_s/,/$pattern_e/" $file | tail -n $(($m+2))
    cd $dir_now
done