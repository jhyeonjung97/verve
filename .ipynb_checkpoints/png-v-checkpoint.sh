dir_now='/pscratch/sd/j/jiuy97/3_V_shape'
cd $dir_now

for dir in */*/
do
        cd $dir
        sh png1.sh
        cd $dir_now
done

for dir in */
do
        cd $dir
        sh png2.sh
        cd $dir_now
done

sh png3.sh