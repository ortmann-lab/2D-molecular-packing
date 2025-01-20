#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH -J 2d
#SBATCH -o out
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=20
#SBATCH --mem-per-cpu=4500M

############## REQUIRED MODULES ##############
module load intel
##############################################

export OMP_NUM_THREADS=7

NUM_STRUCTURES=$(ls -1 *_dftb.gen | wc -l)

for i in $(seq 0 $NUM_STRUCTURES)
do
	mkdir "$i"
        cp "$i"_dftb.gen dftb_in.hsd "$i"
        cd "$i"
        cp "$i"_dftb.gen DFTB.gen
        srun --exclusive --ntasks 1 -c 7  dftb+ > DFTB_output
        cd ..
done



