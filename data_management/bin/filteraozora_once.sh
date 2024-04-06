#!/bin/bash

# Command line options go here
#SBATCH --partition=g2
#SBATCH --time=06:00:00
#SBATCH --nodelist=mlpre-g2-ghpc-9
#SBATCH --job-name=filter
#SBATCH --output=filter.out
#SBATCH --gpus-per-node=0
#SBATCH --cpus-per-task=12

# Command(s) goes here

python -m preprocessing.filtering --input_dir=/persistentshare/storage/team_nakamura/member/horie/dataset/mabiki_a \
    --output_dir=/persistentshare/storage/team_nakamura/member/horie/dataset