dir_now=$PWD
for dir in *_*/
do
    cd $dir
    if [[ -d 'zpe' ]]; then
        echo 'There is already the directory named zpe..'
        exit 1
    else
        mkdir zpe
        cp * ./zpe
        rm ./zpe/*.log
        sed -i 's/opt_bulk3/phonon_bulk/g' ./zpe/submit.sh
        sed -i 's/opt_bulk2/phonon_bulk/g' ./zpe/submit.sh
        sed -i '/bader/d' ./zpe/submit.sh
    fi
    cd $dir_now
done
# echo -e "\e[32mDon't forget to 1) spread correct submit.sh, 2) name -rc, 3) sub -r\e[0m"
# sh ~/bin/verve/lobin.sh