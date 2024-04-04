#!/bin/bash

# Command line options go here
#SBATCH --partition=g2
#SBATCH --time=06:00:00
#SBATCH --nodelist=mlpre-g2-ghpc-11
#SBATCH --job-name=train3
#SBATCH --output=train3.out
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=12

# Command(s) goes here
cd ~/ucllm_nedo_dev/train/scripts/step2_pretrain_model

bash ./gcp_node-1_gpu/dataset-merge_tokenizer-JINIAC_v0_2_model-gpt_0.1113B/zero-0_dp-1_pp-1_tp-1_flashattn2-on.sh \
    --input_tokenizer_file /persistentshare/storage/team_nakamura/member/horie/tokenizer/JINIAC_V0_2.model \
    --output_model_dir /persistentshare/storage/team_nakamura/member/horie/output/step2_pretrain_model/merge \
    --save_interval 100
