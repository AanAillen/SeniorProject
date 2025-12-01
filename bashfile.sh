#!/bin/sh
#SBATCH -N 1
#SBATCH --mem=128G  # memory in Mb
#SBATCH --cpus-per-gpu=8
#SBATCH -p preempt
#SBATCH --gres=gpu:1
#SBATCH -t 24:00:00


module purge
module load singularity/3.6.1
module load cuda/11.0
module load cudnn/7.1
export SINGULARITY_BINDPATH="/path/to/work/directory/:/workdir"

singularity exec --nv --pwd /workdir/ /path/to/singularity.sif  \
python3 path/to/python/main.py​
