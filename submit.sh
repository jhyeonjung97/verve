#!/bin/sh
#SBATCH -J test
#SBATCH -t 00:10:00
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -A m2997
#SBATCH -q debug
#SBATCH -e STDERR.%j.err
#SBATCH -o STDOUT.%j.out

module load vasp-tpc/5.4.4-cpu

echo "import os" > run_vasp.py
echo "exitcode = os.system('srun -n 256 vasp_std')" >> run_vasp.py

export VASP_SCRIPT=./run_vasp.py
export VASP_PP_PATH=/global/cfs/cdirs/m2997/vasp-psp/pseudo54

python opt_bulk.py
