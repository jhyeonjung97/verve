dir_now=$PWD
for dir in *_*/
do
    cd $dir
    if [[ -d 'opt' ]]; then
        echo 'There is already the directory named opt..'
        exit 1
    else
        mkdir opt
        cp * opt/
        for conti in conti*/
        do
            mv $conti opt/
        done
        rm *.log
    fi
    cd $dir_now
done
echo -e "\e[32mDon't forget to 1) spread correct submit.sh, 2) name -rc, 3) sub -r\e[0m"
sh ~/bin/verve/lobin.sh