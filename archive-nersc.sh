#!/bin/bash
/usr/bin/rsync -e ssh --ignore-times --size-only -avlzp -K --max-size=50000m --min-size=1 \
	--include="*/" \
	--include="*.py" \
	--include="*.ipynb" \
	--include="*.sh" \
	--include="*.db" \
	--include="*.cif" \
	--include="*.pdf" \
	--include="*.png" \
	--include="*.dat" \
	--include="*.txt" \
	--include="*.out" \
	--include="*.xml" \
	--include="*.pckl" \
	--include="*.traj" \
	--include="*.json" \
	--include="*.log" \
	--include="*.tsv" \
	--include="*.csv" \
	--include="DONE" \
	--include="CONTCAR" \
	--include="INCAR" \
	--include="POTCAR" \
	--include="KPOINTS" \
	--include="OUTCAR" \
	--include="OSZICAR" \
	--exclude="*" $1 $2

cd $2
echo "Rsync of $1 completed"