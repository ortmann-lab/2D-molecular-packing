#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH -J compare
#SBATCH -o out
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=20
#SBATCH --mem-per-cpu=4500M

############## REQUIRED MODULES ##############
module load intel
module load Python
##############################################

python compare.py


