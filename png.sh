#!/bin/bash
/usr/bin/rsync -e 'ssh' --ignore-times --size-only -avlzp -K --max-size=50000m \
	--include="*/" \
	--include="*.png" \
	--exclude="*" \
 jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/3_V_shape .
