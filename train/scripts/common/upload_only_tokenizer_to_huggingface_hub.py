import argparse
import os
import torch
from huggingface_hub import HfApi
from transformers import AutoTokenizer


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_tokenizer_dir", type=str, required=True)
    parser.add_argument("--output_model_name", type=str, required=True)
    args = parser.parse_args()
    print(f"{args = }")
    return args


def load_tokenizer(input_tokenizer_dir: str):
    tokenizer = AutoTokenizer.from_pretrained(input_tokenizer_dir)
    return tokenizer


def main() -> None:
    args = parse_arguments()

    # Loads and tests the local tokenizer and the local model.
    local_tokenizer = load_tokenizer(args.input_tokenizer_dir)

    # Uploads the local tokenizer and the local model to HuggingFace Hub.
    local_tokenizer.push_to_hub(args.output_model_name)

    # Loads and tests the remote tokenizer and the remote model.
    huggingface_username = HfApi().whoami()["name"]
    remote_tokenizer, remote_model = load_tokenizer(os.path.join(huggingface_username, args.output_model_name))


if __name__ == "__main__":
    main()
    