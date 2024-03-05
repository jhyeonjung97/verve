n=$(awk '/magnetization \(x\)/{flag=1;next}/tot /{if(flag){count++;flag=0}}END{print count}' OUTCAR)
m=$(awk '/magnetization \(x\)/{count=0;flag=1;next}/tot /{if(flag){print count;flag=0}}flag{count++}' OUTCAR | tail -n 1)
awk "/magnetization \(x\)/,/tot /" OUTCAR | tail -n $m