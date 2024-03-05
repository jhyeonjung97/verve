n=$(awk '/total charge /{flag=1;next}/tot /{if(flag){count++;flag=0}}END{print count}' OUTCAR)
m=$(awk '/total charge /{count=0;flag=1;next}/tot /{if(flag){print count;flag=0}}flag{count++}' OUTCAR | tail -n 1)
awk "/total charge /,/tot /" OUTCAR | tail -n $m