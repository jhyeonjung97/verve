#!/bin/bash
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp 
	--include="*/" \
	--include="*.png" \
	--exclude="*" jiuy97@perlmutter.nersc.gov:/pscratch/sd/j/jiuy97/2_icohp/1_octahedron/1_high_spin/mag .