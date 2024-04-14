#!/bin/bash

# Command line options go here
#SBATCH --partition=g2
#SBATCH --time=06:00:00
#SBATCH --nodes=1
#SBATCH --job-name=vocab60000
#SBATCH --output=train.out
#SBATCH --gpus-per-node=2
#SBATCH --cpus-per-task=12

# Command(s) goes here
cd ~/ucllm_nedo_dev/train/scripts/step2_pretrain_model

bash ./gcp_node-2_gpu/tokenizer_test/vocab_60000.sh \
    --input_tokenizer_file /persistentshare/storage/team_nakamura/member/horie/tokenizer/JINIAC_V0_2_60000.model \
    --output_model_dir /persistentshare/storage/team_nakamura/member/horie/output/step2_pretrain_model/vocab60000 \
    --save_interval 100