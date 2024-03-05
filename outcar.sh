mag_tag=0
chg_tag=0
ene_tag=0
dir_tag=0
while getopts ":mcer" opt; do
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

if [[ $mag_tag == 1 ]]; then
    pattern_s='magnetization \(x\)'
    pattern_e='tot '
elif [[ $chg_tag == 1 ]]; then
    pattern_s='total charge '
    pattern_e='tot '
elif [[ $ene_tag == 1 ]]; then
    pattern_s='Free energy of the ion-electron system \(eV\)'
    pattern_e='free energy '
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
    echo -e "\e[1m"; pwd; echo -e "\e[0m"
    n=$(awk "/$pattern_s/{flag=1;next}/$pattern_e/{if(flag){count++;flag=0}}END{print count}" OUTCAR)
    m=$(awk "/$pattern_s/{count=0;flag=1;next}/$pattern_e/{if(flag){print count;flag=0}}flag{count++}" OUTCAR | tail -n 1)
    awk "/$pattern_s/,/$pattern_e/" OUTCAR | tail -n $(($m+2))
    cd $dir_now
done