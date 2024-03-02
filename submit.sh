#!/bin/sh
#SBATCH -J test
#SBATCH -t 12:00:00
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -A m2997
#SBATCH -q regular
#SBATCH -e STDERR.%j.log
#SBATCH -o stdout.%j.log

module purge
module load python/3.11 vasp-tpc/5.4.4-cpu

echo "import os" > run_vasp.py
echo "exitcode = os.system('srun -n 256 vasp_std')" >> run_vasp.py

export VASP_SCRIPT=./run_vasp.py
export VASP_PP_PATH=/global/cfs/cdirs/m2997/vasp-psp/pseudo54

python opt_bulk.py
