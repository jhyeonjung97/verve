$dir_now=$PWD
for i in '*/'
do
    cd $i
    python ~/bin/playground/aloha/cohp.py > icohp.txt
    cd $dir_now
done