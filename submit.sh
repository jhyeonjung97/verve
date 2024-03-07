#!/bin/bash
#SBATCH -N 1
#SBATCH -C gpu
#SBATCH -G 4
#SBATCH -q regular
#SBATCH -J octa-high-gpu
#SBATCH -t 12:00:00
#SBATCH -A m2997
#SBATCH -e err.%j.log
#SBATCH -o out.%j.log

#OpenMP settings:
export OMP_NUM_THREADS=1
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

module load vasp-tpc/6.3.2-gpu

echo "import os" > run_vasp.py
echo "exitcode = os.system('srun -n 4 -c 32 --cpu_bind=cores -G 4 --gpu-bind=none vasp_std')" >> run_vasp.py

export VASP_SCRIPT=./run_vasp.py
export VASP_PP_PATH=/global/cfs/cdirs/m2997/vasp-psp/pseudo54

python ~/bin/verve/opt_bulk3_afm_high.py
python ~/bin/verve/static_bulk.py
python ~/bin/verve/bader.py

~/bin/lobster-5.0.0/lobster-5.0.0
python ~/bin/playground/aloha/cohp.py > icohp.txt
python ~/bin/playground/aloha/cobi.py > icobi.txt
