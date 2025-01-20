#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH -J 2d
#SBATCH -o out
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4500M
#SBATCH --array=0-9

############## REQUIRED MODULES ##############
module load intel
##############################################

NUM_STRUCTURES=$(($(ls -1 input_structures/*.gin | wc -l)/10))

func () {
    mkdir $1_temp
    cd $1_temp
    for i in $(seq 0 $NUM_STRUCTURES)
    do
        cp ../input_structures/"$((10*i + $1))".gin .
	srun --ntasks 18 --time=00:01:00 gulp "$((10*i + $1))"
	continue
    done
}

func "$SLURM_ARRAY_TASK_ID"


